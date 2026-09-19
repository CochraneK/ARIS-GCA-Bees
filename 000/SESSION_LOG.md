# ARIS4C 000 · Session Log

## 2026-09-19 · Controller handoff created

- Added a dedicated Git-resident 000 command-center entry point.
- Bound 000 to the repository operating model and four-state status model.
- Recorded completion-first scheduling and checkpoint-before-switch as controller rules.
- Established that new agents should read 000 first, then enter the selected paper through its `handoff/` package.


## 2026-09-19 · Pre-delete controller checkpoint

- Re-read live `main`, recent commits, `papers/dashboard.json`, 000 controller files, and representative paper handoffs.
- Verified portfolio now contains **17 papers (001–017)**.
- Verified current primary state snapshot: Finish 001/002; Active 003/015; Wait 006/007/008/009/011/012/014/017; Block 004/005/010/013/016.
- Verified the public Research Command Center split-view behavior is already committed on main:
  - All projects → rolling marquee;
  - Finish/Active/Wait/Block → detailed cards;
  - search → detailed cards;
  - Hero summary → All only;
  - public paper actions → English / 中文 only.
- Verified representative handoff snapshots for 004, 011, 014, 015, 016 and 017 are synchronized to current dashboard state.
- Added `PRE_DELETE_CHECKPOINT_2026-09-19.md` as the deletion-safe recovery point.

## 2026-09-19 · Command-center visibility correction

- User clarified that Finish and no-progress-today projects should be hidden **only from the time progress curve**, not from the rest of the command center.
- Removed the accidental global `0 < progress < 100` filtering from the portfolio generator.
- Restored Finish navigation, Finish legend/overview counts, and complete All-projects showcase/card visibility.
- Changed today's chart payload to include only non-Finish projects with an actual percentage change across today's checkpoints.
- Hardened command-center JS so theme/storage/chart/showcase failures cannot prevent navigation, Reset, search, sorting, or other controls from receiving listeners.
- Added CI audit for complete portfolio visibility, chart-only filtering, control presence, and JavaScript syntax.

## 2026-09-19 · Daily progress idle-gap compression

- Replaced the linear wall-clock x-axis with an adaptive discontinuous axis for the daily progress chart.
- Long inactivity is detected relative to the day's normal checkpoint cadence, not by one fixed arbitrary threshold.
- Compressed gaps retain explicit dashed break markers, `//`, real idle duration, and real-time tooltip provenance.
- Added CI audit tokens so accidental removal of the compression/disclosure mechanism fails the command-center audit.

## 2026-09-19 · Adaptive vertical progress range

- Added an adaptive Y-axis to the daily progress chart so unused percentage ranges no longer flatten meaningful movement.
- Kept at least a 20-point visible range as an anti-exaggeration guard.
- Added Y-axis break marks plus an explicit visible Y-range in the chart summary whenever 0–100% is truncated.
- Extended command-center CI audit to require the adaptive-axis safeguards.
