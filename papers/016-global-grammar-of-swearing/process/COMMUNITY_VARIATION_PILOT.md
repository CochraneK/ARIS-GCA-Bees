# ARIS4C016 Community-Variation Pilot

Updated: 2026-09-18

## Purpose

Quantify how much rating variation remains when the lexical item is held
approximately constant across communities that use the same language.

This is a descriptive Phase-0 pilot, not a causal estimate of culture.

## English repeated-community design

Communities:
- AU
- CA
- GB
- SG
- US

Among Study-2 non-filler rows, 139 lexical items occur in at least two English
community samples:

- 68 occur in exactly 2 communities;
- 26 in exactly 3;
- 22 in exactly 4;
- 23 in all 5.

For each rating dimension, we computed:
1. variance across item means; and
2. mean variance of the same item across communities.

A simple diagnostic ratio is:

```
within-item cross-community variance
------------------------------------
within-item variance + between-item-mean variance
```

This is not an ICC and should not be interpreted as a formal variance
component estimate. It is a scale diagnostic for Phase 0.

## English results

| Dimension | Between-item variance | Mean within-item cross-community variance | Simple within share |
|---|---:|---:|---:|
| Tabooness | 0.012571 | 0.003091 | 0.197 |
| Offensiveness | 0.011232 | 0.003040 | 0.213 |
| Valence | 0.010496 | 0.003496 | 0.250 |
| Arousal | 0.006742 | 0.003714 | 0.355 |
| Concreteness | 0.005050 | 0.003367 | 0.400 |
| Age of acquisition | 0.018189 | 0.003098 | 0.146 |

Interpretation:
- lexical identity dominates tabooness/offensiveness differences in this
  simple decomposition;
- nevertheless, same-item cross-community variation is non-trivial;
- arousal and concreteness appear less community-stable than AoA or taboo
  ratings by this crude metric;
- formal inference requires item/community uncertainty and sample-size
  weighting.

## Spanish repeated-community design

Chile vs Spain contains only 16 shared Study-2 taboo items.

Simple within-share diagnostics:
- tabooness: 0.353;
- offensiveness: 0.176;
- valence: 0.194;
- arousal: 0.212;
- concreteness: 0.275;
- AoA: 0.297.

The Spanish comparison is underpowered for broad conclusions and should remain
secondary.

## Relation to pairwise correlations

The earlier Phase-0 audit found strong but imperfect English pairwise
correlations. For example:
- AU–US tabooness r ≈ .891;
- CA–US tabooness r ≈ .869;
- CA–SG tabooness r ≈ .667.

The variance diagnostic and pairwise correlations tell the same qualitative
story: taboo ratings have substantial cross-community stability, but are not
community invariant.

## Scientific implication

ARIS4C016 should not frame the central question as either:
- "swearing is universal", or
- "swearing is culturally relative".

The empirically useful question is:

> Which components of taboo-language structure are stable across communities,
> and which components remain context-sensitive after lexical identity,
> language genealogy and measurement differences are controlled?

## Next model

For English, fit a repeated-item hierarchical model with:
- item random intercept;
- community effect / partial pooling;
- item-by-community residual structure;
- production frequency / corpus frequency sensitivity;
- ontology-domain interactions;
- uncertainty weighted by rating reliability where available.

The model should estimate community-associated variation without calling it a
causal culture effect.
