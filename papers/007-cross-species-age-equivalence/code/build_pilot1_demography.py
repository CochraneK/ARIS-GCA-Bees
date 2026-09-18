#!/usr/bin/env python3
"""ARIS4C007 Pilot 1: independent demographic-event benchmark.

Canonical data flow:
- Pilot 0 is the sole producer of the pinned AnAge-derived life-history inputs.
- Pilot 1 consumes the latest successful Pilot 0 artifact.
- Péron et al. 2019 S5 supplies independent mortality-curve events.

The outcome is cross-species concentration of mapped ages for independently
estimated demographic events. It does not designate a globally "correct" age
mapping.
"""

from __future__ import annotations

import argparse
import csv
import json
import random
import re
import statistics
from collections import defaultdict
from pathlib import Path

from openpyxl import load_workbook

from age_mappings import SpeciesTime, map_by_loglinear, map_by_relative_age
from build_pilot0 import read_anage, species_time


EST_RE = re.compile(r"^\s*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)")


def estimate(value) -> float:
    if value is None:
        raise ValueError("missing estimate")
    if isinstance(value, (int, float)):
        return float(value)
    match = EST_RE.match(str(value))
    if not match:
        raise ValueError(f"cannot parse estimate: {value!r}")
    return float(match.group(1))


def quantile(values: list[float], p: float) -> float:
    xs = sorted(values)
    pos = (len(xs) - 1) * p
    lo = int(pos)
    hi = min(lo + 1, len(xs) - 1)
    frac = pos - lo
    return xs[lo] * (1 - frac) + xs[hi] * frac


def mad(values: list[float]) -> float:
    med = statistics.median(values)
    return statistics.median(abs(x - med) for x in values)


def dispersion(values: list[float]) -> dict[str, float]:
    return {
        "median_human_y": statistics.median(values),
        "mad_human_y": mad(values),
        "iqr_human_y": quantile(values, 0.75) - quantile(values, 0.25),
        "sd_human_y": statistics.stdev(values) if len(values) > 1 else 0.0,
        "min_human_y": min(values),
        "max_human_y": max(values),
    }


def bootstrap_mad_difference(
    a1: list[float],
    a3: list[float],
    *,
    seed: int,
    reps: int = 10000,
) -> dict[str, object]:
    """Paired species bootstrap for MAD(A3) - MAD(A1)."""
    if len(a1) != len(a3):
        raise ValueError("paired vectors must have equal length")
    rng = random.Random(seed)
    n = len(a1)
    diffs = []
    for _ in range(reps):
        idx = [rng.randrange(n) for _ in range(n)]
        b1 = [a1[i] for i in idx]
        b3 = [a3[i] for i in idx]
        diffs.append(mad(b3) - mad(b1))
    diffs.sort()
    return {
        "observed_mad_difference_A3_minus_A1_y": mad(a3) - mad(a1),
        "bootstrap_reps": reps,
        "bootstrap_95pct_interval_y": [
            quantile(diffs, 0.025),
            quantile(diffs, 0.975),
        ],
    }


def load_complete_anage(path: Path) -> dict[str, SpeciesTime]:
    """Fallback/local path for direct raw-AnAge runs."""
    out = {}
    for row in read_anage(path):
        if row.get("Class") != "Mammalia":
            continue
        s = species_time(row)
        if s is not None:
            out[s.name] = s
    return out


def load_pilot0_species(
    grid_path: Path,
    coverage_path: Path,
) -> tuple[dict[str, SpeciesTime], dict[str, object]]:
    """Reconstruct Pilot-0 SpeciesTime inputs from its canonical artifact.

    Pilot 0 currently publishes mapping outputs rather than a direct trait table.
    The underlying three inputs are algebraically identifiable from that grid:

    - maturity_y = source age in the sexual-maturity row
    - max_lifespan_y = 2 * source age in the 50%-maximum-lifespan row
    - gestation_y is recovered from the published A1 mapped age and checked by
      reproducing both A1 and A3 outputs.

    The strict reproduction check turns any future Pilot-0 schema/formula change
    into a loud failure instead of silently changing Pilot 1.
    """
    coverage = json.loads(coverage_path.read_text(encoding="utf-8"))
    human_raw = coverage["seed_species_found"]["Homo sapiens"]
    human = SpeciesTime(
        name="Homo sapiens",
        gestation_y=float(human_raw["gestation_y"]),
        maturity_y=float(human_raw["maturity_y"]),
        max_lifespan_y=float(human_raw["max_lifespan_y"]),
    )
    human.validate()

    with grid_path.open("r", encoding="utf-8", newline="") as fh:
        grid = list(csv.DictReader(fh))

    by_species: dict[str, dict[str, dict[str, str]]] = defaultdict(dict)
    for row in grid:
        by_species[row["species"]][row["stage"]] = row

    species: dict[str, SpeciesTime] = {"Homo sapiens": human}
    max_reproduction_error = 0.0

    required_stages = {
        "sexual_maturity",
        "max_fraction_0.50",
    }

    for name, rows in by_species.items():
        missing = required_stages - set(rows)
        if missing:
            raise RuntimeError(f"{name}: Pilot 0 artifact missing stages {sorted(missing)}")

        maturity_y = float(rows["sexual_maturity"]["source_age_y"])
        half = rows["max_fraction_0.50"]
        half_age_y = float(half["source_age_y"])
        max_lifespan_y = 2.0 * half_age_y

        mapped_human_y = float(half["human_age_relative_lifespan_y"])
        r = (
            mapped_human_y + human.gestation_y
        ) / (
            human.max_lifespan_y + human.gestation_y
        )
        if not 0.0 < r < 1.0:
            raise RuntimeError(f"{name}: invalid recovered relative age {r}")

        gestation_y = (
            r * max_lifespan_y - half_age_y
        ) / (
            1.0 - r
        )
        s = SpeciesTime(
            name=name,
            gestation_y=gestation_y,
            maturity_y=maturity_y,
            max_lifespan_y=max_lifespan_y,
        )
        s.validate()

        # Reproduce every Pilot-0 row for this species using the recovered inputs.
        for row in rows.values():
            age_y = float(row["source_age_y"])
            expected_a1 = float(row["human_age_relative_lifespan_y"])
            expected_a3 = float(row["human_age_loglinear_y"])
            got_a1 = map_by_relative_age(age_y, s, human)
            got_a3 = map_by_loglinear(age_y, s, human)
            max_reproduction_error = max(
                max_reproduction_error,
                abs(got_a1 - expected_a1),
                abs(got_a3 - expected_a3),
            )

        species[name] = s

    if max_reproduction_error > 1e-8:
        raise RuntimeError(
            "Pilot 0 artifact could not be exactly reproduced; "
            f"max error={max_reproduction_error}"
        )

    expected_complete = int(
        coverage["mammals_complete_gestation_maturity_max_lifespan"]
    )
    if len(species) != expected_complete:
        raise RuntimeError(
            f"Pilot 0 coverage expected {expected_complete} complete mammals, "
            f"reconstructed {len(species)}"
        )

    provenance = {
        "source": "pilot0_artifact",
        "grid_path": str(grid_path),
        "coverage_path": str(coverage_path),
        "complete_mammals_including_human": len(species),
        "artifact_mapping_rows": len(grid),
        "max_reproduction_error_y": max_reproduction_error,
        "human_reference": {
            "gestation_y": human.gestation_y,
            "maturity_y": human.maturity_y,
            "max_lifespan_y": human.max_lifespan_y,
        },
    }
    return species, provenance


def load_peron(path: Path) -> list[dict[str, object]]:
    wb = load_workbook(path, read_only=True, data_only=True)
    ws = wb[wb.sheetnames[0]]
    rows = list(ws.iter_rows(values_only=True))
    header = [str(x) for x in rows[0]]
    return [dict(zip(header, row)) for row in rows[1:] if row[0]]


def main() -> None:
    ap = argparse.ArgumentParser()
    source = ap.add_mutually_exclusive_group(required=True)
    source.add_argument("--anage", type=Path)
    source.add_argument("--pilot0-grid", type=Path)
    ap.add_argument("--pilot0-coverage", type=Path)
    ap.add_argument("--peron-s5", type=Path, required=True)
    ap.add_argument("--out", type=Path, default=Path("data/pilot1_demography"))
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    if args.pilot0_grid is not None:
        if args.pilot0_coverage is None:
            ap.error("--pilot0-coverage is required with --pilot0-grid")
        anage, upstream = load_pilot0_species(
            args.pilot0_grid,
            args.pilot0_coverage,
        )
    else:
        anage = load_complete_anage(args.anage)
        upstream = {
            "source": "direct_anage_fallback",
            "path": str(args.anage),
            "complete_mammals_including_human": len(anage),
        }

    human = anage["Homo sapiens"]
    peron = load_peron(args.peron_s5)

    output = []
    unmatched = []
    for row in peron:
        name = str(row["Species"]).strip()
        source_species = anage.get(name)
        if source_species is None:
            unmatched.append(name)
            continue

        juvenile_end = estimate(row["A"])
        prime_duration = estimate(row["Omegatilde"])
        senescence_onset = juvenile_end + prime_duration
        a10 = estimate(row["A10"])

        events = {
            "juvenile_stage_end_A": juvenile_end,
            "actuarial_senescence_onset_Omega": senescence_onset,
            "A10_10pct_survival": a10,
        }

        for event, age in events.items():
            a1 = map_by_relative_age(age, source_species, human)
            a3 = map_by_loglinear(age, source_species, human)
            output.append(
                {
                    "species": name,
                    "preferred_mortality_model": row["pref model"],
                    "event": event,
                    "source_event_age_y": age,
                    "A1_relative_lifespan_human_y": a1,
                    "A3_loglinear_human_y": a3,
                    "A3_minus_A1_y": a3 - a1,
                    "absolute_A1_A3_difference_y": abs(a3 - a1),
                }
            )

    if not output:
        raise RuntimeError("No Péron species overlapped the life-history source")

    csv_path = args.out / "demography_event_mapping.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(output[0]))
        writer.writeheader()
        writer.writerows(output)

    by_event = defaultdict(list)
    for row in output:
        by_event[row["event"]].append(row)

    event_summary = {}
    for event_index, (event, group) in enumerate(sorted(by_event.items())):
        a1 = [float(r["A1_relative_lifespan_human_y"]) for r in group]
        a3 = [float(r["A3_loglinear_human_y"]) for r in group]
        event_summary[event] = {
            "n_species": len(group),
            "A1_relative_lifespan": dispersion(a1),
            "A3_loglinear": dispersion(a3),
            "paired_bootstrap_mad_difference": bootstrap_mad_difference(
                a1,
                a3,
                seed=20260918 + event_index,
            ),
            "note": (
                "Lower cross-species dispersion is a necessary-style coherence "
                "diagnostic for a homologous event, not proof of biological truth."
            ),
        }

    summary = {
        "peron_species_rows": len(peron),
        "life_history_complete_mammals_including_human": len(anage),
        "exact_overlap_species": len({r["species"] for r in output}),
        "unmatched_or_incomplete_species": unmatched,
        "upstream_life_history": upstream,
        "event_summary": event_summary,
        "definitions": {
            "Omega": (
                "A + Omegatilde, where Omegatilde is duration of the "
                "prime-age stage in the Péron table."
            ),
            "A10": (
                "predicted age at which 90% of the cohort is dead "
                "(10% survival)."
            ),
        },
        "guardrail": (
            "Péron demographic parameters are independent of the life-history "
            "traits used to construct A1/A3, but population/captive conditions "
            "and event homology remain substantive limitations."
        ),
    }
    (args.out / "demography_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
