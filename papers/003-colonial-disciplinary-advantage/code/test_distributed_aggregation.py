#!/usr/bin/env python3
"""Synthetic integrity test for distributed result aggregation.

No research outcome or fitted model is used.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent

HEADLINE = {
    "A1_output_2019_2022": 0.10,
    "A2_top10_2019_2022": -0.20,
    "B1_dyad_2019_2022": 0.30,
}


def main() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        comp = root / "components"
        comp.mkdir()
        out = root / "out"

        rows = []
        for model, beta in HEADLINE.items():
            rows.append(
                {
                    "model": model,
                    "sample": "synthetic",
                    "outcome": "y",
                    "parameter": "x",
                    "estimate_log_scale": beta,
                    "std_error": 0.01,
                }
            )
        rows.extend(
            [
                {"model": "A1_output_2007_2022_pooled", "estimate_log_scale": 0.1},
                {"model": "A2_top10_2007_2022_pooled", "estimate_log_scale": -0.2},
                {"model": "B1_dyad_2007_2022_pooled", "estimate_log_scale": 0.3},
            ]
        )
        pd.DataFrame(rows).to_csv(comp / "CORE_MODELS.csv", index=False)
        pd.DataFrame([{"model": "synthetic", "status": "OK"}]).to_csv(
            comp / "TEMPORAL_PROFILE_MODELS.csv", index=False
        )
        pd.DataFrame([{"model": "synthetic"}]).to_csv(
            comp / "SMALL_OUTPUT_SENSITIVITY.csv", index=False
        )
        pd.DataFrame([{"model": "synthetic"}]).to_csv(
            comp / "IKES_MEDIAN_SENSITIVITY.csv", index=False
        )

        ids = [f"D{i:02d}" for i in range(1, 22)]
        for model, beta in HEADLINE.items():
            pd.DataFrame(
                {
                    "left_out_concept_id": ids,
                    "estimate_log_scale": np.linspace(beta - 0.01, beta + 0.01, 21),
                    "std_error": 0.01,
                    "multiplicative_effect": 1.0,
                }
            ).to_csv(comp / f"{model}__LOO_DISCIPLINE.csv", index=False)

            for start, end in ((1, 500), (501, 999)):
                reps = np.arange(start, end + 1)
                vals = np.linspace(-0.5, 0.5, len(reps))
                stem = f"{model}__IKES_PERMUTATION__{start:04d}_{end:04d}"
                pd.DataFrame(
                    {
                        "rep": reps,
                        "estimate_log_scale": vals,
                        "status": "OK",
                        "error": "",
                    }
                ).to_csv(comp / f"{stem}.csv", index=False)
                (comp / f"{stem}.json").write_text(
                    json.dumps(
                        {
                            "model": model,
                            "start_rep": start,
                            "end_rep": end,
                            "requested": end - start + 1,
                            "successful": end - start + 1,
                            "failed": 0,
                            "failure_examples": [],
                            "observed_estimate_log_scale": beta,
                            "seed": 20260918,
                        }
                    ),
                    encoding="utf-8",
                )

        country = root / "country.parquet"
        dyad = root / "dyad.parquet"
        country.write_bytes(b"synthetic-country-panel")
        dyad.write_bytes(b"synthetic-dyad-panel")

        subprocess.run(
            [
                sys.executable,
                str(HERE / "aggregate_confirmatory_components.py"),
                "--components-root",
                str(comp),
                "--country-panel",
                str(country),
                "--dyad-panel",
                str(dyad),
                "--output-dir",
                str(out),
            ],
            check=True,
        )

        summary = json.loads((out / "SENSITIVITY_SUMMARY.json").read_text())
        assert set(summary) == set(HEADLINE)
        for model in HEADLINE:
            assert summary[model]["ikes_label_permutation"]["status"] == "VALID"
            assert (
                summary[model]["ikes_label_permutation"]["reps_successful"] == 999
            )
            assert summary[model]["leave_one_discipline_out"]["status"] == "VALID"

        # Missing one rep must be rejected.
        victim = next(comp.glob("A1_output_2019_2022__IKES_PERMUTATION__0501_0999.csv"))
        bad = pd.read_csv(victim)
        bad = bad[bad["rep"] != 777]
        bad.to_csv(victim, index=False)
        failed = subprocess.run(
            [
                sys.executable,
                str(HERE / "aggregate_confirmatory_components.py"),
                "--components-root",
                str(comp),
                "--country-panel",
                str(country),
                "--dyad-panel",
                str(dyad),
                "--output-dir",
                str(root / "bad-out"),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        if failed.returncode == 0:
            raise AssertionError("Aggregator accepted an incomplete permutation set")

        print(
            {
                "status": "PASS",
                "complete_3x999_accepted": True,
                "missing_rep_rejected": True,
                "synthetic_only": True,
            }
        )


if __name__ == "__main__":
    main()
