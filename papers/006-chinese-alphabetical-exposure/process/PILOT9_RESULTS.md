# ARIS4C006 · Pilot 9 — OpenAlex author-ID canonicalization

Last updated: 2026-09-18

## Verdict

**Naive raw-ID mismatch is fully repaired by canonical OpenAlex author resolution in this deterministic validation sample.**

GitHub Actions run: `35298686061`  
Artifact: `aris4c006-identity-canonicalization-pilot`

Pilot 7 found 61/977 (6.24%) ORCID-verifiable authorships where the OpenAlex author ID embedded in a work did not equal the current OpenAlex author returned by direct ORCID lookup.

Pilot 9 re-resolved every embedded work author ID through the current OpenAlex author endpoint before comparison.

## Results

- resolved ORCID-verifiable checks: **977**
- raw embedded-ID mismatches: **61**
- fixed by canonical author resolution: **61 / 61**
- unresolved conflicts: **0**
- embedded-ID lookup failures: **0**
- residual conflict rate: **0%**

Every raw mismatch in this sample was therefore consistent with an outdated/non-canonical embedded author identifier rather than a remaining ORCID-to-person contradiction.

## Frozen longitudinal join rule

For every authorship used in author-level trajectories:

1. retain the original embedded OpenAlex author ID for provenance;
2. resolve the embedded ID through the current OpenAlex author endpoint;
3. use the returned canonical OpenAlex author ID as the person-level join key;
4. if ORCID exists, require consistency with the canonical author record;
5. never merge people using raw-name similarity alone.

## Interpretation boundary

This result fixes a concrete engineering problem. It does **not** establish perfect OpenAlex entity resolution for authors lacking ORCID.

Residual false merges/splits among common Chinese names remain a validity threat and are handled by:

- ORCID-linked subset;
- uncommon-name subset;
- surname-frequency strata;
- implausible publication/affiliation diagnostics;
- coauthor/institution continuity diagnostics;
- exclusion of high identity-risk records;
- comparison of effect estimates across the sensitivity ladder.

## Gate consequence

**Canonical author-ID engineering: PASS.**

Person-level longitudinal analysis may enter the research-design stage, but confirmatory career outcomes remain locked until the full preregistration and identity-risk thresholds are frozen.
