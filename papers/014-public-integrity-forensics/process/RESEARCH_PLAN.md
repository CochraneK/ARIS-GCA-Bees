# Research plan

## 1. Research objective

Develop and evaluate OpenIntegrity, an auditable multi-source agent for discovering public-integrity leads from lawful public records.

The system is designed for investigative triage, audit support, journalism, civil-society research, compliance research, and computational social science. It is not designed to automate accusations or legal determinations.

## 2. Research questions

### RQ1 — Coverage
Does a multi-source system discover more distinct, verifiable issue types than procurement-only red-flag screening?

### RQ2 — Evidence fusion
Does dependency-aware Evidence Graph fusion improve verified lead yield at a fixed review burden compared with:
- count of flags;
- maximum detector score;
- procurement-red-flag-only screening;
- graph-anomaly-only screening;
- LLM-only synthesis?

### RQ3 — Temporal validity
How much apparent performance disappears when later enforcement, sanctions, investigations, and retrospective registry changes are excluded from the feature set?

### RQ4 — Human burden
Which detector families deliver the most verified leads per reviewer minute?

### RQ5 — Entity resolution
How much of the error budget comes from mistaken person/company matching rather than the detector itself?

### RQ6 — Portability
Which signals transfer across procurement jurisdictions after adjusting for legal thresholds, publication practices, sector, award size, and data completeness?

## 3. System pipeline

```
public sources
   ↓
source adapters + snapshots + licence metadata
   ↓
canonical records
   ↓
entity resolution + temporal identity graph
   ↓
applicability router
   ↓
detector families
   ↓
detector critic / dependency grouping
   ↓
Evidence Graph
   ↓
transparent review-priority policy
   ↓
human verification packet
```

LLMs may assist extraction and synthesis, but deterministic source parsing and source-span provenance are preferred whenever available.

## 4. Canonical entities

Minimum graph nodes:

- contract / tender / lot / award;
- contracting authority;
- supplier / bidder;
- legal entity;
- natural person;
- beneficial owner;
- officer/director;
- public office / occupancy;
- sanction/debarment action;
- donation/lobbying/interests disclosure when available;
- address;
- document;
- source record;
- detector finding.

Minimum temporal edges:

- BID_FOR;
- AWARDED_TO;
- OWNS / CONTROLS;
- OFFICER_OF;
- OCCUPIED_PUBLIC_OFFICE;
- SHARES_ADDRESS_WITH;
- SANCTIONED_OR_DEBARRED;
- DONATED_TO;
- LOBBIED;
- RELATED_TO;
- SAME_ENTITY_AS;
- POSSIBLE_MATCH;
- DERIVED_FROM;
- CORROBORATES / CONTRADICTS.

Every relationship should carry valid-from / valid-to when the source supports it.

## 5. Data tiers

### Tier 1 — standardized procurement
Use OCDS publishers where possible. Add official national adapters such as USAspending and TED.

### Tier 2 — ownership and corporate control
Corporate registries, PSC/beneficial ownership, BODS-compatible sources.

### Tier 3 — public office and restrictions
PEP/office-holder data, sanctions, World Bank debarment, official disciplinary/enforcement records.

### Tier 4 — relationship enrichment
ICIJ Offshore Leaks and other lawfully reusable public-interest datasets, always retaining source caveats.

### Tier 5 — jurisdiction-specific integrity records
Donations, lobbying, declarations of interests/assets, land/property, court records, audit reports, grants.

## 6. Benchmark construction

### 6.1 Unit of analysis
Primary units:
- procurement procedure / award;
- supplier-authority pair;
- entity-time window;
- documented issue.

Paper-level analogues from 011 are therefore replaced by contract/entity-level evaluation.

### 6.2 Outcome hierarchy

Do not collapse all outcomes into "corrupt/not corrupt".

Outcome labels should distinguish:
- official criminal conviction;
- civil/administrative enforcement finding;
- debarment/sanction;
- official audit finding;
- documented procurement-rule breach;
- disclosed conflict of interest;
- journalistic/investigative allegation without adjudication;
- model-only anomaly;
- no known adverse finding.

### 6.3 Track A — temporally blind
For each historical case, construct a source snapshot at time T before the public outcome. Anything first available after T is label-side only.

Primary endpoint:
verified issue-type recall at a fixed number of alerts per 100 contracts.

Secondary endpoints:
precision among reviewed alerts, lead time, reviewer minutes, entity-match error.

### 6.4 Track B — open world
Use all currently public lawful records to rank cases for human review. Evaluate verified lead yield prospectively or through adjudicated review.

### 6.5 Comparators
Match no-known-finding comparators on jurisdiction, agency, sector, year, procurement method, and value band where feasible. Never describe them as confirmed clean.

## 7. Leakage controls

Major leakage risks:

- debarment list used as both feature and outcome;
- current beneficial ownership substituted for historical ownership;
- media reports revealing an investigation included in pre-investigation features;
- later company dissolution/renaming leaking outcome;
- post-award audit findings embedded in procurement portals;
- graph neighbors carrying direct outcome labels into test records.

All records need `observed_at`, `valid_from`, `valid_to`, and `retrieved_at` where feasible.

## 8. Entity-resolution protocol

Entity matching is a first-class model, not hidden preprocessing.

Evidence hierarchy:
1. exact stable identifier;
2. official cross-registry identifier;
3. name + address + date/registration number;
4. name + multiple independent attributes;
5. name-only fuzzy similarity.

Level 5 cannot create a high-priority integrity lead.

Report:
- candidate matches;
- match method;
- confidence/calibration;
- conflicting attributes;
- whether a human identity check is required.

## 9. Fairness and confounding audit

Forbidden shortcut:
"contracts from location X are suspicious because X has a high corruption index."

Country/jurisdiction can instead define:
- legal procurement rules;
- monetary thresholds;
- publication obligations;
- market size;
- source availability;
- baseline tender structure.

Audit performance across:
- jurisdictions;
- data-completeness strata;
- sectors;
- contract-value bands;
- procurement methods;
- language/source formats.

## 10. Pilot sequence

### Pilot 0 — synthetic deterministic test
Create synthetic tenders/entities that deliberately contain:
- single bidder;
- split awards around a threshold;
- company incorporated immediately before award;
- repeated winner concentration;
- shared address among supposed competitors;
- exact stable-ID PEP/ownership link;
- debarment after vs before award;
- missing beneficial-owner data;
- benign offshore relation;
- name-only collision.

Goal: verify routing, ABSTAIN semantics, dependency grouping, time handling, and no automated corruption inference.

### Pilot 1 — one jurisdiction
Prefer a jurisdiction with strong procurement + corporate/ownership identifiers. Initial candidates include UK/EU or US, selected by joinability rather than presumed corruption prevalence.

### Pilot 2 — cross-jurisdiction portability
Add a second source ecosystem and test which detector families transfer after rule configuration.

## 11. Success criteria for v1

- source snapshots are reproducible;
- every detector has an applicability test;
- every finding preserves source record IDs;
- Track A has no known temporal leakage;
- identity matches expose provenance;
- E5-only evidence cannot rank as high priority;
- human reviewers can reproduce a lead from the generated packet;
- code can run on synthetic Pilot 0 without network access.
