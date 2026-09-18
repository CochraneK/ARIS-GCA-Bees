# ARIS4C009A1 · Power and precision sensitivity analysis

**Status:** synthetic design engineering only.  
**Not:** an empirical effect estimate or final sample-size decision.

## Why conventional single-level power is inappropriate

009A1 observations are crossed/nested across:

- participant;
- episode;
- query;
- representation;
- evaluator.

The confirmatory analysis is hierarchical.

Before pilot variance estimates exist, the purpose of simulation is sensitivity analysis, not declaring N.

## Engineering proxy

The script:

`code/power_precision_simulation.py`

simulates a contrast roughly corresponding to:

- **R2:** specialist phenomenological representation;
- **R3P:** questionnaire-format projection generated from the same source.

R3P is **not participant self-report**.

The simulation includes random heterogeneity at:

- participant;
- episode;
- query;
- representation-specific evaluator.

A participant-level paired contrast is used only as a transparent engineering approximation.

## Default synthetic scenario

- 2 focal episodes/person;
- 15 adjudicable queries/episode;
- baseline R3P reconstruction accuracy = 0.68 before heterogeneity;
- participant logit SD = 0.60;
- episode logit SD = 0.50;
- query logit SD = 0.70;
- evaluator logit SD = 0.80;
- seed = 20260918.

Nominal input differences:

- +0.03;
- +0.05;
- +0.075;
- +0.10.

Because logistic-normal mixing attenuates probability differences, realized mean contrasts are smaller.

## Reproduced sensitivity slice

Using 250 Monte Carlo replicates:

| Nominal delta | Participants | Proxy power | Mean realized difference |
|---:|---:|---:|---:|
| 0.05 | 30 | 0.260 | 0.0410 |
| 0.05 | 60 | 0.396 | 0.0403 |
| 0.05 | 80 | 0.532 | 0.0393 |
| 0.05 | 120 | 0.724 | 0.0409 |
| 0.05 | 160 | 0.860 | 0.0423 |
| 0.075 | 30 | 0.500 | 0.0600 |
| 0.075 | 60 | 0.796 | 0.0658 |
| 0.075 | 80 | 0.908 | 0.0641 |
| 0.075 | 120 | 0.968 | 0.0611 |
| 0.10 | 30 | 0.768 | 0.0852 |
| 0.10 | 60 | 0.976 | 0.0853 |
| 0.10 | 80 | 0.984 | 0.0842 |

These are synthetic engineering outputs.

## Design implication

Participant count alone does not determine information.

Precision depends on:

- episodes/person;
- genuinely independent adjudicable queries;
- evaluator variance;
- source ambiguity;
- missing/indeterminate fraction;
- query redundancy;
- representation × domain interactions.

Under the deliberately noisy default scenario:

- ~5 percentage-point nominal contrasts require relatively large samples for stable detection;
- ~7.5-point contrasts stabilize earlier;
- ~10-point contrasts can be detected with substantially smaller samples.

Do not convert this into a final N.

## Pilot parameters required

Estimate empirically:

1. participant variance;
2. episode variance;
3. query variance;
4. evaluator variance;
5. query redundancy/effective query count;
6. missing/indeterminate rate;
7. domain interactions;
8. realized R2–R3P contrast;
9. representation-rate distribution.

Then rerun the simulation.

## Precision-first rule

Final N should target:

- acceptable interval width for primary contrasts;
- adequate precision for key representation × domain interactions.

Report both simulated rejection probability and expected interval precision.

## Required sensitivity grid

At minimum vary:

- participants: 30–200;
- episodes/person: 1–4;
- usable nonredundant queries/episode: 8–30;
- nominal contrast: 0.03–0.12;
- evaluator logit SD: 0.3–1.2;
- missing/indeterminate fraction: 0–30%.

## Stop rule

If pilot-calibrated requirements are infeasible:

- do not weaken fidelity definitions merely to gain power;
- consider more independent episodes;
- improve evaluator calibration;
- narrow confirmatory contrasts;
- redesign as an estimation/feasibility study.
