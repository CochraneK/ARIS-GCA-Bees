"""ARIS4C004 independent identity second review (AI reviewer, blind to review 1).

Inputs: the 40-case blind evidence packet built by build_second_review_packet.py
plus the frozen protocol/handoff. The model never receives
identity_decisions_100.csv or any exposure/mental-health material.
"""

from __future__ import annotations

import argparse
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
CODE_DIR = Path(__file__).resolve().parent
HERE = Path(os.environ.get("ARIS4C004_REVIEW_SCRATCH") or (CODE_DIR / "_second_review_scratch"))

_PAPER_DIR = os.environ.get("ARIS4C_PAPER_DIR")
PAPER = Path(_PAPER_DIR) if _PAPER_DIR else Path(__file__).resolve().parents[2]

STATES = [
    "VERIFIED_SINGLE",
    "VERIFIED_CLUSTER",
    "AMBIGUOUS_COLLISION",
    "NO_GRAPH_RECORD",
    "EXCLUDED_IDENTITY_ERROR",
]


def build_system():
    protocol = (PAPER / "process" / "IDENTITY_SECOND_REVIEW_PROTOCOL.md").read_text(encoding="utf-8")
    handoff = (PAPER / "process" / "IDENTITY_SECOND_REVIEW_HANDOFF.md").read_text(encoding="utf-8")
    return (
        "You are an INDEPENDENT identity second reviewer for ARIS4C004. You have no access to the "
        "first reviewer's verdicts and must not try to guess them. Work only from the evidence "
        "packet included in the user message (public OpenAlex, Wikidata and candidate-frame fields). "
        "Apply the frozen protocol and handoff below verbatim.\n\n"
        "For every case output exactly these JSON keys:\n"
        '  "person_id": string\n'
        f'  "second_review_status": one of {STATES}\n'
        '  "second_review_openalex_ids": semicolon-separated canonical Author IDs (e.g. A1234567890) '
        "for VERIFIED_SINGLE/VERIFIED_CLUSTER, otherwise empty string\n"
        '  "notes": string, <= 60 words, in the handoff Evidence/OpenAlex/Conflicts/Sources structure\n'
        '  "evidence_requests": array of strings naming additional OpenAlex Author IDs (A...) or exact '
        "author search strings you would need to resolve the case; empty array if none\n\n"
        "Reply with a single JSON object of the form {\"cases\": {...person_id: {...}}}. No prose.\n\n"
        "=== FROZEN PROTOCOL ===\n" + protocol
        + "\n\n=== FROZEN HANDOFF ===\n" + handoff
    )


def call(model, system, user, max_tokens=16000, attempts=6):
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
                return json.load(r)
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}"
            if e.code not in (408, 409, 425, 429, 500, 502, 503, 504):
                raise
        except Exception as e:  # noqa: BLE001
            last = f"{type(e).__name__} {e}"[:120]
        wait = min(120, 2 ** i * 4 + random.random() * 3)
        print(f"  retry {i+1} after {last} (sleep {wait:.0f}s)", flush=True)
        time.sleep(wait)
    raise RuntimeError(f"route {model} failed after {attempts} attempts ({last})")


def parse_cases(text, ids):
    """Return every requested case the model actually answered.

    Silent omission of trailing cases is common, so partial coverage is
    accepted here and re-requested by the caller instead of failing the batch.
    """
    text = re.sub(r"<think[^>]*>.*?</think>", "", text, flags=re.S | re.I)
    wanted = [j for j in ids]
    found: dict = {}
    for m in re.finditer(r"\{", text):
        depth = 0
        for i in range(m.start(), min(m.start() + 80000, len(text))):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    try:
                        obj = json.loads(text[m.start() : i + 1])
                    except Exception:  # noqa: BLE001
                        break
                    if isinstance(obj, dict):
                        obj = obj.get("cases", obj)
                        if isinstance(obj, dict) and all(not isinstance(v, dict) for v in obj.values()):
                            obj = {}
                    if isinstance(obj, dict):
                        for pid in wanted:
                            if pid not in found and isinstance(obj.get(pid), dict):
                                found[pid] = obj[pid]
                    break
        if len(found) == len(wanted):
            break
    return found


def sanitize(raw, pid):
    st = str(raw.get("second_review_status") or "").strip().upper().replace(" ", "_")
    given = st
    if st not in STATES:
        st = "AMBIGUOUS_COLLISION" if st == "" else st
    ids = str(raw.get("second_review_openalex_ids") or "")
    canon = re.findall(r"A\d{6,}", ids)
    if st not in ("VERIFIED_SINGLE", "VERIFIED_CLUSTER"):
        canon = []
    elif st == "VERIFIED_SINGLE" and len(canon) > 1:
        canon = canon[:1]
    return {
        "person_id": pid,
        "second_review_status": st,
        "second_review_openalex_ids": ";".join(dict.fromkeys(canon)),
        "notes": re.sub(r"\s+", " ", str(raw.get("notes") or ""))[:400],
        "status_as_returned": given,
        "evidence_requests": [
            str(x).strip() for x in (raw.get("evidence_requests") or [])[:3] if str(x).strip()
        ],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--packet", type=Path, default=HERE / "second_review_evidence_packet.jsonl")
    ap = ap.parse_args()
    model = ap.model

    packets = [json.loads(l) for l in open(ap.packet, encoding="utf-8") if l.strip()]
    ck = HERE / "second_review_checkpoint.json"
    log = HERE / "second_review_provenance.jsonl"
    done = json.load(open(ck, encoding="utf-8")) if ck.exists() else {}
    system = build_system()
    chunk = 4

    for round_no in (1, 2):
        for i in range(0, len(packets), chunk):
            batch = packets[i : i + chunk]
            ids = [p["person_id"] for p in batch]
            pending = [j for j in ids if j not in done]
            if not pending:
                continue
            if round_no == 2:
                pending = [j for j in pending if done_extra.get(j)]
            subset = [p for p in batch if p["person_id"] in pending]
            if not subset:
                continue
            # The model sometimes drops trailing cases without signalling it,
            # so re-request only the still-missing cases at shrinking width.
            queue = subset
            width = len(queue)
            for attempt in range(4):
                if not queue:
                    break
                if attempt:
                    width = max(1, min(width, 2))
                ask = queue[:width]
                user = "CASES:\n" + json.dumps(ask, ensure_ascii=False, indent=1)
                d = call(model, system, user)
                raw = d["choices"][0]["message"]["content"]
                obj = parse_cases(raw, [p["person_id"] for p in ask])
                with open(log, "a", encoding="utf-8") as fh:
                    fh.write(json.dumps({
                        "round": round_no, "attempt": attempt + 1, "requested_model": model,
                        "served_model": d.get("model"),
                        "person_ids": [p["person_id"] for p in ask],
                        "answered": sorted(obj), "temperature": 0, "created": int(time.time()),
                        "usage": d.get("usage"),
                        "messages_sha256": hashlib.sha256((system + user).encode()).hexdigest(),
                        "response_sha256": hashlib.sha256(raw.encode()).hexdigest(),
                    }) + "\n")
                for pid, val in obj.items():
                    done[pid] = sanitize(val, pid)
                json.dump(done, open(ck, "w", encoding="utf-8"), indent=1)
                print(f"round{round_no} attempt{attempt+1} answered {sorted(obj)}", flush=True)
                missing = [p["person_id"] for p in ask if p["person_id"] not in obj]
                queue = [p for p in queue if p["person_id"] not in obj]
                if missing and attempt == 0:
                    continue
                if not missing:
                    break
                time.sleep(2)
            still = [p["person_id"] for p in subset if p["person_id"] not in done]
            if still:
                print(f"  UNRESOLVED after retries: {still}", flush=True)
        if round_no == 1:
            done_extra = resolve_requests(done, packets)
            if not any(done_extra.values()):
                break
            # fresh packets enriched with the requested evidence, then round 2
            json.dump(done_extra, open(HERE / "extra_evidence.json", "w", encoding="utf-8"), indent=1)
            for p in packets:
                ex = done_extra.get(p["person_id"])
                if ex:
                    p["requested_extra_evidence"] = ex
                    p["first_pass_judgment_under_revision"] = {
                        k: v for k, v in done[p["person_id"]].items() if k != "evidence_requests"
                    }
                    done.pop(p["person_id"])

    missing = [p["person_id"] for p in packets if p["person_id"] not in done]
    print(f"complete={len(done)} missing={missing}")
    if missing:
        return
    src = PAPER / "data" / "derived" / "identity_second_review_blind_assignment.csv"
    with src.open(encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))
        header = list(rows[0])
    reviewer = f"AI:{model} (isolated second-review surface, temperature 0)"
    for r in rows:
        j = done[r["person_id"]]
        r["second_review_status"] = j["second_review_status"]
        r["second_review_openalex_ids"] = j["second_review_openalex_ids"]
        r["second_reviewer"] = reviewer
        r["mh_blinded_at_second_review"] = "true"
        r["second_review_date"] = time.strftime("%Y-%m-%d")
        note = j["notes"]
        if j["status_as_returned"] not in STATES:
            note = f"[status token normalized from {j['status_as_returned']!r}] " + note
        r["notes"] = note[:400]
    out = HERE / "identity_second_review_completed.csv"
    with out.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=header, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {out}")


def resolve_requests(done, packets):
    """Fetch OpenAlex evidence the reviewer asked for; returns {pid: extra evidence}."""
    sys.path.insert(0, str(CODE_DIR))
    import build_second_review_packet as B

    cache: dict = {}
    extra = {}
    by_id = {p["person_id"]: p for p in packets}
    for pid, j in done.items():
        reqs = [r for r in j.get("evidence_requests") or [] if r and r != pid]
        if not reqs:
            continue
        got = []
        for q in reqs[:3]:
            q = q.strip()
            try:
                if re.fullmatch(r"A\d{6,}", q):
                    prof = B.author_profile(q, cache)
                    if prof:
                        got.append({"requested": q, "author": prof})
                elif q:
                    res = B.oa("/authors", {"search": q, "per-page": 4, "select": B.AUTHOR_SELECT}, cache)
                    hits = [B.summarize_author(r, cache) for r in (res or {}).get("results", [])]
                    got.append({"requested_search": q, "hits": hits})
            except Exception as e:  # noqa: BLE001
                got.append({"requested": q, "error": str(e)[:80]})
        if got:
            extra[pid] = got
            print(f"  extra evidence for {pid}: {len(got)} retrieval(s)", flush=True)
    return extra


if __name__ == "__main__":
    main()
