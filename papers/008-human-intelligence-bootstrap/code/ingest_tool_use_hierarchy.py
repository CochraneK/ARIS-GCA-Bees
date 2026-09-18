"""Build the hierarchical 22-mode tool-use layer for ARIS4C008.

Source: https://github.com/StochasticBiology/tool-use
Johnston & Royrvik 2020, iScience, DOI 10.1016/j.isci.2020.101245.

Main source codes:
2 = observed in wild
1 = human influence cannot be discounted
0 = no observation in this source catalogue

IMPORTANT: 0 is not converted to tested biological absence.
"""
from __future__ import annotations
import csv, urllib.request
from pathlib import Path

ROOT="https://raw.githubusercontent.com/StochasticBiology/tool-use/master/Data/"
FILES={
    "modes":"modes.txt","taxa":"taxa-names.txt","obs":"all-observations.txt",
    "bird_names":"bird-names.txt","bird_obs":"bird-observations.txt",
}
TARGET_MAP={
 "Pan troglodytes":["Pan troglodytes"],"Pan paniscus":["Pan paniscus"],
 "Pongo pygmaeus":["Pongo pygmaeus"],"Gorilla gorilla":["Gorilla gorilla"],
 "Platyrrhini":["Sapajus libidinosus"],"Cercopithecidae":["Macaca fuscata"],
 "Cetacea":["Tursiops truncatus","Tursiops aduncus","Orcinus orca","Physeter macrocephalus","Megaptera novaeangliae"],
 "Elephantidae":["Loxodonta africana","Elephas maximus"],
 "Aves":["Corvus moneduloides","Corvus corax","Nestor notabilis","Cacatua goffiniana","Psittacus erithacus","Melopsittacus undulatus","Columba livia"],
 "Insecta":["Bombus terrestris","Apis mellifera"],"Cephalopoda":["Octopus vulgaris"],
}
BIRD_MAP={
 "Corvidae":["Corvus moneduloides","Corvus corax"],
 "Cacatuidae":["Cacatua goffiniana"],
 "Psittacidae":["Psittacus erithacus","Melopsittacus undulatus"],
 "Columbidae":["Columba livia"],
}

def lines(name):
    txt=urllib.request.urlopen(ROOT+FILES[name],timeout=90).read().decode("utf-8-sig")
    return [x.strip() for x in txt.splitlines() if x.strip()]

def main():
    base=Path(__file__).resolve().parents[1]
    modes=lines("modes"); taxa=lines("taxa")
    obs=[[int(v) for v in x.split()] for x in lines("obs")]
    bnames=lines("bird_names"); bobs=[[int(v) for v in x.split()] for x in lines("bird_obs")]
    out=[]
    for unit,vals in zip(taxa,obs):
        if unit not in TARGET_MAP: continue
        r={
          "unit_name":unit,"unit_level":"species_or_named_taxon" if " " in unit else "higher_taxon",
          "scope":"exact_species" if " " in unit else "clade_or_family",
          "panel_targets":";".join(TARGET_MAP[unit]),
          "wild_mode_count":sum(v==2 for v in vals),
          "human_influence_mode_count":sum(v==1 for v in vals),
          "total_observed_mode_count":sum(v>0 for v in vals),
        }
        r.update(dict(zip(modes,vals)));out.append(r)
    for unit,vals in zip(bnames,bobs):
        if unit not in BIRD_MAP: continue
        r={"unit_name":unit,"unit_level":"bird_family","scope":"family_presence_catalog",
           "panel_targets":";".join(BIRD_MAP[unit]),"wild_mode_count":"",
           "human_influence_mode_count":"","total_observed_mode_count":sum(v>0 for v in vals)}
        r.update(dict(zip(modes,vals)));out.append(r)
    fields=["unit_name","unit_level","scope","panel_targets","wild_mode_count",
            "human_influence_mode_count","total_observed_mode_count"]+modes
    with open(base/"data"/"tool_use_hierarchy_v0.csv","w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(out)
    print("rows",len(out),"exact_species",[r["unit_name"] for r in out if r["scope"]=="exact_species"])

if __name__=="__main__":
    main()
