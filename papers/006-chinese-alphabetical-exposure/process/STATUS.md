# ARIS4C006 STATUS

Last updated: 2026-09-18

## Current state

**RUNNING — novelty, data-feasibility, and identification stage**

The question is sufficiently defined to enter ARIS, but the project is not yet preregistration-ready and no confirmatory career-outcome analysis should begin.

## Canonical question

Among Chinese scholars, does surname alphabetical position predict academic visibility or career outcomes specifically under greater exposure to empirically measured alphabetical author-ordering regimes, after calibrating against the non-uniform Chinese population surname distribution?

## Completed

- [x] Stable paper ID `006` and canonical folder created.
- [x] ARIS v0.4.26 provenance pinned to commit `951654847b015585385b2448c5667dcd04e7b56b`.
- [x] Scope narrowed to Chinese names / Chinese scholars.
- [x] ChineseNames 2025.8 identified as the primary surname-population baseline; underlying population data remain 1930–2008.
- [x] Raw A–Z equal-frequency comparison prohibited.
- [x] Main mechanism reframed as `surname rank × actual alphabetization exposure`, not a mystical/psychological letter effect.
- [x] Li & Yi (2021) identified as a direct Chinese predecessor.
- [x] D'Angelo (2026) identified as a direct recent bibliometric predecessor using expected national surname distributions.
- [x] Cross-field author-order intensity identified as the main source of mechanism heterogeneity.
- [x] Elicit API route tested and found unavailable under the connected plan; Consensus search quota also exhausted. Public-web / GPTPage fallback is therefore active and must be recorded in provenance.

## In progress

- [ ] Closest-prior-work / novelty map beyond the first anchor papers.
- [ ] Executable ChineseNames extraction and validation pipeline.
- [ ] OpenAlex sampling and author-order pilot.
- [ ] Operational definition of “Chinese scholar.”
- [ ] Surname parsing / Pinyin normalization protocol.
- [ ] Empirical alphabetization-intensity estimator.
- [ ] Causal/DAG audit and confounding-control hierarchy.
- [ ] Author-disambiguation error audit for common Chinese names.
- [ ] Pre-analysis specification / preregistration draft.
- [ ] GPTPage adversarial reviewer packet.

## Hard gates before confirmatory outcome analysis

1. `Chinese scholar` cannot be inferred solely from a Chinese-looking name.
2. Equal-frequency A–Z expectations are forbidden; population calibration is mandatory.
3. Surname initial cannot be treated as randomized without sensitivity to geography/ancestry and surname-frequency structure.
4. Alphabetization exposure must be measured from observed publication-order behavior, preferably at journal × field × year or similarly granular levels.
5. Chance alphabetization must be corrected for team size; a two-author paper being alphabetical is not strong evidence of a convention by itself.
6. Primary exposure construction must not use the focal career outcome.
7. Common-name author disambiguation error must be stress-tested before any surname-frequency or surname-rank effect is interpreted.
8. Li & Yi (2021) and D'Angelo (2026) must be treated as prior art that narrows novelty claims.
9. Single-authored works and low-alphabetization fields must be retained as negative-control contexts where applicable.
10. Elite-list outcomes are secondary validation, not the sole definition of scientific success.

## Next machine-readable checkpoint

When `RESEARCH_PLAN.md`, `DATA_SOURCES.md`, `LITERATURE_SEED.md`, `AUTO_REVIEW.md`, the surname-baseline extraction code, and the OpenAlex pilot specification exist with critical blockers explicitly resolved or downgraded, change `paper.json` status from `feasibility` to `research-design`.
