# RETRIEVAL V0.1 AUDIT — ARIS4C012

Updated: 2026-09-18

## Result

The first reproducible OpenAlex + Crossref retrieval completed successfully and produced:

- 36 provider/query requests;
- 180 selected candidate records;
- raw JSON for every request;
- SHA-256 provenance for raw responses and the candidate CSV.

This establishes that the retrieval pipeline is executable and auditable.

It does **not** pass the relevance portion of Gate R.

## Failure discovered

Broad bibliographic search terms generated systematic lexical/semantic contamination before human screening.

Concrete examples in the frozen v0.1 snapshot include:

- an `autonomy paradox flexibility constant connectivity` query retrieving neuroimaging papers about **dynamic functional connectivity**;
- a `formal choice effective autonomy dependence` query retrieving papers about **cardiovascular autonomic neuropathy**;
- a `safe development paradox protection increased risk` query retrieving unrelated cardiovascular clinical guidelines;
- a `Goodhart law metric target validity` Crossref query retrieving biographical/legal records containing the surname **Goodhart** rather than Goodhart's law;
- Crossref returning peer-review records, datasets, reference entries, and components that are unsuitable as primary screening units.

These are retrieval-quality failures, not OCI-negative findings.

## Decision

Freeze v0.1 unchanged as a failed-but-informative retrieval snapshot.

Amend the protocol to v0.2 **before any full evidence-map screening** by adding only outcome-independent relevance controls:

1. provider-specific scholarly record-type allow-lists;
2. prespecified title anchor groups tied to each search family;
3. explicit rejection logs showing which records fail type or topical gates;
4. larger per-query retrieval depth before deterministic topical filtering;
5. versioned output directories so no historical retrieval is overwritten.

The amendment does not use whether a record supports OCI. It only asks whether the bibliographic record is topically about the prespecified search family.

## Integrity rule

v0.1 remains in `data/retrieval_v0/` permanently.

No record is deleted from that snapshot, and no v0.1 results are silently relabeled as v0.2.
