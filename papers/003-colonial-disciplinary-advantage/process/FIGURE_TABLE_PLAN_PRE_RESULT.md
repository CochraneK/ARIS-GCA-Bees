# ARIS4C003 — PRE-RESULT FIGURE & TABLE PLAN

**Frozen:** 2026-09-19  
**Status when frozen:** DESIGN_LOCKED / OUTCOME_UNLOCKED; OpenAlex materialization running; no confirmatory effect estimate inspected.

The purpose of this plan is to prevent outcome-driven visualization selection.
Every primary figure listed below should be produced regardless of sign,
magnitude, or statistical significance. Supplementary figures may expand, but
not replace, inconvenient primary panels.

## Main figures

### Figure 1 — Research design and estimands

A non-outcome schematic showing:

- historical exposure families: former-colony duration, former-colonial dyad,
  imperial-center intensity;
- frozen D01–D21 discipline layer;
- independently coded IKES;
- three modern outcome families: fractional output, Top-10% impact,
  collaboration;
- separation of confirmatory, secondary temporal, and small-N corroboration
  analyses.

Purpose: make the interaction design intelligible without implying causal
identification.

### Figure 2 — Frozen IKES measurement structure

Required panels:

A. 21 disciplines ordered by final frozen IKES;  
B. 21×11 heatmap of frozen dimension scores;  
C. A-vs-B discipline-level IKES scatter with 1:1 line;  
D. distribution of 231 A/B cell differences, marking the 12 adjudicated cells.

Show Coder A, confirmatory Coder B, and adjudicated final scores transparently.
Do not suppress low-agreement dimensions.

### Figure 3 — Historical exposure geography

Required panels:

A. world map of COLDAT former-colony duration for the frozen current-state
   country universe;
B. eight imperial-center cumulative colony-years / peak simultaneous colonies;
C. CEPII former-colonial/dependency network summary.

Historical-only; no modern scientific performance.

### Figure 4 — Three headline estimates

Forest-style display containing exactly the frozen confirmatory family:

1. 2019–2022 former-colony output Exposure × IKES;
2. 2019–2022 former-colony Top-10% impact-rate Exposure × IKES;
3. 2019–2022 former-colonial-tie collaboration ColonialTie × IKES.

Show log coefficient, 95% interval, and multiplicative transform. Do not add or
remove headline rows based on significance.

### Figure 5 — Temporal persistence profile

For each of the three outcome families, show prespecified period-specific
interaction estimates for:

- 2007–2010;
- 2011–2014;
- 2015–2018;
- 2019–2022.

Add 2023–2025 only to the output panel and label it output-only sensitivity.
Plot all periods even if the trajectory is non-monotonic or null.

### Figure 6 — Finite-discipline robustness

Required panels for each headline coefficient:

A. 21 leave-one-discipline-out estimates, with the frozen full estimate
   overlaid;
B. range/sign stability annotation;
C. identify any discipline whose removal materially shifts the coefficient,
   without retrospectively deleting it from the primary analysis.

### Figure 7 — IKES-label permutation falsification

Three panels, one per headline model:

- full 999-repetition null distribution;
- observed frozen coefficient;
- two-sided Monte Carlo p-value using the preregistered +1 correction.

If any permutation refit fails, the panel must prominently state that the
permutation layer is invalid rather than silently plotting successful fits.

### Figure 8 — Imperial-center small-N corroboration

Required:

A. each of the eight imperial centers' 21-field SRCA-vs-IKES profile slope;
B. profile slope vs log1p cumulative colony-years;
C. leave-one-empire-out across-empire slopes;
D. 999 discipline-label permutation reference distribution.

Label N=8 prominently and describe this as corroboration, not large-N causal
inference.

## Supplementary figures

S1. OpenAlex coverage by discipline and period.  
S2. Country-period mapped-output distribution and >=50 / >=200 thresholds.  
S3. Final IKES mean-vs-median sensitivity.  
S4. Country attribution / identifiable-country coverage diagnostics.  
S5. Dyad collaboration-mass distribution, zeros and positive cells.  
S6. Colonizer-stratified descriptive profiles, if run as prespecified secondary
    analysis.  
S7. Language/work-type sensitivity diagnostics.  
S8. Leiden Open Edition processing/indicator robustness.  
S9. External ranking/prestige triangulation only where licensing permits.

## Main tables

### Table 1 — Frozen 21-discipline operationalization

Columns:

- concept_id;
- conceptual discipline;
- OpenAlex selector level;
- OpenAlex IDs;
- final IKES;
- IKES median;
- crosswalk caveat.

### Table 2 — Historical exposure and analysis samples

Report:

- country universe;
- ever-colonized count;
- eight imperial centers;
- CEPII pair universe / colonial-tie count;
- country×discipline×period panel dimensions;
- dyad×discipline×period panel dimensions;
- coverage/missingness diagnostics.

### Table 3 — Confirmatory models

Exactly the three headline interaction coefficients with:

- estimate;
- robust SE;
- 95% interval;
- asymptotic p-value;
- permutation p-value;
- multiplicative effect;
- N countries/pairs;
- N disciplines.

### Table 4 — Prespecified sensitivity summary

Include:

- IKES median;
- >=50 mapped-output;
- >=200 mapped-output;
- LOO min/max and sign stability;
- temporal profile;
- permutation validity.

## Visualization integrity rules

1. No figure is removed because its result is null or inconvenient.
2. Axis ranges must not be chosen to exaggerate tiny differences.
3. Main-effect significance stars are not used as the primary visual language.
4. Report uncertainty intervals wherever defined.
5. Categorical field colors/order may be chosen for readability but not to imply
   unregistered field groupings.
6. Rankings remain secondary and never replace an OpenAlex headline figure.
7. Any post-result new figure must be labeled exploratory unless it only
   visualizes an already-frozen analysis.
