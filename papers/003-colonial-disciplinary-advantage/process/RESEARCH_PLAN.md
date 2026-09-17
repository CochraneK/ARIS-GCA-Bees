# RESEARCH PLAN — ARIS4C003

## 0. Status

ARIS entry complete. This document defines the executable design before large-scale outcome collection.

Primary principle: **historical theory first, contemporary outcomes second.** Discipline coding and primary hypotheses must be frozen before inspecting the full contemporary country-by-field outcome matrix.

---

## 1. Units of analysis

The project has three linked datasets.

### A. Country × discipline × year panel

Primary unit for specialization and impact analyses.

Core fields:
- country
- discipline / field taxonomy id
- year or multi-year window
- publication output
- fractional output
- citation impact
- elite-paper share
- international collaboration measures
- exposure variables
- controls

### B. Country-pair × discipline × year panel

Unit for former-colonial network persistence.

Core fields:
- country_i
- country_j
- discipline
- year/window
- coauthorship intensity
- former-colonial tie
- common colonizer
- common language
- geographic distance
- bilateral scientific size
- other dyadic controls

### C. University × discipline × ranking-year crosswalk

Secondary robustness/prestige layer.

Core fields:
- institution
- country
- discipline
- ranking source/year
- rank / score / component scores where legally/publicly available
- OpenAlex/Leiden bibliometric counterparts

Do not merge these layers into a single opaque score.

---

## 2. Primary exposures

### 2.1 Imperial-center exposure

Candidate variables, to be evaluated for reproducibility and coverage:

- `imperial_ruler_ever`
- `years_as_overseas_colonial_ruler`
- `dependency_years_total`
- `number_dependencies`
- weighted dependency-years by population/territory where defensible

The primary imperial-center exposure should be chosen before outcome inspection and should have a transparent historical interpretation. Avoid a bespoke weighted index unless each weight has a documented rationale.

### 2.2 Former-colony/dependency exposure

Candidate variables:

- `ever_colonized_or_dependent`
- `years_under_external_rule`
- `primary_colonizer`
- `number_colonizers`
- `independence_year`
- `independence_cohort`

Do not force a common coefficient for all former colonies.

### 2.3 Dyadic exposure

- `direct_colonial_tie_ij`
- `common_colonizer_ij`
- `common_official_or_colonial_language_ij`

ICOW and CEPII are initial candidates. Dataset versions and coding rules must be recorded.

---

## 3. Discipline construct

### 3.1 Confirmatory discipline set

Freeze before full outcome inspection.

Candidate high-entanglement anchors:
- Anthropology
- Archaeology
- Geography
- Development Studies
- Linguistics
- Tropical Medicine / carefully mapped Public Health topics
- Agriculture & Forestry
- Geology / Earth-resource sciences

Candidate medium-entanglement:
- Sociology
- Political Science / International Relations
- Law
- Economics
- Public Administration / Social Policy
- Education
- History
- Demography / Population Studies

Candidate comparison fields:
- Mathematics
- Physics
- Chemistry
- Computer Science
- selected modern engineering/materials sciences

### 3.2 Entanglement score

Preferred approach: a continuous score generated from a preregistered historical coding rubric.

Possible rubric dimensions, each coded independently:

1. colonial administrative demand;
2. territorial survey/mapping;
3. classification of peoples/languages/populations;
4. overseas expedition/field-site dependence;
5. extractive/resource survey;
6. colonial medicine/public-health role;
7. agriculture/forestry transfer;
8. legal/educational institutional transplantation;
9. museum/archive/specimen infrastructure;
10. missionary/linguistic networks;
11. postwar development-administration continuity.

Recommended coding: 0 = little/unclear; 1 = documented but non-central; 2 = substantial; 3 = foundational/major historical role.

Use at least two independent coders or two independent blinded evidence summaries. Adjudicate disagreements before outcome analysis. Report inter-rater reliability.

### 3.3 Alternative discipline taxonomies

Run robustness across at least two taxonomies where mapping is feasible, e.g. OpenAlex field/subfield/topic hierarchy and a ranking/WoS-like subject grouping. Predefine crosswalk rules.

---

## 4. Outcomes

### 4.1 Primary bibliometric specialization outcomes

Prefer fractional authorship/institutional counting for country attribution.

For country c, discipline d, time t:

`RCA_output = (fractional_output_cdt / total_fractional_output_ct) / (world_output_dt / world_output_t)`

Also compute:
- log RCA or symmetric RCA transformation;
- minimum-volume filtered RCA;
- output share residualized on total national science size;
- alternative specialization metric from scientometrics literature.

### 4.2 Impact outcomes

- field/year normalized citation impact;
- PP(top 10%);
- PP(top 1%);
- citation-based comparative advantage;
- robustness excluding self-citations where available.

### 4.3 Network outcomes

Country-level:
- PP(international collaboration)
- number/share of international partners
- degree / strength
- betweenness or brokerage only where network size/stability supports it

Dyadic:
- fractional coauthored-paper intensity
- normalized collaboration propensity relative to expected volume from each country's field size

### 4.4 Prestige/ranking outcomes

Secondary, explicitly separated from bibliometric outcomes:
- QS subject ranking / component indicators when accessible
- THE subject ranking
- Shanghai GRAS
- Leiden Open Edition indicators as an independent bibliometric benchmark

Do not equate ordinal rank spacing with cardinal performance. Prefer scores/component indicators when available. For ranks, use rank bins/top-N presence/survival-type or ordinal models rather than naive linear rank regression.

---

## 5. Primary hypotheses and models

### H1/H2: imperial exposure × discipline entanglement

Primary fixed-effect structure:

`Y_cdt = beta * ImperialExposure_c × Entanglement_d + alpha_c + gamma_d + tau_t + Z_cdt + error_cdt`

where:
- `alpha_c`: country fixed effects
- `gamma_d`: discipline fixed effects
- `tau_t`: year/window fixed effects

Time-invariant country exposure is absorbed by country fixed effects; the estimand is the cross-disciplinary interaction.

For repeated windows, consider country×time fixed effects if feasible to absorb changing national science capacity:

`Y_cdt = beta * ImperialExposure_c × Entanglement_d + alpha_ct + gamma_dt + error_cdt`

This is a stronger design because country-year factors absorb GDP, total science expansion, policy shocks, etc. Identification then comes from relative field structure within the same country-year.

### H3: specificity

Estimate field-specific coefficients or interact exposure with prespecified field groups. Test the joint gradient rather than declaring success from isolated significant fields.

### H4: colonized-state heterogeneity

Use stratified or hierarchical models by:
- primary colonizer;
- independence cohort;
- duration;
- common language;
- institutional/education legacy proxies.

Treat this as secondary unless measurement quality is sufficient for a prespecified model.

### H5: network persistence

Dyadic model:

`Collaboration_ijdt ~ ColonialTie_ij × Entanglement_d + dyad controls + country_i FE + country_j FE + discipline/time FE`

Potential gravity-style controls:
- geographic distance
- common border
- common language
- bilateral scientific mass
- GDP/population
- region
- migration/trade where available and theoretically justified

For count outcomes consider PPML/negative-binomial depending distribution and fixed-effect feasibility.

### H6: prestige persistence

Estimate expected prestige from contemporary bibliometrics and test whether imperial exposure predicts positive residual prestige in relevant fields.

Example:

`Prestige_cd = f(BibliometricPerformance_cd, InstitutionSize, Country) + ImperialExposure_c × Entanglement_d`

Do not call this a causal "premium" unless the identification strategy supports that language. Default label: **prestige residual/persistence signal**.

---

## 6. Controls and identification strategy

### Preferred strategy

Rely on within-country cross-disciplinary comparisons with strong fixed effects rather than trying to control every national characteristic in a simple cross-sectional regression.

### Candidate covariates / robustness

- population
- GDP / GDP per capita
- R&D expenditure
- tertiary education / researchers per capita
- university-system age / historical university stock
- official language / English status
- region
- geographic isolation
- political stability/institutions where justified
- overall international collaboration

Do not automatically include post-treatment variables if the estimand is the total long-run effect of historical empire. Distinguish:

- confounders of historical exposure/outcome association;
- mediators through which historical knowledge capital persists;
- modern robustness covariates.

A DAG should explicitly classify each before final model selection.

---

## 7. Time design

Preferred bibliometric windows: rolling or fixed 4–5 year periods from the earliest reasonably reliable modern coverage through the latest complete period.

Use time primarily to assess persistence/change, not to pretend there is pre-treatment modern bibliometric data for nineteenth-century empire.

Possible estimand:

`ImperialExposure × Entanglement × Time`

This tests whether the specialization gradient is weakening, stable, or strengthening in recent decades.

Avoid causal language implying a modern difference-in-differences treatment unless a credible historical event-time design is separately developed.

---

## 8. Data-quality rules

1. Fractional counting is primary for cross-country output/impact.
2. Set minimum field-country publication thresholds before computing unstable ratios.
3. Report missingness and coverage by country, field, language, and time.
4. Conduct Anglophone/database-coverage sensitivity analysis.
5. Avoid manually scraped ranking data when terms prohibit redistribution or automated access.
6. Record all source versions/download dates.
7. Store raw immutable source files separately from derived datasets when licensing allows.
8. Do not redistribute ICOW or other sources contrary to their stated redistribution requests; provide scripts/instructions to reconstruct instead.

---

## 9. Ranking interpretation plan

Rankings are not primary truth labels.

### QS
Treat as strongly reputation-mediated where subject methodology gives high weight to academic reputation. Use for prestige-persistence tests and triangulation.

### THE
Treat as a broad institutional performance composite spanning teaching, research environment/quality, international outlook, and industry; subject categories are broader than many bibliometric taxonomies.

### Shanghai GRAS
Treat as a more research-output/impact-oriented institutional layer, subject to its own field coverage and indicator definitions.

### Leiden Open Edition
Use as independent/open bibliometric robustness. Its 2025 edition is OpenAlex-based and provides impact and collaboration indicators including PP(top 1/5/10%), MNCS, and international collaboration measures.

Cross-ranking disagreement is analytically informative and should not be hidden by averaging all products.

---

## 10. Planned robustness and falsification tests

Minimum set:

- fractional vs full counting;
- RCA vs symmetric RCA vs alternative specialization measure;
- output vs citation vs top-paper outcomes;
- alternative field taxonomy;
- alternative historical exposure measure;
- minimum-volume thresholds;
- exclude very small states;
- exclude current overseas territories/dependencies;
- leave-one-empire-out;
- leave-one-region-out;
- Anglophone-only vs non-Anglophone analyses;
- English-language publication restriction sensitivity;
- recent-period vs longer-window estimates;
- placebo/comparison disciplines;
- random/permuted entanglement-score falsification;
- blinded entanglement scoring before outcome inspection.

If only one analytic choice yields the headline result, the claim should be downgraded.

---

## 11. Multiple testing

The confirmatory test should center on a small number of interaction coefficients/gradient tests.

For exploratory field-by-field coefficients:
- report all fields, not only significant ones;
- control false discovery rate where inferential p-values are emphasized;
- visualize the full coefficient distribution and uncertainty;
- label exploratory results explicitly.

---

## 12. Data source candidates and current feasibility notes

### ICOW Colonial History Data
Useful for colonial rulers, dependency relations, independence information, and dyadic history. Current public page notes state-level coverage for COW members and requests that users direct others to the official source rather than redistribute the dataset.

### CEPII GeoDist / Gravity
Candidate for distance, common language, colonial link, common colonizer and related dyadic controls. Verify exact version/licence before use.

### OpenAlex
Primary candidate for scalable contemporary works/institution/country/field data. Prefer documented bulk/snapshot or reproducible public-access route for large analyses rather than fragile ad-hoc page scraping.

### Leiden Ranking Open Edition 2025
OpenAlex-based university indicators, publication windows 2006–2009 through 2020–2023, including normalized impact and collaboration indicators. Useful both for validation and institutional robustness.

### Ranking products
Use only publicly obtainable/licensed data. Keep derived summaries if allowed; otherwise store extraction scripts/instructions and not copyrighted/proprietary tables.

---

## 13. GPTPage / no-paid-LLM-API policy

ARIS reasoning/reviewer stages that would normally call an external paid LLM API are replaced by reproducible prompt packets in `GPTPAGE_HANDOFF.md`.

The GPTPage output must be copied back into a dated file under `process/gptpage/` before it is treated as project evidence. Human/ChatGPT-web outputs are advisory and never silently overwrite frozen hypotheses.

This policy concerns LLM/reviewer calls. Public scientific data access should preferentially use bulk downloads, snapshots, or documented public endpoints and must be separately recorded for reproducibility.

---

## 14. Pre-data-analysis gate

Before the full outcome matrix is inspected, freeze:

- [ ] exact imperial exposure variable(s)
- [ ] exact former-colony variable(s)
- [ ] confirmatory discipline set
- [ ] entanglement rubric and coder procedure
- [ ] primary field taxonomy
- [ ] primary bibliometric window
- [ ] primary outcome transformation
- [ ] minimum publication threshold
- [ ] fixed-effect specification
- [ ] primary robustness set
- [ ] missing-data rules
- [ ] exclusion rules
- [ ] multiple-testing policy

Only after this checklist is frozen should the exploratory all-field scan be opened.
