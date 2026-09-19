# ARIS4C002 · TODO

## P0 · Next gate

- [ ] Rebuild the Linguistic Typology submission package from the current six-figure canonical manuscript.
- [ ] Repeat technical/visual/anonymisation QA and record the new workflow run, build commit, artifact ID/digest, page count, and six uploaded figures.
- [ ] Confirm author metadata/declarations required by the journal.
- [ ] Submit through ScholarOne.

## P1 · Reproducibility / consistency

- [ ] Upgrade `code/make_manuscript_figures.py` from the legacy three-core-plot renderer to a complete deterministic six-figure renderer. Until then, CI treats it only as a source-data smoke test and separately checks the six committed canonical figures.
- [ ] Keep `STATUS.md`, `AGENT_HANDOFF.md`, `paper.json`, dashboard metadata, and submission QA synchronized after the package refresh.

## P2 · Optional scientific extensions — do not fold into Paper 002 post hoc

- [ ] Optional 50–100 family-held-out splits.
- [ ] Optional phylogenetic/spatiophylogenetic sensitivity.
- [ ] Optional permutation/p-value supplement.
- [ ] Treat torus/multi-cycle/multi-level/local periodicity as a new hypothesis/paper unless a new review cycle explicitly reopens 002.
