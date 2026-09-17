<p align="right">
  <a href="./README.md"><img src="https://img.shields.io/badge/Language-English-blue" alt="English"></a>
  <a href="./README.zh-CN.md"><img src="https://img.shields.io/badge/语言-中文-red" alt="中文"></a>
</p>

<div align="center">

# ARIS4C

**ARIS for Cochrane · a living research hub for papers developed with ARIS**

[**Paper Hub**](docs/index.html) · [**Papers Registry**](papers/) · [**Paper 001**](docs/paper/en/main.html) · [**中文**](README.zh-CN.md)

</div>

## What is ARIS4C?

**ARIS4C = ARIS for Cochrane.** It is the long-lived research repository for papers developed with the [ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) methodology.

The repository began with the GCA × Bees theory-and-simulation project and now serves as a reusable home for future papers.

The separation is deliberate:

- **ARIS is the research engine** and can keep updating independently.
- **ARIS4C is the research archive and portfolio** for Cochrane's ARIS-assisted research.
- **Each paper records the exact ARIS version/commit used**, so upgrading ARIS does not rewrite the history of older work.
- **The public HTML hub is generated from paper manifests**, rather than maintained by hand.

## Repository model

```text
ARIS4C/
├── papers/
│   ├── 001-gca-bees/
│   │   └── paper.json           # manifest for the original paper
│   └── 002-next-paper/
│       ├── paper.json
│       ├── code/
│       ├── data/
│       ├── figures/
│       ├── manuscript/
│       └── process/
├── docs/
│   └── index.html               # generated public paper hub
├── tools/
│   ├── new_paper.py             # scaffold the next numbered paper
│   ├── build_papers_index.py    # regenerate the HTML hub
│   └── sync_aris.ps1            # update the external ARIS engine on Windows
├── aris.lock.json               # repository-level ARIS update policy
├── code/                        # legacy Paper 001 research code
├── process/                     # legacy Paper 001 ARIS process records
└── simulation_results*.json     # legacy Paper 001 outputs
```

The original Paper 001 files remain in their current locations for link compatibility. New papers should use the numbered `papers/` layout from the start.

## Start a new paper

```bash
python tools/new_paper.py "Your paper title" --slug short-name
```

This creates the next stable paper ID and its standard research folders. Before starting the ARIS run, record the exact ARIS tag and commit in that paper's `paper.json`.

## Keep ARIS current

ARIS itself is **not vendored into ARIS4C**. On Windows, update a separate local ARIS clone with:

```powershell
./tools/sync_aris.ps1
```

The helper clones or pulls the upstream ARIS repository, records the local tag/commit, and uses the upstream smart-update path when Bash is available. Local engine state is gitignored.

The repository currently recommends **ARIS v0.4.26** in `aris.lock.json`; historical papers retain their original provenance instead of being relabeled after upgrades.

## Rebuild the public paper hub

```bash
python tools/build_papers_index.py
```

A GitHub Action also regenerates `docs/index.html` automatically when paper manifests change on `main`.

## Paper 001 · GCA × Bees

**A Unified Predictive Coding Account of Functional Self-Awareness in Bees: Analytically Derived Precision Trade-offs Across Four Behavioral Domains**

This remains a theory + simulation working paper. Its modeled relationships are hypotheses and predictions, not empirical evidence that bees possess a particular form of self-awareness or that the proposed neural mechanism has been demonstrated in vivo.

- [English manuscript](docs/paper/en/main.html)
- [中文论文](docs/paper/zh/main.html)
- [Research pipeline report](process/RESEARCH_PIPELINE_REPORT.md)
- [Idea report](process/IDEA_REPORT.md)
- [Auto review](process/AUTO_REVIEW.md)

## Principle

> Upgrade the research engine; preserve the research record.

Maintainer: **Cunyi Kang**
