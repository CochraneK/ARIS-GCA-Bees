# Pilot 0A Result · Wikidata birth–death phase coupling

**Run date:** 2026-09-18  
**Workflow:** `ARIS4C013 Wikidata Pilot 0A`  
**Workflow run:** 35304392589  
**Input:** `dalager/wikidata-incarnations`, Wikidata 2024-01-01-derived snapshot

## Scope
This was a **methods and artifact-detection pilot**, not a population mortality analysis.

The source contains 2,953,301 notable people with birth/death date strings, but the slim extraction omits Wikidata `timePrecision`. The analysis therefore asked whether the proposed circular-time pipeline works and whether date-quality artifacts can mimic birth–death coupling.

## Sample
- Raw rows: **2,953,301**
- Eligible age/date records before Feb-29 exclusion: **2,100,569**
- Primary 365-day phase sample: **2,098,401**
- Sensitivity sample excluding day-of-month 1 on either date: **1,301,536**

## Naive coupling result
Using a birth-decade × death-decade stratified marginal-independence null:
- observed same month/day: **343,464**
- expected: **128,312.7**
- O/E: **2.6768**

After excluding every record where either birth or death day-of-month was 1:
- O/E: **1.8250**

This is far larger than credible birthday-effect estimates in population mortality studies and therefore triggered the artifact gate rather than a substantive claim.

## Precision/heaping diagnostics
- birth day=1: **26.9710%**
- death day=1: **28.1032%**
- birth Jan-1: **23.8555%**
- death Jan-1: **24.6705%**
- Jan-1 on both birth and death: **336,356 records**

The joint Jan-1 mass alone explains most of the spectacular offset-0 spike.

## ±30-day pattern
Outside offset 0, observed/expected ratios around the birthday were generally below 1 in this dataset (roughly 0.82–0.93 across the displayed ±30-day window). This is mechanically compatible with a large artificial mass concentrated at offset 0 and should not be interpreted biologically.

## Interpretation
**Pilot 0A is an artifact-positive result.**

It demonstrates that:
1. exact-looking calendar strings are not equivalent to verified day-level precision;
2. correlated imputation/rounding on birth and death dates can generate enormous apparent “same birthday/death day” effects;
3. a naive analysis could falsely appear to provide extraordinary support for a mystical or calendrical claim;
4. administrative and source-specific imputation rules must be modeled before H2–H4.

## Consequence for ARIS4C013
The project now promotes date-quality analysis to a first-class component of the paper.

The next administrative source, BUNMD, is especially informative because its own codebook flags day 1 and day 15 as possible SSA imputation dates. Those dates will be prespecified negative-control/heaping strata before any mortality coupling result is inspected.

## Claim
**No evidence for astrology/Bazi is inferred from this pilot.**
