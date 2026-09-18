# Detector taxonomy

## F1 — Procurement process and competition

Candidate checks:
- single bidder / low bidder count;
- non-open or exceptional procedure;
- unusually short advertising/tender period;
- missing publication stages;
- repeated direct awards;
- qualification/specification patterns that narrow competition;
- cancelled-and-reissued tenders with altered criteria.

Base evidence is generally E0; calibrated statistical departures are E4.

## F2 — Value, pricing, arithmetic, and thresholds

Candidate checks:
- award values just below legal/administrative thresholds;
- repeated/split awards clustered around thresholds;
- unit-price outliers relative to comparable procurement;
- duplicate invoices/amounts when public data permit;
- implausible arithmetic across lots/amendments;
- large post-award value increases;
- round-number and digit-law heuristics only under justified assumptions.

Near-threshold alone is not wrongdoing.

## F3 — Supplier concentration and repeat-award structure

Candidate checks:
- authority-level supplier concentration;
- repeated awards to one supplier beyond sector/value baselines;
- winner rotation;
- low entry/exit diversity;
- reciprocal buyer-supplier dependence;
- unusually persistent bidder groups.

Control for market structure and specialized suppliers.

## F4 — Temporal forensics

Candidate checks:
- supplier incorporated shortly before award;
- ownership/director change near tender/award;
- repeated awards immediately after relevant role/disclosure changes;
- contract amendments soon after award;
- sanction/debarment in force on award date;
- disclosure or registration occurring after the claimed relevant date.

Temporal facts require historical, not merely current, registry states.

## F5 — Corporate and beneficial-ownership forensics

Candidate checks:
- PSC/beneficial-owner chains;
- opaque or incomplete control chains;
- shared officers/owners among competitors;
- common addresses/contact details;
- rapid creation/dissolution of supplier entities;
- cross-registry identifier contradictions;
- control through multiple layers.

Opacity is contextual evidence, not guilt.

## F6 — Public office, interests, and conflict-of-interest links

Candidate checks:
- official/decision-maker ↔ supplier ownership links;
- declared-interest ↔ contract relationships;
- public office occupancy overlapping relevant decision period;
- relatives/close associates only when lawfully sourced and identity-resolved;
- revolving-door timing when employment data are public.

PEP/public-office status by itself is never a flag for wrongdoing.

## F7 — Sanctions, debarment, audit, and enforcement

Candidate checks:
- World Bank or other official debarment in force at the relevant time;
- applicable sanctions list matches;
- official audit findings;
- administrative/civil/criminal findings;
- procurement exclusion lists.

Track A must not use outcome-side future findings as features.

## F8 — Cross-source identity and provenance contradictions

Candidate checks:
- inconsistent company identifiers;
- conflicting dates/addresses/directors across official sources;
- unresolved same-name collisions;
- historical vs current ownership mismatch;
- missing provenance for claimed relationships.

This family often produces ABSTAIN rather than FLAG.

## F9 — Document and bidding-coordination forensics

Where public documents lawfully exist:
- near-identical bid text;
- shared unusual errors;
- identical metadata/contact information;
- synchronized formatting/template artifacts;
- tender specifications copied from a supplier's materials;
- unusual document reuse across nominal competitors.

Separate legitimate templates from high-specificity coordinated patterns.

## F10 — Graph/network forensics

Graph entities:
- authorities;
- tenders/awards;
- suppliers;
- officers/owners;
- public officials;
- addresses;
- sanctions;
- disclosures;
- offshore entities.

Candidate signals:
- dense bidder clusters;
- shared-control communities;
- circular ownership;
- unusually central intermediaries;
- repeated authority-supplier subgraphs;
- winner rotation among connected companies;
- shortest paths linking decisions to interests.

Network signals require sector and market-structure controls.

## F11 — Distributional and weak heuristic layer

Candidate checks:
- Benford/Newcomb;
- terminal digit/heaping;
- excessive round numbers;
- generic anomaly ensembles;
- name-only fuzzy match;
- generic LLM suspicion score.

Default E5 unless a detector's assumptions and calibration justify E4. This family cannot independently create HIGH priority.

## Required applicability questions

Before running a detector, answer:

1. Are the required fields present?
2. Is the source authoritative enough for this use?
3. Is the source temporally valid?
4. Are jurisdiction-specific rules configured?
5. Is entity resolution above the detector's minimum threshold?
6. Is the comparison/reference population appropriate?
7. Would missingness itself create a biased flag?

If not, ABSTAIN.
