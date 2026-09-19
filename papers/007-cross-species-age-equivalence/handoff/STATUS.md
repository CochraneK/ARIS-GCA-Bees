# ARIS4C007 · Current status

- **Title:** Are Animal Years Comparable? Benchmarking Cross-Species Biological Age Equivalence Across Mammals
- **Project status:** pilot3c-molecular-smoke
- **Activity:** active
- **Portfolio progress:** 78%
- **Current stage:** Pilot 3C · clock-era preprocessing replication gate
- **Evidence established:** Pilot0 785 mappings + Pilot1 88-species demography + Pilot2 945 held-out events + Pilot3A MMC v3.0.0 parity PASS + Pilot3B frozen 50-sample/6-species pan-clock-training=no holdout. Modern SeSAMe SHCDPB 10-sample smoke resolved IDAT/CRLF/probe-ID layers: Clock2/3 required probe names are 100% present; species-nonmapping 0.5 convention raises usable coverage, but residual QC-missing leaves minimum final coverage 0.8971 / 0.8895, below the frozen 0.95 gate.
- **Next gate:** Run the same frozen 10-sample set under the 2023 clock-era stack (R 4.3 / Bioconductor 3.17 / SeSAMe 1.18.4 / SHCDPM). If >=95% Clock2/3 input coverage passes, run the frozen 50-sample holdout under the same clock-era preprocessing; preserve modern SHCDPB as a sensitivity/QC route.
- **Blocker:** Method replication gate, not download engineering: modern SHCDPB preprocessing does not reproduce >=95% clock-input coverage for all frozen samples. Clock-era SeSAMe 1.18.4/SHCDPM workflow is implemented and queued; the 0.95 threshold remains unchanged.

## Source of truth

This snapshot is synchronized from `paper.json` and `papers/dashboard.json`. Study-specific `process/` files may contain finer-grained status and frozen design details.
