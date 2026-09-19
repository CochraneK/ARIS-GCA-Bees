# ARIS4C015 · Current status

- **Title:** Sleeping Beauty Miner: An Integrity-Aware, Time-Safe Agent for Discovering Delayed and Under-Recognized Scientific Work
- **Project status:** pilot1-benchmark-mechanism-common-support-validation
- **Activity:** active
- **Portfolio progress:** 88%
- **Current stage:** Track M · frozen-case common-support gate
- **Evidence established:** 603-paper deterministic multi-seed acquisition + frozen 3 literature-known primary cases + standard risk-set control reuse + offline reanalysis; 1:1 match rate 1.0 but max abs SMD 1.633; 1:4 worsens to 2.417; Washburn-1921 minimum observed sleep-rate gap 1.180; latest design tests/CI PASS
- **Next gate:** Enumerate the complete same-field/same-year control frame for the 3 known cases without relaxing SMD<0.10; if overlap still fails, freeze an overlap-limited estimand/unmatched-case rule; independently validate OpenAlex trajectory/B against SciSciNet-v2 or another source
- **Blocker:** Primary risk-set common support remains inadequate, especially Washburn 1921; OpenAlex API live acquisition hit its current rate limit; OpenAlex Beauty-Coefficient calibration remains provisional

## Source of truth

This snapshot is synchronized from `paper.json` and `papers/dashboard.json`. Study-specific `process/` files may contain finer-grained status and frozen design details.
