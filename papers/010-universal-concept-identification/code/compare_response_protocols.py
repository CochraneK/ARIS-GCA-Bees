"""Compare UCID P3 judgments with deterministically coarsened P6 judgments.

Input is an ingested human-response JSON/JSONL file accepted by
analyze_human_calibration.py.

This script is descriptive. It does not declare one protocol superior.
"""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

P3_STATES=("YES","NO","MAYBE")
P6_TO_P3={
    "YES":"YES",
    "NO":"NO",
    "BORDERLINE":"MAYBE",
    "UNKNOWN":"MAYBE",
    "UNDEFINED":"MAYBE",
    "BOTH":"MAYBE",
}


def load_rows(path):
    text=Path(path).read_text(encoding="utf-8").strip()
    if not text:
        return []
    try:
        obj=json.loads(text)
    except json.JSONDecodeError:
        return [json.loads(line) for line in text.splitlines() if line.strip()]
    if isinstance(obj,list):
        return obj
    if isinstance(obj,dict) and "rows" in obj:
        return obj["rows"]
    if isinstance(obj,dict):
        return [obj]
    raise ValueError("Unsupported JSON structure")


def distribution(values, states=P3_STATES):
    counts=Counter(values)
    n=sum(counts.values())
    if n==0:
        return None
    return [counts.get(s,0)/n for s in states]


def kl(p,q):
    out=0.0
    for x,y in zip(p,q):
        if x>0:
            if y<=0:
                return math.inf
            out+=x*math.log2(x/y)
    return out


def js_divergence(p,q):
    m=[(x+y)/2 for x,y in zip(p,q)]
    return 0.5*kl(p,m)+0.5*kl(q,m)


def total_variation(p,q):
    return 0.5*sum(abs(x-y) for x,y in zip(p,q))


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("responses")
    ap.add_argument("--min-ratings",type=int,default=3)
    args=ap.parse_args()

    rows=[r for r in load_rows(args.responses) if not r.get("is_retest",False)]
    by=defaultdict(lambda:{"P3":[],"P6":[]})
    p6_fine=Counter()

    for r in rows:
        protocol=r.get("protocol")
        if protocol=="P3":
            by[r["pair_id"]]["P3"].append(r["response"])
        elif protocol=="P6":
            resp=r["response"]
            if resp not in P6_TO_P3:
                raise ValueError(f"Unexpected P6 response: {resp}")
            by[r["pair_id"]]["P6"].append(P6_TO_P3[resp])
            if resp not in ("YES","NO"):
                p6_fine[resp]+=1

    pairs=[]
    for pair_id,cells in sorted(by.items()):
        if len(cells["P3"])<args.min_ratings or len(cells["P6"])<args.min_ratings:
            continue
        p=distribution(cells["P3"])
        q=distribution(cells["P6"])
        pairs.append({
            "pair_id":pair_id,
            "n_p3":len(cells["P3"]),
            "n_p6":len(cells["P6"]),
            "p3":{"YES":p[0],"NO":p[1],"MAYBE":p[2]},
            "p6_coarsened":{"YES":q[0],"NO":q[1],"MAYBE":q[2]},
            "js_divergence_bits":js_divergence(p,q),
            "total_variation":total_variation(p,q),
        })

    fine_total=sum(p6_fine.values())
    result={
        "min_ratings_per_protocol_pair":args.min_ratings,
        "comparable_pairs":len(pairs),
        "mean_js_divergence_bits":(
            None if not pairs else
            sum(x["js_divergence_bits"] for x in pairs)/len(pairs)
        ),
        "mean_total_variation":(
            None if not pairs else
            sum(x["total_variation"] for x in pairs)/len(pairs)
        ),
        "p6_fine_state_counts":dict(p6_fine),
        "p6_fine_state_distribution":(
            {} if fine_total==0 else
            {k:v/fine_total for k,v in sorted(p6_fine.items())}
        ),
        "pairs":pairs,
        "warning":"Descriptive protocol-comparison output; does not establish causal superiority."
    }
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=="__main__":
    main()
