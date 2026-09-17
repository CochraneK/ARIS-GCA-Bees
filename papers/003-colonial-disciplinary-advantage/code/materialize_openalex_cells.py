#!/usr/bin/env python3
"""Materialize preregistered OpenAlex country×discipline×window cells.

THIS IS A CONFIRMATORY-OUTCOME SCRIPT. It refuses to run unless
`preoutcome_gate.py --strict` passes. Do not bypass the gate.

Primary rules implemented here:
- OpenAlex public Parquet Works snapshot;
- publication years 2007-2025 (2023-25 output-only sensitivity retained);
- article, review, conference-paper, book, book-chapter;
- exclude retracted and expansion-corpus (`is_xpac`) works;
- discipline = frozen concept matched through the work's single primary_topic;
- country credit = 1 / number of ALL distinct identifiable OpenAlex countries
  on the work, computed before restricting to the primary COLDAT-anchored
  sovereign-state universe;
- current-state analysis universe = audited COLDAT-anchored ISO2↔ISO3 crosswalk.
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


def q(path: Path) -> str:
    return str(path).replace("'", "''")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("snapshot_root", type=Path)
    p.add_argument("--output-dir", type=Path, default=DATA / "derived" / "openalex")
    args = p.parse_args()

    root = args.snapshot_root.expanduser().resolve()
    subprocess.run(
        [
            sys.executable,
            str(CODE / "preoutcome_gate.py"),
            "--snapshot-root",
            str(root),
            "--strict",
        ],
        check=True,
    )

    glob = root / "**" / "*.parquet"
    crosswalk = PROCESS / "DISCIPLINE_CROSSWALK.csv"
    countries = DATA / "derived" / "COUNTRY_CROSSWALK.csv"
    args.output_dir.mkdir(parents=True, exist_ok=True)
    cells_out = args.output_dir / "COUNTRY_DISCIPLINE_WINDOW.parquet"
    coverage_out = args.output_dir / "COVERAGE_DIAGNOSTICS.parquet"

    types_sql = ",".join("'" + x.replace("'", "''") + "'" for x in WORK_TYPES)
    con = duckdb.connect(database=":memory:")
    con.execute("SET preserve_insertion_order=false")

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
        SELECT upper(openalex_iso2) AS iso2, upper(iso3c) AS iso3c, country
        FROM read_csv_auto('{q(countries)}')
        WHERE status = 'RESOLVED';
        """
    )

    work_source = f"read_parquet('{q(glob)}', union_by_name=true)"
    base_sql = f"""
        WITH eligible AS (
            SELECT
                id AS work_id,
                publication_year,
                type,
                language,
                primary_topic,
                authorships,
                citation_normalized_percentile,
                fwci
            FROM {work_source}
            WHERE publication_year BETWEEN 2007 AND 2025
              AND type IN ({types_sql})
              AND COALESCE(is_retracted, FALSE) = FALSE
              AND COALESCE(is_xpac, FALSE) = FALSE
              AND primary_topic IS NOT NULL
        ),
        classified AS (
            SELECT
                e.*,
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
                  AND regexp_extract(CAST(e.primary_topic.subfield.id AS VARCHAR), '([0-9]+)$', 1) = m.oa_id
              ) OR (
                  m.selector_level = 'field'
                  AND regexp_extract(CAST(e.primary_topic.field.id AS VARCHAR), '([0-9]+)$', 1) = m.oa_id
              )
        ),
        work_country_unique AS (
            SELECT DISTINCT
                c.work_id,
                c.publication_year,
                c.period,
                c.type,
                c.language,
                c.concept_id,
                c.conceptual_discipline,
                c.fwci,
                c.citation_normalized_percentile.is_in_top_10_percent AS is_top10,
                upper(country_code) AS iso2
            FROM classified c
            CROSS JOIN UNNEST(c.authorships) AS au(a)
            CROSS JOIN UNNEST(a.countries) AS cc(country_code)
            WHERE country_code IS NOT NULL
        ),
        country_sized AS (
            SELECT
                *,
                COUNT(*) OVER (PARTITION BY work_id) AS n_all_identifiable_countries
            FROM work_country_unique
        ),
        mapped AS (
            SELECT
                w.*,
                cm.iso3c,
                cm.country
            FROM country_sized w
            JOIN country_map cm USING (iso2)
        ),
        weighted AS (
            SELECT
                *,
                1.0 / n_all_identifiable_countries AS country_weight
            FROM mapped
        ),
        country_coverage AS (
            SELECT
                work_id,
                MAX(n_all_identifiable_countries) AS n_all_identifiable_countries,
                COUNT(*) AS n_mapped_primary_universe_countries
            FROM mapped
            GROUP BY work_id
        )
    """

    # A work must map to at most one frozen concept. This is checked before COPY.
    duplicate_concepts = con.execute(
        base_sql
        + """
        SELECT COUNT(*) FROM (
            SELECT work_id
            FROM classified
            GROUP BY work_id
            HAVING COUNT(DISTINCT concept_id) > 1
        );
        """
    ).fetchone()[0]
    if duplicate_concepts:
        raise SystemExit(
            f"Crosswalk exclusivity failure: {duplicate_concepts} works matched >1 concept"
        )

    con.execute(
        base_sql
        + f"""
        COPY (
            SELECT
                iso3c,
                country,
                concept_id,
                conceptual_discipline,
                period,
                SUM(country_weight) AS fractional_output,
                SUM(CASE WHEN is_top10 IS NOT NULL THEN country_weight ELSE 0 END) AS impact_denominator,
                SUM(CASE WHEN is_top10 = TRUE THEN country_weight ELSE 0 END) AS fractional_top10,
                SUM(CASE WHEN fwci IS NOT NULL THEN country_weight ELSE 0 END) AS fwci_denominator,
                SUM(CASE WHEN fwci IS NOT NULL THEN country_weight * fwci ELSE 0 END)
                  / NULLIF(SUM(CASE WHEN fwci IS NOT NULL THEN country_weight ELSE 0 END), 0)
                  AS weighted_mean_fwci
            FROM weighted
            GROUP BY iso3c, country, concept_id, conceptual_discipline, period
        ) TO '{q(cells_out)}' (FORMAT PARQUET, COMPRESSION ZSTD);
        """
    )

    # Coverage diagnostics do not merge historical exposure or estimate effects.
    con.execute(
        base_sql
        + f"""
        COPY (
            SELECT
                c.period,
                c.concept_id,
                c.conceptual_discipline,
                COUNT(DISTINCT c.work_id) AS classified_works,
                COUNT(DISTINCT CASE WHEN s.n_all_identifiable_countries > 0 THEN c.work_id END)
                  AS works_with_any_identifiable_country,
                COUNT(DISTINCT CASE WHEN cov.n_mapped_primary_universe_countries > 0 THEN c.work_id END)
                  AS works_with_primary_universe_country,
                AVG(CASE WHEN s.n_all_identifiable_countries > 0 THEN 1.0 ELSE 0.0 END)
                  AS share_with_any_identifiable_country,
                AVG(CASE WHEN cov.n_mapped_primary_universe_countries > 0 THEN 1.0 ELSE 0.0 END)
                  AS share_with_primary_universe_country
            FROM classified c
            LEFT JOIN (
                SELECT work_id, MAX(n_all_identifiable_countries) AS n_all_identifiable_countries
                FROM country_sized
                GROUP BY work_id
            ) s USING (work_id)
            LEFT JOIN country_coverage cov USING (work_id)
            GROUP BY c.period, c.concept_id, c.conceptual_discipline
        ) TO '{q(coverage_out)}' (FORMAT PARQUET, COMPRESSION ZSTD);
        """
    )

    print(cells_out)
    print(coverage_out)
    print("Confirmatory outcome cells materialized under a passed hard gate.")


if __name__ == "__main__":
    main()
