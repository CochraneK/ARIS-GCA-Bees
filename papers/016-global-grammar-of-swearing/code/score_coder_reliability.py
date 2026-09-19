#!/usr/bin/env python3
"""Compute aggregate independent-coder reliability for ARIS4C016.

Inputs are private coder CSVs produced from the frozen 300-row sample. The
script never emits raw taboo expressions; outputs contain aggregate agreement
statistics and row hashes only for optional disagreement queues.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import hashlib
from collections import Counter, defaultdict
from pathlib import Path

AXES = (
    "semantic_source",
    "target",
    "pragmatic_function",
    "social_indexical_basis",
    "taboo_mechanism",
)
EXPECTED_N = 300
EXPECTED_MANIFEST_SHA256 = "48c58f91901e8c2a1aab01958e95ea28afaf0f33e7a98677f98e58b8a412c9b4"


def parse_set(value: str | None) -> frozenset[str]:
    raw = (value or "").strip()
    if not raw:
        return frozenset()
    if raw.startswith("["):
        try:
            x = json.loads(raw)
            return frozenset(str(v).strip() for v in x if str(v).strip())
        except json.JSONDecodeError:
            pass
    normalized = raw.replace(";", "|").replace(",", "|")
    return frozenset(v.strip() for v in normalized.split("|") if v.strip())


def parse_bool(value: str | None) -> bool | None:
    raw = (value or "").strip().lower()
    if raw in {"1", "true", "yes", "y"}:
        return True
    if raw in {"0", "false", "no", "n"}:
        return False
    return None


def manifest_sha256(rows: dict[str, dict[str, str]]) -> str:
    manifest_rows = []
    for row in rows.values():
        sample = (row.get("sample") or "").strip()
        row_index = (row.get("source_row_index") or "").strip()
        row_hash = (row.get("row_hash") or "").strip()
        stratum = (row.get("selection_stratum") or "").strip()
        if not all((sample, row_index, row_hash, stratum)):
            raise ValueError(
                "Coder file must retain sample, source_row_index, row_hash, "
                "and selection_stratum to verify the frozen sample."
            )
        manifest_rows.append((sample, int(row_index), row_hash, stratum))
    manifest_rows.sort(key=lambda x: (x[0], x[1]))
    lines = ["sample,row_index,row_hash,stratum"]
    lines.extend(f"{s},{i},{h},{t}" for s, i, h, t in manifest_rows)
    payload = "\n".join(lines) + "\n"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def load(path: Path) -> dict[str, dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != EXPECTED_N:
        raise ValueError(f"{path}: expected {EXPECTED_N} rows, got {len(rows)}")
    out = {}
    for row in rows:
        key = (row.get("row_hash") or "").strip()
        if not key:
            raise ValueError(f"{path}: missing row_hash")
        if key in out:
            raise ValueError(f"{path}: duplicate row_hash {key}")
        out[key] = row
    return out


def jaccard(a: frozenset[str], b: frozenset[str]) -> float:
    if not a and not b:
        return 1.0
    union = a | b
    return len(a & b) / len(union) if union else 1.0


def cohen_kappa(a: list[bool], b: list[bool]) -> float | None:
    n = len(a)
    if not n:
        return None
    agree = sum(x == y for x, y in zip(a, b)) / n
    pa = sum(a) / n
    pb = sum(b) / n
    expected = pa * pb + (1 - pa) * (1 - pb)
    if math.isclose(1 - expected, 0.0):
        return None
    return (agree - expected) / (1 - expected)


def gwet_ac1(a: list[bool], b: list[bool]) -> float | None:
    """Binary Gwet AC1 using pooled marginal positive prevalence."""
    n = len(a)
    if not n:
        return None
    agree = sum(x == y for x, y in zip(a, b)) / n
    p = (sum(a) + sum(b)) / (2 * n)
    chance = 2 * p * (1 - p)
    if math.isclose(1 - chance, 0.0):
        return None
    return (agree - chance) / (1 - chance)


def safe_round(x: float | None, digits: int = 4):
    return None if x is None else round(x, digits)


def axis_stats(
    keys: list[str],
    coder_a: dict[str, dict[str, str]],
    coder_b: dict[str, dict[str, str]],
    axis: str,
) -> dict:
    pairs = [(parse_set(coder_a[k].get(axis)), parse_set(coder_b[k].get(axis))) for k in keys]
    exact = sum(a == b for a, b in pairs) / len(pairs)
    jac = [jaccard(a, b) for a, b in pairs]
    labels = sorted(set().union(*(a | b for a, b in pairs)))

    label_stats = {}
    for label in labels:
        av = [label in a for a, _ in pairs]
        bv = [label in b for _, b in pairs]
        raw_agree = sum(x == y for x, y in zip(av, bv)) / len(av)
        label_stats[label] = {
            "prevalence_a": round(sum(av) / len(av), 4),
            "prevalence_b": round(sum(bv) / len(bv), 4),
            "raw_agreement": round(raw_agree, 4),
            "cohen_kappa": safe_round(cohen_kappa(av, bv)),
            "gwet_ac1": safe_round(gwet_ac1(av, bv)),
        }

    return {
        "n": len(pairs),
        "exact_set_agreement": round(exact, 4),
        "mean_jaccard": round(sum(jac) / len(jac), 4),
        "median_jaccard": round(sorted(jac)[len(jac) // 2], 4),
        "labels": label_stats,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("coder_a", type=Path)
    parser.add_argument("coder_b", type=Path)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    a = load(args.coder_a)
    b = load(args.coder_b)

    for label, rows in (("Coder A", a), ("Coder B", b)):
        digest = manifest_sha256(rows)
        if digest != EXPECTED_MANIFEST_SHA256:
            raise ValueError(
                f"{label} does not match the frozen audit sample: "
                f"expected {EXPECTED_MANIFEST_SHA256}, got {digest}"
            )
    if set(a) != set(b):
        only_a = sorted(set(a) - set(b))
        only_b = sorted(set(b) - set(a))
        raise ValueError(
            f"Coder row sets differ: only A={len(only_a)}, only B={len(only_b)}"
        )

    keys = sorted(a)

    communities: dict[str, list[str]] = defaultdict(list)
    for k in keys:
        sa = (a[k].get("sample") or "").strip()
        sb = (b[k].get("sample") or "").strip()
        if sa != sb:
            raise ValueError(f"Sample metadata mismatch for {k}: {sa!r} vs {sb!r}")
        communities[sa].append(k)

    axes = {axis: axis_stats(keys, a, b, axis) for axis in AXES}

    community_disagreement = {}
    for community, ckeys in sorted(communities.items()):
        community_disagreement[community] = {}
        for axis in AXES:
            pairs = [(parse_set(a[k].get(axis)), parse_set(b[k].get(axis))) for k in ckeys]
            community_disagreement[community][axis] = round(
                1 - sum(x == y for x, y in pairs) / len(pairs), 4
            )

    native_pairs = [
        (parse_bool(a[k].get("native_review_required")),
         parse_bool(b[k].get("native_review_required")))
        for k in keys
    ]
    native_complete = [(x, y) for x, y in native_pairs if x is not None and y is not None]

    confidence_agreement = sum(
        (a[k].get("confidence") or "").strip() == (b[k].get("confidence") or "").strip()
        for k in keys
    ) / len(keys)

    disagreement_hashes = [
        k for k in keys
        if any(parse_set(a[k].get(axis)) != parse_set(b[k].get(axis)) for axis in AXES)
    ]

    result = {
        "project": "ARIS4C016",
        "n_rows": len(keys),
        "expected_frozen_manifest_sha256": EXPECTED_MANIFEST_SHA256,
        "axis_reliability": axes,
        "confidence_exact_agreement": round(confidence_agreement, 4),
        "native_review_flag": {
            "n_complete_pairs": len(native_complete),
            "raw_agreement": (
                round(sum(x == y for x, y in native_complete) / len(native_complete), 4)
                if native_complete else None
            ),
        },
        "community_disagreement_rate": community_disagreement,
        "n_rows_with_any_axis_disagreement": len(disagreement_hashes),
        "disagreement_row_hashes": disagreement_hashes,
        "privacy_note": "No raw lexical expression or translation is emitted.",
    }

    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
        print(f"Wrote aggregate reliability report to {args.output}")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
