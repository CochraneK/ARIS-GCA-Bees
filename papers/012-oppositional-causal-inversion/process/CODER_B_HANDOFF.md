# CODER B BLIND HANDOFF — ARIS4C012

## Independence rule

You are the independent second coder for a 30-paper construct-validation pilot.

**Do not read:**
- `data/pilot0_coderA_feasibility.csv`
- `process/PILOT0A_AUDIT.md`
- any adjudication or Coder A output.

Use only:
- `process/CONCEPT_SCHEMA.md`
- `process/SEARCH_PROTOCOL.md`
- `data/pilot0_coderB_blind.csv`
- the original paper/abstract/full text needed to judge each record.

## Task

For each record, independently code:

1. source_verified
2. screen_stage1
3. opposition_valid
4. opposition_rationale
5. x_construct
6. opposite_construct
7. actor_switch
8. level_switch
9. time_switch
10. construct_switch
11. environment_switch
12. feedback
13. nonlinearity
14. selection_filtering
15. power_asymmetry
16. primary_mechanism
17. study_design
18. evidence_mode
19. evidence_tier
20. causal_claim_strength
21. result_support
22. mediator
23. moderator
24. boundary_conditions
25. counterevidence
26. oci_candidate
27. exclusion_reason
28. notes

## Critical anti-bias rules

- Do not infer that a paper is OCI-positive because its title contains "paradox", "backfire", or "boomerang".
- Do not infer that it is OCI-negative because the reported focal effect is null.
- `oci_candidate` asks whether the paper tests/formalizes a relation that fits the schema.
- `result_support` asks whether its evidence supports that reversal.
- A null paper can therefore be an OCI candidate.
- A famous paradox can fail the strict OCI definition.
- Define the functional opposite before using the result direction to justify it.
- Treat rhetorical/literary similarity as zero evidence.
- Keep political cases descriptive and causal; do not code normative approval/disapproval as evidence.

## Output

Write only into `data/pilot0_coderB_blind.csv`.

After all 30 records are coded, compute no agreement yourself. The adjudication stage will compare A and B only after both are frozen.
