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
import statistics
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path


FIELDS = (
    "coherent_boundary",
    "sufficient_nontrivial",
    "mixed_unrelated_topics",
    "recommended_action",
)
# The judge answer that marks a window as failing that criterion.
FAILING_FLAGS = {
    "coherent_boundary": "no",
    "sufficient_nontrivial": "no",
    "mixed_unrelated_topics": "yes",
}


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


def condition_stats(
    items: list[str], labels: list[str], judges: dict, key: dict
) -> dict:
    """Per-strategy rates for one ensemble of judges (leave-one-out sensitivity reuses this)."""
    by_condition = defaultdict(
        lambda: {"n": 0, "judge_usable": Counter(), "judge_modified": Counter(),
                 "field_yes": defaultdict(Counter), "majority_usable": 0,
                 "unanimous_usable": 0, "majority_modified": 0, "unanimous_modified": 0,
                 "majority_flag": Counter()})
    majority_n = len(labels) // 2 + 1
    for i in items:
        cond = key["items"][i]["condition"]
        d = by_condition[cond]
        d["n"] += 1
        flags = [usable(judges[label][i]) for label in labels]
        modified = [
            judges[label][i]["recommended_action"].strip().lower() in {"merge", "split", "reject"}
            for label in labels
        ]
        for k, label in enumerate(labels):
            d["judge_usable"][label] += int(flags[k])
            d["judge_modified"][label] += int(modified[k])
            for field in FIELDS[:3]:
                d["field_yes"][field][label] += int(
                    judges[label][i].get(field, "").strip().lower() == "yes")
        for field, wanted in FAILING_FLAGS.items():
            d["majority_flag"][field] += int(
                sum(1 for label in labels
                    if judges[label][i].get(field, "").strip().lower() == wanted) >= majority_n)
        d["majority_usable"] += int(sum(flags) >= majority_n)
        d["unanimous_usable"] += int(all(flags))
        d["majority_modified"] += int(sum(modified) >= majority_n)
        d["unanimous_modified"] += int(all(modified))

    words = defaultdict(list)
    for i in items:
        words[key["items"][i]["condition"]].append(key["items"][i]["participant_words"])

    summary = {}
    for cond, d in sorted(by_condition.items()):
        n = d["n"]
        w = words[cond]

        def rate(x: int) -> float | None:
            return round(x / n, 4) if n else None

        summary[cond] = {
            "target_participant_words": key["condition_map"][cond],
            "n": n,
            "judge_usable_rate": {label: rate(d["judge_usable"][label]) for label in labels},
            "judge_modified_action_rate": {
                label: rate(d["judge_modified"][label]) for label in labels
            },
            "field_yes_rate": {
                field: {label: rate(d["field_yes"][field][label]) for label in labels}
                for field in FIELDS[:3]
            },
            "majority_flag_rate": {field: rate(d["majority_flag"][field]) for field in FAILING_FLAGS},
            "majority_usable_rate": rate(d["majority_usable"]),
            "unanimous_usable_rate": rate(d["unanimous_usable"]),
            "majority_modified_rate": rate(d["majority_modified"]),
            "unanimous_modified_rate": rate(d["unanimous_modified"]),
            "realised_participant_words": {
                "median": statistics.median(w) if w else None,
                "min": min(w) if w else None,
                "max": max(w) if w else None,
            },
        }
    return summary


def judge_response_stats(items: list[str], labels: list[str], judges: dict) -> dict:
    """Per-judge self-reported confidence and note usage, for outlier diagnosis."""
    stats = {}
    for label in labels:
        confidences = []
        notes = 0
        for i in items:
            row = judges[label][i]
            try:
                confidences.append(int(str(row.get("confidence_1_5", "")).strip()))
            except ValueError:
                pass
            notes += int(bool(str(row.get("notes", "")).strip()))
        stats[label] = {
            "mean_confidence_1_5": round(statistics.mean(confidences), 4) if confidences else None,
            "confidence_values": sorted(Counter(confidences).items()),
            "note_rate": round(notes / len(items), 4) if items else None,
        }
    return stats


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
    stress = sorted(i for i in common if key["items"][i]["stratum"] == "stress")

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

    condition_summary = condition_stats(regular, labels, judges, key)
    leave_one_out = {}
    for dropped in labels:
        subset = [label for label in labels if label != dropped]
        if len(subset) < 2:
            continue
        leave_one_out[f"without_{dropped}"] = condition_stats(regular, subset, judges, key)

    actions = {}
    for cond in condition_summary:
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
        "judge_response_stats": judge_response_stats(regular, labels, judges),
        "stress_descriptive": condition_stats(stress, labels, judges, key),
        "sensitivity_leave_one_out": leave_one_out,
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

    strategy_header = ("| Condition | Target words | N | " + " | ".join(labels)
                       + " | Majority usable | Unanimous usable | Majority modified | Unanimous modified |")
    strategy_sep = "|---|---:|---:|" + "|".join(["---:"] * len(labels)) + "|---:|---:|---:|---:|"
    strategy_rows = []
    for cond, d in condition_summary.items():
        vals = [str(d["judge_usable_rate"][label]) for label in labels]
        strategy_rows.append(
            f"| {cond} | {d['target_participant_words']} | {d['n']} | "
            + " | ".join(vals)
            + f" | {d['majority_usable_rate']} | {d['unanimous_usable_rate']} "
            + f"| {d['majority_modified_rate']} | {d['unanimous_modified_rate']} |"
        )

    loo_rows = []
    for dropped, stats in leave_one_out.items():
        for cond, d in stats.items():
            loo_rows.append(
                f"| {dropped} | {cond} | {d['target_participant_words']} | {d['n']} "
                f"| {d['unanimous_usable_rate']} | {d['unanimous_modified_rate']} |"
            )

    detail_header = (
        "| Condition | Target words | N | Majority usable | Unanimous usable "
        "| Majority modified | Unanimous modified | "
        + " | ".join(f"≥majority fail on {f}" for f in FAILING_FLAGS)
        + " | Realised participant words |"
    )
    detail_sep = "|---|---:|---:|---:|---:|---:|---:|" + "---:|" * len(FAILING_FLAGS) + "---:|"

    def detail_rows(stats: dict) -> list[str]:
        rows = []
        for cond, d in stats.items():
            w = d["realised_participant_words"]
            rows.append(
                f"| {cond} | {d['target_participant_words']} | {d['n']} "
                f"| {d['majority_usable_rate']} | {d['unanimous_usable_rate']} "
                f"| {d['majority_modified_rate']} | {d['unanimous_modified_rate']} "
                + "".join(f" | {d['majority_flag_rate'][f]}" for f in FAILING_FLAGS)
                + f" | median {w['median']}, range {w['min']}-{w['max']} |"
            )
        return rows

    resp_rows = []
    for label, d in result["judge_response_stats"].items():
        counts = ", ".join(f"{value}x{count}" for value, count in d["confidence_values"])
        resp_rows.append(
            f"| {label} | {d['mean_confidence_1_5']} | {d['note_rate']} | {counts} |"
        )

    agr_rows = []
    for field, d in agreement.items():
        agr_rows.append(f"| {field} | {d['n']} | {d['judges']} | {d['agreement']} | {d['ac1']} |")

    pair_rows = []
    for field, pairs in pairwise.items():
        for pair, d in pairs.items():
            pair_rows.append(f"| {field} | {pair} | {d['n']} | {d['agreement']} | {d['ac1']} |")

    yes_header = "| Condition | Field | Target words | " + " | ".join(labels) + " |"
    yes_sep = "|---|---|---:|" + "|".join(["---:"] * len(labels)) + "|"
    yes_rows = []
    for cond, d in condition_summary.items():
        for field in FIELDS[:3]:
            vals = [str(d["field_yes_rate"][field][label]) for label in labels]
            yes_rows.append(f"| {cond} | {field} | {d['target_participant_words']} | " + " | ".join(vals) + " |")

    mod_header = "| Condition | Target words | " + " | ".join(labels) + " |"
    mod_sep = "|---|---:|" + "|".join(["---:"] * len(labels)) + "|"
    mod_rows = []
    for cond, d in condition_summary.items():
        vals = [str(d["judge_modified_action_rate"][label]) for label in labels]
        mod_rows.append(f"| {cond} | {d['target_participant_words']} | " + " | ".join(vals) + " |")

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

## Per-field "yes" rate by blinded strategy

Higher is better for `coherent_boundary` and `sufficient_nontrivial`; lower is better for `mixed_unrelated_topics`.

{yes_header}
{yes_sep}
{chr(10).join(yes_rows)}

## Modified-action (merge/split/reject) rate per judge

{mod_header}
{mod_sep}
{chr(10).join(mod_rows)}

## Ensemble failure flags and realised window size (regular items)

{detail_header}
{detail_sep}
{chr(10).join(detail_rows(condition_summary))}

## Stress stratum, descriptive only

These windows are excluded from the primary comparison. They sample below-target tails and
>250-word windows, so a usable rate that collapses here is the rubric working as intended.

{detail_header}
{detail_sep}
{chr(10).join(detail_rows(result["stress_descriptive"]))}

## Judge response behaviour on regular items

| Judge | Mean confidence (1-5) | Note written | Confidence value counts |
|---|---:|---:|---|
{chr(10).join(resp_rows)}

## Leave-one-judge-out sensitivity (full agreement within each reduced ensemble)

With two remaining judges, majority and unanimous consensus coincide; these columns are
the strict-agreement view and test whether the strategy ordering depends on one family.

| Ensemble | Condition | Target words | N | Strict usable | Strict modified |
|---|---|---:|---:|---:|---:|
{chr(10).join(loo_rows)}

## Interpretation boundary

This is an automated engineering boundary-calibration result only. It does not establish
human interpretability, clinician agreement, phenomenological validity, disease effects,
or fidelity of any downstream representation.
"""
    mout.write_text(md, encoding="utf-8")


if __name__ == "__main__":
    main()
