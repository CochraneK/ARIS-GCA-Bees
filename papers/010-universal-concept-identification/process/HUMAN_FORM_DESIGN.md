# ARIS4C010 · Human Calibration Form Design

## Primary comparison

The first human calibration compares **P2 versus P3 versus P6** on the same underlying target-query universe.

P6+context remains a targeted follow-up because it changes the interaction structure rather than only the answer alphabet.

## One balanced design cycle

The builder creates:

- 36 base forms;
- each duplicated as P2, P3 and P6;
- 108 participant forms total.

Each form contains:

- 60 lexical main trials — one query for every OEWN target;
- 24 mixed-stress main trials — one query for every stress scenario;
- 8 within-rater retest trials;
- 92 presented trials total.

Across 36 forms **within each protocol**:

- every lexical target-query pair appears exactly 3 times;
- every mixed-stress pair appears exactly 4 times.

Therefore a complete 108-participant three-protocol cycle, with one participant per form, gives balanced first-pass coverage under P2, P3 and P6.

**This is not a sample-size recommendation.** It is a combinatorial assignment cycle. Additional cycles can be run after a power/precision calculation.

## Why participant-level protocol assignment

A participant uses one response protocol throughout a form (P2, P3, or P6).

This avoids:
- constantly changing response alphabets;
- teaching participants P6 categories immediately before a P2 trial;
- direct within-participant contamination of the binary condition.

## Retest

Each form repeats 4 lexical and 4 mixed-stress trials selected deterministically from that form.

Retests are shuffled into the form and immediate duplicates are avoided where possible.

Primary use:
- within-rater exact consistency;
- category-specific instability;
- comparison of P2, P3 and P6 retest reliability.

## Analysis layers

The repository includes a dependency-free descriptive analyzer for:
- response distributions;
- P6 nonbinary-use rate;
- pairwise agreement;
- response entropy;
- retest consistency;
- confidence;
- response time.

Confirmatory hierarchical modeling remains governed by `PREREG_DRAFT.md` and should be frozen before real test data are inspected.


## Mechanistic contrasts

The three protocols decompose the source of any apparent improvement:

1. **P2 vs P3** — does a generic MAYBE option reduce forced binary errors?
2. **P3 vs P6** — do explicit semantic failure states add value beyond generic MAYBE?
3. **P2 vs P6** — total effect of the fine-grained protocol.

The second contrast is the most diagnostic for the distinct 010 contribution.
