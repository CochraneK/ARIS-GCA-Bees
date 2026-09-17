# PREREGISTRATION DRAFT — ARIS4C003

**Version:** 0.1 · 2026-09-18  
**Status:** pre-outcome lock candidate; real confirmatory country×discipline outcomes have not been opened.  
**Study:** *Colonial Legacies and the Global Geography of Disciplinary Advantage*

This document supersedes earlier exploratory wording where it conflicts with the frozen rules below. Any later change requires a dated amendment stating whether real outcome data had already been viewed.

---

## 1. Confirmatory research questions

### RQ1 · Former-colony disciplinary structure

Among contemporary states, is historical exposure to European overseas colonial rule associated with the **shape of present-day disciplinary output and impact**, such that the association varies systematically with the independently coded Imperial/Colonial Knowledge Entanglement Score (IKES)?

No universal positive or negative main effect of colonization is hypothesized. The confirmatory quantity is the **Exposure × IKES gradient** across disciplines.

### RQ2 · Dyadic network persistence

Are former colonizer–dependency country pairs disproportionately connected in contemporary scientific collaboration, and is that excess tie stronger in disciplines with higher IKES?

### RQ3 · Imperial-center corroboration

Across the small set of European overseas imperial centers, do more intensive historical imperial profiles correspond to stronger specialization in higher-IKES disciplines?

This is a small-N corroborative analysis, not a conventional large-N treatment regression.

### RQ4 · Prestige persistence

Do prestige/ranking outcomes show a stronger historical persistence signal than contemporary bibliometric performance would predict?

This is secondary rather than a confirmatory core outcome.

---

## 2. Frozen conceptual disciplines

All 21 concepts in `DISCIPLINE_CROSSWALK.csv` remain reportable:

Anthropology; Archaeology; Geography; Development Studies; Linguistics; Tropical Medicine / colonial-health-related Public Health; Agriculture & Forestry; Geology / Earth-resource sciences; Sociology; Political Science / International Relations; Law; Economics; Public Administration / Social Policy; Education; History; Demography / Population Studies; Mathematics; Physics; Chemistry; Computer Science; Materials Science.

Primary OpenAlex mapping is frozen in `DISCIPLINE_CROSSWALK.csv`. No field is dropped because it produces an inconvenient effect.

---

## 3. Discipline assignment

### 3.1 OpenAlex hierarchy

Primary discipline assignment uses a work's **single `primary_topic` roll-up**.

- subfield selectors use `primary_topic.subfield.id`;
- broad comparator selectors use `primary_topic.field.id`.

This makes each eligible work contribute to at most one ARIS4C003 discipline in the primary analysis.

### 3.2 Unclassified works

Works without a primary topic are not assigned to a discipline. Their rate is reported by country, period, language, and work type as a coverage diagnostic.

### 3.3 Sensitivity only

Using any of a work's secondary topics (`topics.*`) is sensitivity-only and requires explicit multiple-count handling.

---

## 4. IKES moderator

Primary moderator: equal-weight mean of the 11 historical-entanglement dimensions defined in `ENTANGLEMENT_PROTOCOL.md` after Coder A, independent Coder B, and blinded adjudication.

Rules:

- no contemporary country performance enters the scoring;
- no outcome-informed weighting;
- dimensions scored 0–3;
- final adjudicated values are committed as `IKES_FROZEN.csv` before real outcome extraction;
- mean IKES is primary;
- median and leave-one-dimension-out IKES are prespecified sensitivity analyses.

Until `IKES_FROZEN.csv` exists, confirmatory outcome extraction remains gated.

---

## 5. Historical exposure variables

### 5.1 Analysis A primary exposure · former-colony duration

Primary source family: **COLDAT 3.0 / documented Our World in Data processing** of European overseas colonial histories.

Primary variable:

`years_colonized_total`

= total documented years a contemporary independent state spent under the European overseas colonial powers represented in COLDAT.

Primary regression scale:

- raw years centered and divided by one sample standard deviation for coefficient interpretability;
- zero remains zero for states coded as never colonized within the source definition.

Primary Analysis A excludes the eight European COLDAT colonial powers from the former-colony estimand. A broader robustness sample additionally excludes other formal imperial rulers identified in the broader historical source crosswalk.

Prespecified exposure sensitivities:

1. `log1p(years_colonized_total)`;
2. ever-colonized binary;
3. primary/last colonizer strata where sample size permits;
4. broader ICOW dependency-duration/relationship coding after transparent crosswalk.

COLDAT is explicitly an **European overseas-colonial** construct, not a universal measure of every empire.

### 5.2 Analysis B primary exposure · direct former-colonial dyad

Primary dyadic source: CEPII Gravity/GeoDist historical relationship variables, cross-validated where possible against ICOW.

Primary exposure:

`col_dep_ever_ij`

= whether either member of the country pair was ever in a colonial/dependency relationship with the other under the CEPII definition.

Secondary dyadic historical variables:

- end year/duration where available;
- common former colonizer / sibling-colony relationship;
- specific colonizer identity.

Common official/ethnolinguistic language is **not** silently treated as a baseline confounder. Models are reported both before and after language×IKES adjustment because language can be a persistence mechanism.

### 5.3 Analysis C imperial-center intensity

For the eight European overseas colonial powers in COLDAT, primary descriptive intensity is:

`cumulative_colony_years_ruled`

= area under the annual count-of-colonies curve (sum over years of the number of COLDAT colonies under that ruler).

Secondary intensity summaries:

- duration as a colonial ruler;
- peak number of colonies;
- number of distinct colonies.

Inference remains small-N regardless of how many disciplines are observed.

---

## 6. OpenAlex work universe

### 6.1 Primary scholarly-output types

Include:

- `article`
- `review`
- `conference-paper`
- `book`
- `book-chapter`

Rationale: using journal articles alone would structurally underrepresent book-oriented humanities/social sciences, while excluding conference papers would structurally underrepresent Computer Science and some engineering fields.

Primary exclusions:

- preprints, to reduce duplicate publication-stage counting;
- dissertations;
- editorials, letters, corrections/retractions, paratext;
- datasets/software artifacts and data/software papers;
- reports/working papers in the primary analysis because coverage and institutional provenance vary sharply across countries;
- OpenAlex expansion-corpus (`is_xpac=true`) records in the primary analysis because current documentation flags lower/uneven metadata quality;
- retracted works.

### 6.2 Work-type sensitivities

1. article + review only;
2. article + review + conference-paper;
3. primary five types + `report`;
4. Leiden-style/core-publication robustness where reconstructable.

The primary result is not selected based on which type universe gives the largest coefficient.

---

## 7. Country attribution

For each eligible work:

1. collect the set of distinct ISO country codes appearing in `authorships.countries` across all retained authorships;
2. if `n` unique countries are present, assign each country fractional weight `1/n` for that work;
3. the total country weight of a work therefore sums to 1;
4. works with no country information are excluded from country outcome numerators and counted in coverage diagnostics.

This equal-country fractional scheme is primary because it prevents internationally collaborative papers from being counted as a full paper in every country while avoiding strong assumptions about author order/credit.

Sensitivity:

- full counting by country;
- author-affiliation-weighted fractional counting where the snapshot structure allows a reproducible implementation.

OpenAlex caps inline authorships at 100 authors. Large-consortium papers affected by the cap are reported in diagnostics and can be excluded in a prespecified sensitivity.

---

## 8. Time windows

### Primary mature window

**2019–2022**.

Reason: OpenAlex FWCI/normalized citation impact uses publication year plus the three following years. By the end of 2025, works published through 2022 can in principle have a complete four-year citation window; using 2023+ as the main impact period would mix citation maturity with historical exposure.

### Persistence windows

Non-overlapping four-year periods:

- 2007–2010
- 2011–2014
- 2015–2018
- 2019–2022

### Output-only recent sensitivity

- 2023–2025, explicitly **not** used as the primary mature citation-impact window.

The current partial year 2026 is excluded from confirmatory outcomes.

---

## 9. Primary outcome A · fractional publication output

For country `c`, discipline `d`, period `t`, define:

`P_cdt = sum of fractional country weights for eligible works assigned primarily to d in t`.

Construct the **complete eligible country × discipline × period grid** and fill genuine no-output cells with zero rather than dropping them.

### Primary model

Poisson pseudo-maximum-likelihood (PPML):

`E[P_cdt | .] = exp( β * Exposure_c × IKES_d + FE_country×period + FE_discipline×period )`

PPML is used as quasi-maximum-likelihood for non-negative fractional counts; the dependent variable need not be integer-valued. Robust inference is required.

Interpret `exp(β)` as the multiplicative change in relative output associated with a one-SD increase in historical exposure per one-unit increase in IKES, conditional on fixed effects.

### Why PPML rather than raw RCA as the primary regression

PPML:

- retains zero cells;
- avoids arbitrary pseudocounts needed by log-RCA;
- avoids conditioning the primary sample on realized field output through minimum-cell thresholds;
- lets country×period FE absorb aggregate national output scale;
- lets discipline×period FE absorb global discipline size/trends.

### Descriptive specialization metric

RCA remains descriptive:

`RCA_cdt = (P_cdt / P_ct) / (P_dt / P_t)`

Primary plotted transform:

`SRCA = (RCA - 1) / (RCA + 1)`.

RCA/SRCA profile plots are not substituted for the preregistered PPML test.

---

## 10. Primary outcome B · high-impact output

OpenAlex `citation_normalized_percentile` is normalized by work type, publication year, and primary subfield; its boolean `is_in_top_10_percent` is used for the primary elite-impact outcome.

For each country×discipline×period cell:

- denominator `P_impact_cdt` = fractional volume of eligible works with a defined normalized citation percentile;
- numerator `Top10_cdt` = fractional volume among those works with `is_in_top_10_percent = true`.

Primary impact model:

`E[Top10_cdt | .] = exp( β_impact * Exposure_c × IKES_d + FE_country×period + FE_discipline×period + offset(log(P_impact_cdt)) )`

Cells with zero eligible impact denominator cannot enter this rate model; zero Top10 counts with a positive denominator are retained.

Secondary impact outcomes:

- mean FWCI / robust transformed FWCI;
- Top 1% share (secondary due sparsity);
- Leiden Open Edition institutional indicators for triangulation.

---

## 11. Primary outcome C · dyadic scientific collaboration

For unordered country pair `(i,j)`, discipline `d`, period `t`, define `C_ijdt` as fractional eligible coauthored output attributable to direct collaboration between i and j under a reproducible pair-weighting rule.

Primary model candidate:

`E[C_ijdt | .] = exp( β_net * ColonialTie_ij × IKES_d + FE_pair + FE_i×discipline×period + FE_j×discipline×period )`

Estimate by PPML with a high-dimensional fixed-effect implementation that diagnoses separation.

Primary network test:

`ColonialTie_ij × IKES_d`.

Nested language mechanism model adds:

`CommonLanguage_ij × IKES_d`.

Pair FE absorb all time-invariant pair-level baseline affinity, including geographic distance itself; explicit distance/contiguity models without pair FE are secondary gravity robustness specifications.

### Pair weighting

The exact allocation of a multilateral work to bilateral country pairs must be frozen in code before real network outcomes are built. Primary candidate: each international work contributes total dyadic mass 1 distributed equally across all unique unordered country pairs present on that work.

---

## 12. Country/cell eligibility and small-state handling

### Primary output model

No minimum **country×discipline** publication threshold is imposed. Genuine zeros are retained.

A country-period must have:

- valid historical exposure/country crosswalk;
- at least one eligible, country-attributed, primary-topic-classified work among the 21 mapped concepts so its country-period FE is identified.

### Prespecified small-output sensitivities

Repeat Analysis A after requiring aggregate mapped fractional output per four-year country-period of at least:

- 50 works;
- 200 works.

These thresholds are sensitivity analyses and do not determine the primary sample.

Current non-sovereign dependencies/territories are excluded from the primary country-level model because historical and current country mapping is ambiguous; a documented territory-inclusive sensitivity may follow.

No missing historical exposure is imputed in the primary analysis.

---

## 13. Inference

### Analysis A

Primary standard errors/confidence intervals: two-way cluster-robust by **country** and **discipline**.

Because the confirmatory discipline set has only 21 clusters, supplement with:

- discipline-level wild-cluster/bootstrap sensitivity where technically valid;
- a prespecified IKES-label permutation/falsification distribution, clearly described as a sensitivity rather than guaranteed exact randomization inference.

Effect sizes and confidence intervals receive priority over binary significance labels.

### Analysis B

Primary uncertainty: two-way cluster by country pair and discipline, with analogous discipline-cluster sensitivity because IKES varies at the discipline level.

### Analysis C

No naive asymptotic p-value that treats country×discipline cells as independent. Report:

- individual empire profile slopes;
- cumulative-colony-years association with profile slopes/descriptive summaries;
- leave-one-imperial-center-out results;
- discipline-label permutation as a falsification check if assumptions are defensible.

---

## 14. Coverage and bias diagnostics

Before substantive interpretation, report by country/period/discipline where applicable:

- share of eligible works with a primary topic;
- share with any author country;
- language distribution;
- work-type distribution;
- share affected by the 100-author authorship cap where identifiable;
- OpenAlex expansion-corpus share;
- absolute publication counts underlying specialization.

Prespecified sensitivities:

- all languages vs English-only outputs;
- Anglophone vs non-Anglophone country strata once an external language definition is frozen;
- broader topic-assignment rule;
- alternative work-type universes.

An observed association that is confined to English-indexed/core outputs must be described as such rather than generalized to all scholarship.

---

## 15. Multiple testing

Confirmatory family focuses on three gradient coefficients:

1. former-colony output `Exposure × IKES`;
2. former-colony Top10 impact `Exposure × IKES`;
3. dyadic collaboration `ColonialTie × IKES`.

Report all three regardless of result.

Field-specific effects, colonizer-specific effects, ranking analyses, and all-field scans are secondary/exploratory. For broad field-by-field inferential scans, report all coefficients and apply FDR control when p-values are emphasized.

---

## 16. Ranking / prestige analyses

QS, THE, Shanghai GRAS, and Leiden are **not averaged into a master ranking**.

- QS: prestige-heavy institutional layer where reputation components are substantial.
- THE: broad institutional composite.
- Shanghai GRAS: research-oriented ranking layer.
- Leiden Open Edition: open bibliometric institutional robustness.

Numeric ordinal ranks are not treated as interval outcomes in OLS. Prefer published scores/components, top-N presence, ordered categories, or suitable censored/ordinal approaches.

Prestige persistence is interpreted as divergence between ranking/reputation and bibliometric performance, not automatically as research quality.

---

## 17. Confirmatory vs exploratory boundary

### Confirmatory

- 21 frozen concepts;
- final blinded IKES;
- COLDAT former-colony duration exposure;
- CEPII direct colonial dyad;
- primary OpenAlex mapping;
- primary five work types;
- 2019–2022 mature window and four prespecified persistence windows;
- PPML output model;
- PPML Top10 rate model;
- PPML dyadic network model;
- frozen inference strategy.

### Secondary / robustness

- alternative historical exposure definitions;
- work-type universes;
- full vs fractional counting;
- broad vs narrow tropical-health/social-policy topic bundles;
- SRCA/RCA;
- language restrictions;
- Leiden/QS/THE/Shanghai;
- leave-one-colonizer/region-out;
- broader ICOW dependency definitions.

### Exploratory

- all 252 OpenAlex subfields or 4,516 topics;
- data-driven discipline clustering;
- continental/informal empire extensions;
- scientist migration/war/Cold War knowledge-capital shocks;
- case studies selected from residual outliers.

Exploratory findings are never relabeled confirmatory after viewing them.

---

## 18. Required final pre-outcome locks

Before running the real confirmatory outcome models:

- [ ] independent IKES Coder B complete;
- [ ] blinded adjudication complete;
- [ ] `IKES_FROZEN.csv` committed;
- [x] conceptual disciplines frozen;
- [x] OpenAlex discipline crosswalk frozen;
- [x] primary work types frozen;
- [x] primary mature time window frozen;
- [x] primary PPML output model frozen;
- [x] primary Top10 impact model frozen;
- [x] primary dyadic model family frozen;
- [x] country fractional attribution rule frozen;
- [ ] exact country/entity crosswalk frozen;
- [ ] CEPII/COLDAT acquisition manifests created;
- [ ] synthetic inference/separation simulation completed;
- [ ] executable scripts pass synthetic-data tests.

Only after the remaining unchecked gates are closed should the real confirmatory outcome matrix be materialized.
