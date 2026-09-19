"""ARIS4C012 V2 independent coder runner (A2 / B2).

One process per coder: `python run_v2_coders.py A2` then `python run_v2_coders.py B2`.
Each coder has its own checkpoint and provenance file and never reads the other's.

Inputs are restricted to the frozen blind bundle:
  - process/SCHEMA_V2_FROZEN.md
  - data/v2_blind_amendment_02/common_evidence_packet_amendment_02.jsonl
  - data/v2_blind_amendment_02/A2_response_amendment_02.csv (field list only)
Nothing else from the repository is read into the model context.
"""

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
from pathlib import Path

BASE = os.environ["FREELLMAPI_BASE_URL"].rstrip("/")
KEY = os.environ["FREELLMAPI_API_KEY"]
_PAPER_DIR = os.environ.get("ARIS4C_PAPER_DIR")
PAPER = Path(_PAPER_DIR) if _PAPER_DIR else Path(__file__).resolve().parents[1]
OUTDIR = Path(
    os.environ.get("ARIS4C012_V2_CODING_SCRATCH") or (Path(__file__).resolve().parent / "_v2_coder_scratch")
)

PACKET = PAPER / "data" / "v2_blind_amendment_02" / "common_evidence_packet_amendment_02.jsonl"
SCHEMA = PAPER / "process" / "SCHEMA_V2_FROZEN.md"
FORM = PAPER / "data" / "v2_blind_amendment_02" / "A2_response_amendment_02.csv"

CODERS = {
    "A2": "nemotron-3-super-120b",
    "B2": "gpt-oss-120b",
}

TERNARY = {"yes", "no", "uncertain"}
BINARY = {"0", "1", "uncertain"}
VOCAB = {
    "opposition_valid": TERNARY,
    "oci_candidate": TERNARY,
    "evidence_strength": {"none", "weak", "moderate", "strong", "uncertain"},
    "result_direction": {
        "supports_reversal", "null", "opposes_reversal", "mixed",
        "formal_only", "not_tested", "uncertain",
    },
    "normative_valence": {
        "beneficial", "harmful", "mixed", "actor_dependent",
        "not_normatively_classified", "uncertain",
    },
}


def load_fields():
    with open(FORM, newline="", encoding="utf-8") as fh:
        header = next(csv.reader(fh))
    return header, [c for c in header if c not in ("record_id", "title", "coder_note")]


def build_prompt(records, schema_text, fields):
    system = (
        "You are an independent research screener. You are one of two coders who will never see each "
        "other's labels. Code every record using ONLY the evidence text supplied in this message and "
        "the frozen schema below. Never invent tokens. Use `uncertain` whenever the supplied evidence "
        "does not resolve a relevant axis; missing information is not `no` or `0`.\n\n"
        "Respond with a single JSON object and nothing else, of the form "
        '{"records": {"<sample_id>": {<field>: <token>, ...}, ...}}. '
        "Every sample_id in the records array must appear, and every object must contain exactly the "
        "field names listed plus an optional free-text `coder_note`. Each value must be one of that "
        "field's allowed tokens.\n\n"
        "ALLOWED TOKENS BY FIELD:\n"
    )
    for f in fields:
        if f in VOCAB:
            allowed = sorted(VOCAB[f])
        elif f.startswith(("rel_", "idx_", "mech_", "ev_")):
            allowed = sorted(BINARY)
        else:
            raise AssertionError(f"unknown scored field {f}")
        system += f"- {f}: {' | '.join(allowed)}\n"
    system += "\nFROZEN SCHEMA (verbatim):\n" + schema_text
    user = "RECORDS TO CODE (JSON array):\n" + json.dumps(records, ensure_ascii=False, indent=1)
    return system, user


def call(model, system, user, max_tokens=20000, attempts=12):
    body = json.dumps(
        {
            "model": model,
            "temperature": 0,
            "max_tokens": max_tokens,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        }
    ).encode()
    last = None
    for i in range(attempts):
        req = urllib.request.Request(
            BASE + "/chat/completions",
            data=body,
            headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(req, timeout=900) as r:
                d = json.load(r)
            return d
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}"
            if e.code not in (408, 409, 425, 429, 500, 502, 503, 504):
                raise
        except Exception as e:  # noqa: BLE001
            last = type(e).__name__
        time.sleep(min(240, 5 * (i + 1) + random.random() * 3))
    raise RuntimeError(f"route {model} failed after {attempts} attempts ({last})")


def extract_json(text, ids):
    """Return the first balanced JSON object whose keys cover every requested id.

    Reasoning models stream their chain of thought into `content`, sometimes
    quoting braces, so the naive first-brace scan is not usable.
    """
    text = re.sub(r"<think[^>]*>.*?</think>", "", text, flags=re.S | re.I)
    wanted = set(ids)
    for m in re.finditer(r"\{", text):
        depth = 0
        for i in range(m.start(), min(m.start() + 60000, len(text))):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    try:
                        obj = json.loads(text[m.start() : i + 1])
                    except Exception:  # noqa: BLE001
                        break
                    obj = obj.get("records", obj) if isinstance(obj, dict) else obj
                    if isinstance(obj, dict) and wanted <= set(obj):
                        return obj
                    break
    raise ValueError("no JSON object covering the requested sample_ids")


def normalize(obj, fields):
    out = {}
    for f in fields:
        v = obj.get(f)
        if v is None:
            v = "uncertain"
        v = str(v).strip()
        low = v.lower()
        alias = {"0": "0", "1": "1", "no": "no", "yes": "yes", "uncertain": "uncertain",
                 "false": "0", "true": "1", "n/a": "uncertain", "": "uncertain"}
        if f.startswith(("rel_", "idx_", "mech_", "ev_")):
            cand = alias.get(low, low)
            out[f] = cand if cand in BINARY else "uncertain"
        else:
            cand = low.replace(" ", "_").replace("-", "_")
            allowed = VOCAB[f]
            out[f] = cand if cand in allowed else "uncertain"
    note = str(obj.get("coder_note") or "").replace("\n", " ").strip()
    out["coder_note"] = note[:400]
    return out


def run(coder):
    OUTDIR.mkdir(parents=True, exist_ok=True)
    model = CODERS[coder]
    header, fields = load_fields()
    records = [json.loads(l) for l in open(PACKET, encoding="utf-8") if l.strip()]
    schema_text = open(SCHEMA, encoding="utf-8").read()
    ck_path = os.path.join(OUTDIR, f"{coder}_checkpoint.json")
    log_path = os.path.join(OUTDIR, f"{coder}_provenance.jsonl")
    done = json.load(open(ck_path, encoding="utf-8")) if os.path.exists(ck_path) else {}

    chunk = 3
    for i in range(0, len(records), chunk):
        batch = records[i : i + chunk]
        ids = [r["sample_id"] for r in batch]
        pending = [j for j in ids if j not in done]
        if not pending:
            continue
        for try_no in range(3):
            subset = [r for r in batch if r["sample_id"] in pending]
            system, user = build_prompt(subset, schema_text, fields)
            d = call(model, system, user)
            raw = d["choices"][0]["message"]["content"]
            obj = extract_json(raw, pending)
            with open(log_path, "a", encoding="utf-8") as fh:
                fh.write(json.dumps({
                    "coder": coder, "requested_model": model, "served_model": d.get("model"),
                    "sample_ids": pending, "temperature": 0, "created": int(time.time()),
                    "attempt": try_no + 1,
                    "usage": d.get("usage"), "messages_sha256":
                        hashlib.sha256((system + user).encode()).hexdigest(),
                    "response_sha256": hashlib.sha256(raw.encode()).hexdigest(),
                }) + "\n")
            for j in pending:
                if isinstance(obj, dict) and isinstance(obj.get(j), dict):
                    done[j] = normalize(obj[j], fields)
            json.dump(done, open(ck_path, "w", encoding="utf-8"), indent=1)
            pending = [j for j in ids if j not in done]
            if not pending:
                print(f"{coder} coded {ids}", flush=True)
                break
            print(f"{coder} retry {try_no+1} still missing {pending}", flush=True)
            time.sleep(3)
        time.sleep(2)

    missing = [r["sample_id"] for r in records if r["sample_id"] not in done]
    if missing:
        raise SystemExit(f"incomplete: {missing}")

    with open(os.path.join(OUTDIR, f"{coder}_completed.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(header)
        for r in records:
            c = done[r["sample_id"]]
            row = []
            for col in header:
                if col == "record_id":
                    row.append(r["sample_id"])
                elif col == "title":
                    row.append(r["title"])
                elif col == "coder_note":
                    row.append(c["coder_note"])
                else:
                    row.append(c[col])
            w.writerow(row)
    print(f"{coder}: wrote {coder}_completed.csv")


if __name__ == "__main__":
    run(sys.argv[1])
