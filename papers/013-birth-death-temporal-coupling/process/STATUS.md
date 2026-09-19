# STATUS · ARIS4C013

**Project:** Born to Die? Birth–Death Temporal Coupling  
**Stage:** empirical feasibility / administrative-data transfer gate  
**Date:** 2026-09-18

## Completed
- [x] Promoted to ARIS4C slot 013.
- [x] Defined environment → birthday → culture → traditional-calendar hypothesis ladder.
- [x] Seeded birthday-effect and month-of-birth literature.
- [x] Captured the 1993 Chinese-American claim and 2006 failed replication.
- [x] Added multiple-testing, pseudo-calendar and matched-complexity safeguards.
- [x] Distinguished date-only traditional-calendar testing from full Bazi.
- [x] Audited NBER/NVSS 1988 layout: death month/day are present, exact birth day is not; paired exact-date Pilot is blocked on this source.
- [x] Ran Wikidata Pilot 0A on 2,953,301 biographies.
- [x] Demonstrated a major precision artifact: 23.9% of eligible births and 24.7% of deaths were recorded on Jan 1; 336,356 records had Jan 1 for both.
- [x] Identified BUNMD/Numident as the primary public administrative source with exact birth and death day fields.
- [x] Confirmed BUNMD bunmd_v2.zip is public/unrestricted but direct Dataverse access requires guestbook 506.
- [x] Probed guestbook 506: name, email, institution, and position are all required; ARIS4C will not fabricate those fields.
- [x] Built and CI-tested a raw NUMIDENT fixed-width Pilot 1 parser using the published death-file layout.
- [x] Preserved the locked discovery window (1988–1996), untouched holdout (1997–2005), and prespecified date-heaping filters in the raw parser.
- [x] Completed a pre-outcome null-model stress test and upgraded Pilot 1 to **null-model v2** before any administrative coupling outcome was available.
- [x] Removed exact-age boundary selection from the primary sample: year-gap 19–110 is now the phase-safe primary eligibility rule.
- [x] Promoted **exact birth year × death year × sex** to the primary marginal-independence null; birth-decade × death-year × sex is retained as a visible sensitivity null.
- [x] Added a deterministic toy audit showing that an exact-age boundary filter can manufacture an offset-0 O/E of about **2.98** under a true no-effect data-generating process.
- [x] Added fixed-margin offset-0 mean/variance inference and effect-size classification shared by discovery and holdout.
- [x] Froze the ordinary birthday-effect SESOI at **±1%** (O/E 0.99–1.01), including practical-null equivalence rules.
- [x] Built a **mechanically gated temporal holdout runner** for raw NUMIDENT.
- [x] Added a two-step holdout release protocol; the repository default remains locked and CI treats an accidental unlock as failure.
- [x] Drafted the H3/H4 traditional-calendar feature schema with official-calendar vs Bazi-style boundary conventions kept separate.
- [x] Added the identifiability rule that free 60/12-level categorical cycles cannot by themselves support traditional semantic claims.
- [x] Added a **traditional-feature execution gate**.
- [x] Implemented the allowed date-only traditional features with pinned `lunar_python==1.4.8` and passed reference-vector CI across Li-Chun/Lunar-New-Year boundaries.
- [x] Implemented 1,000 deterministic matched pseudo systems for semantic-map/boundary controls.
- [x] Feature construction is now **FROZEN v1.0** with Git blob verification; any implementation/vector/pseudo-generator edit invalidates the gate.
- [x] Split feature materialization from H3/H4 outcome analysis: `TRADITIONAL_MODEL_SCHEMA.json` remains **frozen=false**, so mortality-outcome peeking is still mechanically blocked.

## Pilot 0A result
The naive same-month/day observed/expected ratio was 2.6768. This is **not evidence of a birthday or astrological effect** because the source is dominated by low-precision date heaping. Excluding all records with day-of-month 1 reduced the ratio to 1.8250 but did not remove the anomaly, so further precision filtering is required.

Interpretation: Pilot 0A successfully stress-tested the pipeline and showed why precision metadata and administrative imputation controls are mandatory.

## Administrative data status

### BUNMD
Scientifically suitable and unrestricted, but the Harvard Dataverse download is **interaction-gated** by CenSoc guestbook 506. The guestbook requires four identity fields: name, email, institution, and position. No automated response will be submitted with invented identity information.

### Raw NUMIDENT
The public-use death files are a viable fallback and independent audit source. The death record itself contains birth month/day/year and death month/day/year, plus proof-of-death, DOB-exception, death-source, and verified-EDR fields. The parser and synthetic fixed-width tests are ready.

OpenICPSR hosts two death archives, approximately 938 MB each, but its download flow requires an authenticated browser/terms session rather than a stable anonymous file API.

## Open gates
- **A — Administrative data transfer:** obtain either BUNMD through a truthful guestbook submission or the two raw NUMIDENT death archives through OpenICPSR's authenticated download flow.
- **B — Administrative Pilot 1:** run the **v2-locked** 1988–1996 discovery immediately after either source is available.
- **C — Precision audit:** quantify prespecified day 1/4/15 heaping and report exception/source fields before interpreting offset 0.
- **D — Discovery freeze:** commit discovery results and freeze any justified sensitivity analyses without altering the locked primary specification.
- **E — Temporal holdout:** after discovery freeze and two-step release authorization, evaluate 1997–2005 exactly once under the fixed ±1% benchmark.
- **F — Traditional-calendar feature layer:** **frozen v1.0**. Outcome model remains locked; next step is source-specific H3/H4 model freeze after administrative source metadata are available, without inspecting H3/H4 outcomes.
- **G — External replication:** seek an independent country/registry.

## Claim ceiling
**No current claim that astrology or Bazi predicts mortality.**

Current justified claim: apparent birth–death coupling can be extremely large when date precision is mishandled; the hypothesis is now operationalized for a population-scale administrative test, but the full administrative dataset bytes are not yet present in the execution environment.

## Immediate next action
The data-independent H2 safeguards and the H3/H4 feature-construction freeze are now implemented. The main external blocker remains administrative data transfer. Once a source is acquired, audit its schema/covariates, freeze the still-locked H3/H4 outcome model without looking at H3/H4 results, then run Pilot 1 v2 and preserve the temporal holdout chain.
