---
name: public-integrity-forensics
description: Audits public procurement and related open records for reproducible public-integrity risk signals using applicability-aware procurement, corporate ownership, beneficial ownership, public-office, sanctions/debarment, identity, document, and network checks. Use for open-data investigative triage, audit support, compliance research, journalism, or computational social science. Produces sourced review leads and abstentions, never an automated accusation that a person or organization is corrupt.
compatibility: Python 3.12 reference core in ARIS4C014. Network access is optional for fixtures and required for live public-data adapters.
metadata:
  author: CochraneK
  project: ARIS4C014
  inherits_from: ARIS4C011
  version: "0.1.0"
---

# Public Integrity Forensics / OpenIntegrity

## Purpose

Use this skill to assemble and audit lawful public records for public-integrity review.

The skill is a **forensic triage system**, not a guilt classifier. A procurement red flag, a politically exposed/public-office connection, an offshore relationship, a sanctions match, unusual supplier concentration, or a graph anomaly can each have lawful explanations. The output must preserve that distinction.

## China-first multi-institution mode

For China-facing work, OpenIntegrity is not government-only. Treat the following as first-class institution types:

- government and public agencies;
- public institutions / 事业单位;
- public hospitals and medical institutions;
- central/local SOEs and subsidiaries;
- research institutes;
- universities and affiliated entities;
- foundations, charities, associations and other social organizations / NGOs;
- state-owned financial institutions where public records permit;
- procurement agencies and private suppliers.

China discovery is web-native: combine official structured platforms with institution websites, PDFs, audit/enforcement pages, research-funding records, annual reports, reputable journalism and public-web lead discovery.

Use `process/CHINA_EXPANSION.md`, `data/CHINA_SOURCES.md`, and `data/china_source_registry.json`.

China source tiers:

- CN-A official structured;
- CN-B official institution web/document;
- CN-C official audit/enforcement/disciplinary outcome;
- CN-D reputable journalism;
- CN-E licensed commercial enrichment;
- CN-F public web/social lead.

CN-F is lead-generation only and defaults to E5. Social/web content cannot by itself create a strong or consequential integrity conclusion.

Research-publication forensics can delegate to ARIS4C011.


### China procurement result semantics

For CCGP-style procurement records:

- a final supplier result may become an `AWARDED_TO` relationship after normal source/identity checks;
- a ranked `中标候选人` is a candidate record, not a final award, and must use a distinct candidate relationship;
- percentage/discount pricing is not currency and must never be coerced into a contract value;
- parser misses and inaccessible official sources are coverage gaps, not negative evidence;
- personal contacts, telephone numbers and street addresses should be excluded from public feasibility artifacts unless a later detector explicitly requires and justifies them.

## Core invariants

1. Never output a binary corrupt/not-corrupt verdict.
2. Never infer intent, criminal liability, or political worthiness from a detector output.
3. Every detector must establish applicability before interpreting a result.
4. Missing source coverage becomes ABSTAIN, never PASS.
5. PASS means the relevant source family was actually covered and the applicable check did not flag.
6. Prefer stable identifiers and official cross-registry identifiers over name matching.
7. Name-only person matches cannot create a high-priority relationship.
8. Current ownership cannot silently substitute for historical ownership.
9. Future sanctions, audits, investigations, convictions, or media outcomes cannot leak into Track A features.
10. Country, nationality, ethnicity, religion, and ordinary political affiliation are not intrinsic suspicion features.
11. PEP/public-office status is context, not wrongdoing.
12. Offshore ownership is context, not wrongdoing.
13. Benford, round-number, stylometric, generic LLM suspicion, and fuzzy-name signals default to weak evidence.
14. Correlated detectors must share a dependency group rather than being counted as independent evidence.
15. Every surfaced lead must preserve source record identifiers, dates, and benign explanations.
16. Human review is required before any consequential allegation or action.

## Modes

### Track A — temporally blind screening

Use when testing whether a concern could have been surfaced before a later public outcome.

Define a cutoff T. Feature-side information must have been publicly available on or before T. Later audit findings, sanctions, convictions, investigative reporting, registry changes, or outcome labels are outcome-side only.

If public availability dates cannot be established, mark the relevant source family ABSTAIN or the case BLOCKED.

### Track B — open-world integrity triage

Use current lawful public sources to build a present-day evidence graph for human review.

Post-outcome sources may be used, but official findings, allegations, and model-generated anomalies must remain separate evidence types.

### Ad hoc review

Use for exploratory review of a contract, authority, supplier, company, or public record set. Preserve the same source-coverage and identity rules, but do not imply benchmark validity.

## Workflow

### 1. Define the subject and time scope

Record:
- contract/award/tender/entity identifiers;
- jurisdiction and procurement regime;
- requested mode;
- Track A cutoff if applicable;
- retrieval date;
- source publication and validity dates when available.

Do not silently mix current and historical records.

### 2. Build source coverage

Coverage families include:
- procurement_award;
- procurement_competition;
- ownership;
- public_office;
- debarment;
- sanctions;
- declarations/interests;
- donations/lobbying where lawful;
- property/land where lawful;
- audit/enforcement;
- documents;
- network enrichment.

A family not loaded is unavailable evidence, not a negative finding.

### 3. Normalize public sources

Prefer:
1. official structured records;
2. official unstructured records;
3. reputable public-interest datasets with provenance;
4. investigative reporting tied to cited records;
5. unsourced web claims — excluded from the evidence graph.

Current reference adapters include:
- OCDS 1.1.x releases and lifecycle record packages;
- UK Find a Tender and Contracts Finder OCDS surfaces;
- USAspending spending_by_award results;
- UK Companies House company profile and PSC fragments;
- normalized dated debarment rows after source-specific retrieval.

### 4. Resolve entities conservatively

Identity hierarchy:
1. shared stable identifier;
2. official cross-registry identifier;
3. name plus multiple corroborating attributes;
4. name plus one corroborating attribute — possible match;
5. name only — ABSTAIN.

Expose:
- match method;
- score/calibration if any;
- conflicting attributes;
- whether human identity verification is required.

Never merge persons merely because names match.

### 5. Run applicable detector families

F1 procurement_process  
F2 value_threshold  
F3 supplier_concentration  
F4 temporal_forensics  
F5 corporate_ownership  
F6 conflict_of_interest  
F7 sanctions_debarment  
F8 identity_provenance  
F9 document_coordination  
F10 graph_network  
F11 weak_heuristics

Read the project detector taxonomy before adding new rules.

### 6. Deterministic checks first

Examples:
- reported single-bidder count;
- configured near-threshold values;
- deterministic split-award patterns under explicit comparable-procurement and legal-rule assumptions;
- impossible timeline or arithmetic;
- exact stable-ID ownership links;
- debarment in force on the relevant date.

A deterministic pattern establishes the computational fact only. It does not establish corrupt intent.

### 7. Higher-inference checks second

Examples:
- peer-conditioned supplier concentration;
- price/value anomaly models;
- graph-community or winner-rotation anomalies;
- bid-document similarity;
- model-derived coordinated-bidding signals.

Record the reference population and calibration basis. Sector, procurement method, market structure, contract value, and data completeness can be important confounders.

### 8. Critic pass

For every FLAG:
- verify the source record;
- verify temporal validity;
- verify entity resolution;
- test the detector assumptions;
- list benign explanations;
- identify the dependency group;
- withdraw or downgrade findings that cannot be reproduced.

### 9. Build the Evidence Graph

Typical nodes:
- contract/tender/award;
- authority;
- supplier/bidder;
- legal entity;
- natural person;
- beneficial owner/officer;
- public office/occupancy;
- address;
- sanction/debarment;
- disclosure;
- document;
- source record;
- detector finding.

Typical edges:
- AWARDED_TO;
- BID_FOR;
- OWNS;
- CONTROLS;
- OFFICER_OF;
- OCCUPIED_PUBLIC_OFFICE;
- SHARES_ADDRESS_WITH;
- SANCTIONED_OR_DEBARRED;
- DECLARED_INTEREST_IN;
- SAME_ENTITY_AS;
- POSSIBLE_MATCH;
- DERIVED_FROM;
- CORROBORATES;
- CONTRADICTS;
- DEPENDS_ON.

### 10. Assign review priority

Default pilot semantics:
- HIGH: strong reproducible evidence plus at least one independent corroborating family;
- MODERATE: one E2/E3 finding or multiple independent lower-level reproducible families;
- LOW: isolated contextual or calibrated model anomaly;
- VERY_LOW: E5-only evidence;
- NO_FLAG: covered applicable checks produced no flags;
- ABSTAIN_OR_INCOMPLETE: missing data/source coverage prevents a meaningful negative result;
- BLOCKED: required temporal/provenance safety failed.

Review priority means **what a human should inspect first**, not probability of corruption.

## Evidence classes

E0 — direct metadata/process observation  
E1 — deterministic incompatibility or configured rule-conditioned anomaly  
E2 — externally verifiable official/public-record fact  
E3 — high-specificity cross-source forensic match  
E4 — calibrated model/peer-distribution anomaly  
E5 — weak/context-dependent heuristic

Evidence class is not a guilt scale.

## Human-facing output

A lead packet should answer:
- What exactly triggered?
- Which public record(s) support it?
- Were those records public at the relevant time?
- How were people/companies resolved?
- Was the detector applicable?
- Can the calculation be reproduced?
- Which findings are genuinely independent?
- What lawful explanations remain?
- What should the reviewer verify next?
- What source families were not checked?

Use assets/finding.schema.json and assets/report.schema.json for machine-readable output.

## Bundled project resources

- process/DETECTOR_TAXONOMY.md — detector families and applicability rules.
- process/EVIDENCE_MODEL.md — evidence classes, temporal semantics, and review-priority rules.
- data/SOURCES.md — initial source catalogue and access/licence caveats.
- code/open_integrity_agent.py — reference single-case core.
- code/source_adapters.py — deterministic source normalization.
- code/entity_resolution.py — conservative identity baseline.
- code/batch_detectors.py — cross-contract Pilot 0 rules.
- code/case_enrichment.py — explicit cross-source joins.
- code/debarment_enrichment.py — dated external debarment attachment with conservative identity proof.
- code/source_snapshot.py — SHA-256 source snapshots and Track A publication-time gate.
- code/evidence_graph.py — descriptive Evidence Graph construction.
- code/report_builder.py — standard portable report construction.
- process/PILOT1_PROTOCOL.md — locked UK identifier-first Pilot 1 protocol.
- process/PILOT1_RESULTS.md — frozen UK Pilot 1A source-feasibility result.
- process/CHINA_EXPANSION.md — China-first multi-institution scope and graph design.
- data/CHINA_SOURCES.md — China public/open-web source map.
- data/china_source_registry.json — machine-readable China source registry.
- code/china_scope.py — China institution/source-tier policy.
- code/china_web_leads.py — web-lead evidence contract and Track A gate.
- code/china_ccgp.py — bounded CCGP award-list discovery and buyer routing.
- code/china_ccgp_detail.py — privacy-minimized CCGP award-detail normalization with final-award/candidate separation and supplier USCC extraction where exposed.
- code/china_procurement_graph.py — China procurement graph projection; exact USCC may form stable supplier identity, while name-only records remain source-local.
- code/china_universe.py — official China institution-universe seed adapters with source-unavailable semantics.
- process/CHINA_PILOT0_RESULTS.md — frozen live China source-feasibility results.
