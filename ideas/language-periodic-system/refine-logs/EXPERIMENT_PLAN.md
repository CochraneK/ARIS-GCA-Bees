# Experiment Plan · Language Periodic System

**Status:** pre-review draft. This plan implements the cheapest discriminating tests before any expensive or elaborate periodic model.

## Problem Anchor

Test whether cross-linguistic structural relations exhibit a **recurrent/periodic geometry with out-of-sample predictive value** beyond non-periodic alternatives. Do not widen the claim to “discovering linguistic atoms” or “building the definitive periodic table.”

## Claim ladder

### C0 · Structural signal exists
Already screened in Stage-0: real TLI data are more compressible than a feature-wise shuffle null and contain a tail of residual associations.

### C1 · A low-capacity periodic model predicts held-out structural relations
A circular model trained on one subset of languages predicts feature-feature association structure in held-out languages better than a constant/null baseline.

### C2 · Periodic structure adds value beyond ordinary alternatives
Circular/periodic models outperform or provide complementary predictive value to Euclidean low-rank, hierarchical/tree, and graph-distance baselines with comparable effective complexity.

### C3 · The effect generalizes beyond genealogy/area
Any advantage survives family-held-out evaluation and geography-aware sensitivity analysis.

### C4 · Periodicity is stable enough to interpret
Feature ordering / angular positions are reproducible across bootstrap samples and, if global C2 fails, any local periodic modules are pre-specified or discovered on train data and validated independently.

Only C3–C4 would justify a strong “periodic system” interpretation.

## Stage 1A · Held-out association prediction

### Data
- TLI statistical densified-small as primary screen.
- Use features with adequate joint coverage and bounded cardinality.
- Preserve original missingness for pairwise association calculations; do not let mode imputation define the target association matrix.

### Target
For each train/test split, estimate pairwise normalized mutual information (NMI) among selected linguistic features separately in train and test languages. A structural model sees only the train association matrix and predicts test association strengths.

### Competing models

1. **Null / constant:** predict the training mean association for all pairs.
2. **Euclidean low-rank:** truncated eigendecomposition / low-rank reconstruction of the train similarity matrix.
3. **Hierarchical/tree:** agglomerative linkage on train dissimilarities; convert cophenetic distance back to predicted similarity by calibration fitted on train pairs.
4. **Graph-distance:** k-nearest-neighbor feature graph from train associations; shortest-path/diffusion distance calibrated to similarity.
5. **Circular periodic:** infer one angular coordinate per feature from a two-dimensional spectral embedding; predict association as a smooth function of wrapped angular distance.

No model may use test associations for fitting hyperparameters. Hyperparameters are selected by nested validation among train-language resamples or train feature pairs.

### Metrics
- pairwise Pearson/Spearman correlation between predicted and held-out NMI;
- RMSE / MAE on held-out NMI;
- rank performance among strongest held-out associations;
- bootstrap confidence intervals for pairwise model differences.

### Split hierarchy

1. **Random language split** — screening only; easiest case and likely optimistic.
2. **Family-held-out split** — use Glottolog `Family_ID`; entire top-level families assigned to test where sample size permits.
3. **Geographic block split** — later confirmatory sensitivity analysis using coordinates/regions.

A model that wins only under random splits does not support the paper's substantive claim.

## Stage 1B · Stability / recurrence test

For the circular model:

- refit on bootstrap language samples;
- align angles modulo rotation/reflection;
- quantify circular rank/order stability;
- test whether neighboring feature relations recur across held-out families;
- compare against order stability obtained from shuffled or family-preserving nulls.

This is required because a circle can always be fit to points; the research question is whether the **ordering is reproducible**.

## Stage 1C · Topology sanity check

Persistent homology may be used only as a supporting diagnostic because Port et al. already established this line of work.

Use it to ask whether train-derived feature clouds show stable H1 structure across bootstrap samples and datasets. Do not interpret the existence of an H1 class as periodicity by itself.

## Stage 2 · Replication and stronger controls

Proceed only if Stage 1 produces a non-trivial discriminating signal.

- replicate on GBI / Grambank morphosyntax;
- separate grammar, phonology, and colexification subsets where source metadata permit;
- fit toroidal or multi-cycle models only if a single circular model leaves structured residuals;
- compare with more flexible manifold methods under held-out evaluation;
- incorporate phylogenetic covariance or family-block bootstrap rather than treating languages as IID.

## Missing-cell prediction

This is an optional late-stage experiment, not an initial selling point.

If a validated model provides calibrated probabilities for feature configurations, perform historical/artificial hold-out experiments first: remove attested configurations or languages and test whether the model recovers them. Only then discuss truly unattested but high-probability “missing cells.”

## Stage-1 stop/go criteria

### GO
Continue toward a numbered paper if at least one periodic model:
- clearly beats the null on held-out data;
- remains competitive with non-periodic models under fair capacity control;
- shows reproducible ordering/topology across resamples; and
- retains meaningful signal in at least a family-held-out analysis.

### REFRAME
If graph/manifold/tree models consistently beat periodic models but prediction remains strong, reframe toward **the geometry of linguistic design space** and use the periodic-table hypothesis as the historical question being rejected.

### STOP
Park the candidate if all structured models barely beat null once family/area leakage is removed, or if the circular result is unstable across bootstrap samples.

## Immediate run order

1. Implement Stage 1A random-split screen with 40–80 well-covered TLI features.
2. Add Glottolog family metadata and family-held-out split.
3. Inspect model-pair differences and angular stability.
4. Only after these results, decide whether torus/TDA/replication experiments are warranted.
