# ARIS4C007 · Pilot 4 phylogenetic comparative plan

Last updated: 2026-09-19

## Goal

Once the molecular axis is technically stable, test whether cross-method age-equivalence disagreement is structured by shared ancestry and life-history traits rather than treating species as independent observations.

## Primary phylogeny

**Upham, Esselstyn & Jetz (2019), PLOS Biology — Mammalia credible tree sets.**

Primary source:
- VertLife / Dryad DOI `10.5061/dryad.tb03d03`
- 5,911-species completed mammal phylogenies
- time-scaled branch lengths
- posterior/credible sets propagate both topological and node-age uncertainty

### Mandatory rule

Do **not** use one completed maximum-clade-credibility tree as the sole inferential tree.

Upham et al. explicitly caution that completed trees contain 1,813 species without DNA whose placements vary within taxonomic constraints. For inferential analyses, ARIS4C007 will use a sampled distribution of trees.

## Confirmatory tree strategy

### Primary
Use a deterministic sample of **100 completed NDexp posterior trees**.

For every comparative model:
1. prune each tree to the exact analysis species set;
2. fit the same model independently on each tree;
3. retain coefficient, SE/CI, phylogenetic parameter and model diagnostics;
4. pool/describe estimates across trees;
5. report both within-tree uncertainty and between-tree phylogenetic uncertainty.

### Sensitivity
- DNA-only tree subset where taxonomic overlap is adequate;
- FBD-dated alternative tree family;
- PHYLACINE 1.2 posterior tree set as a taxonomic/phylogenetic robustness source where useful.

## Taxonomic reconciliation

Before modelling:
- preserve original source species names;
- build an explicit synonym/canonical-name crosswalk;
- never silently fuzzy-match scientific names;
- record unmatched taxa;
- record whether a tip is sequence-supported vs phylogenetically imputed if upstream metadata allow.

Primary reconciliation target is the Upham/MamPhy taxonomy.

## Outcomes

Candidate species-level outcomes:
- Pilot 0 A1–A3 disagreement by life stage;
- held-out Pilot 2 A1/A3/A4 error summaries;
- Pilot 1 demographic-event coherence residuals;
- molecular Clock2/3 residual/disagreement once Pilot 3C is complete;
- integrated CSAD / method-dispersion summaries.

The unit of phylogenetic modelling is species or species × prespecified life stage, never individual event rows treated as independent species replicates.

## Predictors

Prespecified predictors:
- log body mass;
- gestation duration;
- sexual-maturity timing;
- maximum lifespan;
- longevity-record sample-size/confidence;
- domestication status where available;
- broad diet/ecology covariates only after source harmonization;
- taxonomic order as descriptive stratification, not a replacement for phylogeny.

Avoid entering mathematically redundant predictors together without collinearity diagnostics.

## Models

### P1 — phylogenetic signal
Estimate phylogenetic signal in disagreement/error outcomes:
- Pagel's lambda;
- descriptive Blomberg's K where assumptions are reasonable.

### P2 — PGLS
Example conceptual model:

`CSAD ~ log(body_mass) + maturity_fraction + gestation_fraction + longevity_quality`

Fit across the posterior tree set.

### P3 — stage interaction
Where coverage supports it:

`disagreement ~ life_stage * life_history_predictor + phylogenetic_error`

Use a model that respects repeated stage observations per species; do not run ordinary row-level OLS.

### P4 — leave-one-order-out generalization
Prediction models must be evaluated with entire taxonomic orders held out.

Random species splitting can be reported only as a secondary optimistic benchmark.

## Maximum-longevity bias

Maximum longevity is a record statistic, not an error-free species constant.

Mandatory sensitivity:
- AnAge confidence qualifier;
- AnAge sample-size class;
- exclude `tiny` longevity records;
- high/acceptable-quality subset;
- Lu-style 1.3× non-human/non-mouse correction;
- clock-era vs current AnAge trait snapshots;
- alternative robust survival-derived longevity denominator where available.

## Alternative longevity concept

Cagan et al. (2022) used the age by which 80% of adults had died for species with deep individual survival records, reducing sensitivity to single extreme longevity records.

ARIS4C007 will treat this as a robustness concept for data-rich subsets, not impute it to species lacking life tables.

## Data-source priorities

1. Upham et al. 2019 / VertLife posterior mammal trees.
2. PHYLACINE 1.2 taxonomy + posterior phylogeny as sensitivity / synonym support.
3. Current AnAge traits + quality/sample-size fields.
4. Myhrvold et al. life-history data for trait completion.
5. PanTHERIA / PHYLACINE ecological covariates only when construct definitions match.

## Gate

**Pilot 4 passes** only if:
- >=80% of the intended species-level primary outcome set is reconciled to phylogeny tips, or a principled narrower set is declared;
- the main qualitative coefficient conclusions are not artifacts of one phylogenetic tree;
- leave-one-order-out results are reported for learned/predictive models;
- maximum-longevity quality sensitivity is explicit.

## Handoff

Do not start a latent common-age model merely because a PGLS coefficient is significant. Pilot 4 is for dependence correction and mechanism exploration; dimensionality of biological age remains an empirical question.
