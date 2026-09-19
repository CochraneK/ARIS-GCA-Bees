# ARIS4C014 · Current status

- **Title:** Public Integrity Forensics: An Auditable Multi-Source Agent for Corruption-Risk Screening from Open Data
- **Project status:** china-pilot1-exact-uscc-enrichment-contract-validated
- **Activity:** active
- **Portfolio progress:** 71%
- **Current stage:** China Pilot 1 · exact-USCC cross-source enrichment contract validated
- **Evidence established:** CCGP/CAS/USCC graph + stable-ID-only resolver now extended with a tested cross-source enrichment contract: only exact valid CN-USCC equality can auto-attach allowlisted factual registry attributes; name-only matches are REVIEW_CANDIDATE, same-name disjoint IDs are conflicts, interactive/unavailable sources are COVERAGE_GAP, sensitive contact fields are not propagated, and corruption_inference remains false. ARIS4C014 CI runs 118–119 PASS.
- **Next gate:** Implement the first lawful second-source organization adapter that exposes exact CN-USCC without bypassing interactive/CAPTCHA controls; run a bounded joinability enrichment and report exact-ID matches, review candidates, conflicts and coverage gaps.
- **Blocker:** No architecture blocker. The primary constraint is lawful machine-readable access to authoritative second-source stable identifiers; interactive/CAPTCHA-protected registries must remain explicit coverage gaps rather than being bypassed.

## Source of truth

This snapshot is synchronized from `paper.json` and `papers/dashboard.json`. Study-specific `process/` files may contain finer-grained status and frozen design details.
