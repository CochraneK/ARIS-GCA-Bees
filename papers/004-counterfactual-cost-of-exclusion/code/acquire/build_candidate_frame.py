#!/usr/bin/env python3
"""Build a deterministic, mental-health-independent science pilot frame.

Source expected: Laouenan et al. cross-verified notable-people CSV(.gz).
The script *never* inspects mental-health fields or keywords. It samples within
historical/visibility strata from people classified by the source as
Discovery/Science, then writes a frozen candidate frame for identity resolution.

The verified compressed mirror contains legacy/mixed text bytes: strict UTF-8
fails, while Latin-1 decoding can expose UTF-8-as-Latin-1 mojibake in some cells.
We therefore decode losslessly as Latin-1 and repair a cell only when its bytes
round-trip cleanly as UTF-8. This avoids `errors=ignore` data loss.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import io
import math
from collections import defaultdict
from pathlib import Path
from typing import Iterable


def open_text(path: Path, encoding: str):
    raw = gzip.open(path, "rb") if path.suffix == ".gz" else path.open("rb")
    return io.TextIOWrapper(raw, encoding=encoding, newline="")


def repair_utf8_mojibake(value: str) -> str:
    """Repair UTF-8 bytes accidentally decoded as Latin-1 when reversible.

    A genuine Latin-1 string such as `Föhl` cannot decode as UTF-8 after
    Latin-1 re-encoding and is left untouched. A mojibaked `FÃ¶hl` round-trips
    to UTF-8 and becomes `Föhl`.
    """
    if not value:
        return value
    # Avoid rewriting ordinary ASCII and most genuine Latin-1 strings.
    markers = ("Ã", "Â", "â", "ð", "¤", "€", "™", "œ", "ž")
    if not any(marker in value for marker in markers):
        return value
    try:
        repaired = value.encode("latin-1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return value
    return repaired


def clean_row(row: dict[str, str]) -> dict[str, str]:
    return {key: repair_utf8_mojibake(value) if isinstance(value, str) else value for key, value in row.items()}


def parse_int(value: str) -> int | None:
    value = (value or "").strip()
    if not value or value.lower() in {"missing", "nan", "na"}:
        return None
    try:
        return int(float(value))
    except ValueError:
        return None


def parse_float(value: str) -> float | None:
    value = (value or "").strip()
    if not value or value.lower() in {"missing", "nan", "na"}:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def cohort(birth: int) -> str:
    if birth < 1875:
        return "pre1875"
    if birth < 1900:
        return "1875_1899"
    if birth < 1925:
        return "1900_1924"
    if birth < 1950:
        return "1925_1949"
    return "1950plus"


def quantile_cutpoints(values: list[float]) -> tuple[float, float, float] | None:
    if len(values) < 4:
        return None
    values = sorted(values)

    def q(p: float) -> float:
        pos = p * (len(values) - 1)
        lo = math.floor(pos)
        hi = math.ceil(pos)
        if lo == hi:
            return values[lo]
        frac = pos - lo
        return values[lo] * (1 - frac) + values[hi] * frac

    return q(0.25), q(0.50), q(0.75)


def visibility_bucket(value: float | None, cuts: tuple[float, float, float] | None) -> str:
    if value is None or cuts is None:
        return "v_missing"
    q1, q2, q3 = cuts
    if value <= q1:
        return "v_q1"
    if value <= q2:
        return "v_q2"
    if value <= q3:
        return "v_q3"
    return "v_q4"


def stable_key(seed: int, row: dict[str, str]) -> str:
    identity = row.get("wikidata_code") or row.get("name") or ""
    payload = f"{seed}|{identity}|{row.get('birth','')}|{row.get('death','')}"
    return hashlib.sha256(payload.encode("utf-8", "replace")).hexdigest()


def round_robin_stratified_sample(
    strata: dict[str, list[dict[str, str]]], target: int, seed: int
) -> list[dict[str, str]]:
    for rows in strata.values():
        rows.sort(key=lambda r: stable_key(seed, r))

    keys = sorted(strata)
    chosen: list[dict[str, str]] = []
    index = {key: 0 for key in keys}
    while len(chosen) < target:
        progressed = False
        for key in keys:
            i = index[key]
            if i < len(strata[key]):
                chosen.append(strata[key][i])
                index[key] += 1
                progressed = True
                if len(chosen) >= target:
                    break
        if not progressed:
            break
    return chosen


def eligible_rows(
    reader: Iterable[dict[str, str]], birth_min: int, birth_max: int, death_min: int, death_max: int
) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for raw_row in reader:
        row = clean_row(raw_row)
        if (row.get("level1_main_occ") or "").strip().lower() != "discovery/science":
            continue
        birth = parse_int(row.get("birth", ""))
        death = parse_int(row.get("death", ""))
        qid = (row.get("wikidata_code") or "").strip()
        if birth is None or death is None or not qid:
            continue
        if not (birth_min <= birth <= birth_max and death_min <= death <= death_max):
            continue
        out.append(row)
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path, help="official cross-verified CSV or CSV.GZ")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--target", type=int, default=100)
    parser.add_argument("--seed", type=int, default=20260918)
    parser.add_argument("--encoding", default="latin-1")
    parser.add_argument("--birth-min", type=int, default=1850)
    parser.add_argument("--birth-max", type=int, default=1975)
    parser.add_argument("--death-min", type=int, default=1900)
    parser.add_argument("--death-max", type=int, default=2026)
    args = parser.parse_args()

    with open_text(args.source, args.encoding) as handle:
        reader = csv.DictReader(handle)
        required = {"wikidata_code", "name", "birth", "death", "level1_main_occ"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise SystemExit(f"Source is missing required columns: {sorted(missing)}")
        eligible = eligible_rows(
            reader, args.birth_min, args.birth_max, args.death_min, args.death_max
        )

    if not eligible:
        raise SystemExit("No eligible Discovery/Science rows after filters")

    vis_values = [
        value
        for value in (parse_float(row.get("sum_visib_ln_5criteria", "")) for row in eligible)
        if value is not None
    ]
    cuts = quantile_cutpoints(vis_values)

    strata: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in eligible:
        birth = parse_int(row.get("birth", ""))
        assert birth is not None
        vis = parse_float(row.get("sum_visib_ln_5criteria", ""))
        stratum = f"{cohort(birth)}|{visibility_bucket(vis, cuts)}"
        row = dict(row)
        row["_pilot_stratum"] = stratum
        strata[stratum].append(row)

    chosen = round_robin_stratified_sample(strata, args.target, args.seed)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "person_id",
        "canonical_name",
        "wikidata_qid",
        "birth_year",
        "death_year",
        "gender",
        "level1_main_occ",
        "level2_main_occ",
        "level3_main_occ",
        "region",
        "candidate_visibility",
        "candidate_frame_group",
        "pilot_stratum",
        "candidate_frame_source",
        "candidate_frame_record_id",
        "orcid",
        "openalex_author_id",
    ]
    with args.output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for idx, row in enumerate(chosen, start=1):
            qid = (row.get("wikidata_code") or "").strip()
            writer.writerow(
                {
                    "person_id": f"cv_{qid}",
                    "canonical_name": (row.get("name") or "").replace("_", " "),
                    "wikidata_qid": qid,
                    "birth_year": row.get("birth", ""),
                    "death_year": row.get("death", ""),
                    "gender": row.get("gender", ""),
                    "level1_main_occ": row.get("level1_main_occ", ""),
                    "level2_main_occ": row.get("level2_main_occ", ""),
                    "level3_main_occ": row.get("level3_main_occ", ""),
                    "region": row.get("un_region", "") or row.get("un_subregion", ""),
                    "candidate_visibility": row.get("sum_visib_ln_5criteria", ""),
                    "candidate_frame_group": row.get("group_wikipedia_editions", ""),
                    "pilot_stratum": row.get("_pilot_stratum", ""),
                    "candidate_frame_source": "Laouenan2022_cross_verified",
                    "candidate_frame_record_id": qid or str(idx),
                    "orcid": "",
                    "openalex_author_id": "",
                }
            )

    print(
        f"Eligible Discovery/Science rows: {len(eligible)}; "
        f"strata: {len(strata)}; sampled: {len(chosen)}; output: {args.output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
