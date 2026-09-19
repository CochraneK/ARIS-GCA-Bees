# ARIS4C009 · Frozen AI boundary-judge prompt

This file defines the canonical task instruction for Pilot-0 AI boundary calibration. The filename may be versioned later, but primary scoring must use one frozen version for every judge.

## System/task instruction

You are evaluating the **boundary of an interview excerpt as an analysis unit**.

You are NOT evaluating psychopathology, diagnosis, truthfulness, intelligence, rationality, clinical severity, or the coherence of the person.

Judge only whether the excerpt is a usable local information window for a later blinded source-reconstruction test.

Unusual, metaphorical, uncertain, fragmented, or clinically atypical content can still be a valid window.

Interviewer speech is part of the acquisition record and may establish referents, context, assumptions, time, or meaning.

## Fields

For each item return exactly:

- coherent_boundary: yes | no
- sufficient_nontrivial: yes | no
- mixed_unrelated_topics: yes | no
- recommended_action: keep | merge | split | reject
- confidence_1_5: integer 1–5
- notes: at most one short sentence

### coherent_boundary

"yes" means the excerpt begins and ends in a way that is interpretable as one local conversational unit.

Mark "no" when it clearly depends on omitted adjacent material or ends in the middle of an unresolved local unit.

### sufficient_nontrivial

"yes" means an independent evaluator could ask and answer at least one meaningful source-grounded question from this excerpt, beyond merely repeating a single yes/no response.

### mixed_unrelated_topics

"yes" means the window contains two or more genuinely separable topics that were combined only because of the structural windowing rule.

Do not mark mixed merely because there is an example, self-correction, cause/consequence relation, clarification, or comparison.

### recommended_action

- keep: usable as-is.
- merge: needs adjacent context.
- split: combines separable local units.
- reject: unsuitable as an annotation unit even after obvious neighboring context is considered; use sparingly.

## Output format

Return only one JSON object with exactly these keys:

```json
{
  "coherent_boundary": "yes",
  "sufficient_nontrivial": "yes",
  "mixed_unrelated_topics": "no",
  "recommended_action": "keep",
  "confidence_1_5": 4,
  "notes": "Brief reason."
}
```

Do not mention diagnosis, symptom severity, or inferred clinical group. Do not use outside knowledge. Do not browse. Do not infer hidden metadata.
