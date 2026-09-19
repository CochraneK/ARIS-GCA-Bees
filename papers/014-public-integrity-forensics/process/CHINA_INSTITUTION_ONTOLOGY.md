# ARIS4C014 · China Institution Ontology

Date: 2026-09-19
Status: canonical design decision for the China expansion

## Design principle

Do not model Chinese public-integrity entities as one flat list such as `government / hospital / SOE / university / NGO / company`.

Use two orthogonal axes:

1. **legal / organizational identity**
2. **functional domain**

This reduces overlap, makes the universe closer to MECE, and allows one organization to have a stable legal identity while carrying multiple functional roles.

## Axis A · Legal / organizational identity

Core classes:

- government / administrative organ;
- public institution / 事业单位;
- enterprise;
- social organization;
- rural collective economic organization;
- mass organization / other special organization;
- other / unresolved.

Enterprise subtyping should preserve ownership/control context where known:

- central SOE;
- local SOE;
- SOE subsidiary;
- state-capital investment / operation company;
- local financing vehicle;
- private enterprise;
- mixed ownership / unresolved ownership.

Social-organization subtyping should distinguish at least:

- social association / 社会团体;
- social service organization / 民办非企业单位（社会服务机构）;
- foundation / 基金会.

## Axis B · Functional domain

Functional labels are independent of legal identity and may be multi-valued:

- public administration / regulation;
- education;
- healthcare;
- research / science;
- finance;
- infrastructure;
- land / construction / urban development;
- agriculture / rural affairs;
- culture / media / sports;
- social welfare / eldercare / disability services;
- charity / public benefit;
- professional intermediary services;
- public utilities / urban operations;
- procurement / transaction services;
- technology transfer / commercialization;
- other / unresolved.

## Priority institutional modules

The China universe should eventually support the following modules.

### Government and public administration

Include administrative organs, courts/procuratorates where relevant to public records, regulators, development-zone management committees, public-resource trading centers and public-service agencies.

Institutional status is routing/provenance metadata, never a suspicion feature.

### Education

Do not collapse all education into universities.

Support:

- university;
- vocational college;
- secondary school;
- primary school;
- kindergarten;
- other education institution.

### Healthcare

Extend beyond hospitals:

- hospital;
- CDC / disease-control institution;
- maternal and child health institution;
- community health center;
- blood center;
- emergency center;
- medical testing institution;
- rehabilitation institution;
- nursing / eldercare medical institution.

### State-owned and state-capital entities

Support:

- central SOEs;
- local SOEs;
- subsidiaries;
- local financing vehicles;
- state-capital investment and operation platforms;
- government-backed funds and fund managers.

Government investment funds should be graph objects rather than being treated as ordinary companies only.

### Rural collective economy

Add rural collective economic organizations as a first-class legal-identity family, including cooperative and shareholding collective forms where public records expose them.

Potential graph relations include collective assets, land, projects, contractors, managers and counterparties.

### Social organizations and charities

Separate legal form from function. Examples:

- foundation × charity;
- association × industry;
- social-service organization × eldercare.

Mission, advocacy topic, religion, donor nationality or foreign links are not suspicion features.

### Professional intermediaries

Treat important intermediaries as explicit graph nodes, not generic suppliers only:

- procurement agency;
- engineering consultant;
- project supervisor;
- accounting / audit firm;
- appraisal firm;
- law firm;
- testing / certification body.

This enables relations such as:

`Buyer -> Procurement Agency -> Supplier`

and

`Project -> Auditor/Appraiser/Supervisor`.

### Public utilities and urban operations

Support function labels for water, gas, heating, transit, sanitation, parking, municipal engineering, housing, land reserve, urban renewal and industrial-park development.

Their legal identity may still be enterprise / SOE, but their functional role should remain separately queryable.

### Research peripheral entities

Extend the research/university layer to include:

- key laboratories / research platforms;
- technology-transfer centers;
- university science parks;
- university-affiliated enterprises;
- spin-offs;
- affiliated hospitals;
- university / institute foundations and learned societies.

Longer-term research graph:

`publication -> patent -> grant/project -> procurement -> technology transfer -> company`

Publication-forensics signals remain delegated to ARIS4C011.

## Highest-value missing modules

The next high-value additions identified in the 2026-09-19 design review are:

1. rural collective economic organizations;
2. local SOEs / local financing vehicles;
3. government investment / guidance funds;
4. primary/secondary/vocational education institutions;
5. professional intermediary organizations;
6. research peripheral / commercialization entities.

These are priority coverage gaps, not claims that the sectors are unusually corrupt.

## Identity-resolution rules

- Prefer authoritative stable identifiers.
- Exact stable-ID matches may support deterministic entity resolution.
- Name-only matches remain source-local or review candidates.
- Functional similarity, geography, ownership category, political role, religious identity, nationality or organization mission must never auto-merge entities.
- Historical names and organizational status must be time-aware.
- An affiliated hospital must not automatically inherit a university identity.
- A subsidiary must not automatically inherit the parent's identity.

## Integrity semantics

Organization-universe membership is provenance and routing metadata.

No institution type, public-office status, ownership form, NGO mission, religion, advocacy position, nationality, foreign connection or sector membership is itself evidence of corruption.

All named integrity outputs remain human-review leads with `corruption_inference = false`.
