# ARIS4C012 · Research conversation log

Public-safe record of material human ↔ ChatGPT / external-agent conversations. This is **not** hidden chain-of-thought and must not contain secrets.

## 2026-09-19 · Historical bootstrap distilled from surviving ARIS4C context

- **Surface:** ChatGPT / ARIS4C project conversations
- **Participants:** Cochrane Kang + AI research assistants
- **Research thread:** Investigate when interventions generate their functional opposite across domains, using an indexed falsification-first causal-inversion framework rather than a loose collection of paradoxes.
- **User operating preference:** Continue in GO mode when requirements are clear; persist important state to Git rather than relying on chat memory alone.
- **Outcome:** The repository state, process files, dashboard state, and handoff package are treated as the recoverable source of truth.
- **Backfill limitation:** Earlier chats are summarized rather than reproduced verbatim where a complete export is unavailable.

## 2026-09-19 · Current chat deletion checkpoint

- **Surface:** ChatGPT, ARIS4C012 thread
- **Participants:** Cochrane Kang + ChatGPT, with an external WorkBuddy run used for independent Coder B
- **Original motivating question:** how to scientifically analyze slogans such as “war is peace,” “freedom is slavery,” and “ignorance is strength” without treating literal contradictions as empirical truths.
- **Core reframing:** replace literal `X = not-X` with indexed causal relations such as `X[a,l,t,d,e] -> mechanism/feedback -> O(X)[a',l',t',d',e']`.
- **Functional-opposition rule:** an opposite must be prespecified through a validated bipolar construct, formal complement, domain theory, or independent coding; lexical antonymy alone is insufficient.
- **Pilot 0A:** completed on 30 records across six strata; useful mainly as a feasibility/discriminant test rather than prevalence estimation.
- **Retrieval:** v0.1 exposed semantic contamination and was preserved; v0.2 added prospective type/title topical gates and produced 165 reproducible candidates from 1,800 raw hits, with 1,375 transparent rejections.
- **Novelty audit:** broad novelty failed. OCI cannot claim to discover unintended consequences or cross-domain backfire. Remaining possible novelty is a validated indexed representation for a restricted functional-opposite class.
- **Manuscript:** theory/methods draft and working references exist.
- **Schema concern identified before viewing B labels:** v1 mixed index-switch dimensions with generative mechanisms; `SCHEMA_V2_PROPOSAL.md` was created as a post-Gate-B redesign proposal.
- **WorkBuddy handoff history:** an earlier WorkBuddy run had completed ARIS4C003 rather than 012, so a 012-only handoff was created. A later isolated WorkBuddy run correctly completed ARIS4C012 Coder B.
- **Coder B provenance:** commit `8f9ec0dd99e25ae0411fd4e06d2b4dbd1ef219d9`; all P01–P30 core fields completed; commit states forbidden Coder A materials were not opened.
- **Raw reliability:** opposition_valid raw agreement 0.767 / kappa 0.466; OCI candidacy 0.833 / kappa 0.592; primary mechanism raw agreement 0 / kappa 0; 141 disagreement cells.
- **Critical diagnostic:** several apparent disagreements are vocabulary/encoding mismatches (e.g. `meta-analysis` vs `meta_analysis`, `level-switch/interdependence` vs `level_switch`) in addition to genuine conceptual disagreements.
- **Scientific decision:** v1 does not pass the frozen reliability gate. Preserve raw reliability unchanged; use adjudication diagnostically; freeze a controlled-vocabulary v2 and validate on a fresh independent sample before full evidence-map screening.
- **Deletion/recovery rule:** after this chat is deleted, resume from `handoff/AGENT_HANDOFF.md` and `process/STATUS.md`; no key project state should depend on this conversation.

### Prospective logging rule

For every future material conversation, append:
- date/session and agent/surface;
- the research question or requested change;
- concise faithful summary;
- important user correction/constraint;
- decision/result;
- affected files/commits where known.

## 2026-09-19 · 000 controller continuation

- **Surface:** ARIS4C 000 controller / ChatGPT.
- **User instruction:** continue work not already being run by the other ARIS4C controller threads, then keep going.
- **Work taken:** ARIS4C012 because active 003/007/011/014 work was avoided.
- **Completed:** exhaustive 141-cell v1 disagreement diagnosis; frozen controlled-vocabulary Schema v2; fresh deterministic 30-record validation draw; immutable blind evidence materialization; evidence-availability Amendments 01 and 02; final 30/30 abstract-level blind packet; coder freeze/reliability tooling and CI independence guards.
- **Scientific constraint preserved:** raw v1 reliability was never rewritten; sample replacement happened before new labels existed and used only same-stratum deterministic order plus evidence availability.
- **Current result:** A2 and B2 have byte-identical final input bundle SHA-256 `9f0d8b785b8f8f739cdd41cf7c6f9f6fc3f7fbdf2299587cbab6d732bdddfc51`.
- **Gate:** current controller cannot impersonate two independent coders. Resume 012 only when genuinely independent A2/B2 execution surfaces are available; otherwise portfolio scheduling should move to another executable paper.
