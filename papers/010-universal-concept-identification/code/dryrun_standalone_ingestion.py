"""End-to-end dry-run: standalone-style exports -> validated ingestion -> analysis.

Synthetic responses are plumbing tests only and carry no scientific meaning.
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


def fake_export(form, participant, out_path):
    rows=[]
    remembered={}
    for i,item in enumerate(form["items"],1):
        key=item["pair_id"]
        if item["is_retest"] and key in remembered:
            response=remembered[key]
        else:
            response=item["allowed_responses"][h(participant+key)%len(item["allowed_responses"])]
            if not item["is_retest"]:
                remembered[key]=response
        rows.append({
            "participant_id":participant,
            "form_id":form["form_id"],
            "protocol":form["protocol"],
            "trial_number":i,
            "pair_id":item["pair_id"],
            "source":item["source"],
            "target_id":item["target_id"],
            "query_id":item["query_id"],
            "response":response,
            "confidence":0.75,
            "response_time_ms":1000+(h(participant+item["query_id"])%1000),
            "occurrence_index":sum(r["pair_id"]==item["pair_id"] for r in rows)+1
        })
    payload={
        "study":"ARIS4C010-UCID-calibration",
        "form_id":form["form_id"],
        "protocol":form["protocol"],
        "participant_id":participant,
        "completed_at":"2099-01-01T00:00:00Z",
        "rows":rows
    }
    Path(out_path).write_text(json.dumps(payload),encoding="utf-8")


def main():
    forms=json.loads(FORMS.read_text(encoding="utf-8"))["forms"]
    selected=[
        next(f for f in forms if f["form_id"]=="P2-F01"),
        next(f for f in forms if f["form_id"]=="P3-F01"),
        next(f for f in forms if f["form_id"]=="P6-F01"),
    ]

    with tempfile.TemporaryDirectory() as td:
        td=Path(td)
        files=[]
        for i,form in enumerate(selected,1):
            path=td/f"response_{i}.json"
            fake_export(form,f"PIPE-{i:02d}",path)
            files.append(str(path))

        combined=td/"combined.json"
        ingest=subprocess.run(
            [sys.executable,str(HERE/"ingest_standalone_responses.py"),
             *files,"-o",str(combined)],
            text=True,capture_output=True,check=True
        )
        assert "PASS standalone response ingestion" in ingest.stdout

        proc=subprocess.run(
            [sys.executable,str(HERE/"analyze_human_calibration.py"),str(combined)],
            text=True,capture_output=True,check=True
        )
        summary=json.loads(proc.stdout)
        assert set(summary["protocols"])=={"P2","P3","P6"}
        assert summary["rows"]==3*92
        assert summary["retest"]["matched"]==3*8
        assert summary["retest"]["exact_consistency"]==1.0

        # Tampering check: alter one pair_id and make sure ingest rejects it.
        bad=json.loads(Path(files[0]).read_text(encoding="utf-8"))
        bad["rows"][0]["pair_id"]="tampered-pair"
        badfile=td/"tampered.json"
        badfile.write_text(json.dumps(bad),encoding="utf-8")
        rejected=subprocess.run(
            [sys.executable,str(HERE/"ingest_standalone_responses.py"),
             str(badfile),"-o",str(td/"badout.json")],
            text=True,capture_output=True
        )
        assert rejected.returncode!=0

    print("PASS end-to-end standalone ingestion dry-run")
    print("protocols: P2/P3/P6")
    print("synthetic participants: 3")
    print("retest matches: 24")
    print("tampered trial metadata rejected: yes")


if __name__=="__main__":
    main()
