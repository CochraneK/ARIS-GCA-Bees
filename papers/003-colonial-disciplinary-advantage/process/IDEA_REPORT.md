# IDEA REPORT — ARIS4C003

## Working title

**Colonial Legacies and the Global Geography of Disciplinary Advantage**

Possible subtitle: **Evidence from bibliometrics, university rankings, and international knowledge networks**

## Core claim to test, not assume

Formal empire may have left durable discipline-specific knowledge capital. The project tests whether imperial and colonial histories are associated with contemporary national specialization in disciplines that were historically intertwined with imperial administration, territorial knowledge, overseas fieldwork, extraction, health, language classification, and colonial social research.

The project is deliberately falsifiable. It does not assume that colonizers are stronger, that colonized states benefit, or that rankings measure objective quality.

## Theoretical mechanism

A generic persistence chain is:

`historical imperial/colonial system`
→ `administrative and scientific demand`
→ `trained personnel + institutions + collections + archives + field stations + professional societies + journals + language/education networks`
→ `disciplinary path dependence`
→ `contemporary specialization / influence / collaboration / prestige`

Potential mechanisms differ by actor:

### Imperial-center pathway

Imperial administration and overseas expansion can increase demand for mapping, ethnography, languages, medicine, agriculture, geology, demography, law, and governance knowledge. Durable institutions and prestige may persist after empire.

### Former-colony pathway

Colonial rule can create universities, administrative data systems, lingua-franca networks, professional institutions, and links to metropolitan universities, but can also produce extraction, underinvestment, center–periphery dependence, external control of research agendas, and later brain drain. The net effect is therefore not signed a priori.

### Dyadic pathway

Former colonial pairs may retain language, institutional, migration, training, funding, and coauthorship ties. This can be tested as a country-pair network persistence hypothesis rather than inferred from national averages.

## Important conceptual distinction

The motivating concept is **historical knowledge capital**, not "colonialism makes science better." Historical knowledge capital is a neutral analytical label for durable stocks of institutions, skills, archives, collections, networks, and prestige that can arise through unequal historical processes.

## Why comparative disciplinary advantage is the main outcome

Raw research output confounds the proposed mechanism with population, GDP, research spending, university-system size, and general scientific capacity.

The more relevant quantity is whether a country performs **unusually strongly in discipline d relative to its own overall scientific profile and the global prevalence of d**.

Candidate measure:

`RCA(c,d,t) = [Output(c,d,t) / Output(c,all,t)] / [Output(world,d,t) / Output(world,all,t)]`

Related measures should be constructed for citations/top papers and compared with alternative specialization indices because classic RCA has known interpretive limitations.

## Anchor literature / methodological precedents

These are starting points, not a completed systematic review.

1. Raja et al. (2022), *Nature Ecology & Evolution*, **Colonial history and global economics distort our understanding of deep-time biodiversity**. Demonstrates that colonial history and contemporary socioeconomic conditions can be modeled as predictors of present-day geography of knowledge production in palaeontology. DOI: 10.1038/s41559-021-01608-8.

2. Abramo et al. (2022), *Journal of Informetrics*, **Revealing the scientific comparative advantage of nations: Common and distinctive features**. Maps 199 countries across 254 fields using field-sensitive measures of scientific specialization. DOI: 10.1016/j.joi.2021.101244.

3. Harzing & Giroud (2014), *Journal of Informetrics*, **The competitive advantage of nations: An application to academia**. Applies revealed comparative advantage to disciplinary research profiles and explicitly includes social sciences. DOI: 10.1016/j.joi.2013.10.007.

4. Literature on the history of anthropology, colonial social science, imperial geography, tropical medicine, colonial linguistics, archaeology, and development studies provides the historical mechanism layer and must be systematically reviewed before the discipline-entanglement score is frozen.

## Novelty target

The intended contribution is **not** merely to show that colonialism shaped particular disciplines historically. That claim already has a large historiography.

The novelty target is to connect that historiography to modern large-scale quantitative science-of-science evidence by asking whether colonial/imperial histories predict a **cross-disciplinary structure of contemporary comparative advantage** across countries, and by decomposing persistence into:

- output specialization;
- citation/elite-paper specialization;
- international knowledge networks;
- institutional/prestige outcomes.

A strong novelty review must search for prior work that already estimates colonial exposure against country-by-discipline specialization. If a close predecessor exists, the project should narrow or differentiate rather than overclaim novelty.

## Confirmatory vs exploratory boundary

### Confirmatory

- preregistered exposure definitions;
- preregistered entanglement coding procedure;
- a limited discipline set with clear historical rationale;
- primary bibliometric outcomes;
- fixed-effect specification and planned robustness checks.

### Exploratory

- all-discipline scan;
- data-driven clusters of fields;
- alternative field taxonomies;
- specific empire/ruler heterogeneity;
- additional ranking products;
- network-community detection;
- historical case studies suggested by outliers.

## Candidate colonial/imperial exposure constructs

Do not collapse these prematurely:

- ever imperial/colonial ruler;
- accumulated years ruling overseas dependencies;
- number of dependencies / population / territory governed;
- empire duration weighted by dependency population or area;
- formerly colonized/dependent indicator;
- years under external rule;
- primary colonial ruler;
- number of colonial rulers;
- independence cohort/date;
- common colonial ruler;
- direct former-colonial dyad;
- common official/colonial language.

The construct review must decide which are substantively meaningful and empirically recoverable without creating an arbitrary "empire score."

## Candidate discipline-entanglement dimensions

A discipline may be historically entangled with empire through multiple mechanisms:

1. administrative/governance demand;
2. territorial mapping and survey;
3. classification of peoples/languages/populations;
4. overseas field sites and expeditions;
5. resource extraction and geological/botanical survey;
6. colonial health and disease control;
7. agriculture/forestry/ecological transfer;
8. law/education/institutional transplantation;
9. museums, collections, archives, specimens;
10. missionary/linguistic networks;
11. postwar development administration.

A preregistered coding protocol should use historical sources and preferably at least two independent coders or a blinded literature-derived scoring process. The score should be frozen before contemporary outcome inspection.

## Candidate data sources

### Colonial history

- ICOW Colonial History Data: dependencies, colonial rulers, independence information for states in the COW system.
- COLDAT / other duration-oriented colonial datasets where documentation and licensing permit.
- CEPII GeoDist/Gravity variables for direct colonial relation, common colonizer, common language, and geographic controls.

### Bibliometrics

- OpenAlex for works, institutions, countries, field/topic taxonomy, citations, and authorship relations.
- Leiden Ranking Open Edition for independently generated university-level OpenAlex bibliometric indicators and robustness checks.

### Rankings/prestige

- QS subject rankings, THE subject rankings, Shanghai GRAS where publicly and legally obtainable.
- These are secondary outcomes; methodology components should be modeled or interpreted separately where possible.

### Controls

Potentially World Bank/UNESCO/OECD/Our World in Data and other documented public sources for population, GDP/GDP per capita, R&D expenditure, tertiary education, English/official language, geography, region, political/institutional variables, and historical university-system covariates.

## Identification threats that must remain visible

1. **General wealth/capacity:** imperial powers are often rich and have old universities.
2. **Reverse historical selection:** states able to build empires may already have institutional/scientific advantages.
3. **Language/database bias:** English-language and Western-indexed outputs are overrepresented in common bibliometric systems.
4. **Ranking endogeneity:** prestige surveys can perpetuate historical reputation.
5. **Discipline selection:** choosing only fields expected to fit the story creates researcher degrees of freedom.
6. **Field taxonomy error:** modern categories do not map cleanly onto historical disciplines.
7. **Postcolonial state changes:** modern countries do not perfectly correspond to historical empires/dependencies.
8. **Migration/human capital shocks:** scientist migration, war, state formation, industrialization, and Cold War investments can generate competing path dependence.
9. **Database time window:** modern bibliometric windows may capture recent policy rather than long-run legacy.
10. **Small-country instability:** RCA-like ratios can explode with tiny denominators.

## What would make this paper strong

- results survive alternative specialization metrics and fractional counting;
- a prespecified discipline-entanglement gradient predicts effect size;
- effects are not generic across all disciplines;
- colonizer-center and colonized-state pathways are separated;
- dyadic former-colonial ties provide an independent network test;
- rankings and bibliometrics tell a coherent but not mechanically identical story;
- null and contrary findings are interpretable within the same design.

## What would kill or radically narrow the original theory

- no association after general capacity controls/fixed effects;
- no discipline gradient;
- only reputation rankings move while objective bibliometrics do not;
- results are explained by common language/English-indexing alone;
- one empire (for example, the British Empire) accounts for nearly all estimates;
- results reverse across reasonable field classifications;
- exposure coding is too ambiguous to preregister reproducibly.

In those cases the project should pivot to a narrower, defensible finding such as **prestige persistence**, **Anglophone knowledge-network persistence**, or a specific historical mechanism rather than preserving the original broad claim.
