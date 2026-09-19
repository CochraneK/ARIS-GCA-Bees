# ARIS4C009 · AI boundary-judge manual

> Legacy filename note: this document replaced the former human-rater manual. Pilot-0 now uses independent AI judges.

## Task

Judge one narrow engineering question:

> **Does this excerpt form a usable information window for a later blinded reconstruction test?**

Do **not** rate psychopathology, diagnosis, truthfulness, intelligence, rationality, the coherence of the person, or clinical severity.

A usable window contains enough local context for at least one nontrivial source-grounded question while avoiding unnecessary mixing of unrelated topics.

## Independence rules

Every model must:

- receive the same frozen prompt in `AI_JUDGE_PROMPT_BOUNDARY.md`;
- see only the current blinded excerpt and task instruction;
- not see the target word count, cohort, participant identity, source filename, or private key;
- not see another model's output;
- not browse or retrieve outside information;
- run with deterministic or near-deterministic decoding where supported;
- use a fresh/isolated context for each item or an equivalent non-leaking batch protocol.

Use at least three materially different model families/providers where feasible. Multiple aliases of one underlying family do not provide strong independence.

## Development versus primary scoring

Synthetic practice cases may be used to debug instructions and parsing.

The 20 real-data training windows are a private dry run for:

- refusal behavior;
- schema compliance;
- context handling;
- instruction-following failures.

They are excluded from primary agreement statistics.

Models do not discuss or reconcile training answers. Prompt changes stop before primary scoring begins.

## Rating fields

### coherent_boundary — yes / no

Does the excerpt begin and end in a way that is interpretable as one local conversational unit?

"No" is appropriate when the excerpt clearly depends on omitted adjacent material or ends in the middle of an unresolved local unit.

### sufficient_nontrivial — yes / no

Could an independent evaluator answer at least one meaningful source-grounded question from the excerpt, beyond merely repeating one yes/no answer?

### mixed_unrelated_topics — yes / no

Does the window combine genuinely separable topics that could be split without losing the meaning of either?

Do not mark mixed merely because of an example, clarification, self-correction, comparison, or cause/consequence relation.

### recommended_action

- **keep** — usable as-is.
- **merge** — needs adjacent context.
- **split** — combines separable local units.
- **reject** — unsuitable as an annotation unit; use sparingly.

### confidence_1_5

1 = highly uncertain; 5 = very confident.

Low confidence is valid data.

## Preserve uncertainty

If a participant is unsure, changes their mind, or gives alternatives, that uncertainty may itself be information. Do not mark the excerpt insufficient merely because it lacks one definite answer.

## Interviewer speech matters

Interviewer prompts are part of the acquisition record. They can establish referents, context, assumptions, time, and meaning.

## Primary analysis

After every judge file is frozen:

1. compute multi-model agreement;
2. compute every pairwise Gwet AC1;
3. inspect systematic model-family outliers;
4. unblind A/B only after scoring inputs are frozen;
5. compare 20 vs 40 strategy usability;
6. preserve raw judge outputs privately and never retroactively edit them.

The result must be described as **AI-judge agreement** or **cross-model agreement**, not human inter-rater reliability.

## Privacy

The private packet contains psychiatric interview text.

Do not commit judge inputs, raw outputs, or source excerpts. Use only local models or external endpoints compatible with the source-data governance. Publish aggregate calibration outputs only after review.
