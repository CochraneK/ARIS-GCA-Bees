# WORKBUDDY HANDOFF — ARIS4C003 INDEPENDENT CODER B

You are the **independent second historical coder (Coder B)** for one research
construct. Treat this as a blinded coding task.

## Independence declaration before starting

Before doing any research or scoring, verify that in this context you have
**not** seen:

- Coder A scores;
- any prior IKES score table;
- any contemporary country-by-discipline publication, citation, collaboration,
  ranking, or prestige results for this project;
- any prior ARIS discussion predicting which of the 21 disciplines should score
  high or low.

If any of those are already present in your context, stop and return only:

`INDEPENDENCE_STATUS: FAIL`

Do not try to "mentally ignore" contaminated information.

## Construct to code

Independently code the historical **Imperial/Colonial Knowledge Entanglement
Score (IKES)**.

IKES asks:

> To what extent did imperial/colonial systems materially shape a discipline's
> institutional formation, methods, objects/data, training, infrastructure,
> professional expansion, or postcolonial continuation?

This is **not**:
- a moral judgment;
- a measure of whether individual scholars supported empire;
- a score of present-day Western dominance;
- a measure of contemporary national strength.

## Frozen conceptual disciplines

Keep these IDs, names, and order exactly:

| concept_id | discipline |
|---|---|
| D01 | Anthropology |
| D02 | Archaeology |
| D03 | Geography |
| D04 | Development Studies |
| D05 | Linguistics |
| D06 | Tropical Medicine / colonial-health-related Public Health |
| D07 | Agriculture & Forestry |
| D08 | Geology / Earth-resource sciences |
| D09 | Sociology |
| D10 | Political Science / International Relations |
| D11 | Law |
| D12 | Economics |
| D13 | Public Administration / Social Policy |
| D14 | Education |
| D15 | History |
| D16 | Demography / Population Studies |
| D17 | Mathematics |
| D18 | Physics |
| D19 | Chemistry |
| D20 | Computer Science |
| D21 | Materials Science |

Do not add, remove, merge, rename, reorder, or substitute disciplines.

## Eleven dimensions

Score every discipline independently on:

**D1 Colonial administrative demand**  
Direct use in governing colonies/dependencies.

**D2 Territorial survey / mapping**  
Land survey, mapping, boundary making, territorial/environmental description.

**D3 Population / people / language classification**  
Census, ethnography, racial/ethnic, linguistic, demographic classification.

**D4 Overseas field sites / expeditions**  
Colonial territories as recurring field sites, expeditionary science,
specimen/data collection.

**D5 Extraction / resource survey**  
Minerals, geology, inventories, economic botany, commercial extraction.

**D6 Colonial medicine / health governance**  
Tropical medicine, sanitation, disease control, military/plantation health,
surveillance.

**D7 Agriculture / forestry / ecological transfer**  
Plantations, crop transfer, botanic gardens, forestry, agricultural stations,
ecological management.

**D8 Legal / educational / institutional transplantation**  
Export/import of law, schooling, universities, bureaucracy, or administrative
systems.

**D9 Museums / archives / collections / specimens**  
Discipline-building reliance on imperial collections, archives, museums, or
specimens.

**D10 Missionary / linguistic / religious networks**  
Missionary knowledge systems, translation, language documentation, mission
schooling where central to the field.

**D11 Postwar development-administration continuity**  
Direct continuity from colonial research/governance into development planning,
modernization, aid, postcolonial administration, or area expertise.

## Score scale

For each discipline × dimension:

- `0` = little credible evidence this mechanism mattered to disciplinary
  formation/institutional development at transnational scale;
- `1` = documented but peripheral or localized;
- `2` = substantial recurring role across important national traditions or
  institutions;
- `3` = foundational/major role in institutional formation, methods, data
  infrastructure, or professional expansion;
- `NA` = evidence genuinely insufficient.

Do not turn uncertainty into zero.

A score of 2 or 3 requires at least one strong scholarly historical source and
preferably two independent sources.

## Evidence rules

Prefer:

- peer-reviewed history of science/history of discipline;
- scholarly monographs from recognized academic presses;
- authoritative academic encyclopedia/history chapters;
- archival/institutional histories with scholarly documentation.

General web summaries may be used only to locate stronger evidence.

Do not use:
- contemporary subject rankings;
- contemporary national publication/citation/collaboration performance;
- Coder A or ARIS prior scores;
- modern "decolonization" statements as sufficient evidence by themselves.

Distinguish the colonial use of a practice from evidence that colonial systems
materially shaped the academic/professional discipline itself.

Do not assume STEM should be low. Do not assume social sciences should be high.

## Required research behavior

Work discipline by discipline. Search for both supporting and disconfirming
historical evidence. When a field has strong national heterogeneity, record it
rather than forcing a universal narrative.

If evidence is too weak to distinguish 0 from 1 or 1 from 2, use `NA` or a
lower-confidence score rather than guessing.

## Required output — Part 1: one CSV block

Return exactly one fenced CSV block with this header:

```csv
concept_id,discipline,D1,D2,D3,D4,D5,D6,D7,D8,D9,D10,D11,IKES_B
```

Provide exactly 21 rows D01–D21 in order.

`IKES_B` = arithmetic mean of all non-NA D1–D11 scores for that discipline.
Do not impute NA.

## Required output — Part 2: 21 evidence sections

After the CSV, provide exactly one section for each concept in order:

`### D01 — Anthropology`

through:

`### D21 — Materials Science`

Each section must contain:

- 2–5 sentences explaining the historical rationale;
- strongest scholarly sources supporting any score ≥2, or an explicit statement
  that no score ≥2 was assigned;
- important uncertainty/national heterogeneity;
- any dimensions scored `NA`;
- exactly one final line:
  - `Confidence: high`
  - `Confidence: medium`
  - `Confidence: low`

Cite enough bibliographic detail that another researcher can locate the source.
Do not cite Coder A, ARIS-generated score files, or contemporary outcomes.

## Required output — Part 3: blinding declaration

End with:

`## BLINDING DECLARATION`

The first two lines underneath must be exactly:

`BUNDLE_ACCESS_STATUS: PASS`

`INDEPENDENCE_STATUS: PASS`

Use `BUNDLE_ACCESS_STATUS: PASS` only if this context accessed **only** the
files whitelisted in the blind bundle plus independently discovered historical
scholarly evidence. If this context opened any ARIS4C003 file outside the blind
bundle — including the paper-root README/STATUS or Coder A material — use:

`BUNDLE_ACCESS_STATUS: FAIL`

Use `INDEPENDENCE_STATUS: PASS` only if you did not encounter Coder A scores
or contemporary confirmatory outcomes. Otherwise use:

`INDEPENDENCE_STATUS: FAIL`

If either status is FAIL, stop after the declaration and do not present the
result as confirmatory Coder B.

After the two status lines, state briefly what information you did and did not
access.

## Critical constraint

Do not read other files in the ARIS4C003 directory. Everything needed to perform
Coder B is contained in this blind bundle plus independently discovered
historical scholarly evidence.

Your output is an independent coding artifact, not an interpretation of whether
the research hypothesis is correct.
