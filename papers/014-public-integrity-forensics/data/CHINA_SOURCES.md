# China public/open web source map

Date checked: 2026-09-18

This file is a source-discovery map for ARIS4C014. Inclusion means the source is potentially useful; it does not imply blanket permission for high-frequency scraping. Respect published interfaces, robots/terms, access controls and rate limits.

## Procurement and public resources

### China Government Procurement Network / 中国政府采购网

Domain: `ccgp.gov.cn`

Roles:
- procurement notices;
- winning/transaction notices;
- contract notices;
- procurement-intention disclosures;
- procurement serious-illegality records;
- agency records;
- official data standards.

Important implementation note:
China Government Procurement Network publishes an official data-interface specification. The source map should prefer documented interfaces/standards over brittle page scraping where available.

### National Public Resource Trading Platform / 全国公共资源交易平台

Domain: `ggzy.gov.cn`

Roles:
- public-resource transactions;
- tenders and awards;
- links to provincial trading platforms;
- cross-domain procurement / construction / resource transactions.

The national platform links provincial platforms and other official transaction systems, so China ingestion should treat national + provincial portals as a federation rather than one complete table.

## Enterprise / supplier identity

### National Enterprise Credit Information Publicity System / 国家企业信用信息公示系统

Domain family: `gsxt.gov.cn`

Roles:
- enterprise identity;
- unified social credit code / registration;
- business status;
- abnormal-operation and serious-illegality public lists;
- corporate record verification.

Use stable identifiers where available. Avoid automated high-frequency scraping if the site imposes interactive or access controls.

### Credit China / 信用中国

Domain: `creditchina.gov.cn`

Roles:
- public credit information;
- administrative penalty/public credit records where published;
- cross-agency credit references.

Penalty/finding type, authority and date must be preserved.

## SOEs

### State-owned Assets Supervision and Administration Commission / 国务院国资委

Domain: `sasac.gov.cn`

Roles:
- current central SOE list;
- group identity;
- official SOE news/disclosures;
- links to central SOEs and local SASACs.

As of 2026-07-11, SASAC publishes a current central-enterprise list. This list is an organization-universe source, not a risk list.

### SOE own procurement platforms

Each SOE/group may publish procurement through its own e-commerce/tender platform.

Build source plugins by group and subsidiary, with:
- official-domain verification;
- supplier identifiers;
- tender/award numbers;
- publication date;
- procurement method;
- attachments;
- historical URL/checksum.

## Hospitals and health institutions

### National Health Commission / 国家卫生健康委员会

Domains:
- `nhc.gov.cn`
- `zwfw.nhc.gov.cn`

Roles:
- medical institution queries;
- hospital practice registration;
- selected licensed-specialty institution lists;
- NHC-supervised social-organization lists;
- public health-sector information.

Hospital universe building should combine NHC/regional-health-authority records with hospital official sites.

### Hospital official websites

Roles:
- procurement notices;
- equipment/reagent/service purchasing;
- leadership pages;
- annual/budget reports where published;
- internal audit/discipline/public notices;
- affiliated company and university links.

Hospital-site data are institution-published facts and require timestamped snapshots.

## Research institutes and universities

### China Government Procurement Network

Many universities and research institutes publish instrument/equipment/service procurement through CCGP.

Current public pages visibly include procurement notices for universities and Chinese Academy of Sciences institutes, so institution-type routing can be applied directly to buyer names.

### National Natural Science Foundation of China / 国家自然科学基金委员会

Domains:
- `nsfc.gov.cn`
- `grants.nsfc.gov.cn`

Roles:
- funding rules;
- institution universe;
- public announcements;
- concluded-project information where publicly queryable.

Important limitation:
some person-level funded-project queries are no longer openly searchable and require account/institution access. Do not bypass these access controls.

### Ministry of Science and Technology / national science-program portals

Potential roles:
- national research programs;
- project calls/results;
- participating institutions.

Add source-specific adapters only after verifying current public interfaces.

### Research institute / university official websites

Roles:
- grant/result notices;
- procurement;
- leadership;
- spin-off / technology-transfer disclosures;
- patents;
- annual reports;
- disciplinary/research-integrity notices.

ARIS4C011 should be reused for publication-level forensic checks.

## NGOs / charities / social organizations

### Ministry of Civil Affairs social-organization public systems

Target records:
- registered social organizations;
- foundations;
- charities;
- annual-report/public disclosure where available;
- legal representative / responsible-person records where lawfully public;
- regulator findings.

### Charity China / 慈善中国

Target records:
- charitable organizations;
- public fundraising;
- charity projects and disclosures.

Donation/project flows are factual context, not wrongdoing indicators.

### Health-sector supervised social organizations

NHC exposes a query/list for organizations it directly supervises or manages, useful for sector-specific entity resolution.

## Audit / disciplinary / enforcement outcome sources

### National Audit Office / 审计署

Domain: `audit.gov.cn`

Roles:
- audit announcements;
- central-budget audit results;
- rectification reports;
- named institutional findings when officially published.

These can serve as documented outcome labels, but the exact finding and responsible entity must be preserved.

### Central Commission for Discipline Inspection / National Commission of Supervision

Domain: `ccdi.gov.cn`

Roles:
- public investigation notices;
- disciplinary sanction notices;
- notices involving officials, SOE/financial executives and other public-sector personnel.

Outcome classes must distinguish:
- investigation;
- disciplinary finding/sanction;
- later judicial outcome if any.

Investigation is not equivalent to guilt or conviction.

### Courts / public execution systems

Use only lawful public interfaces and preserve the type of court/public-execution record.

Do not infer a broader integrity conclusion from an unrelated civil dispute or enforcement entry.

## Media and general Chinese web

### Reputable news media

Use for:
- source discovery;
- chronology;
- locating public documents;
- identifying aliases or earlier reports.

Store:
- article URL;
- publication date;
- outlet;
- exact attributed claim;
- cited primary source if present.

Journalistic allegations remain separate from official findings.

### Search engines and public web

Use to discover:
- institution subdomains;
- archived procurement PDFs;
- old leadership pages;
- subsidiary names;
- supplier aliases;
- public WeChat/Weibo/forum references.

These are discovery surfaces, not automatically evidence sources.

## Source-priority rule

For a concrete factual claim, prefer:

1. official structured source;
2. official institution/regulator page or document;
3. official audit/enforcement/judicial record;
4. reputable journalism with traceable primary sources;
5. licensed commercial database;
6. public social/web lead.

Lower-ranked sources may discover a lead but cannot overwrite stronger contradictory primary records without explicit review.
