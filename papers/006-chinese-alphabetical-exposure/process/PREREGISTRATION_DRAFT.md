# ARIS4C006 · Preregistration draft

**State:** research-design draft; confirmatory outcomes remain locked.

Last updated: 2026-09-19

## 1. Working title

**Alphabetical Exposure and Scholarly Credit in China's Research System**

## 2. Primary question

Within the mainland-China scholarly system, does an author's relative alphabetical family-name position become more predictive of their listed byline position when the publication environment has a stronger independently measured prior convention of alphabetical authorship?

The study is about an institutional credit-allocation mechanism, not a psychological name-letter preference and not intrinsic ability.

## 3. Population language

The study never infers nationality, ethnicity, citizenship, or birthplace from a name.

A focal primary row is a **CN-affiliated authorship with a high-confidence ChineseNames-mappable surname form**.

A work enters the primary within-work mechanism frame only when:
1. it is an eligible primary work type;
2. all listed authors have sufficiently reliable family-name ordering keys;
3. at least 2 focal CN-affiliated ChineseNames-mappable authorships remain;
4. the work has an eligible OpenAlex primary-topic field;
5. the focal rows have valid frozen LOAO exposure.

Full rule: `POPULATION_FRAME.md`.

## 4. Time window

Primary focal work window:

**2011–2025**

selected prospectively from the measurement-only annual coverage sweep.

2010 failed the predeclared DOI threshold; every year 2011–2025 passed the frozen annual rule.

The incomplete year 2026 is excluded from outcome analysis.

## 5. Disciplinary scope

Field assignment:

`primary_topic.field.id`

not `topics.field.id`.

All **26 current OpenAlex fields** passed the prospectively frozen all-field feasibility gate and are globally eligible.

A particular focal observation still requires sufficient LOAO field-window information.

## 5A. Primary field-year sampling design

The primary work-level mechanism is **not a publication-volume census**.

Frozen strata:

**26 primary-topic fields × 15 focal years (2011–2025) = 390 field-year cells.**

Per field-year:
- reproducible deterministic OpenAlex random blocks;
- target **40 informative eligible works**;
- maximum 5 random blocks;
- retain 20–39 if target is not reached;
- exclude the cell if <20 informative works remain after 5 blocks.

Target full frame:
- 15,600 informative work clusters;
- at least 31,200 focal authorship rows.

The primary estimand is therefore approximately **field-year balanced**: the average within-work alphabetical-order mechanism across eligible field-year contexts, not the publication-volume-weighted average paper in China.

A publication-volume-weighted specification may be reported only as a secondary sensitivity and cannot replace the primary because it is larger or more significant.

Full rule: `PRIMARY_FRAME_SAMPLING_RULE.md`.

## 6. Primary work types

Primary:
- `article`
- `conference-paper`

Secondary sensitivity only:
- `review`
- `data-paper`
- `software-paper`

All other OpenAlex work types are excluded from the primary frame.

Convention exposure is estimated from the same primary work-type set.

## 7. Surname evidence

Frozen primary mapping version:

`aris4c006-surname-map-v2-ccnc`

Pronunciation/order authority:
- pinned CCNC Romanized Chinese Last Names Dictionary, commit `a14520b9cc8bd6b251aeb4a7453ab1a45f23aa15`.

Population authority:
- ChineseNames 2025.8 population counts.

Allowed focal routes:

### Tier 1A — direct Han
- validated Han surname;
- compound surnames matched before single surnames;
- exact Han surname occurs in ChineseNames;
- exact Han surname also occurs in the pinned CCNC surname lexicon;
- CCNC supplies the surname-specific canonical Pinyin ordering key.

### Tier 1B — Crossref structured family + exact canonical surname Pinyin
- DOI resolves to Crossref;
- OpenAlex/Crossref author lists pass positional reconciliation;
- structured `family` exists;
- structured family agrees with OpenAlex name evidence;
- normalized family exactly matches a frozen CCNC canonical surname form in the ChineseNames × CCNC intersection;
- no conflicting ORCID/canonical-author evidence.

Unreviewed legacy/regional aliases are excluded from the primary sample.

Tier-3 first-token/last-token heuristics are forbidden.

Pilot 15:
- ChineseNames rows: 1,806;
- direct ChineseNames × CCNC Han intersection: 1,166 rows;
- represented ChineseNames population: **99.9671%**;
- 2024 all-field exact bibliographic mapping coverage: **96.05%**;
- 31 surname-specific initial disagreements with legacy ChineseNames initials, representing **0.4383%** of population mass.

Generic pypinyin is engineering QA only and is not confirmatory pronunciation authority.

## 8. Chinese population calibration

Primary denominator:

**ChineseNames population counts × pinned CCNC surname-specific pronunciation map**, restricted to their direct Han-surname intersection and renormalized over mapped population mass.

Pilot 17:
- mapped population: **1,181,331,391**
- mapped share of ChineseNames population: **99.9671%**
- excluded rare-name population mass: **0.0329%**
- corrected population-weighted initial rank: **16.25491**
- legacy rank on the same rows: **16.21065**

Uniform `1/26` A–Z expectations are forbidden.

The corrected A–Z shares from `PILOT17_RESULTS.md` are the confirmatory population calibration, subject to final byte-for-byte/value reproduction from the pinned ChineseNames 2025.8 R package.

For direct-Han records:
- exact ChineseNames population frequency may be retained;
- alphabetic initial/rank comes from pinned CCNC surname-specific Pinyin.

For Romanized records:
- when multiple Han surnames share one Romanized form, population counts are summed over all compatible ChineseNames × CCNC surnames;
- a specific Han surname is not imputed unless independently observed.

Population calibration is descriptive/contextual and does not make surname rank randomized.

## 9. Work-level ordering variables

For a work `w` with `n_w >= 2`:

### Listed position

`ListedPositionNorm_iw = (listed_position_iw - 1)/(n_w - 1)`

- 0 = first listed
- 1 = last listed

### Relative alphabetical position

`RelAlphaRank_iw`

is the midrank-normalized ordering position of focal author's family name among the **entire actual author list**, including non-focal coauthors.

- 0 = alphabetically earliest
- 1 = alphabetically latest

It is derived without using the actual listed position.

## 10. Convention exposure

For eligible convention work `w`:

- `I_alpha_w = 1` when validated family-name keys are lexicographically non-decreasing.
- with team size `n` and surname tie groups `m_j`:

`p_chance_w = prod_j(m_j!)/n!`

Field-window evidence:

`N_ct = sum_w(I_alpha_w - p_chance_w)`

`D_ct = sum_w(1 - p_chance_w)`

Primary context:

**OpenAlex primary-topic field × prior 3 complete publication years**

Raw source/journal-level exposure is not primary because the prospectively frozen split-half rank-reliability gate failed.

## 11. Anti-leakage exposure

Primary moderator uses exact leave-one-author-out exposure.

For focal canonical author `i`:

`LOAOExposure_ict = (N_ct - N_ict)/(D_ct - D_ict)`

where `N_ict,D_ict` are contributions from lag-window convention works containing author `i`.

Each work contributes at most once to an author's subtraction.

Require:

`D_ct - D_ict >= 50`

Otherwise the focal row is excluded from the primary model for that context/year.

Full rule: `LOAO_EXPOSURE_RULE.md`.

Mandatory robustness:
- convention exposure re-estimated using 3+ author works only.

## 12. Primary hypothesis and model

### H1

Within the same work, later `RelAlphaRank` predicts later listed position more strongly as prior LOAO field alphabetization exposure increases.

Model:

`ListedPositionNorm_iw = WorkFE_w + beta1 RelAlphaRank_iw + beta2(RelAlphaRank_iw × LOAOExposure_ict) + error_iw`

Primary estimand:

`beta2`

The preregistered directional expectation is positive, but formal testing is two-sided.

Work fixed effects absorb all work-shared factors, including journal/source, topic, date, team size, and shared work quality.

## 13. Secondary confirmatory family

Exactly two secondary confirmatory estimands are retained.

### Secondary 1 — first-listed authorship

`FirstListed_iw = 1` if focal author is listed first.

Use a linear-probability work-FE model with the same:
- `RelAlphaRank`;
- LOAO exposure;
- interaction;
- primary work frame;
- clustering structure.

The interaction is the secondary-1 estimand.

### Secondary 2 — observed five-year publication persistence

Longitudinal cohort:
- entry years 2014–2020;
- 3-year clean lookback;
- 5-year fixed follow-up;
- entry is first observed eligible article/conference-paper and includes >=1 CN-affiliated authorship in entry year.

Endpoint:

`Persistence5_i = 1`

when the canonical author has >=1 eligible article/conference-paper in `e+4` or `e+5`.

It measures observed bibliographic persistence, not true employment retention or academic exit.

Early exposure:
- mean LOAO primary-field exposure across eligible article/conference-paper works in `e ... e+2` on which the focal author's own authorship is CN-affiliated;
- require >=2 such exposure-defined CN-affiliated early works.

Stable surname vulnerability:

`InitialRankNorm_i = (InitialRank_i - 1)/25`

Model:

`logit(Persistence5_i) = alpha + beta1 InitialRankNorm_i + beta2 MeanEarlyExposure_i + beta3(InitialRankNorm_i × MeanEarlyExposure_i) + EntryYearFE + EntryPrimaryFieldFE + log1p(EntryWorkCount_i)`

Secondary-2 estimand:
- `beta3`.

H3 inference:
- two-sided test;
- cluster-robust covariance by `EntryPrimaryField × EntryYear`;
- H3 raw p-value enters the frozen Holm-adjusted secondary family jointly with H2.

### Frozen H3 sampling frame

H3 is nested inside the already frozen field-year-balanced primary work frame.

Candidate seed authors are unique canonical authors who appear as focal rows in
the primary frame during 2014–2020.

A candidate is retained only when full-history reconstruction verifies that:
- their first observed eligible article/conference-paper year is `e` in 2014–2020;
- they have at least one primary-frame focal row in that same entry year `e`;
- an eligible entry-year work contains a CN-affiliated authorship;
- the 3-year clean lookback and frozen identity rules pass.

Authors sampled only after their true entry year are excluded, preventing later
survival from becoming a route into the confirmatory H3 cohort.

There is no second-stage outcome-dependent author sampling: all validated
entrants are retained subject to frozen exclusions.

Before H3 may run, the outcome-blind cohort build must contain:
- >=1,000 validated entry authors before the early-exposure requirement;
- >=750 authors after all frozen H3 focal-variable requirements;
- all 7 entry years;
- >=20 of 26 entry primary fields;
- >=100 ORCID-anchored authors;
- >=500 low-identity-risk authors.

If these structural thresholds fail, H3 is removed from the confirmatory family
rather than changing the sampling rule after persistence is observed.

Full rule: `LONGITUDINAL_SAMPLING_RULE.md`.

This is interpreted associationally/mechanistically.

## 14. Structural supportive model

A work-level model using stable Chinese surname initial rank × exposure is supportive, not confirmatory:

`ListedPositionNorm ~ InitialRankNorm × LOAOExposure + prespecified FE/controls`

It cannot replace H1 merely because it produces a stronger result.

## 15. Inference

Primary standard errors use three-way cluster-robust covariance:

1. canonical OpenAlex author ID;
2. OpenAlex work ID;
3. primary-topic field × focal publication year.

Primary:
- two-sided alpha = 0.05;
- 95% CI;
- exactly one primary estimand;
- no multiplicity correction for the single primary test.

Secondary confirmatory family:
- exactly two estimands;
- Holm familywise correction at alpha 0.05.

Full rule: `INFERENCE_RULE.md`.

## 16. Identity resolution

Before author-level joins:
1. preserve raw embedded OpenAlex author ID;
2. resolve it through the current OpenAlex author endpoint;
3. use returned canonical OpenAlex author ID for longitudinal joins;
4. when ORCID exists, require consistency;
5. raw-name-only person merges are forbidden.

Pilot:
- 61/977 raw ID mismatches;
- 61/61 repaired by canonicalization;
- 0 unresolved conflicts in the deterministic validation sample.

Residual non-ORCID split/merge risk is handled through mandatory sensitivity subsets, not declared eliminated.

## 17. Longitudinal cohort identity and survivor rules

The 2024 feasibility seed is never a confirmatory cohort.

Entry cohort is constructed prospectively from first observed eligible publication.

Primary longitudinal analysis excludes:
- canonicalization failures;
- known ORCID conflicts;
- unresolved surname-form mapping;
- authors lacking >=2 early exposure-defined works.

Mandatory sensitivity:
- ORCID-linked subset;
- uncommon-name / low-collision-risk subset;
- direct-Han subset;
- removal of implausible publication/affiliation histories;
- surname-frequency strata.

## 18. Confirmatory robustness and falsification

Mandatory for H1:
- 3+ total-author focal works;
- 3+ author convention-estimation exposure;
- Tier 1 surname evidence only;
- low-identity-risk subset;
- low-alphabetization field-years;
- future-exposure placebo;
- shuffled/permuted surname ordering key preserving team structure.

Where sufficiently powered:
- works with >=3 focal CN-affiliated ChineseNames-mappable authorships.

The institutional mechanism is weakened if:
- interaction persists equally in low-exposure contexts;
- future exposure predicts earlier position;
- permutation produces comparable estimates;
- result exists only under two-author convention evidence.

## 19. Missingness

Primary H1/H2:
- no imputation of family name, focal surname map, author order, field, or exposure;
- primary model is complete-case under the frozen structural eligibility rules;
- work FE means there are no optional work-level nuisance controls to impute.

Longitudinal H3:
- no surname, exposure, author-ID, entry-year, or primary-field imputation;
- excluded counts reported by entry year and field;
- optional descriptive variables do not determine confirmatory inclusion.

## 20. Confirmatory vs exploratory boundary

Confirmatory:
1. H1 normalized listed position;
2. Secondary 1 first-listed probability;
3. Secondary 2 observed five-year publication persistence.

Exploratory:
- citations and normalized citation impact;
- h-index/cumulative metrics;
- corresponding-author status;
- prestige transitions;
- mobility/affiliation transitions;
- elite lists;
- raw source/journal-level exposure;
- nonlinear surname rank;
- individual surnames;
- domestic/international subgrouping beyond frozen robustness;
- variant-expanded surname dictionary;
- given-name features;
- gender/name-valence/name-uniqueness analyses.

Exploratory results cannot replace a failed H1.

## 21. Interpretation boundary

Evidence consistent with the proposed institutional mechanism requires:
- H1 in the preregistered direction;
- stronger surname-position coupling under higher measured prior alphabetization exposure;
- falsification checks behaving appropriately.

The study does not establish:
- surname letters cause ability, intelligence, or personality;
- surname rank is randomized in China;
- CN affiliation means Chinese nationality or ethnicity;
- bibliographic non-persistence equals true academic exit;
- a distal career association is causal without additional assumptions.

## 22. Remaining pre-registration execution gates

No focal surname × outcome estimate may be opened until all are complete:

- [x] reproduce the ChineseNames baseline from the pinned 2025.8 R package, not only the engineering mirror (Pilot 18 PASS);
- [ ] materialize the final primary-field convention/exposure build under article+conference-paper types;
- [x] validate the LOAO implementation against hand/synthetic checks (PASS);
- [x] run a synthetic-only model smoke test for work FE + interaction + frozen multiway clustering (PASS);
- [ ] materialize the primary work frame and report sample/cluster counts **without calculating H1/H2 coefficients**;
- [x] finalize deterministic identity-risk QA flags for the longitudinal secondary and report only their prevalence (120/120 hard-QA pass; no persistence/effect opened);
After all outcome-blind execution checks above pass, generate the deterministic preregistration lock/hash with `code/27_prereg_lock.py --lock`. The existence and SHA-256 content of `PREREGISTRATION_LOCK.json`—not a checkbox in this locked document—records completion. Confirmatory unlock remains a separate later repository change.

Until then, the locked design snapshot retains:

`confirmatory_outcomes_unlocked = false`.

After the preregistration lock is committed, confirmatory execution is enabled
only through a separate `process/CONFIRMATORY_UNLOCK.json` whose lock label
and SHA-256 match the committed preregistration lock. The hashed design files
are not edited merely to unlock analysis. Full rule: `UNLOCK_PROTOCOL.md`.
