# Status

## State

**UK PILOT 1A FROZEN / CHINA-FIRST MULTI-INSTITUTION WEB-MINING EXPANSION ACTIVE**

Date: 2026-09-18

## Current maturity estimate

**~60%**

## Completed foundations

- [x] ARIS4C011 evidence-first architecture inherited;
- [x] OpenIntegrity Agent Skill, E0-E5 evidence semantics and FLAG/PASS/ABSTAIN/ERROR;
- [x] conservative identity resolution and temporal-leakage controls;
- [x] single-case and cross-contract detector prototypes;
- [x] source-coverage semantics: missing source != negative evidence;
- [x] Evidence Graph + canonical report builder;
- [x] OCDS, USAspending, Companies House and dated debarment normalization surfaces;
- [x] frozen UK Pilot 1A source-feasibility artifact;
- [x] UK Pilot 1A: 200 releases -> 223 award cases -> 89 direct GB-COH company-identifier candidates;
- [x] China-first multi-institution scope is now canonical;
- [x] China institution ontology includes government, public institutions, hospitals, SOEs, research institutes, universities, NGOs/social organizations, state-owned financial institutions, procurement agencies and private suppliers;
- [x] China source tiers CN-A through CN-F defined;
- [x] China machine-readable source registry created;
- [x] China web-lead evidence contract created;
- [x] public/social-web content is hard-limited to lead generation and cannot alone produce strong review evidence;
- [x] ARIS4C011 is explicitly reusable for research-publication forensics inside the research-institute/university layer.

## China-first source backbone

Initial official/public source families include:

- 中国政府采购网;
- 全国公共资源交易平台 and provincial/local trading portals;
- 国家企业信用信息公示系统;
- 国务院国资委 and SOE official procurement/disclosure sites;
- 国家卫生健康委员会 and regional health-authority/hospital sites;
- 全国社会组织信用信息公示平台;
- 慈善中国 / 全国慈善信息公开平台;
- 审计署 and local audit offices;
- 中央纪委国家监委 and corresponding official outcome pages;
- 国家自然科学基金委员会 and other public science-program sources where public;
- institution websites, procurement PDFs, annual reports, patents/technology-transfer pages and archived pages;
- reputable journalism as discovery/corroboration;
- public WeChat/Weibo/forum/search-engine results as lead-only discovery surfaces.

Canonical files:

- `process/CHINA_EXPANSION.md`
- `data/CHINA_SOURCES.md`
- `data/china_source_registry.json`
- `code/china_scope.py`
- `code/china_web_leads.py`

## Priority institution modules

### Hospitals

Focus on:
- equipment;
- reagents/consumables;
- maintenance/IT/construction;
- repeated vendors;
- company age and corporate network;
- hospital leadership and licensing;
- official audit/discipline outcomes.

### SOEs

Focus on:
- group/subsidiary structure;
- own procurement portals;
- recurring counterparties;
- common-control supplier structures;
- executive-company cross-links;
- official audit/discipline outcomes.

### Research institutes / universities

Focus on:
- grants;
- instrument/equipment procurement;
- patents;
- technology transfer;
- spin-off companies;
- affiliated hospitals/companies;
- publications and research-integrity signals via ARIS4C011.

### NGOs / charities / social organizations

Focus on:
- registration;
- annual/financial reports;
- fundraising/projects;
- related-party disclosures;
- major transactions where public;
- regulator/audit findings.

Organization mission, advocacy position, religious identity, donor nationality or foreign links are not suspicion features.

## Internet-mining principle

OpenIntegrity China should support two search modes:

1. **entity-centric crawl** — start from an institution/company/person/project and expand aliases, sites, contracts, grants, patents, affiliations and official findings;
2. **event-centric crawl** — start from a procurement event, audit finding, investigation or public report and reconstruct the entity graph backward/forward in time.

All discovered pages should preserve URL, publication time when known, retrieval time, checksum, source tier, stable identifiers and attribution.

## UK Pilot 1A retained as portability baseline

Canonical result: `process/PILOT1_RESULTS.md`

Frozen collection:
- Find a Tender: 119 award cases, 32 direct GB-COH cases;
- Contracts Finder: 104 award cases, 57 direct GB-COH cases;
- raw total: 223 award cases, 89 direct company-ID candidates;
- bidder-count/competition coverage: 0 -> ABSTAIN, not imputed.

UK remains a portability/benchmark track, but China-first internet mining is now the primary expansion direction.

## Immediate next work

1. implement China Government Procurement Network / CCGP discovery-normalization using documented public standards/interfaces where feasible;
2. implement a federated National Public Resource Trading Platform + provincial-source discovery layer;
3. build organization-universe adapters for hospitals, central/local SOEs, research institutes/universities and social organizations;
4. add stable China organization identity around unified social credit code and authoritative registration/licensing IDs;
5. build institution-domain crawler contracts for hospital/SOE/institute/university/NGO procurement pages and PDFs;
6. add audit/discipline/outcome adapters that preserve investigation vs sanction vs penalty vs judgment vs audit-finding classes;
7. add charity/social-organization annual-report and related-party graph extraction;
8. add research grant/patent/technology-transfer edges and delegate publication forensics to 011;
9. create the first frozen China Pilot dataset across at least hospitals + SOEs + research institutes + social organizations rather than only government agencies;
10. run an independent identity/privacy/defamation/temporal-leakage audit before publishing named review packets.

## Hard blockers

No architecture blocker.

China sources vary widely in access method. Interactive systems, CAPTCHAs, authenticated areas and explicit anti-automation controls must not be bypassed. Where machine access is unavailable, OpenIntegrity should use lawful manual/public retrieval, documented interfaces, institution webpages or alternate official sources and record the resulting coverage gap as ABSTAIN.

The ongoing UK Companies House enrichment is no longer the sole critical path; it continues as a portability track while China-first development proceeds.
