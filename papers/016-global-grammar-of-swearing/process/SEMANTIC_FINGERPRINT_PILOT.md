# ARIS4C016 Semantic Fingerprint Pilot — Measurement Failure as Result

Updated: 2026-09-18

## Goal

Test whether the source Study-1 category labels can directly generate a
cross-community semantic "Taboo Fingerprint" after only conservative
high-confidence harmonization.

## Result

**Not yet.**

The pilot is informative precisely because it fails a comparability check.

Using only the semantic mappings already allowed by
`code/harmonize_labels.py`, semantic-source coverage of lexical rows varies
substantially:

| Community | Semantic-mapped row coverage |
|---|---:|
| Cantonese (CN) | 70.7% |
| English (US) | 66.4% |
| Finnish (FI) | 64.8% |
| English (CA) | 59.9% |
| Slovenian (SI) | 59.8% |
| Serbian (RS) | 54.0% |
| Italian (IT) | 52.2% |
| French (FR) | 49.2% |
| English (SG) | 44.6% |
| Mandarin (CN) | 43.7% |
| Spanish (CL) | 40.3% |
| English (GB) | 39.0% |
| English (AU) | 35.8% |
| Dutch (BE) | 31.4% |
| German (DE) | 27.9% |
| Thai (TH) | 26.8% |
| Setswana (BW) | 20.7% |
| Spanish (ES) | 10.9% |

This coverage difference alone is too large for naïve country/language
prevalence comparisons.

## Why the apparent fingerprint is structurally biased

The original source field mixes ontology levels.

Labels such as:
- sexual;
- scatological;
- blasphemy;

directly provide a **semantic source**.

But labels such as:
- insult;
- slur;

do not specify the semantic source of the expression.

Therefore a source row coded only as `insult` may in reality involve:
- sex;
- kinship;
- intelligence;
- animalization;
- appearance;
- identity;
- morality;
- another local taboo domain;

but the original flat annotation does not tell us which.

This means that the subset with recoverable semantic labels is not a random
subset of the taboo lexicon.

## Apparent sexual dominance is not yet a cultural finding

Across all high-confidence semantic assignments:
- 2,387 / 3,921 type-level assignments map to `SEX_SEXUALITY`;
- 7,422 / 11,762 production-weighted assignments map to that domain.

Those large shares **must not** be interpreted as evidence that sex accounts
for ~60% of global taboo language.

They partly reflect the source coding architecture: "sexual" was explicitly
available as a semantic label, whereas the semantic content of many rows
labeled only "insult" or "slur" is latent.

## Consequence

The first scientifically defensible Global Taboo Fingerprint requires
**re-coding the lexical items on orthogonal axes**, not merely translating or
renaming the original categories.

The original labels remain useful as:
- weak supervision;
- sampling strata;
- provenance;
- disagreement diagnostics.

They cannot serve as the final semantic gold standard.

## Two estimands after re-coding

Once reliability is acceptable, report both:

### Type fingerprint
Each unique lexical row contributes once to each independently coded semantic
domain.

This describes lexical repertoire structure.

### Production-weighted fingerprint
Each row is weighted by Study-1 production count `n`.

This approximates elicitation salience in that sample.

Because a row can have multiple semantic domains, domain shares should be
explicitly defined as:
- share of assignments; or
- row prevalence;

and never silently assumed to sum to one.

## Required sensitivity analyses

For every community:
- high-confidence agreed rows only;
- all adjudicated rows;
- type-weighted;
- production-weighted;
- with/without unresolved rows under explicit bounds;
- minimum annotation-coverage thresholds.

A community should not be ranked on a domain if its identification interval is
dominated by unresolved/missing semantic content.

## Scientific payoff

The Phase-0 failure changes the paper's strongest contribution.

Instead of:

> Here is a colorful map showing what each country swears about.

the defensible target becomes:

> Here is a measurement-corrected framework showing which apparent
> cross-cultural differences survive harmonized ontology, annotation
> reliability, lexical identity, language genealogy and missingness.

That is a stronger comparative-linguistic contribution.
