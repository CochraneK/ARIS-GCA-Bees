# ARIS4C009A · Episode-level data dictionary

This schema is representation-agnostic. Evidence and provenance are recorded first; derived representations are stored separately.

## Core identifiers

| Field | Type | Description |
|---|---|---|
| participant_id | string | Pseudonymous study identifier |
| episode_id | string | Unique focal episode |
| source_segment_id | string | Immutable provenance pointer to de-identified source |
| site_id | string | Study-site code |
| language_original | string | Original language |
| assessment_time | datetime / interval | Source-assessment time |

## Source-evidence fields

| Field | Type | Description |
|---|---|---|
| participant_text | protected text | De-identified participant wording |
| interviewer_prompt | protected text | Prompt immediately relevant to the episode |
| context_window | protected text / structured | Necessary conversational/situational context |
| temporal_anchor | structured | Onset, duration, recurrence and ordering |
| uncertainty_source | ordinal + text | Ambiguity already present in source |
| literal_metaphoric_status | categorical/uncertain | Only when explicitly clarified |
| attribution | multi-label + uncertainty | self / other / environment / unknown / mixed |
| affective_valence | multi-label + uncertainty | negative / neutral / positive / mixed / indeterminate |
| participant_clarification | protected text | Follow-up clarification if collected |
| contextual_factors | structured | Relevant sleep/medication/substance/event context if consented |
| source_rater_confidence | probability/ordinal | Confidence in source interpretation |

## Phenomenological relation graph

Every graph record retains a source pointer.

| Field | Type | Description |
|---|---|---|
| node_id | string | Node identifier |
| node_type | controlled vocabulary | self, thought, body, other, world, event, time, space, affect, meaning, etc. |
| node_label | text | Human-readable label |
| edge_source | node_id | Relation origin |
| edge_target | node_id | Relation target |
| relation_type | controlled vocabulary | agency, ownership, causation, precedence, attribution, salience, boundary, etc. |
| relation_confidence | probability/ordinal | Rater confidence |
| provenance_span | source pointer | Evidence supporting node/edge |

## Representation table

| Field | Type | Description |
|---|---|---|
| representation_id | string | Unique encoded representation |
| episode_id | string | Parent episode |
| representation_condition | categorical | R0–R5 / exploratory |
| representation_payload | structured/text/vector | Encoded representation |
| creator_type | categorical | trained rater / participant / algorithm / LLM |
| creator_id_or_version | string | Pseudonymous rater or frozen model/version |
| creation_protocol_version | string | Frozen extraction/coding protocol |
| representation_length | numeric | Tokens/items/dimensions |
| creation_time_minutes | numeric | Human/participant time |
| compute_cost | numeric | Frozen compute-cost unit |
| provenance_complete | boolean | Whether every claim is source-traceable |

## Benchmark-query table

| Field | Type | Description |
|---|---|---|
| query_id | string | Frozen benchmark item |
| query_domain | categorical | semantic / relation / context / temporal / participant meaning |
| query_text | text | Evaluator-facing question |
| response_type | categorical | binary / categorical / ordinal / probabilistic |
| adjudicated_answer | structured | Multi-anchor reference |
| adjudication_uncertainty | probability/ordinal | Reference uncertainty |

## Evaluation table

| Field | Type | Description |
|---|---|---|
| evaluator_id | string | Pseudonymous evaluator |
| representation_id | string | Condition evaluated |
| query_id | string | Query answered |
| evaluator_answer | structured | Response |
| evaluator_confidence | probability/ordinal | Confidence |
| correct_strict | boolean/null | Strict scoring where defined |
| partial_credit | numeric/null | Preregistered partial credit |
| evaluation_time_seconds | numeric | Burden/time |

## Participant-fidelity table

| Field | Type | Description |
|---|---|---|
| participant_id | string | Participant |
| representation_id | string | Reconstruction shown |
| meaning_preserved | ordinal | Structured participant rating |
| important_omission | boolean + text | Important information lost |
| important_distortion | boolean + text | Meaning changed |
| participant_comment | protected text | Optional explanation |

## Data-governance flags

| Field | Type | Description |
|---|---|---|
| consent_scope | categorical | Allowed research uses |
| public_release_allowed | boolean | Derived/raw release permission |
| passive_sensing_consent | boolean | Separate permission if applicable |
| recontact_allowed | boolean | Whether clarification is permitted |
| retention_class | categorical | Retention policy |

## Missingness rule

Never use one blank value to collapse:

- not asked;
- not applicable;
- unknown;
- participant uncertain;
- rater uncertain;
- redacted for privacy;
- technical failure.

These states require distinct codes because uncertainty belongs to both the phenomenon and the measurement process.
