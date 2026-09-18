#!/usr/bin/env python3
"""Probe OpenAlex Works Parquet schema without materializing outcomes.

Allowed while the confirmatory outcome gate is locked. The source may be a
local OpenAlex Works Parquet snapshot root or one public S3 Works Parquet
object. The probe performs no country-by-discipline aggregation and uses
LIMIT 0 for nested-field binding checks.
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


def sql_path(value: object) -> str:
    return str(value).replace("'", "''")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "snapshot_root",
        help="local snapshot root or one public s3://...parquet Works object",
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    source_arg = str(args.snapshot_root)
    con = duckdb.connect(database=":memory:")

    if source_arg.startswith("s3://"):
        con.execute("INSTALL httpfs")
        con.execute("LOAD httpfs")
        source_label = source_arg
        file_count = 1
        read_expr = f"read_parquet('{sql_path(source_arg)}')"
    else:
        root = Path(source_arg).expanduser().resolve()
        files = list(root.rglob("*.parquet"))
        if not files:
            raise SystemExit(f"No .parquet files under {root}")
        source_label = str(root)
        file_count = len(files)
        glob = root / "**" / "*.parquet"
        read_expr = f"read_parquet('{sql_path(glob)}', union_by_name=true)"

    description = con.execute(
        f"DESCRIBE SELECT * FROM {read_expr}"
    ).fetchdf()
    columns = set(description["column_name"].astype(str))
    missing = sorted(REQUIRED_TOP_LEVEL - columns)

    nested_checks: dict[str, str] = {}
    probes = {
        "primary_topic_subfield_id": "primary_topic.subfield.id",
        "primary_topic_field_id": "primary_topic.field.id",
        "authorship_country": "a.countries",
        "citation_top10": "citation_normalized_percentile.is_in_top_10_percent",
    }

    for key, expr in probes.items():
        try:
            if key == "authorship_country":
                con.execute(
                    f"SELECT {expr} FROM {read_expr}, "
                    "UNNEST(authorships) AS u(a) LIMIT 0"
                )
            else:
                con.execute(f"SELECT {expr} FROM {read_expr} LIMIT 0")
            nested_checks[key] = "OK"
        except Exception as exc:
            nested_checks[key] = f"FAIL: {type(exc).__name__}: {exc}"

    result = {
        "snapshot_root": source_label,
        "parquet_file_count": file_count,
        "top_level_columns": description.to_dict(orient="records"),
        "required_top_level_missing": missing,
        "nested_binding_checks": nested_checks,
        "safe_to_build_extractor": (
            not missing and all(v == "OK" for v in nested_checks.values())
        ),
        "note": (
            "Schema-only probe; no country-by-discipline outcome aggregation "
            "performed."
        ),
    }
    text_out = json.dumps(result, indent=2, default=str) + "\n"
    print(text_out)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text_out, encoding="utf-8")

    if not result["safe_to_build_extractor"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
