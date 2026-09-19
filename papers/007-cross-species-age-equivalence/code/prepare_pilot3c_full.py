#!/usr/bin/env python3
"""Prepare all 50 independent pan-clock holdout samples for Pilot 3C.

Separates three trait vintages:
1. MMC v3.0.0 clock-era AnAge traits (primary reproduction);
2. GSE223748 embedded max-lifespan/maturity metadata (audit);
3. current Pilot0 AnAge traits (database-version sensitivity).

Gestation is unavailable in GSE metadata, so the GSE audit does not pretend to
be a complete inverse-transform parameter set.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

from build_pilot1_demography import load_pilot0_species


def fnum(x: str | None) -> float | None:
    try:
        y=float(str(x).strip())
        return y if math.isfinite(y) else None
    except Exception:
        return None


def https_url(url: str) -> str:
    url=url.strip()
    if url.startswith("ftp://ftp.ncbi.nlm.nih.gov/"):
        return "https://ftp.ncbi.nlm.nih.gov/"+url.split("ftp://ftp.ncbi.nlm.nih.gov/",1)[1]
    return url


def load_clockera(path: Path) -> dict[str, dict[str,str]]:
    with path.open(encoding="utf-8-sig",newline="") as f:
        rows=list(csv.DictReader(f))
    out={}
    for r in rows:
        sp=(r.get("SpeciesLatinName") or "").strip()
        if sp:
            out[sp]=r
    return out


def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--holdout",type=Path,required=True)
    ap.add_argument("--pilot0-grid",type=Path,required=True)
    ap.add_argument("--pilot0-coverage",type=Path,required=True)
    ap.add_argument("--clockera-anage",type=Path,required=True)
    ap.add_argument("--out",type=Path,required=True)
    args=ap.parse_args()
    args.out.mkdir(parents=True,exist_ok=True)

    with args.holdout.open(encoding="utf-8",newline="") as f:
        samples=list(csv.DictReader(f))
    if len(samples)!=50:
        raise RuntimeError(f"Expected frozen 50-sample holdout, found {len(samples)}")

    current,_=load_pilot0_species(args.pilot0_grid,args.pilot0_coverage)
    era=load_clockera(args.clockera_anage)

    species=sorted({r["organism"] for r in samples} | {"Homo sapiens"})
    traits=[]
    for sp in species:
        cur=current.get(sp)
        er=era.get(sp)
        if cur is None:
            raise RuntimeError(f"{sp}: absent from current Pilot0 traits")
        if er is None:
            raise RuntimeError(f"{sp}: absent from MMC v3.0.0 anage49.csv")

        eg=fnum(er.get("GestationTimeInYears"))
        em=fnum(er.get("averagedMaturity.yrs"))
        eL=fnum(er.get("maxAge"))
        if None in (eg,em,eL):
            raise RuntimeError(f"{sp}: incomplete MMC clock-era traits")

        sp_rows=[r for r in samples if r["organism"]==sp]
        gse_m={fnum(r.get("sexual_maturity_years")) for r in sp_rows}
        gse_L={fnum(r.get("maximum_lifespan_years")) for r in sp_rows}
        gse_m.discard(None);gse_L.discard(None)

        if len(gse_m)>1 or len(gse_L)>1:
            raise RuntimeError(f"{sp}: inconsistent GSE life-history metadata")

        traits.append({
            "species":sp,
            "clockera_gestation_y":eg,
            "clockera_maturity_y":em,
            "clockera_max_lifespan_y":eL,
            "clockera_highmax_y":eL if sp in {"Homo sapiens","Mus musculus"} else 1.3*eL,
            "gse_maturity_y":next(iter(gse_m)) if gse_m else "",
            "gse_max_lifespan_y":next(iter(gse_L)) if gse_L else "",
            "current_gestation_y":cur.gestation_y,
            "current_maturity_y":cur.maturity_y,
            "current_max_lifespan_y":cur.max_lifespan_y,
            "current_highmax_y":cur.max_lifespan_y if sp in {"Homo sapiens","Mus musculus"} else 1.3*cur.max_lifespan_y,
        })

    trait_path=args.out/"species_traits_vintages.csv"
    with trait_path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(traits[0]))
        w.writeheader();w.writerows(traits)

    sample_path=args.out/"holdout50.csv"
    with sample_path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(samples[0]))
        w.writeheader();w.writerows(samples)

    dl=[]
    for r in samples:
        urls=[https_url(x) for x in r["supplementary_files"].split("|") if x.strip()]
        if len(urls)!=2:
            raise RuntimeError(f"{r['geo_accession']}: expected two IDATs")
        for url in urls:
            dl.append({
                "geo_accession":r["geo_accession"],
                "species":r["organism"],
                "url":url,
                "filename":url.rsplit("/",1)[-1],
            })
    with (args.out/"download_manifest.tsv").open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(dl[0]),delimiter="\t",lineterminator="\n")
        w.writeheader();w.writerows(dl)

    drift=[]
    for t in traits:
        drift.append({
            "species":t["species"],
            "maturity_current_minus_clockera_y":float(t["current_maturity_y"])-float(t["clockera_maturity_y"]),
            "max_current_minus_clockera_y":float(t["current_max_lifespan_y"])-float(t["clockera_max_lifespan_y"]),
            "gestation_current_minus_clockera_y":float(t["current_gestation_y"])-float(t["clockera_gestation_y"]),
        })

    summary={
        "n_samples":len(samples),
        "n_nonhuman_species":len({r["organism"] for r in samples}),
        "species_counts":{sp:sum(r["organism"]==sp for r in samples) for sp in sorted({r["organism"] for r in samples})},
        "trait_vintage_drift":drift,
        "primary_inverse_parameters":"MMC v3.0.0 UniversalPanMammalianClock/ClockParameters/anage49.csv",
        "sensitivity_inverse_parameters":"current Pilot0 official AnAge snapshot",
        "gse_embedded_traits":"used as a provenance/audit cross-check for maximum lifespan and maturity; GSE contains no gestation field",
    }
    (args.out/"prep_full_summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary,indent=2))


if __name__=="__main__":
    main()
