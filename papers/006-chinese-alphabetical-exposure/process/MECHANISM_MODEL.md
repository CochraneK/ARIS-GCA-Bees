# ARIS4C006 · Mechanism model and alphabetical burden

Last updated: 2026-09-18

## Why absolute surname rank is not enough

A fixed Pinyin initial rank (A=1 ... Z=26) captures a scholar's broad structural vulnerability to alphabetical systems, but an author's actual position under alphabetical ordering depends on the surnames of the **specific coauthors on that work**.

ARIS4C006 therefore separates:

1. **Structural alphabetical vulnerability** — a stable author-level surname attribute.
2. **Within-team relative alphabetical rank** — a work-specific mechanical ordering attribute.
3. **Institutional alphabetization exposure** — a lagged context-level convention.
4. **Observed byline position** — the mechanism-proximal outcome.
5. **Downstream visibility/career outcomes** — secondary and identity-gated.

## 1. Structural vulnerability

Primary stable measure:

`InitialRank_i = 1,...,26`

using the validated Pinyin family-name initial.

Population-calibrated descriptive measures include:
- initial population share;
- cumulative population percentile by initial;
- exact surname population frequency when exact Chinese surname mapping is available.

This variable is **not treated as randomized**.

## 2. Within-team alphabetical rank

For an eligible work `w` with `n_w >= 2` validated family-name sort keys:

`RelAlphaRank_iw = (# coauthors with sort key strictly before i + tie adjustment) / (n_w - 1)`

Candidate tie rule:
- midrank among equal family-name keys.

Scale:
- 0 = alphabetically earliest in the team;
- 1 = alphabetically latest.

A binary alternative:
- `AlphaFirst_iw = 1` if focal surname would be first under alphabetical ordering.

These are determined from surname evidence and coauthor composition, not from actual listed position.

## 3. Observed position outcome

Candidate primary mechanism outcome:

`ListedPositionNorm_iw = (listed_position_iw - 1) / (n_w - 1)`

Scale:
- 0 = first listed;
- 1 = last listed.

This normalization is transparent across team sizes.

A binary `FirstListed_iw` is secondary unless the final multiplicity plan promotes it.

## 4. Independently measured convention exposure

`AlphaExposure_c,t-1`

is defined in `EXPOSURE_ESTIMATOR.md` from earlier / cross-fitted works, with exact chance correction and no focal-work leakage.

The exposure score cannot use the focal work's listed position.

## 5. Primary mechanism first-stage

A strong work-internal specification is:

`ListedPositionNorm_iw = WorkFE_w + beta1 RelAlphaRank_iw + beta2 RelAlphaRank_iw × AlphaExposure_c,t-1 + error_iw`

Because `AlphaExposure` is shared within the focal work, its main effect is absorbed by work fixed effects.

The focal mechanism parameter is `beta2`:

> does independently measured prior alphabetical convention make an author's within-team alphabetical rank more predictive of their actual listed position?

Advantages:
- controls all work-level topic/journal/year/team factors with work FE;
- does not compare scientific ability across surname groups;
- uses within-team variation;
- exposure is estimated from other/prior papers;
- directly validates the institutional mechanism before career outcomes.

This model is still not a general causal career model. Coauthor composition can be endogenous, but the first stage identifies whether the measured context convention translates surname order into listed position.

## 6. Structural-vulnerability model

A complementary work-level model retains the population-scale surname predictor:

`ListedPositionNorm_iw ~ InitialRank_i × AlphaExposure_c,t-1 + work/context controls + FE`

This answers a different question: whether scholars with broadly later Chinese surname initials receive later listed positions more strongly in higher-exposure settings.

It is weaker than the within-team model for mechanism identification and should not replace it.

## 7. Realized alphabetical burden

Define a measurement-only burden score:

`RealizedAlphaBurden_iw = RelAlphaRank_iw × AlphaExposure_c,t-1`

Candidate author-year prior burden:

`PriorBurden_it = weighted mean of RealizedAlphaBurden_iw over works before t`

Weights and aggregation are TBF and must be frozen before downstream outcomes.

This quantity is a realized combination of:
- context convention;
- team composition;
- surname position.

Because team/coauthor choice may itself be a behavioral response, `PriorBurden` is not an exogenous treatment.

## 8. Structural expected burden

To avoid conditioning all downstream analyses on realized collaborator choice, also define:

`StructuralBurden_it = InitialRank_i × AlphaExposure_it`

or a population-percentile analogue.

Comparison of structural and realized burden can separate:
- fixed surname vulnerability;
- context selection;
- coauthor/team adaptation.

## 9. Behavioral adaptation outcomes

Potential secondary mechanism outcomes:
- team size;
- probability of multi-authorship;
- distribution of coauthor surname positions;
- movement toward lower-alpha contexts;
- deviation from expected alphabetical order.

These are possible responses to exposure and therefore should not automatically be included as nuisance controls in downstream models.

## 10. Credit-allocation extension

An exploratory extension can compare evaluative credit rules on confirmed alphabetized works:

- equal fractional credit `1/n`;
- first-author / positional credit rules;
- other preregistered bibliometric allocation schemes.

The difference quantifies **evaluation-rule credit redistribution**, not actual intellectual contribution.

This extension is especially relevant because recent mathematics evidence indicates alphabetical order often coexists with approximately equal declared contributions. It must be framed as an evaluation-system simulation rather than evidence of unequal contribution.

## 11. Required validation sequence

1. Validate surname evidence.
2. Validate context exposure variance/reliability.
3. Run the work-FE first-stage mechanism model.
4. Only if the first stage behaves as predicted, consider frozen downstream outcomes.
5. Keep identity-intensive career models behind the separate person-resolution gate.

## Current decision

The within-team rank × independently measured exposure model is the preferred **mechanism-first** specification.

The paper should not lead with a raw `InitialRank -> citations/success` association.
