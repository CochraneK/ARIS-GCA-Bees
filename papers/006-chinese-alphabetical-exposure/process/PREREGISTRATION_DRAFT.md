# ARIS4C006 · Preregistration draft

**State:** draft before data-feasibility gates are passed. Items marked `TBF` must be frozen before confirmatory outcomes are opened.

Last updated: 2026-09-18

## 1. Study title

**Alphabetical Exposure and Academic Careers in Chinese Science**

## 2. Primary question

Among scholars participating in the mainland-China scholarly system, is later Pinyin surname position associated with less favorable authorship visibility specifically under greater **independently measured exposure to alphabetical author-order conventions**?

## 3. Primary hypothesis

`H1` (primary mechanism): within the same multi-author work, an author's **relative alphabetical family-name rank within the actual coauthor team** more strongly predicts later normalized listed position when the publication context has higher independently measured prior alphabetization exposure.

Primary interaction: `RelAlphaRank_iw × PriorAlphabetizationExposure_c,t-1`.

The work fixed-effect design is primary because it compares authors inside the same paper and therefore absorbs all work-level topic, journal, year, and team-wide factors. The stable population-scale `SurnameInitialRank × Exposure` interaction is retained as a secondary structural-vulnerability specification, not the sole headline test.

## 4. Secondary hypotheses

Subject to pilot feasibility, no more than three will remain confirmatory:

- `H2`: the stable Chinese surname-initial rank × prior exposure interaction predicts normalized listed position in the same qualitative direction as the within-team mechanism model.
- `H3`: higher accumulated structural/realized alphabetical burden predicts lower subsequent field/year-normalized citation impact, conditional on the final identity and cohort gates.
- `H4`: higher accumulated alphabetical burden predicts one frozen distal career endpoint (`TBF`: observed 5-year publication persistence, institutional-stratum transition, or affiliation transition; choose from coverage/measurement diagnostics before focal effects are viewed).

Corresponding-author outcomes are confirmatory only if coverage is sufficient under a pre-specified missingness threshold (`TBF`).

## 5. Population

Primary frame: OpenAlex authorships with at least one resolved mainland-China (`CN`) institutional affiliation.

Author-year analyses require a frozen rule for classifying a scholar as China-based in year `t` (`TBF` after coverage pilot).

No nationality, ethnicity, citizenship, or birthplace is inferred from a name.

## 6. Time window

Candidate confirmatory window: 2010–2025.

Final start/end years are `TBF` after inspecting **coverage only**, without inspecting surname-effect estimates or focal career outcomes. Reasons for changes must be documented.

## 7. Inclusion criteria

A confirmatory authorship/work must:

1. meet the frozen publication-type rule (`TBF`);
2. contain >=2 authors for author-order outcomes;
3. contain sufficient surname evidence for all authors needed to classify alphabetization under the validated parser;
4. have the focal China-affiliated authorship defined by resolved institution/country metadata;
5. fall in the frozen time window;
6. have a field/topic and source/context assignment sufficient for exposure construction.

Confirmatory author-year records must additionally satisfy the frozen identity-consistency and career-observation rules.

## 8. Exclusion criteria

Exclude from confirmatory inference:

- Tier-3 heuristic-only surname parses;
- ambiguous family-name assignments;
- records with unresolved duplicate/merge/split red flags above the frozen threshold;
- contexts lacking minimum data for stable convention estimates;
- works whose author ordering cannot be reconstructed reliably;
- records failing temporal ordering of exposure and outcome.

Exact thresholds are `TBF` from outcome-blinded feasibility diagnostics.

## 9. Surname exposure

Primary predictor:

`SurnameInitialRank = 1..26`

using the validated family name's Pinyin initial.

Population attributes from ChineseNames 2025.8:
- initial/rank;
- surname population count/ppm where exact surname identified;
- surname uniqueness;
- compound-surname flag.

Uniform `1/26` expected surname probabilities are prohibited.

## 10. Alphabetization convention exposure

For eligible multi-author works in context `c,t`, define:

- `I_alpha = 1` if validated surname ordering is lexicographically non-decreasing;
- `p_chance` = exact random-order probability given team size and surname ties.

Context-level raw excess:

`ExcessAlpha_ct = (mean(I_alpha) - mean(p_chance)) / (1 - mean(p_chance))`

Final exposure estimator may use hierarchical shrinkage or minimum cells (`TBF`), but must be frozen from convention data only.

### Anti-leakage rule

A focal work/author cannot materially define its own exposure.

Primary approach `TBF` from:
- leave-one-author-out;
- lagged context exposure;
- K-fold cross-fitting by author/work.

Whichever is selected becomes immutable for the confirmatory run.

## 11. Primary outcome

Primary mechanism outcome:

`ListedPositionNorm_iw = (listed_position_iw - 1) / (team_size_w - 1)`

for collaborative works with `team_size >= 2`, so 0 = first listed and 1 = last listed.

Primary work-specific predictor:

`RelAlphaRank_iw`, the midrank-normalized family-name position among the actual coauthors, scaled 0 = alphabetically earliest and 1 = latest.

A binary first-listed outcome is secondary. The 3+ author subset is a mandatory robustness analysis.

## 12. Primary model

Primary work-level mechanism model:

`ListedPositionNorm_iw = WorkFE_w + β1 RelAlphaRank_iw + β2(RelAlphaRank_iw × PriorExposure_c,t-1) + ε_iw`

Primary estimand: `β2`.

Because the focal context exposure is shared within a work, its main effect is absorbed by `WorkFE_w`. Work fixed effects also absorb work-level journal, topic, publication date, team size, and shared quality/context factors.

Secondary structural-vulnerability model:

`ListedPositionNorm_iw = β0 + β1 InitialRank_i + β2 PriorExposure_c,t-1 + β3(InitialRank_i × PriorExposure_c,t-1) + controls + FE + ε_iw`

The structural model is not allowed to supersede the within-work mechanism model merely because its estimate is larger.

Inference must account for repeated authors and shared works. The exact multiway-clustering implementation remains `TBF` until the repeated-measure structure of the frozen frame is summarized, but author clustering is mandatory and work dependence cannot be ignored.

## 13. Author-year downstream model

Generic:

`Y_it = β0 + β1 Rank_i + β2 PriorExposure_i,t-1 + β3 Rank_i×PriorExposure_i,t-1 + PriorY + FE + ε`

Primary distal interpretation is associational unless a separately defended quasi-experimental design is identified.

## 14. Population calibration analysis

Before focal models, report:

`ObservedInitialShare / ChineseNamesExpectedInitialShare`

for A–Z initials with uncertainty intervals.

This serves as sample/data quality context. It is not a causal estimate of academic selection.

Alternative empirical denominator for robustness: surname-initial distribution in preregistered low-alphabetization contexts within the same scholarly system, if sufficiently large and stable.

## 15. Confirmatory negative controls

At minimum:

1. low-alphabetization contexts;
2. single-authored work outcomes for which coauthor order cannot operate (where outcome definition permits);
3. future exposure predicting prior outcomes;
4. randomized/shuffled surname rank preserving empirical distribution;
5. 3+ author teams separately from two-author teams.

## 16. Identity/parser robustness

Mandatory analyses:

- Tier 1 only;
- Tier 1 + validated Tier 2;
- ORCID-linked subset where large enough;
- uncommon full-name subset;
- surname-frequency strata;
- exclude identity records with implausible career/publication patterns.

Parser error must be checked for monotonic association with surname rank in the blinded validation sample.

## 17. Multiplicity

The final confirmatory set will contain:
- 1 primary interaction outcome/model;
- <=3 secondary confirmatory outcomes.

`TBF`: Holm correction across the confirmatory family or a clearly ordered gatekeeping procedure. Exploratory outcomes will be labeled and not folded into a single confirmatory claim.

## 18. Missing data

- no surname imputation for ambiguous names;
- no corresponding-author imputation when absent;
- affiliation-country missingness reported by field/year;
- missing field/context records excluded only under frozen rules;
- complete-case vs missing-indicator strategies for non-focal controls specified before confirmatory run.

## 19. Stopping / pivot rules

Before confirmatory outcomes, stop or narrow if:

1. included surname initial precision fails the frozen threshold;
2. parser error is materially differential by surname rank and cannot be bounded;
3. author disambiguation risk remains strongly rank/frequency dependent;
4. convention exposure lacks meaningful stable variation;
5. closest-prior-work search identifies a study already implementing the same core exposure architecture in China;
6. OpenAlex coverage is insufficient for the frozen outcome hierarchy.

Narrowing to Chinese-character-only records is preferred over lowering parser quality.

## 20. Confirmatory vs exploratory boundary

Confirmatory:
- frozen sample/window;
- frozen parser version;
- primary exposure interaction;
- <=4 total outcomes;
- frozen negative controls and robustness suite.

Exploratory:
- alternative field taxonomies;
- individual surnames;
- nonlinear alphabet rank;
- domestic-vs-international subgrouping not preregistered;
- elite lists;
- given-name variables;
- gender/name-valence/name-uniqueness extensions;
- alternative career endpoints not frozen above.

## 21. Interpretation rule

A significant `Rank × Exposure` interaction consistent across mechanism outcomes and exposure-gradient/negative-control tests is evidence **consistent with an institutional author-order mechanism**.

It is not by itself evidence that surname letters cause ability, intelligence, personality, or general life outcomes.

## 22. Items that must be frozen after feasibility but before outcomes

- [ ] final date window;
- [ ] publication types;
- [ ] China-based author-year definition;
- [ ] parser acceptance threshold/version;
- [ ] disambiguation-risk exclusion threshold;
- [ ] context definition and minimum cell size;
- [ ] shrinkage/cross-fitting exposure estimator;
- [ ] primary position normalization;
- [ ] one distal career endpoint;
- [ ] FE/cluster structure;
- [ ] multiplicity method;
- [ ] missing-control handling.

Until these boxes are frozen, the study remains pre-confirmatory.


## 23. Identity canonicalization rule

Before constructing any author-level history, every OpenAlex author ID embedded in a work authorship must be re-resolved through the current OpenAlex author endpoint.

Pilot evidence:
- 977 ORCID-verifiable authorships;
- 61 raw embedded-ID mismatches (6.24%);
- all 61/61 mismatches reconciled after canonical author resolution;
- 0 unresolved conflicts and 0 lookup failures in the deterministic pilot sample.

Therefore the longitudinal join key is the **current canonical OpenAlex author ID**, not the raw ID embedded in a historical work record.

When ORCID is present, ORCID consistency is checked as additional validation. Raw embedded IDs remain preserved for provenance.

This engineering fix does not eliminate residual split/merge error among non-ORCID authors; the preregistered identity-risk sensitivity ladder remains mandatory.
