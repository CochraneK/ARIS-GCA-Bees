# Pilot 1 protocol — UK identifier-first public-integrity graph

Status: pre-analysis engineering protocol  
Date: 2026-09-18

## Purpose

Pilot 1 tests whether OpenIntegrity can build a reproducible multi-source public-integrity graph from real UK public records without relying on name-only joins or outcome leakage.

This is a source-coverage, entity-resolution, and review-yield study. It is not an attempt to estimate a person's, company's, agency's, or country's "corruption score".

## Why the UK is the first Pilot 1 jurisdiction

Selection is based on machine joinability, not presumed corruption prevalence.

The UK provides:

- Find a Tender OCDS output for regulated procurement;
- Contracts Finder OCDS output for additional procurement coverage;
- PPON organisation identifiers in the central digital platform;
- Companies House identifiers in procurement records when supplied;
- Companies House company and PSC/beneficial-control records;
- public procurement lifecycle identifiers (OCIDs);
- official source timestamps suitable for building a time-aware evidence graph.

A live ARIS4C014 smoke on 2026-09-18 retrieved 50 recent Find a Tender award-stage releases, normalized them into 58 award cases, and found 21 cases with direct `GB-COH` supplier identifiers (36.2% in that bounded convenience sample). This number is a feasibility observation, not a population estimate.

The same smoke found no `numberOfTenderers` coverage in those award cases. A second smoke fetched complete OCDS record packages for eight identifier-joinable OCIDs and still found zero bidder-count coverage in eleven award cases. Therefore FTS is currently treated as strong for award/company identity but not assumed to support every competition detector.

## Locked source roles

### Find a Tender

Primary role:
- regulated procurement lifecycle;
- OCID;
- award;
- supplier identifiers;
- PPON;
- Companies House identifier when published;
- procurement method and other notice-level facts.

Do not infer bidder count when `numberOfTenderers` is absent.

### Contracts Finder

Complementary role:
- additional UK procurement notices;
- OCDS search/record lifecycle;
- supplier Companies House identifiers where published;
- possible additional competition-process fields.

Its empirical contribution is measured rather than assumed.

### Companies House

Primary role:
- stable company identity;
- incorporation date;
- persons with significant control;
- control/ownership relationships;
- notified/ceased dates when present.

API retrieval requires credentials. Secrets must be supplied through runtime secret storage and never committed.

A current Companies House response is not automatically a historically complete ownership snapshot. Track A requires evidence that the relevant record was publicly available by the cutoff.

## Pilot 1A — source/joinability feasibility

### Sampling frame

Freeze an explicit UTC retrieval window before collection.

Initial target:
- Find a Tender award-stage releases in the fixed window;
- Contracts Finder award-stage releases in the fixed window;
- all award cases generated from those releases up to the preregistered cap.

### Primary engineering endpoints

1. percentage of award cases with a direct stable supplier identifier;
2. percentage with direct `GB-COH`;
3. percentage with procurement-competition coverage;
4. percentage successfully joined to a Companies House company profile;
5. percentage with PSC/control records;
6. source-family abstention rate;
7. entity-resolution conflict rate;
8. parser/error rate.

These are data-pipeline outcomes, not corruption outcomes.

### Negative controls

The pipeline must continue to demonstrate:

- no company-name-only merge when a stable identifier is absent;
- no person-name-only merge;
- no offshore-only high-priority lead;
- no PEP/public-office-only wrongdoing inference;
- no PASS when the required source family was never loaded;
- no future sanction/audit backfilled into a historical feature set.

## Pilot 1B — detector feasibility

Run only detectors whose required fields are actually covered.

Candidate deterministic/contextual checks:

- supplier incorporated shortly before award;
- direct-award / limited-method observations where explicitly published;
- configured threshold proximity only after jurisdiction/rule mapping;
- cross-contract splitting only with an explicit comparable-procurement key and applicable threshold rule;
- supplier concentration only relative to a defined authority/sector/time reference population;
- ownership/public-office links only after identity and temporal validation;
- debarment only with a dated official/approved source.

Primary output:
detector applicability and review packets.

Do not report a global corruption score or a "top corrupt suppliers" ranking.

## Pilot 1C — benchmark bridge

Real-world detector performance requires adjudicated or documented outcomes.

Cases enter Track A only when:

- an outcome class is defined independently of the feature set;
- a source cutoff predates the outcome;
- each feature source has a defensible public-availability date;
- later audits, sanctions, investigations, news reports, and registry updates are excluded from features;
- historical ownership validity is checked;
- outcome labels are removed from model inputs.

Comparators are described as `no_known_adverse_finding`, never confirmed clean.

## Identifier policy

Automatic joins may use:

1. exact stable identifier;
2. official cross-registry identifier;
3. name plus multiple independent corroborating attributes under the entity-resolution protocol.

Name-only identity:
`ABSTAIN`.

A PPON and Companies House number can coexist for an organisation. Preserve both identifiers rather than replacing one with the other.

## Snapshot policy

Every raw record used in analysis should preserve, when available:

- source name;
- source record ID;
- source URL;
- raw SHA-256;
- parser version;
- retrieved_at;
- published_at / first_public_at;
- valid_from;
- valid_to.

Retrieval time must never substitute for an unknown publication time.

## Review-priority policy

Priority remains a human-review ordering, not a probability of corruption.

- E5-only evidence cannot be HIGH.
- Missing coverage cannot be negative evidence.
- Correlated signals share a dependency group.
- Strong priority requires reproducible evidence and independent corroboration under the project evidence model.

## Pilot 1A exit gate

Advance from source feasibility to detector-yield analysis only when:

- the collection window is frozen;
- raw snapshots are checksummed;
- identifier join rates are measured;
- parser and identity errors are audited;
- Companies House joins use stable IDs or explicit match decisions;
- no source-coverage regression is present in CI;
- the case registry records Track A eligibility fields.

## Known practical dependency

Live Companies House Public Data API requests require API authentication. The adapter and identifier join are already implemented, but a live bulk enrichment workflow must receive the credential through secure runtime configuration before it can retrieve the company/PSC records.
