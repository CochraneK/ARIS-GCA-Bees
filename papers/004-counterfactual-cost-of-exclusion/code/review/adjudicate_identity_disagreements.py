#!/usr/bin/env python3
"""ARIS4C004 evidence adjudication of the 23 second-review disagreements.

The frozen protocol forbids settling disagreements by model majority or
confidence score, so this surface is given BOTH verdicts plus the public
evidence packet and must argue from the evidence. Where the packet cannot
decide, it must say so and take the narrowing option, because the protocol's
stated goal is near-100% auditable precision rather than recall.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import random
import re
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
VERIFIED = {"VERIFIED_SINGLE", "VERIFIED_CLUSTER"}
THINK = re.compile("<" + "think[^>]*>.*?</" + "think" + ">", re.S | re.I)


def system_prompt():
    proto = (PAPER / "process" / "IDENTITY_SECOND_REVIEW_PROTOCOL.md").read_text(encoding="utf-8")
    code = (PAPER / "process" / "IDENTITY_CODEBOOK.md").read_text(encoding="utf-8")
    return (
        "You are the EVIDENCE ADJUDICATOR for ARIS4C004 identity resolution. Two prior "
        "reviews disagree on the cases below; you decide each one. You may not resolve a "
        "case by preferring one reviewer because of who they are, by counting votes, or by "
        "any confidence heuristic. Decide only from the public evidence in the packet.\n\n"
        "Hard rules from the frozen protocol and codebook:\n"
        f"1. Use exactly one of these final states: {', '.join(STATES)}.\n"
        "2. VERIFIED_SINGLE means exactly one Author ID; VERIFIED_CLUSTER means two or more; "
        "every other state means an empty Author-ID set.\n"
        "3. Author IDs must be copied verbatim from the packet (A followed by 6+ digits). "
        "Never invent an id that does not appear in the packet.\n"
        "4. Where the packet genuinely cannot decide, take the NARROWER option (drop the "
        "disputed fragment, or prefer AMBIGUOUS_COLLISION / NO_GRAPH_RECORD over a VERIFIED "
        "state) and set retrieval_needed to true. The protocol targets near-100% auditable "
        "precision for included identities, not sample size.\n"
        "5. Justify with named evidence: which identifier, work, date range, topic or "
        "institution supports the decision, and what the best argument for the other reading "
        "is. Do not restate a reviewer's conclusion as your reasoning.\n\n"
        'Reply with a single JSON object {"cases": {"<person_id>": {...}}} and no prose. '
        "Each case object must have exactly these keys:\n"
        '  "adjudicated_status": string\n'
        '  "adjudicated_ids": semicolon-separated Author IDs honoring rule 2\n'
        '  "evidence_for_first": string, <= 45 words\n'
        '  "evidence_for_second": string, <= 45 words\n'
        '  "deciding_evidence": string, <= 60 words\n'
        '  "retrieval_needed": true or false\n'
        '  "retrieval_spec": string naming what else is needed, or empty\n\n'
        "=== FROZEN PROTOCOL ===\n" + proto + "\n\n=== IDENTITY CODEBOOK ===\n" + code
    )


def call(model, system, user, max_tokens=16000, attempts=10):
    body = json.dumps({
        "model": model, "temperature": 0, "max_tokens": max_tokens,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
    }).encode()
    last = None
    for i in range(attempts):
        req = urllib.request.Request(
            BASE + "/chat/completions", data=body,
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
        wait = min(240, 5 * (i + 1) + random.random() * 3)
        print(f"  retry {i+1} after {last} (sleep {wait:.0f}s)", flush=True)
        time.sleep(wait)
    raise RuntimeError(f"route failed after {attempts} attempts ({last})")


def parse(text, want):
    """Every requested case the model actually answered, keyed by person_id."""
    text = THINK.sub("", text)
    found: dict = {}
    for m in re.finditer(r"\{", text):
        depth = 0
        for i in range(m.start(), min(m.start() + 120000, len(text))):
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
                        if isinstance(obj, dict) and all(
                            not isinstance(v, dict) for v in obj.values()
                        ):
                            obj = {}
                        if isinstance(obj, dict):
                            for pid in want:
                                if pid not in found and isinstance(obj.get(pid), dict):
                                    found[pid] = obj[pid]
                    break
        if len(found) == len(want):
            break
    return found


def sanitize(raw, pid, packet_ids: set[str]):
    st = str(raw.get("adjudicated_status") or "").strip().upper().replace(" ", "_")
    ids = [x for x in re.findall(r"A\d{6,}", str(raw.get("adjudicated_ids") or ""))]
    ids = [x for x in dict.fromkeys(ids) if x in packet_ids]
    rejected = [x for x in dict.fromkeys(re.findall(r"A\d{6,}", str(raw.get("adjudicated_ids") or "")))
                if x not in packet_ids]
    flag = ""
    if st not in STATES:
        flag = f"invalid status token {st!r}; narrowed to AMBIGUOUS_COLLISION"
        st = "AMBIGUOUS_COLLISION"
    if st == "VERIFIED_SINGLE" and len(ids) != 1:
        flag = (flag + "; " if flag else "") + f"VERIFIED_SINGLE with {len(ids)} ids; kept first"
        ids = ids[:1]
        if not ids:
            st = "AMBIGUOUS_COLLISION"
            flag += "; no packet-grounded id available, narrowed"
    if st == "VERIFIED_CLUSTER" and len(ids) < 2:
        flag = (flag + "; " if flag else "") + f"VERIFIED_CLUSTER with {len(ids)} ids"
        st = "VERIFIED_SINGLE" if ids else "AMBIGUOUS_COLLISION"
    if st not in VERIFIED:
        ids = []
    return {
        "person_id": pid,
        "adjudicated_status": st,
        "adjudicated_ids": ";".join(ids),
        "evidence_for_first": re.sub(r"\s+", " ", str(raw.get("evidence_for_first") or ""))[:300],
        "evidence_for_second": re.sub(r"\s+", " ", str(raw.get("evidence_for_second") or ""))[:300],
        "deciding_evidence": re.sub(r"\s+", " ", str(raw.get("deciding_evidence") or ""))[:400],
        "retrieval_needed": bool(raw.get("retrieval_needed")),
        "retrieval_spec": re.sub(r"\s+", " ", str(raw.get("retrieval_spec") or ""))[:250],
        "normalization_note": flag,
        "invented_ids_dropped": ";".join(rejected),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--chunk", type=int, default=3)
    a = ap.parse_args()

    dossier = list(csv.DictReader((HERE / "adjudication_dossier.csv").open(encoding="utf-8", newline="")))
    packets = {}
    for line in (HERE / "second_review_evidence_packet.jsonl").read_text(encoding="utf-8").splitlines():
        if line.strip():
            p = json.loads(line)
            packets[p["person_id"]] = p
    ck = HERE / "adjudication_checkpoint.json"
    log = HERE / "adjudication_provenance.jsonl"
    done = json.loads(ck.read_text(encoding="utf-8")) if ck.exists() else {}
    sys_txt = system_prompt()

    cases = []
    for d in dossier:
        p = packets.get(d["person_id"]) or {}
        blob = json.dumps(p, ensure_ascii=False)
        cases.append({
            "person_id": d["person_id"],
            "canonical_name": d["canonical_name"],
            "birth_year": d["birth_year"],
            "death_year": d["death_year"],
            "first_review": {
                "status": d["first_status"],
                "included_openalex_ids": [x for x in d["first_ids"].split(";") if x],
                "notes": d["first_notes"],
            },
            "second_review": {
                "status": d["second_status"],
                "included_openalex_ids": [x for x in d["second_ids"].split(";") if x],
                "notes": d["second_notes"],
            },
            "ids_only_in_first": [x for x in d["ids_only_first"].split(";") if x],
            "ids_only_in_second": [x for x in d["ids_only_second"].split(";") if x],
            "evidence_packet": p,
        })

    pending = [c for c in cases if c["person_id"] not in done]
    print(f"adjudicating {len(pending)} of {len(cases)} cases", flush=True)
    for i in range(0, len(pending), a.chunk):
        ask = pending[i : i + a.chunk]
        ids = [c["person_id"] for c in ask]
        got = {}
        queue = list(ask)
        for attempt in range(3):
            if not queue:
                break
            width = a.chunk if attempt == 0 else 1
            sub = queue[:width]
            user = "CASES:\n" + json.dumps(sub, ensure_ascii=False, indent=1)
            d = call(a.model, sys_txt, user)
            raw = d["choices"][0]["message"]["content"]
            obj = parse(raw, [c["person_id"] for c in sub])
            with log.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps({
                    "attempt": attempt + 1, "requested_model": a.model, "served_model": d.get("model"),
                    "person_ids": [c["person_id"] for c in sub], "answered": sorted(obj),
                    "temperature": 0, "created": int(time.time()), "usage": d.get("usage"),
                    "messages_sha256": hashlib.sha256((sys_txt + user).encode()).hexdigest(),
                    "response_sha256": hashlib.sha256(raw.encode()).hexdigest(),
                }) + "\n")
            for pid, val in obj.items():
                pkt = json.dumps(packets.get(pid, {}), ensure_ascii=False)
                got[pid] = sanitize(val, pid, set(re.findall(r"A\d{6,}", pkt)))
            queue = [c for c in queue if c["person_id"] not in obj]
            if not queue:
                break
            time.sleep(2)
        still = [c["person_id"] for c in ask if c["person_id"] not in got]
        if still:
            print(f"  UNRESOLVED after retries: {still}", flush=True)
        done.update(got)
        ck.write_text(json.dumps(done, indent=1, ensure_ascii=False), encoding="utf-8")
        print(f"adjudicated {sorted(got)}  ({len(done)}/{len(cases)})", flush=True)
        time.sleep(2)

    if len(done) < len(cases):
        print("incomplete; rerun to resume")
        return

    fields = [
        "person_id", "canonical_name", "first_status", "second_status", "adjudicated_status",
        "adjudicated_ids", "ids_only_in_first", "ids_only_in_second", "evidence_for_first",
        "evidence_for_second", "deciding_evidence", "retrieval_needed", "retrieval_spec",
        "normalization_note", "invented_ids_dropped", "adjudicator", "adjudicated_at",
    ]
    out = HERE / "identity_adjudication_completed.csv"
    today = time.strftime("%Y-%m-%d")
    with out.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        for c in cases:
            pid = c["person_id"]
            j = done[pid]
            w.writerow({
                "person_id": pid,
                "canonical_name": c["canonical_name"],
                "first_status": c["first_review"]["status"],
                "second_status": c["second_review"]["status"],
                "adjudicated_status": j["adjudicated_status"],
                "adjudicated_ids": j["adjudicated_ids"],
                "ids_only_in_first": ";".join(c["ids_only_in_first"]),
                "ids_only_in_second": ";".join(c["ids_only_in_second"]),
                "evidence_for_first": j["evidence_for_first"],
                "evidence_for_second": j["evidence_for_second"],
                "deciding_evidence": j["deciding_evidence"],
                "retrieval_needed": str(j["retrieval_needed"]).lower(),
                "retrieval_spec": j["retrieval_spec"],
                "normalization_note": j["normalization_note"],
                "invented_ids_dropped": j["invented_ids_dropped"],
                "adjudicator": f"AI:{a.model} (isolated adjudication surface, temperature 0)",
                "adjudicated_at": today,
            })
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
