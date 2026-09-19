# ARIS4C014 · TODO

## P0 · Next gate

- [ ] Bootstrap a standalone `OpenIntegrity` repository from the reusable ARIS4C014 implementation.
- [ ] Migrate reusable core, China adapters, identity resolver, graph, detectors, tests and relevant workflows without changing scientific semantics.
- [ ] Verify parity under CI before deleting or delegating any working ARIS4C014 implementation.
- [x] Implement and CI-validate the exact-stable-ID enrichment layer: exact CN-USCC may auto-attach allowlisted factual attributes; name-only matches route to review; same-name disjoint IDs become conflicts; inaccessible sources remain coverage gaps.
- [ ] Run the first bounded **real second-source** enrichment with an official/public source that exposes exact CN-USCC without bypassing CAPTCHA/authentication/access controls.

## P1 · China institution universe

- [ ] Implement the two-axis legal-identity × functional-domain model from `process/CHINA_INSTITUTION_ONTOLOGY.md`.
- [ ] Add authoritative university universe / stable school identifiers.
- [ ] Add hospital / medical-institution universe coverage, preserving subset-vs-universe semantics.
- [ ] Add social-organization / charity stable-ID coverage.
- [ ] Add local SOE / LGFV coverage.
- [ ] Add rural collective economic organizations.
- [ ] Add government investment / guidance funds.
- [ ] Add primary/secondary/vocational education.
- [ ] Add professional intermediary nodes.
- [ ] Add research peripheral / commercialization entities.
- [ ] **Resolve coverage blocker conservatively:** unavailable sources remain explicit coverage gaps / ABSTAIN; do not bypass CAPTCHAs, authentication or anti-automation controls.

## P1 · Cross-source evidence

- [ ] Implement National Public Resource Trading Platform federation / selected provincial adapters.
- [ ] Enrich exact CN-USCC supplier identities from lawful official/public corporate sources.
- [ ] Add audit / discipline / administrative / judicial outcome adapters with distinct outcome classes.
- [ ] Add research grant / patent / technology-transfer edges and delegate publication forensics to ARIS4C011.
- [ ] Freeze China Pilot 1 as a stratified cross-institution dataset focused on coverage, joinability, parser misses and identity resolution—not targeting “suspicious” people.

## P1 · Repository separation

- [ ] Keep ARIS4C014 as scientific source of truth for papers, pilots, protocols and frozen results.
- [ ] Add reciprocal links between ARIS4C014 and OpenIntegrity after repository creation.
- [ ] Run repo-auditor against OpenIntegrity after extraction.
- [ ] Do not merge OpenIntegrity into repo-auditor.

## P2 · Continuity / packaging

- [ ] Keep `STATUS.md`, `AGENT_HANDOFF.md`, `DECISIONS.md`, `CHATLOG.md` and `SESSION_LOG.md` synchronized after material changes.
- [ ] Keep public outputs, figures/tables, bilingual delivery and repository links consistent with the ARIS4C output standard.
