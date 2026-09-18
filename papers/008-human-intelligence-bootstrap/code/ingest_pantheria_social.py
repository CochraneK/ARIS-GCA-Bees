"""Extract Paper 008 mammal social-demography proxies from PanTHERIA.

Source file: PanTHERIA_1-0_WR05_Aug2008.txt
Original archive: https://ndownloader.figshare.com/files/5604752
Missing source code -999 is converted to blank.

These variables describe group size/density/range, not cultural-network
connectivity. They are J-module baseline demographic proxies.
"""
from __future__ import annotations
import csv, io, urllib.request, zipfile
from pathlib import Path

URL="https://ndownloader.figshare.com/files/5604752"
ALIASES={"Cebus libidinosus":"Sapajus libidinosus","Physeter catodon":"Physeter macrocephalus"}

def clean(v):
    v=(v or "").strip()
    return "" if v in {"","-999","-999.00"} else v

def main():
    base=Path(__file__).resolve().parents[1]
    panel={r["scientific_name"] for r in csv.DictReader(open(base/"data"/"pilot_taxa_v2.csv",encoding="utf-8-sig"))}
    blob=urllib.request.urlopen(URL,timeout=120).read()
    z=zipfile.ZipFile(io.BytesIO(blob))
    member=next(n for n in z.namelist() if n.endswith("PanTHERIA_1-0_WR05_Aug2008.txt"))
    text=z.read(member).decode("utf-8-sig").replace("\r\n","\n").replace("\r","\n")
    rows=list(csv.DictReader(io.StringIO(text,newline=""),delimiter="\t"))
    out=[]
    for r in rows:
        src=(r.get("MSW05_Binomial") or "").strip()
        sp=ALIASES.get(src,src)
        if sp not in panel: continue
        out.append({
            "scientific_name":sp,
            "source_name":src,
            "taxon_mapping":"explicit_synonym" if src in ALIASES else "exact_name",
            "population_group_size":clean(r.get("10-1_PopulationGrpSize")),
            "social_group_size":clean(r.get("10-2_SocialGrpSize")),
            "population_density_per_km2":clean(r.get("21-1_PopulationDensity_n/km2")),
            "home_range_km2":clean(r.get("22-1_HomeRange_km2")),
            "home_range_indiv_km2":clean(r.get("22-2_HomeRange_Indiv_km2")),
        })
    fields=list(out[0])
    out=sorted(out,key=lambda x:x["scientific_name"])
    path=base/"data"/"pantheria_social_demography_v0.csv"
    with open(path,"w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(out)
    print("matched",len(out),
          "social_group",sum(bool(x["social_group_size"]) for x in out),
          "population_group",sum(bool(x["population_group_size"]) for x in out),
          "density",sum(bool(x["population_density_per_km2"]) for x in out))

if __name__=="__main__":
    main()
