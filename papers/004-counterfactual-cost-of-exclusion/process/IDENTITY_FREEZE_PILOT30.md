# IDENTITY FREEZE — PILOT30 v1

Date: 2026-09-18  
Scope: first 30 candidates from the frozen, mental-health-independent science pilot frame  
Mental-health information used in identity review: **none**

## Status

The first 30 candidates now have **zero provisional identity states**.

| Final identity state | n |
|---|---:|
| VERIFIED_SINGLE | 11 |
| VERIFIED_CLUSTER | 7 |
| NO_GRAPH_RECORD | 9 |
| AMBIGUOUS_COLLISION | 2 |
| EXCLUDED_IDENTITY_ERROR | 1 |
| PROVISIONAL_* | **0** |
| Total | **30** |

Eighteen of 30 candidates (60%) have a verified mapping to at least one OpenAlex author record or author cluster. This is an **identity-resolution yield**, not an estimate of population coverage or OpenAlex recall.

Nine of 30 candidates (30%) are currently marked `network_observable=true` under the present pilot rule. The remaining verified identities are held out either because they have fewer than five usable works or because their OpenAlex records still require work-level decontamination/deduplication.

## Currently network-observable

- Mary Alice McWhinnie
- Hilario Hernández Gurruchaga
- Hannah Gavron
- Dan Laksov
- James S. Albus
- Ottomar Rosenbach
- Willy Oelsen
- Carl Föhl
- Friedrich Hoeth

## Verified identity but network not yet released

### Too few usable works under the current >=5-work pilot gate

- Otto Siebert
- Karl Erich Hupka
- Paul J. Torpey

### Correct identity but historical/time metadata is unsuitable

- Ahmad Kasravi — OpenAlex mainly represents modern posthumous editions rather than his 1915–1946 production.

### Work-level contamination / deduplication still required

- Karl-Franz Busch
- Erika Greber
- Joel Olson
- Anton Moortgat
- Fritz Strassmann

These people remain identity-verified but cannot enter confirmatory network analysis until a person-level work corpus is rebuilt from the accepted IDs and audited.

## Final non-verified outcomes

- 9 `NO_GRAPH_RECORD` cases: no adequate OpenAlex graph record under the frozen resolver protocol.
- 2 `AMBIGUOUS_COLLISION` cases, including John I. Yellott, whose apparent OpenAlex record mixes solar-engineering output with a large vision/perception literature.
- 1 `EXCLUDED_IDENTITY_ERROR`: Fred Casey, where OpenAlex leads were namesake/archival records inconsistent with the intended British socialist educationalist.

These cases are not rescued by lowering resolver thresholds.

## Important lessons from the pilot

1. **Historical person -> OpenAlex author is not a simple ID join.** Wikidata supplied QIDs for all 100 frozen candidates but only one ORCID and no usable OpenAlex author IDs in the first pipeline.
2. **Author fragmentation is common.** Eleven of the first 30 candidates triggered multi-record review.
3. **Temporal contamination is common.** Seventeen of 44 fragment profiles in the fragment audit had >50% of fetched works outside the candidate-specific plausible career window.
4. **Weak contextual overlap is unsafe.** Shared institution/coauthors alone produced false support for namesakes; guarded fragment evidence therefore requires stronger identity anchors or high proportional overlap.
5. **Identity and network usability are separate decisions.** A person can be correctly identified while their OpenAlex graph is unusable or requires work-level cleanup.
6. **Coverage must not be optimized by sacrificing precision.** No unresolved candidate is promoted merely to increase N.
7. **The candidate frame remains pre-exposure.** Mental-health evidence has not been used to select, drop, merge, or rescue anyone.

## Data-integrity safeguards now active

- `identity_decisions_pilot30.csv` is validated against the canonical frozen candidate frame.
- person_id, canonical name, birth year, and death year must match exactly.
- malformed CSV rows with unquoted extra fields fail validation.
- provisional/non-verified states cannot set `network_observable=true`.
- verified clusters require multiple OpenAlex IDs and no known conflicting ORCID.
- the identity decision table is now valid quoted CSV; free-text notes may contain commas without corrupting columns.

## What this freeze does **not** mean

This is a first-review pilot identity freeze, not an estimate of final identity precision. Independent second review has not yet been completed for every verified row. Before confirmatory analysis, a random/targeted audit of accepted identities and all difficult clusters should be independently checked.

## Next gate

Build a **verified-person work corpus**:

1. fetch all works for accepted OpenAlex IDs;
2. retain original raw provenance;
3. apply candidate-lifetime temporal flags;
4. deduplicate duplicated DOI/title records across fragments;
5. identify mixed-author contamination at work level;
6. compute clean usable-work counts;
7. update `network_observable` only after the clean corpus passes validation.

Only after this gate should the project decide whether to expand identity resolution from the first 30 to all 100 frozen candidates. Mental-health exposure coding remains locked until the pre-exposure network frame is stable.
