"""Filter and summarize AnimalTraits for ARIS4C008 pilot taxa.

The script accepts a local observations.csv or downloads the frozen Zenodo
AnimalTraits v1.0.7 observations.csv. It retains observation-level provenance
and writes a conservative species summary. Exemplar mappings are explicit and
never silently treated as exact-species matches.
"""
from __future__ import annotations
import argparse, csv, io, math, statistics, urllib.request
from pathlib import Path

DEFAULT_URL = "https://zenodo.org/records/6468938/files/observations.csv?download=1"
TRAITS = ("body mass", "metabolic rate", "brain size")

EXEMPLARS = {
    "Pongo spp.": ["Pongo pygmaeus", "Pongo abelii"],
    "Gorilla spp.": ["Gorilla gorilla", "Gorilla beringei"],
    "Sapajus spp.": ["Sapajus libidinosus"],
    "Macaca spp.": ["Macaca fuscata"],
}

def read_text(path_or_url: str) -> str:
    p = Path(path_or_url)
    if p.exists():
        return p.read_text(encoding="utf-8-sig")
    with urllib.request.urlopen(path_or_url, timeout=120) as r:
        return r.read().decode("utf-8-sig")

def finite_float(x):
    try:
        v = float(x)
        return v if math.isfinite(v) else None
    except (TypeError, ValueError):
        return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--observations", default=DEFAULT_URL)
    ap.add_argument("--pilot", default="../data/pilot_taxa.csv")
    ap.add_argument("--out-observations", default="../data/animaltraits_pilot_observations.csv")
    ap.add_argument("--out-summary", default="../data/animaltraits_pilot_summary.csv")
    args = ap.parse_args()

    pilot_rows = list(csv.DictReader(open(args.pilot, encoding="utf-8-sig")))
    wanted = {}
    for p in pilot_rows:
        label = p["scientific_name"].strip()
        if " spp." not in label and label != "Callitrichidae":
            wanted[label] = (p["taxon_id"], "exact_species", label)
        for exemplar in EXEMPLARS.get(label, []):
            wanted[exemplar] = (p["taxon_id"], "genus_exemplar", label)

    obs = list(csv.DictReader(io.StringIO(read_text(args.observations))))
    kept = []
    for r in obs:
        species = (r.get("species") or "").strip()
        if species not in wanted:
            continue
        taxon_id, scope, pilot_label = wanted[species]
        out = dict(r)
        out["taxon_id"] = taxon_id
        out["pilot_label"] = pilot_label
        out["evidence_scope"] = scope
        kept.append(out)

    if kept:
        fields = ["taxon_id", "pilot_label", "evidence_scope"] + [
            k for k in kept[0].keys() if k not in {"taxon_id","pilot_label","evidence_scope"}
        ]
        with open(args.out_observations, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader(); w.writerows(kept)

    summary = []
    for p in pilot_rows:
        tid, label = p["taxon_id"], p["scientific_name"].strip()
        rr = [r for r in kept if r["taxon_id"] == tid]
        row = {"taxon_id": tid, "scientific_name": label, "n_observations": len(rr)}
        for trait in TRAITS:
            vals = [finite_float(r.get(trait)) for r in rr]
            vals = [v for v in vals if v is not None]
            units = sorted({(r.get(trait + " - units") or "").strip() for r in rr if r.get(trait)})
            row[trait + "_n"] = len(vals)
            row[trait + "_median"] = statistics.median(vals) if vals else ""
            row[trait + "_units"] = ";".join(u for u in units if u)
        scopes = sorted({r["evidence_scope"] for r in rr})
        row["available_scope"] = ";".join(scopes) if scopes else "not_covered"
        summary.append(row)

    fields = ["taxon_id","scientific_name","n_observations","available_scope"]
    for t in TRAITS:
        fields += [t+"_n",t+"_median",t+"_units"]
    with open(args.out_summary, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader(); w.writerows(summary)

if __name__ == "__main__":
    main()
