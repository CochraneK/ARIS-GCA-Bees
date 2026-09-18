#!/usr/bin/env python3
"""Convert Pilot 3A audit outputs into a stable JSON summary."""

from __future__ import annotations
import argparse, csv, json
from pathlib import Path

def parse_scalar(x: str):
    if x == "":
        return None
    try:
        if any(c in x.lower() for c in [".", "e"]):
            return float(x)
        return int(x)
    except ValueError:
        return x

ap=argparse.ArgumentParser()
ap.add_argument("--metrics", type=Path, required=True)
ap.add_argument("--provenance", type=Path, required=True)
ap.add_argument("--out", type=Path, required=True)
args=ap.parse_args()

with args.metrics.open(encoding="utf-8", newline="") as f:
    rows=list(csv.DictReader(f))
metrics={r["metric"]: parse_scalar(r["value"]) for r in rows}
details={r["metric"]: r["detail"] for r in rows if r.get("detail")}

prov={}
with args.provenance.open(encoding="utf-8", newline="") as f:
    for r in csv.DictReader(f, delimiter="\t"):
        prov[r["resource"]]={k:v for k,v in r.items() if k!="resource"}

coef_tol=1e-10
lp_tol=1e-8
summary={
    "decision": "PASS" if (
        metrics.get("clock2_coeff_missing_mmc")==0
        and metrics.get("clock2_coeff_missing_zoller")==0
        and metrics.get("clock3_coeff_missing_mmc")==0
        and metrics.get("clock3_coeff_missing_zoller")==0
        and metrics.get("clock2_coeff_max_abs_diff", 1)>coef_tol
        and False
    ) else "AUDIT",
    "metrics": metrics,
    "details": details,
    "provenance": prov,
}
# Determine sub-gates explicitly; overall gate only passes if the released
# application route matches the reference implementation numerically.
summary["gates"]={
    "coefficient_parity": (
        metrics.get("clock2_coeff_missing_mmc")==0
        and metrics.get("clock2_coeff_missing_zoller")==0
        and metrics.get("clock3_coeff_missing_mmc")==0
        and metrics.get("clock3_coeff_missing_zoller")==0
        and metrics.get("clock2_coeff_max_abs_diff", 1)<=coef_tol
        and metrics.get("clock3_coeff_max_abs_diff", 1)<=coef_tol
    ),
    "linear_predictor_parity": (
        metrics.get("clock2_linear_predictor_max_abs_diff", 1)<=lp_tol
        and metrics.get("clock3_linear_predictor_max_abs_diff", 1)<=lp_tol
    ),
    "clock3_documented_formula_parity": (
        metrics.get("clock3_documented_vs_official_max_abs_year_diff", 1)<=lp_tol
    ),
    "clock3_release_function_parity": (
        metrics.get("clock3_release_function_vs_official_max_abs_year_diff", 1)<=lp_tol
    ),
}
summary["decision"] = (
    "PASS_REFERENCE_IMPLEMENTATION_WITH_WRAPPER_WARNING"
    if (
        summary["gates"]["coefficient_parity"]
        and summary["gates"]["linear_predictor_parity"]
        and summary["gates"]["clock3_documented_formula_parity"]
        and not summary["gates"]["clock3_release_function_parity"]
    )
    else (
        "PASS" if all(summary["gates"].values()) else "FAIL_OR_REVIEW"
    )
)
summary["interpretation"]=(
    "The MMC v3.0.0 reference implementation is the canonical implementation "
    "for Pilot 3. The MammalMethylClock release may be used for coefficient "
    "inventory only unless its released inverse transform is numerically "
    "identical to the MMC reference on this audit."
)
args.out.write_text(json.dumps(summary, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
print(json.dumps(summary, indent=2, ensure_ascii=False))
