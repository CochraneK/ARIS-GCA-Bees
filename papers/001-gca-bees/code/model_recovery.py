"""Synthetic model-recovery diagnostic for ARIS4C001.

Default mode reproduces the full design-support simulation committed in
data/model_recovery_synthetic.json. --smoke runs a tiny executable check for CI
and never overwrites the canonical research output.

This simulation is DESIGN SUPPORT ONLY. It is not empirical evidence about bees.
"""
import argparse
import json
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

SEED = 20260918
FULL_REPETITIONS = 200
FULL_SAMPLE_SIZES = [60, 90, 120, 160]
TRUE_RHO = 0.35
TRUE_LOADING = 0.65


def objective(params, sample_cov, n, model):
    p = sample_cov.shape[0]
    loadings = params[:p]
    residual = np.exp(params[p:2*p])

    if model == "one_factor":
        sigma = np.outer(loadings, loadings) + np.diag(residual)
    elif model in {"two_factor_correlated", "two_factor_independent"}:
        loading_matrix = np.zeros((p, 2))
        loading_matrix[:3, 0] = loadings[:3]
        loading_matrix[3:, 1] = loadings[3:]
        rho = np.tanh(params[-1]) if model == "two_factor_correlated" else 0.0
        phi = np.array([[1.0, rho], [rho, 1.0]])
        sigma = loading_matrix @ phi @ loading_matrix.T + np.diag(residual)
    else:
        raise ValueError(model)

    sign, logdet = np.linalg.slogdet(sigma)
    if sign <= 0:
        return 1e15
    return n / 2 * (logdet + np.trace(sample_cov @ np.linalg.inv(sigma)))


def fit_bic(x, model):
    n, p = x.shape
    sample_cov = np.cov(x, rowvar=False, bias=True)
    start = np.r_[np.full(p, 0.55), np.log(np.full(p, 0.65))]
    if model == "two_factor_correlated":
        start = np.r_[start, np.arctanh(0.3)]

    result = minimize(
        objective,
        start,
        args=(sample_cov, n, model),
        method="L-BFGS-B",
        options={"maxiter": 2000},
    )
    if not result.success and not np.isfinite(result.fun):
        raise RuntimeError(f"optimization failed for {model}: {result.message}")
    k = 2 * p + (1 if model == "two_factor_correlated" else 0)
    return float(2 * result.fun + k * np.log(n))


def generate(n, rng):
    factors = rng.multivariate_normal(
        [0.0, 0.0],
        [[1.0, TRUE_RHO], [TRUE_RHO, 1.0]],
        size=n,
    )
    residual_sd = np.sqrt(1 - TRUE_LOADING**2)
    x = np.empty((n, 6))
    x[:, :3] = TRUE_LOADING * factors[:, [0]] + rng.normal(
        0, residual_sd, size=(n, 3)
    )
    x[:, 3:] = TRUE_LOADING * factors[:, [1]] + rng.normal(
        0, residual_sd, size=(n, 3)
    )
    return x


def run(repetitions=FULL_REPETITIONS, sample_sizes=None, write_output=True):
    sample_sizes = FULL_SAMPLE_SIZES if sample_sizes is None else sample_sizes
    rng = np.random.default_rng(SEED)
    models = [
        "one_factor",
        "two_factor_correlated",
        "two_factor_independent",
    ]
    output = {
        "seed": SEED,
        "repetitions": repetitions,
        "data_generating_model": {
            "two_factors": True,
            "factor_correlation": TRUE_RHO,
            "loading": TRUE_LOADING,
        },
        "note": "Synthetic model-recovery only; not empirical evidence about bees.",
        "sample_sizes": {},
    }

    for n in sample_sizes:
        counts = {model: 0 for model in models}
        delta = []
        for _ in range(repetitions):
            x = generate(n, rng)
            bics = {model: fit_bic(x, model) for model in models}
            counts[min(bics, key=bics.get)] += 1
            delta.append(bics["one_factor"] - bics["two_factor_correlated"])

        output["sample_sizes"][str(n)] = {
            "selection_rate": {
                model: counts[model] / repetitions for model in models
            },
            "median_BIC_one_minus_two_correlated": float(np.median(delta)),
        }

    if write_output:
        out_path = (
            Path(__file__).resolve().parents[1]
            / "data"
            / "model_recovery_synthetic.json"
        )
        out_path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(output, indent=2))
    return output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="Run two replications at N=60 without writing canonical output.",
    )
    args = parser.parse_args()
    if args.smoke:
        run(repetitions=2, sample_sizes=[60], write_output=False)
    else:
        run()


if __name__ == "__main__":
    main()
