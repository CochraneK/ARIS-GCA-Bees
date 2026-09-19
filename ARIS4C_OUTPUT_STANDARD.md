# ARIS4C Final Output Standard · v3

**Effective:** 2026-09-18  
**Owner:** Cochrane Kang  
**Scope:** every numbered ARIS4C research project

ARIS4C treats a research project as complete only when the scientific work and the public-facing output package are both explicit. A project may be scientifically mature before it is publication-ready, but `submission-ready` / `final` status requires the output contract below.

## 0. Alignment with upstream ARIS

This contract strengthens, rather than replaces, the upstream ARIS paper workflow. The current ARIS `paper-writing` pipeline explicitly chains `paper-plan → paper-figure → paper-write → paper-compile → auto-paper-improvement-loop`; its planning stage includes figure/table placement and its writing/review stages require figures and tables to be described, referenced, and checked. ARIS4C therefore treats figures/tables as first-class paper artifacts.

The **bilingual full-paper requirement** and the **article-type-specific minimum visual package** below are ARIS4C-specific completion rules. They are not claimed to be universal journal rules or verbatim upstream ARIS requirements.

## 1. Bilingual paper contract

Every final project should provide:

1. **English full paper** — canonical submission-facing manuscript.
2. **Chinese full paper** — a complete Chinese mirror for reading, communication, teaching, and portfolio use.

The Chinese version may preserve English bibliographic references, technical symbols, equations, variable names, and journal-specific wording where translation would reduce precision. It must not silently broaden claims beyond the English canonical manuscript.

Preferred layout:

```
paper/
  en/
  zh/
manuscript/
  MAIN.md
  MAIN.zh-CN.md
```

During active research, a Chinese extended abstract is acceptable as an interim artifact. It is **not** sufficient for `submission-ready`.

## 2. Figure and table contract

### Core rule: no fixed figure count or fixed figure template

ARIS4C does **not** standardize papers to three figures, nor require the same figure types across projects. Figure count, figure form, and table count must follow the paper's actual inferential structure.

The optimization target is **maximum information gain and visual explainability without redundancy**. A project should create as many scientifically useful visuals as needed to let a reader understand the design, evidence, main results, uncertainty, robustness, heterogeneity, and mechanism with minimal dependence on dense prose. It must not create decorative, duplicated, or weakly differentiated figures merely to increase the count.

Whenever applicable, the visual plan should consider distinct roles such as:
- study/design/data-flow map;
- sample or corpus structure;
- descriptive distributions;
- primary effect/result visualization;
- uncertainty / confidence / posterior visualization;
- model comparison;
- robustness / sensitivity / specification curve;
- subgroup / heterogeneity / interaction visualization;
- ablation / benchmark / error analysis;
- network, spatial, temporal, phylogenetic, or semantic structure;
- conceptual mechanism / ontology / architecture;
- limitations, decision boundaries, or failure modes.

Repeated use of the same chart form is acceptable only when it is the clearest encoding (for example, coordinated small multiples). Otherwise, prefer figure-type diversity that matches the underlying scientific question.

A useful default is to think in terms of a **visual narrative**, not a quota:
**What is the system? → What data entered? → What did we find? → How uncertain/robust is it? → Where does it vary or fail?**



Figures and tables are scientific communication artifacts, not decoration. The required visual package depends on article type.

### Empirical / quantitative papers
Expected package:
- enough substantive figures to cover the main inferential stages rather than a fixed count;
- at least one substantive table when tabular precision adds value;
- main-text figures plus supplementary visuals when additional diagnostics would otherwise overload the narrative.

Typical figure roles include study/data flow, descriptive structure, primary estimates, uncertainty, model comparison, robustness, heterogeneity, and diagnostics.

### Theory / synthesis / review papers
Expected package:
- conceptual/evidence-structure figures wherever relationships are easier to understand visually;
- evidence/model tables where exact comparison matters;
- quantitative figures whenever quantitative synthesis is present;
- additional maps, taxonomies, timelines, networks, or evidence landscapes when they materially clarify the argument.

### Methods / benchmark / agent papers
Expected package:
- architecture/pipeline visualization;
- benchmark/evaluation tables;
- performance, calibration, ablation, failure-mode, and error-analysis figures when results exist;
- additional workflow/evidence-graph visualizations when they improve auditability.

### Exceptions
A paper may remain visually sparse only when additional visuals would add no scientific information. The reason must be explicit in the manuscript/output metadata. Conversely, complex projects should not be artificially capped at a small number of figures.

## 3. Reproducibility contract for visuals

Whenever possible:
- figure source data must be stored or reproducibly derived;
- figure-generation code must be committed;
- captions must distinguish empirical results from simulations/synthetic diagnostics;
- synthetic or illustrative figures must never be presented as empirical evidence;
- figure/table claims must agree with the canonical manuscript and machine-readable outputs.

Preferred layout:

```
figures/
tables/
code/
data/
```

## 4. PDF-first public-delivery contract

Final/submission-ready projects should additionally provide:
- **English PDF** — stable public reading/download artifact;
- **Chinese PDF** — stable bilingual mirror.

Preferred manifest fields:

```json
"links": {
  "paper_en_pdf": "...",
  "paper_zh_pdf": "...",
  "paper_en_full": "...",
  "paper_zh_full": "..."
}
```

The public Research Command Center is **PDF-first**: when a PDF link exists, the English / 中文 buttons point directly to the PDF. HTML or Markdown full text remains a fallback and source-friendly companion, not the preferred final public reading surface.


## 4.5 One-page visual explainer for Finish papers

When a paper reaches the portfolio state **Finish**, it must expose one compact visual that explains the whole paper at a glance.

This visual is a **public communication layer**, not a replacement for the scientific figures. It should compress the paper into the smallest useful narrative, typically:

**research question → evidence/data → main result → evidence boundary / implication**

Requirements:

- one image per Finish paper;
- faithful to the canonical manuscript and evidence state;
- clearly separate supported findings from boundaries, uncertainty, or next-step claims;
- stored as a repository asset and declared in `paper.json -> outputs.one_page_visual`;
- displayed as a small clickable thumbnail in the portfolio README so the table remains compact;
- regenerated when a material manuscript change makes the old summary misleading.

Preferred metadata:

```json
"outputs": {
  "one_page_visual": {
    "status": "complete",
    "repo_path": "docs/assets/paper-at-a-glance/00X.webp",
    "language": "zh-CN",
    "purpose": "one-page visual explanation of the complete paper for the portfolio table"
  }
}
```

The portfolio may use image-generation models for this communication artifact, but the executor must verify the generated text and scientific claims against the paper before marking it complete.

## 5. Continuity / cross-agent handoff contract

Every numbered ARIS4C paper, including early-stage projects, must maintain the handoff package defined in `ARIS4C_CONTINUITY_STANDARD.md`:

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

This requirement exists so another ChatGPT conversation/account, computer, external agent, or human collaborator can resume the project from Git without depending on one conversation's memory.

Material research conversations must be preserved as public-safe summaries in `CHATLOG.md`; important choices belong in `DECISIONS.md`; substantial execution sessions belong in `SESSION_LOG.md`. Current state and next actions must remain recoverable from `STATUS.md`, `TODO.md`, and `AGENT_HANDOFF.md`.

A project missing the required package is **continuity-incomplete** even if its manuscript is otherwise scientifically mature.

## 6. Page contract

The ARIS4C public hub should expose, when available:

- English paper
- 中文论文
- Figures
- Tables
- Pipeline / Status
- Source

The dashboard should also make output completeness visible rather than treating manuscript progress alone as completion.

The public Research Command Center should expose a **progress-over-time curve derived from Git history** of `papers/dashboard.json`. This history is a management trace, not a scientific result. It should support the portfolio mean and per-paper views without requiring manually maintained historical values.

## 7. Final-status gate

A project may be marked `submission-ready` / `final` only if all applicable items pass:

- [ ] English full manuscript
- [ ] Chinese full manuscript
- [ ] English PDF for public delivery when submission-ready/final
- [ ] Chinese PDF for public delivery when submission-ready/final
- [ ] appropriate figure package
- [ ] appropriate table package
- [ ] figures/tables traceable to evidence or explicitly labeled conceptual/synthetic
- [ ] references checked
- [ ] limitations explicit
- [ ] reproducibility artifacts present where applicable
- [ ] independent/reviewer gate complete where required
- [ ] Page/index links current
- [ ] one-page visual explainer present and current for Finish state
- [ ] per-paper continuity/handoff audit PASS
- [ ] current TODO / next gate does not contradict the declared final state
- [ ] material conversation and execution history preserved in public-safe Git records

A journal portal submission itself remains an author action and is not required for repository-level scientific completion.
