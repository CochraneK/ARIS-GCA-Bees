"""Build deterministic human-annotation packets from calibration60.

Input source records are OEWN-derived. This script does not infer answers.
It only pairs targets with a generic semantic query bank.

Outputs:
- full_matrix.generated.json: all 60 × 24 = 1440 target-query pairs
- calibration_subset.generated.json: 12 queries per target = 720 pairs
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DATA = ROOT / "data"
POOL = DATA / "calibration60" / "oewn_source_pool.generated.json"
QBANK = DATA / "calibration60" / "lexical_query_bank.v0.json"
FULL = DATA / "calibration60" / "full_matrix.generated.json"
SUBSET = DATA / "calibration60" / "calibration_subset.generated.json"


def pair_row(target, query):
    return {
        "pair_id": f"{target['source_record_id']}::{query['query_id']}",
        "target_id": target["source_record_id"],
        "group_id": target["group_id"],
        "lemma": target["lemma"],
        "sense_id": target["sense_id"],
        "synset_id": target["synset_id"],
        "definition": target["definition"],
        "query_id": query["query_id"],
        "query_text": query["text"],
        "query_kind": query["query_kind"],
        "protocols": ["P2", "P6"],
        "response": None,
        "confidence": None,
        "annotator_id": None,
        "adjudication_status": "unannotated",
    }


def main():
    pool = json.loads(POOL.read_text(encoding="utf-8"))
    qbank = json.loads(QBANK.read_text(encoding="utf-8"))
    targets = pool["records"]
    queries = qbank["questions"]

    assert len(targets) == 60
    assert len(queries) == 24

    full_rows = [pair_row(t, q) for t in targets for q in queries]

    groups = {name: i for i, name in enumerate(sorted({t["group_id"] for t in targets}))}
    subset_rows = []
    # Deterministic coverage design: 12 of 24 questions per target. Offsets depend
    # only on group and source selection rank, never on an expected semantic answer.
    for target in targets:
        offset = (groups[target["group_id"]] * 5 + target["selection_rank"] * 3) % len(queries)
        selected_indices = [(offset + 2 * k) % len(queries) for k in range(12)]
        # With an even query count and step 2, parity repeats; add one odd shift to
        # cover both halves while keeping exactly 12 unique indices.
        selected_indices = selected_indices[:6] + [((i + 1) % len(queries)) for i in selected_indices[:6]]
        assert len(set(selected_indices)) == 12
        for index in selected_indices:
            subset_rows.append(pair_row(target, queries[index]))

    qcounts = Counter(row["query_id"] for row in subset_rows)
    payload_common = {
        "source_pool": pool["dataset_id"],
        "query_bank": qbank["dataset_id"],
        "protocols": ["P2", "P6"],
        "gold_status": "unannotated",
        "warning": "Blank annotation packet. No response in this file is semantic ground truth.",
    }

    FULL.write_text(
        json.dumps({**payload_common, "pair_count": len(full_rows), "rows": full_rows}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    SUBSET.write_text(
        json.dumps(
            {
                **payload_common,
                "design": "12 generic queries per target; deterministic answer-blind selection",
                "pair_count": len(subset_rows),
                "query_exposure_counts": dict(sorted(qcounts.items())),
                "rows": subset_rows,
            },
            indent=2,
            ensure_ascii=False,
        ) + "\n",
        encoding="utf-8",
    )

    print("PASS annotation-packet build")
    print("full pairs:", len(full_rows))
    print("calibration pairs:", len(subset_rows))
    print("query exposure min/max:", min(qcounts.values()), max(qcounts.values()))


if __name__ == "__main__":
    main()
