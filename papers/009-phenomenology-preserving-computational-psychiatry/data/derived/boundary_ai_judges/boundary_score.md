# ARIS4C009 · AI boundary calibration summary

## Strategy usability

| Condition | Target words | N | rated_judge_04__gpt-oss-120b | rated_judge_05__nemotron-3-ultra | rated_judge_06__stepfun-3.7-flash | Majority usable | Unanimous usable | Majority modified | Unanimous modified |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| A | 40 | 60 | 0.75 | 0.8 | 0.95 | 0.9167 | 0.6167 | 0.0833 | 0.0333 |
| B | 20 | 60 | 0.7333 | 0.7667 | 0.85 | 0.8167 | 0.6167 | 0.1833 | 0.0833 |

## Multi-model agreement

| Field | N | Judges | Percent agreement | Gwet AC1 |
|---|---:|---:|---:|---:|
| coherent_boundary | 120 | 3 | 0.8111 | 0.7425 |
| sufficient_nontrivial | 120 | 3 | 0.9556 | 0.9525 |
| mixed_unrelated_topics | 120 | 3 | 0.9389 | 0.934 |
| recommended_action | 120 | 3 | 0.7694 | 0.7416 |

## Pairwise model agreement

| Field | Judge pair | N | Percent agreement | Gwet AC1 |
|---|---|---:|---:|---:|
| coherent_boundary | rated_judge_04__gpt-oss-120b__rated_judge_05__nemotron-3-ultra | 120 | 0.775 | 0.6764 |
| coherent_boundary | rated_judge_04__gpt-oss-120b__rated_judge_06__stepfun-3.7-flash | 120 | 0.8167 | 0.7539 |
| coherent_boundary | rated_judge_05__nemotron-3-ultra__rated_judge_06__stepfun-3.7-flash | 120 | 0.8417 | 0.7924 |
| sufficient_nontrivial | rated_judge_04__gpt-oss-120b__rated_judge_05__nemotron-3-ultra | 120 | 0.9417 | 0.9361 |
| sufficient_nontrivial | rated_judge_04__gpt-oss-120b__rated_judge_06__stepfun-3.7-flash | 120 | 0.9833 | 0.9828 |
| sufficient_nontrivial | rated_judge_05__nemotron-3-ultra__rated_judge_06__stepfun-3.7-flash | 120 | 0.9417 | 0.9371 |
| mixed_unrelated_topics | rated_judge_04__gpt-oss-120b__rated_judge_05__nemotron-3-ultra | 120 | 0.9417 | 0.935 |
| mixed_unrelated_topics | rated_judge_04__gpt-oss-120b__rated_judge_06__stepfun-3.7-flash | 120 | 0.9083 | 0.8995 |
| mixed_unrelated_topics | rated_judge_05__nemotron-3-ultra__rated_judge_06__stepfun-3.7-flash | 120 | 0.9667 | 0.9655 |
| recommended_action | rated_judge_04__gpt-oss-120b__rated_judge_05__nemotron-3-ultra | 120 | 0.7167 | 0.6749 |
| recommended_action | rated_judge_04__gpt-oss-120b__rated_judge_06__stepfun-3.7-flash | 120 | 0.7667 | 0.7245 |
| recommended_action | rated_judge_05__nemotron-3-ultra__rated_judge_06__stepfun-3.7-flash | 120 | 0.825 | 0.8074 |

## Per-field "yes" rate by blinded strategy

Higher is better for `coherent_boundary` and `sufficient_nontrivial`; lower is better for `mixed_unrelated_topics`.

| Condition | Field | Target words | rated_judge_04__gpt-oss-120b | rated_judge_05__nemotron-3-ultra | rated_judge_06__stepfun-3.7-flash |
|---|---|---:|---:|---:|---:|
| A | coherent_boundary | 40 | 0.8 | 0.85 | 0.95 |
| A | sufficient_nontrivial | 40 | 1.0 | 0.9667 | 1.0 |
| A | mixed_unrelated_topics | 40 | 0.1 | 0.0167 | 0.0167 |
| B | coherent_boundary | 20 | 0.8 | 0.8 | 0.85 |
| B | sufficient_nontrivial | 20 | 0.95 | 0.9 | 0.9833 |
| B | mixed_unrelated_topics | 20 | 0.0667 | 0.0333 | 0.0 |

## Modified-action (merge/split/reject) rate per judge

| Condition | Target words | rated_judge_04__gpt-oss-120b | rated_judge_05__nemotron-3-ultra | rated_judge_06__stepfun-3.7-flash |
|---|---:|---:|---:|---:|
| A | 40 | 0.25 | 0.2 | 0.05 |
| B | 20 | 0.2667 | 0.2333 | 0.15 |

## Ensemble failure flags and realised window size (regular items)

| Condition | Target words | N | Majority usable | Unanimous usable | Majority modified | Unanimous modified | ≥majority fail on coherent_boundary | ≥majority fail on sufficient_nontrivial | ≥majority fail on mixed_unrelated_topics | Realised participant words |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| A | 40 | 60 | 0.9167 | 0.6167 | 0.0833 | 0.0333  | 0.0833 | 0.0 | 0.0167 | median 88.0, range 40-229 |
| B | 20 | 60 | 0.8167 | 0.6167 | 0.1833 | 0.0833  | 0.1333 | 0.0333 | 0.0333 | median 76.0, range 20-231 |

## Stress stratum, descriptive only

These windows are excluded from the primary comparison. They sample below-target tails and
>250-word windows, so a usable rate that collapses here is the rubric working as intended.

| Condition | Target words | N | Majority usable | Unanimous usable | Majority modified | Unanimous modified | ≥majority fail on coherent_boundary | ≥majority fail on sufficient_nontrivial | ≥majority fail on mixed_unrelated_topics | Realised participant words |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| A | 40 | 10 | 0.5 | 0.4 | 0.5 | 0.2  | 0.2 | 0.3 | 0.1 | median 254.0, range 0-606 |
| B | 20 | 10 | 0.6 | 0.2 | 0.4 | 0.2  | 0.3 | 0.1 | 0.1 | median 275.0, range 0-501 |

## Judge response behaviour on regular items

| Judge | Mean confidence (1-5) | Note written | Confidence value counts |
|---|---:|---:|---|
| rated_judge_04__gpt-oss-120b | 3.975 | 1.0 | 3x3, 4x117 |
| rated_judge_05__nemotron-3-ultra | 4.0333 | 1.0 | 2x1, 3x7, 4x99, 5x13 |
| rated_judge_06__stepfun-3.7-flash | 3.95 | 1.0 | 3x11, 4x104, 5x5 |

## Leave-one-judge-out sensitivity (full agreement within each reduced ensemble)

With two remaining judges, majority and unanimous consensus coincide; these columns are
the strict-agreement view and test whether the strategy ordering depends on one family.

| Ensemble | Condition | Target words | N | Strict usable | Strict modified |
|---|---|---:|---:|---:|---:|
| without_rated_judge_04__gpt-oss-120b | A | 40 | 60 | 0.7833 | 0.0333 |
| without_rated_judge_04__gpt-oss-120b | B | 20 | 60 | 0.7333 | 0.1167 |
| without_rated_judge_05__nemotron-3-ultra | A | 40 | 60 | 0.7333 | 0.0333 |
| without_rated_judge_05__nemotron-3-ultra | B | 20 | 60 | 0.6833 | 0.1 |
| without_rated_judge_06__stepfun-3.7-flash | A | 40 | 60 | 0.6333 | 0.0833 |
| without_rated_judge_06__stepfun-3.7-flash | B | 20 | 60 | 0.6333 | 0.1333 |

## Interpretation boundary

This is an automated engineering boundary-calibration result only. It does not establish
human interpretability, clinician agreement, phenomenological validity, disease effects,
or fidelity of any downstream representation.
