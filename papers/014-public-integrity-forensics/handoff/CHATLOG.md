# ARIS4C014 · Research conversation log

Public-safe record of material human ↔ ChatGPT / external-agent conversations. This is **not** hidden chain-of-thought and must not contain secrets.

## 2026-09-19 · Historical bootstrap distilled from surviving ARIS4C context

- **Surface:** ChatGPT / ARIS4C project conversations
- **Participants:** Cochrane Kang + AI research assistants
- **Research thread:** Reuse the research-forensics architecture for public-integrity/corruption-risk screening across government, hospitals, SOEs, research institutes, universities, NGOs/social organizations, and suppliers, with strong China-web coverage and human-review safeguards.
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


## 2026-09-19 · Institution-universe expansion and repository split

- **Surface:** ChatGPT / ARIS4C014
- **Participants:** Cochrane Kang + ChatGPT
- **Question:** Whether additional institution types should be added to the China public-integrity universe, and whether the growing agent belongs inside ARIS4C, repo-auditor, or a separate repository.
- **Institution design result:** Move toward a two-axis ontology: legal/organizational identity × functional domain. Important additions include rural collective economic organizations, local SOEs/LGFVs, government investment/guidance funds, primary/secondary/vocational education, professional intermediaries, public utilities/urban operations, and research peripheral/commercialization entities.
- **Repository result:** ARIS4C014 remains the scientific parent; OpenIntegrity should become a standalone reusable implementation; repo-auditor remains the independent quality/safety/release auditor.
- **Important constraint:** Do not interpret institution category, ownership type, public-office status, NGO mission, religion, advocacy, nationality or foreign links as corruption evidence.
- **Persistence action:** Added `process/CHINA_INSTITUTION_ONTOLOGY.md` and `process/REPOSITORY_ARCHITECTURE.md`; updated handoff state so this chat can be deleted without losing the decision.
