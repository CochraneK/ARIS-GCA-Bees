# DISCIPLINE ENTANGLEMENT CODING PROTOCOL — ARIS4C003

## Purpose

Create a discipline-level historical **Imperial/Colonial Knowledge Entanglement Score (IKES)** without using contemporary ranking, publication, citation, or collaboration outcomes.

This is a construct-coding exercise, not a post-hoc labeling of fields that happen to show strong modern effects.

## Confirmatory conceptual discipline set

Freeze the following 21 conceptual fields before outcome inspection:

1. Anthropology
2. Archaeology
3. Geography
4. Development Studies
5. Linguistics
6. Tropical Medicine / colonial-health-related Public Health
7. Agriculture & Forestry
8. Geology / Earth-resource sciences
9. Sociology
10. Political Science / International Relations
11. Law
12. Economics
13. Public Administration / Social Policy
14. Education
15. History
16. Demography / Population Studies
17. Mathematics
18. Physics
19. Chemistry
20. Computer Science
21. Materials / modern engineering comparator

The later bibliometric crosswalk may map one conceptual field to more than one database field/topic. Mapping rules must be finalized before extracting country-level outcomes.

## Eleven coding dimensions

Each discipline is independently evaluated on:

D1. **Colonial administrative demand** — direct use in governing colonies/dependencies.

D2. **Territorial survey / mapping** — mapping, land survey, boundary making, environmental/territorial description.

D3. **Population / people / language classification** — census, ethnography, racial/ethnic classification, linguistic classification, demographic categorization.

D4. **Overseas field sites / expeditions** — dependence on colonial territories for fieldwork, expeditionary science, specimen/data collection.

D5. **Extraction / resource survey** — mining, geology, resource inventory, commercial extraction, economic botany, etc.

D6. **Colonial medicine / health governance** — disease control, tropical medicine, sanitation, military/plantation health, epidemiological surveillance.

D7. **Agriculture / forestry / ecological transfer** — crop transfer, plantations, forestry, botanical gardens, agricultural stations, ecological management.

D8. **Legal / educational / institutional transplantation** — export/import of legal, schooling, university, bureaucratic, or administrative systems.

D9. **Museums / archives / collections / specimens** — discipline-building reliance on imperial collecting institutions and archives.

D10. **Missionary / linguistic / religious networks** — missionary knowledge systems, translation, language documentation, mission schooling where central to the field.

D11. **Postwar development-administration continuity** — direct continuity from colonial research/governance into development planning, modernization, aid, postcolonial administration, or area expertise.

## Scoring rule

For every discipline × dimension:

- **0** = little credible evidence that this mechanism was important to the discipline's formation/institutional development at transnational scale;
- **1** = documented but peripheral/localized;
- **2** = substantial recurring role across important national traditions or institutions;
- **3** = foundational/major role in the discipline's institutional formation, methods, data infrastructure, or professional expansion.

Use `NA` rather than 0 when evidence is genuinely insufficient. An NA must be resolved by targeted search or explicit adjudication before the confirmatory score is finalized.

## Evidence threshold

A score of 2 or 3 requires at least one strong scholarly historical source and preferably two independent sources, such as:

- peer-reviewed history of science/discipline article;
- academic monograph from a recognized scholarly press;
- authoritative research encyclopedia/history chapter;
- archival/institutional history with scholarly documentation.

General web summaries and present-day decolonization statements may be search leads but are not sufficient evidence by themselves.

## Blinding rule

Coders/evidence summarizers must not consult country-level contemporary outcomes for the field while assigning IKES scores.

They may know general historical facts and the research question. They must not see whether Britain/France/etc. currently score highly in that field.

## Coder design

Preferred:

- Coder A: independent historical evidence summary + scores.
- Coder B: independent historical evidence summary + scores.
- Both use the same rubric and conceptual field definitions.
- Compute agreement (weighted kappa or ICC as appropriate).
- Differences ≥2 points on any dimension require documented adjudication.
- Adjudicator sees evidence, not contemporary outcome matrices.

GPTPage may serve as an evidence-discovery assistant but should not be treated as an independent human coder unless explicitly labeled as AI-assisted coding.

## Primary score

After adjudication:

`IKES_d = mean(D1...D11)`

Equal weighting is primary because it is transparent and avoids outcome-informed weighting.

Secondary summaries:

- governance/social-classification subscore: D1 + D3 + D8 + D11
- field/extraction subscore: D2 + D4 + D5 + D7 + D9
- health subscore: D6
- language/mission subscore: D10

These secondary scores are exploratory unless frozen before outcome extraction.

## Sensitivity definitions

1. Median instead of mean across dimensions.
2. Binary high-entanglement indicator defined *before outcomes* using a prespecified threshold on IKES.
3. Leave-one-dimension-out IKES.
4. Historical-period-specific coding if evidence shows that a discipline's entanglement changed sharply across centuries.

Do not tune the threshold to maximize the historical-exposure coefficient.

## Important interpretation rule

IKES measures **institutional/historical entanglement**, not moral endorsement of colonialism.

A discipline can receive a high score even when many of its scholars criticized empire, because the construct concerns whether colonial/imperial systems materially shaped the field's institutions, methods, objects, datasets, funding, or networks.

## National heterogeneity caveat

A single global discipline score necessarily compresses different national histories. Therefore:

- primary IKES captures broad transnational field entanglement;
- national tradition × discipline case studies are secondary;
- if a field has radically different imperial histories by country, flag this and test country-specific historical interactions where data permit.

## Crosswalk freeze gate

Before contemporary outcome extraction, create `DISCIPLINE_CROSSWALK.csv` with:

- conceptual discipline;
- OpenAlex domain/field/subfield/topic IDs used;
- inclusion/exclusion rationale;
- ranking categories where applicable;
- whether the mapping is primary or sensitivity-only.

The crosswalk must be versioned and frozen before running the confirmatory models.
