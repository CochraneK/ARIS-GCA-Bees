#!/usr/bin/env python3
"""Run frozen ARIS4C009 boundary-judge items through independent AI judge models.

Each judge reads only its own shuffled packet file plus the frozen prompt. Model
outputs are written locally as completed judge TSVs; no interview text is logged.
Agreement computed downstream is cross-model AI-judge agreement, never human
inter-rater reliability.
"""

from __future__ import annotations

import argparse
import concurrent.futures as cf
import csv
import hashlib
import json
import os
import random
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

JSON_KEYS = (
    "coherent_boundary",
    "sufficient_nontrivial",
    "mixed_unrelated_topics",
    "recommended_action",
    "confidence_1_5",
    "notes",
)
ALLOWED = {
    "coherent_boundary": {"yes", "no"},
    "sufficient_nontrivial": {"yes", "no"},
    "mixed_unrelated_topics": {"yes", "no"},
    "recommended_action": {"keep", "merge", "split", "reject"},
}
BRACE = re.compile(r"\{.*\}", re.DOTALL)


def parse_judge_spec(spec: str) -> tuple[str, str]:
    src, _, model = spec.partition("=")
    if not model:
        raise argparse.ArgumentTypeError(f"--judge must look like judge_01=MODEL, got {spec!r}")
    return src.strip(), model.strip()


def extract_json(text: str) -> dict:
    match = BRACE.search(text or "")
    if not match:
        raise ValueError("no JSON object in response")
    obj = json.loads(match.group(0))
    if not isinstance(obj, dict):
        raise ValueError("response JSON is not an object")
    return obj


def normalize(obj: dict) -> dict[str, str]:
    out = {}
    for key in ("coherent_boundary", "sufficient_nontrivial", "mixed_unrelated_topics"):
        value = str(obj.get(key, "")).strip().lower().rstrip(".")
        if value not in ALLOWED[key]:
            raise ValueError(f"{key}={value!r} not allowed")
        out[key] = value
    action = str(obj.get("recommended_action", "")).strip().lower().rstrip(".")
    if action not in ALLOWED["recommended_action"]:
        raise ValueError(f"recommended_action={action!r} not allowed")
    out["recommended_action"] = action
    try:
        conf = int(str(obj.get("confidence_1_5")).strip())
    except (TypeError, ValueError):
        raise ValueError("confidence_1_5 is not an integer")
    if not 1 <= conf <= 5:
        raise ValueError(f"confidence_1_5={conf} out of range")
    out["confidence_1_5"] = str(conf)
    note = " ".join(str(obj.get("notes", "")).split())
    out["notes"] = note[:160]
    return out


def chat(base_url: str, api_key: str, model: str, system: str, user: str,
         temperature: float, max_tokens: int, timeout: int) -> tuple[dict, str]:
    body = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }).encode("utf-8")
    req = urllib.request.Request(
        base_url.rstrip("/") + "/chat/completions",
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    choice = payload["choices"][0]
    content = choice["message"]["content"] or ""
    return payload, content


def judge_item(base_url: str, api_key: str, model: str, system: str, item_text: str,
               temperature: float, max_tokens: int, timeout: int,
               attempts: int) -> tuple[dict, dict]:
    meta = {"model_echo": "", "retries": 0, "finish": ""}
    last_error = "unspecified"
    user = item_text + "\n\nReturn only one JSON object with exactly these keys: " \
        + ", ".join(JSON_KEYS) + "."
    for attempt in range(attempts):
        meta["retries"] = attempt
        try:
            payload, content = chat(base_url, api_key, model, system, user,
                                    temperature, max_tokens, timeout)
            meta["model_echo"] = payload.get("model", "")
            meta["finish"] = payload["choices"][0].get("finish_reason", "")
            verdict = normalize(extract_json(content))
            return verdict, meta
        except urllib.error.HTTPError as exc:
            last_error = f"HTTP {exc.code}"
            wait = (6.0 if exc.code in (408, 409, 429) or exc.code >= 500 else 1.5) * (attempt + 1)
        except (urllib.error.URLError, TimeoutError, OSError, ValueError, KeyError,
                json.JSONDecodeError) as exc:
            last_error = f"{type(exc).__name__}: {exc}"[:200]
            wait = 1.5 * (attempt + 1)
        if attempt + 1 < attempts:
            time.sleep(wait + random.uniform(0, 1.5))
    raise RuntimeError(last_error[:200])


def read_rows(path: Path) -> tuple[list[str], list[dict]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        return list(reader.fieldnames or []), list(reader)


def write_rows(path: Path, fields: list[str], rows: list[dict]) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fields, delimiter="\t", quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(rows)
    tmp.replace(path)


def rated(row: dict) -> bool:
    return all(str(row.get(k, "")).strip() for k in JSON_KEYS[:5])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--packet-dir", required=True)
    ap.add_argument("--prompt-file", required=True)
    ap.add_argument("--judge", action="append", required=True, type=parse_judge_spec,
                    help="packet stem=model, repeat once per judge")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--prefix", default="rated_", help="output filename prefix")
    ap.add_argument("--limit", type=int, default=0, help="rate only the first N items (smoke)")
    ap.add_argument("--concurrency", type=int, default=2)
    ap.add_argument("--temperature", type=float, default=0.0)
    ap.add_argument("--max-tokens", type=int, default=1500)
    ap.add_argument("--timeout", type=int, default=120)
    ap.add_argument("--attempts", type=int, default=6)
    ap.add_argument("--base-url-env", default="FREELLMAPI_BASE_URL")
    ap.add_argument("--api-key-env", default="FREELLMAPI_API_KEY")
    ap.add_argument("--data-handling", default="",
                    help="operator statement of the endpoint data-use/retention mode")
    args = ap.parse_args()

    base_url = os.environ.get(args.base_url_env, "")
    api_key = os.environ.get(args.api_key_env, "")
    if not base_url or not api_key:
        raise SystemExit(f"endpoint not configured: set {args.base_url_env} and {args.api_key_env}")

    packet = Path(args.packet_dir)
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    system = Path(args.prompt_file).read_text(encoding="utf-8")
    prompt_sha = hashlib.sha256(system.encode("utf-8")).hexdigest()

    run_manifest = {"prompt_file": str(args.prompt_file), "prompt_sha256": prompt_sha,
                    "endpoint_base_url": base_url, "data_handling": args.data_handling,
                    "temperature": args.temperature}
    failures = 0
    for stem, model in args.judge:
        src = packet / f"{stem}.tsv"
        dst = out / f"{args.prefix}{stem}__{model}.tsv"
        fields, rows = read_rows(src)
        if dst.exists():
            _, done_rows = read_rows(dst)
            done = {r["item_id"]: r for r in done_rows}
            for i, row in enumerate(rows):
                prev = done.get(row["item_id"])
                if prev and rated(prev):
                    rows[i] = {**row, **{k: prev[k] for k in JSON_KEYS}}

        todo = [r for r in rows if not rated(r)]
        if args.limit:
            todo = todo[: args.limit]
        print(f"[{stem}] model={model} items={len(rows)} to_rate={len(todo)}", flush=True)

        started = datetime.now(timezone.utc).isoformat(timespec="seconds")

        def work(row: dict, /) -> tuple[str, str, dict | str]:
            try:
                verdict, meta = judge_item(
                    base_url, api_key, model, system, row["interview_text"],
                    args.temperature, args.max_tokens, args.timeout, args.attempts)
                return row["item_id"], meta.get("model_echo", ""), verdict
            except RuntimeError as exc:
                return row["item_id"], "", f"{exc}"

        errors: dict[str, str] = {}
        echoes: set[str] = set()
        with cf.ThreadPoolExecutor(max_workers=args.concurrency) as pool:
            for idx, (item_id, echo, result) in enumerate(pool.map(work, todo), 1):
                if echo:
                    echoes.add(echo)
                if isinstance(result, str):
                    errors[item_id] = result
                    print(f"  !! {item_id} {result}", file=sys.stderr, flush=True)
                else:
                    for row in rows:
                        if row["item_id"] == item_id:
                            row.update(result)
                            break
                if idx % 5 == 0 or idx == len(todo):
                    write_rows(dst, fields, rows)
                    print(f"  [{stem}] {idx}/{len(todo)}", flush=True)

        write_rows(dst, fields, rows)
        complete = sum(rated(r) for r in rows)
        if errors:
            (out / f"{stem}__{model}.errors.json").write_text(
                json.dumps(errors, indent=2) + "\n", encoding="utf-8")
        failures += len(errors)
        entry = {
            "judge_file": dst.name,
            "packet_file": src.name,
            "provider": base_url,
            "model_family": model,
            "model_version": model,
            "endpoint_reported_models": sorted(echoes),
            "execution_date": started,
            "temperature_or_determinism": f"temperature={args.temperature}",
            "data_handling_mode": args.data_handling,
            "prompt_file": str(args.prompt_file),
            "items_total": len(rows),
            "items_rated": complete,
            "items_failed": len(errors),
        }
        (out / f"{stem}__{model}.manifest.json").write_text(
            json.dumps({**run_manifest, "judges": [entry]}, indent=2) + "\n",
            encoding="utf-8")
        print(f"[{stem}] rated {complete}/{len(rows)} -> {dst.name}", flush=True)

    if failures:
        print(f"FAILED {failures} item/judge calls; rerun to resume (fail-closed)")
        raise SystemExit(2)


if __name__ == "__main__":
    main()
