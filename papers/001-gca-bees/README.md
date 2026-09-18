# ARIS4C001 · Bee Uncertainty × Cognitive Covariation

## Canonical question

Do honey bees show a common latent cognitive structure linking cross-task learning performance to uncertainty-sensitive decisions, or can the observed behaviors be explained more parsimoniously by domain-specific and associative mechanisms?

This directory is the complete replacement for the legacy Paper 001. The old simulation-based claims are not part of the current main-branch paper. They remain recoverable only through Git history.

## Why the reconstruction was necessary

The legacy study generated several outcomes from the same hand-specified latent precision variable and then treated the induced covariance as support for that variable. It also described manually chosen beta distributions as empirical fitting and reported a grid-search optimum as an analytical biological constant. Those practices are not retained.

The reconstructed paper starts from observed evidence:

- Perry & Barron (2013) showed difficulty-sensitive opt-out behavior in honey bees, while explicitly preserving an associative-learning alternative.
- Finke et al. (2023) found positive individual consistency across several honey-bee learning tasks, but not every pairwise relation was significant.
- Peñaherrera-Aguirre et al. (2024) reanalyzed those learning-task correlations and reported candidate GCA factors explaining 46.8% and 52.3% of variance in visual and olfactory conditions.
- Chittka et al. (2025) reviewed insect consciousness and described the metacognition interpretation as plausible but still compatible with learned-association accounts.
- Bridges et al. (2024) concerns complex social learning; it is no longer used as evidence of tool use or self-awareness.

## Confirmatory model family

The primary empirical comparison is deliberately mechanism-neutral:

1. **M1 — one general factor:** all learning and uncertainty indicators load on one latent factor.
2. **M2 — two correlated factors:** learning indicators load on a learning/GCA factor; uncertainty indicators load on an uncertainty-control factor; their correlation is estimated.
3. **M3 — two independent factors:** the same two-factor structure with zero latent correlation.
4. **M4 — task-local associative model:** trial-level opt-out behavior is predicted from stimulus difficulty, reinforcement history, response value and decision noise without invoking metacognitive access.
5. **Exploratory precision model:** evaluated only after empirical identification; it cannot be supported merely because variables were generated from a shared simulated parameter.

## Current status

This is a **research design**, not a completed empirical result. The published literature establishes that both cross-task covariation and difficulty-sensitive opt-out behavior exist, but it does not currently provide the same-individual dataset needed to identify their latent coupling.

See:

- process/STATUS.md
- process/RESEARCH_PLAN.md
- process/EVIDENCE_MAP.md
- process/ADVERSARIAL_AUDIT.md
- process/MODEL_SPEC_LOCK.json
- manuscript/DRAFT.md
- code/model_recovery.py

The synthetic model-recovery file is a feasibility check only. It is never interpreted as evidence about bees.
