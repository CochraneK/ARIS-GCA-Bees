# ARIS4C016 Phase-0 Structural Audit

Updated: 2026-09-18

## Scope

This audit reads the public Sulpizio et al. (2024) OSF files directly and
summarizes dataset structure without printing raw taboo expressions.

Primary files:
- `taboo_study1.csv` — 8,190 rows, 18 language-community samples;
- `taboo_study2.csv` — 4,240 rows, 18 language-community samples;
- `number_participants_study1.csv` — Study-1 sample sizes.

The reproduction script is `code/phase0_audit.py`. It verifies the OSF
SHA-256 values before analysis.

## Finding 1 — elicitation yield differs dramatically

Study-1 production count divided by participant count ranges from roughly:

- Mandarin (CN): 9.32 items/person;
- Spanish (CL): 12.49;
- Thai (TH): 12.96;
- Canada English: 13.35;
- UK English: 13.86;
- ...
- Dutch (BE): 29.56;
- German (DE): 52.88.

Therefore raw vocabulary size or production count is not interpretable as a
simple cultural "swearing propensity" measure. It can reflect instructions,
task interpretation, compounding/productivity, lexicalization decisions,
researcher cleaning, participant engagement, or the local boundary between
"taboo", "insult", "rude", and merely socially inappropriate language.

## Finding 2 — the category ontology is not harmonized enough for naïve comparison

Study 1 contains 68 distinct non-empty/missing values in the primary
`category` field alone.

Alongside the intended broad labels (insult, slur, sexual, scatological,
blasphemy), the file contains:
- medical / illness / disease;
- political / ideology / WWII / Nazi-related;
- animal / appearance / stupidity / family / death;
- local/custom categories;
- spelling/label variants such as sexualual references and scathological;
- non-semantic workflow-like labels and unclear abbreviations.

This is useful raw material, but it is not yet a cross-language ontology.

## Finding 3 — coding style itself varies by sample

Examples of primary-category missingness:
- Cantonese (CN): 0%;
- German (DE): 0.2%;
- English (GB): 5.6%;
- Setswana (BW): 67.6%;
- Spanish (ES): 80.4%.

Examples of rows with two or more category labels:
- Spanish (ES): 2.7%;
- Setswana (BW): 10.5%;
- Dutch (BE): 15.8%;
- English (US): 52.3%;
- Finnish (FI): 61.1%;
- Thai (TH): 65.7%;
- Cantonese (CN): 67.2%;
- English (CA): 77.3%.

These differences are too large to treat raw category proportions as directly
comparable cultural measurements.

## Finding 4 — same-language communities are similar but not identical

Study-2 shared-word ratings reproduce the broad pattern reported by the
original authors: English-speaking communities often correlate strongly, but
not perfectly, on tabooness/offensiveness.

Examples:
- English AU vs US: tabooness r ≈ .891; offensiveness r ≈ .871;
- English CA vs US: tabooness r ≈ .869; offensiveness r ≈ .860;
- English CA vs SG: tabooness r ≈ .667; offensiveness r ≈ .732;
- Spanish CL vs ES (16 shared items): tabooness r ≈ .662; offensiveness r ≈ .903.

These are descriptive pairwise correlations, not estimates of a cultural
causal effect.

## Methodological correction for ARIS4C016

The first confirmatory target is now **ontology harmonization**, not cultural
regression.

Before comparing countries/languages on semantic-domain prevalence:

1. preserve every raw category label;
2. normalize spelling/format variants;
3. create a language-neutral canonical multi-label ontology;
4. mark labels that cannot be mapped without native-speaker/context review as
   `UNRESOLVED_LOCAL`;
5. quantify inter-coder agreement on a stratified multilingual subset;
6. run all prevalence analyses both:
   - on high-confidence harmonized labels only; and
   - under sensitivity mappings for unresolved labels.

## Consequence for the paper's novelty

The strongest defensible contribution is no longer simply a "global taboo
atlas." It is a **measurement-corrected comparative framework** that separates:

- elicitation behavior;
- annotation behavior;
- lexical semantics;
- community ratings;
- language genealogy;
- sociocultural context.

This prevents annotation heterogeneity from being mistaken for cultural
difference.

## Next analyses

1. Canonical ontology v0 and mapping rules.
2. Stratified mapping audit by community.
3. Reproduce original Study-2 affective/rating baselines.
4. Variance decomposition on tabooness/offensiveness.
5. Same-language cross-country contrasts with measurement-error awareness.
6. Add Glottolog identifiers and language-family structure.
7. Leave-one-family-out tests.
