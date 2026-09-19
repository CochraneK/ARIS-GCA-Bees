# ARIS4C015 · Research conversation log

Public-safe record of material human ↔ ChatGPT / external-agent conversations. This is **not** hidden chain-of-thought and must not contain secrets.

## 2026-09-19 · Historical bootstrap distilled from surviving ARIS4C context

- **Surface:** ChatGPT / ARIS4C project conversations
- **Participants:** Cochrane Kang + AI research assistants
- **Research thread:** Reuse the research-forensics architecture to discover sleeping-beauty science, keeping retrospective identification, mechanism analysis, and time-safe prospective rediscovery as separate tracks.
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

## 2026-09-19 · Pilot-M risk-set common-support hardening

- **Surface:** ChatGPT ARIS4C 000 controller + GitHub Actions.
- **User request:** Continue advancing the project in GO mode.
- **Work performed:** expanded Pilot-M control acquisition, identified the
  non-nested OpenAlex sample-size problem, implemented deterministic multi-seed
  reservoirs, corrected incidence-density control reuse, compared 1:1 and 1:4
  risk-set matching, froze the primary case set to the three literature-known
  SBs, and added offline artifact reanalysis.
- **Key result:** the frozen 3-case 1:1 comparison matches all cases but still
  has max abs SMD 1.633; 1:4 worsens to 2.417. Common-support diagnostics show
  the strongest shortage in the Washburn 1921 stratum.
- **Constraint preserved:** abs SMD < 0.10 was not relaxed and substantive
  mechanism regression remains blocked.
- **Additional validation:** publisher identity and independent evidence of
  later use were cross-checked for two provisional candidates, but their
  annual trajectories / Beauty Coefficients remain unvalidated.
- **Operational result:** the live v8 reacquisition hit an OpenAlex HTTP 429
  rate limit; saved-artifact analysis continues without API calls.
