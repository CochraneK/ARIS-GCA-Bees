# STATUS · ARIS4C013

**Project:** Born to Die? Birth–Death Temporal Coupling  
**Stage:** public NUMIDENT transfer / administrative Pilot 1 gate  
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

## Pilot 0A result
The naive same-month/day observed/expected ratio was 2.6768. This is **not evidence of a birthday or astrological effect** because the source is dominated by low-precision date heaping. Excluding all records with day-of-month 1 reduced the ratio to 1.8250 but did not remove the anomaly, so further precision filtering is required.

Interpretation: Pilot 0A successfully stress-tested the pipeline and showed why precision metadata and administrative imputation controls are mandatory.

## Administrative data status

### BUNMD
Scientifically suitable and unrestricted, but the Harvard Dataverse download is **interaction-gated** by CenSoc guestbook 506. The guestbook requires four identity fields: name, email, institution, and position. No automated response will be submitted with invented identity information.

### Raw NUMIDENT
The public-use death files are a viable fallback and independent audit source. The death record itself contains birth month/day/year and death month/day/year, plus proof-of-death, DOB-exception, death-source, and verified-EDR fields. The parser and synthetic fixed-width tests are ready.

OpenICPSR V3 publicly lists two NUMIDENT death archives, `NUMDEATH01-10_PU.zip` (~938.4 MB) and `NUMDEATH11-20_PU.zip` (~938.1 MB), under DOI `10.3886/E207202V3`. External replication documentation states that the Public-Use NUMIDENT files have no access or use restrictions and explicitly directs replicators to this OpenICPSR deposit. The remaining blocker is file transfer into the execution environment, not scientific eligibility or a BUNMD identity form. Canonical provenance is frozen in `data/numident_source_manifest.json`.

## Open gates
- **A — Administrative data transfer:** transfer the two public-use raw NUMIDENT V3 death archives into the execution environment and verify archive/file-layout hashes. BUNMD remains an optional cleaned replication route, not a prerequisite.
- **B — Administrative Pilot 1:** run the locked 1988–1996 discovery immediately after either source is available.
- **C — Precision audit:** quantify prespecified day 1/4/15 heaping and report exception/source fields before interpreting offset 0.
- **D — Discovery freeze:** commit discovery results and freeze any justified sensitivity analyses without altering the locked primary specification.
- **E — Temporal holdout:** evaluate 1997–2005 exactly once.
- **F — Traditional-calendar feature freeze:** only after the ordinary calendar/anniversary model is established.
- **G — External replication:** seek an independent country/registry.

## Claim ceiling
**No current claim that astrology or Bazi predicts mortality.**

Current justified claim: apparent birth–death coupling can be extremely large when date precision is mishandled; the hypothesis is now operationalized for a population-scale administrative test, but the full administrative dataset bytes are not yet present in the execution environment.

## Immediate next action
Acquire the two public-use NUMIDENT V3 death archives from OpenICPSR, verify the raw layout, and run the already-locked 1988–1996 Pilot 1. Do not change the design while waiting for file transfer. BUNMD can be added later as a cleaned-source replication.
