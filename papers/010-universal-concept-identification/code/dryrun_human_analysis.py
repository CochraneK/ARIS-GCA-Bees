"""Synthetic dry-run for the human calibration analysis pipeline.

No generated response is evidence. This script exists only to catch plumbing
errors before real participant data are collected.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
FORMS=ROOT/"data"/"human_forms"/"forms.generated.json"


def h(text):
    return int(hashlib.sha256(text.encode()).hexdigest()[:8],16)


def main():
    payload=json.loads(FORMS.read_text(encoding="utf-8"))
    chosen=[
        next(f for f in payload["forms"] if f["form_id"]=="P2-F01"),
        next(f for f in payload["forms"] if f["form_id"]=="P2-F02"),
        next(f for f in payload["forms"] if f["form_id"]=="P6-F01"),
        next(f for f in payload["forms"] if f["form_id"]=="P6-F02"),
    ]
    rows=[]
    remembered={}
    for pi,form in enumerate(chosen,1):
        participant=f"SYNTH-{pi:02d}"
        for item in form["items"]:
            key=(participant,item["pair_id"])
            if item["is_retest"] and key in remembered:
                response=remembered[key]
            else:
                allowed=item["allowed_responses"]
                response=allowed[h(participant+item["pair_id"])%len(allowed)]
                if not item["is_retest"]:
                    remembered[key]=response
            rows.append({
                "participant_id":participant,
                "form_id":form["form_id"],
                "protocol":form["protocol"],
                "pair_id":item["pair_id"],
                "response":response,
                "is_retest":item["is_retest"],
                "confidence":0.5+(h(item["pair_id"])%50)/100,
                "response_time_ms":800+(h(participant+item["query_id"])%2200),
            })

    with tempfile.NamedTemporaryFile("w",suffix=".json",encoding="utf-8",delete=False) as tmp:
        json.dump(rows,tmp)
        path=tmp.name

    proc=subprocess.run(
        [sys.executable,str(HERE/"analyze_human_calibration.py"),path],
        text=True,capture_output=True,check=True
    )
    summary=json.loads(proc.stdout)
    assert summary["rows"]==len(rows)
    assert set(summary["protocols"])=={"P2","P6"}
    assert summary["retest"]["matched"]>0
    assert summary["retest"]["exact_consistency"]==1.0
    print("PASS synthetic human-analysis dry-run")
    print("rows:",summary["rows"])
    print("retest matched:",summary["retest"]["matched"])
    print("P2/P6 analyzed")


if __name__=="__main__":
    main()
