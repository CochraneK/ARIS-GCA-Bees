# ARIS4C006 · Pilot 17 — CCNC-corrected Chinese surname population baseline

Last updated: 2026-09-19

## Verdict

**PASS. This is the primary A–Z surname population denominator for confirmatory calibration.**

GitHub Actions run: `35405847078`  
Artifact: `aris4c006-corrected-population-baseline`

## Authority split

- ChineseNames 2025.8 supplies surname population counts.
- Pinned CCNC surname lexicon supplies surname-specific canonical Hanyu-Pinyin forms and initials.
- The primary denominator is the direct Han-surname intersection.

## Coverage

- ChineseNames rows: **1,806**
- mapped ChineseNames × CCNC rows: **1,166**
- excluded rare rows: **640**
- total ChineseNames population: **1,181,719,774**
- mapped population: **1,181,331,391**
- mapped population share: **99.9671%**
- excluded population share: **0.0329%**

Population shares are renormalized over the mapped mass for primary calibration.

## Corrected surname initials

- surnames whose CCNC surname-specific initial differs from legacy ChineseNames initial: **31**
- population share represented by changed-initial surnames: **0.4383%**

Largest examples:
- 覃: Q -> T
- 单: D -> S
- 解: J -> X
- 褚: C -> Z
- 仇: C -> Q
- 查: C -> Z
- 区: Q -> O

## Population-weighted alphabet position

On the same mapped population rows:

- legacy ChineseNames-initial weighted mean rank: **16.21065**
- CCNC-corrected weighted mean rank: **16.25491**
- shift: **+0.04426 alphabet positions**

Thus the final Chinese surname distribution is slightly later in the alphabet than the engineering baseline suggested.

## Corrected initial distribution

Top population initials:

| Initial | Corrected mapped-population share |
|---|---:|
| L | 18.961% |
| Z | 15.627% |
| W | 11.727% |
| Y | 7.758% |
| C | 7.143% |
| H | 6.477% |
| X | 5.047% |
| S | 4.852% |
| G | 3.538% |
| D | 2.902% |

I, U and V remain zero in the mapped Chinese surname baseline.

## Important baseline shifts

Relative to the legacy initial labels on the same mapped surnames:

- C: −0.0993 percentage points
- D: −0.0790 pp
- J: −0.0557 pp
- Q: −0.1530 pp
- O: +0.0119 pp
- S: +0.0790 pp
- T: +0.1751 pp
- W: +0.0118 pp
- X: +0.0531 pp
- Z: +0.0678 pp

These shifts are small at national scale but material enough that the legacy ChineseNames `initial` column is no longer the confirmatory ordering baseline.

## Homophone aggregation

The mapped surname inventory collapses to **365 canonical Romanized forms**.

When multiple Han surnames share one Romanized form, their population mass is aggregated. Romanized bibliographic records are not assigned an invented specific Han surname.

## Frozen primary baseline

Use:
- `corrected_initial_baseline.csv` for A–Z expected population shares;
- `romanized_population_map.csv` for Romanized-form population calibration;
- CCNC surname-specific initial/rank for direct-Han focal surnames.

Do not use:
- uniform 1/26 probabilities;
- legacy ChineseNames initial/rank as pronunciation truth;
- generic pypinyin output as confirmatory surname pronunciation.

## Gate consequence

**Corrected Chinese surname population calibration: PASS.**

The remaining baseline execution check is reproducibility from the pinned ChineseNames 2025.8 R package rather than only the public engineering mirror.
