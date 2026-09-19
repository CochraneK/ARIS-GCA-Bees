# ARIS4C 000 · Portfolio Command Center

This is the Git-resident entry point for the ARIS4C portfolio controller.

**000 is not a paper.** It coordinates numbered papers without becoming a second scientific source of truth.

## Read in this order

1. [AGENT_HANDOFF.md](AGENT_HANDOFF.md) — immediate takeover brief
2. [STATUS.md](STATUS.md) — current portfolio state and live queue
3. [TODO.md](TODO.md) — controller-level next actions
4. [DECISIONS.md](DECISIONS.md) — portfolio operating decisions
5. [CONTEXT.md](CONTEXT.md) — role and canonical boundaries
6. [SESSION_LOG.md](SESSION_LOG.md) — controller execution history

Then read:

- [ARIS4C_OPERATING_MODEL.md](../ARIS4C_OPERATING_MODEL.md)
- [ARIS4C_STATUS_MODEL.md](../ARIS4C_STATUS_MODEL.md)
- [papers/dashboard.json](../papers/dashboard.json)

When 000 selects a paper, switch to that paper's `handoff/README.md` before substantive work.

## Canonical boundaries

- Portfolio state / queue: `papers/dashboard.json`
- Scheduling rules: `ARIS4C_OPERATING_MODEL.md`
- State definitions: `ARIS4C_STATUS_MODEL.md`
- Scientific truth: each paper's native files
- Cross-session continuity: each paper's `handoff/`

000 summarizes and dispatches. It does not override paper-level evidence or frozen design decisions.
