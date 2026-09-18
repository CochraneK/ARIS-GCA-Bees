"""Build fixed deep-coding search manifest for ARIS4C008 Tier-1 taxa.

The manifest standardizes first-pass evidence retrieval so famous taxa and
ordinary controls receive the same module/outcome search families.

It generates A-F and O1-O7 queries for all 50 Tier-1 additions, preserves
OpenTree-resolved synonym names as alternate exact-name queries, and marks
already-seeded A-F cells without removing them from later negative searches.
"""
from __future__ import annotations
import csv
from collections import defaultdict
from pathlib import Path

MODULE_TERMS={
"A": '"problem solving" OR innovation OR "behavioral flexibility" OR "behavioural flexibility" OR "reversal learning" OR detour OR planning OR "means-end" OR causal',
"B": '"social learning" OR imitation OR emulation OR teaching OR transmission OR tradition OR cultural',
"C": '"vocal learning" OR communication OR signalling OR signaling OR referential OR combinatorial OR compositional OR "turn-taking" OR audience',
"D": '"tool use" OR "tool manufacture" OR manipulation OR manipulatory OR construction OR "object modification" OR transport',
"E": 'artifact OR artefact OR construction OR nest OR dam OR cache OR trail OR bower OR "environmental modification" OR externalization OR externalisation',
"F": 'cooperation OR cooperative OR "social tolerance" OR "division of labor" OR "division of labour" OR "social network" OR "group decision" OR "fission-fusion" OR alloparental',
}
OUTCOME_TERMS={
"O1": 'innovation OR "novel problem" OR "problem solving" OR transfer OR detour OR planning OR "means-end" OR reversal',
"O2": 'tradition OR cultural OR culture OR "socially transmitted" OR "social transmission" OR dialect',
"O3": '"cumulative culture" OR cumulative OR "transmission chain" OR "successive improvement" OR "ratchet" OR "naive individuals" OR "independent innovation"',
"O4": '"cultural repertoire" OR "behavioural repertoire" OR "behavioral repertoire" OR "cultural variants" OR traditions',
"O5": 'recombination OR specialization OR specialisation OR "division of labor" OR "division of labour" OR "distributed knowledge" OR "network memory" OR "cross-group"',
"O6": 'artifact OR artefact OR construction OR cache OR trail OR nest OR dam OR bower OR "persistent structure" OR "environmental modification"',
"O7": '"cumulative culture" OR "open-ended" OR "open ended" OR "cultural evolution" OR "cumulative technological" OR "cumulative improvement"',
}
NEGATIVE_TERMS='"failed" OR "failure" OR "chance level" OR "no evidence" OR "did not" OR "unable" OR "not learn" OR "control group"'

def qname(name):
    return '"' + name.replace('"','') + '"'

def main():
    base=Path(__file__).resolve().parents[1]
    queue=list(csv.DictReader(open(base/"data"/"deep_coding_queue_v0.csv",encoding="utf-8-sig")))
    tax={r["query_name"]:r for r in csv.DictReader(open(base/"data"/"screening_pool_taxonomy_v0.csv",encoding="utf-8-sig"))}
    seed=list(csv.DictReader(open(base/"data"/"theory_candidate_evidence_seed_v0.csv",encoding="utf-8-sig")))
    seeded=defaultdict(set)
    for r in seed:seeded[r["scientific_name"]].add(r["module_id"])

    out=[]
    for row in queue:
        sp=row["scientific_name"]
        resolved=(tax.get(sp,{}) or {}).get("resolved_name","")
        aliases=[sp]
        if resolved and resolved!=sp:aliases.append(resolved)
        for target,terms in list(MODULE_TERMS.items())+list(OUTCOME_TERMS.items()):
            kind="module" if target in MODULE_TERMS else "outcome"
            primary=f'{qname(sp)} AND ({terms})'
            alt=f'{qname(resolved)} AND ({terms})' if resolved and resolved!=sp else ""
            neg=f'{qname(sp)} AND ({terms}) AND ({NEGATIVE_TERMS})'
            out.append({
              "tier1_rank":row["tier1_rank"],"scientific_name":sp,"pool_role":row["pool_role"],
              "target_id":target,"target_kind":kind,
              "already_seeded":"yes" if target in seeded[sp] else "no",
              "primary_query":primary,"alternate_taxonomy_query":alt,
              "negative_evidence_query":neg,
              "search_status":"pending","screening_status":"pending",
            })
    fields=list(out[0])
    with open(base/"data"/"deep_search_manifest_v0.csv","w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(out)
    print("rows",len(out),"taxa",len(queue),"targets_per_taxon",len(MODULE_TERMS)+len(OUTCOME_TERMS))
    print("seeded_module_cells",sum(r["already_seeded"]=="yes" for r in out))

if __name__=="__main__":
    main()
