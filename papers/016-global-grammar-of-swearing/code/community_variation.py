#!/usr/bin/env python3
"""Repeated-language community-variation diagnostics for ARIS4C016.

Downloads Study 2 from the public OSF project, verifies its checksum, excludes
fillers, and reports only aggregate statistics. Raw taboo expressions are not
printed.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import math
import statistics
import urllib.request
from collections import Counter, defaultdict

GUID = "t8wj9"
VIEW_ONLY = "60b964248cc64a8793a9013075132a1c"
SHA256 = "617306c5d762586e0426081b13f779d64b30937f2d35cfbe24fdb97ded1f7a5a"
DIMS = ("tabooness", "offensiveness", "valence", "arousal", "concreteness", "aoa")


def load() -> list[dict[str, str]]:
    url = f"https://osf.io/download/{GUID}/?view_only={VIEW_ONLY}"
    with urllib.request.urlopen(url, timeout=120) as response:
        blob = response.read()
    digest = hashlib.sha256(blob).hexdigest()
    if digest != SHA256:
        raise RuntimeError(f"checksum mismatch: {digest}")
    text = blob.decode("utf-8-sig", errors="replace")
    return [
        r for r in csv.DictReader(io.StringIO(text))
        if (r.get("category") or "").strip().lower() != "filler"
    ]


def number(value: str | None) -> float | None:
    try:
        x = float(value)
    except (TypeError, ValueError):
        return None
    return x if math.isfinite(x) else None


def summarize(rows: list[dict[str, str]], prefix: str) -> dict:
    communities = sorted({r["lang"] for r in rows if r["lang"].startswith(prefix)})
    by_word: dict[str, dict[str, dict[str, str]]] = defaultdict(dict)
    for row in rows:
        if row["lang"] in communities:
            by_word[row["word_clean"]][row["lang"]] = row

    output = {"communities": communities, "dimensions": {}}
    for dim in DIMS:
        item_means = []
        within_variances = []
        coverage = Counter()
        for community_rows in by_word.values():
            values = [
                number(row.get(dim)) for row in community_rows.values()
            ]
            values = [x for x in values if x is not None]
            if len(values) < 2:
                continue
            coverage[len(values)] += 1
            mean = sum(values) / len(values)
            item_means.append(mean)
            within_variances.append(
                sum((x - mean) ** 2 for x in values) / (len(values) - 1)
            )

        between = statistics.pvariance(item_means) if len(item_means) > 1 else 0.0
        within = (
            sum(within_variances) / len(within_variances)
            if within_variances else 0.0
        )
        denom = between + within
        output["dimensions"][dim] = {
            "shared_items": sum(coverage.values()),
            "coverage_by_communities": dict(sorted(coverage.items())),
            "between_item_variance_of_means": round(between, 6),
            "mean_within_item_cross_community_variance": round(within, 6),
            "simple_within_share": round(within / denom, 4) if denom else None,
        }
    return output


def main() -> None:
    rows = load()
    print(json.dumps({
        "project": "ARIS4C016",
        "note": "Diagnostic ratio is not a formal ICC.",
        "English": summarize(rows, "English"),
        "Spanish": summarize(rows, "Spanish"),
        "privacy_note": "No raw taboo expressions are emitted.",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
