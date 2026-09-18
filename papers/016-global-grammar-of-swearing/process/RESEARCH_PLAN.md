# ARIS4C016 Research Plan

## Research question

Which properties of taboo language are cross-linguistically recurrent, which cluster by language genealogy, and which vary with sociocultural context?

## Unit of analysis

Keep four levels distinct:
1. lexical item / expression;
2. speaker;
3. language-community sample;
4. language family / cultural context.

A translated English gloss is metadata, not the canonical semantic unit.

## Primary construct families

### Semantic source
Sex/sexuality; excretion/disgust; religion/sacredness; kinship/ancestry; body; animals; death/disease; intelligence/competence; morality; social status; identity/group reference; other community-specific taboo.

### Pragmatic function
Direct insult; expletive/interjection; intensifier; curse/wish of harm; teasing/solidarity; shock/emphasis; threat; self-directed use; quoted/metalinguistic use.

### Target structure
Self; interlocutor; third party; kin; ancestor; deity/sacred entity; social group; no explicit target.

### Form
Part of speech; compounding/derivation; reduplication; euphemism/minced form; orthographic masking; phonological profile.

## Primary hypotheses

**H1 Universal-core:** a small set of semantic taboo domains recurs above matched null expectations across unrelated language families.

**H2 Cultural-allocation:** communities differ in the relative allocation of taboo vocabulary across semantic domains after accounting for elicitation and sample size.

**H3 Genealogical-structure:** taboo-profile similarity is partly predicted by language-family relatedness, but genealogy does not fully explain community variation.

**H4 Same-language cultural divergence:** varieties of the same language sampled in different countries show measurable differences in taboo profiles and ratings.

**H5 Phonological constraint:** candidate phonological patterns in taboo words survive length/frequency/phonotactic controls and held-out-language tests.

H1–H5 are separate. Failure of one does not imply support for another.

## Phase 0 — reproducible reanalysis

Dataset: Sulpizio et al. (2024), 13 languages / 17 countries.

Tasks:
- reproduce published descriptive results;
- inspect the original multi-label categories;
- quantify inter-community category composition;
- hierarchical variance decomposition for tabooness/offensiveness;
- same-language cross-country contrasts where identifiable;
- sensitivity to rare-word thresholds and translation mapping;
- exploratory distance matrix among communities.

No broad cultural-causation claim is allowed in Phase 0.

## Phase 1 — genealogy and geography

Join language samples to Glottolog identifiers and genealogical trees.

Models:
- hierarchical mixed models;
- language-family random effects;
- phylogenetic covariance where sample size permits;
- Mantel-style distance correlations only as secondary descriptive checks;
- leave-one-family-out validation for claims of generality.

## Phase 2 — cultural predictors

Candidate sources may include World Values Survey and carefully mapped ethnographic databases.

Rules:
- ecological predictors stay ecological;
- cultural predictors must have temporal and population alignment;
- avoid high-dimensional country regressions with the small Phase-0 country count;
- prefer preregistered low-dimensional hypotheses and partial pooling.

## Phase 3 — expanded elicitation

Only after Phase 0/1 feasibility is demonstrated.

Sampling goals:
- maximize language-family diversity;
- deliberately include the same language across multiple countries;
- deliberately include multilingual countries;
- collect bottom-up free generation before showing any researcher taxonomy;
- collect speaker ratings independently of researcher semantic coding.

## Negative controls

1. Neutral/high-arousal word sets matched on length and frequency for phonology.
2. Randomized semantic labels preserving category frequencies.
3. Permuted country/community labels within language where structurally valid.
4. Pseudo-cultural predictors matched in dimensionality.
5. Leave-one-language-family-out generalization.
6. Translation-free analyses using native labels/embeddings as sensitivity checks.

## Major identification threats

Translation non-equivalence; researcher-category circularity; country-language confounding; phylogenetic pseudoreplication; platform/censorship bias; age and gender composition; bilingualism; frequency-source mismatch; ecological fallacy; slur underreporting; orthographic masking; historical semantic drift.

## Interpretation ladder

A. descriptive difference;
B. replicated community difference;
C. cross-language-family regularity;
D. genealogy-adjusted cultural association;
E. held-out community/family prediction;
F. independently replicated cross-cultural pattern.

Only C–F can support claims framed as cross-linguistic generalities; only D–F can support culture-related explanatory claims.
