"""Build the 60-target pinned OEWN lexical calibration source pool.

This file deliberately emits SOURCE records only. It does not assign UCID
ontology axes or gold semantic responses.

Requires:
    pip install wn==1.1.1

The first run downloads the pinned Open English WordNet 2025 resource:
    oewn:2025
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

import wn


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DATA = ROOT / "data"
MANIFEST = DATA / "calibration60" / "selection_manifest.v0.json"
OUTPUT = DATA / "calibration60" / "oewn_source_pool.generated.json"


def ensure_oewn() -> wn.Wordnet:
    try:
        return wn.Wordnet("oewn:2025")
    except wn.Error:
        wn.download("oewn:2025")
        return wn.Wordnet("oewn:2025")


def select_diverse_senses(wordnet: wn.Wordnet, lemma: str, quota: int):
    senses = list(wordnet.senses(lemma, pos="n"))
    if len(senses) < quota:
        raise RuntimeError(
            f"{lemma!r} has only {len(senses)} noun senses in oewn:2025; "
            f"need {quota}. Refusing silent substitution."
        )

    enriched = []
    for sense in senses:
        synset = sense.synset()
        enriched.append((synset.lexfile() or "", synset.id, sense.id, sense, synset))
    enriched.sort(key=lambda x: (x[0], x[1], x[2]))

    by_lexfile = defaultdict(list)
    for item in enriched:
        by_lexfile[item[0]].append(item)

    selected = []
    # Round-robin across source lexfiles so one very dense lexfile does not
    # dominate a lemma's six calibration senses.
    while len(selected) < quota and by_lexfile:
        progressed = False
        for lexfile in sorted(list(by_lexfile)):
            bucket = by_lexfile[lexfile]
            if bucket and len(selected) < quota:
                selected.append(bucket.pop(0))
                progressed = True
            if not bucket:
                del by_lexfile[lexfile]
        if not progressed:
            break

    if len(selected) < quota:
        used = {(x[1], x[2]) for x in selected}
        for item in enriched:
            if (item[1], item[2]) not in used:
                selected.append(item)
                if len(selected) == quota:
                    break

    return selected


def main():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    wordnet = ensure_oewn()
    quota = manifest["senses_per_lemma"]
    records = []
    source_counts = {}

    for lemma in manifest["lemma_groups"]:
        all_senses = list(wordnet.senses(lemma, pos="n"))
        source_counts[lemma] = len(all_senses)
        selected = select_diverse_senses(wordnet, lemma, quota)

        for rank, (lexfile, synset_id, sense_id, sense, synset) in enumerate(selected, 1):
            definition = synset.definition() or ""
            if not definition:
                raise RuntimeError(f"Missing definition for {sense_id}")
            records.append(
                {
                    "source_record_id": f"oewn2025:{sense_id}",
                    "group_id": f"lemma:{lemma}",
                    "lemma": lemma,
                    "part_of_speech": "n",
                    "sense_id": sense_id,
                    "synset_id": synset_id,
                    "lexname": lexfile or None,
                    "definition": definition,
                    "examples": list(synset.examples()),
                    "ili": synset.ili,
                    "selection_rank": rank,
                    "source_release": "oewn:2025",
                    "provenance": {
                        "resource": "Open English WordNet 2025",
                        "license": "Princeton WordNet License + CC BY 4.0 for OEWN additions",
                        "builder": "build_oewn_calibration60.py",
                        "retrieved_by": "wn==1.1.1",
                    },
                }
            )

    if len(records) != 60:
        raise RuntimeError(f"Expected 60 records, produced {len(records)}")

    payload = {
        "dataset_id": manifest["dataset_id"],
        "evidence_class": "source_derived_unannotated",
        "source_release": "oewn:2025",
        "record_count": len(records),
        "group_count": len(manifest["lemma_groups"]),
        "source_noun_sense_counts": source_counts,
        "warning": (
            "Source identities/glosses are OEWN-derived. No UCID semantic label or "
            "query response in this file is adjudicated."
        ),
        "records": records,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print("PASS calibration60 build")
    print("records:", len(records))
    print("groups:", len(manifest["lemma_groups"]))
    print("source noun-sense counts:", json.dumps(source_counts, sort_keys=True))
    for lemma in manifest["lemma_groups"]:
        ids = [r["sense_id"] for r in records if r["lemma"] == lemma]
        print(f"{lemma}: " + " | ".join(ids))


if __name__ == "__main__":
    main()
