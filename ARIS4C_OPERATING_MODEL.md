# ARIS4C Operating Model · v1

**Effective:** 2026-09-19  
**Owner:** Cochrane Kang  
**Scope:** how ARIS4C 000 schedules, executes, checkpoints, and switches among numbered papers

## 1. Control-plane model

- **000 is the permanent portfolio command center and default execution entry point.**
- **Git is the canonical long-term state and memory surface.**
- Paper-specific chats are temporary deep-dive rooms, not permanent sources of truth.
- A new agent/account/computer must be able to continue from repository state plus the paper's `handoff/` package.

## 2. One current paper at a time inside 000

Normal 000 execution uses an explicit conceptual lock:

```text
CURRENT PAPER = 00X
```

While a paper is current, read its canonical metadata/handoff first, execute one bounded unit of work, checkpoint it to Git, and only then switch to another paper.

Do not mix scientific assumptions, datasets, frozen decisions, or manuscript claims across papers unless the task explicitly requires a cross-paper comparison.

## 3. Checkpoint-before-switch rule

A substantive research change is not considered complete until it is persisted to Git.

Before switching away from the current paper:

1. update canonical scientific files first;
2. update/synchronize `STATUS.md` and `AGENT_HANDOFF.md`;
3. update `TODO.md`;
4. append material decisions to `DECISIONS.md`;
5. append a public-safe conversation summary to `CHATLOG.md` when relevant;
6. append execution/validation details to `SESSION_LOG.md`;
7. commit the bounded work unit.

**Paper switch gate:** do not intentionally switch to another paper while material state from the current bounded unit remains only in chat.

## 4. WIP limit

- Default in 000: **1 Active paper**.
- Normal upper bound: **3 Active papers** when genuine parallel compute/agents make that useful.
- Do not mark many papers Active merely because they are executable.

See `ARIS4C_STATUS_MODEL.md` for the canonical meanings of Finish / Active / Wait / Block.

## 5. Completion-first scheduling

When the user does not explicitly choose a paper, 000 uses **completion-first scheduling**.

Priority order:

1. **Continue existing Active work first**, provided it is still genuinely moving.
2. If an Active slot is free, select from **Wait** projects by **highest portfolio progress first**.
3. **Block** projects are excluded from the normal execution queue until their dependency is removed.
4. **Finish** projects are skipped unless explicitly reopened.
5. The user's explicit instruction always overrides automatic queue order.

For equal progress, use these tie-breakers in order:

1. smaller/clearer next gate that can be completed as one bounded unit;
2. stronger chance of moving directly to Finish or a major review gate;
3. lower execution cost / fewer new dependencies;
4. lower paper ID as a deterministic final tie-breaker.

## 6. Live-state interpretation

The scheduler distinguishes **can be worked on** from **is actually being worked on**.

- **Active:** a research-specific job is running now, or there has been a recent substantive research update.
- **Wait:** the next step is executable, but the paper is not currently moving.
- **Block:** an external/human/independent-review/data-transfer/permission or similar dependency prevents meaningful progress.
- **Finish:** the current final/output contract is complete.

Repository maintenance alone does not make a paper Active. Examples that do not count by themselves:

- README/index regeneration;
- GitHub Pages deployment;
- handoff synchronization;
- dashboard/status-only edits;
- formatting-only maintenance.

A practical default for “recent” is a **rolling 2-hour window** for substantive paper-folder work. A still-running research job remains Active even if its last commit is older than that window.

## 7. Current queue principle

At any checkpoint, the actionable queue is:

```text
Active first
→ then Wait sorted by progress descending
→ Block only when dependency-clearing work is possible
→ Finish excluded
```

The queue is recalculated from current canonical metadata; it is not a permanent ranking of scientific importance.

## 8. Deep-dive chat rule

Open/use a paper-specific chat when one of these applies:

- sustained theoretical/design discussion would overload 000;
- repeated user–assistant iteration is needed on one paper;
- an independent reviewer/coder context must be separated;
- the task benefits from a long dedicated context.

At the end of the deep dive, checkpoint to Git before treating the result as canonical.

## 9. Failure recovery

If a chat, browser, account, or agent session ends unexpectedly:

1. treat Git as the recoverable truth;
2. read the paper's `handoff/README.md` and `AGENT_HANDOFF.md`;
3. resume from the newest committed bounded unit;
4. do not reconstruct uncommitted scientific decisions from guesswork.
