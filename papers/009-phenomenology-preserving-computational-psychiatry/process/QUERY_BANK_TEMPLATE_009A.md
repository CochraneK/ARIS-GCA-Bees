# ARIS4C009A · Independent query-bank template

## Purpose

The query bank is the exam used to test whether a representation allows reconstruction of information in the source episode.

It must be built **before** Panel C evaluates representations and must not be written by looking at the compressed representations.

This file is a template, not a completed patient-facing or rater-ready instrument.

## Required metadata for every query

| Field | Meaning |
|---|---|
| query_id | Stable identifier |
| episode_id | Source episode |
| query_origin | phenomenology-informed / conventional-clinical / domain-general / participant-generated |
| domain | semantic / relation / context / temporal / participant-meaning |
| subdomain | agency, ownership, salience, body, affect, time, etc. |
| query_text | Evaluator-facing question |
| response_type | categorical / ordinal / probabilistic / relation-set |
| source_answerable | yes / no / uncertain |
| adjudicated_answer | Frozen reference when answerable |
| adjudication_uncertainty | Explicit uncertainty |
| criticality | low / medium / high, assigned before representation evaluation |
| theoretical_vocabulary_required | yes / no |
| source_provenance | Source span/adjudication pointer |

## A. Domain-general semantic queries

These deliberately avoid specialist terminology when possible.

1. **What happened?**  
   What experience/event does the participant describe?

2. **Who or what was involved?**  
   Identify the relevant self/other/body/world entities.

3. **What was the participant's stance toward the experience?**  
   Literal / metaphorical / uncertain / mixed / not established.

4. **Where was the experience located or attributed?**  
   Self / body / external world / other agent / unclear / mixed.

5. **What affect accompanied it?**  
   Positive / negative / neutral / mixed / not established.

6. **How certain was the participant?**  
   Certain / probable / possible / explicitly uncertain / contradictory.

## B. Agency / ownership / self queries

These are phenomenology-informed but phrased without assuming a diagnosis.

7. Did the participant experience the thought/action/sensation as **their own**?

8. Did the participant experience themselves as **causing or controlling** the event/action?

9. Was there a difference between **knowing something was theirs** and **feeling it as theirs**?

10. Did the experience alter the boundary between self and other/world?

11. Was the disturbance persistent, brief, intermittent or unclear?

12. Did the participant distinguish the experience from ordinary distraction, habit or automatic action?

## C. Relation queries

13. What was experienced as causing what?

14. What was interpreted as referring to the participant?

15. Which thought, sensation or external event became unusually important or attention-grabbing?

16. Did an altered bodily experience precede or follow a change in thought/meaning?

17. Was another person experienced as influencing, observing, addressing or merely being present?

18. Which source relation is **explicitly stated**, and which is only an evaluator inference?

## D. Context queries

19. Did the experience occur only in a specific interpersonal or environmental situation?

20. Was sleep/fatigue relevant to the episode?

21. Was medication relevant to how the experience was interpreted?

22. Was substance use or withdrawal relevant, if explicitly available and consented?

23. Was an ordinary/non-pathological alternative explanation explicitly discussed?

24. Did removing one contextual fact materially change the most plausible interpretation?

## E. Temporal queries

25. Which event occurred first?

26. How long did the focal experience last?

27. Was it single, recurrent or persistent?

28. Did it precede, coincide with or follow a change in functioning/distress?

29. Did the participant describe a gradual transition or a sudden shift?

30. Is the current interpretation contemporaneous with the event or retrospective?

## F. Participant-generated preservation queries

Participants can nominate information they regard as essential not to lose.

Example prompts for constructing, not answering, such queries:

- “What would someone misunderstand if they only saw a short checklist?”
- “Which part of this experience changes its meaning if omitted?”
- “What distinction matters most to you in describing what happened?”

These questions are frozen before Panel C evaluation.

## Query-bank balancing rules

The confirmatory bank should not consist mainly of one theoretical vocabulary.

Target a balanced mix across:

- domain-general reconstruction;
- phenomenology-informed distinctions;
- conventional clinical information;
- participant-identified meaning.

Report performance separately by query origin.

## Redundancy control

Many queries can be semantically near-duplicates.

Before freezing the bank:

1. map each query to the relation ontology;
2. identify near-duplicate questions;
3. retain duplicates only when they deliberately test reliability;
4. record query clusters;
5. account for query clustering in simulation/analysis.

Counting paraphrases as independent information would artificially inflate precision.

## Answerability gate

A query is confirmatory only when the source actually supports adjudication.

Allowed source states:

- answerable with point answer;
- answerable with multiple admissible answers;
- answerable probabilistically;
- genuinely unresolved;
- not answerable.

Panel C is not penalized for failing to infer information that is not present in the source.

## Pilot calibration target

Before confirmatory use, test the template on independent pilot episodes and estimate:

- fraction of candidate queries that survive answerability screening;
- adjudicator agreement;
- proportion of indeterminate source answers;
- average queries retained per episode;
- redundancy/correlation between retained queries;
- time needed to construct and adjudicate each query;
- representation-specific ceiling/floor effects.

The pilot may revise the template. The confirmatory bank must then be frozen.
