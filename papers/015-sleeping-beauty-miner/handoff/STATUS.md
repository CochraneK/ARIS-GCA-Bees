# ARIS4C015 · Current status

- **Title:** Sleeping Beauty Miner: An Integrity-Aware, Time-Safe Agent for Discovering Delayed and Under-Recognized Scientific Work
- **Project status:** pilot1-benchmark-mechanism-common-support-validation
- **Activity:** block
- **Portfolio progress:** 88%
- **Current stage:** Track M · frozen-case common-support gate
- **Evidence established:** 603-paper deterministic multi-seed acquisition + frozen 3 literature-known primary cases + standard risk-set control reuse + offline reanalysis; 1:1 match rate 1.0 but max abs SMD 1.633; 1:4 worsens to 2.417; Washburn-1921 minimum observed sleep-rate gap 1.180; exact complete-frame cursor inventory + resumable history reconstruction are now implemented and CI-tested
- **Next gate:** After the OpenAlex rate window resets, execute the complete same-field/same-year frame inventory and resumable histories for the 3 frozen known cases; rerun frozen 1:1 SMD diagnostics without relaxing 0.10; independently validate OpenAlex trajectory/B
- **Blocker:** External acquisition gate: current OpenAlex API rate window is exhausted; complete-frame tooling is ready. Scientific blockers remain inadequate common support (especially Washburn 1921) and provisional OpenAlex Beauty-Coefficient calibration.

## Source of truth

This snapshot is synchronized from `paper.json` and `papers/dashboard.json`. Study-specific `process/` files may contain finer-grained status and frozen design details.
