#!/usr/bin/env python3
"""Item-fixed-effects English community model for ARIS4C016.

Pure-Python implementation of a Frisch-Waugh-Lovell partial-R² diagnostic.
The script downloads checksum-verified Study 2 data and emits aggregates only.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import math
import random
import urllib.request

GUID = "t8wj9"
VIEW_ONLY = "60b964248cc64a8793a9013075132a1c"
SHA256 = "617306c5d762586e0426081b13f779d64b30937f2d35cfbe24fdb97ded1f7a5a"
DIMS = ("tabooness", "offensiveness", "valence", "arousal", "concreteness", "aoa")
BOOTSTRAPS = 500
SEED = 16016


def load() -> list[dict[str, str]]:
    url = f"https://osf.io/download/{GUID}/?view_only={VIEW_ONLY}"
    with urllib.request.urlopen(url, timeout=120) as response:
        blob = response.read()
    if hashlib.sha256(blob).hexdigest() != SHA256:
        raise RuntimeError("Study-2 checksum mismatch")
    rows = csv.DictReader(io.StringIO(blob.decode("utf-8-sig", errors="replace")))
    return [
        r for r in rows
        if (r.get("category") or "").strip().lower() != "filler"
        and r["lang"].startswith("English")
    ]


def solve(matrix: list[list[float]], vector: list[float]) -> list[float]:
    """Small Gaussian-elimination solver; model has only four community columns."""
    n = len(vector)
    aug = [list(map(float, matrix[i])) + [float(vector[i])] for i in range(n)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda i: abs(aug[i][col]))
        if abs(aug[pivot][col]) < 1e-12:
            aug[pivot][col] += 1e-8
        aug[col], aug[pivot] = aug[pivot], aug[col]
        divisor = aug[col][col]
        aug[col] = [x / divisor for x in aug[col]]
        for i in range(n):
            if i == col:
                continue
            factor = aug[i][col]
            aug[i] = [
                aug[i][j] - factor * aug[col][j] for j in range(n + 1)
            ]
    return [aug[i][-1] for i in range(n)]


def fit(
    blocks: list[tuple[str, dict[str, dict[str, str]]]],
    communities: list[str],
    dimension: str,
) -> tuple[float, dict[str, float], int]:
    # FWL: residualize outcome and community dummies by item fixed effects.
    obs: list[tuple[float, list[float], str]] = []
    for _, mapping in blocks:
        values = []
        for community, row in mapping.items():
            try:
                value = float(row[dimension])
            except (TypeError, ValueError):
                continue
            if math.isfinite(value):
                values.append((community, value))
        if len(values) < 2:
            continue
        mean_y = sum(y for _, y in values) / len(values)
        proportions = {
            community: sum(1 for c, _ in values if c == community) / len(values)
            for community in communities
        }
        for community, value in values:
            x = [
                (1.0 if community == c else 0.0) - proportions[c]
                for c in communities[1:]
            ]
            obs.append((value - mean_y, x, community))

    p = len(communities) - 1
    xtx = [[0.0] * p for _ in range(p)]
    xty = [0.0] * p
    rss_item_only = sum(y * y for y, _, _ in obs)

    for y, x, _ in obs:
        for j in range(p):
            xty[j] += x[j] * y
            for k in range(p):
                xtx[j][k] += x[j] * x[k]

    beta = solve(xtx, xty)
    rss_full = 0.0
    for y, x, _ in obs:
        fitted = sum(beta[j] * x[j] for j in range(p))
        rss_full += (y - fitted) ** 2

    partial_r2 = (
        (rss_item_only - rss_full) / rss_item_only if rss_item_only else 0.0
    )

    effects = {communities[0]: 0.0}
    effects.update({c: b for c, b in zip(communities[1:], beta)})
    counts = {
        c: sum(1 for _, _, community in obs if community == c)
        for c in communities
    }
    center = sum(effects[c] * counts[c] for c in communities) / sum(counts.values())
    effects = {c: effects[c] - center for c in communities}
    return partial_r2, effects, len(obs)


def main() -> None:
    rows = load()
    communities = sorted({r["lang"] for r in rows})
    by_word: dict[str, dict[str, dict[str, str]]] = {}
    for row in rows:
        by_word.setdefault(row["word_clean"], {})[row["lang"]] = row
    blocks = [(w, m) for w, m in by_word.items() if len(m) >= 2]

    rng = random.Random(SEED)
    output = {}
    for dimension in DIMS:
        estimate = fit(blocks, communities, dimension)
        r2_boot = []
        effect_boot = {c: [] for c in communities}
        for _ in range(BOOTSTRAPS):
            sample = [blocks[rng.randrange(len(blocks))] for _ in range(len(blocks))]
            boot = fit(sample, communities, dimension)
            r2_boot.append(boot[0])
            for c, value in boot[1].items():
                effect_boot[c].append(value)

        r2_boot.sort()
        community_effects = {}
        for community, values in effect_boot.items():
            values.sort()
            community_effects[community] = {
                "estimate": round(estimate[1][community], 4),
                "bootstrap95": [
                    round(values[int(0.025 * len(values))], 4),
                    round(values[int(0.975 * len(values)) - 1], 4),
                ],
            }

        output[dimension] = {
            "n_item_community_observations": estimate[2],
            "partial_r2_community_after_item_fixed_effects": round(estimate[0], 4),
            "bootstrap95": [
                round(r2_boot[int(0.025 * len(r2_boot))], 4),
                round(r2_boot[int(0.975 * len(r2_boot)) - 1], 4),
            ],
            "centered_community_effects": community_effects,
        }

    print(json.dumps({
        "project": "ARIS4C016",
        "shared_english_items": len(blocks),
        "communities": communities,
        "bootstrap_items": BOOTSTRAPS,
        "results": output,
        "limitations": [
            "Uses aggregate Study-2 item ratings, not participant-level observations.",
            "Intervals reflect item resampling, not full rating-estimation uncertainty.",
            "Community effects are associative, not causal cultural effects.",
        ],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
