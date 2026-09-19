#!/usr/bin/env python3
"""Create and synchronize the ARIS4C per-paper continuity / handoff package."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT / "papers"
DASHBOARD = PAPERS / "dashboard.json"

BOOTSTRAP_CHAT = {
    "001": "Rebuild the bee-cognition project as a final ARIS4C paper, separate learning covariance from uncertainty monitoring/metacognition/consciousness claims, finish the submission package, add Chinese full paper and richer figures, then make the public entry PDF-first.",
    "002": "Develop the language-periodic-table idea as a falsifiable predictive geometry test rather than a metaphor. Stress-test a global circular model against non-circular alternatives, preserve bounded claims, add bilingual delivery, richer figures, and PDF-first public output.",
    "003": "Test whether colonial/imperial history predicts present disciplinary advantage across more than sociology/anthropology and more than one ranking metric. Use an outcome-blind design and independent coding before confirmatory analysis.",
    "004": "Model the counterfactual knowledge-network cost of excluding historically realized contributors while keeping mental-health evidence, stigma/discrimination, identity uncertainty, substitution, and retrospective documentation as separate constructs.",
    "005": "Estimate the global scale and downstream cost of bad science, including wasted effort, displaced good research, and buried sleeping-beauty work, while separating confirmed misconduct from broader reliability and research-waste categories.",
    "006": "Test surname/alphabetical-exposure effects in China with detailed Chinese-name validation, field-aware alphabetical-authorship regimes, and longitudinal scholarly-credit outcomes.",
    "007": "Build a scientifically benchmarked animal-age equivalence framework rather than a single lifespan ratio, comparing life-history, demographic/event, and molecular/epigenetic axes across species.",
    "008": "Identify necessary, sufficient, and bottleneck configurations that distinguish human open-ended cumulative intelligence from other animals, using comparative dissociations rather than a vague human-versus-animal score.",
    "009": "Combine computational psychiatry with phenomenology while minimizing distortion of lived psychopathology; explicitly decompose acquisition loss from encoding/modeling loss.",
    "010": "Generalize Twenty Questions into universal concept identification under finite query budgets, including ambiguity, negation, paradox, ineffability, and alternative semantic response protocols.",
    "011": "Create an auditable multi-evidence research-forensics agent/paper integrating statistical, numerical, text, image, citation, provenance, registration, metadata, and corpus-network checks without equating anomalies with misconduct.",
    "012": "Investigate when interventions generate their functional opposite across domains, using an indexed falsification-first causal-inversion framework rather than a loose collection of paradoxes.",
    "013": "Test whether birth timing and death timing are associated using falsification-first calendar/circular models, ordinary seasonality controls, and prespecified cultural/astrological features rather than treating astrology as established.",
    "014": "Reuse the research-forensics architecture for public-integrity/corruption-risk screening across government, hospitals, SOEs, research institutes, universities, NGOs/social organizations, and suppliers, with strong China-web coverage and human-review safeguards.",
    "015": "Reuse the research-forensics architecture to discover sleeping-beauty science, keeping retrospective identification, mechanism analysis, and time-safe prospective rediscovery as separate tracks.",
    "016": "Develop a cross-linguistic grammar/atlas of swearing and taboo language, with an orthogonal ontology, cross-community comparability, genealogy, harmonization, and independent/native-speaker reliability gates.",
}

BOOTSTRAP_DECISIONS = {
    "001": [
        "Treat positive learning covariance as empirical structure but do not equate it with a unitary biological mechanism.",
        "Treat uncertainty-sensitive opt-out behaviour as a separate evidence stream until same-individual coupling is measured.",
        "Public delivery is bilingual and PDF-first; figure count is adaptive rather than fixed."
    ],
    "002": [
        "Operationalize the strong periodic-table claim as a testable global circular geometry and allow it to fail.",
        "Use held-out predictive comparison and direct closure diagnostics; do not infer that tree superiority proves a universal tree ontology.",
        "Public delivery is bilingual and PDF-first; figure order is sequential and the visual narrative is adaptive."
    ],
    "003": ["Broaden disciplines and outcomes beyond a single ranking metric.", "Freeze outcome-blind coding/design before confirmatory outcome analysis."],
    "004": ["Use sign-neutral counterfactual network effects rather than presuming all exclusion has the same consequence.", "Keep mental-health evidence and discrimination/exclusion exposure as distinct variables."],
    "005": ["Separate misconduct, severe reliability failure, publication-process failure, and broader research waste.", "Require genuinely independent adjudication rather than duplicating one model as two reviewers."],
    "006": ["Validate Chinese surname identity/romanization before testing alphabetical exposure.", "Model alphabetical-authorship regime as an exposure context rather than assuming all fields order authors alphabetically."],
    "007": ["Reject one universal animal-year ratio; benchmark multiple biological-age axes.", "Treat species/stage dependence as a result rather than forcing one conversion formula."],
    "008": ["Use orthogonal capability dimensions and dissociation cases instead of a single intelligence score.", "Focus on configurations/bottlenecks enabling open-ended cumulative intelligence."],
    "009": ["Separate acquisition fidelity from encoding/model fidelity.", "Do not treat a computational representation as equivalent to phenomenology merely because prediction is good."],
    "010": ["Treat admissible response semantics as part of query complexity.", "Compare binary and richer semantic protocols rather than assuming MAYBE-like states always help."],
    "011": ["Use applicability-aware detectors and an evidence graph.", "An anomaly is a review lead, not a misconduct verdict."],
    "012": ["Restrict the construct to functional-opposite-producing causal effects.", "Independent construct coding is a hard gate before broad claims."],
    "013": ["Use ordinary seasonal/cultural mechanisms and pseudo-calendar controls before any astrological interpretation.", "Astrological/Bazi features are incremental prespecified predictors, not privileged explanations."],
    "014": ["Treat public-data anomalies as auditable leads, never as corruption findings.", "Prefer authoritative stable identifiers; route name-only entity matches to human review."],
    "015": ["Separate retrospective SB identification, mechanism inference, and prospective rediscovery.", "Do not infer mechanisms when the robust SB case set is empty or unstable."],
    "016": ["Build a multi-axis ontology before global prevalence claims.", "Independent/native-speaker reliability is required before treating community labels as comparable."],
}


def esc_md(value: object) -> str:
    return str(value or "").replace("\n", " ").strip()


def project_rows() -> tuple[list[dict], dict]:
    dashboard = json.loads(DASHBOARD.read_text(encoding="utf-8")) if DASHBOARD.exists() else {"projects": {}}
    rows = []
    for manifest in sorted(PAPERS.glob("[0-9][0-9][0-9]-*/paper.json")):
        p = json.loads(manifest.read_text(encoding="utf-8"))
        d = dashboard.get("projects", {}).get(str(p.get("id")), {})
        rows.append({"manifest": manifest, "paper": p, "dash": d})
    return rows, dashboard


def canonical_links(p: dict, folder: Path) -> list[str]:
    links = p.get("links", {})
    candidates = [
        ("paper.json", "paper.json"),
        ("process/status or plan", links.get("pipeline", "")),
        ("English paper", links.get("paper_en_pdf") or links.get("paper_en_full") or links.get("paper_en", "")),
        ("Chinese paper", links.get("paper_zh_pdf") or links.get("paper_zh_full") or links.get("paper_zh", "")),
        ("source", links.get("source", "")),
    ]
    return [f"- **{label}:** {target}" for label, target in candidates if target]


def write_if_missing(path: Path, content: str) -> bool:
    if path.exists():
        return False
    path.write_text(content.rstrip() + "\n", encoding="utf-8")
    return True


def sync_managed(path: Path, content: str) -> bool:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    new = content.rstrip() + "\n"
    if old == new:
        return False
    path.write_text(new, encoding="utf-8")
    return True


def build_readme(p: dict) -> str:
    pid = p["id"]
    return f"""# ARIS4C{pid} · Continuity / handoff

This directory is the cold-start entry point for a new ChatGPT account, computer, coding/research agent, or human collaborator.

## Read in this order

1. [AGENT_HANDOFF.md](AGENT_HANDOFF.md) — immediate takeover brief
2. [STATUS.md](STATUS.md) — current state/gate/blocker
3. [TODO.md](TODO.md) — actionable queue
4. [DECISIONS.md](DECISIONS.md) — important choices and rejected alternatives
5. [CONTEXT.md](CONTEXT.md) — compact research context
6. [CHATLOG.md](CHATLOG.md) — public-safe record of material conversations
7. [SESSION_LOG.md](SESSION_LOG.md) — execution history

## Canonical rule

The handoff package summarizes the project; it does not replace canonical scientific files. If a handoff statement conflicts with `paper.json`, `papers/dashboard.json`, a frozen preregistration/design file, or machine-readable results, resolve the conflict in favor of the canonical scientific artifact and then update the handoff.

## Maintenance

`README.md`, `STATUS.md`, and `AGENT_HANDOFF.md` are synchronized from canonical metadata. The other files are append-oriented and should preserve meaningful history.

See repository-level `ARIS4C_CONTINUITY_STANDARD.md`.
"""


def build_status(p: dict, d: dict) -> str:
    return f"""# ARIS4C{p['id']} · Current status

- **Title:** {esc_md(p.get('title'))}
- **Project status:** {esc_md(p.get('status'))}
- **Activity:** {esc_md(d.get('activity') or 'unclassified')}
- **Portfolio progress:** {d.get('progress', 0)}%
- **Current stage:** {esc_md(d.get('stage') or 'Not yet recorded')}
- **Evidence established:** {esc_md(d.get('evidence') or 'Not yet recorded')}
- **Next gate:** {esc_md(d.get('next_gate') or 'Not yet recorded')}
- **Blocker:** {esc_md(d.get('blocker') or 'Not yet recorded')}

## Source of truth

This snapshot is synchronized from `paper.json` and `papers/dashboard.json`. Study-specific `process/` files may contain finer-grained status and frozen design details.
"""


def build_agent_handoff(p: dict, d: dict, folder: Path) -> str:
    links = "\n".join(canonical_links(p, folder))
    return f"""# ARIS4C{p['id']} · Agent takeover brief

## What this project is

**{esc_md(p.get('title'))}**

{esc_md(p.get('summary'))}

## Current state

- Activity: **{esc_md(d.get('activity') or 'unclassified')}**
- Progress: **{d.get('progress', 0)}%**
- Stage: **{esc_md(d.get('stage') or 'Not yet recorded')}**
- Evidence: {esc_md(d.get('evidence') or 'Not yet recorded')}

## Immediate next action

**{esc_md(d.get('next_gate') or 'Review TODO.md and the project process files to establish the next gate.')}**

## Current blocker / gate

{esc_md(d.get('blocker') or 'No blocker recorded.')}

## Canonical files / entry points

{links}

## Before changing anything

1. Read `TODO.md`, `DECISIONS.md`, and the newest entries in `CHATLOG.md` and `SESSION_LOG.md`.
2. Preserve frozen/preregistered design decisions unless the repository explicitly records an authorized amendment.
3. Do not broaden claims beyond the evidence state recorded in the manuscript/process files.
4. Use **Cochrane Kang** for visible author naming.
5. Do not commit secrets, private credentials, hidden chain-of-thought, or unnecessary sensitive personal data.
6. After a material change, update canonical research files first, then continuity files.

## Handoff completion rule

Before ending a substantial session:
- update `TODO.md`;
- append any material research decision to `DECISIONS.md`;
- append a public-safe conversation summary to `CHATLOG.md`;
- append what was executed/validated to `SESSION_LOG.md`.
"""


def build_context(p: dict) -> str:
    tags = ", ".join(str(x) for x in p.get("tags", []))
    return f"""# ARIS4C{p['id']} · Research context

## Project

**{esc_md(p.get('title'))}**

## Compact scope

{esc_md(p.get('summary'))}

## Domain

{esc_md(p.get('domain'))}

## Working tags

{tags}

## Construct / claim discipline

Read `DECISIONS.md` before changing construct definitions or claim strength. The current manuscript, preregistration/design files, and machine-readable results remain canonical.

## Where to continue

Start from `AGENT_HANDOFF.md`, then inspect the project-specific `process/`, manuscript, data, code, figure, table, and agent directories referenced by `paper.json`.
"""


def build_todo(p: dict, d: dict) -> str:
    blocker = esc_md(d.get("blocker") or "")
    blocker_line = ""
    if blocker and not blocker.lower().startswith("none"):
        blocker_line = f"- [ ] **P1 · Remove/resolve blocker:** {blocker}\n"
    return f"""# ARIS4C{p['id']} · TODO

## P0 · Next gate

- [ ] {esc_md(d.get('next_gate') or 'Establish the next scientific/review gate from the canonical process files.')}

## P1 · Enabling work

{blocker_line}- [ ] Keep `STATUS.md` and `AGENT_HANDOFF.md` synchronized after the next material state change.
- [ ] Append the next material ChatGPT/human/agent exchange to `CHATLOG.md`.
- [ ] Append the next substantial execution session to `SESSION_LOG.md`.

## P2 · Packaging / optional

- [ ] Keep public outputs, figures/tables, bilingual delivery, and repository links consistent with the current ARIS4C output standard when applicable.
"""


def build_decisions(p: dict) -> str:
    lines = BOOTSTRAP_DECISIONS.get(p["id"], [])
    bullets = "\n".join(f"- {x}" for x in lines) or "- No project-specific historical decision has been backfilled yet."
    return f"""# ARIS4C{p['id']} · Decision log

This file is append-oriented. Preserve superseded decisions when they explain why the project changed direction; mark them as superseded rather than deleting them.

## 2026-09-19 · Continuity-standard bootstrap

**Decision:** Adopt the repository-level ARIS4C continuity/handoff contract for this paper.

**Why:** The project must remain recoverable across ChatGPT conversations, accounts, computers, and external agents without relying on one chat's memory.

**Project-specific decisions distilled from surviving project context:**
{bullets}

**Canonical follow-up:** Future material decisions should be appended with date, rationale, and affected files/commits when known.
"""


def build_chatlog(p: dict) -> str:
    summary = BOOTSTRAP_CHAT.get(p["id"], p.get("summary", ""))
    return f"""# ARIS4C{p['id']} · Research conversation log

Public-safe record of material human ↔ ChatGPT / external-agent conversations. This is **not** hidden chain-of-thought and must not contain secrets.

## 2026-09-19 · Historical bootstrap distilled from surviving ARIS4C context

- **Surface:** ChatGPT / ARIS4C project conversations
- **Participants:** Cochrane Kang + AI research assistants
- **Research thread:** {esc_md(summary)}
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
"""


def build_session_log(p: dict) -> str:
    return f"""# ARIS4C{p['id']} · Session log

Append substantial execution sessions in reverse chronological order or chronological order, but remain consistent.

## 2026-09-19 · Continuity retrofit

- Added the standardized ARIS4C per-paper handoff package.
- Bootstrapped project context, current state, TODO, decision history, and a public-safe conversation record.
- Established Git as the cross-device / cross-account / cross-agent continuity surface.
- Future material sessions must append execution results and validation here.
"""


def main() -> int:
    rows, _ = project_rows()
    changed = []
    for row in rows:
        manifest = row["manifest"]
        p = row["paper"]
        d = row["dash"]
        folder = manifest.parent
        handoff = folder / "handoff"
        handoff.mkdir(parents=True, exist_ok=True)

        managed = {
            "README.md": build_readme(p),
            "STATUS.md": build_status(p, d),
            "AGENT_HANDOFF.md": build_agent_handoff(p, d, folder),
        }
        for name, content in managed.items():
            path = handoff / name
            if sync_managed(path, content):
                changed.append(str(path.relative_to(ROOT)))

        seeded = {
            "CONTEXT.md": build_context(p),
            "TODO.md": build_todo(p, d),
            "DECISIONS.md": build_decisions(p),
            "CHATLOG.md": build_chatlog(p),
            "SESSION_LOG.md": build_session_log(p),
        }
        for name, content in seeded.items():
            path = handoff / name
            if write_if_missing(path, content):
                changed.append(str(path.relative_to(ROOT)))

    print(f"Continuity packages checked: {len(rows)}")
    if changed:
        print("Created/updated:")
        for path in changed:
            print(f"- {path}")
    else:
        print("No changes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
