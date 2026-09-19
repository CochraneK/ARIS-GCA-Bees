#!/usr/bin/env python3
"""Materialize positive OpenAlex country-pair collaboration cells.

THIS IS A CONFIRMATORY-OUTCOME SCRIPT and is hard-gated.

Frozen multilateral-work rule:
If a work contains n distinct identifiable OpenAlex countries (n>=2), it
contributes total scientific-collaboration mass 1 across all n*(n-1)/2
unordered country pairs. Thus each pair receives 2/[n(n-1)] **before**
restricting endpoints to the frozen 159-country analysis universe. A work that
also contains an out-of-universe country therefore contributes less than total
mass 1 to the retained analysis pairs, rather than being renormalized upward.

The output contains positive observed dyadic mass only. The confirmatory model
must complete the eligible pair×discipline×period grid with genuine zeros using
the frozen CEPII country-pair universe before PPML estimation.

The OpenAlex Works source may be either a local Parquet snapshot root or an
anonymous public-S3 Parquet glob.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import duckdb

PAPER = Path(__file__).resolve().parents[1]
CODE = PAPER / "code"
PROCESS = PAPER / "process"
DATA = PAPER / "data"
WORK_TYPES = ("article", "review", "conference-paper", "book", "book-chapter")


def q(value: object) -> str:
    return str(value).replace("'", "''")


def prepare_source(source_arg: str) -> tuple[str, list[str]]:
    if source_arg.startswith("s3://"):
        return source_arg, [
            sys.executable,
            str(CODE / "preoutcome_gate.py"),
            "--strict",
        ]

    root = Path(source_arg).expanduser().resolve()
    return str(root / "**" / "*.parquet"), [
        sys.executable,
        str(CODE / "preoutcome_gate.py"),
        "--snapshot-root",
        str(root),
        "--strict",
    ]


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument(
        "snapshot_root",
        help=(
            "local Works Parquet root or public S3 parquet glob, e.g. "
            "s3://openalex/data/parquet/works/**/*.parquet"
        ),
    )
    p.add_argument(
        "--output",
        type=Path,
        default=(
            DATA
            / "derived"
            / "openalex"
            / "DYAD_DISCIPLINE_WINDOW_POSITIVE.parquet"
        ),
    )
    args = p.parse_args()

    source_arg = str(args.snapshot_root)
    parquet_source, gate_cmd = prepare_source(source_arg)
    subprocess.run(gate_cmd, check=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)

    crosswalk = PROCESS / "DISCIPLINE_CROSSWALK.csv"
    countries = DATA / "derived" / "COUNTRY_CROSSWALK.csv"
    types_sql = ",".join("'" + x.replace("'", "''") + "'" for x in WORK_TYPES)

    con = duckdb.connect(database=":memory:")
    con.execute("SET preserve_insertion_order=false")
    if source_arg.startswith("s3://"):
        con.execute("INSTALL httpfs")
        con.execute("LOAD httpfs")

    con.execute(
        f"""
        CREATE TEMP TABLE concept_map AS
        SELECT
            concept_id,
            conceptual_discipline,
            selector_level,
            trim(oa_id) AS oa_id
        FROM read_csv_auto('{q(crosswalk)}'),
             UNNEST(string_split(openalex_ids, ';')) AS u(oa_id);
        """
    )
    con.execute(
        f"""
        CREATE TEMP TABLE country_map AS
        SELECT upper(openalex_iso2) AS iso2, upper(iso3c) AS iso3c
        FROM read_csv_auto('{q(countries)}')
        WHERE status = 'RESOLVED';
        """
    )

    source = (
        f"read_parquet('{q(parquet_source)}', "
        "union_by_name=true, hive_partitioning=true)"
    )
    sql = f"""
    COPY (
        WITH eligible AS (
            SELECT id AS work_id, publication_year, primary_topic, authorships
            FROM {source}
            WHERE publication_year BETWEEN 2007 AND 2025
              AND type IN ({types_sql})
              AND COALESCE(is_retracted, FALSE) = FALSE
              AND COALESCE(is_xpac, FALSE) = FALSE
              AND primary_topic IS NOT NULL
        ),
        classified AS (
            SELECT
                e.work_id,
                e.publication_year,
                e.authorships,
                m.concept_id,
                m.conceptual_discipline,
                CASE
                    WHEN publication_year BETWEEN 2007 AND 2010 THEN '2007-2010'
                    WHEN publication_year BETWEEN 2011 AND 2014 THEN '2011-2014'
                    WHEN publication_year BETWEEN 2015 AND 2018 THEN '2015-2018'
                    WHEN publication_year BETWEEN 2019 AND 2022 THEN '2019-2022'
                    WHEN publication_year BETWEEN 2023 AND 2025 THEN '2023-2025'
                END AS period
            FROM eligible e
            JOIN concept_map m
              ON (
                  starts_with(m.selector_level, 'subfield')
                  AND regexp_extract(
                      CAST(e.primary_topic.subfield.id AS VARCHAR),
                      '([0-9]+)$',
                      1
                  ) = m.oa_id
              ) OR (
                  m.selector_level = 'field'
                  AND regexp_extract(
                      CAST(e.primary_topic.field.id AS VARCHAR),
                      '([0-9]+)$',
                      1
                  ) = m.oa_id
              )
        ),
        work_country_all AS (
            SELECT DISTINCT
                c.work_id,
                c.period,
                c.concept_id,
                c.conceptual_discipline,
                upper(country_code) AS iso2
            FROM classified c
            CROSS JOIN UNNEST(c.authorships) AS au(a)
            CROSS JOIN UNNEST(a.countries) AS cc(country_code)
            WHERE country_code IS NOT NULL
        ),
        sized_all AS (
            SELECT
                *,
                COUNT(*) OVER (PARTITION BY work_id) AS n_all_identifiable_countries
            FROM work_country_all
        ),
        mapped AS (
            SELECT
                w.work_id,
                w.period,
                w.concept_id,
                w.conceptual_discipline,
                w.n_all_identifiable_countries,
                cm.iso3c
            FROM sized_all w
            JOIN country_map cm USING (iso2)
        ),
        pairs AS (
            SELECT
                a.work_id,
                a.period,
                a.concept_id,
                a.conceptual_discipline,
                a.iso3c AS iso3_i,
                b.iso3c AS iso3_j,
                2.0 / (
                    a.n_all_identifiable_countries
                    * (a.n_all_identifiable_countries - 1)
                ) AS pair_weight
            FROM mapped a
            JOIN mapped b
              ON a.work_id = b.work_id
             AND a.iso3c < b.iso3c
            WHERE a.n_all_identifiable_countries >= 2
        )
        SELECT
            iso3_i || '__' || iso3_j AS pair_id,
            iso3_i,
            iso3_j,
            concept_id,
            conceptual_discipline,
            period,
            SUM(pair_weight) AS fractional_collaboration_mass,
            COUNT(DISTINCT work_id) AS raw_coauthored_works
        FROM pairs
        GROUP BY
            iso3_i,
            iso3_j,
            concept_id,
            conceptual_discipline,
            period
    ) TO '{q(args.output)}' (FORMAT PARQUET, COMPRESSION ZSTD);
    """
    con.execute(sql)
    print(args.output)
    print(
        "Pair weighting frozen at total dyadic mass = 1 per multilateral work. "
        f"source={parquet_source}"
    )


if __name__ == "__main__":
    main()
