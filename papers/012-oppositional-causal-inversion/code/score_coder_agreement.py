#!/usr/bin/env python3
"""Score independent Pilot 0 coder agreement for ARIS4C012.

The script is deterministic and does not adjudicate disagreements. It:
- aligns Coder A and B by record_id;
- checks that the blind B packet has the required fields completed;
- reports coverage, raw agreement, Cohen's kappa, and nominal
  Krippendorff alpha for prespecified categorical fields;
- writes a disagreement packet for later adjudication.

If Coder B is incomplete, the JSON status is BLOCKED_INCOMPLETE_CODER_B.
This is an intentional scientific gate, not an execution failure.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from typing import Iterable

CORE_FIELDS = [
    "opposition_valid",
    "oci_candidate",
    "primary_mechanism",
]

AGREEMENT_FIELDS = [
    "opposition_valid",
    "oci_candidate",
    "primary_mechanism",
    "actor_switch",
    "level_switch",
    "time_switch",
    "construct_switch",
    "environment_switch",
    "feedback",
    "nonlinearity",
    "selection_filtering",
    "power_asymmetry",
    "evidence_mode",
    "evidence_tier",
    "causal_claim_strength",
    "result_support",
]


def norm(value: str | None) -> str:
    return " ".join((value or "").strip().lower().split())


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def index_rows(rows: Iterable[dict[str, str]]) -> dict[str, dict[str, str]]:
    out = {}
    for row in rows:
        rid = (row.get("record_id") or "").strip()
        if not rid:
            continue
        if rid in out:
            raise ValueError(f"duplicate record_id: {rid}")
        out[rid] = row
    return out


def raw_agreement(pairs: list[tuple[str, str]]) -> float | None:
    if not pairs:
        return None
    return sum(a == b for a, b in pairs) / len(pairs)


def cohen_kappa(pairs: list[tuple[str, str]]) -> float | None:
    if not pairs:
        return None
    n = len(pairs)
    po = sum(a == b for a, b in pairs) / n
    ca = Counter(a for a, _ in pairs)
    cb = Counter(b for _, b in pairs)
    cats = set(ca) | set(cb)
    pe = sum((ca[c] / n) * (cb[c] / n) for c in cats)
    if pe == 1:
        return 1.0 if po == 1.0 else None
    return (po - pe) / (1 - pe)


def krippendorff_alpha_nominal(pairs: list[tuple[str, str]]) -> float | None:
    """Nominal alpha for two coders with pairwise-complete items."""
    if not pairs:
        return None

    # Observed disagreement: proportion of coder pairs that disagree.
    do = sum(a != b for a, b in pairs) / len(pairs)

    # Expected disagreement from pooled coder marginals without replacement.
    pooled = Counter()
    for a, b in pairs:
        pooled[a] += 1
        pooled[b] += 1
    total = sum(pooled.values())
    if total <= 1:
        return None
    agree_expected = sum(v * (v - 1) for v in pooled.values()) / (total * (total - 1))
    de = 1 - agree_expected
    if de == 0:
        return 1.0 if do == 0 else None
    return 1 - do / de


def field_pairs(
    a_rows: dict[str, dict[str, str]],
    b_rows: dict[str, dict[str, str]],
    field: str,
) -> tuple[list[tuple[str, str]], list[str]]:
    pairs = []
    missing = []
    for rid in sorted(set(a_rows) & set(b_rows)):
        av, bv = norm(a_rows[rid].get(field)), norm(b_rows[rid].get(field))
        if not av or not bv:
            missing.append(rid)
            continue
        pairs.append((av, bv))
    return pairs, missing


def completeness(
    b_rows: dict[str, dict[str, str]],
    expected_ids: set[str],
) -> dict:
    missing_records = sorted(expected_ids - set(b_rows))
    missing_core = {}
    for rid in sorted(expected_ids & set(b_rows)):
        miss = [f for f in CORE_FIELDS if not norm(b_rows[rid].get(f))]
        if miss:
            missing_core[rid] = miss
    return {
        "expected_records": len(expected_ids),
        "present_records": len(expected_ids & set(b_rows)),
        "missing_records": missing_records,
        "records_missing_core_fields": missing_core,
        "complete": not missing_records and not missing_core,
    }


def make_disagreements(
    a_rows: dict[str, dict[str, str]],
    b_rows: dict[str, dict[str, str]],
) -> list[dict[str, str]]:
    out = []
    for rid in sorted(set(a_rows) & set(b_rows)):
        for field in AGREEMENT_FIELDS:
            av = (a_rows[rid].get(field) or "").strip()
            bv = (b_rows[rid].get(field) or "").strip()
            if av and bv and norm(av) != norm(bv):
                out.append({
                    "record_id": rid,
                    "title": a_rows[rid].get("title", ""),
                    "field": field,
                    "coder_a": av,
                    "coder_b": bv,
                    "adjudicated_value": "",
                    "adjudication_rationale": "",
                })
    return out


def write_disagreements(path: Path, rows: list[dict[str, str]]) -> None:
    fields = [
        "record_id","title","field","coder_a","coder_b",
        "adjudicated_value","adjudication_rationale",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--coder-a", required=True)
    ap.add_argument("--coder-b", required=True)
    ap.add_argument("--summary", required=True)
    ap.add_argument("--disagreements", required=True)
    args = ap.parse_args()

    a = index_rows(read_csv(Path(args.coder_a)))
    b = index_rows(read_csv(Path(args.coder_b)))

    comp = completeness(b, set(a))
    result = {
        "classification": "INDEPENDENT_CODER_RELIABILITY",
        "coder_a_records": len(a),
        "coder_b_records": len(b),
        "completeness": comp,
        "fields": {},
    }

    for field in AGREEMENT_FIELDS:
        pairs, missing = field_pairs(a, b, field)
        result["fields"][field] = {
            "n_pairwise_complete": len(pairs),
            "n_missing_either": len(missing),
            "raw_agreement": raw_agreement(pairs),
            "cohen_kappa": cohen_kappa(pairs),
            "krippendorff_alpha_nominal": krippendorff_alpha_nominal(pairs),
        }

    if comp["complete"]:
        result["status"] = "READY_FOR_ADJUDICATION"
        key = {
            f: result["fields"][f]
            for f in ["opposition_valid", "oci_candidate", "primary_mechanism"]
        }
        result["key_gate_metrics"] = key
    else:
        result["status"] = "BLOCKED_INCOMPLETE_CODER_B"
        result["key_gate_metrics"] = {}

    disagreements = make_disagreements(a, b)
    result["disagreement_cells"] = len(disagreements)

    summary_path = Path(args.summary)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_disagreements(Path(args.disagreements), disagreements)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
