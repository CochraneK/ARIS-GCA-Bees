# PILOT RESULTS — ARIS4C004

Last updated: 2026-09-18

This file is the canonical record of **pre-exposure science-pilot results**. No mental-health evidence was used to select or resolve candidates in these runs.

## Pilot purpose

Before coding any mental-health exposure, test whether a mental-health-independent historical science candidate frame can be linked to a sufficiently reproducible scholarly network.

The pilot is deliberately staged:

1. candidate-frame construction;
2. identity-resolution leads;
3. OpenAlex author/work observability;
4. author-fragment / name-collision review;
5. person-level identity validation and cluster assembly;
6. only after a network analytic frame is frozen: mental-health evidence coding.

## Candidate-frame result

Source: Laouenan et al. cross-verified notable-people dataset, verified mirror SHA-256:

`fe44aa6f97cf9f6c12d040137f92a9f4d0fd1f50e28f7f5d80eeae29b487828d`

Eligibility filter produced **108,626 Discovery/Science candidates** before pilot sampling.

The pilot sampled **100 candidates** with fixed seed `20260918`, balanced across 20 birth-cohort × visibility strata: 5 candidates per stratum.

### Sample composition

- Europe: 68
- America: 22
- Asia: 7
- Africa: 1
- missing region: 2
- Academia: 92
- Explorer/Inventor/Developer: 8

Interpretation: deterministic stratification by cohort × visibility worked, but the source frame remains heavily Europe-weighted. This is a property to measure and potentially re-stratify before exposure coding, not evidence that the historical contributor population was actually distributed this way.

## Identifier-lead result

For the 100 frozen candidates:

- Wikidata QID: 100/100
- ORCID lead found through Wikidata: 1/100
- OpenAlex author-ID lead found through Wikidata: 0/100

Conclusion: **Wikidata external identifiers are insufficient as the primary historical person → OpenAlex bridge.** The project must solve entity resolution rather than rely on identifier joins.

## OpenAlex pilot evolution

### Pilot v1 — identifier-only

The initial resolver required an existing OpenAlex ID or ORCID.

Result on first 30 candidates:

- resolved: 0/30
- resolution rate: 0%

Interpretation: design failure of the resolver, not evidence that OpenAlex lacks historical records.

Corrective action: add conservative name search plus lifetime/publication plausibility scoring while preserving unresolved/ambiguous states.

### Pilot v2 — evidence-scored name resolution

GitHub Actions run: `35272905327`

First 30 frozen candidates:

- automatically accepted top records: 17/30 = **56.7%**
- ambiguous: 1/30
- unresolved: 12/30
- accepted candidates with at least one work in 1900–2000: 14/30 = **46.7%**
- works acquired: 306
- API key: none / keyless pilot

This demonstrated that OpenAlex contains usable records for a substantial subset, but audit inspection identified two major problems:

1. some source names were mojibaked by a global Latin-1 decode;
2. one historical person is often split across multiple OpenAlex Author IDs.

Examples found during audit included James S. Albus, Erika Greber, Ottomar Rosenbach, Fritz Strassmann, Hilario Hernández Gurruchaga, and others with multiple highly similar OpenAlex author records. These examples are identity-resolution diagnostics only; they have no mental-health role in the study.

### Encoding correction

A strict UTF-8 decode of the 250MB source mirror failed, showing that the file is not clean global UTF-8. The pipeline now:

1. decodes bytes losslessly as Latin-1;
2. performs **cell-level reversible UTF-8 mojibake repair** only where the Latin-1 text round-trips as UTF-8;
3. leaves genuine Latin-1 strings unchanged when repair is invalid.

Regression examples:

- `HernÃ¡ndez` → `Hernández`
- genuine `Föhl` remains `Föhl`

No `errors=ignore` decoding is used.

### Pilot v3 — repaired names

GitHub Actions run: `35273279428`

First 30 frozen candidates:

- automatically accepted top records: 19/30 = **63.3%**
- ambiguous: 1/30
- unresolved: 10/30
- accepted candidates with at least one work in 1900–2000: 15/30 = **50.0%**
- works acquired: 311
- resolver errors: 0

The encoding repair therefore improved apparent automatic resolution from 56.7% to 63.3% and observed-work coverage from 46.7% to 50.0% in this bounded pilot.

**Important:** these numbers are not final identity accuracy because OpenAlex fragmentation can make a high-scoring top hit incomplete or misleading.

### Pilot v4 — explicit author-fragment review

GitHub Actions run: `35273825936`

The same first 30 candidates were passed through an explicit fragmentation/name-collision review layer that considers all plausible search hits rather than silently selecting only the top-scoring Author ID.

Result:

- candidate records reviewed: **30**
- `possible_author_fragmentation`: **11/30 = 36.7%**
- `single_plausible_author_record`: **9/30 = 30.0%**
- `no_openalex_search_hit`: **9/30 = 30.0%**
- `name_collision_or_low_similarity`: **1/30 = 3.3%**
- apparent candidates with at least one plausible OpenAlex network lead: **20/30 = 66.7%**
- identity-verified candidates: **0/30 by design at this stage**

Interpretation:

1. **Author fragmentation is a first-order problem, not an edge case.** More than one-third of this bounded historical-science pilot has multiple plausible OpenAlex Author IDs requiring cluster review.
2. The earlier single-top-record work-coverage estimate of 50% understated apparent graph availability because fragmented records were being ignored. Once plausible fragments are retained for review, 20/30 candidates have at least one apparent network lead.
3. The 66.7% figure is **not identity-validated coverage**. It is a review-queue observability measure only.
4. Expanding immediately to 100 candidates without stabilizing cluster evidence would scale identity error faster than scientific information.

This run changed the immediate priority from sample expansion to person-level author-cluster validation.

## Identity-resolution correction: coverage ≠ precision

The original feasibility gate "95% of sampled candidates resolve" was too coarse. Two distinct quantities are now required.

### Candidate-frame network coverage

Question:

> What fraction of a mental-health-independent historical candidate frame has enough scholarly-network information to support the planned analysis?

This quantity can legitimately be below 95%, but missingness must be characterized by era, region, visibility, discipline, gender, and other available frame variables.

Current first-30 estimates:

- accepted single-top-record with >=1 acquired 1900–2000 work: **15/30 = 50.0%**;
- candidates with at least one plausible OpenAlex network lead after fragment review: **20/30 = 66.7%**.

Neither number is yet the final verified network coverage.

### Analytic-frame identity precision

Question:

> For people who enter the final network analytic frame, how certain are we that all included OpenAlex records belong to the intended historical person and that important fragments have not been omitted?

Target:

- **near-100% externally auditable identity decisions for the final analytic frame**;
- no automatic top-hit acceptance is considered final verification;
- multiple plausible OpenAlex IDs trigger cluster review rather than silent top-hit selection;
- conflicting ORCIDs or other strong identity evidence prohibit blind merging.

This precision gate is more important than maximizing raw candidate-frame coverage.

## Person-level OpenAlex identity protocol

`IDENTITY_CODEBOOK.md` now defines the target mapping as:

`historical person -> {one or more verified OpenAlex Author IDs}`

Allowed states include:

- `VERIFIED_SINGLE`
- `VERIFIED_CLUSTER`
- `PROVISIONAL_SINGLE`
- `PROVISIONAL_CLUSTER`
- `AMBIGUOUS_COLLISION`
- `NO_GRAPH_RECORD`
- `EXCLUDED_IDENTITY_ERROR`

Only `VERIFIED_SINGLE` and `VERIFIED_CLUSTER` can enter the confirmatory network analytic frame.

Identity evidence must go beyond bare name equality unless a strong external identifier is available. Candidate signals include known works, institutions, coauthors, field/topic, career timing, ORCID/authority identifiers, duplicate works and other fragment-linking evidence.

A dedicated `validate_identity.py` enforces these invariants before confirmatory network inclusion.

## Current science feasibility interpretation

**Continue, but do not expand exposure coding yet.** The science route has passed the minimal "data exist and can be programmatically connected" test, but has **not** passed the final identity/network analytic-frame gate.

The major bottleneck has shifted from general data availability to:

1. historical person ↔ OpenAlex author-cluster validation;
2. selection bias induced by OpenAlex observability;
3. network sufficiency after verified clusters are assembled;
4. only then, Tier-A/Tier-B mental-health evidence yield.

## Revised order of operations

1. Build fragment-cluster evidence for every plausible OpenAlex ID in the first-30 queue.
2. Use `IDENTITY_CODEBOOK.md` to manually/externally validate the first 30, especially all 11 fragmentation cases.
3. Estimate automated false-positive and missed-fragment rates.
4. Estimate verified coverage and fragmentation by cohort/visibility/region.
5. Expand identity pilot beyond 30 only after precision rules are stable.
6. Freeze a **network-observable analytic frame without using mental-health information**.
7. Begin exposure coding under `EXPOSURE_CODEBOOK.md`.
8. Measure Tier-A/Tier-B yield.
9. Decide final sample expansion and simulation-based precision target.

No mental-health outcome or CPE comparison should be run before step 6–7 is frozen.

## Pilot v5 — lifetime-aware fragment evidence and conservative guard

The fragment audit was upgraded from raw overlap counting to candidate-lifetime-aware evidence.

For 11 fragmentation candidates:

- candidate Author IDs fetched: **44**
- pairwise fragment comparisons: **82**
- Author profiles with >50% works outside the candidate-specific plausible career window: **17/44 = 38.6%**

Raw lifetime-aware pair labels:

- support: 1
- conflict: 45
- needs review: 36

The remaining raw support was a false-positive-like case driven by a small number of shared contextual links. A separate conservative evidence guard was therefore frozen. It never promotes a pair; it can only retain or downgrade support.

Guarded labels:

- **support: 0**
- **conflict: 45**
- **needs review: 37**
- weak contextual support pairs downgraded: 1

This means no fragment pair in the first 30 is allowed to auto-merge solely from OpenAlex overlap evidence.

## Pilot30 identity adjudication freeze

A unified identity packet combined:

- candidate-frame metadata;
- lifetime-aware OpenAlex representative works;
- fragment evidence;
- Wikidata occupation/field/employer/education data;
- VIAF/ISNI/GND/LoC authority identifiers where available;
- external bibliographic/official-source checks for difficult cases.

Wikidata authority retrieval for the first 30 yielded:

- entities found: 30/30
- occupation/field evidence: 28/30
- employer/education evidence: 21/30
- at least one external authority ID: 24/30
- mental-health fields requested: **false**

After evidence review, the first 30 now have **zero provisional identity states**:

- VERIFIED_SINGLE: **11**
- VERIFIED_CLUSTER: **7**
- NO_GRAPH_RECORD: **9**
- AMBIGUOUS_COLLISION: **2**
- EXCLUDED_IDENTITY_ERROR: **1**

Thus **18/30 = 60%** have a verified person ↔ OpenAlex mapping after first review.

Currently **9/30 = 30%** satisfy the present identity + minimum-work release rule and are marked network-observable:

- Mary Alice McWhinnie
- Hilario Hernández Gurruchaga
- Hannah Gavron
- Dan Laksov
- James S. Albus
- Ottomar Rosenbach
- Willy Oelsen
- Carl Föhl
- Friedrich Hoeth

The other verified identities remain held for one of three reasons:

1. fewer than five usable works under the pilot gate;
2. OpenAlex represents modern/posthumous editions rather than historical production;
3. work-level duplicate/mixed-author contamination remains after identity verification.

### Illustrative failure modes discovered before exposure coding

- **John I. Yellott:** one OpenAlex author record mixes solar-engineering work with a large vision/perception literature; final state is collision rather than forced match.
- **Fred Casey:** apparent OpenAlex hits were Maine alien-registration/namesake records, not the intended British socialist educationalist; excluded identity error.
- **Fritz Strassmann:** true nuclear-chemistry fragments coexist with medical/forensic namesakes and contamination inside a large author record; identity can be verified but work-level filtering is still required.
- **Ahmad Kasravi:** OpenAlex records match real Kasravi titles but largely encode modern posthumous editions, so identity is verified while historical network observability remains false.

These examples show why identity accuracy and network usability are separate quantities.

## Data-integrity corrections converted into permanent gates

Two repository/data failures were caught during adjudication and converted into CI invariants:

1. An early manually assembled decision table contained incorrect person_id/QID transcriptions for many rows. The table was repaired from the canonical frozen frame, and `validate_identity.py --candidate-frame` now requires exact person_id/name/birth/death agreement.
2. Free-text notes containing commas were initially serialized without CSV quoting. The table was rewritten as valid quoted CSV and the validator now rejects malformed rows with unexpected extra fields.

No downstream mental-health analysis had begun when either issue was detected.

## Next empirical gate — verified-person work corpus

Identity resolution is no longer the only blocker. The next stage rebuilds all works for accepted OpenAlex IDs at the **person** level and will:

1. preserve source Author-ID provenance;
2. apply candidate-specific temporal flags;
3. deduplicate repeated DOI or normalized-title/year records across fragments;
4. separate out-of-window works;
5. flag mixed-author contamination for manual work review;
6. compute clean usable-work counts;
7. update network observability only after explicit review.

Mechanical cleanup is not allowed to automatically release a previously held person into the confirmatory network frame.

Only after this work-level gate is characterized should the project decide whether to scale identity resolution from the first 30 to all 100 frozen candidates. Mental-health exposure coding remains locked.

