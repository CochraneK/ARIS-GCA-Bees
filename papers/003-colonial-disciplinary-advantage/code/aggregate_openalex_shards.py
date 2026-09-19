#!/usr/bin/env python3
"""Aggregate exact OpenAlex materialization shard outputs."""

from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
import duckdb

def q(v: object) -> str:
    return str(v).replace("'", "''")

def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):
            h.update(b)
    return h.hexdigest()

def paths_sql(paths: list[Path]) -> str:
    return "["+", ".join("'" + q(p) + "'" for p in paths)+"]"

def main() -> None:
    p=argparse.ArgumentParser()
    p.add_argument("--kind",choices=["country","dyad"],required=True)
    p.add_argument("--input-root",type=Path,required=True)
    p.add_argument("--output-dir",type=Path,required=True)
    a=p.parse_args()
    a.output_dir.mkdir(parents=True,exist_ok=True)
    con=duckdb.connect(database=":memory:")
    con.execute("SET preserve_insertion_order=false")

    if a.kind=="country":
        cells=sorted(a.input_root.rglob("COUNTRY_DISCIPLINE_WINDOW.parquet"))
        covs=sorted(a.input_root.rglob("COVERAGE_DIAGNOSTICS.parquet"))
        if not cells or len(cells)!=len(covs):
            raise SystemExit(f"country shard mismatch cells={len(cells)} coverage={len(covs)}")
        out=a.output_dir/"COUNTRY_DISCIPLINE_WINDOW.parquet"
        cov=a.output_dir/"COVERAGE_DIAGNOSTICS.parquet"
        con.execute(f"""
        COPY (
          SELECT iso3c, any_value(country) country, concept_id,
                 any_value(conceptual_discipline) conceptual_discipline, period,
                 sum(fractional_output) fractional_output,
                 sum(impact_denominator) impact_denominator,
                 sum(fractional_top10) fractional_top10,
                 sum(fwci_denominator) fwci_denominator,
                 sum(CASE WHEN fwci_denominator>0
                     THEN weighted_mean_fwci*fwci_denominator ELSE 0 END)
                   / NULLIF(sum(fwci_denominator),0) weighted_mean_fwci
          FROM read_parquet({paths_sql(cells)}, union_by_name=true)
          GROUP BY iso3c, concept_id, period
        ) TO '{q(out)}' (FORMAT PARQUET, COMPRESSION ZSTD)
        """)
        con.execute(f"""
        COPY (
          SELECT period, concept_id,
                 any_value(conceptual_discipline) conceptual_discipline,
                 sum(classified_works) classified_works,
                 sum(works_with_any_identifiable_country)
                   works_with_any_identifiable_country,
                 sum(works_with_primary_universe_country)
                   works_with_primary_universe_country,
                 sum(works_with_any_identifiable_country)
                   / NULLIF(sum(classified_works),0)
                   share_with_any_identifiable_country,
                 sum(works_with_primary_universe_country)
                   / NULLIF(sum(classified_works),0)
                   share_with_primary_universe_country
          FROM read_parquet({paths_sql(covs)}, union_by_name=true)
          GROUP BY period, concept_id
        ) TO '{q(cov)}' (FORMAT PARQUET, COMPRESSION ZSTD)
        """)
        audit={"status":"PASS","kind":"country","partial_shards":len(cells),
               "output_sha256":sha256(out),"coverage_sha256":sha256(cov)}
    else:
        files=sorted(a.input_root.rglob("DYAD_DISCIPLINE_WINDOW_POSITIVE.parquet"))
        if not files:
            raise SystemExit("no dyad shard files")
        out=a.output_dir/"DYAD_DISCIPLINE_WINDOW_POSITIVE.parquet"
        con.execute(f"""
        COPY (
          SELECT pair_id, iso3_i, iso3_j, concept_id,
                 any_value(conceptual_discipline) conceptual_discipline, period,
                 sum(fractional_collaboration_mass)
                   fractional_collaboration_mass,
                 sum(raw_coauthored_works) raw_coauthored_works
          FROM read_parquet({paths_sql(files)}, union_by_name=true)
          GROUP BY pair_id, iso3_i, iso3_j, concept_id, period
        ) TO '{q(out)}' (FORMAT PARQUET, COMPRESSION ZSTD)
        """)
        audit={"status":"PASS","kind":"dyad","partial_shards":len(files),
               "output_sha256":sha256(out)}

    (a.output_dir/f"{a.kind.upper()}_SHARD_AGGREGATION_AUDIT.json").write_text(
        json.dumps(audit,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(audit,indent=2))

if __name__=="__main__":
    main()
