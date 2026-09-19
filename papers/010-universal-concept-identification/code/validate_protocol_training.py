"""Validate protocol-training items and their separation from formal trials."""

from __future__ import annotations

import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
TRAINING=ROOT/"data"/"human_forms"/"protocol_training.v1.json"
FORMS=ROOT/"data"/"human_forms"/"forms.generated.json"

ALLOWED={
    "P2":{"YES","NO"},
    "P3":{"YES","NO","MAYBE"},
    "P6":{"YES","NO","BORDERLINE","UNKNOWN","UNDEFINED","BOTH"},
}


def main():
    training=json.loads(TRAINING.read_text(encoding="utf-8"))
    forms=json.loads(FORMS.read_text(encoding="utf-8"))["forms"]
    protocols=training["protocols"]

    assert set(protocols)==set(ALLOWED)

    practice_ids=[]
    for protocol,items in protocols.items():
        assert items, protocol
        for item in items:
            assert item["practice_id"] not in practice_ids
            practice_ids.append(item["practice_id"])
            assert item["correct"] in ALLOWED[protocol]
            assert item["target"].strip()
            assert item["query"].strip()
            assert item["explanation"].strip()

    assert {x["correct"] for x in protocols["P6"]}==ALLOWED["P6"]

    formal_pair_ids={item["pair_id"] for form in forms for item in form["items"]}
    formal_query_ids={item["query_id"] for form in forms for item in form["items"]}
    assert not (set(practice_ids)&formal_pair_ids)
    assert not (set(practice_ids)&formal_query_ids)

    print("PASS protocol training validation")
    print("practice items:",sum(len(v) for v in protocols.values()))
    print("P2/P3/P6:",*(len(protocols[p]) for p in ("P2","P3","P6")))
    print("P6 response-state coverage: complete")
    print("formal-trial ID overlap: none")


if __name__=="__main__":
    main()
