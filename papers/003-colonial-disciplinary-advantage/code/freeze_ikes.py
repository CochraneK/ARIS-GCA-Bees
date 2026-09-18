#!/usr/bin/env python3
"""Create IKES_FROZEN.csv only after blinded A/B coding and adjudication.

Canonical key: concept_id (D01-D21). Unflagged A/B cells are averaged. Every
missing pair or absolute disagreement >= threshold must contain an explicit
adjudicated_score and note. Contemporary outcomes are never read.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

DIMS = [f"D{i}" for i in range(1, 12)]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("adjudication_csv", type=Path)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--provenance", type=Path)
    p.add_argument("--threshold", type=float, default=2.0)
    p.add_argument("--coder-a", type=Path, required=True)
    p.add_argument("--coder-b", type=Path, required=True)
    p.add_argument("--coder-b-notes", type=Path, required=True)
    p.add_argument("--coder-b-raw", type=Path, required=True)
    args = p.parse_args()

    df = pd.read_csv(args.adjudication_csv)
    required = {
        "concept_id", "discipline", "dimension", "score_A", "score_B",
        "abs_diff", "needs_adjudication", "adjudicated_score", "adjudication_note",
    }
    missing = required - set(df.columns)
    if missing:
        raise SystemExit(f"Adjudication file missing columns: {sorted(missing)}")
    if len(df) != 21 * 11:
        raise SystemExit(f"Expected 231 concept×dimension rows, got {len(df)}")
    if df.duplicated(["concept_id", "dimension"]).any():
        raise SystemExit("Duplicate concept_id×dimension rows in adjudication file")

    expected_ids = {f"D{i:02d}" for i in range(1, 22)}
    if set(df["concept_id"].astype(str)) != expected_ids:
        raise SystemExit("Adjudication file does not contain exactly D01-D21")

    df["score_A"] = pd.to_numeric(df["score_A"], errors="coerce")
    df["score_B"] = pd.to_numeric(df["score_B"], errors="coerce")
    df["adjudicated_score"] = pd.to_numeric(df["adjudicated_score"], errors="coerce")

    calculated_flag = (
        df["score_A"].isna()
        | df["score_B"].isna()
        | ((df["score_A"] - df["score_B"]).abs() >= args.threshold)
    )
    unresolved = calculated_flag & df["adjudicated_score"].isna()
    if unresolved.any():
        cols = ["concept_id", "discipline", "dimension", "score_A", "score_B"]
        raise SystemExit(
            "Cannot freeze IKES: flagged cells still lack adjudicated_score:\n"
            + df.loc[unresolved, cols].to_string(index=False)
        )

    has_adjudication = df["adjudicated_score"].notna()
    illegal_override = (~calculated_flag) & has_adjudication
    if illegal_override.any():
        cols = [
            "concept_id", "discipline", "dimension",
            "score_A", "score_B", "adjudicated_score"
        ]
        raise SystemExit(
            "Cannot freeze IKES: unflagged cells may not be manually overridden. "
            "Primary rule is the A/B mean for abs-difference < threshold:\n"
            + df.loc[illegal_override, cols].to_string(index=False)
        )

    bad_adj = df.loc[has_adjudication, "adjudicated_score"]
    if (~bad_adj.between(0, 3)).any():
        raise SystemExit("Adjudicated scores must be in [0,3]")
    missing_notes = has_adjudication & (
        df["adjudication_note"].fillna("").str.strip() == ""
    )
    if missing_notes.any():
        raise SystemExit("Every flagged adjudication requires a non-empty adjudication_note")

    df["final_score"] = (df["score_A"] + df["score_B"]) / 2.0
    df.loc[has_adjudication, "final_score"] = df.loc[has_adjudication, "adjudicated_score"]
    if df["final_score"].isna().any():
        raise SystemExit("Final score matrix still contains NA")

    labels = (
        df[["concept_id", "discipline"]]
        .drop_duplicates()
        .sort_values("concept_id")
    )
    if labels["concept_id"].duplicated().any():
        raise SystemExit("A concept_id has multiple discipline labels in adjudication data")

    wide = df.pivot(index="concept_id", columns="dimension", values="final_score")
    missing_dims = set(DIMS) - set(wide.columns)
    if missing_dims:
        raise SystemExit(f"Missing dimensions after pivot: {sorted(missing_dims)}")
    wide = wide[DIMS].reset_index().merge(labels, on="concept_id", how="left", validate="one_to_one")
    wide = wide[["concept_id", "discipline", *DIMS]]
    wide["IKES"] = wide[DIMS].mean(axis=1)
    wide["IKES_median"] = wide[DIMS].median(axis=1)
    wide = wide.sort_values("concept_id").reset_index(drop=True)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    wide.to_csv(args.output, index=False, float_format="%.6f")

    provenance = args.provenance or args.output.with_suffix(".provenance.json")
    payload = {
        "paper": "ARIS4C003",
        "created_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "canonical_key": "concept_id D01-D21",
        "rule": "unflagged A/B cells are immutable means; missing or abs-diff>=threshold requires explicit outcome-blind adjudication",
        "threshold": args.threshold,
        "coder_a": {"path": str(args.coder_a), "sha256": sha256(args.coder_a)},
        "coder_b": {"path": str(args.coder_b), "sha256": sha256(args.coder_b)},
        "coder_b_notes": {
            "path": str(args.coder_b_notes),
            "sha256": sha256(args.coder_b_notes),
        },
        "coder_b_raw": {
            "path": str(args.coder_b_raw),
            "sha256": sha256(args.coder_b_raw),
        },
        "adjudication": {"path": str(args.adjudication_csv), "sha256": sha256(args.adjudication_csv)},
        "frozen": {"path": str(args.output), "sha256": sha256(args.output)},
        "n_explicit_adjudications": int(has_adjudication.sum()),
    }
    provenance.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"IKES FROZEN: {args.output}")
    print(f"sha256: {payload['frozen']['sha256']}")


if __name__ == "__main__":
    main()
