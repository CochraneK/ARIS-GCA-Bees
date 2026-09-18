#!/usr/bin/env python3
"""Regenerate Paper 002 manuscript figures from archived stage JSON outputs."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
IDEA = ROOT / "ideas" / "language-periodic-system"
OUT = ROOT / "papers" / "002-language-geometry" / "figures"
OUT.mkdir(parents=True, exist_ok=True)


def load(name: str):
    return json.loads((IDEA / name).read_text(encoding="utf-8"))


def figure_cross_dataset():
    f = load("stage1f-results.json")
    h = load("stage1h-results.json")
    i = load("stage1i-results.json")

    labels = ["TLI", "GBI", "WALS"]
    tree = [
        f["models"]["tree"]["mean_spearman"],
        h["family_heldout"]["summary"]["tree"]["mean"],
        i["family_heldout"]["models"]["tree"]["mean"],
    ]
    circle = [
        f["models"]["circular_optimized"]["mean_spearman"],
        h["family_heldout"]["summary"]["circular_optimized"]["mean"],
        i["family_heldout"]["models"]["circular_optimized"]["mean"],
    ]

    x = np.arange(len(labels))
    width = 0.36

    fig, ax = plt.subplots(figsize=(8.4, 5.2))
    bars1 = ax.bar(x - width / 2, tree, width, label="Tree benchmark")
    bars2 = ax.bar(x + width / 2, circle, width, label="Optimized circle")
    ax.set_xticks(x, labels)
    ax.set_ylabel("Mean held-out Spearman")
    ax.set_title("Family-held-out predictive ranking across representations")
    ax.legend()
    ax.bar_label(bars1, fmt="%.3f", padding=3)
    ax.bar_label(bars2, fmt="%.3f", padding=3)
    ax.text(
        0.5,
        -0.16,
        "Absolute magnitudes are not directly comparable across datasets.",
        transform=ax.transAxes,
        ha="center",
    )
    fig.tight_layout()
    fig.savefig(OUT / "figure1_cross_dataset.svg", bbox_inches="tight")
    plt.close(fig)


def figure_tli_contrasts():
    f = load("stage1f-results.json")
    keys = [
        ("tree_minus_circular", "Tree - circle"),
        ("lowrank_minus_circular", "Low-rank - circle"),
        ("euclidean_minus_circular", "Euclidean - circle"),
    ]
    means = np.array([f["paired_contrasts"][k]["mean"] for k, _ in keys])
    lows = np.array([f["paired_contrasts"][k]["ci95_low"] for k, _ in keys])
    highs = np.array([f["paired_contrasts"][k]["ci95_high"] for k, _ in keys])
    labels = [label for _, label in keys]
    y = np.arange(len(labels))

    fig, ax = plt.subplots(figsize=(8.4, 4.8))
    ax.errorbar(
        means,
        y,
        xerr=np.vstack([means - lows, highs - means]),
        fmt="o",
        capsize=5,
    )
    ax.axvline(0, linewidth=1)
    ax.set_yticks(y, labels)
    ax.invert_yaxis()
    ax.set_xlabel("Paired held-out Spearman difference")
    ax.set_title("TLI repeated family-held-out contrasts")
    ax.text(
        0.5,
        -0.18,
        "95% bootstrap intervals resample split-level contrasts; they are not phylogenetic uncertainty intervals.",
        transform=ax.transAxes,
        ha="center",
    )
    fig.tight_layout()
    fig.savefig(OUT / "figure2_tli_paired_contrasts.svg", bbox_inches="tight")
    plt.close(fig)


def figure_circular_diagnostics():
    d = load("stage1d-results.json")
    counts = ["40", "60"]
    circular = [d["feature_counts"][n]["summary"]["circular_mean_violation"]["mean"] for n in counts]
    tree = [d["feature_counts"][n]["summary"]["tree_mean_violation"]["mean"] for n in counts]
    random = [d["feature_counts"][n]["summary"]["random_mean_violation"]["mean"] for n in counts]

    x = np.arange(len(counts))
    width = 0.24
    fig, ax = plt.subplots(figsize=(8.4, 5.0))
    ax.bar(x - width, circular, width, label="Circular order")
    ax.bar(x, tree, width, label="Tree leaf order")
    ax.bar(x + width, random, width, label="Random order")
    ax.set_xticks(x, [f"{n} features" for n in counts])
    ax.set_ylabel("Mean row-unimodality violation (lower is better)")
    ax.set_title("Held-out circular-Robinson-style sensitivity")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT / "figure3_circular_diagnostics.svg", bbox_inches="tight")
    plt.close(fig)


def main():
    figure_cross_dataset()
    figure_tli_contrasts()
    figure_circular_diagnostics()


if __name__ == "__main__":
    main()
