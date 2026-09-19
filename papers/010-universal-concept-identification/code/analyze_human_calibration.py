"""Summarize UCID human calibration responses.

Input: JSONL or JSON array of completed trial records with at least:
participant_id, form_id, protocol, pair_id, response, is_retest.
Optional: confidence, response_time_ms.

This is a dependency-free descriptive analysis layer. Confirmatory modeling is
specified separately and should be frozen before test data are analyzed.
"""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

P2={"YES","NO"}
P3={"YES","NO","MAYBE"}
P6={"YES","NO","BORDERLINE","UNKNOWN","UNDEFINED","BOTH"}


def load_rows(path):
    text=Path(path).read_text(encoding="utf-8").strip()
    if not text:
        return []
    if text.startswith("["):
        return json.loads(text)
    obj=json.loads(text) if text.startswith("{") and "\n" not in text else None
    if isinstance(obj,dict) and "rows" in obj:
        return obj["rows"]
    return [json.loads(line) for line in text.splitlines() if line.strip()]


def entropy(counts):
    n=sum(counts.values())
    if not n:
        return 0.0
    return -sum((c/n)*math.log2(c/n) for c in counts.values() if c)


def pair_agreement(responses):
    n=len(responses)
    if n<2:
        return None
    counts=Counter(responses)
    agreeing=sum(c*(c-1)//2 for c in counts.values())
    return agreeing/(n*(n-1)//2)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("responses")
    args=ap.parse_args()
    rows=load_rows(args.responses)
    if not rows:
        raise SystemExit("No responses")

    invalid=[]
    for r in rows:
        allowed={"P2":P2,"P3":P3,"P6":P6}.get(r["protocol"])
        if allowed is None:
            invalid.append((r.get("participant_id"), r["pair_id"], "unknown protocol " + str(r.get("protocol"))))
            continue
        if r["response"] not in allowed:
            invalid.append((r.get("participant_id"),r["pair_id"],r["response"]))
    if invalid:
        raise SystemExit(f"Invalid response values, first examples: {invalid[:5]}")

    main_rows=[r for r in rows if not r.get("is_retest",False)]
    retest_rows=[r for r in rows if r.get("is_retest",False)]

    by_protocol=defaultdict(list)
    for r in main_rows:
        by_protocol[r["protocol"]].append(r)

    result={"rows":len(rows),"main_rows":len(main_rows),"retest_rows":len(retest_rows),"protocols":{}}
    for protocol,prows in sorted(by_protocol.items()):
        counts=Counter(r["response"] for r in prows)
        by_pair=defaultdict(list)
        for r in prows:
            by_pair[r["pair_id"]].append(r["response"])
        agreements=[a for vals in by_pair.values() if (a:=pair_agreement(vals)) is not None]
        result["protocols"][protocol]={
            "n":len(prows),
            "response_counts":dict(counts),
            "escape_rate":(
                0.0 if protocol=="P2" else
                counts.get("MAYBE",0)/len(prows) if protocol=="P3" else
                sum(counts.get(x,0) for x in ("BORDERLINE","UNKNOWN","UNDEFINED","BOTH"))/len(prows)
            ),
            "fine_grained_nonbinary_rate":(
                0.0 if protocol!="P6" else
                sum(counts.get(x,0) for x in ("BORDERLINE","UNKNOWN","UNDEFINED","BOTH"))/len(prows)
            ),
            "mean_pairwise_agreement":None if not agreements else sum(agreements)/len(agreements),
            "mean_pair_response_entropy_bits":
                sum(entropy(Counter(v)) for v in by_pair.values())/len(by_pair),
            "mean_confidence":(
                None if not [r.get("confidence") for r in prows if r.get("confidence") is not None]
                else sum(float(r["confidence"]) for r in prows if r.get("confidence") is not None)
                    /sum(r.get("confidence") is not None for r in prows)
            ),
            "mean_response_time_ms":(
                None if not [r.get("response_time_ms") for r in prows if r.get("response_time_ms") is not None]
                else sum(float(r["response_time_ms"]) for r in prows if r.get("response_time_ms") is not None)
                    /sum(r.get("response_time_ms") is not None for r in prows)
            )
        }

    # Retest consistency: match participant + pair between main and retest.
    first={}
    for r in main_rows:
        first[(r.get("participant_id"),r["pair_id"])]=r["response"]
    matched=0
    same=0
    for r in retest_rows:
        key=(r.get("participant_id"),r["pair_id"])
        if key in first:
            matched+=1
            same+=first[key]==r["response"]
    result["retest"]={
        "matched":matched,
        "exact_consistency":None if matched==0 else same/matched
    }

    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=="__main__":
    main()
