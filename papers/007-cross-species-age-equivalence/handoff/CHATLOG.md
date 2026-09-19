# ARIS4C007 · Research conversation log

Public-safe record of material human ↔ ChatGPT / external-agent conversations. This is **not** hidden chain-of-thought and must not contain secrets.

## 2026-09-19 · Historical bootstrap distilled from surviving ARIS4C context

- **Surface:** ChatGPT / ARIS4C project conversations
- **Participants:** Cochrane Kang + AI research assistants
- **Research thread:** Build a scientifically benchmarked animal-age equivalence framework rather than a single lifespan ratio, comparing life-history, demographic/event, and molecular/epigenetic axes across species.
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

## 2026-09-19 · Pilot 3 molecular continuation and deletion handoff

- **Surface:** ChatGPT / ARIS4C project conversation
- **Participants:** Cochrane Kang + ChatGPT
- **User direction:** Continue ARIS4C007 in GO mode; before deleting the chat, read the latest Git state, persist all useful current information back to Git, and only then confirm deletion is safe.
- **Work completed in conversation:** advanced from Pilot 3A reference parity through Pilot 3B metadata/holdout freeze; designed and implemented Pilot 3C smoke/full molecular workflows; separated methylation linear predictors from life-history inverse transforms; froze trait-vintage sensitivity and Pilot 4 phylogenetic design.
- **Important correction:** smoke size is 10 samples across 6 species, not 12, because two eligible holdout species contribute only one sample each.
- **Important implementation decision:** MMC v3.0.0 is canonical for Universal Clock 2/3; MammalMethylClock v1.1.0 Clock-3 inverse wrapper is not canonical.
- **Important independence constraint:** 50-sample primary molecular holdout contains only samples explicitly marked not used in pan-mammalian-clock training.
- **Latest engineering finding:** run `35424097947` downloaded all 20 smoke IDATs but failed because CRLF in the TSV manifest contaminated Bash filenames with a trailing carriage return.
- **Fix committed:** LF-only TSV manifests + defensive R `trimws()` filename handling.
- **Continuation pointer:** inspect run `35433019496` first; if PASS, verify the automatic 50-sample full workflow; if FAIL, debug only the newly exposed layer.
- **Persistence outcome:** canonical metadata, process status, decisions, TODO, context, chat log and session log were synchronized to Git so this chat is not required for recovery.
