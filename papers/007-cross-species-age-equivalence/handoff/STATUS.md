# ARIS4C007 · Current status

- **Title:** Are Animal Years Comparable? Benchmarking Cross-Species Biological Age Equivalence Across Mammals
- **Project status:** pilot3c-molecular-smoke
- **Activity:** active
- **Portfolio progress:** 76%
- **Current stage:** Pilot 3C · independent raw-IDAT molecular smoke
- **Evidence established:** Pilot0 785 mappings + Pilot1 88-species demography + Pilot2 945 held-out events + Pilot3A MMC v3.0.0 parity PASS + Pilot3B frozen 50-sample/6-species pan-clock-training=no holdout
- **Next gate:** Pass 10-sample/6-species SeSAMe SHCDPB Clock2/3 smoke at >=95% CpG coverage, then auto-run frozen 50-sample full holdout
- **Blocker:** Engineering only: latest failed smoke downloaded all 20 IDATs but CRLF in download_manifest.tsv polluted Bash filenames; fix is committed and rerun 35433019496 is in progress

## Source of truth

This snapshot is synchronized from `paper.json` and `papers/dashboard.json`. Study-specific `process/` files may contain finer-grained status and frozen design details.
