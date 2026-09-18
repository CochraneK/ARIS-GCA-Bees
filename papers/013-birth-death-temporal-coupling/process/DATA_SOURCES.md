# Data Sources and Feasibility · ARIS4C013

## Tier 1 — U.S. NVSS mortality microdata
CDC/NCHS states that public-use vital-statistics files for **1988 and before** can include exact year/month/day of birth and death; later public-use eras remove exact dates.

**Pilot 0 use:** exact birth–death phase coupling and birthday-window analysis.

NBER also distributes NVSS Multiple Cause of Death files with year-specific documentation and convenient formats. Exact required fields must be audited against the original 1988 layout before analysis.

## Tier 2 — Swiss mortality
National studies already demonstrate birthday-effect analyses. Underlying exact-date microdata should be treated as a replication target requiring lawful access/collaboration unless a public release is confirmed.

## Tier 3 — other population registers
Austria, Denmark, Australia, Sweden, and other settings have published birth-season/longevity work. Exact-date access often requires institutional approval.

## Tier 4 — genealogy
Useful for historical replication only with careful deduplication, date-certainty scoring, calendar-conversion rules, and documentation-bias analysis.

## Minimum variable requirements
**H1:** birth month/year, age at death or death date, sex, cohort.  
**H2:** exact birth day/month and exact death day/month/year.  
**H3:** enough precision for cultural-calendar conversion plus, ideally, cultural-exposure proxies.  
**H4 full Bazi:** exact date **and hour of birth**.

### Critical scope rule
The hour pillar cannot be reconstructed from date-only mortality records. Date-only analyses must be labeled **partial traditional-calendar tests**, not full Bazi validation.
