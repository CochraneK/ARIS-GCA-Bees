# ARIS4C010 · Ethics / Recruitment Gate Checklist

This checklist is organizational documentation, not ethics approval or legal advice.

## Institutional status

Before recruitment, record:

- institution / responsible investigator: **TBD**
- ethics committee / IRB / REC process: **TBD**
- protocol/application ID: **TBD**
- approval / exemption / determination date: **TBD**
- approved recruitment population: **TBD**
- approved compensation: **TBD**
- approved data retention period: **TBD**
- approved storage location: **TBD**

No field should be guessed by the repository.

## Participant information should explain

- study purpose at a non-deceptive level;
- approximate task type and duration;
- that some semantic judgments may be unusual or difficult;
- voluntary participation and withdrawal procedure;
- compensation rules;
- what data are collected;
- whether response time is collected;
- whether any demographic/language data are collected;
- confidentiality/pseudonymization;
- data retention and contact route;
- complaints/ethics contact required by the institution.

## Data minimization

The current calibration does not inherently require:

- legal name;
- home address;
- phone number;
- precise location;
- medical information;
- political/religious information.

Do not add such fields merely because a survey platform offers them.

If demographic covariates are scientifically justified, pre-specify them and collect the minimum needed.

## Language eligibility

Calibration60 uses English OEWN senses and English query wording.

Define an English comprehension criterion appropriate to the target population.

Do not call English calibration results language-universal.

## Recruitment balance

Protocol/form allocation must be independent of participant responses.

Maintain a form-assignment ledger containing only the minimum administration data needed to prevent accidental overuse of a form.

## Standalone interface limitation

The no-backend HTML interface is suitable for QA or an approved local workflow.

It deliberately does not implement:

- consent infrastructure;
- authentication;
- secure server upload;
- payment;
- recruitment-platform completion codes.

Those must be provided by the approved study environment if required.

## Stop conditions during pilot administration

Pause recruitment if:

- a form/export is technically corrupted;
- participant files cannot be mapped back to canonical forms;
- instructions contain a discovered material error;
- a response label is systematically misunderstood due to wording;
- an institutional/privacy requirement is not being met.

Version the affected materials before resuming; do not silently edit live stimuli.
