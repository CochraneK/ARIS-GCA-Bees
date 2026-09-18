# ARIS4C006 · Pilot 10 — source-context split-half reliability

Last updated: 2026-09-18

## Verdict

**Source-level context does not pass the prospectively frozen standard for the primary confirmatory exposure.**

**Primary exposure is therefore downgraded to: field × prior-3-year lag window.**

Source × field × lag-window exposure remains available only as a shrunk secondary/exploratory moderator.

GitHub Actions run: `35300821340`  
Artifact: `aris4c006-source-reliability-pilot`

## Prospective decision rule

Before reading this artifact, `EXPOSURE_ESTIMATOR.md` froze the primary-source acceptance standard:

- >=16 eligible source contexts;
- split-half Pearson >=0.60;
- split-half Spearman >=0.60;
- median absolute half-sample difference <=0.15;
- 3+ author estimates must not qualitatively collapse.

The document also explicitly stated that the design should favor the coarser field-level exposure if source measurement is unstable.

## Results

- source contexts total: **24**
- eligible contexts: **24**
- split-half Pearson: **0.704**
- split-half Spearman: **0.156**
- median absolute half-score difference: **0.064**
- eligible 3+ author contexts: **23**
- 3+ author split-half Pearson: **0.796**
- 3+ author split-half Spearman: **0.083**

## Interpretation

The result has a clear structure:

1. Large differences are reproducible enough to generate a high Pearson correlation.
2. Rank ordering among the many near-zero / moderate source contexts is highly unstable.
3. The same pattern persists or strengthens in 3+ author works: high Pearson, very low rank correlation.
4. Therefore raw source-level exposure is not reliable enough to be the primary confirmatory moderator.

Examples illustrate the issue:

- strongly alphabetizing mathematics sources remain visibly high across halves;
- many medicine/engineering/business/psychology sources cluster near zero, where small sample fluctuations substantially reorder ranks;
- some contexts such as Sustainability and Physica A show large half-to-half differences.

## Protocol decision

The primary confirmatory context is frozen as:

**OpenAlex field × prior 3 complete publication years**

For focal year `t`:

`PrimaryExposure(field,t) <- chance-corrected alphabetization evidence from years t-3 ... t-1`

The estimator remains:
- tie-aware;
- chance-corrected;
- lagged;
- outcome-blind;
- independent of focal surname/career outcomes.

## Source-level role

`source × field × lag-window` may be retained only as:

- a hierarchically shrunk secondary exposure;
- an exploratory heterogeneity analysis;
- a sensitivity analysis focused on clearly high-information/high-alphabetization contexts.

Raw source scores cannot replace the field-level primary moderator based on which produces a stronger surname interaction.

## 3+ author robustness

The primary field-level exposure will be re-estimated using:
- all eligible multi-author works with exact chance correction;
- 3+ author works as mandatory robustness.

A main mechanism claim that exists only in two-author evidence is insufficient.

## Gate consequence

**Exposure granularity gate: PASS by narrowing.**

This is a successful ARIS outcome: the pilot rejected an unnecessarily fine-grained primary measurement layer before focal outcome inspection.
