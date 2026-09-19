# ARIS4C007 · TODO

## P0 · Current gate

- [x] Inspect the corrected modern Pilot 3C smoke path through run `35438430019`; IDAT download, CRLF handling, SeSAMe execution and probe-name mapping are resolved.
- [x] Separate required-probe name coverage, raw finite coverage, species-structural 0.5 imputation and residual QC missingness. All Clock2/3 required probe names are present in all 10 samples.
- [ ] Require every smoke sample to produce finite Clock 2/3 linear predictors with >=95% required-CpG coverage; modern SHCDPB still fails this frozen gate (min final coverage 0.8971 / 0.8895).
- [ ] Execute the independent clock-era replication workflow under R 4.3 / Bioconductor 3.17 / SeSAMe 1.18.4 / SHCDPM on the same frozen 10-sample set.
- [ ] If the clock-era smoke passes, run the frozen 50-sample / 6-species `panmammalianclocktrainingset = no` holdout under the same clock-era preprocessing and retain modern SHCDPB as sensitivity/QC.
- [ ] If clock-era smoke still fails, debug only the first newly failing layer; do **not** relax the 0.95 threshold or redesign the already-passed Pilot 3A/3B protocol.

## P1 · Full molecular benchmark

- [ ] Run all 50 independent holdout samples through the clock-era primary preprocessing if its smoke gate passes; keep modern SeSAMe `SHCDPB` as a sensitivity route, with compressed GEO IDATs read directly and `collapseToPfx=TRUE`.
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
