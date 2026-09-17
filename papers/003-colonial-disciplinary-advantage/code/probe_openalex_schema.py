#!/usr/bin/env python3
"""Probe a local OpenAlex Works Parquet snapshot without materializing outcomes.

This is allowed while the confirmatory outcome gate is locked. It inspects
schema/types and validates that the fields frozen in the preregistration exist.
It intentionally does not group publications by country or discipline.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import duckdb

REQUIRED_TOP_LEVEL = {
    "id",
    "publication_year",
    "type",
    "primary_topic",
    "authorships",
    "citation_normalized_percentile",
    "fwci",
    "language",
    "is_retracted",
    "is_xpac",
}


def sql_path(path: Path) -> str:
    return str(path).replace("'", "''")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot_root", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    root = args.snapshot_root.expanduser().resolve()
    files = list(root.rglob("*.parquet"))
    if not files:
        raise SystemExit(f"No .parquet files under {root}")

    glob = root / "**" / "*.parquet"
    con = duckdb.connect(database=":memory:")
    description = con.execute(
        f"DESCRIBE SELECT * FROM read_parquet('{sql_path(glob)}', union_by_name=true)"
    ).fetchdf()
    columns = set(description["column_name"].astype(str))
    missing = sorted(REQUIRED_TOP_LEVEL - columns)

    nested_checks = {}
    probes = {
        "primary_topic_subfield_id": "primary_topic.subfield.id",
        "primary_topic_field_id": "primary_topic.field.id",
        "authorship_country": "a.countries",
        "citation_top10": "citation_normalized_percentile.is_in_top_10_percent",
    }

    # LIMIT 0 validates field binding without inspecting substantive values.
    for key, expr in probes.items():
        try:
            if key == "authorship_country":
                con.execute(
                    f"SELECT {expr} FROM read_parquet('{sql_path(glob)}', union_by_name=true), "
                    "UNNEST(authorships) AS u(a) LIMIT 0"
                )
            else:
                con.execute(
                    f"SELECT {expr} FROM read_parquet('{sql_path(glob)}', union_by_name=true) LIMIT 0"
                )
            nested_checks[key] = "OK"
        except Exception as exc:
            nested_checks[key] = f"FAIL: {type(exc).__name__}: {exc}"

    result = {
        "snapshot_root": str(root),
        "parquet_file_count": len(files),
        "top_level_columns": description.to_dict(orient="records"),
        "required_top_level_missing": missing,
        "nested_binding_checks": nested_checks,
        "safe_to_build_extractor": not missing and all(v == "OK" for v in nested_checks.values()),
        "note": "Schema-only probe; no country×discipline outcome aggregation performed.",
    }
    text = json.dumps(result, indent=2, default=str) + "\n"
    print(text)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")

    if not result["safe_to_build_extractor"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
