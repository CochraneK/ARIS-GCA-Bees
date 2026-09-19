# ARIS4C007 · Session log

Append substantial execution sessions in reverse chronological order or chronological order, but remain consistent.

## 2026-09-19 · Continuity retrofit

- Added the standardized ARIS4C per-paper handoff package.
- Bootstrapped project context, current state, TODO, decision history, and a public-safe conversation record.
- Established Git as the cross-device / cross-account / cross-agent continuity surface.
- Future material sessions must append execution results and validation here.

## 2026-09-19 · Pilot 3A–3C molecular build and deletion checkpoint

- Read the current Git repository before handoff and treated Git as canonical.
- Confirmed Pilot 3A PASS: MMC v3.0.0 Clock2/3 coefficient and linear-predictor parity; MammalMethylClock v1.1.0 Clock-3 inverse wrapper warning; Clock 1 quarantined.
- Confirmed Pilot 3B PASS: GSE223748 metadata-first audit; 50-sample / 6-species independent `panmammalianclocktrainingset=no` holdout frozen.
- Built the Pilot 3C bounded smoke pipeline and full 50-sample chained workflow.
- Split the full molecular pipeline into raw IDAT → SeSAMe → molecular Clock2/3 linear predictors, followed by separate life-history inverse transforms.
- Added clock-era versus current-AnAge trait-vintage sensitivity.
- Added Pilot 4 phylogenetic plan using posterior mammal tree sets and longevity-record quality sensitivity.
- Diagnosed four Pilot 3C smoke attempts layer by layer. The latest pre-fix run `35424097947` downloaded all 20 raw IDATs; the remaining failure was a CRLF filename bug in `download_manifest.tsv`.
- Fixed TSV manifests to LF and added defensive filename trimming in both R runners.
- Triggered corrected verification run `35433019496`; at deletion checkpoint it was the active gate.
- Updated `paper.json`, `papers/dashboard.json`, `process/STATUS.md`, and the handoff package before chat deletion.
- User requested chat deletion only after the useful state was persisted to Git; this log is the public-safe execution record for that handoff.

## 2026-09-19 · Pilot 3C coverage diagnosis and clock-era replication gate

- Modern SeSAMe SHCDPB smoke run `35438430019` completed all acquisition and preprocessing infrastructure but failed the unchanged >=95% required-CpG coverage gate.
- Added diagnostics separating required-probe name presence, raw finite betas, species-structural non-mapping, residual QC missingness and final clock-input coverage.
- Verified that Clock2/3 required probe-name coverage is 100% across the frozen 10-sample smoke set, eliminating probe-ID mismatch as the current failure layer.
- Applied beta=0.5 only to CpGs structurally masked by SeSAMe species inference; residual pOOBAH/QC missingness remains missing and continues to count against the gate.
- Modern SHCDPB minimum final coverage is 0.8971 for Clock2 and 0.8895 for Clock3; the 0.95 threshold was not relaxed.
- Historical method audit identified the 2023 Mammal40 non-human recommendation as SeSAMe 1.18.4 / SHCDPM rather than the current SHCDPB recipe.
- Added a separate clock-era smoke workflow using R 4.3, Bioconductor 3.17, SeSAMe 1.18.4 and SHCDPM on the same frozen samples and pinned MMC v3.0.0 coefficients.
- Modern SHCDPB is retained as a sensitivity/QC route; it is not being rewritten as the primary clock-era replication.
