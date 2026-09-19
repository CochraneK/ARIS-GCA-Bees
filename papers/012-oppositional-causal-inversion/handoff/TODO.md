# ARIS4C012 · TODO

## P0 · Current scientific gate

- [x] Complete genuinely independent WorkBuddy Coder B on P01–P30.
- [x] Generate raw agreement / Cohen kappa / Krippendorff alpha and disagreement packet.
- [x] Diagnose all 141 disagreement cells by:
  - lexical/token-vocabulary mismatch;
  - overlapping v1 categories;
  - genuine conceptual disagreement;
  - source/metadata disagreement.
- [x] Preserve raw v1 reliability outputs unchanged.
- [x] Convert `SCHEMA_V2_PROPOSAL.md` into a frozen controlled-vocabulary v2 coding specification (`process/SCHEMA_V2_FROZEN.md` + freeze JSON + blank coding template).
- [x] Draw and freeze a fresh 30-record balanced validation sample (5 per stratum; zero Pilot 0B overlap).
- [x] Materialize and freeze the final blind v2 evidence bundle. The initial packet had 24/30 abstract excerpts; evidence-only Amendment 01 recovered 0/6; frozen Amendment 02 deterministically replaced the six unavailable slots within the same strata, yielding 30/30 abstract excerpts. Final A2/B2 input bundle SHA-256: `9f0d8b785b8f8f739cdd41cf7c6f9f6fc3f7fbdf2299587cbab6d732bdddfc51`.
- [ ] Run **genuinely independent** A2 and B2 on separate isolated execution surfaces using `A2_INPUT_AMENDMENT_02_FREEZE.json` / `B2_INPUT_AMENDMENT_02_FREEZE.json`; the current controller must not count itself twice.
- [ ] Freeze each completed coder file separately with `freeze_v2_coder.py`; integrate labels only after both completion freezes exist.
- [ ] Run `score_v2_agreement.py` and require the frozen v2 reliability gate to pass before full evidence-map screening.
- [ ] Require revised reliability to pass before full evidence-map screening (remains locked).

## P1 · Evidence-map expansion after schema validation

- [ ] Screen the 165-record reproducible frame only after a reliable schema exists.
- [ ] Target-expand underrepresented query families:
  - public information / welfare / coordination;
  - control / optimization / fragility;
  - Goodhart / proxy failure;
  - generic intervention backfire beyond iatrogenic care;
  - autonomy / dependence / delegation;
  - safe-development analogues.
- [ ] Add backward/forward citation chasing and historical terminology.
- [ ] Keep retrieval frequency distinct from phenomenon prevalence.

## P2 · Manuscript

- [ ] Update Results with validated reliability only after v2 Pilot.
- [ ] Keep novelty claim narrow: indexed representation, not a universal theory of backfire.
- [ ] Finish English full paper.
- [ ] Produce Chinese full paper.
- [ ] Add evidence-traceable figures/tables under ARIS4C output standard.

## Continuity

- [ ] After each material session, synchronize `process/STATUS.md`, this TODO, `DECISIONS.md`, `CHATLOG.md`, and `SESSION_LOG.md`.
