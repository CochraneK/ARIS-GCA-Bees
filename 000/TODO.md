# ARIS4C 000 · TODO

## P0 · Scheduling

- [ ] Continue the current genuine Active paper until a bounded unit is checkpointed.
- [ ] When the Active slot becomes free, promote the highest-progress Wait paper.
- [ ] Recalculate the queue after every material paper-state change.

## P1 · Portfolio integrity

- [ ] Keep `papers/dashboard.json` aligned with real execution rather than merely executable work.
- [ ] Keep Active WIP at 1 by default and no more than 3 without a genuine parallel-work reason.
- [ ] Ensure every paper switch passes the checkpoint-before-switch rule.
- [ ] Keep Block reasons explicit and actionable.

## P2 · Public/control surfaces

- [ ] Keep README and Research Command Center synchronized with canonical states.
- [ ] Keep 000 handoff current enough for a new agent/account/computer to resume safely.
