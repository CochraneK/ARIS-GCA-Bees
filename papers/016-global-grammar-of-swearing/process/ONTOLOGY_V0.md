# ARIS4C016 Taboo-Language Ontology v0

Updated: 2026-09-18

## Why a new ontology is needed

The Phase-0 audit shows that the source dataset's category field mixes
different conceptual levels:

- **insult** is mainly a pragmatic function;
- **slur** is mainly a socially targeted/identity-indexing attack class;
- **sexual**, **scatological**, and **blasphemy** are semantic taboo sources;
- local labels may instead encode topic, historical context, social group,
  morphology, or annotator judgement.

These are not mutually exclusive categories. Treating them as one flat
classification creates artificial cross-sample differences in coding style.

ARIS4C016 therefore uses a **multi-axis ontology**. A single expression can
receive one or more values on each axis.

## Axis A — semantic taboo source

Primary question: *what semantic material supplies the taboo force?*

Canonical v0 values:

- `SEX_SEXUALITY`
- `GENITAL_BODY`
- `EXCRETION_DISGUST`
- `RELIGION_SACRED`
- `KINSHIP_ANCESTRY`
- `DEATH_DISEASE`
- `ANIMAL_DEHUMANIZATION`
- `INTELLIGENCE_COMPETENCE`
- `MORALITY_CHARACTER`
- `APPEARANCE_ABILITY`
- `VIOLENCE_HARM`
- `SUBSTANCE_ILLEGALITY`
- `POLITICS_HISTORY`
- `OTHER_SEMANTIC`
- `UNRESOLVED_LOCAL`

Multiple semantic sources are allowed.

## Axis B — target

Primary question: *who or what is being targeted?*

- `NO_EXPLICIT_TARGET`
- `SELF`
- `INTERLOCUTOR`
- `THIRD_PERSON`
- `KIN`
- `ANCESTOR`
- `SOCIAL_GROUP`
- `SACRED_ENTITY`
- `INSTITUTION`
- `UNKNOWN_TARGET`

Target is conceptually separate from semantic source.

## Axis C — pragmatic function

Primary question: *what is the expression doing in context?*

- `DIRECT_INSULT`
- `EXPLETIVE_INTERJECTION`
- `INTENSIFIER_EMPHASIS`
- `CURSE_WISH_HARM`
- `THREAT`
- `DISMISSAL_COMMAND`
- `TEASING_BANTER`
- `SOLIDARITY_IN_GROUP`
- `QUOTED_METALINGUISTIC`
- `OTHER_PRAGMATIC`
- `CONTEXT_REQUIRED`

A lexical inventory collected without sentence context may not permit reliable
function coding; `CONTEXT_REQUIRED` is preferable to guessing.

## Axis D — social-indexical basis

Primary question: *does the expression derive force from a socially indexed
identity/status category?*

- `NONE_OBVIOUS`
- `RACE_ETHNICITY_NATIONALITY`
- `GENDER_SEX`
- `SEXUAL_ORIENTATION`
- `DISABILITY_HEALTH`
- `AGE`
- `CLASS_STATUS_OCCUPATION`
- `RELIGIOUS_IDENTITY`
- `POLITICAL_IDENTITY`
- `OTHER_IDENTITY`
- `UNRESOLVED_IDENTITY`

This axis is where many expressions traditionally called "slurs" are
represented. The project should not infer a protected/social identity solely
from an English gloss.

## Axis E — taboo mechanism

Primary question: *how is derogation/transgression produced?*

- `POLLUTION_DISGUST`
- `SEXUALIZATION`
- `DEHUMANIZATION`
- `INCOMPETENCE`
- `IMMORALITY`
- `SACRILEGE`
- `KINSHIP_DISHONOR`
- `STATUS_DEGRADATION`
- `THREAT_HARM`
- `IDENTITY_DEROGATION`
- `OTHER_MECHANISM`
- `UNKNOWN_MECHANISM`

This is an interpretive layer and requires stronger evidence than raw lexical
form.

## Axis F — linguistic form

Primary question: *what linguistic construction carries the expression?*

Fields rather than mutually exclusive classes:

- lexical unit / multi-word expression;
- part of speech;
- compounding;
- derivation;
- reduplication;
- metaphor/metonymy;
- euphemism/minced form;
- orthographic masking;
- borrowing/code-switching;
- phonological representation where available.

## Confidence

Every mapped value receives:

- `HIGH` — directly supported by native-language annotation/context;
- `MEDIUM` — defensible mapping from source annotation plus translation;
- `LOW` — translation-based inference only;
- `UNRESOLVED` — insufficient evidence.

Low-confidence mappings are excluded from confirmatory prevalence analyses.

## Mapping policy for the Phase-0 dataset

1. Never overwrite source labels.
2. Store `raw_category1/2/3` unchanged.
3. Normalize obvious spelling variants separately from conceptual mapping.
4. Do not force local categories into a global class.
5. Do not use English translation alone to assign identity or pragmatic
   function.
6. Allow multi-label coding on every substantive axis.
7. Record annotator and mapping-rule provenance.
8. Audit a stratified sample with independent coding before full conversion.

## Key methodological implication

Cross-cultural comparison should operate on **axes**, not on the original flat
category field.

For example, an expression can simultaneously be:

- semantic source: `SEX_SEXUALITY`;
- target: `KIN`;
- function: `DIRECT_INSULT`;
- social-indexical basis: `GENDER_SEX`;
- mechanism: `KINSHIP_DISHONOR`.

A flat label such as "insult" or "sexual" loses this structure and makes
different laboratories' annotation habits appear as cultural differences.

## Status

v0 is a research ontology draft, not a validated gold standard. Promotion to
v1 requires:
- native-speaker review across multiple language families;
- independent coder reliability;
- unresolved-label analysis;
- evidence that the axes improve cross-sample comparability without erasing
  meaningful local categories.
