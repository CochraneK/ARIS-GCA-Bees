# ARIS4C009A · Preregistration-ready protocol

## Title

**How Much Lived Psychopathology Survives Quantification? A Blinded Benchmark of Representation Fidelity**

## Status

Protocol skeleton for preregistration. No participant data have been collected under this protocol.

## Primary question

When the **same source episode** is represented at progressively more compressed levels, how much source-grounded phenomenological structure can a blinded evaluator recover?

The study does not treat the source interview as the participant's complete inner reality. It treats it as the richest common evidential reference available to all representation conditions.

## Design summary

A within-episode, blinded reconstruction benchmark.

Each focal episode is transformed into multiple representations. Independent evaluators receive exactly one representation and answer a preregistered set of questions about the episode. Their answers are compared with a multi-anchor source adjudication.

### Core representation conditions

1. **R0 · Rich source record** — de-identified transcript segment, relevant interviewer prompts and contextual qualifiers.
2. **R1 · Structured phenomenological episode graph** — self, body, thought, other, world, time, space, affect, salience, agency, attribution, certainty and context, all with provenance.
3. **R2 · Specialist phenomenological coding** — trained-rater representation using the selected EASE/EAWE/STEP-compatible coding scheme.
4. **R3 · Self-report abstraction** — participant-completed or source-derived self-report representation using a frozen instrument.
5. **R4 · Conventional symptom abstraction** — conventional symptom/dimensional coding.
6. **R5 · Low-dimensional quantitative representation** — compact latent vector or summary with decoding instructions frozen before evaluation.

An LLM-assisted representation may be tested as exploratory but is not part of the human-only primary contrast unless preregistered before data access.

## Population

The initial benchmark domain is schizophrenia-spectrum / early-psychosis phenomenology because detailed phenomenological instruments and prior neurophenomenology are comparatively mature. This does not imply that the ontology generalizes unchanged to other disorders.

A clinically relevant comparison group and/or non-clinical participants may be included to test whether compression errors are psychopathology-specific rather than generic narrative compression.

## Unit structure

The analysis is multilevel:

- participant;
- focal episode;
- benchmark query or relation;
- representation;
- evaluator.

The number of observations is not equated with the number of participants.

## Source construction

For every focal episode preserve, subject to ethics and de-identification:

- participant wording;
- interviewer prompt;
- immediate context;
- temporal qualifiers;
- certainty/uncertainty;
- literal/metaphoric status when explicitly clarified;
- attribution;
- relevant medication, sleep, substance or acute-context information when consented;
- unresolved ambiguity;
- provenance pointer.

### Multi-anchor adjudication

The reference answer set is produced from:

1. the source record;
2. two independent trained raters;
3. adjudication of disagreement;
4. participant clarification where feasible and ethically appropriate.

Uncertainty and alternative interpretations are stored rather than forced into false certainty.

## Query bank

The benchmark query bank is frozen before representation evaluation and contains at least five classes.

### Q1 · Semantic content

Examples include agency, attribution, literal/metaphoric/uncertain status and affective valence.

### Q2 · Relations

Examples include self–thought, self–body, self–other, event–meaning, causation and salience–belief relationships.

### Q3 · Context

Questions test whether the representation preserves situational qualifiers and alternative explanations such as sleep, medication or ordinary experience.

### Q4 · Time

Questions test order, duration, recurrence and episodic versus trait-like status.

### Q5 · Participant-meaning checks

A subset of reconstructed descriptions is shown back to participants under a structured fidelity rubric when feasible.

## Primary endpoint

The primary family is **source-grounded semantic reconstruction fidelity** at the query level.

For categorical queries, the primary analysis uses correct/incorrect/indeterminate judgments against the adjudicated reference in a hierarchical model. The primary estimand is the representation-condition contrast in probability of a correct answer.

Semantic, relational, contextual, temporal and participant-endorsed fidelity remain separate. A scalar composite is not the primary endpoint because its weights would encode an unvalidated value judgment.

## Secondary endpoints

1. relation-level precision, recall and F1;
2. context-loss error;
3. temporal-order accuracy;
4. participant-endorsed reconstruction fidelity;
5. evaluator-confidence calibration;
6. inter-rater reliability;
7. representation length/dimensionality;
8. participant acquisition burden;
9. expert annotation burden;
10. computational burden.

## Core hypotheses

### H1 · Richness gradient

R0/R1/R2 preserve more source-grounded semantic and relational information than R3/R4 on average.

### H2 · Domain interaction

Compression loss is larger for agency, minimal-self, self-world boundary, temporality and atmospheric/salience phenomena than for more behaviorally concrete facts.

### H3 · Context effect

Removing contextual qualifiers increases interpretive error, particularly for distinctions among anomalous self-experience, ordinary experience, medication/sleep effects and overt psychotic phenomena.

### H4 · Non-equivalence at equal predictive utility

If an external prediction task is added, representations with similar predictive accuracy may still differ in phenomenological fidelity.

### H5 · Structured middle-layer efficiency

R1/R2 occupy a favorable region of the fidelity–burden Pareto frontier relative to both full narrative and coarse symptom representation.

## Blinding

- evaluators do not see participant identity;
- evaluators do not see other representation conditions for the same episode;
- representation creators do not evaluate their own representations;
- adjudicators are separated from representation-condition evaluation where feasible.

## Randomization

Episodes are assigned using a balanced incomplete-block design so that each episode is evaluated in every representation condition across the evaluator pool, no evaluator sees the same episode in more than one condition, and evaluator × representation imbalance is minimized.

Randomization code and seed are frozen before unblinding.

## Exclusion rules

Preregister before data inspection:

- source episode lacks enough information for adjudication;
- transcript failure prevents reliable reconstruction;
- representation violates its frozen specification;
- evaluator fails prespecified training/attention checks;
- duplicate episode accidentally included.

Clinical severity or unusual content is not itself an exclusion criterion.

## Statistical analysis

### Primary model

A hierarchical logistic model for query-level correctness:

[
logit(P(correct_{ierq}=1)) =
\beta_0 + \beta_{representation[r]} + \beta_{domain[q]}
+ \beta_{representation\times domain}
+ u_i + v_{episode} + z_{evaluator}
]

Query-level random effects are added when supported by the design.

### Planned primary contrasts

Freeze before data access, with candidates:

- R2 vs R3;
- R2 vs R4;
- R1 vs R4;
- R0 vs R1.

Other pairwise contrasts are secondary.

### Missing / indeterminate answers

Indeterminate is retained as a substantive outcome when ambiguity exists. It is never silently recoded as incorrect.

Sensitivity analyses compare strict accuracy, preregistered partial-credit scoring and probabilistic scoring.

## Power

Use simulation-based power/precision after pilot variance components are available.

The target is precision for the smallest scientifically meaningful representation contrast, not a conventional participant-count heuristic. A single-level formula that ignores episodes, queries and evaluators is not acceptable.

## Pareto analysis

Each representation receives:

[
M(R)=\{F(R),V(R),U(R),C(R)\}
]

where (F) is phenomenological fidelity, (V) independent validity, (U) predictive/intervention utility and (C) burden/cost.

A representation is Pareto-dominated only if another is no worse on all relevant dimensions and strictly better on at least one. No universal “best representation” is declared.

## Robustness analyses

1. leave-one-participant-out;
2. leave-one-evaluator-out;
3. domain-specific effects;
4. representation-length matched analysis;
5. confidence-weighted vs unweighted scoring;
6. specialist vs non-specialist evaluator strata;
7. original-language vs translated cases where applicable;
8. alternative adjudication for unresolved ambiguity.

## Falsification thresholds

The central claim is weakened if:

- coarse self-report or symptom representations show negligible fidelity loss at much lower burden;
- apparent fidelity advantages disappear after matching representation length;
- fidelity metrics cannot achieve acceptable independent-rater reliability;
- participant checks systematically contradict supposedly source-faithful reconstructions;
- relative representation performance is unstable across sites/evaluator panels;
- richer phenomenological detail yields no reproducible scientific value beyond verbosity.

## LLM policy

If LLMs are used:

- model/version/date and prompt are frozen;
- no identifying information is sent to non-approved services;
- extraction and evaluation use independent pipelines;
- human evaluation remains the initial primary endpoint;
- repeated generations quantify stochastic variability;
- outputs are labeled derived data, never source evidence.

## Ethics and privacy

“Preserve the source” means preserve provenance, not indiscriminately publish or permanently retain identifiable psychiatric records.

Require ethics approval where applicable, explicit consent, de-identification, access control, data minimization, retention policy, separate passive-sensing consent and no automated clinical decision based on benchmark scores.

## Confirmatory versus exploratory boundary

### Confirmatory

- frozen representation conditions;
- frozen query bank;
- primary endpoint;
- primary contrasts;
- blinding;
- exclusion criteria;
- hierarchical primary model.

### Exploratory

- LLM conditions;
- neural/behavioral associations;
- unsupervised latent representations;
- alternative graph metrics;
- transdiagnostic extension;
- intervention forecasting.

## Registration gate

This becomes preregistration-ready only after:

1. exact instruments are selected;
2. evaluator training and acceptable reliability threshold are frozen;
3. query-bank construction is piloted without tuning on confirmatory cases;
4. simulation-based sample-size target is frozen;
5. ethics/data-governance plan is approved.
