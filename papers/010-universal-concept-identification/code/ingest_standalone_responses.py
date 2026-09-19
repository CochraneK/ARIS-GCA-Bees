"""Validate and ingest standalone UCID response JSON files.

Participant-visible HTML intentionally omits internal design labels such as
is_retest. This researcher-side ingest step reconstructs those labels from the
canonical generated form, while rejecting altered or mismatched submissions.

Usage:
    python ingest_standalone_responses.py response1.json response2.json ... -o combined.json

The output is suitable for analyze_human_calibration.py.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FORMS = ROOT / "data" / "human_forms" / "forms.generated.json"
TRAINING = ROOT / "data" / "human_forms" / "protocol_training.v1.json"


def load_forms():
    payload=json.loads(FORMS.read_text(encoding="utf-8"))
    return {f["form_id"]:f for f in payload["forms"]}


def load_training():
    return json.loads(TRAINING.read_text(encoding="utf-8"))["protocols"]


def validate_training_attempts(path: Path, payload, protocol, training):
    expected=training[protocol]
    expected_by_id={x["practice_id"]:x for x in expected}
    attempts=payload.get("training_attempts")
    if not isinstance(attempts,list):
        raise ValueError(f"{path}: missing training_attempts")

    seen={pid:[] for pid in expected_by_id}
    allowed={
        "P2":{"YES","NO"},
        "P3":{"YES","NO","MAYBE"},
        "P6":{"YES","NO","BORDERLINE","UNKNOWN","UNDEFINED","BOTH"},
    }[protocol]

    normalized=[]
    for raw in attempts:
        pid=raw.get("practice_id")
        if pid not in expected_by_id:
            raise ValueError(f"{path}: unexpected practice_id {pid!r}")
        selected=raw.get("selected")
        if selected not in allowed:
            raise ValueError(f"{path}: invalid training response {selected!r}")
        correct=selected==expected_by_id[pid]["correct"]
        record={
            "practice_id":pid,
            "attempt":int(raw.get("attempt",len(seen[pid])+1)),
            "selected":selected,
            "correct":correct,
        }
        seen[pid].append(record)
        normalized.append(record)

    for pid,records in seen.items():
        if not records:
            raise ValueError(f"{path}: missing training item {pid}")
        if not records[-1]["correct"]:
            raise ValueError(f"{path}: training item {pid} not completed correctly")

    return {
        "attempts":normalized,
        "practice_items":len(expected),
        "training_attempt_count":len(normalized),
        "training_errors":sum(not x["correct"] for x in normalized),
        "training_completed":True,
    }


def ingest_file(path: Path, forms, training):
    payload=json.loads(path.read_text(encoding="utf-8"))
    required={"study","form_id","protocol","participant_id","rows"}
    missing=required-set(payload)
    if missing:
        raise ValueError(f"{path}: missing top-level fields {sorted(missing)}")
    if payload["study"]!="ARIS4C010-UCID-calibration":
        raise ValueError(f"{path}: unexpected study identifier")

    form_id=payload["form_id"]
    if form_id not in forms:
        raise ValueError(f"{path}: unknown form_id {form_id}")
    form=forms[form_id]
    if payload["protocol"]!=form["protocol"]:
        raise ValueError(f"{path}: protocol does not match canonical form")

    training_summary=validate_training_attempts(
        path,payload,form["protocol"],training
    )

    rows=payload["rows"]
    if len(rows)!=form["presented_trial_count"]:
        raise ValueError(
            f"{path}: expected {form['presented_trial_count']} rows, got {len(rows)}"
        )

    participant=str(payload["participant_id"]).strip()
    if not participant:
        raise ValueError(f"{path}: empty participant_id")

    out=[]
    for position,(row,item) in enumerate(zip(rows,form["items"]),1):
        if row.get("trial_number")!=position:
            raise ValueError(f"{path}: noncanonical trial_number at position {position}")
        for key in ("form_id","protocol","pair_id","target_id","query_id"):
            expected={
                "form_id":form_id,
                "protocol":form["protocol"],
                "pair_id":item["pair_id"],
                "target_id":item["target_id"],
                "query_id":item["query_id"],
            }[key]
            if row.get(key)!=expected:
                raise ValueError(
                    f"{path}: {key} mismatch at trial {position}: "
                    f"{row.get(key)!r} != {expected!r}"
                )

        allowed=set(item["allowed_responses"])
        response=row.get("response")
        if response not in allowed:
            raise ValueError(
                f"{path}: invalid response {response!r} for {form['protocol']} "
                f"at trial {position}"
            )

        confidence=row.get("confidence")
        if confidence is not None and not (0 <= float(confidence) <= 1):
            raise ValueError(f"{path}: confidence outside [0,1] at trial {position}")

        rt=row.get("response_time_ms")
        if rt is not None and float(rt)<0:
            raise ValueError(f"{path}: negative response time at trial {position}")

        out.append({
            "participant_id":participant,
            "session_completed_at":payload.get("completed_at"),
            "source_file":path.name,
            "form_id":form_id,
            "protocol":form["protocol"],
            "base_form":form["base_form"],
            "trial_number":position,
            "pair_id":item["pair_id"],
            "source":item["source"],
            "target_id":item["target_id"],
            "group_id":item.get("group_id"),
            "lemma":item.get("lemma"),
            "target":item.get("target"),
            "query_id":item["query_id"],
            "query_kind":item["query_kind"],
            "response":response,
            "confidence":confidence,
            "response_time_ms":rt,
            "is_retest":bool(item["is_retest"]),
        })
    return out, training_summary


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("responses",nargs="+")
    ap.add_argument("-o","--output",required=True)
    args=ap.parse_args()

    forms=load_forms()
    training=load_training()
    combined=[]
    sessions=[]
    seen_sessions=set()
    participant_protocol={}

    for raw in args.responses:
        path=Path(raw)
        rows,training_summary=ingest_file(path,forms,training)
        session=(rows[0]["participant_id"],rows[0]["form_id"])
        if session in seen_sessions:
            raise SystemExit(f"Duplicate participant/form session: {session}")
        seen_sessions.add(session)

        participant=rows[0]["participant_id"]
        protocol=rows[0]["protocol"]
        prior=participant_protocol.get(participant)
        if prior is not None and prior!=protocol:
            raise SystemExit(
                f"Participant {participant!r} appears in multiple protocols: "
                f"{prior}, {protocol}"
            )
        participant_protocol[participant]=protocol
        combined.extend(rows)
        sessions.append({
            "participant_id":participant,
            "form_id":rows[0]["form_id"],
            "protocol":protocol,
            **training_summary,
        })

    output={
        "dataset_id":"ucid-human-calibration-responses-ingested",
        "input_files":len(args.responses),
        "participants":len({r["participant_id"] for r in combined}),
        "sessions":sessions,
        "rows":combined,
        "warning":"Internal design labels are reconstructed from canonical forms; participant files are not trusted for trial metadata."
    }
    Path(args.output).write_text(
        json.dumps(output,indent=2,ensure_ascii=False)+"\n",
        encoding="utf-8"
    )
    print("PASS standalone response ingestion")
    print("files:",len(args.responses))
    print("participants:",output["participants"])
    print("rows:",len(combined))


if __name__=="__main__":
    main()
