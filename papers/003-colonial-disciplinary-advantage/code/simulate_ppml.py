#!/usr/bin/env python3
"""Outcome-blind synthetic sanity test for ARIS4C003.

This script does not read any real colonial-history or bibliometric outcome data.
Its job is narrower: verify that the planned PPML specification accepts positive
fractional outcomes and recovers a known exposure x IKES interaction under a
controlled data-generating process.

It is NOT a power analysis and it does NOT certify final standard errors. With
only ~21 confirmatory disciplines, final inference must not rely blindly on
large-cluster asymptotics; discipline-level permutation / small-cluster
sensitivity checks remain required by the preregistration.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

FORMULA = (
    "fractional_output ~ exposure:ikes "
    "+ C(country):C(window) + C(discipline):C(window)"
)


@dataclass
class Result:
    beta_true: float
    beta_hat: float
    cluster_se_country: float
    n_rows: int
    n_countries: int
    n_disciplines: int
    n_windows: int


def simulate(
    seed: int,
    beta: float,
    n_countries: int = 80,
    n_disciplines: int = 21,
    n_windows: int = 4,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    countries = [f"C{i:03d}" for i in range(n_countries)]
    disciplines = [f"D{i:02d}" for i in range(n_disciplines)]
    windows = [f"T{i}" for i in range(n_windows)]

    exposure = rng.beta(2, 2, n_countries)
    ikes = np.linspace(0, 1, n_disciplines)
    country_window = rng.normal(0, 0.45, (n_countries, n_windows))
    discipline_window = rng.normal(0, 0.35, (n_disciplines, n_windows))

    rows: list[tuple[object, ...]] = []
    for ci, country in enumerate(countries):
        for di, discipline in enumerate(disciplines):
            for ti, window in enumerate(windows):
                eta = (
                    2.0
                    + country_window[ci, ti]
                    + discipline_window[di, ti]
                    + beta * exposure[ci] * ikes[di]
                )
                mu = float(np.exp(eta))
                # Gamma outcome is deliberately non-integer: this checks the
                # quasi-Poisson/PPML use case for fractional publication mass.
                y = float(rng.gamma(shape=10.0, scale=mu / 10.0))
                rows.append(
                    (country, discipline, window, exposure[ci], ikes[di], y)
                )

    return pd.DataFrame(
        rows,
        columns=[
            "country",
            "discipline",
            "window",
            "exposure",
            "ikes",
            "fractional_output",
        ],
    )


def fit(df: pd.DataFrame, beta_true: float) -> Result:
    model = smf.glm(
        FORMULA,
        data=df,
        family=sm.families.Poisson(),
    ).fit(
        cov_type="cluster",
        cov_kwds={"groups": df["country"]},
        maxiter=100,
        disp=0,
    )
    return Result(
        beta_true=beta_true,
        beta_hat=float(model.params["exposure:ikes"]),
        cluster_se_country=float(model.bse["exposure:ikes"]),
        n_rows=len(df),
        n_countries=df["country"].nunique(),
        n_disciplines=df["discipline"].nunique(),
        n_windows=df["window"].nunique(),
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=20260918)
    parser.add_argument("--beta", type=float, default=0.35)
    parser.add_argument("--tolerance", type=float, default=0.12)
    parser.add_argument("--no-assert", action="store_true")
    args = parser.parse_args()

    null_df = simulate(args.seed, 0.0)
    signal_df = simulate(args.seed, args.beta)
    null = fit(null_df, 0.0)
    signal = fit(signal_df, args.beta)

    payload = {
        "design_formula": FORMULA,
        "purpose": "point-estimate/code-path sanity only; not final inference certification",
        "null": asdict(null),
        "signal": asdict(signal),
        "tolerance": args.tolerance,
    }
    print(json.dumps(payload, indent=2))

    if not args.no_assert:
        if abs(null.beta_hat) > args.tolerance:
            raise SystemExit(
                f"FAIL: null estimate {null.beta_hat:.3f} exceeds tolerance"
            )
        if abs(signal.beta_hat - args.beta) > args.tolerance:
            raise SystemExit(
                "FAIL: signal recovery outside tolerance: "
                f"true={args.beta:.3f}, hat={signal.beta_hat:.3f}"
            )
        print("SYNTHETIC GATE: PASS")


if __name__ == "__main__":
    main()
