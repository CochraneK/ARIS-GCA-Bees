# ARIS4C006 · Author identity-resolution audit

Last updated: 2026-09-18

## Why this is a first-class validity problem

Chinese bibliographic names are unusually vulnerable to homonymy and name-order variation. OpenAlex resolves raw authorships into person-level author IDs algorithmically, but its own documentation recognizes two failure modes: one person split across multiple profiles and multiple people merged into one profile.

For ARIS4C006, this error can be **differential** because common surnames/name strings are not uniformly distributed across Pinyin initials. A merge can inflate publications, citations, career length, affiliations, and mobility; a split can attenuate them. This can mimic a surname-effect signal.

Relevant methodological anchor:
- Xu, S. B., & Hu, G. (2025; online 2024). *Rethinking the author name ambiguity problem and beyond: The case of the Chinese context*. Accountability in Research, 32(6), 913–936. DOI: `10.1080/08989621.2024.2349115`.

## 1. Audit variables per OpenAlex author

Construct an `identity_risk` table containing:

- OpenAlex author ID;
- ORCID present/absent;
- number of raw author-name variants;
- number of distinct Romanized family-name candidates;
- number of works;
- active publication years;
- maximum papers/year;
- number of distinct institutions/year;
- number of countries/year;
- impossible/implausible geographic overlaps;
- field entropy / abrupt field switching;
- raw-affiliation consistency;
- coauthor-network continuity;
- surname population frequency;
- full-name estimated frequency where available;
- parser tier/confidence;
- candidate merge-risk score;
- candidate split-risk evidence.

## 2. Merge-risk diagnostics

Flag profiles with combinations such as:

- implausibly high papers/year;
- simultaneous unrelated institutions/countries;
- disconnected coauthor communities with little temporal/affiliation overlap;
- incompatible raw-name variants;
- abrupt unrelated field clusters;
- multiple ORCID-like identity signals where detectable.

A single flag is not proof of a merge. Use a transparent rule/score and validate samples.

## 3. Split-risk diagnostics

Search for near-duplicate author profiles sharing:

- same or near-identical name variants;
- overlapping/coherent affiliations;
- strongly overlapping coauthor networks;
- sequential non-overlapping publication periods;
- same ORCID or other external identifier where available.

Do not automatically merge records in the analysis dataset. Maintain candidate pairs/clusters and perform sensitivity analyses.

## 4. Outcome-blinded validation

Identity audit thresholds must be selected without observing the focal `surname rank × alphabetization exposure` career-effect estimates.

Validate a stratified sample by:
- surname-frequency decile;
- early/middle/late alphabet position;
- ORCID status;
- publication-volume decile;
- domestic-only vs internationally mobile affiliation history;
- field.

## 5. Differential-error regressions

Treat quality indicators as outcomes:

`MergeRisk ~ InitialRank + SurnameFrequency + Field + CareerAge + Year`

`SplitRisk ~ InitialRank + SurnameFrequency + Field + CareerAge + Year`

`ORCID_present ~ InitialRank + SurnameFrequency + Field + Year`

`RawNameVariantCount ~ InitialRank + SurnameFrequency + Field + Mobility`

These are diagnostic, not substantive surname-effect results.

## 6. Confirmatory sensitivity ladder

Run the frozen substantive model on nested samples:

1. all high-confidence surname parses passing base identity rules;
2. remove top identity-risk tail (`threshold TBF` outcome-blind);
3. ORCID-linked authors only, if powered;
4. uncommon full-name strings;
5. stable coauthor-network/institution-history subset;
6. Tier-1 surname parses only.

A result existing only in high-risk/common-name records is treated as evidence against the substantive interpretation.

## 7. Negative-control signal

If surname rank predicts obviously implausible data-quality outcomes—e.g. simultaneous country count or extreme papers/year—this indicates measurement structure correlated with the focal predictor.

Such relationships must be reported before career-effect interpretation.

## 8. Name-order variation

Preserve all raw strings because international publication may convert a Chinese family-first name into Western given-first order. Name-order changes across venues can be informative for parsing but also correlate with internationalization, which itself predicts career outcomes.

Therefore:
- name-format variables may inform parser confidence;
- they should not be treated as innocuous controls without a causal rationale;
- internationalization-stratified parser accuracy is mandatory.

## 9. ORCID role

ORCID is useful as a higher-confidence identity anchor, not a gold-standard random subset. ORCID adoption is incomplete and selected by field, cohort, institution, and internationalization.

Use ORCID for:
- validation/corroboration;
- a robustness subset;
- potential resolution of candidate split profiles.

Do not generalize ORCID-only effect sizes to all scholars without qualification.

## 10. Stop rule

The author-level career analysis is blocked if identity-risk indicators remain substantially associated with surname rank/frequency and no high-confidence subset demonstrates that the focal pattern is robust to those errors.

In that case, ARIS4C006 can still narrow to work-level authorship-order mechanisms, which depend less on long-horizon person-level career reconstruction.
