# ARIS4C006 · Frozen publication / visualization plan

Last updated: 2026-09-19

This plan is result-neutral and was created before confirmatory H1/H2/H3 results were opened. It fixes the minimum publication package so figures are not selected only because they look favorable.

## Final bilingual outputs

Required final artifacts:

- English manuscript;
- Chinese manuscript;
- English publication PDF;
- Chinese publication PDF;
- reproducible figures and figure-data exports;
- machine-readable confirmatory result tables;
- methods / provenance appendix;
- public-safe GitHub Page entry linked to the PDFs.

Working paper title:

**Alphabetical Exposure and Scholarly Credit in China's Research System**

Chinese working title:

**字母排序暴露与中国科研体系中的署名信用分配**

## Main figures

### Figure 1 — Chinese surname alphabetic population landscape

Purpose:
- show why uniform A–Z is invalid.

Panels:
1. ChineseNames × CCNC population share by canonical surname initial;
2. cumulative population mass by alphabetical rank;
3. observed corrected population-weighted initial rank vs uniform-A–Z benchmark;
4. mapped vs excluded rare surname population mass.

This figure is descriptive and does not contain scientific-outcome effects.

### Figure 2 — Measured alphabetical-authorship regimes

Purpose:
- visualize the institutional moderator independently of surname outcomes.

Panels:
1. field × year heatmap of prior-3-year chance-corrected alphabetization exposure;
2. field-level distribution / ranking over time;
3. all-author vs 3+ author convention estimates;
4. information-support D distribution and unsupported cells.

Primary field assignment must use `primary_topic.field.id`.

### Figure 3 — Preregistered within-work mechanism

Purpose:
- visualize H1 without replacing the model.

After unlock:
- plot predicted normalized listed position against `RelAlphaRank`;
- display at prespecified low / median / high measured LOAO exposure values;
- include 95% CI from the frozen model;
- report beta2 and CI in caption.

Do not choose exposure cut points from effect-maximizing values.

### Figure 4 — Mechanism robustness / falsification dashboard

Predefined panels:
- primary H1;
- 3+ focal-work robustness;
- 3+ convention-exposure robustness;
- Tier-1 surname evidence;
- low-identity-risk subset where applicable;
- low-alphabetization contexts;
- future-exposure placebo;
- shuffled surname-order placebo.

Show coefficient + 95% CI using a common axis.

### Figure 5 — Secondary confirmatory results

Panels:
1. H2 first-listed interaction estimate;
2. H3 five-year observed publication persistence interaction, only if its frozen structural cohort gate passes;
3. Holm-adjusted secondary-family inference.

If H3 structural adequacy fails, panel 2 is explicitly marked “confirmatory H3 not estimable under preregistered adequacy rule”; it is not replaced with a different endpoint.

### Figure 6 — Design / provenance flow

A compact visual pipeline:

ChineseNames 2025.8
→ pinned CCNC surname pronunciation
→ OpenAlex primary-topic field / authorships
→ Crossref structured family names
→ canonical author IDs
→ chance-corrected field convention
→ LOAO exposure
→ balanced primary work frame
→ preregistration lock
→ H1/H2/H3

Include counts only from outcome-blind materialization or final reporting.

## Main tables

### Table 1 — Data sources and frozen operational definitions
ChineseNames, CCNC, OpenAlex, Crossref, population/frame definitions, date windows.

### Table 2 — Outcome-blind materialization quality
- 390 field-year cells;
- retained/excluded cells;
- works;
- focal rows;
- canonical authors;
- LOAO support;
- surname-map route;
- reconstruction exclusions.

### Table 3 — Confirmatory estimands
- H1 estimate, SE, CI, p;
- H2 estimate, SE, CI, raw p, Holm p;
- H3 estimate, SE, CI, raw p, Holm p if retained.

### Table 4 — Mandatory robustness and falsification
All prespecified checks, including null/placebo behavior.

## Supplementary figures

At minimum:

- S1 exact A–Z population shares;
- S2 surname-map coverage by field/year;
- S3 Crossref/OpenAlex positional reconciliation audit;
- S4 canonical author-ID reconciliation;
- S5 source-level split-half reliability that motivated field-level primary exposure;
- S6 field-specific convention trajectories;
- S7 cell sample-size distribution;
- S8 team-size distribution;
- S9 exclusion flow by reason;
- S10 identity-risk prevalence for H3 cohort;
- S11 H1 field-wise descriptive heterogeneity (exploratory, clearly labeled);
- S12 population-volume-weighted sensitivity versus balanced field-year primary estimand.

## Visualization rule

Do not force every ARIS4C paper into a fixed three-figure template.

ARIS4C006 uses as many figures as needed to make its specific data-generating process, mechanism, robustness and limitations visually legible.

No main figure may be dropped solely because its confirmatory result is null.

No exploratory figure may replace a preregistered main figure because it looks stronger.

## PDF / Page rule

The public project card should ultimately point first to:
- English PDF;
- Chinese PDF;

with repository/source links secondary.

The Page may show selected figure thumbnails/previews but should not duplicate the entire manuscript UI.
