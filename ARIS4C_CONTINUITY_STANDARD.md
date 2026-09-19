# ARIS4C Research Continuity & Agent Handoff Standard · v1

**Effective:** 2026-09-19  
**Owner:** Cochrane Kang  
**Scope:** every numbered ARIS4C paper project, regardless of maturity

ARIS4C treats the Git repository as the canonical cross-session, cross-device, cross-account, and cross-agent source of truth. A paper is not operationally reproducible if a new collaborator or AI agent can see the manuscript but cannot reconstruct the current state, pending work, important decisions, and the conversation context that produced them.

## 1. Required handoff package

Every `papers/NNN-*/` project must contain:

```
handoff/
  README.md
  STATUS.md
  TODO.md
  DECISIONS.md
  CONTEXT.md
  CHATLOG.md
  AGENT_HANDOFF.md
  SESSION_LOG.md
```

### README.md
The first file a new human or agent reads. It explains the read order, canonical sources, and which handoff files are machine-maintained versus append-only.

### STATUS.md
A current machine-readable/human-readable snapshot of:
- ARIS4C activity state;
- portfolio progress;
- current research stage;
- evidence already established;
- current next gate;
- current blocker.

Canonical state comes from `paper.json` plus `papers/dashboard.json`.

### TODO.md
The actionable queue. It should distinguish:
- P0: next scientific/review gate;
- P1: enabling work and blocker removal;
- P2: packaging, polish, or optional extensions.

Completed items should be checked rather than silently deleted when they explain project history.

### DECISIONS.md
An append-oriented decision log recording:
- what was decided;
- why;
- rejected alternatives when material;
- which evidence or conversation caused the decision;
- affected files/commits when known.

### CONTEXT.md
The compact research context required for a cold start: research question, scope, construct boundaries, key datasets/methods, terminology, and canonical files.

### CHATLOG.md
A **public-safe research conversation record** covering material ChatGPT / human / external-agent exchanges. It should preserve:
- date/session;
- surface or agent when known;
- user request or research question;
- concise summary of the exchange;
- important user corrections/instructions;
- resulting decision or repository change;
- links to files/commits when known.

It is not a dump of hidden chain-of-thought. Do not commit API keys, credentials, private personal data, confidential third-party material, or other secrets. Verbatim excerpts are optional; concise faithful summaries are preferred when the repository is public.

### AGENT_HANDOFF.md
A cold-start takeover brief. A different ChatGPT account, computer, Codex/WorkBuddy/Qoder-like agent, or human collaborator should be able to read it and continue without reconstructing the project from chat history.

It must say:
- what the project is;
- what is already done;
- what is not done;
- the immediate next action;
- current blockers/gates;
- canonical files;
- important “do not” constraints;
- how to record the next session.

### SESSION_LOG.md
An append-oriented execution log. Each substantial work session should record:
- date;
- executor/surface;
- work performed;
- validation/tests;
- commits or artifacts;
- remaining work.

## 2. Cold-start takeover protocol

A new executor should read, in order:

1. `handoff/README.md`
2. `handoff/AGENT_HANDOFF.md`
3. `handoff/STATUS.md`
4. `handoff/TODO.md`
5. `handoff/DECISIONS.md`
6. `handoff/CHATLOG.md`
7. project-specific process/manuscript/data/code files referenced above

The handoff package is a bridge, not a substitute for scientific source files.

## 3. Canonical-source rule

There is only one canonical research truth per project.

- Scientific metadata: `paper.json`
- Portfolio state: `papers/dashboard.json`
- Study-specific status/design: project `process/` files
- Cross-agent continuity: project `handoff/`
- Manuscript/evidence/code: their project-native locations

The handoff package must summarize these sources, not create an independent contradictory state.

## 4. Update rule

After any material interaction that changes research direction, design, status, gate, blocker, interpretation, output requirements, or next actions:

- update canonical project files first;
- synchronize `STATUS.md` / `AGENT_HANDOFF.md` when state changed;
- append the relevant decision to `DECISIONS.md`;
- append a public-safe conversation record to `CHATLOG.md`;
- update `TODO.md`;
- append the execution result to `SESSION_LOG.md`.

Minor wording edits need not create chat-log noise.

## 5. Continuity gate

Every ARIS4C paper, including early-stage papers, must pass the continuity audit. A project missing any required handoff file is **continuity-incomplete**.

Submission-ready/final projects must additionally have:
- no stale P0 item contradicting the declared final state;
- a handoff that explains any author-only submission step;
- session/history records sufficient to explain the final repository state.

## 6. Historical backfill

For projects created before this standard, exact historical chat transcripts may be unavailable. They should receive a clearly labeled **bootstrap distilled history** based on the surviving conversation/project record. From adoption onward, material conversations must be logged prospectively.

## 7. Public-repository safety

Because ARIS4C is public, continuity must never override security or privacy:
- no credentials or API keys;
- no private tokens or cookies;
- no hidden model chain-of-thought;
- no unnecessary personally identifying or sensitive data;
- no copyrighted full-text material that cannot legally be redistributed.

When raw conversation export is unsuitable for a public repository, preserve a faithful research-relevant summary instead.
