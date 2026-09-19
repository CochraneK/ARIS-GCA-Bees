# ARIS4C Portfolio Status Model · v1

**Effective:** 2026-09-19  
**Scope:** the primary activity state of every numbered ARIS4C paper

ARIS4C uses exactly three mutually exclusive primary activity states.

| State | 中文 | Meaning |
|---|---|---|
| `active` | 进行中 | The next meaningful research step is known and executable now with the currently available environment/resources. |
| `waiting` | 等待中 | The next step is known, but meaningful progress depends on an external condition such as human/independent review, native-speaker annotation, data transfer/acquisition, permission, another execution surface, or similar dependency. |
| `quiet` | 静默 | The project is intentionally not under active execution. This includes submission-ready/completed work and deliberately parked work. |

## What is not a primary state

The following are orthogonal signals and must not become new top-level categories:

- **Freshness / last meaningful update** — how long since scientific work changed.
- **Running** — whether a CI, compute, or research job is executing right now.
- **Blocker / dependency reason** — why a project is waiting or what constrains the next step.
- **Scientific/review gate** — a research-process checkpoint; it does not itself define portfolio activity.

Therefore:

- an `active` project can be stale;
- a `waiting` project can receive frequent metadata/CI commits while still waiting;
- a `quiet` project may remain unchanged indefinitely without being considered stale in a problematic sense.

## Canonical rule

`papers/dashboard.json -> projects -> <id> -> activity` is the canonical portfolio activity field.

Only these values are valid:

```text
active
waiting
quiet
```

Legacy values such as `gated` and `blocked` are invalid as primary activity states. Their underlying meaning belongs in `next_gate`, `blocker`, handoff status, or freshness/running metadata instead.
