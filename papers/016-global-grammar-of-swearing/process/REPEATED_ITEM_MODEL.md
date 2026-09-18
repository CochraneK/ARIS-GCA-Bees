# ARIS4C016 Repeated-Item English Model

Updated: 2026-09-18

## Question

Among lexical items shared by multiple English-speaking community samples,
how much additional rating variation is associated with community **after
holding lexical item identity fixed**?

This is a Phase-0 measurement model. It estimates community-associated
variation, not a causal culture effect.

## Data

Source: Sulpizio et al. (2024) Study 2 public OSF data.

Included:
- English (AU)
- English (CA)
- English (GB)
- English (SG)
- English (US)
- non-filler items;
- lexical items observed in at least two English communities.

Resulting design:
- 139 shared lexical items;
- 417 item × community aggregate-rating observations.

## Estimator

We use a fixed-effects Frisch–Waugh–Lovell decomposition:

1. residualize the rating with respect to lexical-item fixed effects;
2. residualize community indicators with respect to lexical-item fixed effects;
3. regress residualized ratings on residualized community indicators;
4. compute the partial R² of community relative to the item-only model.

Uncertainty:
- 500 bootstrap resamples over lexical items;
- intervals therefore reflect item-sampling variability;
- they do **not** fully propagate the original participant-level rating
  uncertainty because the public Study-2 table contains aggregate item ratings.

## Results

| Dimension | Community partial R² after item FE | Item-bootstrap 95% interval |
|---|---:|---:|
| Tabooness | 0.0265 | 0.0095–0.0837 |
| Offensiveness | 0.0361 | 0.0125–0.1045 |
| Valence | 0.0446 | 0.0173–0.1150 |
| Arousal | 0.0827 | 0.0384–0.1689 |
| Concreteness | 0.2112 | 0.1198–0.3105 |
| Age of acquisition | 0.0874 | 0.0347–0.1783 |

## Main interpretation

For taboo-specific judgements:
- lexical identity explains most of the stable structure;
- a community main effect remains detectable;
- the community contribution is modest relative to item differences.

This supports a **stable-core + contextual-modulation** framing rather than an
all-universal or all-relative framing.

## Centered community effects

The fitted effects are on the dataset's normalized 0–1 rating scale and are
centered for readability. They should not be ranked as intrinsic properties of
countries because sample composition, rating behavior and aggregation differ.

### Tabooness
- AU: -0.0084
- CA: +0.0130
- GB: -0.0021
- SG: -0.0051
- US: -0.0008

### Offensiveness
- AU: -0.0139
- CA: +0.0081
- GB: +0.0094
- SG: -0.0029
- US: -0.0002

These small main effects can coexist with larger **item-specific community
differences**, which are a later target.

## Important negative finding

Community is much more explanatory for concreteness (partial R² ≈ .21) than
for tabooness/offensiveness (~.03).

This warns against interpreting any cross-community rating difference as
specifically about taboo culture: general semantic/rating behavior can vary
across samples too.

A stronger taboo-specific test should therefore compare taboo dimensions
against non-taboo rating dimensions and/or matched neutral controls.

## Next model

The next confirmatory version should add:
- item × ontology-domain interactions;
- sample reliability / uncertainty weights where defensible;
- matched non-taboo controls;
- community-specific residual diagnostics;
- sensitivity to only items shared by 3+, 4+, and all 5 English communities.

The strongest claim available at this stage is:

> taboo judgements are highly item-structured and measurably, but modestly,
> community-modulated in the English repeated-item subset.
