# ARIS4C016 Delete-Safe Checkpoint

Date: 2026-09-19

Purpose: preserve the useful state of the ChatGPT conversation before the user
deletes the chat. **Git is canonical.**

## Confirmation scope

The current conversation's scientifically useful decisions and results have
been persisted to the repository.

Most important current state:
- ARIS route confirmed; full ARIS completion is not required to count as having
  followed the ARIS route;
- Phase 0 bilingual working paper;
- portfolio maturity: 68% / block;
- semantic ontology gate frozen at 300 deterministic rows;
- frozen audit manifest SHA-256:
  `48c58f91901e8c2a1aab01958e95ea28afaf0f33e7a98677f98e58b8a412c9b4`;
- English repeated-item FWL model and filler negative control complete;
- community effects are not yet demonstrably taboo-specific;
- pronunciation engineering route complete for all 13 project languages;
- full technical pronunciation result:
  **8,187 / 8,190 = 99.9634%**;
- Epitran 1.35.2 and Flite source commit
  `6c9f20dc915b17f5619340069889db0aa007fcdc` frozen;
- technical pronunciation success must not be confused with pronunciation
  validity;
- confirmatory semantic inference still requires independent Coder A/B +
  native-language review;
- confirmatory phonology still requires pronunciation-validity review, matched
  neutral controls and frozen segment/approximant coding.

## Recovery order for a new chat / agent

Read:
1. `process/STATUS.md`
2. `process/HANDOFF.md`
3. `process/CHATLOG_SUMMARY.md`
4. `paper.json`
5. `manuscript/DRAFT.md`
6. `manuscript/DRAFT.zh-CN.md`
7. `process/CODER_HANDOFF.md`
8. `process/AUDIT_SAMPLE_FREEZE.md`
9. `process/G2P_FULL_ROUTE_AUDIT.md`
10. `data/phonology_runtime_lock.json`

Then continue from the two external validity gates rather than re-deriving the
project from chat history.

## Delete safety

No unique project decision from this conversation is intentionally left only
in chat. The raw private coder sheets have not been generated/committed, by
design; their generator and protocol are in Git.

Deleting this chat should therefore not remove the canonical ARIS4C016 project
state.
