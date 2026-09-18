"""Build a module-specific OpenAlex research-effort proxy for ARIS4C008.

This is a nuisance/bias proxy, never an animal-ability score.

Search window: 1990-01-01 through 2026-09-18.
Queries require the exact scientific-name phrase and add broad module terms.
Counts overlap across modules and include title/abstract/fulltext matches.
"""
from __future__ import annotations
import argparse, csv, json, os, time, urllib.parse, urllib.request
from pathlib import Path

MODULES = {
    "all_taxon": None,
    "behavior_general": "(behavior OR behaviour OR cognition OR cognitive OR learning OR social)",
    "cognition": '(cognition OR cognitive OR intelligence OR "problem solving" OR innovation)',
    "social_transmission": '("social learning" OR imitation OR teaching OR culture OR cultural OR tradition)',
    "manipulation": '("tool use" OR tool OR manipulation OR construction OR object)',
    "communication": "(communication OR vocal OR vocalization OR signal OR signaling OR language)",
}
DATE_FILTER = "from_publication_date:1990-01-01,to_publication_date:2026-09-18"
BASE = "https://api.openalex.org/works"

def count_query(species: str, terms: str | None, api_key: str | None) -> int:
    q = f'"{species}"' if terms is None else f'"{species}" AND {terms}'
    params = {"search": q, "filter": DATE_FILTER, "per_page": 1, "select": "id"}
    if api_key:
        params["api_key"] = api_key
    url = BASE + "?" + urllib.parse.urlencode(params)
    last = None
    for attempt in range(8):
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": "ARIS4C008/1.0 research-effort proxy"}
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                return int(json.loads(resp.read().decode())["meta"]["count"])
        except Exception as exc:
            last = exc
            time.sleep(1.0 + attempt * 1.5)
    raise RuntimeError(f"OpenAlex failed for {species}: {terms}: {last}")

def main():
    base = Path(__file__).resolve().parents[1]
    ap = argparse.ArgumentParser()
    ap.add_argument("--panel", default=str(base / "data" / "pilot_taxa_v2.csv"))
    ap.add_argument("--output", default=str(base / "data" / "openalex_research_effort_v0.csv"))
    ap.add_argument("--sleep", type=float, default=0.35)
    args = ap.parse_args()

    panel = list(csv.DictReader(open(args.panel, encoding="utf-8-sig")))
    api_key = os.getenv("OPENALEX_API_KEY")
    out = []
    for p in panel:
        species = p["scientific_name"].strip()
        row = {"scientific_name": species}
        for module, terms in MODULES.items():
            row[module] = count_query(species, terms, api_key)
            time.sleep(args.sleep)
        out.append(row)

    fields = ["scientific_name"] + list(MODULES)
    with open(args.output, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader(); w.writerows(out)
    print(f"species={len(out)} queries={len(out)*len(MODULES)} output={args.output}")

if __name__ == "__main__":
    main()
