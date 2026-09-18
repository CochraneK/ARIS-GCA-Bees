# China Pilot 0 Results

Date: 2026-09-18  
Project: ARIS4C014 / OpenIntegrity  
Status: frozen source-feasibility record

## Scope

China Pilot 0 tests whether OpenIntegrity can reproducibly discover and normalize public Chinese procurement/institution records while preserving:

- source provenance;
- publication/retrieval time;
- institution routing;
- final-award versus candidate semantics;
- coverage gaps as explicit missingness;
- privacy-minimized public artifacts;
- `corruption_inference = false`.

This is a **source-feasibility pilot**, not a corruption-prevalence study and not a ranking of organizations or suppliers.

## Pilot 0A — CCGP award-list discovery

Workflow run: **35314543749**  
Artifact: `aris4c014-china-ccgp-pilot0`  
Artifact ID: **10534773079**  
Artifact digest:  
`sha256:083e07dbc447a9e159ef2632ab5459ab1c9fb68b10dd7b239dbc58bfcd635e78`

Bounded live collection from the public China Government Procurement Network award-result lists:

- unique award-notice leads: **36**;
- buyer metadata coverage: **100%**;
- publication-time coverage: **100%**;
- heuristic institution routing:
  - government: 13;
  - hospital: 2;
  - university: 10;
  - public institution: 3;
  - other / not confidently classified from buyer name alone: 8.

Interpretation:

- public CCGP list pages are machine-discoverable in a bounded workflow;
- buyer and publication-time fields are sufficiently available for first-stage routing in this sample;
- name-based institution type is routing metadata only and should later be replaced/enriched by authoritative organization-universe joins;
- the distribution above is **not** an estimate of corruption, procurement intensity, or the population distribution of Chinese public institutions.

### Parser lesson

The first live parser returned zero notices because CCGP list items used directory-relative detail links. The adapter was corrected to resolve the URL first and then validate that the resolved destination belongs to the award-result directory.

A parser miss is therefore treated as an engineering coverage gap, not as a statement that a source contains no records.

## Pilot 0B — official institution-universe seeds

Workflow run: **35314852919**  
Artifact: `aris4c014-china-institution-universe-pilot0`  
Artifact ID: **10534003915**  
Artifact digest:  
`sha256:365f524f4a4c952f8ca60c02d7f5e324c27d30e75708fed47ae2d8bfb79108c8`

Sources attempted:

1. State-owned Assets Supervision and Administration Commission central-enterprise list;
2. Chinese Academy of Sciences official research-unit page.

Result:

- source families attempted: **2**;
- successfully machine-covered source families: **1**;
- unavailable source families: **1**;
- official organization seeds successfully normalized: **106**;
- normalized type among successfully retrieved seeds: **research_institute = 106**.

The SASAC source was recorded as unavailable in the GitHub Actions environment because its TLS certificate chain could not be validated there. TLS verification was **not** disabled.

Interpretation:

- the 106 records are the current machine-covered CAS research-unit seeds from this bounded adapter, not the total number of research institutes in China;
- the SASAC failure is `source_unavailable`, not “zero SOEs”;
- organization-universe membership is a provenance/routing fact, not an integrity-risk feature.

## Pilot 0C — CCGP award-detail normalization

Latest extended workflow run: **35315845079**  
Head commit: `d3721925bf640390d40ff8185153dbfe970cc94b`  
Artifact: `aris4c014-china-ccgp-detail-pilot0`  
Artifact ID: **10535041457**  
Artifact digest:  
`sha256:e699d06f5ceeb3897b5ed137c3c1cdd31af4d5195338ef9a0a707e01b072ff99`

Bounded live sample:

- notices requested: **12**;
- normalized supplier-result records: **14**;
- final-award records: **11**;
- ranked candidate records: **3**;
- notices with no supplier-result parsed under current templates: **2**;
- supplier-name coverage among parsed result records: **100%**;
- currency-value coverage among parsed result records: **100%**;
- supplier-USCC coverage in this particular moving 12-notice sample: **0%**;
- percentage-pricing records in this particular bounded sample: **0**.

The 0% USCC rate in this moving sample is a property of the sampled page templates, not evidence that CCGP does not expose supplier stable IDs. A dedicated official-page regression below verifies the stable-ID path.

Because one notice can produce multiple supplier/candidate records, the record count and notice count are not expected to match.

### Semantics fixed during Pilot 0

#### Central vs local CCGP body schemas

Observed public templates include at least:

Central-style:

```
一、项目编号
二、项目名称
三、中标（成交）信息
```

and local-style variants such as:

```
一、项目编号
二、采购计划备案号
三、项目名称
四、中标（成交）信息
```

plus variants using headings such as `三、中标信息`.

The parser now supports these separately rather than assuming one national DOM/body schema.

#### Amount units

Observed amount representations include:

- `中标（成交）金额：84.6（万元）`;
- `中标金额(万元)：259.071`;
- percentage/discount quotations in other CCGP pages.

Rules:

- `万元` is normalized to yuan;
- currency values are rounded to cent precision to avoid binary floating-point artifacts;
- percentage/discount values must remain a non-currency pricing basis and cannot be converted into an invented contract value.

#### Final award vs candidate ranking

Some public notices encode strings such as:

```
供应商名称：第一中标候选人：...
供应商名称：第二中标候选人：...
```

OpenIntegrity now records:

- `result_status = awarded` for a final award;
- `result_status = candidate` plus `candidate_rank` for ranked candidates.

A candidate record must **not** generate an `AWARDED_TO` graph edge unless a separate final-award record establishes that outcome.

## Pilot 0D — stable supplier identity regression

Workflow run: **35315934988**  
Artifact: `aris4c014-china-ccgp-uscc-regression`  
Artifact ID: **10535420478**  
Artifact digest:  
`sha256:caa94f9505fbef9759e493e969471e0a8ff6d21827d62d442d92b0a4d3ecb773`

A fixed public CCGP award page known to expose supplier unified social credit codes was used as a regression target.

Aggregate-only result:

- project ID: `SHGP-2026-A409`;
- final-award lots: **4**;
- final-award lots with parsed USCC: **4**;
- stable-ID coverage in this regression page: **100%**;
- parser warnings: **0**.

The regression artifact intentionally does not emit supplier names, addresses, phone numbers or contact persons.

OpenIntegrity treats a normalized USCC as a stable organization identifier. Supplier nodes with an exact USCC can therefore use a stable graph identity such as `CN-USCC:<code>`; supplier-name-only records remain source-local until separately resolved.

This does not make an award or supplier suspicious. It only improves identity resolution.

## Privacy behavior

Pilot 0 public normalized artifacts intentionally exclude:

- personal contact names;
- telephone numbers;
- supplier/buyer street addresses when not needed for the current feasibility question.

The safe live diagnostic prints only procurement-structure fields needed to debug parsers and filters contact/address fields.

This is data minimization, not a claim that those fields are never useful. Address information may be introduced in a later dedicated related-party/address detector only when needed, with explicit provenance and public-output controls.

## Evidence interpretation

Pilot 0 establishes that:

1. current CCGP public award-list discovery can generate reproducible notice leads;
2. a bounded set of award details can be normalized into buyer/project/supplier/result/value structures, including stable supplier USCC where the official page exposes it;
3. final award and ranked candidate roles can be distinguished and projected into different graph edges;
4. official Chinese institution-universe pages can be used as organization seeds where machine access succeeds;
5. source failures and parser misses can be represented as explicit coverage gaps rather than false negative evidence.

Pilot 0 does **not** establish:

- that any named buyer, supplier or institution is corrupt;
- that any procurement price is anomalous;
- that a repeated supplier relationship is improper;
- that a candidate relationship is a final award;
- that an institution missing from a current adapter does not exist;
- population-level prevalence or risk estimates.

## CI state

After candidate/local-template/currency-normalization fixes, the canonical OpenIntegrity CI run for commit `5f3f7544bdb15d14a6c4067e885785932f7eb382` passed.

The suite includes the existing OpenIntegrity invariants plus China-specific tests for:

- source tiers;
- web-lead evidence restrictions;
- CCGP discovery;
- institution routing;
- central/local detail schemas;
- percentage-price semantics;
- candidate-vs-award semantics;
- official-universe coverage-gap handling.

## Next Pilot

China Pilot 1 should move from source parsing to **cross-source entity and event graphs**:

1. convert final CCGP results into procurement graph relations;
2. keep candidate relations separate from final awards;
3. resolve suppliers to authoritative organization identifiers where lawfully available;
4. expand hospital, SOE, university/research, NGO/social-organization universes;
5. add the National Public Resource Trading Platform federation;
6. add audit/disciplinary/administrative outcome adapters while preserving outcome type;
7. freeze a stratified sample across hospitals, SOEs, research institutes/universities, social organizations and government/public institutions;
8. evaluate entity-join rate, source coverage, parser miss rate and temporal provenance before any risk-yield analysis.
