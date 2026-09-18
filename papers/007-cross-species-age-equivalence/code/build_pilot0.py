#!/usr/bin/env python3
"""Build the low-cost ARIS4C007 life-history benchmark from AnAge.

Usage:
    python build_pilot0.py path/to/anage_data.txt --out data/pilot0

The script does not download data. Use download_public_sources.py or the
official AnAge download page. Raw data should remain immutable.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from age_mappings import SpeciesTime, map_by_loglinear, map_by_relative_age


DAYS_PER_YEAR = 365.25
SEED_SPECIES = [
    "Homo sapiens",
    "Pan troglodytes",
    "Macaca mulatta",
    "Canis lupus",
    "Felis catus",
    "Mus musculus",
    "Rattus norvegicus",
    "Oryctolagus cuniculus",
    "Ovis aries",
    "Heterocephalus glaber",
]


def _num(value: str | None) -> float | None:
    if value is None:
        return None
    value = value.strip()
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def _mean_present(*values: float | None) -> float | None:
    xs = [x for x in values if x is not None]
    return sum(xs) / len(xs) if xs else None


def read_anage(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def species_time(row: dict[str, str]) -> SpeciesTime | None:
    gest = _num(row.get("Gestation/Incubation (days)"))
    female = _num(row.get("Female maturity (days)"))
    male = _num(row.get("Male maturity (days)"))
    maturity = _mean_present(female, male)
    longevity = _num(row.get("Maximum longevity (yrs)"))
    if gest is None or maturity is None or longevity is None:
        return None
    name = f"{row.get('Genus','').strip()} {row.get('Species','').strip()}".strip()
    s = SpeciesTime(
        name=name,
        gestation_y=gest / DAYS_PER_YEAR,
        maturity_y=maturity / DAYS_PER_YEAR,
        max_lifespan_y=longevity,
    )
    s.validate()
    return s


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("anage", type=Path)
    parser.add_argument("--out", type=Path, default=Path("data/pilot0"))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    rows = read_anage(args.anage)
    mammals = [r for r in rows if r.get("Class") == "Mammalia"]

    complete: dict[str, tuple[SpeciesTime, dict[str, str]]] = {}
    for row in mammals:
        s = species_time(row)
        if s is not None:
            complete[s.name] = (s, row)

    if "Homo sapiens" not in complete:
        raise RuntimeError("Homo sapiens with complete timing traits is required")
    human = complete["Homo sapiens"][0]

    stages = [
        ("sexual_maturity", lambda s: s.maturity_y),
        ("max_fraction_0.25", lambda s: 0.25 * s.max_lifespan_y),
        ("max_fraction_0.50", lambda s: 0.50 * s.max_lifespan_y),
        ("max_fraction_0.75", lambda s: 0.75 * s.max_lifespan_y),
    ]

    output_rows: list[dict[str, object]] = []
    for name, (s, raw) in sorted(complete.items()):
        if name == human.name:
            continue
        for stage_name, age_fn in stages:
            age = age_fn(s)
            rel_h = map_by_relative_age(age, s, human)
            loglin_h = map_by_loglinear(age, s, human)
            output_rows.append(
                {
                    "species": name,
                    "common_name": raw.get("Common name", ""),
                    "order": raw.get("Order", ""),
                    "data_quality": raw.get("Data quality", raw.get("Dataquality", "")),
                    "stage": stage_name,
                    "source_age_y": age,
                    "human_age_relative_lifespan_y": rel_h,
                    "human_age_loglinear_y": loglin_h,
                    "absolute_disagreement_y": abs(rel_h - loglin_h),
                    "normalized_disagreement_human_max": abs(rel_h - loglin_h)
                    / human.max_lifespan_y,
                }
            )

    mapping_path = args.out / "life_history_mapping_grid.csv"
    fieldnames = list(output_rows[0])
    with mapping_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)

    seed = {}
    for name in SEED_SPECIES:
        if name in complete:
            s, raw = complete[name]
            seed[name] = {
                "gestation_y": s.gestation_y,
                "maturity_y": s.maturity_y,
                "max_lifespan_y": s.max_lifespan_y,
                "data_quality": raw.get("Data quality", raw.get("Dataquality", "")),
            }

    summary = {
        "source_file": str(args.anage),
        "all_rows": len(rows),
        "mammal_rows": len(mammals),
        "mammals_complete_gestation_maturity_max_lifespan": len(complete),
        "mapping_rows": len(output_rows),
        "seed_species_found": seed,
        "warning": (
            "Outputs compare candidate coordinates only. They are not estimates of "
            "a true human-equivalent age."
        ),
    }
    (args.out / "coverage_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
