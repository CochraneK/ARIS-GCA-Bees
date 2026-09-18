# RETRIEVAL FRAME STRUCTURE AUDIT — ARIS4C012

Updated: 2026-09-18

## Scope

This audit evaluates the **structure** of the v0.2 reproducible retrieval frame. It does not label any record as OCI-positive or OCI-negative.

## Frame size

Total selected candidates: **165**

### By stratum

| Stratum | n |
|---|---:|
| conflict/security | 30 |
| autonomy/choice | 30 |
| information/attention | 30 |
| backfire/iatrogenic | 30 |
| economic/network rebound | 30 |
| organization/measurement | 15 |

### By provider

| Provider | n |
|---|---:|
| OpenAlex | 76 |
| Crossref | 89 |

No stratum is sourced from only one provider.

## Temporal structure

| Decade | n |
|---|---:|
| 1970s | 1 |
| 1980s | 2 |
| 1990s | 6 |
| 2000s | 20 |
| 2010s | 53 |
| 2020s | 83 |

The frame is strongly weighted toward recent literature. This is partly substantive and partly a retrieval/indexing artifact. Full evidence mapping must therefore include backward citation chasing and historical terminology before making prevalence claims.

## Record types

| Type | n |
|---|---:|
| article | 70 |
| journal-article | 38 |
| book-chapter | 25 |
| posted-content | 21 |
| report | 5 |
| book | 2 |
| proceedings-article | 2 |
| preprint | 2 |

161/165 records contain a DOI.

23/165 are preprint/posted-content records. These are useful for discovery but should be distinguished from peer-reviewed evidence in synthesis.

## Query-family imbalance

The stratum quotas conceal large within-stratum query imbalance.

### conflict/security
- intergroup/intragroup: 10
- rally/external threat: 10
- security dilemma/deterrence: 10

Balanced.

### autonomy/choice
- choice overload: 12
- autonomy/flexibility/connectivity: 11
- autonomy/dependence/delegation: 7

Moderately imbalanced.

### information/attention
- less-is-more/heuristics: 14
- rational inattention/ignorance/avoidance: 13
- public information/welfare/coordination: **3**

Strongly imbalanced.

### backfire/iatrogenic
- boomerang: 5
- iatrogenic: **20**
- generic intervention backfire: 5

Strongly imbalanced toward iatrogenic terminology.

### economic/network rebound
- Jevons/rebound: 12
- Braess/network: 11
- safe development: 7

Moderately balanced.

### organization/measurement
- capability-rigidity/organizational paradox: 9
- Goodhart/proxy failure: 4
- control/optimization paradox: **2**

Strongly underpowered and only 15 records total.

## Consequence

The 165-record frame is suitable as a **reproducible candidate universe for a Pilot-scale screen**, but it is not a balanced or saturated evidence-map sample.

A naive analysis of raw frequencies would overestimate families with:
- established standardized terminology;
- stronger bibliographic indexing;
- more recent publication volume;
- broader title-level lexical overlap.

## Full-map sampling rule

After Gate B construct validation passes:

1. screen the entire 165-record frame for schema performance;
2. report raw retrieval frequencies only as retrieval frequencies, not phenomenon prevalence;
3. run targeted expansion for underrepresented query families;
4. add backward/forward citation chasing from benchmark sources;
5. search historical terminology and seminal pre-digital sources;
6. preserve peer-reviewed vs preprint/posted-content status;
7. freeze a saturation log showing when each mechanism/query family stops yielding materially new OCI mechanism classes.

### Minimum family target before comparative frequency analysis

Before comparing mechanism-family proportions, seek at least **20 screened candidates per prespecified query family** where feasible.

This is a workflow target, not a power calculation.

## Priority expansion order

1. public information / welfare / coordination;
2. control / optimization / fragility paradoxes;
3. Goodhart / proxy failure;
4. generic intervention backfire beyond iatrogenic care;
5. autonomy / dependence / delegation;
6. safe-development and analogous protection-risk feedbacks.

## Key methodological rule

Retrieval abundance must never be interpreted as scientific prevalence without correcting for search vocabulary, database coverage, publication era, and family-specific indexing.

The purpose of the evidence map is first to test the **representation and taxonomy**, not to claim that one inversion mechanism is objectively more common in nature.
