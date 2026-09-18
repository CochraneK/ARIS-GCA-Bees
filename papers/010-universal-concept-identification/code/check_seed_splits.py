"""Check leakage and completeness of UCID synthetic seed splits."""

from __future__ import annotations

import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SEED_DIR = HERE.parent / "data" / "seed"


def main():
    package = json.loads((SEED_DIR / "targets.v0.json").read_text(encoding="utf-8"))
    splits = json.loads((SEED_DIR / "splits.v0.json").read_text(encoding="utf-8"))

    target_ids = {row["target_id"] for row in package["targets"]}
    memberships = {}

    for split_name in ("development", "calibration", "test"):
        for target_id in splits[split_name]:
            if target_id in memberships:
                raise SystemExit(
                    f"FAIL: {target_id} appears in both "
                    f"{memberships[target_id]} and {split_name}"
                )
            memberships[target_id] = split_name

    assigned = set(memberships)
    missing = target_ids - assigned
    extra = assigned - target_ids
    if missing or extra:
        raise SystemExit(f"FAIL: missing={sorted(missing)} extra={sorted(extra)}")

    for group_name, members in splits.get("forced_groups", {}).items():
        locations = {memberships[m] for m in members}
        if len(locations) != 1:
            raise SystemExit(
                f"FAIL: leakage group {group_name} crosses splits: {sorted(locations)}"
            )

    print("PASS")
    print("targets:", len(target_ids))
    for split_name in ("development", "calibration", "test"):
        print(split_name + ":", len(splits[split_name]))
    print("forced groups checked:", len(splits.get("forced_groups", {})))


if __name__ == "__main__":
    main()
