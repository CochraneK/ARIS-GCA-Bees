"""Toy model-recoverability simulation for ARIS4C008.

This is a design diagnostic, not a biological power analysis.
It asks whether additive, weakest-link and threshold architectures
can be distinguished under finite taxa, measurement error and missingness.
"""
from __future__ import annotations
import numpy as np
import pandas as pd

SEED = 20260918
CANDIDATE_MODELS = ("additive", "weakest", "threshold", "interaction")

def features(X, model):
    if model == "additive":
        return X.mean(1)[:, None]
    if model == "weakest":
        return X.min(1)[:, None]
    if model == "threshold":
        return np.c_[(X >= 0.6).mean(1), X.min(1)]
    if model == "interaction":
        return np.c_[X.mean(1), X.min(1), (X ** 2).mean(1)]
    raise ValueError(model)

def ols_predict(A, y, B):
    A = np.c_[np.ones(len(A)), A]
    B = np.c_[np.ones(len(B)), B]
    return B @ (np.linalg.pinv(A) @ y)

def cv_rmse(X, y, model, rng, folds=4):
    idx = np.arange(len(y))
    parts = np.array_split(rng.permutation(idx), folds)
    F = features(X, model)
    errs = []
    for te in parts:
        tr = np.setdiff1d(idx, te, assume_unique=True)
        p = ols_predict(F[tr], y[tr], F[te])
        errs.append(np.sqrt(np.mean((y[te] - p) ** 2)))
    return float(np.mean(errs))

def generate_outcome(X, true_model, rng):
    if true_model == "additive":
        z = X.mean(1)
    elif true_model == "weakest":
        z = X.min(1)
    elif true_model == "threshold":
        k = (X >= 0.6).sum(1)
        z = 0.15 * X.mean(1) + 0.85 / (1 + np.exp(-(k - 5.5) * 2))
    else:
        raise ValueError(true_model)
    return z + rng.normal(0, 0.07, len(X))

def farthest(S, n):
    S = (S - S.mean(0)) / (S.std(0) + 1e-9)
    centroid = S.mean(0)
    chosen = [int(np.argmax(((S - centroid) ** 2).sum(1)))]
    d = ((S - S[chosen[0]]) ** 2).sum(1)
    for _ in range(1, n):
        j = int(np.argmax(d))
        chosen.append(j)
        d = np.minimum(d, ((S - S[j]) ** 2).sum(1))
    return np.asarray(chosen)

def model_discriminating_select(X, n):
    signature = np.c_[X.mean(1), X.min(1), (X >= 0.6).mean(1)]
    return farthest(signature, n)

def run(reps=50):
    rng = np.random.default_rng(SEED)
    records = []
    for n_taxa in (25, 40, 80, 120):
        for missing in (0.2, 0.4):
            for true_model in ("additive", "weakest", "threshold"):
                for sampling in ("random", "model_discriminating"):
                    wins = 0
                    for _ in range(reps):
                        N = max(1200, n_taxa * 10)
                        latent = rng.beta(2, 2, (N, 1))
                        raw = rng.beta(1.5, 1.5, (N, 8))
                        pool = np.clip(0.25 * latent + 0.75 * raw, 0, 1)
                        if sampling == "random":
                            sel = rng.choice(N, n_taxa, replace=False)
                        else:
                            sel = model_discriminating_select(pool, n_taxa)
                        X = pool[sel]
                        y = generate_outcome(X, true_model, rng)
                        Z = np.clip(X + rng.normal(0, 0.08, X.shape), 0, 1)
                        mask = rng.random(Z.shape) < missing
                        Z[mask] = np.nan
                        means = np.nanmean(Z, 0)
                        ii = np.where(np.isnan(Z))
                        Z[ii] = means[ii[1]]
                        scores = {m: cv_rmse(Z, y, m, rng) for m in CANDIDATE_MODELS}
                        wins += min(scores, key=scores.get) == true_model
                    records.append({
                        "n_taxa": n_taxa,
                        "missing": missing,
                        "true_model": true_model,
                        "sampling": sampling,
                        "recovery_rate": wins / reps,
                    })
    return pd.DataFrame(records)

if __name__ == "__main__":
    df = run()
    print(df.to_csv(index=False))
