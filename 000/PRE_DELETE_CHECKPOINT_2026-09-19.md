# ARIS4C 000 · Pre-delete checkpoint · 2026-09-19

This checkpoint was written immediately before deleting the controlling ChatGPT conversation. Git is canonical; this file is a public-safe recovery summary, not a transcript or hidden chain-of-thought.

## Verified repository state

Base state inspected on `main` after commit `01dea4f3` (`docs: apply ARIS4C migration and regenerate index`).

Current portfolio:
- numbered papers: **001–017**;
- Finish: **001, 002**;
- Active: **003, 015**;
- Wait: **006, 007, 008, 009, 011, 012, 014, 017**;
- Block: **004, 005, 010, 013, 016**.

Canonical live state remains:
- portfolio: `papers/dashboard.json`;
- controller rules: `ARIS4C_OPERATING_MODEL.md` + `ARIS4C_STATUS_MODEL.md`;
- per-paper continuity: `papers/NNN-*/handoff/`;
- public dashboard generator: `tools/build_papers_index.py`;
- dashboard behavior: `docs/command-center.js` + `docs/command-center.css`.

## Public Research Command Center UI decisions

These are deliberate product rules and should not be accidentally reverted:

1. **All projects** uses the rolling horizontal research showcase / marquee.
2. **Finish / Active / Wait / Block** use the previous detailed project-card panel, not the marquee.
3. Any non-empty **search** uses the detailed project-card panel so results are easy to inspect.
4. The top portfolio Hero/overview belongs only to **All projects**; child status views open directly into their work cards.
5. Public project cards expose exactly two paper actions:
   - **English**
   - **中文**
6. Paper buttons are **PDF-first when available**; otherwise they fall back to the best full-paper target. If a full text is not ready, keep the button position disabled rather than inventing another action.
7. Do **not** restore public card buttons for Figures, Tables, Pipeline, Source, or output-readiness badges such as `EN full / 中文 full / FIG / TAB`.
8. Figures/tables/pipeline/source metadata and output gates still exist in Git/CI; they are simply not public card actions.

Relevant UI commits immediately before this checkpoint include:
- `f21f68eb` — rolling board for All, detailed cards for filtered views;
- `122614f7` — show marquee only for All and detailed grid for subviews;
- `486ecb81` — keep a single detailed portfolio grid for subviews;
- `d760c79f` — switch All marquee against the existing detailed portfolio panel;
- `01dea4f3` — regenerate public index from latest canonical state.

## Scientific/project continuity verified

Project handoff snapshots were checked for 004, 011, 014, 015, 016 and 017 and already reflect the current dashboard state.

Notable current gates:
- **004**: blocked on genuinely independent 40-case identity second review.
- **011**: five development true-positive evaluations across F5/F3/F8/F3/F1; now Wait, with comparator/control + confirmatory-freeze work next.
- **014**: conservative China cross-source entity layer; stable-ID-only auto-merge policy remains in force.
- **015**: Active at event-time risk-set balance gate; do not relax SMD < 0.10 post hoc.
- **016**: blocked on independent/native-speaker annotation.
- **017**: Wait; new predictive-language-space project separated from finished 002.

Do not reconstruct these papers from this file alone. Enter each project through its `handoff/README.md`.

## Resume instructions for a new chat / account / agent

1. Read `000/README.md` and `000/AGENT_HANDOFF.md`.
2. Read `papers/dashboard.json`.
3. Inspect the latest commits after this checkpoint before assuming any paper status.
4. Preserve the Research Command Center UI invariants above.
5. Continue genuine Active work first. Current completion-first dispatch is **015 first**, while **003** is also genuinely Active.
6. Before intentionally switching papers, checkpoint the bounded work unit and synchronize that paper's handoff.
7. Use visible author name **Cochrane Kang** only.

## Deletion-safety statement

At the time this checkpoint was created, the useful recoverable state of this controller conversation had been distilled into Git. The original chat is not required to recover the current portfolio, UI rules, scheduling model, or per-paper handoff state.
