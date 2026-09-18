"""Extract exact/synonym-resolved ARIS4C008 taxa from EltonTraits 1.0.

EltonTraits source files use Windows-1252 encoding and tab delimiters.
The source retains two older names that are explicitly reconciled here:
Cebus libidinosus -> Sapajus libidinosus
Physeter catodon -> Physeter macrocephalus
"""
from __future__ import annotations
import csv, io, urllib.request
from pathlib import Path

FILES = {
    "birds": "https://ndownloader.figshare.com/files/5631081",
    "mammals": "https://ndownloader.figshare.com/files/5631084",
}
ALIASES = {
    "Cebus libidinosus": "Sapajus libidinosus",
    "Physeter catodon": "Physeter macrocephalus",
}

def read_table(url):
    raw=urllib.request.urlopen(url,timeout=90).read()
    text=raw.decode("cp1252").replace("\r\n","\n").replace("\r","\n")
    return list(csv.DictReader(io.StringIO(text,newline=""),delimiter="\t"))

def main():
    base=Path(__file__).resolve().parents[1]
    panel={r["scientific_name"] for r in csv.DictReader(open(base/"data"/"pilot_taxa_v2.csv",encoding="utf-8-sig"))}
    out=[]
    diet_cols=["Diet-Inv","Diet-Vend","Diet-Vect","Diet-Vfish","Diet-Vunk","Diet-Scav","Diet-Fruit","Diet-Nect","Diet-Seed","Diet-PlantO"]
    for clade,url in FILES.items():
        for r in read_table(url):
            src=(r.get("Scientific") or "").strip()
            species=ALIASES.get(src,src)
            if species not in panel:
                continue
            x={"scientific_name":species,"source_scientific_name":src,"source_clade":clade,
               "taxon_mapping":"explicit_synonym" if src in ALIASES else "exact_name"}
            for k in diet_cols: x[k]=r.get(k,"")
            if clade=="birds":
                x["diet_summary"]=r.get("Diet-5Cat","")
                strata=[
                    ("below_water",r.get("ForStrat-watbelowsurf","")),("water_surface",r.get("ForStrat-wataroundsurf","")),
                    ("ground",r.get("ForStrat-ground","")),("understory",r.get("ForStrat-understory","")),
                    ("midhigh",r.get("ForStrat-midhigh","")),("canopy",r.get("ForStrat-canopy","")),
                    ("aerial",r.get("ForStrat-aerial",""))]
                x["foraging_stratum"]=";".join(f"{k}:{v}" for k,v in strata if v not in ("","0"))
                x["activity_nocturnal"]=r.get("Nocturnal","")
                x["activity_crepuscular"]=""; x["activity_diurnal"]=""
                x["diet_certainty"]=r.get("Diet-Certainty","")
                x["foraging_certainty"]=r.get("ForStrat-SpecLevel","")
                x["activity_certainty"]=""
            else:
                x["diet_summary"]=""
                x["foraging_stratum"]=r.get("ForStrat-Value","")
                x["activity_nocturnal"]=r.get("Activity-Nocturnal","")
                x["activity_crepuscular"]=r.get("Activity-Crepuscular","")
                x["activity_diurnal"]=r.get("Activity-Diurnal","")
                x["diet_certainty"]=r.get("Diet-Certainty","")
                x["foraging_certainty"]=r.get("ForStrat-Certainty","")
                x["activity_certainty"]=r.get("Activity-Certainty","")
            x["body_mass_g"]=r.get("BodyMass-Value","")
            out.append(x)

    fields=["scientific_name","source_scientific_name","source_clade","taxon_mapping"]+diet_cols+[
        "diet_summary","foraging_stratum","activity_nocturnal","activity_crepuscular","activity_diurnal",
        "body_mass_g","diet_certainty","foraging_certainty","activity_certainty"]
    out=sorted(out,key=lambda x:x["scientific_name"])
    with open(base/"data"/"eltontraits_pilot_v0.csv","w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(out)
    print(f"matched_species={len(out)}")

if __name__=="__main__":
    main()
