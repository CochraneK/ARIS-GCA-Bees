#!/usr/bin/env python3
"""Run the frozen ARIS4C003 confirmatory PPML models.

This script consumes only already-materialized, hard-gated analysis panels.
It does not alter sample definitions, discipline mappings, IKES, or exposure
construction. Main outputs are:

1. 2019-2022 former-colony output PPML;
2. 2019-2022 former-colony Top-10% impact-rate PPML;
3. 2019-2022 former-colonial-tie collaboration PPML;
4. pooled 2007-2022 persistence specifications;
5. 21 leave-one-discipline-out estimates for each headline model;
6. fixed-seed 999-repetition IKES-label permutation falsification tests;
7. prespecified >=50 and >=200 mapped-output sensitivities for country models.

Any failed permutation/LOO refit invalidates that sensitivity instead of being
silently discarded.

Requires PyFixest. See process/PREREGISTRATION_DRAFT.md and amendments.
"""

from __future__ import annotations

import hashlib
import json
import math
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd
import pyfixest as pf

PAPER = Path(__file__).resolve().parents[1]
CODE = PAPER / "code"
PROCESS = PAPER / "process"
DATA = PAPER / "data"

PRIMARY_PERIOD = "2019-2022"
PERSISTENCE_PERIODS = ("2007-2010", "2011-2014", "2015-2018", "2019-2022")
CONFIRMATORY_PERIODS = set(PERSISTENCE_PERIODS)
RECENT_OUTPUT_PERIOD = "2023-2025"
PERMUTATION_REPS = 999
PERMUTATION_SEED = 20260918
EXPECTED_CONCEPTS = [f"D{i:02d}" for i in range(1, 22)]

COUNTRY_CLUSTER = {"CRV1": "iso3c + concept_id"}
DYAD_CLUSTER = {"CRV1": "pair_fe + concept_id"}


@dataclass(frozen=True)
class ModelSpec:
    name: str
    family: str
    outcome: str
    param: str
    formula: str
    cluster: dict[str, str]
    offset: str | None = None


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read_parquet(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise SystemExit(f"Missing analysis panel: {path}")
    con = duckdb.connect(database=":memory:")
    try:
        return con.execute(
            "SELECT * FROM read_parquet(?)",
            [str(path)],
        ).fetchdf()
    finally:
        con.close()


def validate_concepts(df: pd.DataFrame, label: str) -> None:
    if "concept_id" not in df.columns:
        raise SystemExit(f"{label} missing concept_id")
    got = sorted(df["concept_id"].dropna().astype(str).unique())
    if got != EXPECTED_CONCEPTS:
        raise SystemExit(
            f"{label} does not contain exactly D01-D21. "
            f"Missing={sorted(set(EXPECTED_CONCEPTS)-set(got))}; "
            f"extra={sorted(set(got)-set(EXPECTED_CONCEPTS))}"
        )


def fit_ppml(spec: ModelSpec, df: pd.DataFrame):
    if len(df) == 0:
        raise ValueError(f"{spec.name}: empty estimation sample")
    kwargs: dict[str, object] = {
        "fml": spec.formula,
        "data": df,
        "vcov": spec.cluster,
        "fixef_rm": "singleton",
        "separation_check": ["fe", "ir"],
        "iwls_maxiter": 100,
    }
    if spec.offset:
        kwargs["offset"] = spec.offset
    return pf.fepois(**kwargs)


def extract_result(
    fit,
    spec: ModelSpec,
    df: pd.DataFrame,
    sample_label: str,
) -> dict[str, object]:
    coef = fit.coef()
    se = fit.se()
    pval = fit.pvalue()
    if spec.param not in coef.index:
        raise ValueError(
            f"{spec.name}: parameter {spec.param!r} not found; "
            f"available={list(coef.index)}"
        )
    beta = float(coef.loc[spec.param])
    serr = float(se.loc[spec.param])
    p = float(pval.loc[spec.param])
    return {
        "model": spec.name,
        "sample": sample_label,
        "outcome": spec.outcome,
        "parameter": spec.param,
        "estimate_log_scale": beta,
        "std_error": serr,
        "z_or_t": beta / serr if serr > 0 else math.nan,
        "p_asymptotic": p,
        "ci95_low_log": beta - 1.959963984540054 * serr,
        "ci95_high_log": beta + 1.959963984540054 * serr,
        "multiplicative_effect": math.exp(beta),
        "input_rows": int(len(df)),
        "countries": int(df["iso3c"].nunique()) if "iso3c" in df else None,
        "pairs": int(df["pair_fe"].nunique()) if "pair_fe" in df else None,
        "disciplines": int(df["concept_id"].nunique()),
        "periods": int(df["period"].nunique()) if "period" in df else None,
        "formula": spec.formula,
        "offset": spec.offset or "",
        "cluster": next(iter(spec.cluster.values())),
    }


def with_country_interaction(df: pd.DataFrame, ikes_col: str = "IKES") -> pd.DataFrame:
    out = df.copy()
    out["exposure_x_ikes"] = out["colonial_years_sd"].astype(float) * out[ikes_col].astype(float)
    return out


def with_dyad_interaction(df: pd.DataFrame, ikes_col: str = "IKES") -> pd.DataFrame:
    out = df.copy()
    out["colonial_tie_x_ikes"] = out["col_dep_ever"].astype(float) * out[ikes_col].astype(float)
    return out


def permute_ikes(
    df: pd.DataFrame,
    rng: np.random.Generator,
    interaction_kind: str,
) -> pd.DataFrame:
    concept = (
        df[["concept_id", "IKES"]]
        .drop_duplicates()
        .sort_values("concept_id")
        .reset_index(drop=True)
    )
    if concept["concept_id"].tolist() != EXPECTED_CONCEPTS:
        raise ValueError("Permutation requires all D01-D21 in the estimation data")
    values = concept["IKES"].to_numpy(copy=True)
    shuffled = rng.permutation(values)
    mapping = dict(zip(concept["concept_id"], shuffled))
    out = df.copy()
    out["_ikes_perm"] = out["concept_id"].map(mapping).astype(float)
    if interaction_kind == "country":
        out["exposure_x_ikes"] = out["colonial_years_sd"].astype(float) * out["_ikes_perm"]
    elif interaction_kind == "dyad":
        out["colonial_tie_x_ikes"] = out["col_dep_ever"].astype(float) * out["_ikes_perm"]
    else:
        raise ValueError(interaction_kind)
    return out


def permutation_test(
    spec: ModelSpec,
    df: pd.DataFrame,
    observed_beta: float,
    interaction_kind: str,
) -> tuple[pd.DataFrame, dict[str, object]]:
    rng = np.random.default_rng(PERMUTATION_SEED)
    rows: list[dict[str, object]] = []
    failures: list[str] = []
    for rep in range(1, PERMUTATION_REPS + 1):
        pdata = permute_ikes(df, rng, interaction_kind)
        try:
            fit = fit_ppml(spec, pdata)
            beta = float(fit.coef().loc[spec.param])
            rows.append({"rep": rep, "estimate_log_scale": beta})
        except Exception as exc:  # do not silently discard failed permutations
            failures.append(f"rep={rep}: {type(exc).__name__}: {exc}")
            rows.append({"rep": rep, "estimate_log_scale": np.nan})

    dist = pd.DataFrame(rows)
    if failures:
        summary = {
            "status": "INVALID_DUE_TO_FAILED_REFITS",
            "reps_requested": PERMUTATION_REPS,
            "reps_successful": int(dist["estimate_log_scale"].notna().sum()),
            "failed_refits": len(failures),
            "failure_examples": failures[:20],
            "p_two_sided": None,
        }
        return dist, summary

    extreme = int((dist["estimate_log_scale"].abs() >= abs(observed_beta)).sum())
    p = (1 + extreme) / (PERMUTATION_REPS + 1)
    return dist, {
        "status": "VALID",
        "seed": PERMUTATION_SEED,
        "reps_requested": PERMUTATION_REPS,
        "reps_successful": PERMUTATION_REPS,
        "failed_refits": 0,
        "extreme_abs_count": extreme,
        "p_two_sided": p,
        "observed_estimate_log_scale": observed_beta,
        "null_mean": float(dist["estimate_log_scale"].mean()),
        "null_sd": float(dist["estimate_log_scale"].std(ddof=1)),
        "null_q025": float(dist["estimate_log_scale"].quantile(0.025)),
        "null_q975": float(dist["estimate_log_scale"].quantile(0.975)),
    }


def leave_one_discipline_out(
    spec: ModelSpec,
    df: pd.DataFrame,
) -> tuple[pd.DataFrame, dict[str, object]]:
    rows: list[dict[str, object]] = []
    failures: list[str] = []
    for concept in EXPECTED_CONCEPTS:
        subset = df[df["concept_id"] != concept].copy()
        try:
            fit = fit_ppml(spec, subset)
            beta = float(fit.coef().loc[spec.param])
            serr = float(fit.se().loc[spec.param])
            rows.append(
                {
                    "left_out_concept_id": concept,
                    "estimate_log_scale": beta,
                    "std_error": serr,
                    "multiplicative_effect": math.exp(beta),
                }
            )
        except Exception as exc:
            failures.append(f"{concept}: {type(exc).__name__}: {exc}")
            rows.append(
                {
                    "left_out_concept_id": concept,
                    "estimate_log_scale": np.nan,
                    "std_error": np.nan,
                    "multiplicative_effect": np.nan,
                }
            )
    out = pd.DataFrame(rows)
    valid = out["estimate_log_scale"].dropna()
    summary = {
        "status": "VALID" if not failures else "INVALID_DUE_TO_FAILED_REFITS",
        "failed_refits": len(failures),
        "failure_examples": failures,
        "min_estimate_log_scale": float(valid.min()) if len(valid) else None,
        "max_estimate_log_scale": float(valid.max()) if len(valid) else None,
        "sign_all_same": bool((valid > 0).all() or (valid < 0).all()) if len(valid) else None,
    }
    return out, summary


def country_period_volume_filter(df: pd.DataFrame, threshold: float) -> pd.DataFrame:
    totals = (
        df.groupby(["iso3c", "period"], as_index=False)["fractional_output"]
        .sum()
        .rename(columns={"fractional_output": "_mapped_period_output"})
    )
    keep = totals[totals["_mapped_period_output"] >= threshold][["iso3c", "period"]]
    return df.merge(keep, on=["iso3c", "period"], how="inner")


def model_specs() -> dict[str, ModelSpec]:
    return {
        "output_primary": ModelSpec(
            name="A1_output_2019_2022",
            family="PPML",
            outcome="fractional_output",
            param="exposure_x_ikes",
            formula="fractional_output ~ exposure_x_ikes | iso3c + concept_id",
            cluster=COUNTRY_CLUSTER,
        ),
        "impact_primary": ModelSpec(
            name="A2_top10_2019_2022",
            family="PPML_rate",
            outcome="fractional_top10",
            param="exposure_x_ikes",
            formula="fractional_top10 ~ exposure_x_ikes | iso3c + concept_id",
            cluster=COUNTRY_CLUSTER,
            offset="log_impact_denominator",
        ),
        "dyad_primary": ModelSpec(
            name="B1_dyad_2019_2022",
            family="PPML",
            outcome="fractional_collaboration_mass",
            param="colonial_tie_x_ikes",
            formula=(
                "fractional_collaboration_mass ~ colonial_tie_x_ikes "
                "| pair_fe + i_discipline_period_fe + j_discipline_period_fe"
            ),
            cluster=DYAD_CLUSTER,
        ),
        "output_pooled": ModelSpec(
            name="A1_output_2007_2022_pooled",
            family="PPML",
            outcome="fractional_output",
            param="exposure_x_ikes",
            formula=(
                "fractional_output ~ exposure_x_ikes "
                "| country_period_fe + discipline_period_fe"
            ),
            cluster=COUNTRY_CLUSTER,
        ),
        "impact_pooled": ModelSpec(
            name="A2_top10_2007_2022_pooled",
            family="PPML_rate",
            outcome="fractional_top10",
            param="exposure_x_ikes",
            formula=(
                "fractional_top10 ~ exposure_x_ikes "
                "| country_period_fe + discipline_period_fe"
            ),
            cluster=COUNTRY_CLUSTER,
            offset="log_impact_denominator",
        ),
        "dyad_pooled": ModelSpec(
            name="B1_dyad_2007_2022_pooled",
            family="PPML",
            outcome="fractional_collaboration_mass",
            param="colonial_tie_x_ikes",
            formula=(
                "fractional_collaboration_mass ~ colonial_tie_x_ikes "
                "| pair_fe + i_discipline_period_fe + j_discipline_period_fe"
            ),
            cluster=DYAD_CLUSTER,
        ),
    }


def single_period_specs(period: str) -> tuple[ModelSpec, ModelSpec, ModelSpec]:
    slug = period.replace("-", "_")
    return (
        ModelSpec(
            name=f"A1_output_{slug}_temporal",
            family="PPML",
            outcome="fractional_output",
            param="exposure_x_ikes",
            formula="fractional_output ~ exposure_x_ikes | iso3c + concept_id",
            cluster=COUNTRY_CLUSTER,
        ),
        ModelSpec(
            name=f"A2_top10_{slug}_temporal",
            family="PPML_rate",
            outcome="fractional_top10",
            param="exposure_x_ikes",
            formula="fractional_top10 ~ exposure_x_ikes | iso3c + concept_id",
            cluster=COUNTRY_CLUSTER,
            offset="log_impact_denominator",
        ),
        ModelSpec(
            name=f"B1_dyad_{slug}_temporal",
            family="PPML",
            outcome="fractional_collaboration_mass",
            param="colonial_tie_x_ikes",
            formula=(
                "fractional_collaboration_mass ~ colonial_tie_x_ikes "
                "| pair_fe + i_discipline_period_fe + j_discipline_period_fe"
            ),
            cluster=DYAD_CLUSTER,
        ),
    )


def safe_secondary_fit(
    spec: ModelSpec,
    df: pd.DataFrame,
    sample_label: str,
) -> dict[str, object]:
    try:
        fit = fit_ppml(spec, df)
        row = extract_result(fit, spec, df, sample_label)
        row["status"] = "OK"
        row["error"] = ""
        return row
    except Exception as exc:
        return {
            "model": spec.name,
            "sample": sample_label,
            "outcome": spec.outcome,
            "parameter": spec.param,
            "status": "FAILED_NO_REPAIR",
            "error": f"{type(exc).__name__}: {exc}",
            "input_rows": int(len(df)),
            "disciplines": (
                int(df["concept_id"].nunique()) if "concept_id" in df else None
            ),
            "formula": spec.formula,
            "offset": spec.offset or "",
            "cluster": next(iter(spec.cluster.values())),
        }


def main() -> None:
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument(
        "--country-panel",
        type=Path,
        default=DATA / "analysis" / "COUNTRY_DISCIPLINE_PANEL.parquet",
    )
    p.add_argument(
        "--dyad-panel",
        type=Path,
        default=DATA / "analysis" / "DYAD_DISCIPLINE_PANEL.parquet",
    )
    p.add_argument(
        "--output-dir",
        type=Path,
        default=DATA / "results" / "confirmatory",
    )
    args = p.parse_args()

    # Run-time integrity gate. The panels themselves can only be produced after
    # the same gate; this second check protects against stale/copied panels.
    subprocess.run(
        [sys.executable, str(CODE / "preoutcome_gate.py"), "--strict"],
        check=True,
    )

    country = read_parquet(args.country_panel)
    dyad = read_parquet(args.dyad_panel)
    validate_concepts(country, "country panel")
    validate_concepts(dyad, "dyad panel")

    required_country = {
        "iso3c", "concept_id", "period", "IKES", "IKES_median",
        "colonial_years_sd", "fractional_output", "impact_denominator",
        "fractional_top10", "country_period_fe", "discipline_period_fe",
        "log_impact_denominator",
    }
    required_dyad = {
        "pair_fe", "concept_id", "period", "IKES", "IKES_median",
        "col_dep_ever", "fractional_collaboration_mass",
        "i_discipline_period_fe", "j_discipline_period_fe",
    }
    if not required_country.issubset(country.columns):
        raise SystemExit(
            f"Country panel missing: {sorted(required_country-set(country.columns))}"
        )
    if not required_dyad.issubset(dyad.columns):
        raise SystemExit(
            f"Dyad panel missing: {sorted(required_dyad-set(dyad.columns))}"
        )

    country = with_country_interaction(country)
    dyad = with_dyad_interaction(dyad)

    country_primary = country[country["period"].eq(PRIMARY_PERIOD)].copy()
    country_pooled = country[country["period"].isin(CONFIRMATORY_PERIODS)].copy()
    impact_primary = country_primary[country_primary["impact_denominator"] > 0].copy()
    impact_pooled = country_pooled[country_pooled["impact_denominator"] > 0].copy()
    dyad_primary = dyad[dyad["period"].eq(PRIMARY_PERIOD)].copy()
    dyad_pooled = dyad[dyad["period"].isin(CONFIRMATORY_PERIODS)].copy()

    specs = model_specs()
    jobs = [
        (specs["output_primary"], country_primary, "2019-2022 primary"),
        (specs["impact_primary"], impact_primary, "2019-2022 primary"),
        (specs["dyad_primary"], dyad_primary, "2019-2022 primary"),
        (specs["output_pooled"], country_pooled, "2007-2022 pooled persistence"),
        (specs["impact_pooled"], impact_pooled, "2007-2022 pooled persistence"),
        (specs["dyad_pooled"], dyad_pooled, "2007-2022 pooled persistence"),
    ]

    args.output_dir.mkdir(parents=True, exist_ok=True)
    primary_rows: list[dict[str, object]] = []
    fitted: dict[str, object] = {}
    for spec, data, label in jobs:
        fit = fit_ppml(spec, data)
        fitted[spec.name] = fit
        primary_rows.append(extract_result(fit, spec, data, label))

    pd.DataFrame(primary_rows).to_csv(
        args.output_dir / "CONFIRMATORY_AND_PERSISTENCE_MODELS.csv",
        index=False,
    )

    # Secondary temporal profile: estimate the identical within-period gradient
    # separately in each preregistered mature period. These rows do not expand
    # the three-coefficient confirmatory family and are not used to choose the
    # headline period/model. 2023-2025 is output-only by design.
    temporal_rows: list[dict[str, object]] = []
    for period in PERSISTENCE_PERIODS:
        out_spec, impact_spec, dyad_spec = single_period_specs(period)
        c_period = country[country["period"].eq(period)].copy()
        i_period = c_period[c_period["impact_denominator"] > 0].copy()
        d_period = dyad[dyad["period"].eq(period)].copy()
        temporal_rows.append(
            safe_secondary_fit(out_spec, c_period, f"{period} temporal output")
        )
        temporal_rows.append(
            safe_secondary_fit(
                impact_spec, i_period, f"{period} temporal Top10 impact"
            )
        )
        temporal_rows.append(
            safe_secondary_fit(dyad_spec, d_period, f"{period} temporal dyad")
        )

    recent = country[country["period"].eq(RECENT_OUTPUT_PERIOD)].copy()
    recent_output_spec, _, _ = single_period_specs(RECENT_OUTPUT_PERIOD)
    temporal_rows.append(
        safe_secondary_fit(
            recent_output_spec,
            recent,
            f"{RECENT_OUTPUT_PERIOD} recent output-only sensitivity",
        )
    )
    pd.DataFrame(temporal_rows).to_csv(
        args.output_dir / "TEMPORAL_PROFILE_MODELS.csv",
        index=False,
    )

    # Headline finite-field sensitivities: exactly three confirmatory coefficients.
    headline = [
        (specs["output_primary"], country_primary, "country"),
        (specs["impact_primary"], impact_primary, "country"),
        (specs["dyad_primary"], dyad_primary, "dyad"),
    ]
    sensitivity_summary: dict[str, object] = {}
    for spec, data, kind in headline:
        observed_beta = float(fitted[spec.name].coef().loc[spec.param])

        loo, loo_summary = leave_one_discipline_out(spec, data)
        loo.to_csv(args.output_dir / f"{spec.name}__LOO_DISCIPLINE.csv", index=False)

        perm, perm_summary = permutation_test(
            spec, data, observed_beta, interaction_kind=kind
        )
        perm.to_csv(args.output_dir / f"{spec.name}__IKES_PERMUTATION.csv", index=False)

        sensitivity_summary[spec.name] = {
            "leave_one_discipline_out": loo_summary,
            "ikes_label_permutation": perm_summary,
        }

    # Prespecified small-output sensitivity for country models, primary period.
    small_output_rows: list[dict[str, object]] = []
    for threshold in (50.0, 200.0):
        filtered = country_period_volume_filter(country_primary, threshold)
        for key in ("output_primary", "impact_primary"):
            spec = specs[key]
            data = (
                filtered
                if key == "output_primary"
                else filtered[filtered["impact_denominator"] > 0].copy()
            )
            fit = fit_ppml(spec, data)
            row = extract_result(
                fit,
                spec,
                data,
                f"2019-2022 mapped country-period output >= {int(threshold)}",
            )
            row["sensitivity_threshold"] = int(threshold)
            small_output_rows.append(row)
    pd.DataFrame(small_output_rows).to_csv(
        args.output_dir / "SMALL_OUTPUT_SENSITIVITY.csv",
        index=False,
    )

    # Prespecified median-IKES sensitivity.
    median_rows: list[dict[str, object]] = []
    for spec, base, kind in headline:
        data = (
            with_country_interaction(base, "IKES_median")
            if kind == "country"
            else with_dyad_interaction(base, "IKES_median")
        )
        fit = fit_ppml(spec, data)
        row = extract_result(fit, spec, data, "IKES median sensitivity")
        median_rows.append(row)
    pd.DataFrame(median_rows).to_csv(
        args.output_dir / "IKES_MEDIAN_SENSITIVITY.csv",
        index=False,
    )

    # Analysis provenance. Hash only pre-existing input/artifact files, not the
    # result files just created, so reruns can verify the same analysis inputs.
    provenance_paths = [
        args.country_panel,
        args.dyad_panel,
        PROCESS / "IKES_FROZEN.csv",
        PROCESS / "IKES_FROZEN.provenance.json",
        PROCESS / "DISCIPLINE_CROSSWALK.csv",
        PROCESS / "PREREGISTRATION_DRAFT.md",
        PROCESS / "PREREGISTRATION_AMENDMENT_001.md",
        DATA / "derived" / "COLDAT_FORMER_COLONY_EXPOSURE.csv",
        DATA / "derived" / "COUNTRY_CROSSWALK.csv",
        DATA / "derived" / "CEPII_DYADS.csv",
    ]
    prov = {
        "paper": "ARIS4C003",
        "created_utc": utc_now(),
        "primary_period": PRIMARY_PERIOD,
        "confirmatory_periods": list(PERSISTENCE_PERIODS),
        "recent_output_only_period": RECENT_OUTPUT_PERIOD,
        "permutation_reps": PERMUTATION_REPS,
        "permutation_seed": PERMUTATION_SEED,
        "headline_models": [x[0].name for x in headline],
        "temporal_profile_status": {
            str(row.get("model")): str(row.get("status"))
            for row in temporal_rows
        },
        "pyfixest_version": getattr(pf, "__version__", "unknown"),
        "input_sha256": {
            str(p.relative_to(PAPER) if p.is_relative_to(PAPER) else p): sha256(p)
            for p in provenance_paths
            if p.exists() and p.is_file()
        },
        "sensitivity_status": sensitivity_summary,
        "integrity_rule": (
            "Permutation or leave-one-discipline sensitivity with any failed refit "
            "is marked invalid rather than silently dropping failures."
        ),
    }
    (args.output_dir / "ANALYSIS_PROVENANCE.json").write_text(
        json.dumps(prov, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(prov, indent=2))
    print(args.output_dir)


if __name__ == "__main__":
    main()
