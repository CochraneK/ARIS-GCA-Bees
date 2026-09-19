# ARIS4C009 Pilot-1 · AMP-SCZ minimum-access plan

**Prepared:** 2026-09-19  
**Target dataset:** AMP-SCZ Release 4.0  
**Reference manual:** DOI 10.5281/zenodo.21923460  
**NDA release study:** DOI 10.15154/5wdf-9136

## Why AMP-SCZ is the preferred Pilot-1

DAIS-C is sufficient for open-data engineering but was not designed around psychosis-risk
phenomenology.

AMP-SCZ provides a stronger bridge because the same cohort contains:

- PSYCHS semi-structured clinical assessment;
- open-ended language samples;
- longitudinal language sampling;
- clinical/dimensional measures;
- daily smartphone survey data;
- passive smartphone sensing;
- actigraphy;
- EEG;
- MRI/dMRI/rs-fMRI;
- treatment and health-service variables.

This makes it possible to test richer representations without treating any single
third-person modality as the definition of subjective experience.

## Release-4 availability anchor

The public Release-4 availability record contains 2,438 subject rows and includes
structures such as:

- `ampscz_psychs01_screening/baseline/month_1/month_2/month_3`;
- `langsamp01_screening_psychs`;
- `langsamp01_baseline_open`;
- `langsamp01_baseline_psychs`;
- `langsamp01_month_1_psychs`;
- `langsamp01_month_2_open`;
- `langsamp01_month_2_psychs`;
- `langsamp01_month_3_psychs`;
- `langsamp01_features_open/psychs/diary`;
- `ampscz_sp_survey01`;
- `ampscz_sp_sensors01`;
- `actirec01`;
- `ampscz_eeg_featuresrest01`;
- `ampscz_eeg_featurestask01`;
- `image03` / `imagingcollection01`.

Presence in the availability record does not imply every subject has every modality.

## Access principle

Request the **minimum data necessary for each gate**.

Do not request raw geolocation, raw imaging, raw EEG, or raw speech merely because they
exist.

## Tier 1 request · acquisition + clinical evidence

This is the minimum useful Pilot-1 package.

### Required

- subject linkage key allowed by NDA;
- cohort/group;
- site and language where available;
- visit;
- age/time variables required for longitudinal matching;
- PSYCHS structured data;
- redacted open-ended interview transcripts;
- redacted PSYCHS language-sample transcripts or approved transcript-level derivatives;
- language-sample acquisition metadata.

### Strongly useful

- BPRS or comparable conventional symptom measure;
- treatment/medication timing;
- basic functioning measures;
- minimal demographics needed to test measurement heterogeneity.

### Not required initially

- exact geolocation;
- raw audio/video;
- raw MRI;
- raw EEG;
- fluid biomarkers.

## Tier 1 studies

### P1 · Same-source encoding fidelity

Use **one open-ended transcript as the fixed source**.

Generate:

- R0 source;
- R1 episode/relation graph;
- R2 phenomenology-informed structured representation;
- R3P questionnaire-format projection;
- R4P conventional clinical projection;
- optional compact representation.

This is the cleanest extension of 009A1.

### P2 · Observational acquisition divergence

For participants with open-ended and PSYCHS samples at the same visit window:

[
X^{open}_{it} quad vs quad X^{PSYCHS}_{it}
]

Compare:

- domain coverage;
- relation coverage;
- uncertainty;
- context;
- temporal information;
- unique/non-overlapping information.

This is **not** a randomized acquisition experiment.

Differences can reflect:

- prompt structure;
- intended construct;
- interviewer behavior;
- timing;
- participant state;
- recording/transcription process.

Therefore P2 estimates naturalistic method divergence, not a pure causal format effect.

## Tier 2 request · physical/context constraints

Add only after Tier 1 pipeline is stable.

Candidate structures:

- daily smartphone survey;
- actigraphy;
- screen state;
- accelerometry;
- sleep/activity derivatives;
- coarse mobility/context summaries.

### Geolocation rule

Prefer derived/coarsened features such as:

- time at home-like anchor;
- mobility radius;
- location entropy;
- transition count;

over exact coordinate histories.

Exact geolocation should be requested only if a preregistered question genuinely needs it.

## Tier 2 study

For an interview/episode at time (t), construct:

[
W_t=(sleep,activity,mobility,screen use,EMA,ldots)
]

Use (W_t) to constrain contextual claims such as:

- sleep disruption;
- activity change;
- mobility;
- daily affect/self-report.

Do **not** use (W_t) to decide whether an experience felt self-authored, salient,
unreal, owned, or meaningful.

## Tier 3 request · cross-level constraints

Only after source and context measurement layers pass.

Prefer **derived features first**:

- EEG rest/task features;
- imaging-derived measures if available;
- later raw EEG/MRI only when a specific mechanistic hypothesis requires reprocessing.

## Tier 3 study

Test whether phenomenological/relational structure adds out-of-sample information beyond:

- PSYCHS severity;
- conventional symptoms;
- existing speech features;
- context features.

Neural concordance is a validation channel, not subjective ground truth.

## Participant/visit selection

### Primary Pilot-1 cohort

Select participants with:

1. usable redacted open transcript at baseline;
2. PSYCHS structured assessment near the same visit;
3. usable PSYCHS language sample where available.

Month-2 repeated pairs provide longitudinal replication.

### Later longitudinal cohort

Add month 1/month 3 PSYCHS language samples and daily context streams.

## Leakage prevention

All train/validation/test splits are by participant.

No visit from a participant in the test set may appear in model training.

Site and language should be monitored because acquisition and transcription processes may differ.

## Missingness

Do not use complete-case filtering as the default.

Model/report:

- modality availability;
- visit availability;
- transcript availability;
- passive-sensing missingness;
- site/device missingness.

Missingness itself may be informative and must not be silently erased.

## Data minimization order

1. transcripts + PSYCHS + visit linkage;
2. minimal clinical covariates;
3. derived phone/actigraphy context;
4. derived EEG/imaging;
5. raw high-dimensional modalities only when justified.

## Public repository boundary

No controlled-access AMP-SCZ participant data enter public ARIS4C.

Public artifacts may contain:

- analysis code;
- NDA structure names;
- preregistered variable families;
- aggregate non-disclosive results permitted by the DUC;
- provenance and software versions.

## Pilot-1 pass condition

Pilot-1 passes if the representation-fidelity framework can be reproduced on a
psychosis-risk dataset whose acquisition, clinical, contextual and cross-modal layers
are explicitly separated and linked without treating any one layer as latent truth.

## Sources

- AMP-SCZ Release 4.0 Data Reference Manual, DOI 10.5281/zenodo.21923460.
- NIMH Data Archive AMP-SCZ Release study, DOI 10.15154/5wdf-9136.
- AMP-SCZ observational study SOPs and study-design publications.
