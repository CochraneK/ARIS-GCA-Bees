#!/usr/bin/env python3
"""Score N ARIS4C009 AI boundary-judge files.

Inputs are private. Outputs are aggregate and may be written to public-safe derived
locations after review. Agreement here is cross-model AI-judge agreement, not human
inter-rater reliability.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from itertools import combinations
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


def gwet_ac1_pair(a: list[str], b: list[str]) -> dict:
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


def gwet_ac1_multi(matrix: list[list[str]]) -> dict:
    rows = []
    for row in matrix:
        vals = [x.strip().lower() for x in row]
        if vals and all(vals):
            rows.append(vals)
    if not rows:
        return {"n": 0, "judges": 0, "agreement": None, "ac1": None}
    m = len(rows[0])
    if m < 2:
        raise ValueError("Need at least two judges")
    cats = sorted({x for row in rows for x in row})
    pair_total = m * (m - 1) / 2
    po_items = []
    for row in rows:
        counts = Counter(row)
        agreeing_pairs = sum(v * (v - 1) / 2 for v in counts.values())
        po_items.append(agreeing_pairs / pair_total)
    po = sum(po_items) / len(po_items)
    if len(cats) <= 1:
        pe = 0.0
    else:
        pooled = Counter(x for row in rows for x in row)
        denom = len(rows) * m
        ps = [pooled[c] / denom for c in cats]
        pe = sum(p * (1 - p) for p in ps) / (len(cats) - 1)
    ac1 = (po - pe) / (1 - pe) if pe < 1 else None
    return {
        "n": len(rows),
        "judges": m,
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


def unique_labels(paths: list[Path]) -> list[str]:
    labels, seen = [], Counter()
    for p in paths:
        base = p.stem
        seen[base] += 1
        labels.append(base if seen[base] == 1 else f"{base}_{seen[base]}")
    return labels


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--judge", action="append", required=True, help="Completed judge TSV; repeat >=2 times")
    ap.add_argument("--key", required=True)
    ap.add_argument("--json-out", required=True)
    ap.add_argument("--md-out", required=True)
    args = ap.parse_args()

    judge_paths = [Path(x) for x in args.judge]
    if len(judge_paths) < 2:
        raise ValueError("At least two judge files are required; >=3 materially different models are recommended")

    labels = unique_labels(judge_paths)
    judges = {label: load_tsv(path) for label, path in zip(labels, judge_paths)}
    key = json.loads(Path(args.key).read_text(encoding="utf-8"))

    common = set(key["items"])
    for rows in judges.values():
        common &= set(rows)
    regular = sorted(i for i in common if key["items"][i]["stratum"] == "regular")

    agreement = {}
    pairwise = {}
    for field in FIELDS:
        matrix = [[judges[label][i].get(field, "") for label in labels] for i in regular]
        agreement[field] = gwet_ac1_multi(matrix)
        pairwise[field] = {}
        for la, lb in combinations(labels, 2):
            pairwise[field][f"{la}__{lb}"] = gwet_ac1_pair(
                [judges[la][i].get(field, "") for i in regular],
                [judges[lb][i].get(field, "") for i in regular],
            )

    by_condition = defaultdict(lambda: {"n": 0, "judge_usable": Counter(), "majority_usable": 0, "unanimous_usable": 0})
    majority_n = len(labels) // 2 + 1
    for i in regular:
        cond = key["items"][i]["condition"]
        flags = {label: usable(judges[label][i]) for label in labels}
        d = by_condition[cond]
        d["n"] += 1
        for label, flag in flags.items():
            d["judge_usable"][label] += int(flag)
        n_usable = sum(flags.values())
        d["majority_usable"] += int(n_usable >= majority_n)
        d["unanimous_usable"] += int(n_usable == len(labels))

    condition_summary = {}
    for cond, d in sorted(by_condition.items()):
        n = d["n"]
        condition_summary[cond] = {
            "target_participant_words": key["condition_map"][cond],
            "n": n,
            "judge_usable_rate": {
                label: round(d["judge_usable"][label] / n, 4) if n else None for label in labels
            },
            "majority_usable_rate": round(d["majority_usable"] / n, 4) if n else None,
            "unanimous_usable_rate": round(d["unanimous_usable"] / n, 4) if n else None,
        }

    actions = {}
    for cond in sorted(by_condition):
        ids = [i for i in regular if key["items"][i]["condition"] == cond]
        actions[cond] = {
            label: dict(Counter(judges[label][i]["recommended_action"].strip().lower() for i in ids))
            for label in labels
        }

    result = {
        "judge_count": len(labels),
        "judge_labels": labels,
        "regular_items_scored": len(regular),
        "agreement": agreement,
        "pairwise_agreement": pairwise,
        "by_condition": condition_summary,
        "recommended_action_counts": actions,
        "interpretation_boundary": (
            "Automated engineering calibration only. Cross-model agreement is not human "
            "inter-rater reliability and does not establish clinical or phenomenological validity."
        ),
    }

    jout, mout = Path(args.json_out), Path(args.md_out)
    jout.parent.mkdir(parents=True, exist_ok=True)
    mout.parent.mkdir(parents=True, exist_ok=True)
    jout.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    strategy_header = "| Condition | Target words | N | " + " | ".join(labels) + " | Majority usable | Unanimous usable |"
    strategy_sep = "|---|---:|---:|" + "|".join(["---:"] * len(labels)) + "|---:|---:|"
    strategy_rows = []
    for cond, d in condition_summary.items():
        vals = [str(d["judge_usable_rate"][label]) for label in labels]
        strategy_rows.append(
            f"| {cond} | {d['target_participant_words']} | {d['n']} | "
            + " | ".join(vals)
            + f" | {d['majority_usable_rate']} | {d['unanimous_usable_rate']} |"
        )

    agr_rows = []
    for field, d in agreement.items():
        agr_rows.append(f"| {field} | {d['n']} | {d['judges']} | {d['agreement']} | {d['ac1']} |")

    pair_rows = []
    for field, pairs in pairwise.items():
        for pair, d in pairs.items():
            pair_rows.append(f"| {field} | {pair} | {d['n']} | {d['agreement']} | {d['ac1']} |")

    md = f"""# ARIS4C009 · AI boundary calibration summary

## Strategy usability

{strategy_header}
{strategy_sep}
{chr(10).join(strategy_rows)}

## Multi-model agreement

| Field | N | Judges | Percent agreement | Gwet AC1 |
|---|---:|---:|---:|---:|
{chr(10).join(agr_rows)}

## Pairwise model agreement

| Field | Judge pair | N | Percent agreement | Gwet AC1 |
|---|---|---:|---:|---:|
{chr(10).join(pair_rows)}

## Interpretation boundary

This is an automated engineering boundary-calibration result only. It does not establish
human interpretability, clinician agreement, phenomenological validity, disease effects,
or fidelity of any downstream representation.
"""
    mout.write_text(md, encoding="utf-8")


if __name__ == "__main__":
    main()
