#!/usr/bin/env python3
"""Distributed executor for the frozen ARIS4C003 confirmatory models.

This module imports the canonical model definitions and fit function from
run_confirmatory_models.py. It changes only execution topology, not estimands.

Components:
- core: primary/pooled/temporal/volume/median fits, no permutation or LOO;
- loo: all 21 leave-one-discipline fits for one headline model;
- permutation: a deterministic inclusive repetition range for one headline
  model, reproducing the canonical seed-20260918 permutation sequence.

No failed refit is silently removed.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

import run_confirmatory_models as r

MODEL_KEYS = {
    "output": "output_primary",
    "impact": "impact_primary",
    "dyad": "dyad_primary",
}


def load_inputs(country_path: Path, dyad_path: Path):
    country = r.read_parquet(country_path)
    dyad = r.read_parquet(dyad_path)
    r.validate_concepts(country, "country panel")
    r.validate_concepts(dyad, "dyad panel")
    country = r.with_country_interaction(country)
    dyad = r.with_dyad_interaction(dyad)
    return country, dyad


def headline_data(country: pd.DataFrame, dyad: pd.DataFrame, name: str):
    specs = r.model_specs()
    if name == "output":
        data = country[country["period"].eq(r.PRIMARY_PERIOD)].copy()
    elif name == "impact":
        data = country[
            country["period"].eq(r.PRIMARY_PERIOD)
            & (country["impact_denominator"] > 0)
        ].copy()
    elif name == "dyad":
        data = dyad[dyad["period"].eq(r.PRIMARY_PERIOD)].copy()
    else:
        raise ValueError(name)
    return specs[MODEL_KEYS[name]], data


def run_core(country: pd.DataFrame, dyad: pd.DataFrame, out: Path) -> None:
    specs = r.model_specs()
    country_primary = country[country["period"].eq(r.PRIMARY_PERIOD)].copy()
    country_pooled = country[country["period"].isin(r.CONFIRMATORY_PERIODS)].copy()
    impact_primary = country_primary[country_primary["impact_denominator"] > 0].copy()
    impact_pooled = country_pooled[country_pooled["impact_denominator"] > 0].copy()
    dyad_primary = dyad[dyad["period"].eq(r.PRIMARY_PERIOD)].copy()
    dyad_pooled = dyad[dyad["period"].isin(r.CONFIRMATORY_PERIODS)].copy()

    jobs = [
        (specs["output_primary"], country_primary, "2019-2022 primary"),
        (specs["impact_primary"], impact_primary, "2019-2022 primary"),
        (specs["dyad_primary"], dyad_primary, "2019-2022 primary"),
        (specs["output_pooled"], country_pooled, "2007-2022 pooled persistence"),
        (specs["impact_pooled"], impact_pooled, "2007-2022 pooled persistence"),
        (specs["dyad_pooled"], dyad_pooled, "2007-2022 pooled persistence"),
    ]
    rows = []
    for spec, data, label in jobs:
        fit = r.fit_ppml(spec, data)
        rows.append(r.extract_result(fit, spec, data, label))
    pd.DataFrame(rows).to_csv(out / "CORE_MODELS.csv", index=False)

    temporal = []
    for period in r.PERSISTENCE_PERIODS:
        ospec, ispec, dspec = r.single_period_specs(period)
        cd = country[country["period"].eq(period)].copy()
        idf = cd[cd["impact_denominator"] > 0].copy()
        dd = dyad[dyad["period"].eq(period)].copy()
        temporal.append(r.safe_secondary_fit(ospec, cd, f"{period} temporal output"))
        temporal.append(r.safe_secondary_fit(ispec, idf, f"{period} temporal Top10 impact"))
        temporal.append(r.safe_secondary_fit(dspec, dd, f"{period} temporal dyad"))
    recent = country[country["period"].eq(r.RECENT_OUTPUT_PERIOD)].copy()
    rspec, _, _ = r.single_period_specs(r.RECENT_OUTPUT_PERIOD)
    temporal.append(
        r.safe_secondary_fit(
            rspec, recent, f"{r.RECENT_OUTPUT_PERIOD} recent output-only sensitivity"
        )
    )
    pd.DataFrame(temporal).to_csv(out / "TEMPORAL_PROFILE_MODELS.csv", index=False)

    volume_rows = []
    for threshold in (50.0, 200.0):
        filtered = r.country_period_volume_filter(country_primary, threshold)
        for key in ("output_primary", "impact_primary"):
            spec = specs[key]
            data = (
                filtered
                if key == "output_primary"
                else filtered[filtered["impact_denominator"] > 0].copy()
            )
            fit = r.fit_ppml(spec, data)
            row = r.extract_result(
                fit, spec, data,
                f"2019-2022 mapped country-period output >= {int(threshold)}",
            )
            row["sensitivity_threshold"] = int(threshold)
            volume_rows.append(row)
    pd.DataFrame(volume_rows).to_csv(out / "SMALL_OUTPUT_SENSITIVITY.csv", index=False)

    median_rows = []
    for name in ("output", "impact", "dyad"):
        spec, base = headline_data(country, dyad, name)
        data = (
            r.with_dyad_interaction(base, "IKES_median")
            if name == "dyad"
            else r.with_country_interaction(base, "IKES_median")
        )
        fit = r.fit_ppml(spec, data)
        median_rows.append(
            r.extract_result(fit, spec, data, "IKES median sensitivity")
        )
    pd.DataFrame(median_rows).to_csv(out / "IKES_MEDIAN_SENSITIVITY.csv", index=False)

    status = {
        "status": "PASS",
        "component": "core",
        "headline_family": [
            specs["output_primary"].name,
            specs["impact_primary"].name,
            specs["dyad_primary"].name,
        ],
        "temporal_status": {
            str(x.get("model")): str(x.get("status")) for x in temporal
        },
    }
    (out / "CORE_STATUS.json").write_text(
        json.dumps(status, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(status, indent=2))


def run_loo(country: pd.DataFrame, dyad: pd.DataFrame, model: str, out: Path) -> None:
    spec, data = headline_data(country, dyad, model)
    frame, summary = r.leave_one_discipline_out(spec, data)
    frame.to_csv(out / f"{spec.name}__LOO_DISCIPLINE.csv", index=False)
    payload = {"model": spec.name, **summary}
    (out / f"{spec.name}__LOO_STATUS.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


def run_permutation(
    country: pd.DataFrame,
    dyad: pd.DataFrame,
    model: str,
    start: int,
    end: int,
    out: Path,
) -> None:
    if start < 1 or end > r.PERMUTATION_REPS or start > end:
        raise SystemExit(
            f"Invalid permutation range {start}-{end}; expected within 1-{r.PERMUTATION_REPS}"
        )
    spec, data = headline_data(country, dyad, model)
    fit_obs = r.fit_ppml(spec, data)
    observed = float(fit_obs.coef().loc[spec.param])

    concept = (
        data[["concept_id", "IKES"]]
        .drop_duplicates()
        .sort_values("concept_id")
        .reset_index(drop=True)
    )
    if concept["concept_id"].tolist() != r.EXPECTED_CONCEPTS:
        raise SystemExit("Permutation component requires exactly D01-D21")
    values = concept["IKES"].to_numpy(copy=True)
    rng = np.random.default_rng(r.PERMUTATION_SEED)

    rows = []
    failures = []
    for rep in range(1, end + 1):
        shuffled = rng.permutation(values)
        if rep < start:
            continue
        mapping = dict(zip(concept["concept_id"], shuffled))
        pdata = data.copy()
        pdata["_ikes_perm"] = pdata["concept_id"].map(mapping).astype(float)
        if model == "dyad":
            pdata["colonial_tie_x_ikes"] = (
                pdata["col_dep_ever"].astype(float) * pdata["_ikes_perm"]
            )
        else:
            pdata["exposure_x_ikes"] = (
                pdata["colonial_years_sd"].astype(float) * pdata["_ikes_perm"]
            )
        try:
            fit = r.fit_ppml(spec, pdata)
            beta = float(fit.coef().loc[spec.param])
            rows.append(
                {
                    "rep": rep,
                    "estimate_log_scale": beta,
                    "status": "OK",
                    "error": "",
                }
            )
        except Exception as exc:
            failures.append(f"rep={rep}: {type(exc).__name__}: {exc}")
            rows.append(
                {
                    "rep": rep,
                    "estimate_log_scale": np.nan,
                    "status": "FAILED",
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )

    shard = pd.DataFrame(rows)
    name = f"{spec.name}__IKES_PERMUTATION__{start:04d}_{end:04d}"
    shard.to_csv(out / f"{name}.csv", index=False)
    payload = {
        "model": spec.name,
        "start_rep": start,
        "end_rep": end,
        "requested": end - start + 1,
        "successful": int(shard["estimate_log_scale"].notna().sum()),
        "failed": len(failures),
        "failure_examples": failures[:20],
        "observed_estimate_log_scale": observed,
        "seed": r.PERMUTATION_SEED,
    }
    (out / f"{name}.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--country-panel", type=Path, required=True)
    p.add_argument("--dyad-panel", type=Path, required=True)
    p.add_argument("--output-dir", type=Path, required=True)
    p.add_argument("--component", choices=["core", "loo", "permutation"], required=True)
    p.add_argument("--model", choices=["output", "impact", "dyad"])
    p.add_argument("--start-rep", type=int)
    p.add_argument("--end-rep", type=int)
    args = p.parse_args()

    import subprocess, sys
    subprocess.run(
        [sys.executable, str(r.CODE / "preoutcome_gate.py"), "--strict"],
        check=True,
    )
    country, dyad = load_inputs(args.country_panel, args.dyad_panel)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    if args.component == "core":
        run_core(country, dyad, args.output_dir)
    elif args.component == "loo":
        if args.model is None:
            raise SystemExit("--model is required for loo")
        run_loo(country, dyad, args.model, args.output_dir)
    else:
        if args.model is None or args.start_rep is None or args.end_rep is None:
            raise SystemExit("--model, --start-rep and --end-rep are required")
        run_permutation(
            country, dyad, args.model, args.start_rep, args.end_rep, args.output_dir
        )


if __name__ == "__main__":
    main()
