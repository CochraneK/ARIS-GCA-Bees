#!/usr/bin/env python3
"""Aggregate distributed ARIS4C003 confirmatory model components.

Rejects incomplete sensitivity work. Canonical permutation inference requires:
- exactly 999 repetitions per headline model;
- reps exactly 1..999 once each;
- zero failed/undefined refits;
- shard-observed estimates consistent with the core headline estimate.

Canonical LOO requires exactly D01-D21 once each and no failed refit.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import pyfixest as pf

import run_confirmatory_models as r

HEADLINE = {
    "A1_output_2019_2022",
    "A2_top10_2019_2022",
    "B1_dyad_2019_2022",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def one_file(root: Path, pattern: str) -> Path:
    found = list(root.rglob(pattern))
    if len(found) != 1:
        raise SystemExit(f"Expected exactly one {pattern}, found {len(found)}")
    return found[0]


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--components-root", type=Path, required=True)
    p.add_argument("--country-panel", type=Path, required=True)
    p.add_argument("--dyad-panel", type=Path, required=True)
    p.add_argument("--output-dir", type=Path, required=True)
    args = p.parse_args()
    root = args.components_root
    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)

    core_path = one_file(root, "CORE_MODELS.csv")
    core = pd.read_csv(core_path)
    if set(core["model"]) != {
        "A1_output_2019_2022",
        "A2_top10_2019_2022",
        "B1_dyad_2019_2022",
        "A1_output_2007_2022_pooled",
        "A2_top10_2007_2022_pooled",
        "B1_dyad_2007_2022_pooled",
    }:
        raise SystemExit("Core model set differs from frozen six-model set")
    core.to_csv(out / "CONFIRMATORY_AND_PERSISTENCE_MODELS.csv", index=False)

    for name in (
        "TEMPORAL_PROFILE_MODELS.csv",
        "SMALL_OUTPUT_SENSITIVITY.csv",
        "IKES_MEDIAN_SENSITIVITY.csv",
    ):
        src = one_file(root, name)
        df = pd.read_csv(src)
        df.to_csv(out / name, index=False)

    headline_core = (
        core[core["model"].isin(HEADLINE)]
        .set_index("model")["estimate_log_scale"]
        .astype(float)
        .to_dict()
    )
    if set(headline_core) != HEADLINE:
        raise SystemExit("Missing headline observed estimates in core component")

    sensitivity: dict[str, object] = {}
    for model in sorted(HEADLINE):
        # LOO
        loo_path = one_file(root, f"{model}__LOO_DISCIPLINE.csv")
        loo = pd.read_csv(loo_path)
        if loo["left_out_concept_id"].tolist() != r.EXPECTED_CONCEPTS:
            raise SystemExit(f"{model}: LOO must contain D01-D21 exactly in order")
        if loo["estimate_log_scale"].isna().any():
            raise SystemExit(f"{model}: failed/undefined LOO refit")
        loo.to_csv(out / f"{model}__LOO_DISCIPLINE.csv", index=False)
        vals = loo["estimate_log_scale"].astype(float)
        loo_summary = {
            "status": "VALID",
            "failed_refits": 0,
            "min_estimate_log_scale": float(vals.min()),
            "max_estimate_log_scale": float(vals.max()),
            "sign_all_same": bool((vals > 0).all() or (vals < 0).all()),
        }

        # permutations
        shard_paths = sorted(
            root.rglob(f"{model}__IKES_PERMUTATION__*.csv")
        )
        if not shard_paths:
            raise SystemExit(f"{model}: no permutation shards")
        frames = []
        for path in shard_paths:
            x = pd.read_csv(path)
            x["_source"] = str(path)
            frames.append(x)
        perm = pd.concat(frames, ignore_index=True)
        if perm["rep"].duplicated().any():
            dups = sorted(perm.loc[perm["rep"].duplicated(), "rep"].unique().tolist())
            raise SystemExit(f"{model}: duplicate permutation reps {dups[:20]}")
        perm = perm.sort_values("rep").reset_index(drop=True)
        expected_reps = list(range(1, r.PERMUTATION_REPS + 1))
        if perm["rep"].astype(int).tolist() != expected_reps:
            got = set(perm["rep"].astype(int))
            missing = sorted(set(expected_reps) - got)
            extra = sorted(got - set(expected_reps))
            raise SystemExit(
                f"{model}: permutation coverage incomplete; "
                f"missing={missing[:30]} extra={extra[:30]}"
            )
        if "status" in perm.columns and not perm["status"].eq("OK").all():
            raise SystemExit(f"{model}: at least one permutation refit failed")
        if perm["estimate_log_scale"].isna().any():
            raise SystemExit(f"{model}: at least one permutation estimate undefined")

        # Shard metadata must agree on the observed coefficient and seed.
        metas = []
        for path in sorted(root.rglob(f"{model}__IKES_PERMUTATION__*.json")):
            metas.append(json.loads(path.read_text(encoding="utf-8")))
        if len(metas) != len(shard_paths):
            raise SystemExit(
                f"{model}: shard metadata count {len(metas)} != CSV count {len(shard_paths)}"
            )
        obs = float(headline_core[model])
        for meta in metas:
            if int(meta.get("seed")) != r.PERMUTATION_SEED:
                raise SystemExit(f"{model}: shard seed mismatch")
            m_obs = float(meta.get("observed_estimate_log_scale"))
            if not math.isclose(m_obs, obs, rel_tol=1e-10, abs_tol=1e-10):
                raise SystemExit(
                    f"{model}: shard/core observed estimate mismatch {m_obs} vs {obs}"
                )
            if int(meta.get("failed", 0)) != 0:
                raise SystemExit(f"{model}: shard reports failed permutation fits")

        estimates = perm["estimate_log_scale"].astype(float)
        extreme = int((estimates.abs() >= abs(obs)).sum())
        perm_summary = {
            "status": "VALID",
            "seed": r.PERMUTATION_SEED,
            "reps_requested": r.PERMUTATION_REPS,
            "reps_successful": r.PERMUTATION_REPS,
            "failed_refits": 0,
            "extreme_abs_count": extreme,
            "p_two_sided": (1 + extreme) / (r.PERMUTATION_REPS + 1),
            "observed_estimate_log_scale": obs,
            "null_mean": float(estimates.mean()),
            "null_sd": float(estimates.std(ddof=1)),
            "null_q025": float(estimates.quantile(0.025)),
            "null_q975": float(estimates.quantile(0.975)),
        }
        perm[["rep", "estimate_log_scale"]].to_csv(
            out / f"{model}__IKES_PERMUTATION.csv", index=False
        )

        sensitivity[model] = {
            "leave_one_discipline_out": loo_summary,
            "ikes_label_permutation": perm_summary,
        }

    (out / "SENSITIVITY_SUMMARY.json").write_text(
        json.dumps(sensitivity, indent=2) + "\n", encoding="utf-8"
    )

    input_paths = [
        args.country_panel,
        args.dyad_panel,
        r.PROCESS / "IKES_FROZEN.csv",
        r.PROCESS / "IKES_FROZEN.provenance.json",
        r.PROCESS / "DISCIPLINE_CROSSWALK.csv",
        r.PROCESS / "PREREGISTRATION_DRAFT.md",
        r.PROCESS / "PREREGISTRATION_AMENDMENT_001.md",
        r.PROCESS / "PREREGISTRATION_AMENDMENT_002.md",
        r.PROCESS / "PREREGISTRATION_AMENDMENT_003.md",
        r.PROCESS / "MODEL_SPEC_LOCK.json",
        r.DATA / "derived" / "COLDAT_FORMER_COLONY_EXPOSURE.csv",
        r.DATA / "derived" / "COUNTRY_CROSSWALK.csv",
        r.DATA / "derived" / "CEPII_DYADS.csv",
    ]
    prov = {
        "paper": "ARIS4C003",
        "created_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "execution_mode": "distributed components; canonical frozen model functions imported",
        "primary_period": r.PRIMARY_PERIOD,
        "confirmatory_periods": list(r.PERSISTENCE_PERIODS),
        "recent_output_only_period": r.RECENT_OUTPUT_PERIOD,
        "permutation_reps": r.PERMUTATION_REPS,
        "permutation_seed": r.PERMUTATION_SEED,
        "headline_models": sorted(HEADLINE),
        "pyfixest_version": getattr(pf, "__version__", "unknown"),
        "input_sha256": {
            str(path): sha256(path)
            for path in input_paths
            if path.exists() and path.is_file()
        },
        "sensitivity_status": sensitivity,
        "integrity_rule": (
            "Aggregation aborts unless each headline has complete D01-D21 LOO "
            "and exactly reps 1-999 once each with no failed permutation fit."
        ),
    }
    (out / "ANALYSIS_PROVENANCE.json").write_text(
        json.dumps(prov, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(prov, indent=2))


if __name__ == "__main__":
    main()
