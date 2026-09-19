# IDENTITY SECOND-REVIEW HANDOFF — ARIS4C004

## Role

You are an **independent identity reviewer** for ARIS4C004.

Your task is narrow:

> Independently determine whether each selected historical person is correctly mapped to the relevant OpenAlex Author ID(s), or whether the evidence instead supports collision, no usable graph identity, or identity error.

Do **not** evaluate mental health, scientific importance, network impact, CPE, or whether inclusion would help the study.

## Files to use

Primary assignment:

`data/derived/identity_second_review_blind_assignment.csv`

It contains exactly **40 frozen review cases** and intentionally omits first-review verdicts.

Protocol:

`process/IDENTITY_SECOND_REVIEW_PROTOCOL.md`

Candidate frame metadata may be read from:

`data/derived/science_candidates_frozen.csv`

FORD/domain metadata may be read from:

`data/derived/ford_domains_frozen.csv`

### Do not open before submitting independent judgments

Do **not** inspect:

- `data/derived/identity_decisions_100.csv`
- `data/derived/identity_second_review_selection.csv`
- first-review notes/verdicts
- mental-health/exposure files
- CPE/network-removal outputs

until all 40 independent judgments are locked.

## Evidence you may retrieve

For each person you may independently use public evidence such as:

- Wikidata / VIAF / ISNI / GND / LoC authority information;
- OpenAlex Author profiles and works;
- ORCID where historically plausible;
- university, academy, museum, government, professional-society or archival biographies;
- bibliographies / catalogues / authoritative obituaries;
- titles, publication dates, institutions, coauthors and fields/topics.

Prefer primary/authority/bibliographic evidence over unsourced biography pages.

## Allowed second-review states

Use exactly one:

- `VERIFIED_SINGLE`
- `VERIFIED_CLUSTER`
- `AMBIGUOUS_COLLISION`
- `NO_GRAPH_RECORD`
- `EXCLUDED_IDENTITY_ERROR`

For VERIFIED states you must supply the exact accepted OpenAlex Author ID set.

### VERIFIED_SINGLE

Use only when one OpenAlex Author ID can be defensibly mapped to the historical person.

### VERIFIED_CLUSTER

Use when multiple OpenAlex Author IDs are required for the same historical person.

Do not merge fragments merely because names match.

### AMBIGUOUS_COLLISION

Use when candidate OpenAlex records cannot be separated from namesakes or incompatible identities with adequate confidence.

### NO_GRAPH_RECORD

Use when the historical person is identifiable but no adequate OpenAlex Author mapping is supported.

### EXCLUDED_IDENTITY_ERROR

Use when the apparent candidate graph evidence demonstrably refers to a different person rather than the target identity.

## Minimum reasoning standard

For every VERIFIED judgment, check at least:

1. name/alias compatibility;
2. birth/death/career chronology;
3. occupation/field compatibility;
4. at least one representative work or bibliographic anchor;
5. obvious institution/coauthor consistency where available;
6. strong identifier conflict, especially ORCID.

For clusters, inspect every included Author ID.

For collisions, record the concrete incompatible evidence.

## Blinding requirement

You must not use or infer mental-health information.

Set:

`mh_blinded_at_second_review=true`

for every completed row.

## Output

Return the same 40 rows and columns from:

`identity_second_review_blind_assignment.csv`

Populate:

- `second_review_status`
- `second_review_openalex_ids`
- `second_reviewer`
- `mh_blinded_at_second_review`
- `second_review_date`
- `notes`

### OpenAlex ID format

Use semicolon-separated canonical IDs without URL prefixes, for example:

`A1234567890;A9876543210`

For non-VERIFIED states leave `second_review_openalex_ids` blank.

## Notes format

Keep notes concise but auditable.

Recommended structure:

`Evidence: <authority/bibliographic anchors>. OpenAlex: <why ID(s) fit or fail>. Conflicts: <none or concrete issue>. Sources: <source names/URLs or identifiers>.`

## Independence rule

Do not seek agreement with a presumed first reviewer.

Your job is not to "confirm" the study's mapping. Your job is to produce an independent mapping.

## After all 40 rows

Return:

1. completed CSV;
2. short summary of any difficult cases;
3. no comparison with first review.

ARIS4C will compare the two reviews only after your judgments are frozen.

## Exact execution prompt

> Review every row in `papers/004-counterfactual-cost-of-exclusion/data/derived/identity_second_review_blind_assignment.csv` independently under `process/IDENTITY_SECOND_REVIEW_PROTOCOL.md` and this handoff. Do not inspect `identity_decisions_100.csv` or any mental-health/CPE results. Use public authority, bibliographic, OpenAlex and institutional evidence. Fill all 40 rows with one allowed identity state, exact OpenAlex Author IDs for VERIFIED states, reviewer/date/blinding fields, and auditable evidence notes. Preserve person_id/name/birth/death exactly. Return a complete CSV; do not leave unresolved blanks merely because a case is difficult—use AMBIGUOUS_COLLISION or NO_GRAPH_RECORD when evidence cannot support a positive mapping.
