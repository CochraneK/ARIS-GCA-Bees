"""Resolve ARIS4C008 species through Open Tree of Life and build an induced topology.

Outputs:
- opentree_taxonomy_v2.csv
- opentree_v2_induced_subtree.tre
- opentree_v2_metadata.json

Important: OpenTree's synthetic induced subtree is a topology, not a calibrated
chronogram. Do not use it as a dated tree without an explicit branch-length
strategy.
"""
from __future__ import annotations
import argparse, csv, json, urllib.request
from pathlib import Path

TNRS = "https://api.opentreeoflife.org/v3/tnrs/match_names"
SUBTREE = "https://api.opentreeoflife.org/v3/tree_of_life/induced_subtree"

def post(url: str, payload: dict) -> dict:
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        url, data=data, headers={"Content-Type": "application/json"}, method="POST"
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode())

def main():
    base = Path(__file__).resolve().parents[1]
    ap = argparse.ArgumentParser()
    ap.add_argument("--panel", default=str(base / "data" / "pilot_taxa_v2.csv"))
    ap.add_argument("--mapping", default=str(base / "data" / "opentree_taxonomy_v2.csv"))
    ap.add_argument("--tree", default=str(base / "data" / "opentree_v2_induced_subtree.tre"))
    ap.add_argument("--metadata", default=str(base / "data" / "opentree_v2_metadata.json"))
    args = ap.parse_args()

    rows = list(csv.DictReader(open(args.panel, encoding="utf-8-sig")))
    names = [r["scientific_name"].strip() for r in rows]

    tn = post(TNRS, {
        "names": names,
        "context_name": "Animals",
        "do_approximate_matching": False,
    })

    unmatched = tn.get("unmatched_names", [])
    if unmatched:
        raise RuntimeError(f"Unmatched names: {unmatched}")

    mapping, ott_ids = [], []
    for q in tn["results"]:
        matches = q.get("matches", [])
        if len(matches) != 1:
            raise RuntimeError(f"Expected one exact match for {q['name']}, got {len(matches)}")
        m = matches[0]
        tax = m["taxon"]
        if m.get("is_approximate_match"):
            raise RuntimeError(f"Approximate match not allowed: {q['name']} -> {tax.get('name')}")
        ott_ids.append(tax["ott_id"])
        mapping.append({
            "query_name": q["name"],
            "matched_name": tax["name"],
            "ott_id": tax["ott_id"],
            "rank": tax.get("rank", ""),
            "is_synonym": bool(m.get("is_synonym", False)),
            "score": m.get("score", ""),
            "is_approximate_match": bool(m.get("is_approximate_match", False)),
        })

    with open(args.mapping, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(mapping[0]))
        w.writeheader(); w.writerows(mapping)

    sub = post(SUBTREE, {"ott_ids": ott_ids, "label_format": "name_and_id"})
    Path(args.tree).write_text(sub["newick"].rstrip() + "\n", encoding="utf-8")

    meta = {
        "n_queries": len(names),
        "n_unmatched": len(unmatched),
        "n_synonyms": sum(x["is_synonym"] for x in mapping),
        "taxonomy": tn.get("taxonomy"),
        "n_supporting_studies": len(sub.get("supporting_studies", [])),
        "supporting_studies": sub.get("supporting_studies", []),
        "tree_type": "OpenTree synthetic induced topology; no calibrated branch lengths",
    }
    Path(args.metadata).write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in meta.items() if k != "supporting_studies"}, indent=2))

if __name__ == "__main__":
    main()
