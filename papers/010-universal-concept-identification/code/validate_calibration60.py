"""Validate the generated OEWN calibration60 source pool."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DATA = ROOT / "data"
MANIFEST = DATA / "calibration60" / "selection_manifest.v0.json"
POOL = DATA / "calibration60" / "oewn_source_pool.generated.json"


def main():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    pool = json.loads(POOL.read_text(encoding="utf-8"))
    records = pool["records"]

    assert pool["source_release"] == "oewn:2025"
    assert len(records) == 60
    assert len({r["source_record_id"] for r in records}) == 60
    assert len({r["sense_id"] for r in records}) == 60

    counts = Counter(r["lemma"] for r in records)
    expected = {lemma: manifest["senses_per_lemma"] for lemma in manifest["lemma_groups"]}
    assert dict(counts) == expected, (dict(counts), expected)

    for record in records:
        assert record["group_id"] == f"lemma:{record['lemma']}"
        assert record["part_of_speech"] == "n"
        assert record["definition"].strip()
        assert record["source_release"] == "oewn:2025"

    print("PASS calibration60 validation")
    print("records: 60")
    print("groups: 10")
    print("senses/group: 6")


if __name__ == "__main__":
    main()
