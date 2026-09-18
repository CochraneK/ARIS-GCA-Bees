# Module evidence-state v1 · standardized data integrations

This revision integrates standardized cross-species sources added after v0:
- MacLean et al. self-control tasks → A indicator coverage;
- global bird nest traits → E persistent-structure evidence;
- ASNR → F/J network measurements;
- EltonTraits → I ecology.

## Current counts

- **A · generative_cognition:** measurement coverage 4/29; states: not_tested=28, positive=1
- **B · social_transmission:** measurement coverage 0/29; states: not_tested=18, positive=11
- **C · communication:** measurement coverage 0/29; states: not_tested=21, positive=8
- **D · manipulation_embodiment:** measurement coverage 0/29; states: not_tested=26, positive=3
- **E · externalization:** measurement coverage 7/29; states: not_tested=22, positive=2, ambiguous=5
- **F · social_architecture:** measurement coverage 6/29; states: not_tested=24, positive=5
- **G · life_history_learning_opportunity:** measurement coverage 24/29; states: measured=24, not_measured=5
- **H · energetics_neural_budget:** measurement coverage 18/29; states: measured_multi_axis=3, partial_measured=15, not_measured=11
- **I · ecological_challenge_opportunity:** measurement coverage 26/29; states: measured_ecology=26, not_systematically_joined=3
- **J · demography_cultural_population:** measurement coverage 6/29; states: not_systematically_joined=23, measured_network_proxy=6

## Rules

Measurement coverage is not equivalent to a positive ability state. In particular:
- MacLean task scores remain task-specific proxies;
- ASNR network metrics remain interaction/context dependent;
- EltonTraits ecology variables are exposures/opportunities, not cognitive scores;
- bird nest `u` remains ambiguous and `NA` remains unavailable.

The matrix still contains substantial behavioural missingness and must not be zero-imputed.
