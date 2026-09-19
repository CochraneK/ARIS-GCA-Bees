# ARIS4C 000 · Current Portfolio Status

> Generated snapshot. Canonical live portfolio state remains `papers/dashboard.json`.

- **Controller:** ARIS4C 000
- **Scheduling:** completion-first
- **Canonical state:** git
- **Default Active WIP:** 1
- **Active WIP policy:** adaptive
- **Soft reference:** 3 for ordinary single-controller workflows; **no fixed hard maximum**
- **States:** Finish / Active / Wait / Block
- **Paper switch rule:** checkpoint bounded substantive work to Git before switching

## Current queue snapshot

- **Finish:** 001, 002
- **Active:** 015, 007, 003
- **Wait:** 011, 014, 012, 006, 008, 009, 017
- **Block:** 004, 010, 005, 016, 013

## Current dispatch

Continue **015** first. The next completion-first Wait candidate is **011** whenever additional genuine execution capacity becomes available.

The current three Active papers do **not** fill a hard cap. More papers may become Active if the current model/agent/tool setup can sustain real parallel research without weakening context isolation, checkpoint discipline, or state accuracy.

Recalculate from `papers/dashboard.json` after any material state change.
