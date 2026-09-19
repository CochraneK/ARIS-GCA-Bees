# ARIS4C012 · Session log

Append substantial execution sessions in chronological order.

## 2026-09-19 · Continuity retrofit

- Added the standardized ARIS4C per-paper handoff package.
- Bootstrapped project context, current state, TODO, decision history, and a public-safe conversation record.
- Established Git as the cross-device / cross-account / cross-agent continuity surface.

## 2026-09-19 · Pre-deletion reconciliation

- Re-read the live Git state rather than relying on chat memory.
- Detected and resolved a status conflict:
  - older `process/STATUS.md` said Coder B was missing;
  - `paper.json`, handoff files, completed B data, and reliability outputs showed that Coder B had since completed.
- Verified independent WorkBuddy Coder B commit:
  `8f9ec0dd99e25ae0411fd4e06d2b4dbd1ef219d9`.
- Verified P01–P30 core B fields are complete.
- Verified reliability workflow output is `READY_FOR_ADJUDICATION`.
- Reinterpreted that workflow state correctly: mechanical completeness, not a scientific reliability pass.
- Recorded key raw reliability:
  - opposition_valid kappa 0.466;
  - OCI candidacy kappa 0.592;
  - primary_mechanism kappa 0;
  - 141 disagreement cells.
- Identified a measurement/instrument issue: A and B used inconsistent value vocabularies in several fields, so exact-string nominal agreement confounds lexical encoding with substantive disagreement.
- Added `process/PILOT0B_RELIABILITY_AUDIT.md`.
- Updated canonical `process/STATUS.md`.
- Updated the handoff package to make the next scientific step unambiguous:
  diagnostic adjudication -> controlled-vocabulary Schema v2 -> fresh A2/B2 Pilot -> only then full evidence-map screening.
- Prepared the repository so the current chat can be deleted without losing necessary project state.

## 2026-09-19 · Exhaustive Pilot 0B disagreement diagnosis

- Read the frozen raw Pilot 0B disagreement packet without modifying coder labels or raw reliability statistics.
- Classified all 141 disagreement cells into four diagnostic failure modes: lexical/token-vocabulary mismatch (30), schema-category overlap (24), source/metadata disagreement (26), and genuine conceptual disagreement (61).
- Added a reproducible diagnostic script plus row-level CSV, JSON summary, and process audit artifact.
- Kept `adjudicated_value` blank and preserved Pilot 0B as a failed v1 reliability gate rather than retroactively normalizing it into a pass.
- Next bounded unit: freeze the Schema v2 controlled vocabulary and validation form before drawing a fresh A2/B2 sample.

## 2026-09-19 · Schema v2 freeze

- Converted the pre-existing v2 proposal into a frozen controlled-vocabulary coding specification for fresh validation only.
- Removed the forced single primary-mechanism field in favor of orthogonal opposition, index-switch, mechanism, and evidence-mode vectors.
- Added exact allowed tokens, uncertainty rules, blinding rules, a blank v2 coding template, and prespecified reliability gates.
- Preserved Pilot 0B raw labels/statistics unchanged.
- Next bounded unit is fresh balanced validation-sample construction; independent A2/B2 coding remains a later separate execution gate.

## 2026-09-19 · Fresh v2 validation sample freeze

- Re-read the 165-record reproducible retrieval frame and Pilot 0B coder-A identifiers.
- Excluded all Pilot 0B records by stable identifier/title, leaving 155 fresh candidates.
- Froze a deterministic 30-record validation sample with 5 records in each of six strata and zero Pilot 0B overlap.
- Added a reproducible draw script, manifest, freeze contract, and audit note.
- Next bounded unit is to materialize identical blind evidence packets and hash them before independent A2/B2 coding.
