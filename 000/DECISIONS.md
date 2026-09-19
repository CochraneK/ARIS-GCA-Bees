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


## 2026-09-19 · Research Command Center split-view UI

**Decision:** Keep two distinct public portfolio presentations.

- `All projects` uses the rolling horizontal research marquee/showcase.
- `Finish / Active / Wait / Block` use the detailed project-card panel.
- Non-empty search results use the detailed card panel.
- The top portfolio Hero/overview is shown only on `All projects`.

**Public card action rule:** expose exactly two paper actions: **English** and **中文**. Prefer PDF targets when available. Do not expose Figures, Tables, Pipeline, Source, or output-readiness badges on project cards.

**Why:** The top-level view is for portfolio discovery and visual scanning; status subviews are operational work surfaces and need denser evidence/gate/blocker detail.


## 2026-09-19 · Adaptive capability-aware Active WIP

**Decision:** Remove the fixed three-paper Active ceiling. Keep 1 as the default WIP and 3 only as a conservative soft reference for ordinary single-controller execution.

**Why:** The useful degree of parallelism depends on the execution environment. Stronger future models, multi-agent orchestration, parallel compute, or better tooling may be able to advance more than three papers simultaneously without sacrificing scientific quality or continuity.

**Guardrail:** Additional Active papers are justified only when they are genuinely moving and paper-level context isolation, bounded Git checkpointing, supervision, and truthful live-state tracking remain intact. If those degrade, WIP should contract rather than preserve a target count.
