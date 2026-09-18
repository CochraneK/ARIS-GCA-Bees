"""Build balanced participant forms for UCID human calibration.

Inputs are blank calibration packets generated earlier in CI.
Primary comparison: P2 versus P6.

One complete cycle:
- 36 base forms
- duplicated across P2 and P6 => 72 participant forms
- each main form: 60 lexical + 24 mixed-stress = 84 unique main trials
- plus 8 within-rater retest trials = 92 presented trials

This script does not estimate a required sample size. It only supplies a balanced
assignment structure that can be replicated for additional participants.
"""

from __future__ import annotations

import hashlib
import json
import random
from collections import Counter, defaultdict
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
DATA=ROOT/"data"
LEX=DATA/"calibration60"/"calibration_subset.generated.json"
MIX=DATA/"mixed_calibration"/"annotation_packet.generated.json"
OUT=DATA/"human_forms"/"forms.generated.json"


def slot_partition(rows, group_key, expected_per_group):
    grouped=defaultdict(list)
    for row in rows:
        grouped[row[group_key]].append(row)
    for key in grouped:
        grouped[key].sort(key=lambda r:r["query_id"])
        if len(grouped[key])!=expected_per_group:
            raise RuntimeError(f"{key}: expected {expected_per_group}, got {len(grouped[key])}")
    slots=[[] for _ in range(expected_per_group)]
    for key in sorted(grouped):
        for idx,row in enumerate(grouped[key]):
            slots[idx].append(row)
    return slots


def stable_seed(text):
    return int(hashlib.sha256(text.encode()).hexdigest()[:16],16)


def compact(row, source, protocol, retest=False):
    return {
        "source":source,
        "pair_id":row["pair_id"],
        "target_id":row.get("target_id") or row.get("scenario_id"),
        "group_id":row.get("group_id"),
        "lemma":row.get("lemma"),
        "target":row.get("target"),
        "definition":row.get("definition") or row.get("operational_definition"),
        "frozen_context":row.get("frozen_context"),
        "query_id":row["query_id"],
        "query_text":row["query_text"],
        "query_kind":row["query_kind"],
        "protocol":protocol,
        "allowed_responses":["YES","NO"] if protocol=="P2" else
            ["YES","NO","BORDERLINE","UNKNOWN","UNDEFINED","BOTH"],
        "is_retest":retest,
    }


def main():
    lex=json.loads(LEX.read_text(encoding="utf-8"))
    mix=json.loads(MIX.read_text(encoding="utf-8"))

    lex_slots=slot_partition(lex["rows"],"target_id",12)
    mix_slots=slot_partition(mix["rows"],"scenario_id",9)

    assert all(len(slot)==60 for slot in lex_slots)
    assert all(len(slot)==24 for slot in mix_slots)

    forms=[]
    main_exposure={"P2":Counter(),"P6":Counter()}
    retest_exposure={"P2":Counter(),"P6":Counter()}

    for protocol in ("P2","P6"):
        for base in range(36):
            lex_slot=base%12
            mix_slot=base%9
            main=[
                *[compact(r,"lexical",protocol) for r in lex_slots[lex_slot]],
                *[compact(r,"mixed_stress",protocol) for r in mix_slots[mix_slot]],
            ]
            assert len(main)==84
            assert len({r["pair_id"] for r in main})==84

            for item in main:
                main_exposure[protocol][item["pair_id"]]+=1

            # Four lexical + four stress retests, chosen deterministically.
            rng=random.Random(stable_seed(f"{protocol}:{base}:retest"))
            lex_candidates=[i for i in main if i["source"]=="lexical"]
            mix_candidates=[i for i in main if i["source"]=="mixed_stress"]
            repeats=rng.sample(lex_candidates,4)+rng.sample(mix_candidates,4)
            retests=[{**x,"is_retest":True} for x in repeats]
            for item in retests:
                retest_exposure[protocol][item["pair_id"]]+=1

            presented=[*main,*retests]
            rng=random.Random(stable_seed(f"{protocol}:{base}:order"))
            rng.shuffle(presented)

            # Avoid an immediate duplicate where possible.
            for i in range(1,len(presented)):
                if presented[i]["pair_id"]==presented[i-1]["pair_id"]:
                    swap=next((j for j in range(i+1,len(presented))
                               if presented[j]["pair_id"]!=presented[i-1]["pair_id"]),None)
                    if swap is not None:
                        presented[i],presented[swap]=presented[swap],presented[i]

            forms.append({
                "form_id":f"{protocol}-F{base+1:02d}",
                "protocol":protocol,
                "base_form":base+1,
                "lexical_slot":lex_slot+1,
                "mixed_slot":mix_slot+1,
                "main_trial_count":84,
                "retest_trial_count":8,
                "presented_trial_count":92,
                "items":presented,
            })

    # Balance guarantees for one full 36-form cycle per protocol.
    for protocol in ("P2","P6"):
        lex_counts=[count for pid,count in main_exposure[protocol].items()
                    if pid.startswith("oewn2025:")]
        mix_counts=[count for pid,count in main_exposure[protocol].items()
                    if not pid.startswith("oewn2025:")]
        assert set(lex_counts)=={3}, set(lex_counts)
        assert set(mix_counts)=={4}, set(mix_counts)

    payload={
        "dataset_id":"ucid-human-calibration-forms-v0",
        "design":"36 balanced base forms duplicated across P2/P6",
        "protocols":["P2","P6"],
        "base_forms_per_protocol":36,
        "total_forms":72,
        "trials_per_form":{"main":84,"retest":8,"presented":92},
        "one_cycle_participant_count_if_one_participant_per_form":72,
        "sample_size_warning":"72 is a balanced-design cycle, not a powered sample-size recommendation. Replicate form cycles as required by the precision/power plan.",
        "main_pair_exposure_per_protocol":{
            "lexical":3,
            "mixed_stress":4
        },
        "forms":forms
    }
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(payload,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")

    print("PASS human form build")
    print("forms:",len(forms))
    print("trials/form: 92 (84 main + 8 retest)")
    print("lexical main exposure/pair/protocol: 3")
    print("mixed main exposure/pair/protocol: 4")


if __name__=="__main__":
    main()
