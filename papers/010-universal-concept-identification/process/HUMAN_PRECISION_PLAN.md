# ARIS4C010 · Human Calibration Precision and Stopping Plan

**Status:** design-stage precision plan; final confirmatory thresholds should be frozen after ethics/platform feasibility review and before real calibration responses are inspected.

## Why the form cycle is not the sample size

One balanced three-protocol form cycle contains 108 participants if each of the 108 P2/P3/P6 forms is assigned once.

Within one cycle:

- each lexical main pair receives 3 ratings per protocol;
- each mixed-stress main pair receives 4 ratings per protocol;
- each participant contributes 8 covert retest judgments.

This is enough to test the pipeline and detect gross response-protocol problems, but **3–4 ratings per pair are not automatically sufficient to establish gold semantic labels**.

## Staged design

### Stage A · one complete balanced cycle

Nominal design: 72 completed participants, 36 P2 and 36 P6.

Primary purpose:
- verify comprehension and category use;
- estimate response time/cognitive burden;
- estimate retest consistency;
- identify response categories that are unused or confused;
- estimate pair-level response entropy;
- test whether P3 reduces binary forcing relative to P2, and whether P6 adds value beyond P3.

Stage A is a protocol-feasibility calibration, not final gold construction.

### Stage B · second balanced cycle if P6 survives

If P6 is interpretable and adds value beyond P3, repeat the 108-form three-protocol cycle with new participants or use a frozen sequential design focused on the P3–P6 contrast.

Cumulative nominal coverage:

- 216 completed participants under a full second three-protocol cycle;
- lexical pair ratings: 6 per protocol;
- mixed-stress pair ratings: 8 per protocol;
- 576 retest judgments per protocol before exclusions.

These counts are still analyzed with participant/item clustering rather than as independent Bernoulli observations.

### Stage C · targeted adjudication / additional ratings

Do not automatically run a third full cycle.

Flag target-query pairs for extra ratings when one or more hold:

- insufficient valid responses after exclusions;
- no dominant response category;
- high response entropy;
- strong P2/P6 disagreement not explained by deterministic coarsening;
- low retest stability;
- theory-sensitive stress case;
- suspected wording ambiguity.

Pairs with stable high consensus should stop receiving ratings.

## Pair-level maturity

Suggested operational ladder:

### human_annotated
At least the minimum planned independent ratings have been collected and provenance is complete.

### expert_reviewed
A theory- or ontology-sensitive pair has been reviewed by an appropriate adjudicator or documented secondary process.

### adjudicated_gold
Only when:
- target identity is stable;
- query meaning is stable;
- context is sufficient;
- response distribution is adequately concentrated **or** a probabilistic gold representation is explicitly retained;
- disagreement has been reviewed rather than silently majority-voted away.

Gold need not always be a single categorical label. Some vague or contested pairs may be best represented as a response distribution.

## Precision targets

The calibration should report uncertainty rather than rely only on null-hypothesis tests.

For protocol-level outcomes such as retest consistency or invalid-answer rate:
- use participant/item clustered bootstrap or an appropriate hierarchical model;
- report 95% intervals;
- predefine a practically meaningful difference before confirmatory comparison.

For pair-level response distributions:
- report counts and posterior/interval uncertainty;
- avoid treating six ratings as exact semantic truth.

## P6 continuation rule relative to P3

P6 should proceed into Benchmark v0 as the preferred rich protocol only if Stage A shows all of the following:

1. non-binary states are used on the mixed-stress set rather than being effectively absent;
2. their use is semantically patterned rather than random;
3. retest reliability is not materially worse than P2 after accounting for genuinely borderline items;
4. P6 improves reliability, interpretability, or downstream identification **relative to P3**, enough to justify the extra labels and response time.

If not, simplify the protocol.

## Recruitment and exclusions

Recruitment platform is not yet fixed.

Before data collection freeze:
- eligibility criteria;
- language proficiency criterion;
- compensation;
- expected duration;
- device restrictions if any;
- exclusion/quality rules;
- ethics approval/exemption determination.

These must not be chosen after seeing the outcome difference between P2 and P6.


## P3 mechanism-control interpretation

P3 is the mechanism-control arm.

- If **P3 ≈ P6 > P2**, most benefit comes from allowing a generic non-binary escape response.
- If **P6 > P3 > P2**, fine-grained semantic response states add incremental value.
- If **P2 ≈ P3 ≈ P6**, richer response alphabets are not justified.
- If P6 is slower or less reliable than P3 without enough downstream benefit, prefer P3.
