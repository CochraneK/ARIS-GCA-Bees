# ARIS4C 000 · Current Portfolio Status

> Generated snapshot. Canonical live portfolio state remains `papers/dashboard.json`.

- **Controller:** ARIS4C 000
- **Scheduling:** completion-first
- **Canonical state:** git
- **Default Active WIP:** 1
- **Active WIP policy:** adaptive
- **Soft Active WIP reference:** 3
- **Fixed Maximum Active WIP:** none
- **States:** Finish / Active / Wait / Block
- **Paper switch rule:** checkpoint bounded substantive work to Git before switching

## Current queue snapshot

- **Finish:** 001, 002
- **Active:** 011, 003, 007
- **Wait:** 014, 006, 008, 009, 017
- **Block:** 015, 004, 010, 005, 016, 012, 013

## Current dispatch

Continue **011** first. The next completion-first Wait candidate is **014** whenever additional genuine execution capacity becomes available.

A higher Active count is allowed when the current model/agent/tool setup can
sustain genuine parallel research without weakening paper-level isolation,
bounded Git checkpoints, supervision, or truthful live-state tracking.

Recalculate from `papers/dashboard.json` after any material state change.
