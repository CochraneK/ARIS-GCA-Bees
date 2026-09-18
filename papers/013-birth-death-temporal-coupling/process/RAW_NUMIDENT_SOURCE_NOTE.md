# Raw NUMIDENT route · source and acquisition note

## Why this route exists

ARIS4C013's preferred cleaned administrative source, BUNMD, is publicly listed as unrestricted, but Harvard Dataverse file access is gated by CenSoc guestbook 506. A live probe on 2026-09-18 showed that the guestbook requires name, email, institution, and position. ARIS4C will not fabricate those fields.

The raw public-use NUMIDENT Death Files are therefore the primary fallback and an important independent audit source.

## Source

OpenICPSR project: Numerical Identification Files (NUMIDENT), 1936–2007.

- DOI: 10.3886/E207202V1
- NUMDEATH01-10_PU.zip: approximately 938.4 MB
- NUMDEATH11-20_PU.zip: approximately 938.1 MB

The replication package that republishes these files states that the public-use NUMIDENT files have no access/use restrictions beyond attribution. OpenICPSR itself uses an interactive login/terms download flow and does not provide a stable anonymous per-file API suitable for unattended CI.

## Exact death-record layout used by ARIS4C013

The parser follows the fixed-width positions published in hollina/duke-replication, analysis/scripts/code/1_process_raw_data.do.

| variable | 1-based columns | meaning |
|---|---:|---|
| mobdth | 97–98 | birth month |
| dobdth | 99–100 | birth day |
| yobdth | 101–104 | birth year |
| sex | 105 | sex |
| prfdth | 117 | proof-of-death indicator |
| dobexcep | 137 | DOB exception indicator |
| spexch | 138 | special exception change indicator |
| mbrdobex | 139 | MBR DOB exception indicator |
| dthsrc | 142–143 | source of death |
| verifedri | 144 | verified EDR indicator |
| mod | 145–146 | death month |
| dod | 147–148 | death day |
| yod | 149–152 | death year |

The DOB and DOD variables coexist in the death record, so Pilot 1 does not require joining the application/SS-5 files.

## Analysis contract

The file code/pilot1_numident_raw.py:

1. reads both death zip archives directly;
2. never summarizes the 1997–2005 holdout;
3. uses the same 1988–1996 discovery window as the BUNMD lock;
4. preserves the same birth-decade × death-year × sex marginal-independence null;
5. reports raw and prespecified strict date-heaping estimates;
6. reports DOB exception, proof-of-death, death-source, and EDR fields as diagnostics rather than post-hoc primary filters.

## Current acquisition gate

The code is ready, but the OpenICPSR archives require an authenticated/interactive download session. This is a data-transfer gate, not a scientific-design gate.

Once both archives are available to a runner or local workspace, run:

    python papers/013-birth-death-temporal-coupling/code/pilot1_numident_raw.py \
      --zip NUMDEATH01-10_PU.zip \
      --zip NUMDEATH11-20_PU.zip \
      --json-out pilot1_numident.json \
      --md-out PILOT1_NUMIDENT_RESULT.md
