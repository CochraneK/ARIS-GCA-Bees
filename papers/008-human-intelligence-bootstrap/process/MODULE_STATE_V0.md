# Module evidence-state v0 · coverage diagnostic

This is the first direct implementation of the condition ontology across the 29-species v2 panel.

## Coding distinction

- **A–F behavioural/social modules:** positive / positive-with-uncertainty / tested-negative / ambiguous / not-tested.
- **G–H quantitative constraint modules:** measured / partial / not measured. A long lifespan or high metabolic value is not itself a "positive" state.
- **I–J ecology/demography:** currently marked not-systematically-joined; this is a data-engineering gap, not biological absence.

## Current state counts

- **A · generative_cognition:** not_tested=28, positive=1
- **B · social_transmission:** not_tested=18, positive=11
- **C · communication:** not_tested=21, positive=8
- **D · manipulation_embodiment:** not_tested=26, positive=3
- **E · externalization:** not_tested=29
- **F · social_architecture:** not_tested=24, positive=5
- **G · life_history_learning_opportunity:** measured=24, not_measured=5
- **H · energetics_neural_budget:** measured_multi_axis=3, partial_measured=15, not_measured=11
- **I · ecological_challenge_opportunity:** not_systematically_joined=29
- **J · demography_cultural_population:** not_systematically_joined=29

## Interpretation

This diagnostic shows that the current project is **not yet allowed** to fit a 10-module confirmatory threshold/weakest-link model. The evidence seed is intentionally sparse outside social transmission, selected manipulation/communication cases, life history and neural/energetic proxies.

The correct next action is targeted gap-filling, especially:
- A generative cognition;
- C communication;
- D manipulation across ordinary/calibration taxa;
- E persistent externalization;
- F social architecture;
- I ecology;
- J cultural demography.

Crucially, "not tested" remains missing and is never converted to zero.
