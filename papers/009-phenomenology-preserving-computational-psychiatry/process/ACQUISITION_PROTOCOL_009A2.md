# ARIS4C009A2 · Acquisition-method benchmark

## Working title

**How Much Does the Method Change the Experience We Measure? A Randomized Multi-Method Benchmark of Psychopathology Acquisition**

## Status

Protocol design. This study requires purpose-collected human data and ethics approval.

## 1. Why 009A2 exists

009A1 asks:

> Given the **same fixed source record**, what information is lost when it is encoded differently?

009A2 asks a different question:

> When the **same person and focal experience** are assessed using different acquisition methods, how do the resulting evidential records diverge?

This distinction is necessary because psychiatric information is not passively read out from a hidden state.

For method (m):

[
X^{(m)}=A_m(H,C,I_m)+epsilon_m
]

where:

- (H) = lived state, not directly observed;
- (C) = context;
- (I_m) = interaction/process features of method (m);
- (X^{(m)}) = resulting evidence;
- (epsilon_m) = omission/noise.

The interview can alter articulation, recall, categorization and salience. A self-administered item can be interpreted differently. EMA can sample a different temporal slice.

Therefore 009A2 studies **method-conditioned evidence**, not which method reads the "true mind."

## 2. Two acquisition experiments

### 2.1 009A2a · Matched-content acquisition experiment

Goal: isolate the effect of **response/interaction format** as much as possible.

The same focal experience and same conceptual domains are assessed through three matched-content methods:

- **M1 — self-administered fixed-response module**
- **M2 — fully structured interviewer module**
- **M3 — conversational phenomenological semi-structured interview**

The domain coverage is held as similar as practicable.

The methods differ deliberately in:

- interviewer interaction;
- opportunity for clarification;
- response format;
- branching/probing;
- participant-generated examples;
- tolerance of ambiguity/metaphor.

This is the cleaner acquisition-method experiment.

### 2.2 009A2b · Native-instrument ecological comparison

Goal: compare methods **as they are actually used**.

Candidate methods:

- EASE / EAWE / STEP-style phenomenological assessment;
- actual participant-completed self-report;
- conventional clinical symptom assessment;
- EMA/ESM;
- selected passive/contextual measures where explicitly consented.

Native instruments may differ in:

- construct coverage;
- time window;
- wording;
- intended use;
- scoring;
- burden.

Therefore A2b estimates practical method divergence, not a pure causal "format effect."

## 3. Focal-experience anchoring

A central problem is ensuring the methods are talking about the same experience.

### Preferred anchor

Use a recent, participant-confirmed focal episode sampled from a short EMA/event-capture period.

Example workflow:

1. participant completes 3–7 days of low-burden EMA;
2. EMA records timestamp and minimal contextual information;
3. one or two candidate focal episodes are selected using preregistered rules;
4. participant confirms which event is being discussed;
5. all A2a methods refer to that same episode.

### Why not rely only on retrospective diagnosis windows?

A six-month or lifetime score can be clinically useful but is a poor anchor for a method experiment because different reports may refer to different events.

## 4. Physical/context anchors

The project aims to preserve physical/contextual reality where independently observable, without treating third-person data as the truth of subjective meaning.

Define an optional contextual anchor vector:

[
W_t=(time,location,activity,social context,sleep,medication timing,physiology,ldots)
]

Possible ethically collected anchors:

- timestamp;
- coarse location category rather than exact GPS where possible;
- activity state;
- participant-recorded social company;
- sleep/wake timing;
- medication timing;
- optional wearable physiology;
- external event markers.

### Rule

(W_t) can constrain claims about context.

It cannot determine:

- ownership/mineness;
- agency as experienced;
- felt salience;
- meaning;
- reality quality;
- self-world boundary.

Third-person physical correspondence and first-person fidelity are reported separately.

## 5. Randomized order design

Repeated assessment can itself alter later answers.

Prior psychiatric assessment research has documented order effects, and EMA research recognizes assessment reactivity.

### Primary solution

Randomize participants to the six possible orders of M1/M2/M3:

- 123
- 132
- 213
- 231
- 312
- 321

Use balanced allocation where feasible.

### Two estimands

#### First-method estimand

Compare only the first administered method across randomized groups.

Advantages:

- no carryover from another study method;
- strongest estimate of acquisition-method effect.

Disadvantage:

- between-person rather than within-person.

#### Full crossover estimand

Use all three methods in every participant.

Advantages:

- direct within-person divergence;
- efficient descriptive comparison.

Disadvantages:

- carryover;
- priming;
- fatigue;
- articulation learning.

Model position/order explicitly.

## 6. Assessment intervals

For A2a, methods should be close enough in time that genuine state change is minimized, but not so close that fatigue is intolerable.

Candidate engineering schedule:

- focal episode confirmed;
- Method 1;
- neutral break/task;
- Method 2;
- neutral break/task;
- Method 3.

Record exact start/end times.

A sensitivity design can repeat one method after a longer interval to separate short-term reactivity from ordinary test-retest change.

## 7. Method content

### Common matched domains for A2a

Use a frozen subset of the relation ontology:

- ownership/mineness;
- agency;
- source attribution;
- self-other/world boundary;
- bodily experience;
- salience/familiarity;
- affect;
- temporal structure;
- context;
- meaning/interpretation;
- certainty.

### M1 · Self-administered

Properties:

- fixed wording;
- fixed response categories;
- optional brief free text after each domain;
- no interviewer clarification.

### M2 · Fully structured interviewer

Properties:

- same fixed core wording and order;
- standardized neutral clarification only;
- no open phenomenological probing.

### M3 · Phenomenological interview

Properties:

- conversational;
- participant examples required where relevant;
- interviewer may clarify terms;
- metaphor/uncertainty explicitly explored;
- no forced premature categorization.

## 8. Output representation before comparison

Acquisition method and later coding must be separated.

Each method produces raw evidence (X^{(m)}).

Then a common blinded encoding procedure maps each method output into:

[
Z^{(m,common)}
]

using the same episode graph / query-answer representation.

This avoids confounding:

[
acquisition method + different coding method
]

in the primary comparison.

Native method scores are preserved as secondary outcomes.

## 9. Primary outcomes

### 9.1 Acquisition divergence

For each pair of methods, quantify disagreement in the common representation:

- semantic disagreement;
- relation disagreement;
- context disagreement;
- temporal disagreement;
- uncertainty disagreement.

### 9.2 Additional-information yield

For each method, quantify information that is:

- unique to that method;
- corroborated by another method;
- contradicted by another method;
- unresolved.

Do not define "unique information" as automatically true.

### 9.3 Clarification gain

For M3 relative to fixed formats, estimate how often probing changes:

- category assignment;
- certainty;
- context;
- causal attribution;
- literal/metaphorical interpretation.

### 9.4 Participant endorsement

After all acquisition methods are complete, show participants carefully blinded/standardized reconstructions and ask:

- does this preserve what you meant?
- is anything important missing?
- is anything distorted?
- did the method make you answer in a way you would not naturally describe the experience?

## 10. Secondary outcomes

- burden;
- completion time;
- distress;
- fatigue;
- perceived understanding;
- perceived intrusiveness;
- interviewer-rated difficulty;
- missingness;
- abstention/uncertainty;
- evaluator confidence;
- native instrument scores;
- optional intended-use outcomes.

## 11. Physical-context concordance

Where a query concerns independently observable context, compare method reports to (W_t).

Examples:

- approximate time;
- location category;
- activity;
- presence/absence of another person;
- sleep state.

This yields a separate:

[
F_{physical}
]

It is **not** combined with phenomenological fidelity into one score.

## 12. Statistical model

### 12.1 First-method analysis

For outcome (Y):

[
Y=eta_0+eta_{method}+eta_{domain}+u_{person}+u_{episode}+epsilon
]

Because first method is randomized, (eta_{method}) has the cleanest causal interpretation available in the protocol.

### 12.2 Full crossover analysis

[
Y=eta_0+eta_{method}+eta_{position}+eta_{sequence}
+eta_{method	imes position}
+u_{person}+u_{episode}+u_{domain}+epsilon
]

Add evaluator effects when outcomes depend on blinded coding.

### 12.3 Multitrait–multimethod layer

Use MTMM/hierarchical latent-variable models to estimate:

- domain/trait variance;
- method variance;
- person variance;
- method × domain interactions.

Do not force a single latent "true psychopathology" unless model fit and theory support it.

## 13. Carryover and reactivity tests

Primary carryover indicators:

- method × position interaction;
- increased detail after phenomenological interview;
- shifts in certainty;
- shifts in terminology;
- self-reported "I had not thought of it that way before";
- change in distress/focus across methods.

If M3 strongly changes later responses, that is a scientific result about acquisition, not merely nuisance variance.

## 14. Pilot sample

Do not freeze confirmatory N yet.

A calibration pilot should allocate evenly across six method orders.

Useful engineering sizes:

- 36 participants = 6/order;
- 48 participants = 8/order;
- 60 participants = 10/order.

The pilot estimates:

- carryover magnitude;
- completion burden;
- method variance;
- domain × method effects;
- usable episode yield;
- coding reliability.

Final N is then simulation-calibrated.

## 15. Native-instrument A2b analysis

A2b should avoid calling disagreement "error."

For native tools report:

- convergence;
- unique content;
- method-specific content;
- intended-use validity;
- burden;
- predictive associations;
- participant preference/meaning preservation.

A native measure may be scientifically useful precisely because it samples a different construct or time scale.

## 16. EMA role

EMA is especially useful for:

- reducing retrospective recall;
- identifying focal episodes;
- quantifying temporal variability;
- measuring real-world context.

But EMA can itself produce reactivity and repeated-question burden.

Therefore record:

- prompt frequency;
- response latency;
- missingness;
- perceived reactivity;
- whether prompts changed attention to symptoms.

## 17. Safety and ethics

For psychosis-spectrum participants:

- assess capacity to consent;
- define distress/stopping rules;
- provide clinician escalation pathway where appropriate;
- avoid unnecessary repeated probing of destabilizing content;
- do not require exact GPS when coarse context suffices;
- allow participant refusal of any contextual sensor stream;
- separate research inference from clinical diagnosis.

## 18. Falsification

The acquisition hypothesis is weakened if:

- M1/M2/M3 produce near-identical common representations;
- order/carryover is negligible;
- phenomenological probing adds only verbosity;
- participant meaning ratings do not favor richer elicitation;
- method variance is much smaller than ordinary test-retest/state variance.

A null result would be highly informative: it would imply that simpler acquisition can preserve more than phenomenological theory predicts.

## 19. Literature anchors

- Nordgaard, Sass & Parnas (2013), DOI 10.1007/s00406-012-0366-z — interview process and subjectivity.
- Jensen et al. (1999), PMID 10821625 — counterbalanced structured-interview order effects.
- Y-BOCS interview vs self-report study, PMID 8870295 — method and order effects can be empirically tested.
- Psychosis EMA feasibility, PMCID PMC5369417 — real-world repeated assessment is feasible but has burden/awareness effects.
- Psychotic/mood symptom EMA convergence, PMCID PMC8195558 — EMA and standard clinical assessments can converge while sampling different temporal properties.
- EMA assessment-reactivity literature, e.g. PMCID PMC5075187 / PMC9120419 — repeated measurement can itself alter reported states.

## 20. Relationship to 009A1

009A1 should be executed first because it can be piloted using existing ethically usable source material.

009A2 requires purpose-collected multimethod data and is therefore a separate ethics/resource commitment.

The final ARIS4C009 measurement framework needs both:

[
	ext{total observed divergence}
approx
	ext{acquisition divergence}
+
	ext{encoding divergence}
+
	ext{state/time change}
+
	ext{interaction}
]

This is a conceptual decomposition, not assumed literal additivity.
