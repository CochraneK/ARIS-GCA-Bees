#!/usr/bin/env python3
"""Score two ARIS4C009 boundary-calibration rating files.

Inputs are private. Outputs are aggregate and may be written to public-safe derived
locations after review.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


FIELDS = (
    "coherent_boundary",
    "sufficient_nontrivial",
    "mixed_unrelated_topics",
    "recommended_action",
)


def load_tsv(path: Path) -> dict[str, dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return {row["item_id"]: row for row in csv.DictReader(f, delimiter="\t")}


def gwet_ac1(a: list[str], b: list[str]) -> dict:
    pairs = [(x.strip().lower(), y.strip().lower()) for x, y in zip(a, b) if x.strip() and y.strip()]
    n = len(pairs)
    if n == 0:
        return {"n": 0, "agreement": None, "ac1": None}
    cats = sorted({x for pair in pairs for x in pair})
    po = sum(x == y for x, y in pairs) / n
    if len(cats) <= 1:
        pe = 0.0
    else:
        pooled = Counter()
        for x, y in pairs:
            pooled[x] += 1
            pooled[y] += 1
        ps = [pooled[c] / (2 * n) for c in cats]
        pe = sum(p * (1 - p) for p in ps) / (len(cats) - 1)
    ac1 = (po - pe) / (1 - pe) if pe < 1 else None
    return {
        "n": n,
        "agreement": round(po, 4),
        "ac1": None if ac1 is None else round(ac1, 4),
        "categories": cats,
    }


def usable(row: dict[str, str]) -> bool:
    return (
        row.get("coherent_boundary", "").strip().lower() == "yes"
        and row.get("sufficient_nontrivial", "").strip().lower() == "yes"
        and row.get("mixed_unrelated_topics", "").strip().lower() == "no"
        and row.get("recommended_action", "").strip().lower() == "keep"
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rater-a", required=True)
    ap.add_argument("--rater-b", required=True)
    ap.add_argument("--key", required=True)
    ap.add_argument("--json-out", required=True)
    ap.add_argument("--md-out", required=True)
    args = ap.parse_args()

    a = load_tsv(Path(args.rater_a))
    b = load_tsv(Path(args.rater_b))
    key = json.loads(Path(args.key).read_text(encoding="utf-8"))

    common = sorted(set(a) & set(b) & set(key["items"]))
    regular = [i for i in common if key["items"][i]["stratum"] == "regular"]

    agreement = {}
    for field in FIELDS:
        agreement[field] = gwet_ac1(
            [a[i].get(field, "") for i in regular],
            [b[i].get(field, "") for i in regular],
        )

    by_condition = defaultdict(lambda: {"n": 0, "a_usable": 0, "b_usable": 0, "both_usable": 0})
    for i in regular:
        cond = key["items"][i]["condition"]
        au, bu = usable(a[i]), usable(b[i])
        d = by_condition[cond]
        d["n"] += 1
        d["a_usable"] += int(au)
        d["b_usable"] += int(bu)
        d["both_usable"] += int(au and bu)

    condition_summary = {}
    for cond, d in sorted(by_condition.items()):
        target = key["condition_map"][cond]
        n = d["n"]
        condition_summary[cond] = {
            "target_participant_words": target,
            **d,
            "rater_a_usable_rate": round(d["a_usable"] / n, 4) if n else None,
            "rater_b_usable_rate": round(d["b_usable"] / n, 4) if n else None,
            "both_usable_rate": round(d["both_usable"] / n, 4) if n else None,
        }

    actions = {}
    for cond in sorted(by_condition):
        ids = [i for i in regular if key["items"][i]["condition"] == cond]
        actions[cond] = {
            "rater_a": dict(Counter(a[i]["recommended_action"].strip().lower() for i in ids)),
            "rater_b": dict(Counter(b[i]["recommended_action"].strip().lower() for i in ids)),
        }

    result = {
        "regular_items_scored": len(regular),
        "agreement": agreement,
        "by_condition": condition_summary,
        "recommended_action_counts": actions,
        "interpretation_boundary": (
            "Engineering calibration only; does not establish clinical or phenomenological validity."
        ),
    }

    jout, mout = Path(args.json_out), Path(args.md_out)
    jout.parent.mkdir(parents=True, exist_ok=True)
    mout.parent.mkdir(parents=True, exist_ok=True)
    jout.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    rows = []
    for cond, d in condition_summary.items():
        rows.append(
            f"| {cond} | {d['target_participant_words']} | {d['n']} | "
            f"{d['rater_a_usable_rate']} | {d['rater_b_usable_rate']} | {d['both_usable_rate']} |"
        )

    agr = []
    for field, d in agreement.items():
        agr.append(f"| {field} | {d['n']} | {d['agreement']} | {d['ac1']} |")

    md = f"""# ARIS4C009 · Boundary calibration summary

## Strategy usability

| Blinded condition | Target participant words | N | Rater A usable | Rater B usable | Both usable |
|---|---:|---:|---:|---:|---:|
{chr(10).join(rows)}

## Inter-rater agreement

| Field | N | Percent agreement | Gwet AC1 |
|---|---:|---:|---:|
{chr(10).join(agr)}

## Interpretation boundary

This is an engineering boundary-calibration result only. It does not establish
phenomenological validity, disease effects, or fidelity of any representation.
"""
    mout.write_text(md, encoding="utf-8")


if __name__ == "__main__":
    main()
