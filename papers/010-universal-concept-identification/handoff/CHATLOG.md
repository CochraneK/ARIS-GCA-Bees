# ARIS4C010 · Research conversation log

Public-safe record of material human ↔ ChatGPT / external-agent conversations. This is **not** hidden chain-of-thought and must not contain secrets.

## 2026-09-19 · Historical bootstrap distilled from surviving ARIS4C context

- **Surface:** ChatGPT / ARIS4C project conversations
- **Participants:** Cochrane Kang + AI research assistants
- **Research thread:** Generalize Twenty Questions into universal concept identification under finite query budgets, including ambiguity, negation, paradox, ineffability, and alternative semantic response protocols.
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


## 2026-09-19 · Deletion checkpoint · full 010 thread distilled

- **Surface:** ChatGPT / ARIS4C010
- **Participants:** Cochrane Kang + ChatGPT
- **Initial idea:** Can a finite-question system identify any word/concept efficiently, and does that require a taxonomy of all concepts, including negation, paradox and ineffable concepts?
- **Major conceptual correction:** A single universal taxonomy tree is not required. The formal requirement is a separating query family relative to a defined candidate universe; a multi-axis typed representation is more appropriate for cross-cutting semantic phenomena.
- **Core metric adopted:** Semantic Query Overhead = extra identification cost imposed by semantically admissible questions relative to unrestricted partitions.
- **Formal boundaries distinguished:** finite closed world, infinite candidate universes, open-world/OOS targets, context dependence, empirical unknowns, undecidability and strong ineffability.
- **Pilot progression:** combinatorial Pilot 0 → constructed semantic Pilot 1 → source-derived OEWN Pilot 2.
- **Pilot 2 exploratory estimate:** 15 OEWN senses; semantic optimal expected cost 4.2667 vs unrestricted Huffman 3.9333, yielding +0.3333 expected questions; semantic worst case 6 vs unrestricted 4, yielding +2.
- **Source/data discipline:** OEWN 2025 pinned; source-native assertions kept separate from UCID mappings; constructed/model labels never treated as gold.
- **Calibration design:** 60 OEWN noun senses (10 polysemous lemmas × 6 senses), 24 mixed stress scenarios, leakage-aware grouped design, covert retests, adjudication policy and staged precision plan.
- **Novelty narrowing:** Test Cover, GBS, REG, description-logic active learning, RSA/reference games, adaptive elicitation, ontology-guided active querying and open-world active learning are baselines/ancestors.
- **2026 collision:** ICAART 2026 already combines rooted ontology + semantic retrieval + binary active querying + Bayesian refinement, so “ontology-guided active questioning” is not a novelty claim.
- **P3 addition:** Because coarse YES/NO/MAYBE-style answers already exist in prior art, the study now compares P2 = YES/NO, P3 = YES/NO/MAYBE, and P6 = fine semantic states. The key mechanism test is P3→P6.
- **Human-study rule:** LLM/synthetic/model answers cannot substitute for real human semantic calibration.
- **Current state:** engineering is human-calibration-ready; the meaningful next step is ethics/recruitment setup and Stage-A real human P2/P3/P6 data.
- **User workflow requirement reaffirmed:** important state must live in Git so the chat can be deleted and work can resume from repository state alone.
