# ARIS4C009A · Minimal episode relation ontology

## Design goal

This is **not** a proposed complete ontology of psychopathology.

It is a deliberately small, orthogonal annotation language for testing whether relationships present in a source episode survive representation.

The axes are separated so that one code does not silently bundle entity, relation, certainty, severity and diagnosis.

## Axis E · Entity type

An episode may contain zero or more entities of each type.

| Code | Entity |
|---|---|
| SELF | experienced self / first-person center |
| THOUGHT | thought, image, inner speech, idea |
| PERCEPTION | sensory/perceptual content |
| BODY | bodily state or body part |
| AFFECT | affective state |
| OTHER | another person or agent |
| WORLD | object, place, environment or world-as-experienced |
| EVENT | discrete event or episode |
| ACTION | action, urge or behavior |
| LANGUAGE | spoken/written/sign-like expression |
| MEANING | belief, interpretation, significance or meaning |
| TIME | experienced or clock/calendar time |
| SPACE | experienced or physical space |

Entity types are descriptive. They do not imply pathology.

## Axis R · Relation type

| Code | Relation | Question it captures |
|---|---|---|
| OWNERSHIP | mineness / possession | Is X experienced as mine/not-mine/uncertain? |
| AGENCY | authorship/control | Do I experience myself as causing or controlling X? |
| SOURCE | source attribution | From where/whom is X experienced as originating? |
| BOUNDARY | demarcation | How clearly separated are self/other/world/body? |
| CAUSAL | causal attribution | What is experienced or inferred to cause what? |
| TEMPORAL | before/after/during | What is the temporal relation? |
| SPATIAL | inside/outside/near/far/etc. | What spatial relation is experienced? |
| SALIENCE | importance/attention capture | What is experienced as unusually significant? |
| FAMILIARITY | familiar/strange/unreal | How is familiarity/reality quality altered? |
| REFERENTIAL | about/refers-to | What is a thought/sign/event taken to concern? |
| EMBODIMENT | self–body coupling | How is experience related to body/self? |
| SOCIAL | self–other interpersonal relation | How is an experience embedded in another person/interaction? |
| EXPRESSION | experience → language/action | How is the experience expressed or enacted? |

Relations can be multi-label when the source supports multiple distinct relations.

## Axis M · Modifiers

Modifiers never replace the underlying entity/relation.

### Epistemic stance

- certain;
- probable;
- possible;
- explicitly uncertain;
- contradictory/mixed;
- not established.

### Valence

- positive;
- negative;
- neutral;
- mixed;
- not established.

### Intensity

Use a preregistered ordinal or continuous scale only when source material supports it.

### Frequency

- single;
- occasional;
- recurrent;
- persistent;
- unknown.

### Perspective/status

- literal endorsement;
- metaphor/analogy;
- hypothetical;
- retrospective reinterpretation;
- mixed;
- unclear.

## Axis T · Temporal annotation

Keep at least:

- onset;
- offset/duration;
- recurrence;
- order relative to other episode events;
- trait-like versus episode-like characterization when supportable.

Do not infer exact duration from vague wording.

## Axis C · Context

Context is represented separately from phenomenological content.

Candidate context classes:

- interpersonal;
- location/environment;
- sleep/fatigue;
- medication;
- substance;
- acute physical state;
- stressor/life event;
- task/interview context;
- cultural/linguistic context;
- other participant-specified context.

A context code does not assert causation unless a CAUSAL relation is separately recorded.

## Provenance requirement

Every entity, relation and modifier must point to one or more source spans or an adjudication note.

No provenance pointer → no confirmatory graph edge.

## Uncertainty requirement

Annotators may store alternatives:

[
{edge_1:p_1, edge_2:p_2, unresolved:p_u}
]

A forced single edge is prohibited when the source is genuinely ambiguous.

## Mapping to established instruments

EASE, EAWE, STEP, PANSS and other instruments can be mapped **onto** this graph for analysis, but their item structures do not define the graph.

This permits a fair test of whether multiple instruments preserve or discard the same source relations.

## Relation-fidelity scoring

For confirmatory analysis:

1. freeze source graph after independent adjudication;
2. reconstruct a graph from each representation under blinding;
3. match entity references using a frozen alignment procedure;
4. compute relation precision, recall and F1;
5. report relation-specific confusion.

Do not let a graph with many trivial edges inflate fidelity.

Primary relation types should be weighted equally or analyzed separately; any criticality weighting is secondary unless preregistered.

## Ontology extension rule

A new relation type can enter the confirmatory ontology only before confirmatory scoring starts and only if:

- existing types cannot express it without semantic distortion;
- at least two independent annotators can apply it reliably;
- a clear definition and counterexample are added.

Otherwise it remains exploratory.
