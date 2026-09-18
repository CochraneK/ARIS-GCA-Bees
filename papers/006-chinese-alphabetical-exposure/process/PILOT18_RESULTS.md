# ARIS4C006 · Pilot 18 — official ChineseNames 2025.8 source-package provenance

Last updated: 2026-09-19

## Verdict

**PASS. The population table used by ARIS4C006 is reproduced from the official ChineseNames 2025.8 R-universe source package.**

GitHub Actions run: `35406948638`  
Artifact: `aris4c006-chinesenames-r-verify`

## Source

Official R-universe source package:

`ChineseNames_2025.8.tar.gz`

Observed SHA-256:

`899d5af6137e726d0940fd9f28d3f436af06ccb500fd964704cab5bfb0406cad`

The workflow reads the source-package `familyname` data directly with base R and does not install the package's large dependency graph.

## Reproduction

- package name: **ChineseNames**
- package version: **2025.8**
- source-package surname rows: **1,806**
- engineering mirror rows: **1,806**
- surname characters and legacy initials: exact match
- integer fields including `n.1930_2008`: exact match
- package population total: **1,181,719,774**
- mirror population total: **1,181,719,774**

Derived display fields:
- maximum `ppm.1930_2008` difference: 0.0004984
- maximum `surname.uniqueness` difference: 0.0004995

Those differences are solely the engineering mirror's three-decimal rounding: rounding the official package values to 3 decimals gives exact equality.

## Consequence

The public engineering mirror is validated as a faithful source for the integer population counts used in pipeline development.

Confirmatory population weights are provenance-anchored to:
- ChineseNames **2025.8** official source tarball;
- the above SHA-256;
- exact `n.1930_2008` values.

Surname-specific pronunciation/order remains supplied by the separately pinned CCNC lexicon, not the ChineseNames legacy initial field.

## Gate consequence

**Pinned ChineseNames population-provenance gate: PASS.**

Together with Pilots 15 and 17, the surname population-calibration stack is now fully provenance-closed before outcome estimation.
