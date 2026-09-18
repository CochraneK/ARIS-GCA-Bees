#!/usr/bin/env python3
"""Synthetic end-to-end smoke test for the IKES Coder B pipeline.

No real Coder B judgment is generated here. The test creates artificial,
identical A/B matrices only to verify:
raw GPTPage response -> ingest -> agreement -> freeze/provenance.
"""

from __future__ import annotations

import csv
import io
import subprocess
import sys
import tempfile
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
DIMS = [f"D{i}" for i in range(1, 12)]


def main() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        a_path = root / "A.csv"
        raw_path = root / "coder_b_raw.md"
        b_path = root / "B.csv"
        b_notes = root / "B.md"
        adj_dir = root / "adjudication"
        frozen = root / "IKES_FROZEN.csv"
        prov = root / "IKES_FROZEN.provenance.json"

        rows = []
        for i in range(1, 22):
            cid = f"D{i:02d}"
            vals = [float((i + j) % 4) for j in range(1, 12)]
            row = {
                "concept_id": cid,
                "discipline": f"Synthetic Discipline {i:02d}",
                **{d: vals[j] for j, d in enumerate(DIMS)},
            }
            row["IKES"] = sum(vals) / len(vals)
            rows.append(row)

        a = pd.DataFrame(rows)
        a.to_csv(a_path, index=False)

        buf = io.StringIO()
        writer = csv.writer(buf, lineterminator="\n")
        writer.writerow(["concept_id", "discipline", *DIMS, "IKES_B"])
        for _, row in a.iterrows():
            writer.writerow(
                [
                    row["concept_id"],
                    row["discipline"],
                    *[int(row[d]) for d in DIMS],
                    f"{row['IKES']:.6f}",
                ]
            )

        fence = chr(96) * 3
        evidence = []
        for i in range(1, 22):
            cid = f"D{i:02d}"
            evidence.append(
                f"### {cid} — Synthetic Discipline {i:02d}\n\n"
                "Synthetic rationale for parser and pipeline testing only. "
                "No historical or contemporary empirical claim is made. "
                "No score >=2 source requirement is being substantively tested here.\n\n"
                "Uncertainty: synthetic fixture.\n\n"
                "Confidence: high\n"
            )
        raw = (
            "# Synthetic Coder B response\n\n"
            + fence
            + "csv\n"
            + buf.getvalue()
            + fence
            + "\n\n## Evidence notes\n\n"
            + "\n".join(evidence)
            + "\n## BLINDING DECLARATION\n"
            "INDEPENDENCE_STATUS: PASS\n"
            "Synthetic test fixture; no real outcomes or Coder A evidence were consulted.\n"
        )
        raw_path.write_text(raw, encoding="utf-8")

        subprocess.run(
            [
                sys.executable,
                str(HERE / "ingest_coder_b.py"),
                str(raw_path),
                "--output-csv",
                str(b_path),
                "--output-notes",
                str(b_notes),
            ],
            check=True,
        )

        subprocess.run(
            [
                sys.executable,
                str(HERE / "adjudicate_ikes.py"),
                str(a_path),
                str(b_path),
                "--output-dir",
                str(adj_dir),
            ],
            check=True,
        )

        subprocess.run(
            [
                sys.executable,
                str(HERE / "freeze_ikes.py"),
                str(adj_dir / "IKES_DISAGREEMENTS.csv"),
                "--output",
                str(frozen),
                "--provenance",
                str(prov),
                "--coder-a",
                str(a_path),
                "--coder-b",
                str(b_path),
                "--coder-b-notes",
                str(b_notes),
                "--coder-b-raw",
                str(raw_path),
            ],
            check=True,
        )

        f = pd.read_csv(frozen)
        assert len(f) == 21
        assert f["concept_id"].tolist() == [f"D{i:02d}" for i in range(1, 22)]
        assert f["IKES"].notna().all()
        assert prov.exists() and prov.stat().st_size > 0

        # Unflagged A/B agreements are immutable means. A manual override must
        # be rejected even when a note is supplied.
        illegal_adj = pd.read_csv(adj_dir / "IKES_DISAGREEMENTS.csv")
        illegal_adj["adjudication_note"] = illegal_adj[
            "adjudication_note"
        ].astype("object")
        target = (
            illegal_adj["score_A"].notna()
            & illegal_adj["score_B"].notna()
            & ((illegal_adj["score_A"] - illegal_adj["score_B"]).abs() < 2)
        )
        idx = illegal_adj.index[target][0]
        illegal_adj.loc[idx, "adjudicated_score"] = 3.0
        illegal_adj.loc[idx, "adjudication_note"] = "Synthetic illegal override"
        illegal_path = root / "illegal_override.csv"
        illegal_adj.to_csv(illegal_path, index=False)
        illegal = subprocess.run(
            [
                sys.executable,
                str(HERE / "freeze_ikes.py"),
                str(illegal_path),
                "--output",
                str(root / "illegal_frozen.csv"),
                "--coder-a",
                str(a_path),
                "--coder-b",
                str(b_path),
                "--coder-b-notes",
                str(b_notes),
                "--coder-b-raw",
                str(raw_path),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        if illegal.returncode == 0:
            raise AssertionError("Unflagged IKES manual override was incorrectly accepted")

        contaminated = raw.replace(
            "INDEPENDENCE_STATUS: PASS", "INDEPENDENCE_STATUS: FAIL"
        )
        contaminated_path = root / "contaminated.md"
        contaminated_path.write_text(contaminated, encoding="utf-8")
        bad = subprocess.run(
            [
                sys.executable,
                str(HERE / "ingest_coder_b.py"),
                str(contaminated_path),
                "--output-csv",
                str(root / "bad.csv"),
                "--output-notes",
                str(root / "bad.md"),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        if bad.returncode == 0:
            raise AssertionError("Contaminated Coder B fixture was incorrectly accepted")

        print(
            {
                "status": "PASS",
                "pipeline": "raw -> ingest -> adjudicate -> freeze",
                "synthetic_only": True,
                "contamination_rejection": True,
                "unflagged_override_rejection": True,
            }
        )


if __name__ == "__main__":
    main()
