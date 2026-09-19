# ARIS4C009 · Boundary-rater manual

## Task

You are **not** rating psychopathology, diagnosis, truthfulness, intelligence, coherence of
the person, or clinical severity.

You are rating one narrow measurement question:

> **Does this excerpt form a usable information window for a later blinded reconstruction test?**

A usable window should contain enough local context to support at least one nontrivial
question while avoiding unnecessary mixing of unrelated topics.

## What raters are blinded to

During primary rating you must not know:

- whether the source is clinical or comparison;
- whether the window came from the 20- or 40-word structural rule;
- participant identity;
- source file name;
- the other rater's decision.

Do not open `private_key.json` until both primary rating files are frozen.

## Training order

1. Read this manual.
2. Independently rate the synthetic practice cases.
3. Open the synthetic answer key and discuss disagreements.
4. Independently rate the 20 private real-data `training.tsv` items.
5. Only after both training ratings are complete, open `training_key.json` and discuss.
6. Resolve rule interpretation questions.
7. Freeze the rule.
8. Independently rate the 140 primary/stress items.
9. Do not discuss primary items until both files are frozen.

Training items never enter the primary agreement estimate.

## Fields

### 1. coherent_boundary — yes / no

Ask:

> Does the excerpt begin and end in a way that makes it interpretable as one local
> conversational unit?

**Yes** does not mean the participant's account is logically consistent or clinically
ordinary.

Mark **no** when the window obviously depends on omitted adjacent material or ends in
the middle of an unresolved local unit.

Examples of boundary problems:

- starts with “yes, exactly” but the relevant proposition is missing;
- pronouns/references cannot be resolved because their antecedent is outside the window;
- ends with an interviewer question whose answer is outside the window;
- clearly begins halfway through an explanation.

### 2. sufficient_nontrivial — yes / no

Ask:

> Could an independent evaluator answer at least one meaningful source-grounded
> question from this window?

A **nontrivial** question goes beyond merely repeating a single yes/no answer.

Possible question families:

- what happened?
- what did the participant mean or believe?
- what relation existed between two events/ideas?
- what caused or preceded what?
- what context changed the interpretation?
- what was certain versus uncertain?
- what temporal order was described?
- how did the participant distinguish two experiences?

A short answer can still be sufficient if the interviewer prompt supplies the needed
context.

### 3. mixed_unrelated_topics — yes / no

Ask:

> Does this window combine two or more topics that could be separated without losing
> the meaning of either?

Do **not** mark mixed merely because:

- the participant gives an example;
- the participant self-corrects;
- the participant moves between cause and consequence;
- the interviewer clarifies the same topic;
- one experience is compared with another.

Mark mixed when the window contains genuinely separable topic units joined only because
of the structural word threshold.

### 4. recommended_action

Choose exactly one:

#### keep

Use the window as it is.

Typical profile:

- coherent boundary;
- sufficient information;
- no unrelated topic mixing.

#### merge

The window is too dependent on adjacent context.

Use when:

- answer is too short to stand alone;
- opening reference depends on immediately previous material;
- window ends before local meaning is resolved.

“Merge” means *add adjacent context*, not “the participant said too little.”

#### split

The window is too broad.

Use when:

- two separable topics were structurally combined;
- one long response contains multiple clearly independent local units;
- the later reconstruction task would benefit from treating them separately.

#### reject

The source window is unsuitable as an annotation unit even after obvious neighboring
context is considered.

Examples:

- transcription/format failure;
- no substantive participant content;
- non-conversational technical material accidentally parsed as dialogue.

Use reject sparingly. Ordinary ambiguity is **not** grounds for rejection.

### 5. confidence_1_5

- 1 = highly uncertain;
- 2 = uncertain;
- 3 = moderate;
- 4 = confident;
- 5 = very confident.

Low confidence is valid data.

## Do not evaluate the participant

The following are **not** rating criteria:

- whether a belief is factually correct;
- whether an experience is bizarre;
- whether language is unusual;
- whether grammar is polished;
- whether the account is clinically plausible;
- whether the participant seems symptomatic.

A metaphorical, uncertain, fragmented, or unusual experience can still be a perfectly
usable source window.

## Preserve uncertainty

If the participant says they do not know, are unsure, changed their mind, or offer
multiple alternatives, that uncertainty may itself be important information.

Do not mark a window insufficient merely because it lacks a single definite answer.

## Interviewer speech matters

Interviewer prompts are part of the acquisition record.

They can:

- establish referents;
- constrain meaning;
- introduce assumptions;
- clarify time/context;
- shape the participant's response.

Do not strip interviewer speech mentally when judging boundary sufficiency.

## What “coherent” means here

“Coherent” refers only to the **window boundary**, not to formal thought disorder or
discourse quality.

Never convert the boundary task into a rating of the speaker.

## Adjudication after independent rating

After both primary rating files are frozen:

1. compute agreement first;
2. inspect disagreements second;
3. distinguish rule ambiguity from genuine judgment disagreement;
4. do not retroactively alter the original independent files;
5. store any adjudicated decision as a separate layer.

## Privacy

The private packet contains source interview text.

Do not:

- paste excerpts into public issues;
- commit TSV files;
- upload packet folders as GitHub artifacts;
- share participant text outside the permitted research context.

Only aggregate calibration outputs may enter public ARIS4C after review.
