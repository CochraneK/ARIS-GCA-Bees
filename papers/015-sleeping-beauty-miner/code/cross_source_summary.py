"""Summarize cross-source Sleeping Beauty replication probes."""

from __future__ import annotations

import argparse
import csv
import json
import statistics
from pathlib import Path
from typing import Iterable


def load_result(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def summarize_results(results: Iterable[dict]) -> dict:
    rows = list(results)
    if not rows:
        raise ValueError("at least one result is required")

    relative_b = [
        float(row["cross_source_difference"]["beauty_coefficient_relative"])
        for row in rows
        if row["cross_source_difference"]["beauty_coefficient_relative"] is not None
    ]
    awakening_diff = [
        int(row["cross_source_difference"]["awakening_year"])
        for row in rows
    ]

    return {
        "n_cases": len(rows),
        "mean_relative_B_difference": statistics.fmean(relative_b)
        if relative_b
        else None,
        "mean_absolute_relative_B_difference": statistics.fmean(
            abs(x) for x in relative_b
        )
        if relative_b
        else None,
        "median_absolute_relative_B_difference": statistics.median(
            abs(x) for x in relative_b
        )
        if relative_b
        else None,
        "mean_awakening_year_difference": statistics.fmean(awakening_diff),
        "mean_absolute_awakening_year_difference": statistics.fmean(
            abs(x) for x in awakening_diff
        ),
        "max_absolute_awakening_year_difference": max(
            abs(x) for x in awakening_diff
        ),
    }


def result_row(result: dict) -> dict:
    return {
        "case_id": result["case_id"],
        "doi": result["target"]["doi"],
        "openalex_id": result["target"]["openalex_id"],
        "publication_year": result["target"]["publication_year"],
        "citations_through_2011": result["trajectory"]["total_citations"],
        "openalex_B": result["reconstructed"]["beauty_coefficient"],
        "reference_WoS_B": result["reference_ke2015"]["beauty_coefficient"],
        "relative_B_difference": result["cross_source_difference"][
            "beauty_coefficient_relative"
        ],
        "openalex_awakening_year": result["reconstructed"]["awakening_year"],
        "reference_WoS_awakening_year": result["reference_ke2015"][
            "awakening_year"
        ],
        "awakening_year_difference": result["cross_source_difference"][
            "awakening_year"
        ],
    }


def write_csv(results: Iterable[dict], output: str | Path) -> None:
    rows = [result_row(row) for row in results]
    if not rows:
        raise ValueError("at least one result is required")
    with Path(output).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", nargs="+", type=Path)
    parser.add_argument("--csv-output", type=Path)
    parser.add_argument("--json-output", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    results = [load_result(path) for path in args.inputs]
    summary = summarize_results(results)

    if args.csv_output:
        write_csv(results, args.csv_output)

    text = json.dumps(summary, indent=2) + "\n"
    if args.json_output:
        args.json_output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
