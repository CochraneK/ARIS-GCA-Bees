#!/usr/bin/env python3
"""F1 significance-claim / p-direction consistency check.

This detector is intentionally narrow. It flags a textual assertion of a
statistically significant increase/decrease when the same sentence reports
p > .05. It does not infer misconduct or scientific intent.
"""
from __future__ import annotations
import argparse,json,re
from pathlib import Path

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    obj=json.loads(a.input.read_text())
    if obj.get("safe_exact") is not True:
        raise SystemExit("FAIL CLOSED: input is not SAFE_EXACT")
    if obj.get("outcome_or_correction_metadata_included") is not False:
        raise SystemExit("FAIL CLOSED: outcome metadata visible")
    text=obj.get("text") or ""
    significance=bool(re.search(r"\bsignificant(?:ly)?\b|\bsignificant\s+(?:increase|decrease)s?\b",text,re.I))
    p_gt=bool(re.search(r"p\s*>\s*(?:0?\.0*5|\.0*5)",text,re.I))
    finding="FLAG" if significance and p_gt else "NO_FLAG"
    out={
        "track":"A_CONTENT_ONLY",
        "detector_family":"F1",
        "detector_id":"F1_SIGNIFICANCE_P_DIRECTION_V1",
        "paper_id":obj["paper_id"],
        "finding":finding,
        "significance_claim_detected":significance,
        "p_greater_than_005_detected":p_gt,
        "detector_visible_text":text,
        "outcome_metadata_used":False,
        "correction_metadata_used":False,
        "misconduct_inference":False,
        "interpretation":"Internal statistical-reporting inconsistency only; FLAG is not a misconduct judgment.",
    }
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2))
if __name__=="__main__": main()
