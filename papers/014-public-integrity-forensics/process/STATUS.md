# Status

## State

**CHINA PILOT 1 · EXACT-USCC ENRICHMENT CONTRACT VALIDATED / REAL SECOND-SOURCE JOIN NEXT**

Date: 2026-09-18

## Current maturity estimate

**~71%**

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
- [x] ARIS4C011 is explicitly reusable for research-publication forensics inside the research-institute/university layer;
- [x] completed bounded live CCGP award-list discovery: 36 unique notices with 100% buyer/publication-time metadata coverage in the sample;
- [x] implemented central/local CCGP award-detail parsing with source hashing and privacy-minimized output;
- [x] separated final awards from ranked bid candidates so candidate records cannot silently become AWARDED_TO relations;
- [x] normalized CCGP currency fields including unit-in-label local templates and preserved percentage pricing as non-currency;
- [x] completed extended bounded live CCGP detail smoke: 12 notices -> 14 supplier-result records -> 11 final awards + 3 candidate records, with 2 parser-miss notices retained as coverage gaps;
- [x] implemented official institution-universe seed adapters;
- [x] normalized 106 CAS official research-unit seeds in the live universe pilot;
- [x] isolated SASAC machine-access TLS failure as source_unavailable rather than inferring an empty SOE universe;
- [x] froze China Pilot 0 results in process/CHINA_PILOT0_RESULTS.md;
- [x] extracted supplier unified social credit codes from structured CCGP award tables without retaining addresses/phones;
- [x] completed a fixed official-page USCC regression: 4/4 final-award lots carried parsed stable supplier IDs;
- [x] implemented a China procurement graph where final awards use AWARDED_TO, ranked candidates use HAS_RANKED_CANDIDATE, and name-only suppliers remain source-local;
- [x] exact USCC suppliers can share a stable CN-USCC graph identity across notices; same-name-only suppliers cannot auto-merge.
- [x] implemented and CI-validated `china_stable_id_enrichment.py`: only exact CN-USCC equality can auto-attach allowlisted factual registry attributes; name-only equality is review-only; same-name disjoint stable IDs are conflicts; interactive/unavailable sources remain `COVERAGE_GAP`; contact-person/telephone fields are not propagated; every output keeps `corruption_inference=false`.

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

## China Pilot 0 frozen result

Canonical result: `process/CHINA_PILOT0_RESULTS.md`

### CCGP list discovery

Workflow **35314543749**:
- 36 unique award-notice leads;
- buyer metadata coverage 100%;
- publication-time coverage 100%;
- institution routing is source feasibility only, not a risk distribution.

### Official institution universe

Workflow **35314852919**:
- 106 successfully normalized CAS research-unit seeds;
- SASAC source unavailable in GitHub Actions because the source TLS chain could not be verified;
- TLS verification was not disabled;
- unavailable source != zero organizations.

### CCGP detail normalization

Latest extended workflow **35315845079**:
- 12 bounded live notices;
- 14 normalized supplier-result records;
- 11 final-award records;
- 3 ranked candidate records;
- 2 notices retained as parser-miss coverage gaps;
- supplier/value coverage among parsed records: 100%;
- the moving sample happened to contain 0 USCC-bearing parsed lots.

Dedicated stable-ID regression **35315934988**:
- 4 final-award lots;
- 4/4 supplier USCC parsed;
- aggregate-only artifact; no supplier addresses, telephone numbers or contact persons.

Candidate records are structurally distinct from final awards and must not create `AWARDED_TO` edges.

All China Pilot 0 statistics are engineering/source-feasibility results, not corruption findings or prevalence estimates.

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

## Cross-source identity layer

A stable-ID-only cross-source entity resolver is now implemented and covered by CI.

Policy:
- exact shared CN-USCC → deterministic `SAME_ORG` auto-merge;
- exact normalized organization name without a shared stable ID → `REVIEW_CANDIDATE` only;
- name similarity, organization type, geography, mission, nationality or other contextual resemblance never auto-merges entities;
- every resolution object carries `corruption_inference=false`.

This advances the China procurement graph beyond source-local nodes without turning ambiguous name matching into asserted relationships.

## Immediate next work

1. run the first bounded real second-source organization enrichment using exact CN-USCC from a lawful machine-readable official/public source; if the authoritative source is interactive/CAPTCHA-only, record `COVERAGE_GAP` rather than bypassing controls;
2. extend the now-working CCGP procurement graph with those provenance-preserving exact-ID enrichment records, never falling back to name-only auto-merging;
3. implement the National Public Resource Trading Platform federation and selected provincial adapters;
4. build official organization-universe adapters for hospitals, SOEs, universities/research institutes and social organizations/charities;
5. build institution-domain crawler contracts for hospital/SOE/institute/university/NGO procurement pages and PDFs;
6. add audit/discipline/administrative/judicial outcome adapters that preserve investigation vs sanction vs penalty vs judgment vs audit-finding classes;
7. add charity/social-organization annual-report, related-party and project-flow extraction;
8. add research grant/patent/technology-transfer edges and delegate publication forensics to 011;
9. freeze China Pilot 1 as a stratified cross-institution dataset rather than a government-only sample;
10. run independent identity/privacy/defamation/temporal-leakage review before any named integrity-review packet is surfaced.

## Hard blockers

No architecture blocker.

China sources vary widely in access method. Interactive systems, CAPTCHAs, authenticated areas and explicit anti-automation controls must not be bypassed. Where machine access is unavailable, OpenIntegrity should use lawful manual/public retrieval, documented interfaces, institution webpages or alternate official sources and record the resulting coverage gap as ABSTAIN.

The ongoing UK Companies House enrichment is no longer the sole critical path; it continues as a portability track while China-first development proceeds.
