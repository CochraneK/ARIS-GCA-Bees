# Model recoverability pilot · ARIS4C008

**Status:** toy simulation for design decisions, not a power analysis and not evidence about real animal evolution.

## Question

Can the planned cross-species panel distinguish three causal architectures under realistic pilot conditions?

- **additive:** advanced outcomes track average module level;
- **weakest-link:** the lowest critical module constrains performance;
- **threshold:** advanced outcomes emerge when enough modules cross a threshold.

The simulation used eight latent modules, correlated trait values, measurement noise (SD 0.08), 20% or 40% cell missingness with mean imputation, and four-fold cross-validation. Each cell is based on 50 seeded replicates.

## Main result

With **25 taxa and 20% missingness**, selecting taxa to maximize disagreement among the candidate models improved mean exact architecture recovery from **0.447 to 0.587**.

For the mechanisms most central to 008:

- threshold recovery: **0.30 → 0.50**;
- weakest-link recovery: **0.36 → 0.56**.

With **40 taxa and 20% missingness**:

- threshold recovery: **0.16 → 0.46**;
- weakest-link recovery: **0.30 → 0.50**.

At **40% missingness**, performance remains unstable. This is a direct warning that simply increasing the number of famous species will not rescue a sparse behaviour matrix.

## Design decision

The pilot panel should be optimized for **model discrimination**, not prestige, familiarity, or phylogenetic distance alone.

The sampling algorithm should seek taxa whose module configurations make the models disagree. Examples of especially informative configurations include:

- high mean module score with one severe bottleneck;
- modest mean score with no severe bottleneck;
- many modules just below versus just above the hypothesized threshold;
- similar cognition with very different manipulation / externalization;
- similar social transmission with very different life history or network structure.

## Consequences

1. The current 25-taxon scaffold is a **seed**, not the final panel.
2. We should add negative/calibration taxa specifically to occupy missing configuration cells.
3. Missingness above roughly 20–30% in critical modules is a design threat, not merely an inconvenience.
4. The multiplicative/geometric-mean model was highly confounded with additive structure in earlier toy runs and should remain exploratory until richer data are available.
5. Confirmatory inference should emphasize falsification contrasts and independent evolutionary origins rather than a single omnibus regression.

## Reproducibility

The exact simulation logic is stored in `code/simulate_model_recoverability.py`; summary output is in `data/model_recoverability_summary.csv`.
