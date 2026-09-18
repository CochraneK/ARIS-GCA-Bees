# OpenIntegrity Agent Skill

This directory is the portable Agent Skill surface for ARIS4C014.

It inherits the evidence-first design of ARIS4C011 Research Forensics and adapts it to public-integrity/open-data review.

## Entry point

Read `SKILL.md`.

## Guarantees

- missing coverage -> ABSTAIN, not PASS;
- no automatic corruption verdict;
- no name-only high-priority person match;
- temporal leakage controls for historical evaluation;
- source-level provenance and benign explanations;
- E5-only evidence cannot create HIGH priority.

## Reference implementation

The executable prototype currently lives in `../../../code/`.

The Agent Skill schemas in `assets/` define portable finding/report outputs independent of any specific LLM or orchestration platform.
