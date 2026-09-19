# ARIS4C015 · Session log

Append substantial execution sessions in reverse chronological order or chronological order, but remain consistent.

## 2026-09-19 · Continuity retrofit

- Added the standardized ARIS4C per-paper handoff package.
- Bootstrapped project context, current state, TODO, decision history, and a public-safe conversation record.
- Established Git as the cross-device / cross-account / cross-agent continuity surface.
- Future material sessions must append execution results and validation here.

## 2026-09-19 · Pilot-M risk-set design hardening and offline reanalysis

- Ran v4 (100 controls/case), v5 (deterministic nested 200), v6 (standard
  cross-risk-set control reuse), and v7 (1:4 sensitivity) live workflows.
- Added deterministic multi-seed control acquisition beyond the OpenAlex
  one-page 100-work limit and accompanying tests.
- Corrected primary risk-set semantics to allow eligible controls to recur
  across distinct event-time risk sets while remaining unique within one set.
- Added and tested explicit frozen primary case IDs.
- Parameterized controls-per-case and confirmed that 1:4 does not rescue
  balance.
- Added an offline workflow that downloads the v7 603-paper acquisition
  artifact and recomputes matching without any OpenAlex request.
- Frozen 3-case results:
  - 1:1: match rate 1.0; n=3; max abs SMD 1.633.
  - 1:4: match rate 1.0; n=12; max abs SMD 2.417.
- Common-support minimum event-time sleep-rate gaps:
  - EPR 1935: 0.438.
  - Washburn 1921: 1.180.
  - Hummers 1958: 0.063.
- Cross-checked provisional candidate identity/later-use evidence; trajectory/B
  validation remains open.
- Live v8 acquisition failed with OpenAlex HTTP 429 after the rate window was
  exhausted; this did not invalidate the existing cohort artifact.
- Checkpointed the consolidated evidence in
  `data/pilotM_riskset_diagnostics_2026-09-19.json`.
- Updated paper metadata/dashboard to 88%, Active, stage
  `Track M · frozen-case common-support gate`.

## 2026-09-19 · Complete-frame acquisition tooling

- Added exact OpenAlex Works cursor enumeration and frame-count reconciliation.
- Added a metadata-only complete-frame inventory stage for the three frozen
  literature-known cases.
- Added resumable JSONL citation-history reconstruction that skips completed
  OpenAlex IDs and supports bounded batches.
- Added manual GitHub Actions workflows for full-frame inventory and resumable
  history batches; partial checkpoints are preserved as artifacts.
- Added unit tests for cursor enumeration, exact year × field filters, resume
  semantics, and bounded batches. ARIS4C015 CI runs 186–191 passed.
- No mechanism threshold or substantive result changed.
- Current live OpenAlex rate window remains exhausted, so the next empirical
  full-frame run is externally blocked rather than code-blocked.
- Dashboard activity moved from Active to Block at 88% so the 000 controller
  can allocate execution capacity elsewhere.
