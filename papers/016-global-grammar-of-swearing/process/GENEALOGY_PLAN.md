# ARIS4C016 Genealogy and Identification Plan

Updated: 2026-09-18

## The key correction

The public dataset contains **18 community samples, not 18 independent languages**.

After linking samples to Glottolog IDs:
- 18 community samples;
- 13 unique languages;
- 17 countries;
- 5 top-level Glottolog families;
- 8 of 13 languages (61.5%) are Indo-European.

Repeated-language structure:
- English: 5 countries (AU, CA, GB, SG, US);
- Spanish: 2 countries (CL, ES).

Repeated-country structure:
- China: 2 language samples (Yue/Cantonese and Mandarin).

This structure is scientifically useful, but it is not a balanced
language-by-country factorial design.

## Why this matters

A model that treats all 18 samples as independent "languages" would:
1. over-weight English;
2. understate genealogical dependence;
3. conflate community variation with language variation;
4. produce overconfident claims about universality.

Likewise, a model with both language and country effects cannot cleanly
identify them for most samples because most language-country combinations
occur only once.

## Phase-0 identification hierarchy

### Tier 1 — within-language community variation

Strongest current design.

Primary:
- English across AU, CA, GB, SG, US.

Secondary:
- Spanish across CL and ES.

Questions:
- How stable are ratings for shared lexical items?
- Which items show the greatest community divergence?
- Does divergence remain after uncertainty / item-frequency adjustment?
- Are differences larger for particular ontology axes?

These comparisons hold language identity approximately fixed and vary
community/country context, although dialect, demographics and sampling still
differ.

### Tier 2 — within-country language contrast

China contains Cantonese/Yue and Mandarin samples.

This is **not** a clean culture-controlled language experiment:
- the varieties are genealogically related;
- the sampling sites/subnational environments differ;
- local linguistic ecologies differ.

Use this contrast descriptively, not as a causal language-vs-culture
decomposition.

### Tier 3 — cross-language comparison

Use only after ontology harmonization and coverage correction.

Cross-language prevalence/rating comparisons should:
- cluster or partially pool by community;
- represent repeated language IDs explicitly;
- include language family / phylogenetic dependence in sensitivity analyses;
- report family imbalance.

## What the current data cannot identify well

The current 13-language set cannot support a strong global estimate of
"culture versus language" as two orthogonal causal components.

Reasons:
- only English has substantial cross-country replication;
- Spanish has one pair;
- most languages appear in one country only;
- 8/13 languages are Indo-European;
- three top-level families are represented by only one language each;
- annotation coverage differs sharply across samples.

Therefore the initial paper should use terms such as:
- community-associated variation;
- language-associated variation;
- genealogically structured similarity;

and avoid causal phrasing such as:
- culture causes;
- language determines.

## Genealogy-aware analysis plan

### Descriptive layer
Compute ontology fingerprints by community with explicit annotation-coverage
intervals.

### Repeated-language layer
For English and Spanish, compare common lexical items and ontology-domain
scores across communities.

### Language layer
Collapse/partially pool repeated communities when estimating language-level
fingerprints.

### Family layer
Treat top-level family as dependence structure/sensitivity, not a five-level
causal predictor.

With only 5 top-level families, leave-one-family-out analysis is useful as a
stress test but too coarse to establish a universal law by itself.

### Future phylogenetic layer
If the expanded dataset contains substantially more languages/families, use a
Glottolog-derived tree or distance matrix to model phylogenetic covariance.

## Expansion design implied by Phase 0

Future sampling should deliberately create crossed cells rather than simply
add more languages.

High-value additions:
- multiple countries for the same language;
- multiple languages within the same country;
- multiple unrelated families within comparable cultural settings;
- non-Indo-European replication at substantially greater depth.

The optimization target is **identifiability and family diversity**, not a
headline language count.

## Data artifact

See `data/language_metadata.json` for the canonical mapping between the 18
community samples and 13 Glottolog language IDs.
