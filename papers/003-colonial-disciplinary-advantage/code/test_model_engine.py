#!/usr/bin/env python3
"""Outcome-blind smoke test for the frozen PyFixest model engine.

Generates synthetic country×discipline and dyad×discipline panels that mimic the
columns consumed by run_confirmatory_models.py. No historical or contemporary
research data are read.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import run_confirmatory_models as r  # noqa: E402


def synthetic_country(seed: int = 20260918) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    countries = [f"C{i:03d}" for i in range(48)]
    concepts = r.EXPECTED_CONCEPTS
    exposure = dict(zip(countries, rng.normal(0, 1, len(countries))))
    ikes = dict(zip(concepts, np.linspace(0.2, 2.4, len(concepts))))
    country_fe = dict(zip(countries, rng.normal(0, 0.55, len(countries))))
    discipline_fe = dict(zip(concepts, rng.normal(0, 0.35, len(concepts))))
    beta = 0.30

    rows = []
    for country in countries:
        for concept in concepts:
            x = exposure[country] * ikes[concept]
            eta = 2.3 + country_fe[country] + discipline_fe[concept] + beta * x
            mu = math.exp(eta)
            y = rng.gamma(shape=18.0, scale=mu / 18.0)

            impact_den = max(2.0, y * rng.uniform(0.75, 0.98))
            top_eta = math.log(0.10) + 0.18 * x
            top_mu = impact_den * math.exp(top_eta)
            top10 = rng.gamma(shape=15.0, scale=max(top_mu, 1e-9) / 15.0)

            rows.append(
                {
                    "iso3c": country,
                    "concept_id": concept,
                    "period": r.PRIMARY_PERIOD,
                    "IKES": ikes[concept],
                    "IKES_median": ikes[concept] * 0.98 + 0.01,
                    "colonial_years_sd": exposure[country],
                    "fractional_output": y,
                    "impact_denominator": impact_den,
                    "fractional_top10": top10,
                    "log_impact_denominator": math.log(impact_den),
                    "country_period_fe": f"{country}__{r.PRIMARY_PERIOD}",
                    "discipline_period_fe": f"{concept}__{r.PRIMARY_PERIOD}",
                }
            )
    return r.with_country_interaction(pd.DataFrame(rows))


def synthetic_dyad(seed: int = 20260919) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    nodes = [f"N{i:02d}" for i in range(12)]
    concepts = r.EXPECTED_CONCEPTS
    ikes = dict(zip(concepts, np.linspace(0.2, 2.4, len(concepts))))
    endpoint_disc = {
        (node, concept): rng.normal(0, 0.25)
        for node in nodes
        for concept in concepts
    }
    pair_fe = {}
    colonial = {}
    for i, a in enumerate(nodes):
        for b in nodes[i + 1 :]:
            pid = f"{a}__{b}"
            pair_fe[pid] = rng.normal(-0.1, 0.45)
            colonial[pid] = int(rng.random() < 0.22)

    beta = 0.26
    rows = []
    for i, a in enumerate(nodes):
        for b in nodes[i + 1 :]:
            pid = f"{a}__{b}"
            for concept in concepts:
                x = colonial[pid] * ikes[concept]
                eta = (
                    0.8
                    + pair_fe[pid]
                    + endpoint_disc[(a, concept)]
                    + endpoint_disc[(b, concept)]
                    + beta * x
                )
                mu = math.exp(eta)
                y = rng.gamma(shape=14.0, scale=mu / 14.0)
                rows.append(
                    {
                        "pair_fe": pid,
                        "pair_id": pid,
                        "iso3_i": a,
                        "iso3_j": b,
                        "concept_id": concept,
                        "period": r.PRIMARY_PERIOD,
                        "IKES": ikes[concept],
                        "IKES_median": ikes[concept] * 0.98 + 0.01,
                        "col_dep_ever": colonial[pid],
                        "fractional_collaboration_mass": y,
                        "i_discipline_period_fe": f"{a}__{concept}__{r.PRIMARY_PERIOD}",
                        "j_discipline_period_fe": f"{b}__{concept}__{r.PRIMARY_PERIOD}",
                    }
                )
    return r.with_dyad_interaction(pd.DataFrame(rows))


def assert_finite(fit, param: str, label: str) -> float:
    coef = float(fit.coef().loc[param])
    se = float(fit.se().loc[param])
    if not (math.isfinite(coef) and math.isfinite(se) and se > 0):
        raise AssertionError(f"{label}: non-finite estimate/se: {coef}, {se}")
    return coef


def test_demeaner_fallback_contract() -> None:
    """Only FE demeaning non-convergence may trigger the LSMR retry."""
    spec = r.model_specs()["output_primary"]
    dummy = pd.DataFrame({"stub": [1]})

    class DummyFit:
        pass

    fit2 = DummyFit()
    with patch.object(
        r.pf,
        "fepois",
        side_effect=[
            ValueError("Demeaning failed after 10000 iterations."),
            fit2,
        ],
    ) as mocked:
        got = r.fit_ppml(spec, dummy)

    if got is not fit2:
        raise AssertionError("LSMR fallback did not return retry fit")
    if mocked.call_count != 2:
        raise AssertionError("Expected exactly one MAP attempt and one LSMR retry")
    second_kwargs = mocked.call_args_list[1].kwargs
    if "demeaner" not in second_kwargs:
        raise AssertionError("LSMR retry did not pass an explicit demeaner")
    if getattr(got, "_aris4c_demeaner_route", None) != "lsmr_within_additive_fallback":
        raise AssertionError("Fallback route provenance was not recorded")

    with patch.object(
        r.pf,
        "fepois",
        side_effect=ValueError("some unrelated model failure"),
    ) as mocked:
        try:
            r.fit_ppml(spec, dummy)
        except ValueError as exc:
            if "unrelated model failure" not in str(exc):
                raise
        else:
            raise AssertionError("Non-demeaning ValueError was incorrectly repaired")
        if mocked.call_count != 1:
            raise AssertionError("Non-demeaning failures must not be retried")


def main() -> None:
    test_demeaner_fallback_contract()
    specs = r.model_specs()
    country = synthetic_country()
    dyad = synthetic_dyad()

    r.validate_concepts(country, "synthetic country")
    r.validate_concepts(dyad, "synthetic dyad")

    output_fit = r.fit_ppml(specs["output_primary"], country)
    impact_fit = r.fit_ppml(specs["impact_primary"], country)
    dyad_fit = r.fit_ppml(specs["dyad_primary"], dyad)

    b_output = assert_finite(output_fit, "exposure_x_ikes", "output")
    b_impact = assert_finite(impact_fit, "exposure_x_ikes", "impact")
    b_dyad = assert_finite(dyad_fit, "colonial_tie_x_ikes", "dyad")

    # Directional sanity only; this is not a power/calibration test.
    if b_output <= 0:
        raise AssertionError(f"output planted-positive interaction recovered as {b_output}")
    if b_impact <= 0:
        raise AssertionError(f"impact planted-positive interaction recovered as {b_impact}")
    if b_dyad <= 0:
        raise AssertionError(f"dyad planted-positive interaction recovered as {b_dyad}")

    # Verify the frozen secondary temporal-profile model factory uses the same
    # within-period estimator family without expanding the headline tests.
    temporal_specs = r.single_period_specs("2007-2010")
    temporal_fit = r.fit_ppml(temporal_specs[0], country)
    assert_finite(
        temporal_fit,
        "exposure_x_ikes",
        "secondary temporal output specification",
    )

    # Verify median-IKES and one leave-one-field code path without running the
    # expensive 999-permutation final sensitivity in CI.
    median_country = r.with_country_interaction(country, "IKES_median")
    median_fit = r.fit_ppml(specs["output_primary"], median_country)
    assert_finite(median_fit, "exposure_x_ikes", "median IKES")

    one_loo = country[country["concept_id"] != "D01"].copy()
    loo_fit = r.fit_ppml(specs["output_primary"], one_loo)
    assert_finite(loo_fit, "exposure_x_ikes", "single LOO")

    # Verify a single deterministic permutation code path.
    perm = r.permute_ikes(
        country,
        np.random.default_rng(r.PERMUTATION_SEED),
        interaction_kind="country",
    )
    perm_fit = r.fit_ppml(specs["output_primary"], perm)
    assert_finite(perm_fit, "exposure_x_ikes", "single permutation")

    print(
        {
            "status": "PASS",
            "output_beta": b_output,
            "impact_beta": b_impact,
            "dyad_beta": b_dyad,
            "note": "synthetic only; no real historical or bibliometric outcomes",
        }
    )


if __name__ == "__main__":
    main()
