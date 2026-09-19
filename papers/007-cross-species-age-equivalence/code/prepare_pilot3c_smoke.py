#!/usr/bin/env python3
"""Prepare a deterministic bounded Pilot 3C molecular smoke sample.

Consumes:
- Pilot 3B independent pan-clock holdout artifact (training=no samples)
- Pilot 0 canonical mapping artifact

Produces:
- smoke_sample.csv with up to 2 age-spread samples/species
- species_traits.csv with gestation/maturity/max-lifespan reconstructed from Pilot 0
- download_manifest.tsv with HTTPS IDAT URLs
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path

from build_pilot1_demography import load_pilot0_species


def age_spread(rows: list[dict[str, str]], n: int) -> list[dict[str, str]]:
    rows=sorted(rows,key=lambda r:(float(r["age_years"]),r["geo_accession"]))
    if len(rows)<=n:
        return rows
    if n==1:
        return [rows[len(rows)//2]]
    idx=sorted({round(i*(len(rows)-1)/(n-1)) for i in range(n)})
    return [rows[i] for i in idx]


def https_url(url: str) -> str:
    url=url.strip()
    if url.startswith("ftp://ftp.ncbi.nlm.nih.gov/"):
        return "https://ftp.ncbi.nlm.nih.gov/"+url.split("ftp://ftp.ncbi.nlm.nih.gov/",1)[1]
    return url


def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--holdout",type=Path,required=True)
    ap.add_argument("--pilot0-grid",type=Path,required=True)
    ap.add_argument("--pilot0-coverage",type=Path,required=True)
    ap.add_argument("--out",type=Path,required=True)
    ap.add_argument("--per-species",type=int,default=2)
    args=ap.parse_args()
    args.out.mkdir(parents=True,exist_ok=True)

    with args.holdout.open(encoding="utf-8",newline="") as f:
        holdout=list(csv.DictReader(f))

    by_species=defaultdict(list)
    for r in holdout:
        try:
            age=float(r["age_years"])
        except Exception:
            continue
        if not math.isfinite(age):
            continue
        by_species[r["organism"]].append(r)

    selected=[]
    for sp in sorted(by_species):
        selected.extend(age_spread(by_species[sp],args.per_species))

    if not selected:
        raise RuntimeError("no smoke samples selected")

    species_times,upstream=load_pilot0_species(args.pilot0_grid,args.pilot0_coverage)

    smoke_path=args.out/"smoke_sample.csv"
    fields=list(selected[0].keys())
    with smoke_path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields)
        w.writeheader();w.writerows(selected)

    trait_rows=[]
    for sp in sorted({r["organism"] for r in selected}):
        s=species_times.get(sp)
        if s is None:
            raise RuntimeError(f"{sp}: missing Pilot0 life-history traits")
        trait_rows.append({
            "species":sp,
            "gestation_y":s.gestation_y,
            "maturity_y":s.maturity_y,
            "max_lifespan_y":s.max_lifespan_y,
            "clock2_highmax_y":s.max_lifespan_y if sp in {"Homo sapiens","Mus musculus"} else 1.3*s.max_lifespan_y,
        })

    traits_path=args.out/"species_traits.csv"
    with traits_path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(trait_rows[0]))
        w.writeheader();w.writerows(trait_rows)

    downloads=[]
    for r in selected:
        urls=[https_url(x) for x in r["supplementary_files"].split("|") if x.strip()]
        if len(urls)!=2:
            raise RuntimeError(f"{r['geo_accession']}: expected 2 IDAT URLs, found {len(urls)}")
        for url in urls:
            name=url.rsplit("/",1)[-1]
            downloads.append({
                "geo_accession":r["geo_accession"],
                "species":r["organism"],
                "url":url,
                "filename":name,
            })

    manifest=args.out/"download_manifest.tsv"
    with manifest.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(downloads[0]),delimiter="\t",lineterminator="\n")
        w.writeheader();w.writerows(downloads)

    summary={
        "n_samples":len(selected),
        "n_species":len(trait_rows),
        "species_counts":{sp:sum(r["organism"]==sp for r in selected) for sp in sorted(by_species)},
        "per_species_target":args.per_species,
        "pilot0_upstream":upstream,
    }
    (args.out/"prep_summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary,indent=2))


if __name__=="__main__":
    main()
