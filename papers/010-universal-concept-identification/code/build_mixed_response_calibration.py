"""Build the mixed response-state calibration packet.

This packet is intentionally NOT an identification benchmark. It calibrates
whether human annotators can distinguish NO / BORDERLINE / UNKNOWN / UNDEFINED /
BOTH / CONTEXT_REQUEST on controlled semantic stress scenarios.

No expected answer is stored.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
SRC=ROOT/"data"/"mixed_calibration"/"stress_scenarios.v1.json"
OUT=ROOT/"data"/"mixed_calibration"/"annotation_packet.generated.json"


def main():
    package=json.loads(SRC.read_text(encoding="utf-8"))
    scenarios=package["scenarios"]
    probes=package["generic_probes"]

    rows=[]
    for si,scenario in enumerate(scenarios):
        # 9 generic probes per scenario, selected answer-blind from scenario index.
        # Different scenarios rotate through the same fixed bank.
        chosen=[probes[(si+2*k)%len(probes)] for k in range(9)]
        for probe in chosen:
            rows.append({
                "pair_id":f"{scenario['scenario_id']}::{probe['query_id']}",
                "scenario_id":scenario["scenario_id"],
                "target":scenario["target"],
                "operational_definition":scenario["operational_definition"],
                "phenomenon_tags":scenario["phenomenon_tags"],
                "frozen_context":scenario["frozen_context"],
                "query_id":probe["query_id"],
                "query_text":probe["text"],
                "query_kind":probe["kind"],
                "protocols":["P2","P3","P6","P6_CONTEXT"],
                "response":None,
                "confidence":None,
                "response_time_ms":None,
                "annotator_id":None,
                "notes":None,
                "adjudication_status":"unannotated"
            })

    assert len(scenarios)==24
    assert len(probes)==18
    assert len(rows)==216
    assert len({r["pair_id"] for r in rows})==216

    exposures=Counter(r["query_id"] for r in rows)
    payload={
        "dataset_id":package["dataset_id"],
        "gold_status":"unannotated",
        "scenario_count":len(scenarios),
        "query_bank_size":len(probes),
        "pair_count":len(rows),
        "query_exposure_counts":dict(sorted(exposures.items())),
        "warning":"Blank calibration packet. Intended phenomenon tags are not gold response labels.",
        "rows":rows
    }
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(payload,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("PASS mixed response-state calibration build")
    print("scenarios:",len(scenarios))
    print("queries:",len(probes))
    print("pairs:",len(rows))
    print("exposure min/max:",min(exposures.values()),max(exposures.values()))


if __name__=="__main__":
    main()
