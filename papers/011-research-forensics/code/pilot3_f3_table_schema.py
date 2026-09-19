#!/usr/bin/env python3
"""Content-only F3 table-schema detector for ARIS4C011 Pilot 3.

The detector receives only a SAFE_EXACT original-table object. It does not read
correction/retraction/outcome metadata. A flag is an anomaly requiring review,
not a misconduct judgment.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    obj=json.loads(a.input.read_text(encoding="utf-8"))
    if obj.get("outcome_or_correction_metadata_included") is not False:
        raise SystemExit("FAIL CLOSED: detector object contains outcome/correction metadata")
    if obj.get("safe_exact") is not True:
        raise SystemExit("FAIL CLOSED: object is not SAFE_EXACT")

    A=list(obj.get("section_A_observed_headers") or [])
    B=list(obj.get("section_B_observed_headers") or [])
    drop=max(0,len(A)-len(B))
    # General structural trigger: a named model subsection suddenly exposes at
    # least two fewer result columns than the preceding analysis subsection.
    flag=drop>=2
    result={
        "track":"A_CONTENT_ONLY",
        "detector_family":"F3",
        "detector_id":"F3_TABLE_SCHEMA_COLUMN_DROP_V1",
        "paper_id":obj["paper_id"],
        "object_label":obj["object_label"],
        "finding":"FLAG" if flag else "NO_FLAG",
        "flag_reason":"section-to-section result-schema column count drops by >=2" if flag else "no >=2-column structural drop",
        "section_A_header_n":len(A),
        "section_B_header_n":len(B),
        "header_count_drop":drop,
        "detector_visible_A_headers":A,
        "detector_visible_B_headers":B,
        "outcome_metadata_used":False,
        "correction_metadata_used":False,
        "misconduct_inference":False,
        "interpretation":"Structural anomaly only; FLAG requires evidence review and is not a fraud/misconduct claim.",
    }
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))

if __name__=="__main__": main()
