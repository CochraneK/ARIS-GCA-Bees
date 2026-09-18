# China-first multi-institution expansion

Date: 2026-09-18  
Status: canonical scope expansion for ARIS4C014 / OpenIntegrity

## Core change

OpenIntegrity is **not** a government-only procurement monitor.

The China-facing system treats public-interest institutions as a heterogeneous network of organizations, people, vendors, grants, contracts, projects, subsidiaries, publications, patents, donations, audits and official findings.

Priority institution types:

- government departments and public agencies;
- public institutions / 事业单位;
- public hospitals and medical institutions;
- central and local state-owned enterprises and their subsidiaries;
- research institutes;
- universities and affiliated entities;
- foundations, charities, associations and other registered social organizations / NGOs;
- state-owned financial institutions where public records permit;
- procurement agencies and intermediary service providers;
- private suppliers, contractors, consultancies and related legal entities.

Selection priority is based on **public-data availability, joinability and public-interest relevance**, not on a presumption that any institution type is more corrupt.

## China-first design principle

The China module is intentionally **web-native**.

It must combine structured official datasets with public internet evidence:

1. national and local procurement / public-resource trading portals;
2. institution and regulator websites;
3. corporate and social-organization registries;
4. audit, disciplinary, enforcement and court/public-credit records;
5. grant and research-program information;
6. annual reports, financial disclosures and donation/charity disclosures;
7. procurement notices and PDFs hosted on hospitals, universities, institutes, SOEs and NGOs;
8. reputable reporting that cites source documents;
9. licensed commercial databases as optional enrichment;
10. public social/web content only as low-evidence discovery leads.

No single Chinese website is treated as complete.

## Institution ontology

### GOVERNMENT

Examples:
- ministries / commissions;
- local governments;
- bureaus and administrative agencies;
- public-resource trading centers.

Typical data:
- procurement;
- tenders;
- contracts;
- budgets;
- audit results;
- administrative penalties;
- public officials / leadership rosters.

### PUBLIC_INSTITUTION

Examples:
- 事业单位;
- public service centers;
- public cultural/scientific institutions.

Typical data:
- procurement;
- leadership;
- annual budget/final accounts;
- external contracts;
- audit findings.

### HOSPITAL

Examples:
- public hospitals;
- university-affiliated hospitals;
- specialist medical institutions.

Typical data:
- equipment procurement;
- reagent and consumable procurement;
- maintenance / IT / construction contracts;
- drug-device related procurement where public;
- hospital leadership;
- health-authority licensing;
- audit/discipline findings;
- supplier recurrence and related-party structure.

Important: a vendor relationship with a hospital is not itself suspicious.

### SOE

Examples:
- central SOEs;
- local SOEs;
- listed and unlisted subsidiaries;
- state-owned financial institutions where appropriate.

Typical data:
- group/subsidiary structure;
- procurement and tender portals;
- supplier concentration;
- executives / board positions;
- related-party transactions when disclosed;
- audit and disciplinary findings;
- equity / corporate registry data.

### RESEARCH_INSTITUTE

Examples:
- CAS and other academy institutes;
- ministerial institutes;
- independent public research institutes.

Typical data:
- scientific grants;
- instrument/equipment procurement;
- construction and service contracts;
- institutional leadership;
- patents and technology transfer;
- spin-off companies;
- publications;
- research-integrity events.

ARIS4C011 can be called as a specialized research-forensics sub-agent for the publication/research-output layer.

### UNIVERSITY

Typical data:
- government procurement;
- university procurement portals;
- research grants;
- affiliated hospitals and companies;
- patents / technology transfer;
- construction;
- research publications;
- leadership / departmental structure.

### NGO_OR_SOCIAL_ORGANIZATION

Includes:
- foundations;
- charities;
- associations;
- chambers;
- registered social-service organizations.

Typical data:
- registration;
- legal representative / responsible persons where public;
- annual reports;
- donations and charitable projects;
- related organizations;
- public fundraising records;
- procurement / service contracts where public;
- regulator or audit findings.

NGO status, foreign links, religious identity or advocacy position are **not** risk features.

## Stable identity policy for China

Preferred organization identifiers:

1. unified social credit code / 统一社会信用代码;
2. authoritative registration / licensing number;
3. official organization identifier published by the relevant regulator;
4. exact organization name + jurisdiction + registered address or other independent attributes;
5. organization name alone -> possible match / ABSTAIN depending on use.

For people:

- never use or infer national ID numbers;
- prefer official role + organization + time interval;
- cross-source same-name person linkage requires multiple corroborating attributes;
- name-only person linkage cannot become high-priority evidence.

## China web evidence tiers

### CN-A — official structured

Examples:
- government procurement interfaces;
- public-resource trading records;
- enterprise/social-organization registries;
- regulator query systems.

Default maximum evidence class:
E2/E3 when identity and time are verified.

### CN-B — official institution websites

Examples:
- hospital procurement notice;
- university tender PDF;
- SOE award notice;
- institute leadership page;
- NGO annual report.

Default maximum evidence class:
E0/E2 depending on whether the page establishes a factual relationship.

### CN-C — official audit / enforcement / disciplinary record

Examples:
- National Audit Office or local audit office;
- regulator penalty;
- disciplinary/inspection public notice;
- court/public execution record where lawfully available.

This is outcome/provenance evidence, not permission to infer unrelated misconduct.

### CN-D — reputable journalism with source documents

Useful for discovery and corroboration.

Allegation and official adjudication must remain separate outcome classes.

### CN-E — licensed commercial databases

Examples may include corporate/intelligence databases with permitted API or licensed access.

They are optional enrichments, never the only source for a consequential assertion.

### CN-F — public internet / social content

Examples:
- public WeChat articles;
- Weibo posts;
- forums;
- cached webpages;
- public complaint pages.

Use for **lead generation only** unless independently corroborated.

Default evidence class:
E5, occasionally E4 for calibrated aggregate signals.

## Cross-sector graph

Important node types:

- organization;
- hospital;
- SOE group/subsidiary;
- research institute;
- university;
- NGO/foundation;
- person;
- supplier;
- procurement agency;
- contract/tender/award;
- grant;
- research project;
- publication;
- patent;
- technology-transfer transaction;
- donation;
- charitable project;
- audit/enforcement/disciplinary record;
- address;
- website/document/source record;
- detector finding.

Important edges:

- AWARDED_TO;
- BID_FOR;
- SUPPLIED_TO;
- SUBSIDIARY_OF;
- CONTROLS;
- OWNS;
- EXECUTIVE_OF;
- LEGAL_REPRESENTATIVE_OF;
- EMPLOYED_BY;
- OCCUPIED_PUBLIC_OFFICE;
- FUNDED_BY;
- GRANT_AWARDED_TO;
- AFFILIATED_WITH;
- DONATED_TO;
- IMPLEMENTED_CHARITY_PROJECT;
- PATENT_ASSIGNED_TO;
- TECHNOLOGY_TRANSFERRED_TO;
- AUTHORED;
- RETRACTED_OR_CORRECTED;
- AUDITED_BY;
- PENALIZED_BY;
- SUBJECT_OF_OFFICIAL_FINDING;
- SHARES_ADDRESS_WITH;
- SAME_ENTITY_AS;
- POSSIBLE_MATCH;
- DERIVED_FROM;
- CORROBORATES;
- CONTRADICTS.

No graph edge named CORRUPT, BRIBED, COLLUDER or equivalent may be generated automatically.

## China-specific detector families

### C1 Procurement and award structure

- repeated awards;
- narrow / single-source procedure when explicitly documented;
- short tender periods;
- cancellation/restart patterns;
- repeated procurement agents;
- unusual supplier turnover;
- threshold proximity only under explicit applicable rules.

### C2 Supplier and corporate graph

- supplier concentration;
- newly incorporated supplier;
- shared legal representatives / officers / addresses;
- common parent or beneficial-control links;
- vendor-company and institution-affiliate relationships.

Shared address alone remains contextual because incubators, agents and group companies can legitimately share addresses.

### C3 Hospital / medical procurement

- high-frequency equipment/reagent/service vendors;
- repeated vendor wins by department or hospital;
- newly incorporated medical suppliers;
- equipment-price outliers only with comparable model/specification controls;
- vendor corporate-network links;
- official discipline/audit outcomes as outcome labels only.

### C4 SOE network

- parent/subsidiary procurement loops;
- recurring counterparties;
- supplier / subsidiary common control;
- executive-company cross-links;
- repeated sole-source/limited procedure only where rules and fields are explicit.

### C5 Research and university integrity

- grant -> institution -> procurement -> supplier;
- principal-investigator / spin-off-company links where officially documented;
- patent/technology-transfer relationships;
- instrument procurement anomalies;
- paper/publication forensic signals delegated to ARIS4C011.

A scientist founding or owning a company is not wrongdoing by itself.

### C6 NGO / charity integrity

- registration and responsible-person consistency;
- annual-report continuity;
- disclosed donation/project flows;
- related-party organization graph;
- public fundraising/project consistency;
- regulator/audit findings.

Donor identity, advocacy topic or political/religious orientation are not suspicion features.

### C7 Outcome/provenance

- official audit finding;
- administrative penalty;
- procurement serious-illegality record;
- disciplinary investigation / sanction;
- court/execution record where applicable;
- correction/retraction;
- documented rule breach.

Investigations and allegations are not equivalent to adjudicated findings.

### C8 Web inconsistency / disappearance

- changed leadership pages;
- procurement PDF disappearance;
- conflicting dates/amounts across official pages;
- official page vs registry mismatch;
- archived vs current corporate relationship.

Website deletion or change is not misconduct by itself.

## Internet-mining architecture

```
seed entities / keywords / stable IDs
  -> search/discovery layer
  -> domain allowlist + source classifier
  -> structured API adapters
  -> HTML/PDF/document parsers
  -> named-entity + identifier extraction
  -> temporal snapshot / checksum
  -> identity resolution
  -> China Evidence Graph
  -> detector router
  -> dependency-aware fusion
  -> human verification packet
```

The system should be able to start from any of:

- institution;
- supplier;
- person;
- company ID;
- project;
- contract;
- grant;
- research paper;
- patent;
- NGO/foundation;
- keyword/industry.

## Search strategy

Use two complementary passes.

### Entity-centric crawl

Starting from a known institution/person/company:
- aliases;
- official pages;
- subsidiaries/affiliates;
- contracts;
- procurement notices;
- grants;
- patents;
- leadership;
- audit/enforcement records;
- archived versions.

### Event-centric crawl

Starting from a contract, finding, investigation, audit issue or public report:
- all named entities;
- earlier procurement history;
- corporate history;
- ownership/leadership at the relevant date;
- connected institutions;
- later outcome documents.

Track A must only use information public before its cutoff even if the event-centric crawl discovers later outcomes.

## Safety and evidentiary wording

The China module must distinguish:

- model-generated anomaly;
- public-record relationship;
- complaint;
- journalistic allegation;
- official investigation;
- disciplinary sanction;
- administrative penalty;
- court judgment;
- audit finding.

A public investigation notice is not a conviction.

A procurement relationship is not a conflict of interest unless an applicable rule and relevant relationship are independently established.

No automated output may label a named person or institution corrupt.
