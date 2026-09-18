# ARIS4C009A · Fidelity metric specification

## Purpose

This document operationalizes "phenomenological fidelity" without making any psychiatric representation judge itself.

The central rule is:

> **Representations are evaluated by reconstruction tasks generated independently from the representations.**

A longer interview is allowed to preserve more information, but the study must also ask whether that gain survives comparison at equal information and acquisition budgets.

## 1. Three-panel architecture

### Panel A · Query constructors

Panel A sees the de-identified source episode but **never** the compressed representations.

They construct candidate questions that test semantic, relational, contextual and temporal information.

### Panel B · Source adjudicators

Panel B sees the source episode and candidate questions.

They establish:

- admissible answer set;
- reference answer or probability distribution;
- source ambiguity;
- importance/criticality;
- whether the source actually supports answering the question.

### Panel C · Representation evaluators

Panel C sees exactly one representation of an episode and answers the frozen questions.

Panel C does not see the source episode, other representations, or the hypothesized representation ordering.

This separation prevents EASE-like, symptom-like or computational representations from writing their own exam.

## 2. Query admissibility

A query enters the confirmatory bank only if:

1. the answer is supported by the source record;
2. at least two adjudicators agree it is answerable or explicitly uncertain;
3. it does not require information absent from the source;
4. it is not phrased using terminology unique to one representation condition unless all evaluators receive a definition;
5. its scoring rule can be frozen before representation evaluation.

Queries that fail are retained only for exploratory analysis.

## 3. Fidelity components

Report a vector rather than a single total:

[
F(R)=(F_{sem},F_{rel},F_{ctx},F_{temp},F_{pers})
]

### 3.1 Semantic fidelity

For categorical answers with a single adjudicated category:

[
F_{sem}^{strict}=rac{1}{Q}sum_q I(hat y_q=y_q)
]

For uncertain source adjudication, the preferred representation is a probability distribution (p_q) over admissible categories.

If evaluators also provide probabilities (hat p_q), use a proper scoring rule.

Multiclass Brier loss:

[
L_{Brier,q}=sum_c(hat p_{qc}-p_{qc})^2
]

A normalized fidelity score may be reported relative to a preregistered null predictor, but raw Brier loss is retained.

### 3.2 Relational fidelity

Source adjudicators create a relation set:

[
E_X={(source,relation,target,modifiers)}
]

Representation evaluators reconstruct the relation set.

Primary relation outcomes:

- edge precision;
- edge recall;
- edge F1;
- relation-type confusion matrix.

Graph edit distance is secondary because its cost weights are less directly interpretable.

### 3.3 Context fidelity

For questions whose answer depends on context, compare reconstruction with and without the relevant contextual qualifier.

For a proper loss (L):

[
D_{ctx}=L(hat y_{without context},y)-L(hat y_{with context},y)
]

Positive (D_{ctx}) means context removal harmed interpretation.

This can be tested by deliberate context-ablation variants of the same representation.

### 3.4 Temporal fidelity

Separate:

- pairwise event-order concordance;
- onset/duration error;
- recurrence classification;
- transition preservation.

For ordered event pairs:

[
F_{order}=rac{correctly ordered pairs}{adjudicable ordered pairs}
]

Temporal fidelity is not inferred from a static symptom total unless temporal information is explicitly encoded.

### 3.5 Participant-endorsed fidelity

When feasible, participants evaluate blinded reconstructions for:

- meaning preserved;
- important omission;
- important distortion;
- unacceptable reinterpretation.

Participant endorsement is indispensable but not infallible. It is analyzed alongside source adjudication, not used as a sole ground truth.

## 4. Criticality weighting

Not all lost details have equal scientific or clinical importance.

Before representation evaluation, Panel B labels each query:

- low criticality;
- medium criticality;
- high criticality;

or assigns a preregistered weight.

Both **unweighted** and **criticality-weighted** results are reported. The unweighted result remains necessary so weights cannot manufacture the desired conclusion.

## 5. Source uncertainty

Source ambiguity must propagate forward.

Reference answers can therefore be:

- point category;
- set of admissible categories;
- probability distribution;
- unresolved.

Representations are **not penalized for preserving uncertainty**.

A confident but incorrect compression can be worse than an explicitly uncertain representation.

## 6. Reliability gate

Reliability is measured separately from fidelity.

Pilot targets are engineering gates, not universal laws:

- categorical adjudication: report percent agreement and Gwet's AC1/AC2; aim for AC1/AC2 >= 0.70 for core domains before confirmatory use;
- continuous/ordinal ratings: report ICC with interval estimates; aim for ICC >= 0.75 for primary continuous components;
- relation annotation: report edge-level F1 between raters and relation-specific disagreement.

If a core domain fails the gate, revise definitions and repeat pilot calibration before confirmatory data are scored.

Cohen's kappa is reported only when its prevalence sensitivity is acceptable; it is not the sole reliability criterion.

## 7. Preventing the "more text always wins" artifact

### 7.1 Raw frontier

First report real-world fidelity and real-world burden exactly as observed.

### 7.2 Equal-description-rate analysis

Serialize each representation under a common measurement protocol and estimate representation rate using:

- token/character count;
- number of structured fields;
- entropy/compressed description length when defensible.

Then fit fidelity as a function of representation rate.

Compare representations at overlapping rates rather than assuming raw length is irrelevant.

### 7.3 Equal-acquisition-burden analysis

Compare fidelity at matched or modeled acquisition burden:

- participant minutes;
- specialist minutes;
- total staff minutes;
- monetary cost where available.

### 7.4 Controlled budget curves

Where methodologically possible, generate **predefined budget variants** of a representation using a frozen compression protocol.

Do not hand-edit a representation after seeing which details matter.

Estimate:

[
F_R(b)
]

where (b) is a representation budget.

The area under this fidelity-rate curve is exploratory unless its budget grid and compression rule are preregistered.

## 8. Avoiding ontology favoritism

The benchmark query bank combines:

1. phenomenology-informed queries;
2. clinically conventional queries;
3. domain-general factual/relational queries;
4. participant-generated "what must not be lost" questions.

Results are stratified by query origin.

A representation should not be declared globally superior because it performs well only on questions written in its own theoretical vocabulary.

## 9. Avoiding evaluator-theory leakage

Record evaluator background:

- phenomenological psychopathology;
- conventional clinical psychiatry;
- computational psychiatry;
- psychology/neuroscience;
- trained non-specialist.

Test representation × evaluator-background interactions.

Primary fidelity estimates pool across a deliberately mixed evaluator panel unless the preregistration specifies otherwise.

## 10. Calibration and confidence

Evaluators provide confidence or probabilities when feasible.

Report:

- accuracy/fidelity;
- Brier score;
- calibration curves;
- overconfidence.

This distinguishes a representation that correctly signals uncertainty from one that gives confident but distorted reconstructions.

## 11. Missingness and abstention

"Cannot infer from this representation" is an allowed response.

Abstention is scored separately from wrong inference.

Primary analyses report at least:

- coverage;
- accuracy conditional on answer;
- overall proper scoring loss.

This prevents forced guessing from making a sparse representation look falsely informative.

## 12. Hierarchical analysis

For binary query correctness, a candidate primary model is:

[
logit(P(Y=1))=
\beta_0+
\beta_R+
\beta_D+
\beta_{R\times D}+
u_{participant}+
u_{episode}+
u_{query}+
u_{evaluator}
]

where (R) is representation and (D) is phenomenological domain.

If query origin matters, include it as a preregistered factor.

## 13. Pareto frontier

Keep distinct:

- fidelity vector (F);
- independent validity vector (V);
- predictive utility (U);
- burden vector (C).

A representation (A) dominates (B) only if it is no worse in every selected comparison dimension and strictly better in at least one.

The frontier is reported separately for different use cases when their constraints differ.

## 14. Minimum confirmatory metric set

009A can remain tractable with five confirmatory outputs:

1. semantic reconstruction accuracy/proper score;
2. relation F1;
3. context-ablation loss;
4. temporal-order concordance;
5. acquisition burden.

Participant-endorsed fidelity is a key secondary endpoint when recontact is feasible.

## 15. Metric falsification

The measurement framework itself fails or needs revision if:

- independently generated queries systematically favor one theoretical vocabulary;
- reliability remains poor after calibration;
- fidelity differences vanish under all rate-matched comparisons;
- participant meaning checks conflict strongly with source-derived scoring;
- results change radically when reasonable scoring rules change;
- evaluator background fully determines the representation ordering.

These are substantive failures, not inconveniences to be hidden.
