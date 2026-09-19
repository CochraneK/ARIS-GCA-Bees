# ARIS4C006 · Research conversation log

Public-safe record of material human ↔ ChatGPT / external-agent conversations. This is **not** hidden chain-of-thought and must not contain secrets.

## 2026-09-19 · Historical bootstrap distilled from surviving ARIS4C context

- **Surface:** ChatGPT / ARIS4C project conversations
- **Participants:** Cochrane Kang + AI research assistants
- **Research thread:** Test surname/alphabetical-exposure effects in China with detailed Chinese-name validation, field-aware alphabetical-authorship regimes, and longitudinal scholarly-credit outcomes.
- **User operating preference:** Continue in GO mode when requirements are clear; persist important state to Git rather than relying on chat memory alone.
- **Outcome:** The current repository state, process files, dashboard state, and handoff package are treated as the recoverable source of truth.
- **Backfill limitation:** Earlier chats are summarized rather than reproduced verbatim where a complete export is unavailable.

### Prospective logging rule

For every future material conversation, append:
- date/session and agent/surface;
- the research question or requested change;
- concise faithful summary;
- important user correction/constraint;
- decision/result;
- affected files/commits where known.

## 2026-09-19 · ChatGPT session — ARIS4C006 design-to-analysis handoff checkpoint

- **Surface:** ChatGPT ARIS4C006 project chat.
- **Participants:** Cochrane Kang + ChatGPT.
- **User instruction:** Run the idea through ARIS in GO mode, keep advancing with minimal confirmation, persist state to Git, and before deleting the chat read Git first and synchronize all useful information.
- **Research evolution in this chat:** China-only surname/name-letter idea → population-corrected alphabetical-authorship mechanism → measured field/source regimes → Crossref structured surname validation → OpenAlex identity canonicalization → all-field primary-topic scope → conservative field-level lagged exposure → exact leave-one-author-out exposure → entry-based longitudinal design.
- **Important corrections made during the chat:** rejected uniform A–Z null; rejected raw source-level exposure as primary after poor split-half rank reliability; changed primary field assignment from multi-topic `topics.field.id` to unique `primary_topic.field.id`; prohibited last-token surname heuristic; separated CN affiliation from nationality/ethnicity; replaced raw work author IDs with canonical OpenAlex author IDs for longitudinal joins.
- **Repository reconciliation at deletion checkpoint:** Git is ahead of the conversational state. Canonical Git shows all outcome-blind gates passed, preregistration lock/unlock committed, H1/H2 opened, H1 robustness passed, and H3 entry-cohort structural materialization as the current remaining confirmatory gate.
- **H1:** beta +0.6479808, SE 0.1228913, 95% CI [0.4071182, 0.8888434], p 1.3436e-07.
- **H2 raw:** beta -0.6280066, SE 0.1408537, 95% CI [-0.9040748, -0.3519384], p 8.2507e-06; Holm adjustment awaits H3.
- **Deletion rule:** after this handoff synchronization is verified in Git, this chat can be deleted without losing the canonical research state.
