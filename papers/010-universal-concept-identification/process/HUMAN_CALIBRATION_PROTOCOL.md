# ARIS4C010 · Human Annotation & Oracle Calibration Protocol v0.1

## Goal

Estimate whether UCID's richer response states are reproducible enough to support scientific comparison with strict binary Twenty Questions.

The annotation study is calibration, not a survey of personal beliefs.

## Response protocol

### YES
Under the frozen benchmark interpretation, the predicate/query applies to the target.

### NO
The query is meaningful and applicable, but false of the target.

### BORDERLINE
The query is applicable, but the target is genuinely borderline/graded under the provided context or ordinary interpretation.

Use this for vagueness, not for lack of knowledge.

### UNKNOWN
The query has a determinate answer in principle, but the annotator/oracle does not know it from the allowed information.

Use this for epistemic uncertainty, not for type mismatch.

### UNDEFINED
The question is not truth-evaluable as posed for the target because of:
- target-type mismatch;
- missing required context;
- failed presupposition;
- empty-reference handling under the chosen protocol;
- other explicitly defined semantic failure.

### BOTH
The benchmark representation intentionally supports both positive and negative evidence under the adopted non-explosive/paraconsistent interpretation.

This state should be rare and never used as a generic "confusing" option.

### CONTEXT_REQUEST
Only in the P6+context protocol. The annotator identifies which context variable is missing before attempting an answer.

## Annotation order

For each target-query pair:

1. read target definition and frozen context;
2. judge whether the query is applicable;
3. if context is missing and P6+context is enabled, request it;
4. if inapplicable/presupposition-failed, choose UNDEFINED;
5. otherwise judge truth status;
6. choose BORDERLINE only for genuine graded/borderline application;
7. choose UNKNOWN only for epistemic limitation;
8. choose BOTH only when the benchmark case explicitly permits inconsistency;
9. record confidence.

## Calibration design

Initial calibration subset: about 60 targets spanning all strata.

Each target receives approximately 15–25 queries:
- high-information ordinary questions;
- at least one expected non-informative question;
- at least one type/context stress question where scientifically appropriate.

### Repeated judgments
Repeat at least 10–20% of pairs within-rater after delay to estimate retest consistency.

### Multiple raters
Use multiple raters per target-query pair. Publication design should determine sample size with an explicit precision target rather than an arbitrary fixed number.

## Comparison conditions

At minimum compare:

### Condition P2
YES / NO only.

### Condition P6
YES / NO / BORDERLINE / UNKNOWN / UNDEFINED / BOTH.

### Optional P6+context
Adds CONTEXT_REQUEST and typed context resolution.

The main empirical question is not whether P6 has more categories. It is whether richer categories:
- reduce contradiction/retest error;
- reduce invalid forced answers;
- improve target identifiability;
- do so at acceptable time/cognitive cost.

## Primary reliability measures

Do not rely on one agreement statistic.

Report:
- raw agreement;
- per-class confusion matrix;
- within-rater retest agreement;
- multi-rater reliability appropriate to nominal categories;
- entropy of response distribution by target/query;
- confidence distribution;
- response time.

For sparse rare states such as BOTH, report counts explicitly.

## Adjudication

A response matrix becomes `adjudicated_gold` only after:

1. provenance check;
2. duplicate/leakage check;
3. independent judgments;
4. disagreement review;
5. explicit rationale for theory-sensitive cases;
6. final adjudicator decision or preserved probabilistic distribution.

Some items may remain `human_annotated` without promotion to gold.

## Handling philosophical disagreement

For cases such as:
- empty descriptions;
- liar-like paradoxes;
- fictional reference;
- vague predicates;
- phenomenal concepts;

the benchmark should not hide substantive theoretical choices.

Where multiple respectable analyses exist:
- state the adopted operational semantics;
- preserve alternate labels in notes or alternate benchmark tracks;
- avoid wording such as "the objectively correct philosophical answer."

## Exclusion rules

Exclude or quarantine a target-query pair when:
- annotators cannot agree on what the query means;
- necessary context cannot be frozen;
- the item depends on specialist knowledge beyond the intended population without an explicit expert-oracle condition;
- translation changes the target interpretation;
- the item is accidentally self-revealing.

## Human-study ethics / data minimization

The intended task is low-risk semantic annotation, but any actual participant study should:
- collect only needed demographic variables;
- avoid unnecessary sensitive personal information;
- obtain the appropriate institutional ethics review/approval or exemption determination;
- keep participant identifiers separate from semantic judgments;
- publish only de-identified aggregate/annotation data consistent with consent.

## Model oracles

LLM judgments may be collected as a separate oracle class.

They must never silently replace human gold labels.

For model oracles record:
- provider/model/version;
- system/prompt template;
- temperature/sampling parameters;
- date;
- repeated runs;
- whether web/tools were enabled.

## Promotion gate

The P6 response protocol is retained for publication only if the calibration data show that annotators can use the categories with interpretable reliability and that the richer protocol improves at least one preregistered validity/efficiency outcome after accounting for response cost.
