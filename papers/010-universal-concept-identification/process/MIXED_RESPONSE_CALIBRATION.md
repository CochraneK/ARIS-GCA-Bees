# ARIS4C010 · Mixed Response-State Calibration

The 60-target OEWN lexical calibration is intentionally ordinary: it is strong for polysemy and semantic separation, but weak for evaluating rare response states such as BORDERLINE, UNDEFINED or BOTH.

This companion calibration therefore uses **24 constructed semantic scenarios** spanning:

- negation with different universes;
- vagueness;
- missing versus resolved context;
- empty reference;
- fiction;
- inconsistency;
- self-reference/paradox;
- paraconsistent contradictory information;
- epistemic unknowns;
- stochastic futures;
- undecidability;
- oracle-access limits;
- newly coined/open-world concepts;
- uninterpretable tokens.

It is a **response-state calibration**, not the main identification benchmark.

## Core rule

No expected response is stored as gold.

The scenario's `phenomenon_tags` document why the item was included; they are not labels for the query response.

## Design

- 24 scenarios;
- 18 generic probes;
- 9 probes per scenario in a deterministic answer-blind rotation;
- 216 target-query pairs;
- identical semantic material available to P2, P3, P6 and P6+context conditions.

## Protocol mechanism

### P2
Forced YES/NO.

### P3 mechanism control
YES / NO / MAYBE. MAYBE deliberately collapses all reasons a confident binary answer may fail.

### P6
YES / NO / BORDERLINE / UNKNOWN / UNDEFINED / BOTH.

This allows a direct test of whether fine-grained semantic states improve reliability or identification beyond a generic uncertainty escape response.

## Primary question

Can human annotators reproducibly distinguish:

```text
NO
BORDERLINE
UNKNOWN
UNDEFINED
BOTH
CONTEXT_REQUEST
```

rather than using them as interchangeable forms of uncertainty?

## Success criteria before using P6 in the main benchmark

P6 should be retained only if:

1. category use is interpretable rather than arbitrary;
2. within-rater retest is acceptable;
3. between-rater confusion concentrates in theoretically adjacent categories rather than everywhere;
4. richer states reduce forced binary contradictions or invalid answers;
5. the benefit survives accounting for response time/cognitive burden.

If those conditions fail, UCID should simplify the response protocol rather than preserve P6 for conceptual elegance.
