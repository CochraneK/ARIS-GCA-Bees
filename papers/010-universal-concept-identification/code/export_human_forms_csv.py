"""Export generated human calibration forms to platform-neutral CSV files."""

from __future__ import annotations

import csv
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
FORMS=ROOT/"data"/"human_forms"/"forms.generated.json"
OUT=ROOT/"data"/"human_forms"/"csv"


FIELDS=[
    "trial_number","form_id","protocol","base_form","source","pair_id","target_id",
    "group_id","lemma","target","definition","frozen_context_json","query_id",
    "query_text","query_kind","allowed_responses","is_retest"
]


def main():
    payload=json.loads(FORMS.read_text(encoding="utf-8"))
    OUT.mkdir(parents=True,exist_ok=True)
    index=[]

    for form in payload["forms"]:
        path=OUT/f"{form['form_id']}.csv"
        with path.open("w",encoding="utf-8",newline="") as fh:
            writer=csv.DictWriter(fh,fieldnames=FIELDS)
            writer.writeheader()
            for n,item in enumerate(form["items"],1):
                writer.writerow({
                    "trial_number":n,
                    "form_id":form["form_id"],
                    "protocol":form["protocol"],
                    "base_form":form["base_form"],
                    "source":item["source"],
                    "pair_id":item["pair_id"],
                    "target_id":item["target_id"],
                    "group_id":item.get("group_id"),
                    "lemma":item.get("lemma"),
                    "target":item.get("target"),
                    "definition":item.get("definition"),
                    "frozen_context_json":json.dumps(item.get("frozen_context"),ensure_ascii=False),
                    "query_id":item["query_id"],
                    "query_text":item["query_text"],
                    "query_kind":item["query_kind"],
                    "allowed_responses":"|".join(item["allowed_responses"]),
                    "is_retest":str(item["is_retest"]).lower(),
                })
        index.append({
            "form_id":form["form_id"],
            "protocol":form["protocol"],
            "base_form":form["base_form"],
            "csv_file":path.name,
            "presented_trials":len(form["items"])
        })

    with (OUT/"forms_index.csv").open("w",encoding="utf-8",newline="") as fh:
        writer=csv.DictWriter(fh,fieldnames=list(index[0]))
        writer.writeheader()
        writer.writerows(index)

    print("PASS form CSV export")
    print("form CSVs:",len(index))
    print("index rows:",len(index))


if __name__=="__main__":
    main()
