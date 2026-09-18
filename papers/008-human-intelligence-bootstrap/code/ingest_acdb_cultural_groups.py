"""Extract ACDB cultural-group context for the ARIS4C008 v2 panel.

Upstream:
https://raw.githubusercontent.com/datadiversitylab/ACDB/main/db/table_csvs/species.csv
https://raw.githubusercontent.com/datadiversitylab/ACDB/main/db/table_csvs/groups.csv

Exact species are retained directly. Subspecies nested under one panel species
are retained with evidence_scope='subspecies_nested'. Group-size strings that
are not plain numeric values remain in size_raw and are never coerced to zero.
"""
from __future__ import annotations
import csv, io, urllib.request
from pathlib import Path

SPECIES_URL="https://raw.githubusercontent.com/datadiversitylab/ACDB/main/db/table_csvs/species.csv"
GROUPS_URL="https://raw.githubusercontent.com/datadiversitylab/ACDB/main/db/table_csvs/groups.csv"

def read_csv(url):
    text=urllib.request.urlopen(url,timeout=90).read().decode("utf-8-sig")
    return list(csv.DictReader(io.StringIO(text)))

def number_or_blank(x):
    try:
        s=(x or "").strip()
        if s in {"","NA","not searched"}: return ""
        return float(s)
    except ValueError:
        return ""

def main():
    base=Path(__file__).resolve().parents[1]
    panel=[r["scientific_name"] for r in csv.DictReader(open(base/"data"/"pilot_taxa_v2.csv",encoding="utf-8-sig"))]
    species=read_csv(SPECIES_URL); groups=read_csv(GROUPS_URL)
    smap={r["species_id"]:r for r in species}
    out=[]
    for g in groups:
        s=smap.get(g["species_id"])
        if not s: continue
        canon=s["canonicalName"]
        if canon in panel:
            target,scope=canon,"exact_species"
        else:
            hits=[sp for sp in panel if canon.startswith(sp+" ")]
            if len(hits)!=1: continue
            target,scope=hits[0],"subspecies_nested"
        out.append({
            "panel_species":target,"source_canonical":canon,"evidence_scope":scope,
            "group_id":g["group_id"],"group_name":g["group_name"],
            "group_level":g["group_level"],"group_above":g["group_above"],
            "size_numeric":number_or_blank(g["size"]),"size_raw":g["size"],
            "size_evidence":g["size_evidence"],"size_date":g["size_date"],
            "size_source":g["size_source"],"lat":g["lat"],"long":g["long"],
        })
    fields=list(out[0])
    path=base/"data"/"acdb_cultural_groups_v0.csv"
    with open(path,"w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(out)
    print("rows",len(out),"species",len({r["panel_species"] for r in out}),
          "numeric_species",len({r["panel_species"] for r in out if r["size_numeric"]!=""}))

if __name__=="__main__":
    main()
