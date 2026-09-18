"""Extract ARIS4C008 exact species from the Animal Social Network Repository.

Network metrics are summarized by species only for coverage diagnostics.
Interaction type, population context and sampling methodology must remain in
formal models; density/transitivity from unlike interaction definitions are not
assumed directly comparable.
"""
from __future__ import annotations
import csv, statistics, urllib.request, io
from pathlib import Path

URL = "https://raw.githubusercontent.com/bansallab/asnr/master/Network_summary_masterfile.csv"

TARGETS = {
"Homo sapiens","Pan troglodytes","Pan paniscus","Pongo abelii","Pongo pygmaeus",
"Gorilla gorilla","Gorilla beringei","Sapajus libidinosus","Macaca fuscata",
"Callithrix jacchus","Leontopithecus rosalia","Corvus moneduloides","Corvus corax",
"Nestor notabilis","Cacatua goffiniana","Psittacus erithacus","Melopsittacus undulatus",
"Tursiops truncatus","Tursiops aduncus","Orcinus orca","Physeter macrocephalus",
"Megaptera novaeangliae","Loxodonta africana","Elephas maximus","Octopus vulgaris",
"Bombus terrestris","Apis mellifera","Columba livia","Suricata suricatta"
}

def num(x):
    try: return float(x)
    except: return None

def median(vals):
    vals=[v for v in vals if v is not None]
    return statistics.median(vals) if vals else ""

def main():
    text=urllib.request.urlopen(URL,timeout=90).read().decode("utf-8-sig")
    rows=list(csv.DictReader(io.StringIO(text)))
    hit=[r for r in rows if f"{r.get('genus','').strip()} {r.get('species','').strip()}".strip() in TARGETS]
    out=[]
    for sp in sorted({f"{r['genus'].strip()} {r['species'].strip()}" for r in hit}):
        rr=[r for r in hit if f"{r['genus'].strip()} {r['species'].strip()}"==sp]
        out.append({
            "scientific_name":sp,
            "n_networks":len(rr),
            "interaction_types":"; ".join(sorted({r.get("interaction_type","") for r in rr if r.get("interaction_type","")})),
            "population_types":"; ".join(sorted({r.get("population_type","") or "unspecified" for r in rr})),
            "median_nodes":median([num(r.get("nodes")) for r in rr]),
            "median_density":median([num(r.get("network.density")) for r in rr]),
            "median_avg_degree":median([num(r.get("avg.degree")) for r in rr]),
            "median_transitivity":median([num(r.get("transitivity")) for r in rr]),
            "median_Qrel":median([num(r.get("Qrel")) for r in rr]),
        })
    fields=list(out[0])
    path=Path(__file__).resolve().parents[1]/"data"/"asnr_pilot_summary.csv"
    with open(path,"w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(out)
    print(f"master_rows={len(rows)} matched_networks={len(hit)} matched_species={len(out)} output={path}")

if __name__=="__main__":
    main()
