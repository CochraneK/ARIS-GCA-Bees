#!/usr/bin/env python3
"""Prioritize ARIS4C004 held-work audit rows without making work decisions.

This is a review-ordering tool only. It never assigns KEEP/EXCLUDE states and
never changes network_observable. Signals are intentionally interpretable and
derived only from pre-exposure identity/work metadata.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

RISK_NOTE_TOKENS = (
    "namesake",
    "mixed",
    "contamination",
    "work-filter",
    "dedup",
    "posthumous",
    "reprint",
    "fragment",
    "excluded",
)

CONTAINER_PATTERNS = (
    r"^front\s*matter$",
    r"^frontmatter$",
    r"^back\s*matter$",
    r"^contents?$",
    r"^table of contents$",
    r"^acknowledg(?:e)?ments?$",
    r"^index$",
    r"^preface$",
)

STOP = {
    "and","the","of","in","to","for","a","on","with","from","research",
    "studies","study","analysis","science","sciences","history"
}

def read_csv(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as h:
        return list(csv.DictReader(h))

def words(value: str):
    return {
        x for x in re.findall(r"[a-z0-9]+", (value or "").casefold())
        if len(x) >= 3 and x not in STOP
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--audit",type=Path,required=True)
    p.add_argument("--identities",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--summary-json",type=Path,required=True)
    a=p.parse_args()

    audit=read_csv(a.audit)
    ids={r["person_id"]:r for r in read_csv(a.identities)}

    # Build a weak lexical topic core only for review prioritization.
    topic_token_counts=defaultdict(Counter)
    for r in audit:
        for token in words(r.get("primary_topic_name","")):
            topic_token_counts[r["person_id"]][token]+=1

    out=[]
    for r in audit:
        identity=ids[r["person_id"]]
        score=0
        signals=[]

        notes=(identity.get("notes") or "").casefold()
        note_hits=sorted({t for t in RISK_NOTE_TOKENS if t in notes})
        if note_hits:
            score += 5
            signals.append("identity_note_risk:"+"|".join(note_hits))

        if identity.get("identity_status")=="VERIFIED_CLUSTER":
            score += 2
            signals.append("verified_cluster")

        source_ids=[x for x in (r.get("source_author_ids") or "").split(";") if x.strip()]
        if len(source_ids)>1:
            score += 2
            signals.append("multi_author_fragment_manifestation")

        try:
            year=int(r.get("publication_year") or 0)
            death=int(identity.get("death_year") or 0)
        except ValueError:
            year=death=0
        if year and death and year > death:
            score += 5
            signals.append(f"posthumous_year:+{year-death}")
        elif year and death and year >= death-1:
            score += 2
            signals.append("near_death_boundary")

        title=(r.get("title") or "").strip().casefold()
        if any(re.search(pat,title) for pat in CONTAINER_PATTERNS):
            score += 6
            signals.append("container_like_title")

        topic_tokens=words(r.get("primary_topic_name",""))
        core={t for t,n in topic_token_counts[r["person_id"]].items() if n>=2}
        if core and topic_tokens and not (core & topic_tokens):
            score += 1
            signals.append("lexical_topic_outlier_review_only")

        if r.get("sample_reason","").startswith("accepted_author_fragment:"):
            score += 1
            signals.append("fragment_anchor")

        tier="P1" if score>=7 else ("P2" if score>=4 else "P3")
        out.append({
            **r,
            "review_priority_score":score,
            "review_priority_tier":tier,
            "priority_signals":";".join(signals),
            "machine_verdict":"NONE",
            "auto_release_allowed":"false",
            "auto_exclusion_allowed":"false",
        })

    out.sort(key=lambda r:(-int(r["review_priority_score"]),r["person_id"],r["publication_year"],r["openalex_work_id"]))
    for i,r in enumerate(out,1):
        r["review_rank"]=i

    fields=["review_rank"]+[x for x in out[0].keys() if x!="review_rank"]
    a.output.parent.mkdir(parents=True,exist_ok=True)
    with a.output.open("w",encoding="utf-8",newline="") as h:
        w=csv.DictWriter(h,fieldnames=fields); w.writeheader(); w.writerows(out)

    people=defaultdict(list)
    for r in out:
        people[r["person_id"]].append(r)
    summary={
        "rows":len(out),
        "people":len(people),
        "priority_tiers":dict(Counter(r["review_priority_tier"] for r in out)),
        "people_with_P1":sum(any(x["review_priority_tier"]=="P1" for x in rr) for rr in people.values()),
        "machine_verdicts":dict(Counter(r["machine_verdict"] for r in out)),
        "auto_release_rows":sum(r["auto_release_allowed"]=="true" for r in out),
        "auto_exclusion_rows":sum(r["auto_exclusion_allowed"]=="true" for r in out),
        "mental_health_information_used":False,
        "interpretation":"Review ordering only. Scores/signals are not work-authorship decisions and cannot change network release state.",
    }
    a.summary_json.write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary,indent=2))

if __name__=="__main__":
    main()
