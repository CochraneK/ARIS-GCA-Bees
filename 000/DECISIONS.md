# ARIS4C 000 · Decision Log

## 2026-09-19 · Git-resident 000 controller

**Decision:** Create a dedicated Git-resident 000 command-center handoff.

**Why:** The chat named 000 is the human-facing portfolio controller, but cross-account/computer/agent continuity cannot rely on that chat being available. A new executor needs one obvious repository entry point before selecting a numbered paper.

**Boundary:** 000 summarizes portfolio state and scheduling. It does not duplicate or override paper-level scientific truth.

## 2026-09-19 · Four-state live execution taxonomy

**Decision:** Use Finish / Active / Wait / Block as the only primary portfolio execution states.

**Why:** The controller needs to distinguish completed work, genuinely moving work, executable-but-idle work, and externally blocked work.

## 2026-09-19 · Completion-first scheduling

**Decision:** In the absence of an explicit user override, continue genuine Active work first, then select the highest-progress Wait paper.

**Why:** The portfolio should convert near-complete work into finished outputs rather than spreading effort thinly across all executable projects.

## 2026-09-19 · Checkpoint before paper switch

**Decision:** A bounded substantive unit must be committed and its handoff synchronized before 000 intentionally switches to another paper.

**Why:** Git, not chat context, is the recoverable source of truth.
