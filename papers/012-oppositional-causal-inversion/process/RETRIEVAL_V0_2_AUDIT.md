# RETRIEVAL V0.2 AUDIT — ARIS4C012

Updated: 2026-09-18

## Verdict

**Gate R1 — executable / provenance-safe retrieval: PASS.**  
**Gate R2 — gross topical relevance for Pilot retrieval: PASS.**  
**Gate R3 — systematic-review saturation / recall: OPEN.**

The v0.2 search is suitable for generating a reproducible Pilot screening frame. It is **not** yet a claim that the full OCI literature has been saturated.

## Execution result

The GitHub Actions workflow completed successfully and persisted an immutable versioned snapshot at:

`data/retrieval_v0_2_0/`

The snapshot contains:

- 36 OpenAlex/Crossref requests;
- 1,800 raw bibliographic hits before topical/type gates;
- 1,375 transparent pre-screen rejections;
- 165 deterministic candidate records after topical/type gates and deduplicated stratum selection;
- all raw JSON responses;
- candidate and rejection CSV hashes;
- request URLs, retrieval time, and source-specific acceptance counts.

## Stratum coverage

| Stratum | Selected | OpenAlex | Crossref |
|---|---:|---:|---:|
| conflict/security | 30 | 16 | 14 |
| autonomy/choice | 30 | 14 | 16 |
| information/attention | 30 | 16 | 14 |
| backfire/iatrogenic | 30 | 12 | 18 |
| economic/network rebound | 30 | 14 | 16 |
| organization/measurement | 15 | 4 | 11 |
| **Total** | **165** | **76** | **89** |

No stratum depends on a single provider.

## v0.1 failures corrected

The v0.2 title/type gates successfully prevent the main v0.1 failures from automatically entering the candidate frame:

- generic dynamic functional-connectivity neuroimaging is no longer admitted merely because a query contains “connectivity”;
- cardiovascular autonomic-neuropathy papers do not satisfy the required autonomy + dependence/delegation anchor structure;
- biographical records containing the surname Goodhart fail the metric/target/proxy anchor and/or scholarly record-type gate;
- peer-review records, datasets, components and reference entries are excluded as primary screening units;
- unrelated high-citation “safe” / “risk” papers fail the safe-development/flood-protection anchors.

The original v0.1 snapshot is preserved and was not rewritten.

## Residual noise is intentionally not eliminated algorithmically

Some v0.2 candidates remain ambiguous at title level. Examples include:

- generic optimization papers containing “less is more” or “heuristic”;
- political/educational uses of autonomy and delegation;
- broad medical iatrogenic-harm papers outside the initial psychological examples;
- broad organizational-paradox records that may later fail strict OCI coding.

These are not retrieval bugs. A high-sensitivity evidence map requires human/LLM screening to distinguish:
1. strict OCI candidates;
2. neighboring theories;
3. ordinary side effects;
4. rhetorical paradoxes;
5. topical but non-OCI records.

Further title filtering based on anticipated OCI-positive status would risk circularity and false recall claims.

## Important limitation

The 165 candidates are generated from a **Pilot search architecture**, not a database-complete systematic-review strategy. Search families, citation chasing, additional databases, historical terminology, and formal-model literatures must still be expanded before any claim of literature saturation.

Accordingly:

- reproducibility of retrieval is now solved for Pilot 0;
- broad-search recall remains an empirical review-method problem;
- the full protocol must report database coverage and search-date limitations.

## Gate consequence

The project no longer needs to block on engineering a reproducible candidate frame.

The remaining decisive validity gate is **independent construct coding (Gate B)**. Full evidence-map scaling should occur only after the functional-opposition and mechanism schema demonstrates adequate independent agreement.
