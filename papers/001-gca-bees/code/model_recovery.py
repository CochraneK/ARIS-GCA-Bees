"""Synthetic model-recovery diagnostic for ARIS4C001.

This script is DESIGN SUPPORT ONLY. It does not simulate a claimed bee
mechanism and its outputs are not empirical evidence about bees.

It asks a narrow question: if six standardized indicators were truly generated
by two moderately correlated latent factors (three learning indicators and
three uncertainty/control indicators), how often would simple Gaussian
covariance models recover one factor vs two factors at several sample sizes?
"""

import json
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

SEED = 20260918
REPETITIONS = 200
SAMPLE_SIZES = [60, 90, 120, 160]
TRUE_RHO = 0.35
TRUE_LOADING = 0.65


def objective(params, sample_cov, n, model):
    p = sample_cov.shape[0]
    loadings = params[:p]
    residual = np.exp(params[p:2*p])

    if model == "one_factor":
        sigma = np.outer(loadings, loadings) + np.diag(residual)
        k = 2 * p
    elif model in {"two_factor_correlated", "two_factor_independent"}:
        loading_matrix = np.zeros((p, 2))
        loading_matrix[:3, 0] = loadings[:3]
        loading_matrix[3:, 1] = loadings[3:]
        if model == "two_factor_correlated":
            rho = np.tanh(params[-1])
        else:
            rho = 0.0
        phi = np.array([[1.0, rho], [rho, 1.0]])
        sigma = loading_matrix @ phi @ loading_matrix.T + np.diag(residual)
        k = 2 * p + (1 if model == "two_factor_correlated" else 0)
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
    x[:, :3] = (
        TRUE_LOADING * factors[:, [0]]
        + rng.normal(0, residual_sd, size=(n, 3))
    )
    x[:, 3:] = (
        TRUE_LOADING * factors[:, [1]]
        + rng.normal(0, residual_sd, size=(n, 3))
    )
    return x


def run():
    rng = np.random.default_rng(SEED)
    models = [
        "one_factor",
        "two_factor_correlated",
        "two_factor_independent",
    ]
    output = {
        "seed": SEED,
        "repetitions": REPETITIONS,
        "data_generating_model": {
            "two_factors": True,
            "factor_correlation": TRUE_RHO,
            "loading": TRUE_LOADING,
        },
        "note": "Synthetic model-recovery only; not empirical evidence about bees.",
        "sample_sizes": {},
    }

    for n in SAMPLE_SIZES:
        counts = {model: 0 for model in models}
        delta = []

        for _ in range(REPETITIONS):
            x = generate(n, rng)
            bics = {model: fit_bic(x, model) for model in models}
            counts[min(bics, key=bics.get)] += 1
            delta.append(
                bics["one_factor"] - bics["two_factor_correlated"]
            )

        output["sample_sizes"][str(n)] = {
            "selection_rate": {
                model: counts[model] / REPETITIONS for model in models
            },
            "median_BIC_one_minus_two_correlated": float(np.median(delta)),
        }

    out_path = Path(__file__).resolve().parents[1] / "data" / "model_recovery_synthetic.json"
    out_path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    run()
