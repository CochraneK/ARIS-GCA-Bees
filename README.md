<p align="right">
  <a href="./README.md"><img src="https://img.shields.io/badge/Language-English-blue" alt="English"></a>
  <a href="./README.zh-CN.md"><img src="https://img.shields.io/badge/语言-中文-red" alt="中文"></a>
</p>

<div align="center">

# ARIS-GCA-Bees

**A theory-and-simulation project on functional self-awareness in bees**

<p>
  <img alt="Stage" src="https://img.shields.io/badge/stage-theory%20%2B%20simulation-6C63FF">
  <img alt="Domain" src="https://img.shields.io/badge/domain-computational%20neuroethology-2F80ED">
  <img alt="Pipeline" src="https://img.shields.io/badge/pipeline-ARIS-27AE60">
</p>

[**Web bundle**](docs/index.html) · [**Research pipeline**](process/RESEARCH_PIPELINE_REPORT.md) · [**English manuscript**](docs/paper/en/main.html) · [**中文论文**](docs/paper/zh/main.html)

</div>

## Overview

ARIS-GCA-Bees is a computational neuroethology project developed through the [ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) automated research pipeline.

The project proposes a **predictive-coding account of functional self-awareness in bees** and uses simulation to explore whether a shared latent parameter — **precision** — can jointly organize four modeled behavioral domains:

- metacognitive opt-out behavior;
- tool-use anticipation;
- caste-appropriate learning;
- general cognitive ability (GCA).

> [!IMPORTANT]
> This repository is at the **theory + simulation** stage. Its relationships and sign changes are model-generated hypotheses and predictions, not empirical evidence that bees possess a particular form of self-awareness or that the proposed neural mechanism has been demonstrated in vivo.

## Main idea

Within the current model, the project explores three central predictions:

- metacognitive performance can follow an inverted-U relationship with precision;
- higher modeled GCA can coincide with poorer metacognitive calibration under some parameter regimes;
- circadian disruption can change the sign of the modeled metacognition–GCA relationship.

The value of the project is therefore in **formalization, simulation, falsifiable prediction generation, and transparent research packaging**.

## Repository structure

The README previously described an older layout. The current repository is organized as follows:

```text
ARIS-GCA-Bees/
├── code/                         # simulation scripts
│   ├── experiment_r2_4domain.py
│   ├── experiment_unified_selfmodel_full.py
│   └── pilot_*.py
├── docs/                         # web / manuscript bundle
│   ├── index.html
│   ├── zh.html
│   ├── figures/
│   └── paper/
│       ├── en/
│       ├── zh/
│       ├── sections/
│       └── references.bib
├── process/                      # research-generation records
│   ├── IDEA_REPORT.md
│   ├── AUTO_REVIEW.md
│   ├── PAPER_PLAN.md
│   └── RESEARCH_PIPELINE_REPORT.md
├── simulation_results.json
├── simulation_results_r2.json
├── README.md
└── README.zh-CN.md
```

## Start here

| Goal | File |
| --- | --- |
| Understand how the project was generated | [Research Pipeline Report](process/RESEARCH_PIPELINE_REPORT.md) |
| See the original idea development | [Idea Report](process/IDEA_REPORT.md) |
| Review the automated critique stage | [Auto Review](process/AUTO_REVIEW.md) |
| Read the English manuscript | [docs/paper/en/main.html](docs/paper/en/main.html) |
| Read the Chinese manuscript | [docs/paper/zh/main.html](docs/paper/zh/main.html) |
| Open the web landing bundle | [docs/index.html](docs/index.html) |

## Reproduce the main simulation

```bash
python code/experiment_r2_4domain.py
```

Additional simulations and pilots are available under `code/`. Numerical outputs currently live in the repository root as `simulation_results.json` and `simulation_results_r2.json`.

## Workflow

```text
idea discovery
→ pilot testing
→ full simulation
→ review loop
→ paper planning
→ manuscript drafting
→ web / manuscript packaging
```

## Working paper

**A Unified Predictive Coding Account of Functional Self-Awareness in Bees: Analytically Derived Precision Trade-offs Across Four Behavioral Domains**

This is a working research artifact, not a published empirical paper.

## Citation

If you reference the repository before formal publication:

```text
Kang, C. (2026). ARIS-GCA-Bees: A unified predictive coding account of functional self-awareness in bees. GitHub repository.
```

## Contact

Maintainer: **Cunyi Kang**

For questions, comments, or collaboration, please open a GitHub issue.
