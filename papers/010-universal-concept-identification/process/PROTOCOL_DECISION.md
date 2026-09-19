# ARIS4C010 · Protocol Decision Record

**Decision date:** 2026-09-19  
**Status:** canonical for Stage-A human calibration

## Decision

Use three response protocols in the first human calibration:

- **P2:** YES / NO
- **P3:** YES / NO / MAYBE
- **P6:** YES / NO / BORDERLINE / UNKNOWN / UNDEFINED / BOTH

Keep **P6+context** as a later extension rather than adding it to the first factorial comparison.

## Why the original P2 vs P6 design was insufficient

The initial design compared forced binary responding directly with a fine-grained semantic response alphabet.

The 2025–2026 prior-art re-audit showed that adaptive Twenty Questions research already uses coarse non-binary responses such as YES / MAYBE / NO. Therefore any P6 advantage over P2 would be mechanistically ambiguous:

1. participants may benefit merely because they are no longer forced into YES/NO; or
2. they may benefit specifically because BORDERLINE, UNKNOWN, UNDEFINED and BOTH are distinguished.

A two-arm P2/P6 experiment cannot separate these explanations.

## Mechanism decomposition

### Contrast A · P2 → P3
Tests the value of a generic escape response from binary forcing.

### Contrast B · P3 → P6
Tests the incremental value of distinguishing *why* binary judgment is inappropriate.

This is the key contrast for the distinctive UCID response-semantics contribution.

### Contrast C · P2 → P6
Measures the total protocol difference but is not sufficient to establish the fine-graining mechanism.

## Interpretation rules

- **P3 ≈ P6 > P2:** benefit is mainly a generic MAYBE/escape option.
- **P6 > P3 > P2:** fine-grained semantic states add incremental value.
- **P2 ≈ P3 ≈ P6:** richer response alphabets are not justified.
- **P3 > P6:** fine-graining harms reliability/usability; prefer the simpler protocol unless downstream identification clearly compensates.

## Claim ceiling

Do not claim that P6 is superior until real human data support the **P3 → P6** contrast under an analysis plan frozen before confirmatory testing.

Do not treat the existence of multiple response labels as novel.

## Engineering consequence

The balanced design contains:

- 36 base forms per protocol;
- 108 participant forms total;
- 84 unique main trials + 8 covert retests per form;
- equal lexical and mixed-pair exposure within each protocol.

One 108-form cycle is a balanced feasibility cycle, not a definitive sample-size requirement.

## Why P6+context is deferred

CONTEXT_REQUEST changes the interaction structure, not merely the answer alphabet. Including it in Stage A would confound response-state granularity with an active repair action.

It should therefore be evaluated after P2/P3/P6 establishes whether fine-grained response semantics are worth retaining.
