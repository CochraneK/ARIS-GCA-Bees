# ARIS4C006 · Adversarial auto-review

Last updated: 2026-09-18

## Overall verdict

**CONDITIONAL GO — methodologically interesting only if the paper is about measured institutional alphabetization exposure, not a generic surname-success correlation.**

A naive version of this study should be rejected as insufficiently novel and vulnerable to severe measurement bias. The upgraded design can be valuable, but its hardest problems are surname parsing, bibliometric person resolution, and endogenous exposure.

## Reviewer 1 — “This has already been done”

### Objection

The literature already contains:
- alphabetical discrimination in economics (Einav & Yariv, 2006);
- a Chinese identification design with economists vs physicists/statisticians and China/US placement (Li & Yi, 2021);
- multi-field authorship-convention analyses (Öz, 2024);
- a 2026 global top-scientist analysis using expected national surname distributions (D'Angelo, 2026).

Therefore a paper showing `surname initial -> citations/success in China` would add little.

### Resolution

Keep the project only if it implements **continuous, observed, time-varying institutional exposure** and longitudinal mechanism tests at scale.

The paper's novelty statement must be phrased narrowly:

> We estimate whether the association between surname alphabetical position and scholarly outcomes scales with independently estimated local author-order conventions within the China-based scholarly system, using a population-calibrated Chinese surname baseline and longitudinal exposure histories.

### Gate

**Resolved conditionally.** Closest-prior-work sweep remains mandatory before preregistration.

---

## Reviewer 2 — “Your surname variable is wrong”

### Objection

OpenAlex does not guarantee a clean family-name field for every record. Chinese names may be written `Wang Wei` or `Wei Wang`; Romanizations vary; compound and polyphonic surnames exist. A final-token parser can systematically misclassify the focal exposure.

If error differs by international mobility or field, it can create exactly the desired interaction.

### Resolution

- define parser tiers;
- use Chinese-character raw names when possible;
- build surname-specific Romanization exceptions;
- corroborate Romanized family-name positions using repeated raw variants/ORCID/structured sources;
- validate a stratified sample before inspecting focal outcomes;
- exclude heuristic-only Tier 3 from confirmatory inference;
- report parser coverage and precision by field, surname frequency, mobility, and year.

### Gate

**OPEN / CRITICAL.** Failure to obtain high precision collapses the confirmatory design.

---

## Reviewer 3 — “OpenAlex common-name disambiguation manufactures the effect”

### Objection

Chinese scholars with common surnames/given names are unusually difficult to disambiguate. False merges inflate publication counts/citations; false splits truncate careers. Because name commonness correlates with surname frequency, bibliometric identity error may correlate with the focal predictor.

### Resolution

Mandatory sensitivity analyses:
- ORCID-linked subset;
- uncommon-full-name subset;
- surname-frequency strata;
- implausible simultaneous-affiliation/publication filters;
- within-author raw-name-variant diagnostics;
- outcome comparisons by disambiguation-risk score.

No surname-frequency effect is interpretable unless identity-resolution error is bounded.

### Gate

**OPEN / CRITICAL.** Must be passed before distal career outcomes.

---

## Reviewer 4 — “Alphabetical papers happen by chance”

### Objection

For two distinct authors, alphabetical order occurs with probability 1/2 under random contribution ordering. Labeling every alphabetically ordered two-author paper as evidence of a convention grossly overstates exposure.

### Resolution

Estimate excess alphabetization relative to exact team-size-specific random-order probability. For repeated surnames, compute the number of distinguishable permutations. Use 3+ author teams as a core robustness analysis and shrink small context cells.

### Gate

**RESOLVED IN DESIGN.** Must be correctly implemented.

---

## Reviewer 5 — “Your moderator is endogenous”

### Objection

Scholars choose fields, journals, collaborators, countries, and teams. Later-surname scholars may strategically avoid alphabetical environments. Then `SurnameRank × AlphaExposure` can reflect selection, not treatment by a convention.

### Resolution

Do not oversell causal identification. Strengthen using:
- lagged/cross-fitted exposure estimated from other works;
- field × year fixed effects;
- within-author changes in convention exposure;
- independently identified journal convention changes where available;
- pre-period outcomes;
- explicit tests for selective journal/coauthor choice as a mechanism/outcome rather than simply controlling it away.

### Gate

**PARTIALLY RESOLVED.** Default language is associational/mechanistic unless stronger natural variation is found.

---

## Reviewer 6 — “Surname rank is not randomized in China”

### Objection

Chinese surnames have geographic, historical, clan, migration, and potentially socioeconomic structure. Pinyin initial is mechanically derived from surname, so an A-vs-Z contrast is not a randomized lottery.

### Resolution

- never state that surname initial is random;
- population-calibrate descriptions;
- include surname frequency/uniqueness and appropriate institution/geography controls;
- exploit interaction with author-order exposure rather than raw rank alone;
- use low-alphabetization contexts as falsification;
- where data permit, compare within narrower institutional/field/cohort contexts.

### Gate

**RESOLVED AS INTERPRETATION LIMITATION**, not eliminated as confounding.

---

## Reviewer 7 — “China-based is not Chinese”

### Objection

CN affiliation does not identify nationality or ethnicity. Name-based inclusion also cannot ethically/scientifically establish identity.

### Resolution

Primary population is the **mainland-China scholarly system / China-affiliated authorships**, not “all Chinese people.” The surname is used as a bibliographic attribute, not as proof of ethnicity/citizenship.

### Gate

**RESOLVED.** Wording must remain disciplined.

---

## Reviewer 8 — “Your outcome is mechanically contaminated by author order”

### Objection

If the outcome is first-author position and the exposure is estimated from the same paper's author order, the result is tautological. Similar leakage can occur if context exposure includes the focal author/paper.

### Resolution

- leave-one-paper/author out;
- lag convention exposure;
- cross-fit contexts;
- separate mechanism-proximal outcomes from distal career outcomes;
- never use the focal outcome to tune the exposure estimator.

### Gate

**RESOLVED IN DESIGN.** Cross-fitting/lags are mandatory.

---

## Reviewer 9 — “Citations may simply not respond”

### Objection

Large-scale economics evidence reports little general citation advantage for alphabetized coauthorship after controls. A strong citation hypothesis may be unsupported.

### Resolution

Do not make citation impact the only or primary mechanism endpoint. Headline tests should first address listed position, visibility-related mechanisms, collaboration, convention exposure, and then downstream outcomes.

A null citation result is informative and does not invalidate the institutional-order analysis.

### Gate

**RESOLVED.** Outcome hierarchy revised.

---

## Reviewer 10 — “Population baseline mismatch”

### Objection

ChineseNames is based on a 1930–2008 household-registration population, while active scholars in 2010–2025 are age-selected and educationally selected. Even a nationwide population denominator is not the exact counterfactual surname distribution of potential academics.

### Resolution

Treat ChineseNames as a **population calibration**, not a perfect scholar-risk-set denominator. Validate against newer aggregate Ministry of Public Security surname reports and report sensitivity using:
- cohort-relevant surname subsets if obtainable;
- observed low-exposure-field surname distribution as an alternative empirical benchmark;
- institution/field/cohort conditioning.

### Gate

**RESOLVED AS LIMITATION / ROBUSTNESS REQUIREMENT.** Do not interpret population over-representation as career causation.

---

## Reviewer 11 — “You are doing too much”

### Objection

The design risks becoming an uncontrolled fishing expedition across fields, journals, citations, mobility, prestige, collaboration, and elite lists.

### Resolution

Freeze a hierarchy:
1. convention measurement;
2. 2–4 mechanism-proximal outcomes;
3. a small number of longitudinal distal outcomes;
4. exploratory extensions clearly separated.

Use a multiplicity plan and pre-register the primary interaction.

### Gate

**RESOLVED IN PLAN.** Final preregistration must narrow the endpoint set.

---

## Failure modes that should stop or radically narrow the paper

1. High-confidence surname parsing cannot reach acceptable accuracy/coverage.
2. OpenAlex identity-resolution error remains strongly associated with surname position after restrictions.
3. Measured alphabetization exposure shows little meaningful variation across contexts.
4. A closer prior study is found that already combines Chinese population calibration, measured continuous convention exposure, and longitudinal cross-field careers.
5. Results exist only under heuristic name parsing or only in two-author teams.
6. The interaction does not attenuate in negative-control contexts.

## Claims allowed if the design succeeds

Potentially defensible:
- local author-order conventions modify the relationship between surname position and authorship visibility;
- institutional exposure may accumulate into some downstream bibliometric/career differences;
- Chinese surname population non-uniformity materially changes naive A–Z comparisons.

Not defensible from this design alone:
- surname letters cause intelligence or scientific ability;
- later-surname scholars are intrinsically disadvantaged in all life domains;
- China-wide nationality/ethnicity effects inferred from affiliation/name data;
- a causal career effect without additional assumptions/design evidence;
- a psychological name-letter mechanism.

## Final recommendation

**Proceed to validated surname-parser + OpenAlex convention pilot. Do not yet run confirmatory career-outcome models.**
