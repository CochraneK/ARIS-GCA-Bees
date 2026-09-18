# Pilot 2 — seed acquisition attrition and issue readiness

Updated: 2026-09-18

## Purpose

Pilot 2 converts the six-case source-anatomy seed into the first quantitative Track A acquisition result.

The key distinction is between:

1. **artifact availability** — whether any time-safe historical object exists for a paper; and
2. **issue readiness** — whether the exact artifact role needed to evaluate the documented issue is time-safe and available.

These are deliberately not treated as the same quantity.

## Six-seed issue classification

The six documented issues split into:

- **3 CONTENT_ELIGIBLE issues**
  - PLOS figure-panel switch;
  - Nature Fig. 6 scientific-content correction;
  - SAGE Table 1 row-information omission.
- **2 CONTENT_INELIGIBLE issues for primary Track A issue recall**
  - gift authorship;
  - manipulated peer review/editorial process.
- **1 ADJUDICATION_REQUIRED issue**
  - a retraction notice giving broad concerns about scientific accuracy and legitimacy without a sufficiently specific issue type for confirmatory issue-level scoring.

The two content-ineligible cases may still be screened for other manuscript anomalies, but absence of a content signal is not counted as failure to detect the officially documented process/authorship issue.

## Artifact availability result

Two of the six target papers currently have at least one verified SAFE_EXACT historical object:

- PLOS correction target: pre-correction publisher HTML;
- J-STAGE retraction target: pre-retraction publisher HTML and PDF.

This is **descriptive acquisition evidence only**. The seed is too small and intentionally heterogeneous to estimate population-level archival availability.

## Issue-readiness result

Among the three clearly content-eligible documented errors:

| Target issue | Required historical role | Current strict status |
| --- | --- | --- |
| PLOS figure-panel switch | figure_image | BLOCKED_REQUIRED_ROLE |
| Nature Fig. 6 correction | figure_image | BLOCKED_REQUIRED_ROLE |
| SAGE Table 1 omission | table | BLOCKED_REQUIRED_ROLE |

Therefore, at the current strict acquisition stage:

- SAFE_EXACT issue-ready: **0/3**
- PROXY_ONLY issue-ready: **0/3**
- blocked on required artifact role: **3/3**

This is not a detector-performance result. No detector has yet been given a valid denominator for these three known-error issues.

## Why the 0/3 result is useful

The PLOS case demonstrates the central failure mode. A pre-correction HTML page exists and is SAFE_EXACT for body text, but the historical Figure 1 image object has not been independently verified. Calling the entire paper "historically available" would therefore make an image benchmark look more complete than it is.

The J-STAGE case demonstrates the converse. An excellent SAFE_EXACT historical PDF exists, yet the target issue is gift authorship. Artifact availability is high while issue-specific content detectability is low.

Thus:

**paper-level historical availability != issue-level benchmark readiness**

## Funnel interpretation

For the six-case seed, the current funnel is:

6 documented issues
→ 3 clearly content-eligible for primary Track A issue recall
→ 0 currently have every required SAFE_EXACT artifact role
→ detector recall is therefore not yet estimable for the eligible issue subset

Separately:

6 target papers
→ 2 have at least one SAFE_EXACT historical object

The two funnels answer different questions and must not be merged.

## Next threshold

Pilot 2 should not be treated as a confirmatory benchmark. The next operational target is to expand acquisition until there are enough SAFE_EXACT issue-ready cases in multiple detector families to calculate at least a descriptive detector yield and false-alert burden without a denominator dominated by archive failure.
