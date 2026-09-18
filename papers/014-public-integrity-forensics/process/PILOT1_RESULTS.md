# Pilot 1A results — UK identifier-first source feasibility

Date: 2026-09-18  
Pilot ID: `014-UK-P1A-v0`  
Status: **frozen source collection complete**

## Frozen window

- Start: `2026-09-01T00:00:00Z`
- End: `2026-09-17T23:59:59Z`
- Find a Tender: award-stage OCDS releases, cap 100
- Contracts Finder: award-stage OCDS releases, cap 100
- Join policy: exact/official identifiers first; name-only joins disabled
- Companies House live enrichment: not included in this collection

The window and collection parameters are committed in `data/pilot1_uk_config.json`.

## Reproducible collection artifact

GitHub Actions run: **35305663110**  
Artifact: `aris4c014-pilot1-uk-p1a-v0`  
Artifact ID: **10531344179**  
Artifact digest: `sha256:400d7843872a75271ba13d7da8df38d0d4af0fa886962c56289e67c16b982473`  
Head SHA: `75262ffcce944ecbe233650b1004ab939ad298c2`

The artifact contains the raw official release packages plus a manifest with per-release SHA-256 digests and normalized source-coverage summaries. It is a bounded feasibility artifact, not a corruption dataset.

## Source coverage results

| Source | Releases | Award cases | Direct GB-COH cases | Direct joinability | Competition-covered cases |
|---|---:|---:|---:|---:|---:|
| UK Find a Tender | 100 | 119 | 32 | 26.9% | 0 |
| UK Contracts Finder | 100 | 104 | 57 | 54.8% | 0 |
| **Raw total** | **200** | **223** | **89** | not pooled as population estimate | **0** |

Important: the raw total does **not** de-duplicate possible overlap across the two procurement services. The percentages are descriptive of this frozen bounded collection only and are not population estimates.

## What this establishes

1. A real UK identifier-first procurement sample can be assembled without company-name matching.
2. At least 89 award cases in the frozen collection expose a supplier identifier directly usable as a Companies House join candidate.
3. Find a Tender and Contracts Finder are useful for award/company identity coverage in this pilot.
4. `numberOfTenderers` was not available in any of the 223 normalized award cases. Therefore the current single-bidder/competition detector family remains **ABSTAIN** for this collection.
5. Missing competition data are treated as missing source coverage, not evidence that competition was adequate or inadequate.
6. No automated corruption inference is produced by the collection.

## Pre-freeze live engineering observations

Before freezing Pilot 1A, three live engineering smokes were used to validate adapters:

- USAspending smoke: run `35304795418`
- Find a Tender joinability smoke: run `35305146659`
- Find a Tender lifecycle-record smoke: run `35305254618`
- Contracts Finder coverage smoke: final successful run `35305502362`

The FTS joinability smoke found 21 direct `GB-COH` award cases among 58 normalized award cases in a recent bounded sample. The lifecycle smoke then checked eight identifier-joinable OCIDs (11 award cases) and still found no bidder-count coverage. Contracts Finder's final bounded engineering smoke found 25 direct `GB-COH` cases among 50 award cases, also with zero bidder-count coverage.

These smokes informed the frozen protocol but are not combined with the Pilot 1A frozen results.

## Current interpretation

Pilot 1A supports proceeding to authenticated Companies House enrichment for the direct company-identifier subset.

The next empirical stage should prioritize:

- incorporation date;
- PSC / beneficial-control records;
- temporal validity of control relationships;
- deterministic company-age/award timing checks;
- ownership graph construction.

Competition/bidder-count checks should remain unavailable unless a source with actual competition-process coverage is added.

## Boundaries

This result does not identify corrupt suppliers, public officials, contracting authorities, or countries. It measures source coverage and cross-source joinability.

No company, person, or authority should be ranked by "corruption risk" from these coverage results.
