# ARIS4C002 · Research conversation log

Public-safe record of material human ↔ ChatGPT / external-agent conversations. This is **not** hidden chain-of-thought and must not contain secrets.

## 2026-09-19 · Historical bootstrap distilled from surviving ARIS4C context

- **Surface:** ChatGPT / ARIS4C project conversations
- **Participants:** Cochrane Kang + AI research assistants
- **Research thread:** Develop the language-periodic-table idea as a falsifiable predictive geometry test rather than a metaphor. Stress-test a global circular model against non-circular alternatives, preserve bounded claims, add bilingual delivery, richer figures, and PDF-first public output.
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


## 2026-09-19 · Paper 002 continuation, figure visibility, CI repair, and deletion handoff

- **Surface:** ChatGPT / ARIS4C Paper 002 thread
- **Participants:** Cochrane Kang + ChatGPT
- **Request sequence:** continue Paper 002; clarify why the manuscript/page appeared to have no figures; repair a failing `Paper 002 manuscript CI / manuscript-smoke`; persist all useful state to Git before deleting the chat.
- **Key correction from user:** figures must be visible in the actual manuscript/public reading surface, not merely stored in `figures/` or a separate landing page.
- **Actions/results:** 002 status was aligned to 100% repository-output completion; public EN/ZH visual pages were added/routed; figures were embedded into both manuscripts; the later canonical visual narrative was expanded/renumbered to six figures; the manifest CI failure was traced to the new `submission-ready-author-metadata-pending` status and the workflow was fixed to accept it.
- **Validation:** Paper 002 manuscript CI run #114 (`35422718503`) on commit `99568d00...` succeeded for the six-figure repository state. During this deletion checkpoint, CI was further hardened to validate the six current canonical figure files and the EN/ZH reference order instead of only checking legacy three-figure output names.
- **Important packaging caveat found at handoff:** the recorded Linguistic Typology `TECHNICAL_SUBMISSION_PACKAGE_PASS` belongs to build commit `608bc871...` and a 3-figure package. Canonical manuscripts now contain 6 figures; rebuild/re-QA the journal package before ScholarOne.
- **Scientific boundary:** no scientific reopening is required; do not infer universal tree ontology or falsification of every possible periodicity.
