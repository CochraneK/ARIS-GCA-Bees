# Data Sources and Feasibility · ARIS4C013

## Tier 1 — Berkeley Unified Numident Mortality Database (BUNMD)

**Primary administrative analysis target.**

BUNMD is a cleaned, harmonized public version of the U.S. Social Security Numident mortality records with approximately 49–50 million deceased individuals. Its published codebook contains:
- `byear`, `bmonth`, `bday`;
- `dyear`, `dmonth`, `dday`;
- sex, race/application variables, place of birth, Social Security state, ZIP at death, and other covariates.

The recommended high-coverage mortality window is **1988–2005**.

### Critical precision warning
The BUNMD codebook explicitly notes surplus death-day counts on the **1st and 15th of the month**, suggesting SSA may have imputed missing day values to those dates. Therefore:
1. day=1 and day=15 are prespecified administrative-heaping flags;
2. coupling estimates must be reported with and without flagged dates;
3. same-day effects at offsets 0, ±14/15, month boundaries, and common imputation dates are treated as data-generation diagnostics before substantive interpretation.

Harvard Dataverse DOI: `10.7910/DVN/TTWNK8`.

## Tier 2 — raw NARA NUMIDENT

NARA's Numerical Identification Files (1936–2007) are publicly released, and a modern OpenICPSR deposit provides the raw death/application/claim files. FamilySearch's current index description confirms records can include exact birth and death dates.

**Use:** independent reconstruction / audit of BUNMD transformations and potentially a second administrative specification.

**Cost:** very large raw files and more complex record harmonization.

## Tier 3 — Social Security Death Master File (DMF)

The underlying public DMF historically contains exact date of birth and date of death. Coverage is high in approximately 1975–2005, but access to the current Limited Access DMF is through NTIS and post-2005 completeness is affected by policy changes.

**Use:** valuable independent U.S. administrative replication if access is available.

## Tier 4 — Wikidata biographies

A third-party 2024-01-01 Wikidata-derived snapshot contains 2,953,301 people with P569/P570 date strings.

**Pilot role only.** Pilot 0A found extreme date heaping:
- eligible records before Feb-29 exclusion: 2,100,569;
- Jan-1 birth rate: 23.86%;
- Jan-1 death rate: 24.67%;
- Jan-1 on both dates: 336,356 records;
- naive same-month/day O/E: 2.6768;
- excluding day=1 on either date: O/E 1.8250.

Because the slim extraction drops Wikidata `timePrecision`, these numbers are treated as a demonstration of precision artifacts, not mortality evidence.

## Blocked route — NBER/NVSS Multiple Cause of Death 1988

A live repository audit of NBER's 1988 Stata layout found:
- `monthdth`;
- `daydth`;
- **no exact birth-day field**.

Therefore this specific mortality file cannot support individual paired birth-day/death-day coupling despite broader CDC wording about exact event dates in older public-use vital-statistics files.

## External replication targets

Swiss national mortality studies already demonstrate birthday-effect analysis at population scale, but exact-date microdata access should be treated as requiring lawful registry access/collaboration unless a public release is confirmed.

Other promising settings include Austria, Denmark, Sweden, Australia, Japan, and Taiwan because birth-season/longevity effects have been studied there and several have population-register infrastructure.

## Minimum variable requirements

**H1:** birth month/year, age at death or death date, sex, cohort.  
**H2:** exact birth day/month and exact death day/month/year.  
**H3:** enough precision for cultural-calendar conversion plus, ideally, cultural-exposure proxies.  
**H4 full Bazi:** exact date **and hour of birth**.

### Critical scope rule
The hour pillar cannot be reconstructed from date-only mortality records. Date-only analyses must be labeled **partial traditional-calendar tests**, not full Bazi validation.
