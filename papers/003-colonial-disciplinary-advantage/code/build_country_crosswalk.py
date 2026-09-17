#!/usr/bin/env python3
"""Build an auditable ICOW/COW -> modern ISO3 crosswalk for ARIS4C003.

Historical identifiers must never be silently forced onto a modern state.
Rows that cannot be mapped cleanly remain UNRESOLVED for manual review.

Requires the Python `countrycode` package, whose panel dictionary explicitly
supports Correlates of War codes and historical country-year reconciliation.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import pandas as pd

try:
    from countrycode import countrycode, load_codelist_panel
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Missing dependency `countrycode`. Install paper003/code/requirements.txt first."
    ) from exc


def pick(columns: list[str], candidates: list[str]) -> str | None:
    lookup = {c.lower(): c for c in columns}
    for candidate in candidates:
        if candidate.lower() in lookup:
            return lookup[candidate.lower()]
    return None


def load_overrides(path: Path | None) -> dict[tuple[str, str], tuple[str, str]]:
    if path is None or not path.exists():
        return {}
    out: dict[tuple[str, str], tuple[str, str]] = {}
    with path.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            if not row.get("key_type") or not row.get("key") or not row.get("iso3c"):
                continue
            out[(row["key_type"].strip(), row["key"].strip())] = (
                row["iso3c"].strip().upper(),
                row.get("note", "").strip(),
            )
    return out


def safe_convert(value: object, origin: str) -> str | None:
    if pd.isna(value):
        return None
    try:
        ans = countrycode(value, origin=origin, destination="iso3c", warn=False)
    except Exception:
        return None
    if ans is None:
        return None
    ans = str(ans).strip().upper()
    if len(ans) != 3 or ans in {"NA", "NAN", "NONE"}:
        return None
    return ans


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_csv", type=Path)
    parser.add_argument("output_csv", type=Path)
    parser.add_argument("--overrides", type=Path)
    parser.add_argument("--cow-numeric-col")
    parser.add_argument("--cow-char-col")
    parser.add_argument("--name-col")
    parser.add_argument("--year-col")
    args = parser.parse_args()

    df = pd.read_csv(args.input_csv)
    cols = list(df.columns)
    cown_col = args.cow_numeric_col or pick(cols, ["cown", "ccode", "cowcode", "cow_num"])
    cowc_col = args.cow_char_col or pick(cols, ["cowc", "stateabb", "cow_abbr", "state_abbr"])
    name_col = args.name_col or pick(cols, ["country", "state", "statenme", "state_name", "name"])
    year_col = args.year_col or pick(cols, ["year", "independence_year", "indepyear"])
    overrides = load_overrides(args.overrides)

    if not any([cown_col, cowc_col, name_col]):
        raise SystemExit(
            "Could not identify COW numeric/character or country-name column. "
            "Pass --cow-numeric-col/--cow-char-col/--name-col explicitly."
        )

    # Load once so package/version failures happen before any output is written.
    panel = load_codelist_panel()
    panel_columns = set(panel.columns)

    records: list[dict[str, object]] = []
    unique_cols = [c for c in [cown_col, cowc_col, name_col, year_col] if c]
    unique = df[unique_cols].drop_duplicates().reset_index(drop=True)

    for idx, row in unique.iterrows():
        cown = row[cown_col] if cown_col else None
        cowc = row[cowc_col] if cowc_col else None
        name = row[name_col] if name_col else None
        year = row[year_col] if year_col else None
        iso3: str | None = None
        method = ""
        note = ""

        for key_type, value in (("cown", cown), ("cowc", cowc), ("name", name)):
            if value is None or pd.isna(value):
                continue
            key = str(value).strip()
            if (key_type, key) in overrides:
                iso3, note = overrides[(key_type, key)]
                method = f"manual_override:{key_type}"
                break

        # Prefer a country-year panel match when year and COW code are available.
        if iso3 is None and year_col and not pd.isna(year) and "year" in panel_columns:
            try:
                yr = int(float(year))
                candidate = panel[panel["year"].eq(yr)]
                if cown_col and "cown" in panel_columns and not pd.isna(cown):
                    candidate = candidate[candidate["cown"].eq(int(float(cown)))]
                elif cowc_col and "cowc" in panel_columns and not pd.isna(cowc):
                    candidate = candidate[candidate["cowc"].astype(str).eq(str(cowc))]
                else:
                    candidate = candidate.iloc[0:0]
                vals = candidate["iso3c"].dropna().astype(str).unique() if "iso3c" in panel_columns else []
                if len(vals) == 1:
                    iso3 = vals[0].upper()
                    method = "countrycode_panel"
                elif len(vals) > 1:
                    note = "ambiguous country-year panel match"
            except Exception as exc:
                note = f"panel match failed: {type(exc).__name__}"

        if iso3 is None and cown_col and not pd.isna(cown):
            iso3 = safe_convert(cown, "cown")
            if iso3:
                method = "countrycode_cross_section:cown"
        if iso3 is None and cowc_col and not pd.isna(cowc):
            iso3 = safe_convert(cowc, "cowc")
            if iso3:
                method = "countrycode_cross_section:cowc"
        if iso3 is None and name_col and not pd.isna(name):
            iso3 = safe_convert(name, "country.name")
            if iso3:
                method = "countrycode_cross_section:name"

        status = "RESOLVED" if iso3 else "UNRESOLVED_REVIEW_REQUIRED"
        records.append(
            {
                "source_unique_row": idx,
                "source_cown": cown,
                "source_cowc": cowc,
                "source_name": name,
                "source_year": year,
                "iso3c": iso3 or "",
                "mapping_method": method,
                "status": status,
                "note": note,
            }
        )

    out = pd.DataFrame(records)
    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.output_csv, index=False)

    unresolved = int((out["status"] != "RESOLVED").sum())
    print(f"Wrote {len(out)} unique mappings to {args.output_csv}")
    print(f"Unresolved: {unresolved}")
    if unresolved:
        print("Gate remains open until every confirmatory-analysis entity is reviewed.")


if __name__ == "__main__":
    main()
