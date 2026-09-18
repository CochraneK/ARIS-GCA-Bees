#!/usr/bin/env python3
"""Build the primary OpenAlex ISO2 <-> canonical ISO3 crosswalk.

The primary former-colony analysis universe is anchored to the current-state
COLDAT exposure table. This avoids treating every OpenAlex ISO geography as an
independent sovereign state and automatically leaves territories outside the
primary estimand unless a later preregistered sensitivity explicitly adds them.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

try:
    from countrycode import countrycode
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Install code/requirements.txt first (missing countrycode)") from exc


def convert(iso3: str) -> str | None:
    try:
        value = countrycode([iso3], origin="iso3c", destination="iso2c")
        if isinstance(value, (list, tuple)):
            value = value[0] if value else None
        elif hasattr(value, "to_list"):
            vals = value.to_list()
            value = vals[0] if vals else None
    except Exception:
        return None
    if value is None:
        return None
    value = str(value).strip().upper()
    return value if len(value) == 2 and value not in {"NA", "NAN"} else None


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("coldat_exposure_csv", type=Path)
    p.add_argument("output_csv", type=Path)
    p.add_argument("--unresolved-output", type=Path)
    args = p.parse_args()

    df = pd.read_csv(args.coldat_exposure_csv)
    required = {"country", "iso3c", "years_colonized_total"}
    missing = required - set(df.columns)
    if missing:
        raise SystemExit(f"COLDAT exposure table missing: {sorted(missing)}")

    out = df[["country", "iso3c"]].drop_duplicates().copy()
    out["iso3c"] = out["iso3c"].astype(str).str.upper()
    out["openalex_iso2"] = out["iso3c"].map(convert)
    out["status"] = out["openalex_iso2"].notna().map(
        {True: "RESOLVED", False: "UNRESOLVED_REVIEW_REQUIRED"}
    )
    out["mapping_method"] = "countrycode iso3c->iso2c; universe anchored to COLDAT current states"

    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    resolved = out[out["status"] == "RESOLVED"].sort_values("iso3c")
    resolved.to_csv(args.output_csv, index=False)

    unresolved_path = args.unresolved_output or args.output_csv.with_name(
        args.output_csv.stem + "_UNRESOLVED.csv"
    )
    unresolved = out[out["status"] != "RESOLVED"].sort_values("iso3c")
    unresolved.to_csv(unresolved_path, index=False)

    print(f"resolved={len(resolved)} unresolved={len(unresolved)}")
    print(args.output_csv)
    if len(unresolved):
        print(f"Review required: {unresolved_path}")
        print(unresolved.to_string(index=False))
        raise SystemExit(2)


if __name__ == "__main__":
    main()
