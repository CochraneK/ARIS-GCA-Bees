# NETWORK FEASIBILITY — PILOT30

Date: 2026-09-18  
Scope: 13 network-observable people derived from the first 30 frozen science candidates  
Exposure status: **mental-health blind / not yet coded**

## Decision

**Citation-network feasibility passes for science-first expansion, with a preregistered citation-sparse stratum.**

The project should proceed to MH-blind identity/network expansion for the remaining frozen candidates. It should **not** yet begin mental-health exposure coding.

## Clean focal network

After identity verification, work-level adjudication and temporal cleanup:

- frozen pilot candidates: 30
- verified identities: 18/30
- network-observable identities: **13/30 = 43.3%**
- clean focal works: **693**
- build errors: **0**

Metadata coverage across clean focal works:

- topic metadata: **98.99%**
- external-coauthor metadata: **63.06%**
- unique external coauthors: **395**
- institution metadata: **48.05%**
- reference metadata: **44.59%**

The clean focal-work citation graph initially contained 28 time-reversed OpenAlex citation relations. These are now quarantined and excluded from the temporal graph.

After temporal filtering:

- valid internal clean citation edges: **638**
- within-person edges: **638**
- cross-person focal edges: **0**
- excluded time-reversed edges: **28**

Interpretation: the first 13 focal people do not form one meaningful common citation graph. This is expected because they span heterogeneous periods and subfields. Person-specific temporal ego networks are therefore the canonical network object; raw centrality in a pooled 13-person graph is not a valid primary comparison.

## Bounded downstream citation pilot

Pilot parameters were fixed before reading person-level downstream results:

- maximum anchors per person: 6
- deterministic anchors: earliest + temporal median + latest + highest-cited remaining
- downstream horizon: 20 years
- study end: 2026
- maximum citing works per anchor: 50
- citing-work acquisition: earliest first
- OpenAlex relation: works satisfying `cites:<anchor_work_id>`

Result:

- people: **13**
- anchors: **76**
- anchors with >=1 downstream citer: **52/76 = 68.4%**
- downstream citation edges: **897**
- unique downstream person-work pairs: **817**
- people with >=1 downstream work: **13/13**
- people with >=10 downstream works: **8/13**
- time-reversed downstream edges: **0**
- API errors: **0**

This passes the minimum feasibility question: every network-observable focal person has an observable temporally ordered downstream citation neighborhood under a common acquisition protocol.

## Person-level downstream result

| Person | Clean works | Anchors with downstream / anchors | Downstream unique works | Citation stratum |
|---|---:|---:|---:|---|
| James S. Albus | 311 | 4/6 | 151 | citation-rich |
| Joel Olson | 18 | 6/6 | 211 | citation-rich |
| Mary Alice McWhinnie | 27 | 6/6 | 130 | citation-rich |
| Fritz Strassmann | 57 | 5/6 | 97 | citation-rich |
| Dan Laksov | 76 | 4/6 | 88 | citation-rich |
| Hannah Gavron | 7 | 4/6 | 65 | citation-rich |
| Erika Greber | 28 | 6/6 | 32 | citation-rich |
| Willy Oelsen | 85 | 4/6 | 25 | citation-rich |
| Carl Föhl | 5 | 3/5 | 6 | citation-sparse |
| Ottomar Rosenbach | 52 | 4/6 | 5 | citation-sparse |
| Friedrich Hoeth | 5 | 2/5 | 3 | citation-sparse |
| Anton Moortgat | 13 | 1/6 | 2 | citation-sparse |
| Hilario Hernández Gurruchaga | 9 | 3/6 | 2 | citation-sparse |

## Citation-rich / citation-sparse rule

The feasibility code already reported the threshold `>=10 downstream unique works` before the person-level table was inspected.

For the pilot architecture:

- **citation-rich**: >=10 unique downstream works under the fixed anchor/horizon protocol;
- **citation-sparse**: 1–9 unique downstream works;
- **no-downstream**: 0 downstream works.

This status describes the observability of the citation layer, **not the importance of the person**.

Citation-sparse people remain in the pre-exposure network frame. They are not discarded and are not called low-impact.

### Planned use

- citation-rich: eligible for primary citation-based ego-network CPE feasibility;
- citation-sparse: retain for multiplex/sensitivity analyses and evaluate coauthor/topic/institution or domain-appropriate bibliographic influence layers;
- no-downstream: would require an alternative influence layer before confirmatory inclusion.

This rule is frozen before mental-health exposure is examined.

## Why not exclude citation-sparse cases

Sparse citation coverage may reflect:

- book-heavy publication practices;
- older bibliographic indexing;
- language/geographic coverage;
- discipline-specific citation behavior;
- incomplete historical metadata.

Dropping these people because OpenAlex under-observes them would create a new selection mechanism and could amplify geography/era/discipline bias.

## Consequence for the final CPE model

The project will not compare raw downstream work counts or raw centrality across people.

Person-level effects should be standardized within the observed ego network, for example:

- fraction of reachable downstream value lost;
- fraction recovered under substitution;
- recovery/rediscovery delay;
- normalized change in topic diversity;
- normalized brokerage/efficiency change;
- CPE relative to observed ego-network value.

Cross-person comparisons should additionally use matched era/field/visibility contexts.

## Next gate

Proceed with **all-100 MH-blind identity expansion**.

Before exposure coding:

1. resolve/adjudicate the remaining 70 frozen candidates;
2. build clean work corpora for newly verified identities;
3. assign citation-rich / citation-sparse / no-downstream network status under the same fixed protocol;
4. characterize network observability bias by cohort, visibility, geography, gender and subdomain;
5. freeze the final pre-exposure analytic frame.

Only after those steps may `EXPOSURE_CODEBOOK.md` be applied.
