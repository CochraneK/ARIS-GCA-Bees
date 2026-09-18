"""Extract AnAge life-history traits for ARIS4C008 taxa.

Downloads the stable bulk AnAge dataset, preserves source data-quality fields,
and keeps exact-species versus exemplar matches explicit.
"""
from __future__ import annotations
import argparse, csv, io, urllib.request, zipfile
from pathlib import Path

URL = "https://genomics.senescence.info/species/dataset.zip"

EXEMPLARS = {
    "Pongo spp.": ["Pongo pygmaeus", "Pongo abelii"],
    "Gorilla spp.": ["Gorilla gorilla", "Gorilla beringei"],
    "Sapajus spp.": ["Sapajus libidinosus"],
    "Macaca spp.": ["Macaca fuscata"],
    "Callitrichidae": ["Callithrix jacchus", "Leontopithecus rosalia"],
    "Tursiops truncatus": ["Tursiops aduncus"],
}

KEEP = [
    "Common name","Female maturity (days)","Male maturity (days)",
    "Gestation/Incubation (days)","Weaning (days)","Litter/Clutch size",
    "Inter-litter/Interbirth interval","Adult weight (g)",
    "Maximum longevity (yrs)","Metabolic rate (W)","Body mass (g)",
    "Temperature (K)","Data quality"
]

def main():
    base = Path(__file__).resolve().parents[1]
    ap = argparse.ArgumentParser()
    ap.add_argument("--pilot", default=str(base / "data" / "pilot_taxa.csv"))
    ap.add_argument("--output", default=str(base / "data" / "anage_pilot_summary.csv"))
    args = ap.parse_args()

    with urllib.request.urlopen(URL, timeout=120) as r:
        blob = r.read()
    z = zipfile.ZipFile(io.BytesIO(blob))
    member = next(n for n in z.namelist() if n.endswith("anage_data.txt"))
    rows = list(csv.DictReader(io.StringIO(z.read(member).decode("utf-8-sig")), delimiter="\t"))

    pilot = list(csv.DictReader(open(args.pilot, encoding="utf-8-sig")))
    wanted = {}
    for p in pilot:
        label = p["scientific_name"].strip()
        if " spp." not in label and label != "Callitrichidae":
            wanted[label] = (p["taxon_id"], label, "exact_species")
        for sp in EXEMPLARS.get(label, []):
            wanted.setdefault(sp, (p["taxon_id"], label,
                                   "family_exemplar" if label == "Callitrichidae" else "genus_exemplar"))

    out = []
    for r in rows:
        sp = (r.get("Genus","") + " " + r.get("Species","")).strip()
        if sp not in wanted:
            continue
        taxon_id, label, scope = wanted[sp]
        x = {"taxon_id": taxon_id, "pilot_label": label,
             "evidence_scope": scope, "scientific_name": sp}
        for k in KEEP:
            x[k] = r.get(k, "")
        out.append(x)

    fields = ["taxon_id","pilot_label","evidence_scope","scientific_name"] + KEEP
    with open(args.output, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader(); w.writerows(out)

    print(f"bulk_rows={len(rows)} matched_rows={len(out)} output={args.output}")

if __name__ == "__main__":
    main()
