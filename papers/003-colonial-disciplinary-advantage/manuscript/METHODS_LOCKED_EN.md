# Methods — pre-result locked draft

**Paper:** ARIS4C003 — *Colonial Legacies and the Global Geography of Disciplinary Advantage*  
**Draft status:** written after design lock and IKES freeze, before inspection of confirmatory effect estimates.

## Study design

We test whether historical colonial exposure is associated with the
cross-disciplinary shape of contemporary scientific activity, and whether that
association varies systematically with a discipline's historical entanglement
with imperial and colonial systems. The design therefore treats the discipline,
rather than the country alone, as a source of structured variation. The primary
quantity of interest is an interaction between historical exposure and a
pre-outcome discipline characteristic, the Imperial/Colonial Knowledge
Entanglement Score (IKES).

The study separates three estimands that should not be conflated. First, the
former-colony analysis asks whether countries with greater historical colonial
exposure have relatively different contemporary disciplinary portfolios as a
function of IKES. Second, the dyadic analysis asks whether former
colonial/dependency ties are associated with greater contemporary scientific
collaboration specifically in more historically entangled disciplines. Third,
an eight-imperial-center analysis provides small-N corroboration rather than
large-sample causal evidence.

The analyses are associational. Fixed effects remove broad country, discipline,
period, and dyadic heterogeneity relevant to the specified comparisons, but do
not render historical colonial exposure exogenous. We therefore use language
such as “associated with,” “predicts,” and “consistent with historical path
dependence,” rather than interpreting coefficients as identified causal effects
of colonialism.

## Historical exposure data

The primary country exposure is derived from COLDAT 3.0, using the openly
distributed processed series and the original Harvard Dataverse source for
cross-checking. The confirmatory former-colony exposure is total years under
European overseas colonial rule. Exposure remains zero for countries not coded
as colonized in the primary COLDAT scope. The eight European overseas colonial
powers represented by COLDAT — Belgium, the United Kingdom, France, Germany,
the Netherlands, Portugal, Spain, and Italy — are excluded from the primary
former-colony country analysis and analyzed separately as imperial centers.

For country models, colonial duration is centered and standardized using the
eligible historical country universe excluding the eight imperial centers. The
historical data pipeline resolves 159 current-state countries and retains the
untransformed duration measure for descriptive reporting.

The dyadic historical exposure comes from CEPII Gravity version 202211. The
primary pair-level treatment is `col_dep_ever`, indicating a direct historical
colonial/dependency relationship. CEPII data are collapsed to the complete
unordered pair universe among the 159 frozen countries, yielding 12,561 pairs.
Distance, common language, and related historical variables are retained for
secondary or mechanism analyses but do not replace the frozen primary
colonial-tie exposure.

## Discipline set and OpenAlex crosswalk

Before contemporary outcomes were inspected, we froze 21 conceptual
disciplines spanning fields expected to vary substantially in their historical
relationship to empire: Anthropology; Archaeology; Geography; Development
Studies; Linguistics; Tropical Medicine / colonial-health-related Public
Health; Agriculture & Forestry; Geology / Earth-resource sciences; Sociology;
Political Science / International Relations; Law; Economics; Public
Administration / Social Policy; Education; History; Demography / Population
Studies; Mathematics; Physics; Chemistry; Computer Science; and Materials
Science.

Each concept is mapped to a frozen OpenAlex field or subfield selector. A work
is assigned through its single OpenAlex `primary_topic` roll-up, preventing the
same work from contributing to multiple confirmatory study disciplines.
Any-of-topics classification is reserved for sensitivity analysis rather than
the primary estimand.

## Imperial/Colonial Knowledge Entanglement Score

IKES operationalizes historical discipline-level entanglement with imperial and
colonial systems. It is not a moral rating of a field and does not measure
present-day Western dominance. Eleven dimensions were frozen before modern
outcome inspection:

1. colonial administrative demand;
2. territorial survey and mapping;
3. population, people, or language classification;
4. overseas field sites and expeditions;
5. extraction and resource survey;
6. colonial medicine and health governance;
7. agriculture, forestry, and ecological transfer;
8. legal, educational, or institutional transplantation;
9. museums, archives, collections, and specimens;
10. missionary, linguistic, and religious networks; and
11. postwar development-administration continuity.

Each discipline-dimension cell is scored 0–3, with NA allowed when historical
evidence is insufficient. Scores of 2 or 3 require strong scholarly historical
support. Coder A completed an outcome-blind historical pass. The confirmatory
Coder B pass was conducted in an isolated Qoder context using the user-reported
Qwen Flash 3.8 model, under a file-whitelist protocol that excluded Coder A,
the parent project context, and contemporary scientific outcomes.

Unflagged cells are frozen as the arithmetic mean of A and B. A cell requires
explicit outcome-blind adjudication only when either coder is missing or their
absolute difference is at least two points. Twelve of 231 cells met that
criterion. Each was adjudicated against historical evidence before contemporary
outcomes were materialized. Final IKES is the equal-weight mean across available
dimensions; a median-based score is retained as a prespecified sensitivity.
The full coding, adjudication, and frozen matrix are cryptographically linked by
SHA-256 provenance.

## Contemporary scientific outcomes

Contemporary outcomes are constructed from the pinned OpenAlex public Parquet
Works snapshot. The primary work universe contains articles, reviews,
conference papers, books, and book chapters published from 2007 through 2025.
Retracted works, `is_xpac=true` expansion-corpus records, preprints,
dissertations, paratext, corrections, datasets, software, and other
non-primary document types are excluded according to the frozen protocol.

The mature confirmatory window is 2019–2022. The earlier four-year windows
2007–2010, 2011–2014, and 2015–2018 are used to assess temporal persistence.
The 2023–2025 period is retained only as a recent output sensitivity because
citation-normalized impact for that period is not treated as mature.

### Country fractional attribution

For each eligible work, all distinct identifiable OpenAlex country codes across
authorships are collected first. If a work has (n) identifiable countries,
each receives (1/n) country credit. Only after this denominator is determined
are credits restricted to the frozen current-state analysis universe. Thus
works that include out-of-universe countries are not renormalized upward among
retained countries.

The primary output outcome is the sum of fractional country credits within
country × discipline × period cells. Genuine no-output cells in eligible
country-periods are represented as zero rather than omitted.

### Normalized impact

The primary impact outcome uses OpenAlex
`citation_normalized_percentile.is_in_top_10_percent`, which is normalized
within publication year, work type, and primary subfield. For each
country × discipline × period cell, the numerator is fractional Top-10% work
mass and the denominator is fractional work mass with a defined normalized
citation percentile. The confirmatory impact model is a count-rate PPML with
the log denominator as an offset. FWCI and Top-1% measures are secondary.

### Dyadic collaboration attribution

For a work with (n) distinct identifiable countries, total collaboration mass
1 is divided equally across all (n(n-1)/2) unordered pairs, giving each pair
weight (2/[n(n-1)]). The denominator is calculated before restricting
endpoints to the frozen 159-country universe. This preserves the total-work
normalization and avoids inflating retained pairs on papers that also contain
out-of-universe countries.

Positive collaboration cells are then merged onto the complete eligible
CEPII pair × discipline × period grid, with genuine no-collaboration cells
represented as zero.

## Primary statistical models

### Former-colony output

The primary output model is Poisson pseudo-maximum likelihood (PPML):

[
E(P_{cdt}) =
\exp\left[
\beta(Exposure_c \times IKES_d)
+ \alpha_{c\times t}
+ \gamma_{d\times t}
\right].
]

For the single 2019–2022 headline window, the corresponding country and
discipline fixed effects are used. PPML is used as a quasi-maximum-likelihood
estimator for nonnegative fractional outcomes and retains genuine zeros; the
outcome need not be integer Poisson-distributed.

### Former-colony normalized impact

The Top-10% model uses the same interaction and fixed-effect structure, with
fractional Top-10% mass as the outcome and the log of eligible fractional impact
mass as an offset.

### Former-colonial-tie collaboration

The dyadic model is:

[
E(C_{ijdt}) =
\exp\left[
\beta(Tie_{ij} \times IKES_d)
+ \mu_{ij}
+ \lambda_{i\times d\times t}
+ \rho_{j\times d\times t}
\right],
]

where (mu_{ij}) is a pair fixed effect and the endpoint × discipline × period
fixed effects absorb broad country-specific discipline-period collaboration
propensities. The coefficient is identified from whether historically linked
pairs exhibit a systematically different cross-disciplinary collaboration
gradient with IKES.

## Inference and prespecified robustness

The three confirmatory coefficients are exactly:

1. 2019–2022 former-colony output Exposure × IKES;
2. 2019–2022 former-colony Top-10% impact Exposure × IKES; and
3. 2019–2022 former-colonial-tie collaboration ColonialTie × IKES.

Country models use multiway CRV1 clustering by country and discipline; the
dyadic model clusters by pair and discipline. Because the design contains only
21 study disciplines, asymptotic clustered inference is supplemented by a
finite-field falsification layer.

For each headline coefficient, we prespecified:

- 21 leave-one-discipline-out refits;
- 999 fixed-seed IKES-label permutations with seed 20260918;
- a median-IKES sensitivity;
- for country models, minimum mapped country-period output thresholds of 50 and
  200.

Every requested permutation and LOO refit must be reported. A sensitivity layer
with a failed refit is marked invalid rather than silently dropping the failed
case.

Temporal persistence is reported for all four mature four-year windows for
output, impact, and collaboration. The 2023–2025 window is output-only. These
period-specific coefficients are secondary profile estimates and do not expand
the three-member confirmatory family.

## Imperial-center corroboration

The eight COLDAT imperial centers are analyzed separately because they provide
only eight independent historical units. Within each center, contemporary
disciplinary specialization is summarized using symmetric revealed comparative
advantage (SRCA) across the frozen 21 concepts, and the SRCA–IKES profile slope
is estimated. Across the eight centers, profile slopes are related
descriptively to log cumulative colony-years ruled. Leave-one-empire-out and
999 IKES-label permutations are reported. This layer is explicitly
corroborative and is not treated as large-N causal inference.

## Reproducibility and result locking

The design, discipline crosswalk, historical exposures, IKES rubric, Coder
inputs, adjudication, and model specification are versioned in the repository.
The strict pre-outcome gate had to report `DESIGN_LOCKED /
OUTCOME_UNLOCKED` with zero problems before any modern confirmatory outcome
was materialized.

The first complete result package is generated by automated workflows and
SHA-256 locked before human inspection. Primary figures and tables were also
specified before result inspection so that null or inconvenient analyses cannot
be replaced post hoc by more favorable visualizations.
