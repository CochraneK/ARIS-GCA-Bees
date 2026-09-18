# ARIS4C010 · Semantic Stress Suite Seed

**Status:** design seed only — NOT adjudicated gold data.

The purpose of this file is to ensure that UCID contains qualitatively different failure modes. The examples are templates for annotation and formalization, not claims that the proposed labels are philosophically uncontested.

| Seed | Target | Why it is included | Main axes stressed | Required clarification |
|---|---|---|---|---|
| S01 | not a mammal | complement/negation | logical form; universe dependence | explicitly fix universe (U) |
| S02 | cat or dog | disjunction | compositionality | target is a class/concept, not a particular animal |
| S03 | tall | sorites/comparison class | vagueness; context | specify comparison population or allow BORDERLINE/context request |
| S04 | here | indexical | spatial context | speaker/location must be frozen |
| S05 | today | temporal indexical | temporal context | reference time must be frozen |
| S06 | my mother | relational + speaker-relative referent | relation; context | identify speaker and intended relation convention |
| S07 | the current king of France | meaningful description with no current satisfier | empty reference; presupposition | freeze date/context; distinguish empty from meaningless |
| S08 | unicorn | fictional/nonactual kind | existence/modal status | distinguish fiction from logical impossibility |
| S09 | round square | inconsistent/impossible description | contradiction | specify background geometry/logic |
| S10 | bank — financial sense | same form, different sense | target level; polysemy | benchmark target is a sense, not string |
| S11 | bank — river-edge sense | paired lexical ambiguity | target level; polysemy | grouped with S10 for leakage control |
| S12 | justice | abstract/normative concept | ontology kind; convention | avoid assuming one culture-neutral definition |
| S13 | and | function/logical word | lexical vs formal operation | separate lexeme from truth-functional connective |
| S14 | this sentence is false | liar-like self-reference | self-reference; semantic paradox | formalize quoted sentence and chosen truth theory |
| S15 | the general halting set | undecidability | computability status | distinguish general undecidability from ignorance about one program |
| S16 | an unfamiliar odor quality recognizable by exemplar | weak linguistic ineffability | grounding; lexicalization | requires exemplar/ostension condition |
| S17 | pain quality P known only first-personally | phenomenal access | grounding; oracle limits | define whose experience/oracle is queried |
| S18 | a possible but nonactual blue swan | modality | possible-world semantics | define modal background |
| S19 | not red | negation + vagueness at color boundaries | complement; graded predicates | color space/universe/threshold |
| S20 | Russell-style set of all sets that are not members of themselves | self-membership paradox | higher-order/pathology | formal system must be specified |
| S21 | the former president | discourse/time-sensitive description | anaphora/context | country, reference time, discourse |
| S22 | expensive | evaluator/comparison context | vagueness; scale | currency, market, comparison class, evaluator |
| S23 | tomorrow's weather at an unspecified place | underdetermination | missing context vs epistemic uncertainty | location must be supplied before "unknown" is used |
| S24 | a randomly sampled quantum outcome before measurement | stochasticity | epistemic/stochastic status | distinguish probability from missing knowledge |
| S25 | a newly coined concept defined during the dialogue | open-world expansion | OOS; compositionality | test whether ontology can add target rather than force-match |

## Failure-mode taxonomy exercised by the suite

The suite should preserve these distinctions:

```text
ordinary false
≠ unknown fact
≠ missing context
≠ borderline
≠ presupposition failure / undefined
≠ contradiction
≠ paradox
≠ undecidable-in-general
≠ out-of-support
≠ weakly ineffable/ostensive
≠ strong-ineffability boundary
```

## Adjudication rule

No row becomes gold simply because it appears here.

For each seed:
1. write an explicit formal or operational target definition;
2. identify the response protocol;
3. freeze all required context;
4. list legitimate competing analyses from the literature where relevant;
5. obtain human/expert annotations if the case is language-dependent;
6. mark unresolved theoretical disagreement rather than force consensus.

## Why pathological examples matter

They are not decorative edge cases. A system that succeeds only after silently converting every target into an ordinary concrete noun has not solved the stated UCID problem.

Conversely, the project should not over-weight paradoxes so heavily that ordinary lexical identification becomes irrelevant. The stress suite is a **diagnostic slice**, not a model of natural concept frequency.
