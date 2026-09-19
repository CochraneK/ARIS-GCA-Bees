# ARIS4C017 · LING-02 Research Plan v0.1

## Working question

Can the empirical constraint structure of human language predict typological configurations that were hidden from the model, and can that validated predictive structure be used to identify plausible versus structurally unsupported regions of language space?

## Relation to ARIS4C002 / LING-01

ARIS4C002 tested a strong, simple periodic-table hypothesis: a global circular organization of language structure. That form was not supported.

ARIS4C017 is not a rescue of the rejected circle. It changes the target from **recovering one global geometry** to **predicting held-out configurations under competing constraint models**.

Reusable assets from 002 may include cleaned typological matrices, family-aware splitting logic, model-comparison infrastructure, and lessons about leakage. They must be revalidated for the new prediction target.

## Prediction ladder

### P1 · Held-out observed languages — primary

Hide complete languages from model fitting and predict their typological features/configurations.

Required split families:

- ordinary held-out languages;
- language-family-held-out;
- macroarea-held-out where coverage supports it.

This is the principal falsification layer.

### P2 · Masked feature cells and feature bundles — primary

Mask individual features and prespecified multi-feature bundles within observed languages, then predict them from the remaining structure.

Evaluate both accuracy and uncertainty calibration.

### P3 · Structural-empty-space prediction — secondary

After P1/P2 validity is established, score feature combinations that are absent from the observed sample.

The output is a graded support/compatibility estimate, **not** a declaration that an absent combination is impossible.

### P4 · Extinct-language proxy / historical holdout — tertiary

Only if sufficiently documented historical/ancient language profiles can be assembled independently, treat them as temporal/external holdouts.

Do not infer actual extinct languages from modern typological absence alone.

## Comparator families

No model family is privileged in advance. Candidate comparators should include, where feasible:

1. feature marginals / independence baseline;
2. family/geography priors;
3. hierarchical/tree-aware models;
4. latent-factor or low-dimensional models;
5. graph/dependency models;
6. nonlinear manifold models;
7. constraint / energy-style models.

A global circle may be included only as a historical comparator inherited from 002, not as the default ontology.

## Evaluation

Primary evaluation should emphasize predictive performance and calibration under hard splits.

Candidate metrics:

- held-out categorical log loss / cross-entropy;
- Brier score where probabilities are available;
- macro-averaged feature accuracy as a descriptive supplement;
- calibration error / reliability curves;
- ranking quality for held-out bundles;
- performance degradation from random → family-held-out → macroarea-held-out;
- uncertainty coverage for abstention or prediction sets.

## Main hypotheses

**H1. Predictive constraint:** multivariate structure predicts held-out typological features better than feature-frequency baselines.

**H2. Genealogical robustness:** at least part of the predictive gain survives family-held-out evaluation.

**H3. Configuration prediction:** models validated at P1/P2 rank true held-out feature bundles above matched pseudo-configurations.

**H4. Calibrated emptiness:** low-support empty-space combinations can be identified with calibrated uncertainty, rather than by raw absence alone.

## Falsifiers

The strong predictive-language-space idea should be weakened or rejected if:

- gains disappear under family-held-out splits;
- performance is explained by geography/family priors alone;
- models cannot beat simple marginal baselines on prespecified bundle prediction;
- empty-space scores are unstable across datasets/model families;
- confidence is badly miscalibrated;
- predictions fail on independent historical/external holdouts.

## Data strategy

Start from reusable 002 typological resources only after checking target leakage and dataset versions. Likely evidence layers include WALS/Grambank-derived matrices already used in 002 and any independently auditable historical typology source added later.

Do not merge datasets merely to maximize coverage; preserve source-specific analyses before harmonized synthesis.

## First bounded unit

1. inventory reusable 002 datasets/code;
2. define the exact prediction target schema;
3. create leakage-safe random/family/macroarea split manifests;
4. benchmark the marginal and family/geography baselines;
5. freeze a Pilot-0 result table before exploring richer models.
