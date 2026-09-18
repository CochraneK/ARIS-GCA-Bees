# DOMAIN STRATIFICATION — ARIS4C004

Date frozen: 2026-09-18

## Why this is necessary

The upstream Laouenan candidate source uses a broad `Discovery/Science` category. Inspection of the frozen 100-person frame shows that this source category contains not only STEM/biomedical contributors but also historians, philosophers, linguists, psychologists, economists, archaeologists, art historians and other knowledge-producing occupations.

Therefore ARIS4C004 should not describe the frozen frame as a homogeneous "science" sample.

Preferred description:

> a frozen historical research / knowledge-contributor frame drawn from the upstream Discovery/Science category.

The science-first OpenAlex route remains the bibliographic infrastructure pilot, but field heterogeneity must be explicit.

## Standard taxonomy

Broad domains use the **OECD Frascati Manual 2015 Fields of R&D (FORD) classification**, Table 2.2.

Broad fields are:

1. Natural sciences
2. Engineering and technology
3. Medical and health sciences
4. Agricultural and veterinary sciences
5. Social sciences
6. Humanities and the arts

The OECD framework explicitly places psychology/cognitive sciences, economics, education and sociology under Social sciences, and history/archaeology, languages/literature, philosophy/religion and arts/art history under Humanities and the arts.

Reference:

OECD (2015), *Frascati Manual 2015: Guidelines for Collecting and Reporting Data on Research and Experimental Development*, Table 2.2, DOI: 10.1787/9789264239012-en.

## Frozen-frame first-pass mapping

The deterministic source-occupation mapping in `code/analysis/map_ford_domains.py` yields the following expected broad-field composition for the 100-person frame:

| FORD broad field | N |
|---|---:|
| Natural sciences | 27 |
| Engineering and technology | 7 |
| Medical and health sciences | 13 |
| Agricultural and veterinary sciences | 0 |
| Social sciences | 20 |
| Humanities and the arts | 16 |
| Unclassified / generic occupation | 17 |
| **Total** | **100** |

This is a **pre-exposure classification**.

## Mapping conservatism

Direct occupations are mapped when the broad FORD field is reasonably clear.

Examples:

- mathematician -> Natural sciences / mathematics
- chemist -> Natural sciences / chemical sciences
- engineer -> Engineering and technology
- physician/surgeon -> Medical and health sciences
- psychologist -> Social sciences / psychology and cognitive sciences
- economist -> Social sciences / economics and business
- historian/archaeologist -> Humanities and the arts / history and archaeology
- philosopher -> Humanities and the arts / philosophy, ethics and religion

Generic labels such as:

- academic
- professor
- scientist
- research

remain **unclassified** at this stage.

Do not infer a field from a person's mental-health history, later network importance, or exposure status.

## Refining unclassified cases

Unclassified source occupations may later be mapped using pre-exposure evidence such as:

- Wikidata field of work;
- institutional department;
- dominant clean-work topic distribution;
- authoritative biography/discipline description.

Any refinement rule must be frozen before exposure analysis and preserve provenance.

If evidence is genuinely multidisciplinary, record a primary FORD broad field plus secondary field(s) rather than forcing a false single-field identity.

## Analysis rule

### Within-domain first

Primary comparisons of network/CPE quantities should be within or conditioned on broad field and historical period wherever sample size permits.

### Cross-domain only after standardization

Across FORD fields, do not compare raw:

- citations;
- work counts;
- network degree;
- betweenness;
- downstream-node counts.

Field publication/citation cultures and database coverage differ too strongly.

Cross-domain synthesis may compare standardized quantities such as:

- proportion of local downstream value lost;
- proportion recovered under adaptation;
- standardized rediscovery/recovery delay;
- percentile/rank within field × era × visibility reference sets;
- standardized topic-diversity change;
- meta-analytic standardized CPE.

## Citation-layer limitation

The pilot already shows that some book-heavy/historical contributors are citation-sparse in OpenAlex despite verified identity and clean works.

Domain stratification therefore interacts with the citation-rich/citation-sparse layer:

`FORD broad field × era × citation observability`

Citation sparsity is an observability property, not a low-importance label.

## Consequence for paper architecture

The primary application should no longer be described simply as "science versus mental-health exclusion."

Preferred framing:

> Counterfactual knowledge-network loss among historically realized research and knowledge contributors, with a bibliometric primary implementation and field-stratified analysis.

If the final verified frame becomes too heterogeneous for one confirmatory model, the principled fallback is:

1. analyze sufficiently sized FORD domains separately;
2. standardize person-level effects within domain;
3. synthesize standardized effects at the meta level;
4. keep sparse domains exploratory rather than pooling raw metrics.

## Exposure firewall

FORD assignment is determined before mental-health coding.

Mental-health exposure must not influence:

- domain assignment;
- whether a generic occupation gets resolved;
- whether a domain is retained;
- which field-specific metric is chosen.

Any domain-specific exclusions after exposure coding require explicit versioning and sensitivity analysis.
