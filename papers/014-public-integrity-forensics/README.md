# ARIS4C014 — Public Integrity Forensics

## Working title

**Public Integrity Forensics: An Auditable Multi-Source Agent for Corruption-Risk Screening from Open Data**

## Agent name

**OpenIntegrity**

## Core question

Can a modular, applicability-aware agent combine public procurement, corporate ownership, beneficial ownership, public-office/PEP, sanctions/debarment, offshore-entity, disclosure, and document/network signals to surface high-value corruption-risk leads while preserving provenance, reproducibility, calibration, and a strict distinction between anomalies, conflicts of interest, administrative irregularities, and proven corruption?

## Relationship to ARIS4C011

014 is a separate project that **inherits the forensic architecture of 011** rather than merging with it.

Reused invariants:

1. applicability routing before detection;
2. PASS is different from ABSTAIN / NOT_APPLICABLE;
3. detector outputs are findings, not accusations;
4. independent evidence families are tracked explicitly;
5. weak heuristics cannot become high-priority findings by themselves;
6. an Evidence Graph stores source-level provenance;
7. a critic layer checks entity resolution, temporal leakage, duplicated evidence, and benign explanations;
8. evaluation is issue/lead-level, not a single opaque "corruption score".

The domain changes from scientific manuscripts to public-integrity records.

## Why this is not an "AI corruption detector"

OpenIntegrity does **not** infer intent, guilt, criminal liability, or political worthiness.

Its atomic output is an auditable lead:

- what public records were checked;
- whether each check was applicable;
- which entities were resolved and with what uncertainty;
- which rule/model triggered;
- the exact source records and dates;
- whether the finding can be reproduced;
- what benign explanations remain;
- what independent evidence corroborates it;
- what a human reviewer should verify next.

An unusual contract may be legitimate. A PEP connection may be entirely lawful. An offshore company is not evidence of wrongdoing. A company appearing on a sanctions/debarment list is an externally verifiable fact, but must be temporally and jurisdictionally interpreted.

## Initial scope

### Core, jurisdiction-agnostic layer

- procurement and contract lifecycle;
- suppliers and contracting authorities;
- companies and corporate officers;
- beneficial ownership;
- public office / PEP roles;
- sanctions and debarment;
- offshore entity relationships;
- entity resolution and temporal alignment;
- graph/network analysis;
- deterministic arithmetic and threshold checks;
- anomaly detection;
- document similarity where lawful public tender documents exist.

### Jurisdiction plugins

- political donations;
- lobbying registers;
- public officials' asset/interests declarations;
- land/property ownership;
- grants and subsidies;
- court/enforcement decisions;
- public audit findings;
- revolving-door/employment records.

## Initial public-data backbone

- Open Contracting Data Standard (OCDS)
- Open Contracting Partnership procurement red flags
- USAspending API
- EU TED Search API / TED Open Data
- Companies House Public Data API and PSC records
- Beneficial Ownership Data Standard (BODS) / Open Ownership tools
- World Bank debarred and cross-debarred entities
- ICIJ Offshore Leaks Database
- OpenSanctions PEP/sanctions data where licensing permits

Each source adapter must record retrieval time, source URL, licence/access terms, schema version, and raw-record identifiers.

## Primary detector families

1. procurement-process red flags;
2. price/value and threshold anomalies;
3. supplier concentration and repeated-award structure;
4. temporal anomalies;
5. corporate/beneficial-ownership opacity and inconsistency;
6. conflict-of-interest / public-office relationship signals;
7. sanctions/debarment/enforcement matches;
8. cross-source identity and provenance contradictions;
9. document/text similarity and coordinated-bidding signals;
10. graph/network anomalies;
11. weak numerical heuristics (e.g. Benford/round-number patterns) only when assumptions justify them.

## Primary estimand

The primary target is **verified lead yield at a fixed human-review burden**, not "corruption accuracy".

Candidate metrics:

- verified issues per 100 reviewed alerts;
- recall of historically documented issue types among eligible cases;
- alerts per contract/entity;
- reviewer minutes per verified issue;
- lead time relative to an official audit/sanction/enforcement finding;
- entity-resolution false-match rate;
- abstention rate when required data are absent.

## Benchmark design

Two tracks are inherited from 011 and adapted:

### Track A — temporally blind risk screening

Only records that would have been publicly available before a defined cutoff may be used. Later audit findings, sanctions, convictions, or investigative reports may define outcomes but cannot leak into features.

### Track B — open-world integrity triage

All lawful public sources may be used to assemble a present-day evidence graph and rank records for human review.

Records without known adverse findings are **no-known-finding comparators**, never "clean" controls.

## Non-negotiable safeguards

- No detector may emit `corruption_inference=true`; detector-level value is always false.
- Protected characteristics, nationality, ethnicity, religion, and ordinary political affiliation are not suspicion features.
- Country can be used for source routing, legal context, market baselines, and data-availability calibration, not as an intrinsic corruption prior.
- PEP status is a relationship/context feature, not wrongdoing.
- Offshore ownership is not wrongdoing.
- Name-only matches cannot be treated as identity matches.
- Later sanctions/audits cannot leak into Track A features.
- Benford, round-number, stylometric, and generic anomaly scores default to weak evidence.
- Every high-priority lead must expose source records and at least one reproducible path for human verification.
- Public release must avoid defamatory wording and distinguish allegations, official findings, and model-generated anomalies.

## Current state

**INITIAL DESIGN + AGENT SKELETON.**

Next gates:

1. freeze the 014 detector taxonomy and evidence semantics;
2. implement normalized source schemas and source adapters;
3. build a synthetic Pilot 0 that tests routing, abstention, dependency groups, and evidence fusion;
4. construct a small real-data Pilot 1 from one procurement jurisdiction plus company/ownership data;
5. build a temporally safe benchmark using concluded public cases and matched no-known-finding comparators.
