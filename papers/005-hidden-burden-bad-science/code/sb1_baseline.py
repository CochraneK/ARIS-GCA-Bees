#!/usr/bin/env python3
"""Leakage-safe early-citation baseline for ARIS4C005 SB1.

The model uses only explicitly whitelisted feature_* columns created at the
landmark. It predicts an engineering delayed-recognition outcome with
publication-year-blocked out-of-fold validation.

This is predictive infrastructure, not a causal model and not a Sleeping Beauty
prevalence estimator.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Any

FEATURES = [
    "feature_citations_cumulative",
    "feature_citations_last_year",
    "feature_citations_max_annual",
    "feature_citations_mean_annual",
    "feature_zero_citation_years",
    "feature_positive_citation_years",
    "feature_citation_slope",
]

DEFAULT_TARGET = "outcome_awakening_within_horizon_after_landmark"


def sigmoid(x: float) -> float:
    if x >= 0:
        z = math.exp(-x)
        return 1.0 / (1.0 + z)
    z = math.exp(x)
    return z / (1.0 + z)


def mean(values: list[float]) -> float:
    if not values:
        raise ValueError("mean of empty sequence")
    return sum(values) / len(values)


def standardize_fit(x: list[list[float]]) -> tuple[list[float], list[float]]:
    if not x:
        raise ValueError("empty feature matrix")
    p = len(x[0])
    means = []
    scales = []
    for j in range(p):
        col = [row[j] for row in x]
        m = mean(col)
        var = mean([(v - m) ** 2 for v in col])
        sd = math.sqrt(var)
        means.append(m)
        scales.append(sd if sd > 1e-12 else 1.0)
    return means, scales


def standardize(
    x: list[list[float]],
    means: list[float],
    scales: list[float],
) -> list[list[float]]:
    return [
        [(v - means[j]) / scales[j] for j, v in enumerate(row)]
        for row in x
    ]


def fit_logistic(
    x: list[list[float]],
    y: list[int],
    *,
    l2: float = 0.1,
    learning_rate: float = 0.05,
    iterations: int = 1500,
) -> tuple[list[float], float]:
    if not x or len(x) != len(y):
        raise ValueError("invalid training data")
    if set(y) - {0, 1}:
        raise ValueError("target must be binary")
    p = len(x[0])
    w = [0.0] * p
    prevalence = min(1 - 1e-6, max(1e-6, mean([float(v) for v in y])))
    b = math.log(prevalence / (1.0 - prevalence))

    n = len(y)
    for step in range(iterations):
        grad_w = [0.0] * p
        grad_b = 0.0
        for row, target in zip(x, y):
            score = b + sum(a * weight for a, weight in zip(row, w))
            pred = sigmoid(score)
            err = pred - target
            grad_b += err
            for j in range(p):
                grad_w[j] += err * row[j]

        grad_b /= n
        for j in range(p):
            grad_w[j] = grad_w[j] / n + l2 * w[j]

        # Mild inverse-time decay improves stability across folds.
        lr = learning_rate / (1.0 + 0.001 * step)
        b -= lr * grad_b
        for j in range(p):
            w[j] -= lr * grad_w[j]

    return w, b


def predict(x: list[list[float]], w: list[float], b: float) -> list[float]:
    return [
        sigmoid(b + sum(a * weight for a, weight in zip(row, w)))
        for row in x
    ]


def auc(y: list[int], p: list[float]) -> float | None:
    if len(y) != len(p):
        raise ValueError("length mismatch")
    n_pos = sum(y)
    n_neg = len(y) - n_pos
    if n_pos == 0 or n_neg == 0:
        return None

    indexed = sorted(enumerate(p), key=lambda z: z[1])
    ranks = [0.0] * len(p)
    i = 0
    while i < len(indexed):
        j = i + 1
        while j < len(indexed) and indexed[j][1] == indexed[i][1]:
            j += 1
        avg_rank = (i + 1 + j) / 2.0
        for k in range(i, j):
            ranks[indexed[k][0]] = avg_rank
        i = j

    rank_sum_pos = sum(r for r, target in zip(ranks, y) if target == 1)
    return (rank_sum_pos - n_pos * (n_pos + 1) / 2.0) / (n_pos * n_neg)


def brier(y: list[int], p: list[float]) -> float:
    return mean([(target - pred) ** 2 for target, pred in zip(y, p)])


def log_loss(y: list[int], p: list[float]) -> float:
    eps = 1e-12
    values = []
    for target, pred in zip(y, p):
        pred = min(1 - eps, max(eps, pred))
        values.append(
            -(target * math.log(pred) + (1 - target) * math.log(1 - pred))
        )
    return mean(values)


def parse_rows(
    rows: list[dict[str, str]],
    target: str,
) -> list[dict[str, Any]]:
    parsed = []
    for row in rows:
        if str(row.get("eligible_for_horizon") or "").strip() != "1":
            continue
        raw_target = str(row.get(target) or "").strip()
        if raw_target not in {"0", "1"}:
            continue

        features = []
        for name in FEATURES:
            raw = str(row.get(name) or "").strip()
            if raw == "":
                raise ValueError(f"{row.get('paper_id')}: missing {name}")
            features.append(float(raw))

        parsed.append(
            {
                "paper_id": str(row.get("paper_id") or ""),
                "publication_year": int(row["publication_year"]),
                "x": features,
                "y": int(raw_target),
            }
        )
    return parsed


def year_block_folds(
    parsed: list[dict[str, Any]],
    folds: int,
) -> dict[int, int]:
    if folds < 2:
        raise ValueError("folds must be >=2")
    years = sorted({int(r["publication_year"]) for r in parsed})
    if len(years) < 2:
        raise ValueError("need at least two publication years")
    k = min(folds, len(years))

    mapping: dict[int, int] = {}
    for i, year in enumerate(years):
        fold = min(k - 1, int(i * k / len(years)))
        mapping[year] = fold
    return mapping


def evaluate(
    rows: list[dict[str, str]],
    *,
    target: str = DEFAULT_TARGET,
    folds: int = 5,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    parsed = parse_rows(rows, target)
    if len(parsed) < 20:
        raise ValueError("need at least 20 eligible rows for baseline evaluation")

    fold_map = year_block_folds(parsed, folds)
    realized_folds = sorted(set(fold_map.values()))
    predictions: list[dict[str, Any]] = []
    fold_summaries = []

    for fold in realized_folds:
        train = [
            r for r in parsed if fold_map[r["publication_year"]] != fold
        ]
        test = [
            r for r in parsed if fold_map[r["publication_year"]] == fold
        ]
        if not train or not test:
            continue

        x_train = [r["x"] for r in train]
        y_train = [r["y"] for r in train]
        x_test = [r["x"] for r in test]
        y_test = [r["y"] for r in test]

        train_prev = mean([float(v) for v in y_train])
        if len(set(y_train)) < 2:
            probs = [train_prev] * len(test)
            model_status = "PREVALENCE_ONLY_NO_CLASS_VARIATION"
        else:
            means, scales = standardize_fit(x_train)
            sx_train = standardize(x_train, means, scales)
            sx_test = standardize(x_test, means, scales)
            w, b = fit_logistic(sx_train, y_train)
            probs = predict(sx_test, w, b)
            model_status = "LOGISTIC"

        for rec, prob in zip(test, probs):
            predictions.append(
                {
                    "paper_id": rec["paper_id"],
                    "publication_year": rec["publication_year"],
                    "fold": fold,
                    "target": rec["y"],
                    "predicted_probability": prob,
                    "train_prevalence_baseline": train_prev,
                }
            )

        fold_summaries.append(
            {
                "fold": fold,
                "test_year_min": min(r["publication_year"] for r in test),
                "test_year_max": max(r["publication_year"] for r in test),
                "train_n": len(train),
                "test_n": len(test),
                "train_prevalence": train_prev,
                "test_prevalence": mean([float(v) for v in y_test]),
                "model_status": model_status,
            }
        )

    predictions.sort(key=lambda r: r["paper_id"])
    y = [int(r["target"]) for r in predictions]
    p = [float(r["predicted_probability"]) for r in predictions]
    p0 = [float(r["train_prevalence_baseline"]) for r in predictions]

    if len(predictions) != len(parsed):
        raise ValueError("not all eligible rows received out-of-fold predictions")

    summary = {
        "classification": "SB1_EARLY_CITATION_BASELINE_ENGINEERING_NOT_CAUSAL",
        "target": target,
        "rows_eligible": len(parsed),
        "positives": sum(y),
        "prevalence": mean([float(v) for v in y]),
        "feature_columns": FEATURES,
        "validation": "publication-year-blocked out-of-fold",
        "folds_requested": folds,
        "folds_realized": len(realized_folds),
        "metrics": {
            "auc": auc(y, p),
            "brier": brier(y, p),
            "log_loss": log_loss(y, p),
            "prevalence_baseline_brier": brier(y, p0),
            "prevalence_baseline_log_loss": log_loss(y, p0),
            "brier_improvement_vs_prevalence_baseline": brier(y, p0) - brier(y, p),
        },
        "folds": fold_summaries,
        "warnings": [
            "Only whitelisted feature_* columns are used; full-history outcomes are excluded from predictors.",
            "This small engineering pilot is not a final predictive model.",
            "Prediction does not identify causal suppression by integrity failures.",
            "Current features are early citation trajectory only; semantic/network predictors must be frozen at the same landmark before addition.",
            "No universal Sleeping Beauty threshold is used.",
        ],
    }
    return predictions, summary


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys()) if rows else []
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("landmark_csv", type=Path)
    p.add_argument("predictions_csv", type=Path)
    p.add_argument("summary_json", type=Path)
    p.add_argument("--target", default=DEFAULT_TARGET)
    p.add_argument("--folds", type=int, default=5)
    args = p.parse_args()

    with args.landmark_csv.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    predictions, summary = evaluate(
        rows,
        target=args.target,
        folds=args.folds,
    )
    write_csv(args.predictions_csv, predictions)
    args.summary_json.parent.mkdir(parents=True, exist_ok=True)
    args.summary_json.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
