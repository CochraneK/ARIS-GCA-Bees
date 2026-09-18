"""Extract exact ARIS4C008 species from the MacLean et al. (2014) self-control dataset.

The two tasks are standardized inhibitory-control proxies. Their scores are NOT
converted directly into a universal generative-cognition or intelligence score.
Taxonomically ambiguous source labels (e.g. "Gorilla", "Orangutan",
"Marmoset") are deliberately excluded from exact-species joins.
"""
from __future__ import annotations
import csv, io, statistics, urllib.request
from pathlib import Path

FILES = {
    "A_not_B": "https://ndownloader.figshare.com/files/9700537",
    "Cylinder": "https://ndownloader.figshare.com/files/9700540",
}
EXACT = {
    "Bonobo": ("Pan paniscus", "exact_species"),
    "Chimpanzee": ("Pan troglodytes", "exact_species"),
    "Elphas maximus": ("Elephas maximus", "exact_species_typo_in_source"),
    "White Carnea Pigeon": ("Columba livia", "exact_species_breed_label"),
    "White Carneau Pigeon": ("Columba livia", "exact_species_breed_label"),
}

def fetch_csv(url):
    text = urllib.request.urlopen(url, timeout=60).read().decode("utf-8-sig")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return list(csv.DictReader(io.StringIO(text, newline="")))

def main():
    base = Path(__file__).resolve().parents[1]
    out = []
    for task, url in FILES.items():
        rows = fetch_csv(url)
        for label, (species, scope) in EXACT.items():
            rr = [r for r in rows if r["Species"] == label]
            if not rr:
                continue
            if task == "A_not_B":
                vals = [100 * float(r["Test Accuracy"]) for r in rr if r.get("Test Accuracy", "") != ""]
            else:
                vals = [float(r["Test % Correct"]) for r in rr if r.get("Test % Correct", "") != ""]
            if not vals:
                continue
            out.append({
                "scientific_name": species,
                "source_species_label": label,
                "task": task,
                "n": len(vals),
                "mean_percent": sum(vals) / len(vals),
                "sd_percent": statistics.stdev(vals) if len(vals) > 1 else 0,
                "source_scope": scope,
            })

    fields = ["scientific_name","source_species_label","task","n","mean_percent","sd_percent","source_scope"]
    path = base / "data" / "maclean_self_control_v0.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(out)
    print(f"rows={len(out)} species={len(set(r['scientific_name'] for r in out))} output={path}")

if __name__ == "__main__":
    main()
