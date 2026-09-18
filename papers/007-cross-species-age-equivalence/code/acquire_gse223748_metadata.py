#!/usr/bin/env python3
"""ARIS4C007 Pilot 3B: metadata-first audit of GEO GSE223748.

Downloads GEO sample metadata only. The 4.2 GB normalized beta matrix and
11 GB raw archive are deliberately not downloaded.

Primary route: GEO Accession Display metadata-only SOFT query.
Fallback: compressed family SOFT, still parsing only SAMPLE metadata fields.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import io
import json
import math
import re
import statistics
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable

GSE = "GSE223748"
BRIEF_URL = (
    "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?"
    "acc=GSE223748&targ=gsm&view=brief&form=text"
)
FAMILY_SOFT_URL = (
    "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE223nnn/GSE223748/"
    "soft/GSE223748_family.soft.gz"
)

PILOT2_SPECIES = {
    "Homo sapiens",
    "Felis catus",
    "Mus musculus",
    "Pan troglodytes",
}

AGE_KEY_HINTS = (
    "age",
    "chronological age",
    "chronologic age",
    "age years",
    "age year",
    "age yrs",
    "age yr",
)

SEX_KEY_HINTS = ("sex", "gender")
TISSUE_KEY_HINTS = ("tissue", "tissue type", "organ", "source tissue")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def get(url: str) -> tuple[bytes, str, str]:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (compatible; ARIS4C007/1.0; "
                "+https://github.com/CochraneK/ARIS4C)"
            ),
            "Accept": "text/plain,*/*",
        },
    )
    with urllib.request.urlopen(req, timeout=240) as r:
        return r.read(), r.geturl(), r.headers.get("Content-Type", "")


def parse_soft_lines(lines: Iterable[str]) -> list[dict[str, object]]:
    samples: list[dict[str, object]] = []
    current: dict[str, object] | None = None

    for raw in lines:
        line = raw.rstrip("\r\n")
        if line.startswith("^SAMPLE = "):
            if current is not None:
                samples.append(current)
            current = {
                "geo_accession": line.split("=", 1)[1].strip(),
                "characteristics": [],
            }
            continue
        if current is None:
            continue
        if line.startswith("^") and not line.startswith("^SAMPLE"):
            samples.append(current)
            current = None
            continue
        if not line.startswith("!Sample_"):
            continue

        key, sep, value = line.partition("=")
        if not sep:
            continue
        key = key.strip()[len("!Sample_"):]
        value = value.strip()

        if key == "characteristics_ch1":
            current["characteristics"].append(value)
        else:
            old = current.get(key)
            if old is None:
                current[key] = value
            elif isinstance(old, list):
                old.append(value)
            else:
                current[key] = [old, value]

    if current is not None:
        samples.append(current)
    return samples


def normalize_key(text: str) -> str:
    text = text.strip().lower().replace("_", " ")
    text = re.sub(r"\s+", " ", text)
    return text


def characteristic_map(values: list[str]) -> dict[str, list[str]]:
    out: dict[str, list[str]] = defaultdict(list)
    for item in values:
        if ":" in item:
            k, v = item.split(":", 1)
            out[normalize_key(k)].append(v.strip())
        else:
            out["__unkeyed__"].append(item.strip())
    return dict(out)


def first_char(cmap: dict[str, list[str]], hints: tuple[str, ...]) -> str:
    for hint in hints:
        if hint in cmap and cmap[hint]:
            return cmap[hint][0]
    for key, values in cmap.items():
        if any(hint in key for hint in hints) and values:
            return values[0]
    return ""


def parse_age_years(raw: str) -> tuple[float | None, str]:
    """Conservative parser. Returns years only for explicit/credible age values."""
    if not raw:
        return None, ""
    s = raw.strip().lower()
    if s in {"na", "n/a", "unknown", "none", "not available"}:
        return None, ""

    # Ranges are preserved as raw but use midpoint for metadata stratification.
    nums = [float(x) for x in re.findall(r"(?<![A-Za-z])(-?\d+(?:\.\d+)?)", s)]
    if not nums:
        return None, ""

    if len(nums) >= 2 and re.search(r"\b(to|[-–—])\b", s):
        val = (nums[0] + nums[1]) / 2
    else:
        val = nums[0]

    if "day" in s:
        return val / 365.25, "days"
    if "week" in s:
        return val * 7 / 365.25, "weeks"
    if "month" in s:
        return val / 12, "months"
    if "year" in s or "yr" in s:
        return val, "years"

    # Consortium metadata commonly stores age as numeric years. Accept a
    # plausible mammalian range but flag the unit as inferred.
    if -1.0 <= val <= 250:
        return val, "inferred_years"
    return None, ""


def clean_scalar(x: object) -> str:
    if isinstance(x, list):
        return " | ".join(str(v) for v in x)
    return "" if x is None else str(x)


def load_species_from_pilot0(path: Path) -> set[str]:
    out=set()
    with path.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            for key in ("source_species", "species", "SpeciesLatinName"):
                v=(row.get(key) or "").strip()
                if v and v != "Homo sapiens":
                    out.add(v)
                    break
    out.add("Homo sapiens")
    return out


def load_species_from_peron(path: Path) -> set[str]:
    out=set()
    with path.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            for key in ("Species", "species", "SpeciesLatinName", "species_name"):
                v=(row.get(key) or "").strip()
                if v:
                    out.add(v)
                    break
    return out


def load_species_from_translating_time(path: Path) -> set[str]:
    mapping={
        "Felis": "Felis catus",
        "Mus musculus": "Mus musculus",
        "Pan troglodytes": "Pan troglodytes",
        "Homo sapiens": "Homo sapiens",
    }
    out=set()
    with path.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            v=(row.get("Species") or "").strip()
            if v:
                out.add(mapping.get(v, v))
    return out


def quantiles(xs: list[float]) -> dict[str, float]:
    if not xs:
        return {}
    ys=sorted(xs)
    def q(p: float) -> float:
        if len(ys)==1:
            return ys[0]
        pos=(len(ys)-1)*p
        lo=int(math.floor(pos)); hi=int(math.ceil(pos))
        if lo==hi: return ys[lo]
        return ys[lo]*(hi-pos)+ys[hi]*(pos-lo)
    return {
        "min": ys[0],
        "q25": q(0.25),
        "median": q(0.5),
        "q75": q(0.75),
        "max": ys[-1],
    }


def select_bounded(rows: list[dict[str, object]], per_species: int = 24) -> list[dict[str, object]]:
    """Deterministic age-spread sample for Pilot2-overlap species.

    This is metadata selection only. Pilot 3C may later narrow further by
    tissue and training-membership before downloading individual IDATs.
    """
    chosen=[]
    for sp in sorted(PILOT2_SPECIES):
        pool=[
            r for r in rows
            if r["organism"]==sp and isinstance(r["age_years"], float)
            and math.isfinite(r["age_years"])
        ]
        pool=sorted(pool, key=lambda r:(r["age_years"], r["geo_accession"]))
        if not pool:
            continue
        if len(pool)<=per_species:
            picks=pool
        else:
            idx=sorted({
                round(i*(len(pool)-1)/(per_species-1))
                for i in range(per_species)
            })
            picks=[pool[i] for i in idx]
        for r in picks:
            x=dict(r)
            x["selection_reason"]="Pilot2 species overlap; deterministic age-spread metadata sample"
            chosen.append(x)
    return chosen


def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--pilot0-grid", type=Path)
    ap.add_argument("--peron", type=Path)
    ap.add_argument("--translating-time", type=Path)
    args=ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    attempts=[]
    payload=None
    route=""
    try:
        body, final, ctype=get(BRIEF_URL)
        text=body.decode("utf-8", errors="replace")
        parsed=parse_soft_lines(io.StringIO(text))
        if len(parsed)<1000:
            raise RuntimeError(f"metadata-only query returned only {len(parsed)} samples")
        payload=body
        route="GEO accession metadata-only SOFT query"
        attempts.append({
            "url": BRIEF_URL, "final_url": final, "content_type": ctype,
            "bytes": len(body), "sha256": sha256_bytes(body),
            "parsed_samples": len(parsed), "success": True,
        })
        raw_samples=parsed
    except Exception as exc:
        attempts.append({"url": BRIEF_URL, "success": False, "error": f"{type(exc).__name__}: {exc}"})
        body, final, ctype=get(FAMILY_SOFT_URL)
        if not body.startswith(b"\x1f\x8b"):
            raise RuntimeError("GEO family SOFT fallback was not gzip")
        text=gzip.decompress(body).decode("utf-8", errors="replace")
        raw_samples=parse_soft_lines(io.StringIO(text))
        if len(raw_samples)<1000:
            raise RuntimeError(f"family SOFT returned only {len(raw_samples)} samples")
        payload=body
        route="GEO compressed family SOFT fallback"
        attempts.append({
            "url": FAMILY_SOFT_URL, "final_url": final, "content_type": ctype,
            "bytes": len(body), "sha256": sha256_bytes(body),
            "parsed_samples": len(raw_samples), "success": True,
        })

    normalized=[]
    key_counts=Counter()
    for s in raw_samples:
        chars=s.get("characteristics") or []
        cmap=characteristic_map(chars)
        key_counts.update(cmap.keys())

        organism=clean_scalar(s.get("organism_ch1"))
        tissue=first_char(cmap, TISSUE_KEY_HINTS) or clean_scalar(s.get("source_name_ch1"))
        sex=first_char(cmap, SEX_KEY_HINTS)
        age_raw=first_char(cmap, AGE_KEY_HINTS)
        age_years, age_unit=parse_age_years(age_raw)

        normalized.append({
            "geo_accession": clean_scalar(s.get("geo_accession")),
            "title": clean_scalar(s.get("title")),
            "source_name": clean_scalar(s.get("source_name_ch1")),
            "organism": organism,
            "platform_id": clean_scalar(s.get("platform_id")),
            "tissue_raw": tissue,
            "sex_raw": sex,
            "age_raw": age_raw,
            "age_years": age_years if age_years is not None else "",
            "age_parse_unit": age_unit,
            "characteristics_json": json.dumps(cmap, ensure_ascii=False, sort_keys=True),
        })

    # Remove duplicate GSM records defensively.
    dedup={}
    for row in normalized:
        dedup[row["geo_accession"]]=row
    normalized=list(dedup.values())

    metadata_path=args.out/"sample_metadata.csv"
    with metadata_path.open("w", encoding="utf-8", newline="") as f:
        w=csv.DictWriter(f, fieldnames=list(normalized[0]))
        w.writeheader(); w.writerows(normalized)

    field_path=args.out/"characteristic_field_inventory.csv"
    with field_path.open("w", encoding="utf-8", newline="") as f:
        w=csv.writer(f)
        w.writerow(["characteristic_key","sample_occurrences"])
        for key,n in key_counts.most_common():
            w.writerow([key,n])

    bounded=select_bounded(normalized)
    bounded_path=args.out/"bounded_pilot2_overlap_sample.csv"
    with bounded_path.open("w", encoding="utf-8", newline="") as f:
        fields=list(bounded[0]) if bounded else list(normalized[0])+["selection_reason"]
        w=csv.DictWriter(f, fieldnames=fields)
        w.writeheader(); w.writerows(bounded)

    organisms=Counter(r["organism"] for r in normalized if r["organism"])
    tissues=Counter(r["tissue_raw"] for r in normalized if r["tissue_raw"])
    sexes=Counter(r["sex_raw"] for r in normalized if r["sex_raw"])
    platforms=Counter(r["platform_id"] for r in normalized if r["platform_id"])
    ages=[float(r["age_years"]) for r in normalized if r["age_years"]!=""]

    pilot0=load_species_from_pilot0(args.pilot0_grid) if args.pilot0_grid and args.pilot0_grid.exists() else set()
    peron=load_species_from_peron(args.peron) if args.peron and args.peron.exists() else set()
    tt=load_species_from_translating_time(args.translating_time) if args.translating_time and args.translating_time.exists() else set()
    gse_species=set(organisms)

    bounded_by_species=Counter(r["organism"] for r in bounded)
    bounded_by_tissue=Counter(r["tissue_raw"] for r in bounded)

    summary={
        "gse": GSE,
        "acquisition_route": route,
        "download_attempts": attempts,
        "n_samples": len(normalized),
        "n_unique_species": len(gse_species),
        "n_unique_tissue_labels": len(tissues),
        "n_samples_with_parseable_age": len(ages),
        "age_years_summary": quantiles(ages),
        "platform_counts": dict(platforms),
        "sex_raw_top": sexes.most_common(20),
        "tissue_raw_top": tissues.most_common(30),
        "characteristic_key_top": key_counts.most_common(50),
        "overlap": {
            "pilot0_species_n": len(gse_species & pilot0),
            "pilot0_species": sorted(gse_species & pilot0),
            "pilot1_peron_species_n": len(gse_species & peron),
            "pilot1_peron_species": sorted(gse_species & peron),
            "pilot2_species_n": len(gse_species & tt),
            "pilot2_species": sorted(gse_species & tt),
        },
        "bounded_sample": {
            "n": len(bounded),
            "species_counts": dict(bounded_by_species),
            "tissue_top": bounded_by_tissue.most_common(30),
            "rule": "Up to 24 samples per Pilot-2-overlap species, evenly spread over parseable chronological age; metadata-only selection.",
        },
        "guardrails": [
            "No normalized beta matrix or raw IDAT archive was downloaded.",
            "Age parsing is conservative and retains raw values for audit.",
            "The bounded sample is provisional until tissue balance and training-membership flags are reviewed.",
            "Exact species-name overlap is descriptive and may undercount synonym/subspecies matches.",
        ],
    }
    (args.out/"summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False)+"\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__=="__main__":
    main()
