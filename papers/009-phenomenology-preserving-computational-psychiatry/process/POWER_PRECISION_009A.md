# ARIS4C009A · Power and precision sensitivity analysis

**Status:** synthetic design engineering only.  
**Not:** an empirical estimate of effect size or a frozen sample-size decision.

## Why a single conventional power calculation is inappropriate

009A does not have one independent Bernoulli observation per participant.

The data are crossed and nested across:

- participant;
- episode;
- query;
- representation;
- evaluator.

The confirmatory model is hierarchical. Before real pilot data exist, the honest question is therefore:

> Under plausible ranges of representation differences and evaluator heterogeneity, how quickly does design precision improve as participants, episodes and benchmark queries increase?

## Engineering proxy

The script:

`code/power_precision_simulation.py`

simulates two representations corresponding roughly to an expert phenomenological representation (R2) and a self-report abstraction (R3).

It includes random heterogeneity at:

- participant level;
- episode level;
- query level;
- representation-specific evaluator level.

Because different evaluators may see different representations of the same episode, evaluator effects do **not** cancel perfectly.

The script then aggregates to a participant-level paired difference and uses a two-sided normal threshold as a transparent **proxy** for power.

This is intentionally simpler than the final hierarchical logistic analysis and must be replaced/calibrated after a real pilot supplies variance components.

## Default sensitivity scenario

The default engineering scenario uses:

- 2 focal episodes per participant;
- 15 adjudicable benchmark queries per episode;
- baseline R3 accuracy = 0.68 before random heterogeneity;
- participant logit SD = 0.60;
- episode logit SD = 0.50;
- query logit SD = 0.70;
- evaluator logit SD = 0.80;
- seed = 20260918.

Candidate target differences are varied rather than assumed true:

- +0.03;
- +0.05;
- +0.075;
- +0.10.

Because logistic-normal mixing attenuates probability differences, the realized average contrast is smaller than the nominal input delta.

## One reproduced sensitivity slice

Using 250 Monte Carlo replicates, the following values are design-sensitivity outputs, not empirical findings.

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

The exact Monte Carlo estimates vary with replicate count and assumptions.

## Design implication

The simulation makes one point that should survive parameter changes:

**participant count alone does not determine information.**

Precision also depends strongly on:

- how many independent focal episodes are obtained per participant;
- how many questions are genuinely adjudicable rather than redundant;
- evaluator variance;
- source ambiguity;
- representation × domain interactions.

Under the deliberately noisy default scenario:

- a small ~5 percentage-point nominal difference is difficult to estimate precisely without a relatively large sample;
- a ~7.5 percentage-point difference becomes detectable much earlier;
- a ~10 percentage-point difference can be detected in considerably smaller samples.

This should **not** be converted into “009 needs N = X” yet.

## What the real pilot must estimate

Before freezing confirmatory N, obtain empirical estimates of:

1. participant-level variance;
2. episode-level variance;
3. query-level variance;
4. evaluator-level variance;
5. missing/indeterminate query rate;
6. within-episode query correlation;
7. representation × phenomenological-domain interaction;
8. realized semantic-fidelity contrast.

Then refit the simulation to those values.

## Precision-first rule

The final sample size should be selected to achieve acceptable interval width for the primary R2-versus-R3 contrast and key domain interactions, not merely 80% rejection probability.

The preregistration should report both:

- simulated rejection probability;
- expected interval precision.

## Sensitivity grid required before registration

At minimum vary:

- participants: 30–200;
- episodes/person: 1–4;
- usable queries/episode: 8–30;
- nominal primary contrast: 0.03–0.12;
- evaluator logit SD: 0.3–1.2;
- indeterminate/missing query fraction: 0–30%.

No single scenario should be presented as the truth before pilot calibration.

## Stop rule

If pilot estimates imply that the required confirmatory sample is infeasible, do **not** weaken the fidelity metric to manufacture power.

Instead, consider:

- increasing repeated episodes or independent queries where scientifically justified;
- narrowing the primary representation contrast;
- improving evaluator calibration;
- redesigning the study as an estimation-focused feasibility paper.
