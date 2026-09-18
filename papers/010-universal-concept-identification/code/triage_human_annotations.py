"""Triage UCID human annotations for additional rating or adjudication.

This tool intentionally does NOT promote majority votes to gold. It produces a
review queue based on response concentration and sample size.
"""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter, defaultdict
from pathlib import Path


def load_rows(path):
    text=Path(path).read_text(encoding="utf-8").strip()
    if text.startswith("["):
        return json.loads(text)
    obj=json.loads(text)
    return obj["rows"] if isinstance(obj,dict) and "rows" in obj else [obj]


def entropy_bits(counts):
    n=sum(counts.values())
    if not n:
        return 0.0
    return -sum((c/n)*math.log2(c/n) for c in counts.values() if c)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("responses")
    ap.add_argument("--min-ratings",type=int,default=6)
    ap.add_argument("--dominance",type=float,default=0.70)
    ap.add_argument("--entropy",type=float,default=1.20)
    args=ap.parse_args()

    rows=[r for r in load_rows(args.responses) if not r.get("is_retest",False)]
    groups=defaultdict(list)
    for r in rows:
        groups[(r["protocol"],r["pair_id"])].append(r)

    queue=[]
    stable=[]
    for (protocol,pair_id),items in sorted(groups.items()):
        counts=Counter(r["response"] for r in items)
        n=sum(counts.values())
        top_label,top_count=counts.most_common(1)[0]
        dominance=top_count/n
        ent=entropy_bits(counts)
        reasons=[]
        if n<args.min_ratings:
            reasons.append("insufficient_ratings")
        if dominance<args.dominance:
            reasons.append("low_dominance")
        if ent>args.entropy:
            reasons.append("high_entropy")
        record={
            "protocol":protocol,
            "pair_id":pair_id,
            "n":n,
            "response_counts":dict(counts),
            "modal_response":top_label,
            "dominance":dominance,
            "entropy_bits":ent,
            "reasons":reasons,
            "status":"review" if reasons else "stable_for_next_gate"
        }
        (queue if reasons else stable).append(record)

    result={
        "thresholds":{
            "min_ratings":args.min_ratings,
            "dominance":args.dominance,
            "entropy_bits":args.entropy
        },
        "pair_protocol_cells":len(groups),
        "stable_count":len(stable),
        "review_count":len(queue),
        "stable":stable,
        "review_queue":queue,
        "warning":"stable_for_next_gate is not equivalent to adjudicated_gold."
    }
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=="__main__":
    main()
