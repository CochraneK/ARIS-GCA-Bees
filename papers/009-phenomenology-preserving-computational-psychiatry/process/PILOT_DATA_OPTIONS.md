# ARIS4C009 · Pilot data options

**Status:** source triage completed 2026-09-19.

The objective is to move 009A1 from conceptual design to empirical calibration without pretending that every available psychiatric corpus measures phenomenological self-disorder.

## Tier 0 · DAIS-C — immediate open-data engineering pilot

**Dataset:** Discussing Abstract Ideas in Schizophrenia Corpus (DAIS-C)  
**Repository:** UK Data Service ReShare, study 855021  
**DOI:** 10.5255/UKDA-SN-855021  
**Paper:** Delgaram-Nejad et al. (2023), DOI 10.1016/j.acorp.2023.100069

### Why it is useful

The public record reports:

- 15 speakers with a formal schizophrenia diagnosis;
- 14 non-clinical comparison speakers;
- naturalistic/unstructured interviews;
- detailed true-verbatim transcription;
- interviewer speech retained;
- text plus metadata/participant-facing documentation;
- open download without registration.

This is unusually suitable for testing whether the 009A1 machinery can operate on **real schizophrenia interviews** rather than synthetic examples.

### What it can establish

DAIS-C can test:

- corpus ingestion;
- provenance preservation;
- episode segmentation;
- independent query construction;
- relation-graph annotation;
- source uncertainty handling;
- R1 structured-graph generation;
- R3P/R4P projection feasibility;
- evaluator blinding/QC;
- representation-rate accounting;
- rater burden;
- query redundancy;
- preliminary inter-rater reliability.

### What it cannot establish

The interviews were designed around linguistic creativity, abstract ideas and associated tasks rather than EASE/EAWE/STEP phenomenology.

Therefore DAIS-C **cannot** by itself establish:

- self-disorder coverage;
- EASE fidelity;
- prevalence of phenomenological abnormalities;
- superiority of phenomenological interviewing;
- the complete fidelity frontier for psychosis.

DAIS-C is Pilot-0: a real-clinical-data methods calibration.

## Tier 1 · AMP-SCZ — high-value psychosis-risk validation

**Dataset:** Accelerating Medicines Partnership Schizophrenia (AMP-SCZ)  
**Access:** NIMH Data Archive under approved Data Use Certification  
**Current reference materials:** AMP-SCZ data-release manuals are publicly documented; underlying participant-level data require controlled access.

### Why it is especially valuable

Current releases include combinations of:

- clinical-high-risk participants and comparison participants;
- PSYCHS semi-structured assessment;
- redacted partial PSYCHS transcripts;
- open-ended interview language samples;
- audio diaries/language samples;
- behavioral and clinical measures;
- EEG;
- MRI/dMRI/rs-fMRI;
- actigraphy;
- smartphone data.

This makes AMP-SCZ a much stronger substrate for the later 009 architecture because acquisition evidence can eventually be linked to third-person contextual and biological streams without defining subjective meaning by those streams.

### Candidate 009 uses

- validate A1 representations on psychosis-relevant interview material;
- compare open interview versus structured PSYCHS evidence;
- study acquisition-method divergence;
- add temporal/context constraints;
- later test whether retained phenomenological structure adds prediction beyond standard severity scores.

### Constraint

No AMP-SCZ participant data should be copied into the public ARIS4C repository.

Any use must comply with NDA approval, project authorization and data-sharing rules.

## Tier 2 · Purpose-collected phenomenological cohort

This is the ideal confirmatory route if resources permit.

Candidate acquisition battery:

- EASE;
- EAWE;
- STEP;
- conventional clinical symptom assessment;
- matched-content self-administered module;
- EMA focal-event capture;
- optional contextual sensing;
- later EEG/fMRI/behavioral tasks.

This tier is needed if the final paper aims to make direct claims about phenomenological self/world/time structure rather than only representation methodology.

## Engineering fallback · DAIC-WOZ

DAIC-WOZ contains 189 semi-structured clinical interviews with transcripts, audio/video and questionnaire data and is available to eligible academic/non-profit researchers upon application.

It is useful for:

- testing interview parsers at larger scale;
- representation-rate experiments;
- depression/distress-oriented generalization;
- multimodal engineering.

It is **not** a psychosis phenomenology dataset and must not be used as evidence for schizophrenia-specific hypotheses.

## Recommended sequence

1. **DAIS-C Pilot-0** — run the full A1 engineering pipeline on open schizophrenia interview data.
2. **AMP-SCZ application/feasibility** — establish whether the needed transcript and linked-variable access can be obtained.
3. **DAIS-C reliability pilot** — independent raters calibrate source/query/graph rules.
4. **AMP-SCZ Pilot-1** — validate on psychosis-risk/PSYCHS material if access is granted.
5. **Purpose-collected Tier-2** — only if the paper proceeds to direct phenomenological claims.

## Public-repository rule

Even for open psychiatric corpora:

- do not mirror raw transcripts into ARIS4C;
- do not publish participant-level quotations merely because they are publicly downloadable;
- record source DOI/URL, version and archive checksum;
- process source data at runtime or in approved local storage;
- commit only non-identifying aggregate inventory and explicitly approved derived metadata.

This rule is stricter than minimum availability requirements by design.
