# ARIS4C Portfolio Status Model · v2

**Effective:** 2026-09-19  
**Scope:** the primary live execution state of every numbered ARIS4C paper

ARIS4C uses exactly four mutually exclusive primary states.

| State | 中文 | Meaning |
|---|---|---|
| `finish` | 完成 | The current final/output contract is complete. No further execution is required unless the paper is deliberately reopened. |
| `active` | 正在推进 | Meaningful research work is running now, or the project has produced a recent substantive paper-folder update. |
| `wait` | 待推进 | The next meaningful step is executable with available resources, but the project is not currently being advanced. |
| `block` | 阻塞 | Meaningful progress depends on an external condition such as human/independent review, native-speaker annotation, data transfer/acquisition, permission, another execution surface, or similar dependency. |

## Active is a live signal

`active` is intentionally stricter than “this project can continue.”

A project is Active when there is evidence that it is actually moving now, for example:

- a research-specific CI/compute job is currently running;
- a recent substantive commit changes scientific code, data, analysis, results, manuscript content, figures/tables, or research design.

The following do **not** by themselves make a paper Active:

- README/index regeneration;
- GitHub Pages deployment;
- handoff synchronization;
- dashboard/status-only metadata edits;
- formatting-only or repository-maintenance commits.

If a project can be continued but has no current/recent meaningful execution, classify it as `wait`.

## Canonical rule

`papers/dashboard.json -> projects -> <id> -> activity` is the canonical portfolio state.

Only these values are valid:

```text
finish
active
wait
block
```

The old portfolio values `quiet`, `waiting`, `gated`, and `blocked` are invalid.

Scientific “gates” can still appear in `stage`, `next_gate`, or project process files. They describe the research workflow, not the portfolio execution state.

## Current mapping after v2 migration

- **Finish:** 001, 002
- **Active:** 015
- **Wait:** 003, 004, 006, 007, 008, 009, 010, 011, 012, 014
- **Block:** 005, 013, 016

This mapping is a snapshot. Active/Wait may change as real research execution starts or stops.
