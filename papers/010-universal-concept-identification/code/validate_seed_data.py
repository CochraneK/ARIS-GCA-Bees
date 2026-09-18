"""Validate UCID constructed seed records.

Uses jsonschema when installed. Otherwise runs a conservative standard-library
check for required keys, duplicate IDs, and annotation maturity.
"""

from __future__ import annotations

import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
SEED = DATA / "seed" / "targets.v0.json"
SCHEMA = DATA / "ucid-target.schema.json"


def basic_validate(records, schema):
    required = set(schema["required"])
    seen = set()
    errors = []

    for index, record in enumerate(records):
        missing = sorted(required - set(record))
        if missing:
            errors.append(f"record {index}: missing {missing}")

        target_id = record.get("target_id")
        if target_id in seen:
            errors.append(f"duplicate target_id: {target_id}")
        seen.add(target_id)

        if record.get("annotation_status") != "constructed_seed":
            errors.append(
                f"{target_id}: expected constructed_seed maturity in seed dataset"
            )

    return errors


def main():
    package = json.loads(SEED.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    records = package["targets"]

    errors = basic_validate(records, schema)

    try:
        import jsonschema  # type: ignore
    except ImportError:
        jsonschema = None

    if jsonschema is not None:
        validator = jsonschema.Draft202012Validator(schema)
        for record in records:
            for error in validator.iter_errors(record):
                errors.append(f"{record.get('target_id')}: {error.message}")

    if errors:
        print("FAIL")
        for error in errors:
            print("-", error)
        raise SystemExit(1)

    print("PASS")
    print("records:", len(records))
    print("full_jsonschema:", jsonschema is not None)
    print("annotation_status: constructed_seed only")


if __name__ == "__main__":
    main()
