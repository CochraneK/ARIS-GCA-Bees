# ARIS4C007 · TODO

## P0 · Current gate

- [ ] Inspect corrected Pilot 3C smoke run `35433019496`.
- [ ] Require every smoke sample to produce finite Clock 2/3 linear predictors with >=95% required-CpG coverage.
- [ ] If smoke passes, confirm `.github/workflows/007-pilot3c-full-molecular.yml` auto-starts the frozen 50-sample / 6-species `panmammalianclocktrainingset = no` holdout.
- [ ] If smoke still fails, debug only the first newly failing layer; do **not** redesign the already-passed Pilot 3A/3B protocol.

## P1 · Full molecular benchmark

- [ ] Run all 50 independent holdout samples through SeSAMe `SHCDPB` with compressed GEO IDATs read directly and `collapseToPfx=TRUE`.
- [ ] Preserve Clock2/3 molecular linear predictors before applying any life-history inverse transform.
- [ ] Use MMC v3.0.0 `anage49.csv` clock-era gestation/maturity/max-age traits for the primary reproduction.
- [ ] Re-express the same molecular predictors with current Pilot0/AnAge traits as a trait-version sensitivity analysis.
- [ ] Report species/tissue/life-stage residuals and Clock2-vs-Clock3 molecular human-equivalent disagreement.
- [ ] Keep target-transform circularity explicit: Clock2 and Clock3 targets encode A1/A3-like life-history assumptions.

## P2 · Cross-method integration

- [ ] Add the molecular axis to the A1/A3/A4/A5/A6 disagreement benchmark.
- [ ] Use the 74-sample Pilot2-overlap molecular set only for event-conditioned triangulation, never as the primary independent holdout.
- [ ] Proceed to the frozen Pilot 4 phylogeny plan: posterior mammal trees, multi-tree inference, and leave-one-order-out validation.
- [ ] Build the first multi-axis disagreement atlas only after the independent molecular holdout is stable.

## Continuity / hygiene

- [x] Canonical metadata updated to Pilot 3C molecular smoke.
- [x] CRLF manifest bug isolated and fixed in both smoke/full preparation code; R filename parsing hardened with `trimws()`.
- [x] Current state frozen in `process/STATUS.md`.
- [x] Public-safe conversation/session summary appended before chat deletion.
- [ ] After the next material state change, resync `STATUS.md` and `AGENT_HANDOFF.md`.

## Do not regress

- Do not use MammalMethylClock v1.1.0 `fun_llinreladult.inv()` as canonical Clock 3 inverse.
- Do not include Clock 1 until its separate reference-script issue is validated.
- Do not treat strong DNAm chronological-age accuracy as proof of a unique biological-age equivalence scale.
- Do not silently substitute current AnAge traits for the clock-era traits in the primary molecular reproduction.
