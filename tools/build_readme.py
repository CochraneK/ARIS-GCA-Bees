#!/usr/bin/env python3
"""Generate the bilingual ARIS4C repository README from canonical metadata."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT / "papers"
DASHBOARD = PAPERS / "dashboard.json"

ZH_TITLES = {
    "001": "蜜蜂 GCA × 不确定性",
    "002": "LING-01 · 语言周期性检验",
    "003": "殖民遗产 × 学科优势",
    "004": "排斥的反事实知识网络成本",
    "005": "坏科学的全球隐性负担",
    "006": "中国姓名字母顺序暴露",
    "007": "跨物种年龄等价",
    "008": "人类高级智力演化 Bootstrap",
    "009": "现象学保持型计算精神病学",
    "010": "Universal Concept Identification",
    "011": "Research Forensics",
    "012": "Oppositional Causal Inversion",
    "013": "出生—死亡时间耦合",
    "014": "Public Integrity Forensics",
    "015": "Sleeping Beauty Miner",
    "016": "全球脏话 / 禁忌语言语法",
    "017": "LING-02 · 预测性语言空间",
}

STATE = {
    "finish": ("🔵 Finish", "🔵 完成"),
    "active": ("🟢 Active", "🟢 正在推进"),
    "wait": ("🟡 Wait", "🟡 待推进"),
    "block": ("🔴 Block", "🔴 阻塞"),
}


def load():
    dashboard = json.loads(DASHBOARD.read_text(encoding="utf-8"))
    rows = []
    for manifest in sorted(PAPERS.glob("[0-9][0-9][0-9]-*/paper.json")):
        p = json.loads(manifest.read_text(encoding="utf-8"))
        d = dashboard["projects"].get(p["id"], {})
        links = p.get("links", {})
        rows.append({
            "id": p["id"],
            "folder": manifest.parent.name,
            "title": p.get("title", ""),
            "short_title": p.get("short_title") or p.get("title", ""),
            "status": p.get("status", ""),
            "activity": d.get("activity", "active"),
            "progress": int(d.get("progress", 0)),
            "stage": d.get("stage", ""),
            "next_gate": d.get("next_gate", ""),
            "paper_en_pdf": links.get("paper_en_pdf", ""),
            "paper_zh_pdf": links.get("paper_zh_pdf", ""),
        })
    return dashboard, rows


def site_link(path: str) -> str:
    if not path:
        return ""
    if path.startswith(("https://", "http://")):
        return path
    return f"https://cochranek.github.io/ARIS4C/{path.lstrip('/')}"


def paper_rows(rows: list[dict], zh: bool = False) -> str:
    lines = []
    for r in rows:
        state = STATE.get(r["activity"], (r["activity"], r["activity"]))[1 if zh else 0]
        title = ZH_TITLES.get(r["id"], r["short_title"]) if zh else r["short_title"]
        lines.append(
            f'| **{r["id"]}** | [{title}](papers/{r["folder"]}/) | {state} | '
            f'{r["progress"]}% | [handoff](papers/{r["folder"]}/handoff/AGENT_HANDOFF.md) |'
        )
    return "\n".join(lines)


def ready_papers(rows: list[dict], zh: bool = False) -> str:
    ready = [r for r in rows if r["paper_en_pdf"] and r["paper_zh_pdf"]]
    if not ready:
        return "_No bilingual PDF package is public yet._" if not zh else "_目前还没有公开双语 PDF 包。_"
    lines = []
    for r in ready:
        title = ZH_TITLES.get(r["id"], r["short_title"]) if zh else r["short_title"]
        lines.append(
            f'- **{r["id"]} · {title}** — '
            f'[English PDF]({site_link(r["paper_en_pdf"])}) · '
            f'[中文 PDF]({site_link(r["paper_zh_pdf"])})'
        )
    return "\n".join(lines)


def common_badges() -> str:
    return """<p align="center">
  <a href="https://github.com/CochraneK/ARIS4C/actions/workflows/build-paper-index.yml"><img src="https://github.com/CochraneK/ARIS4C/actions/workflows/build-paper-index.yml/badge.svg" alt="Paper index"></a>
  <a href="https://github.com/CochraneK/ARIS4C/actions/workflows/build-public-pdfs.yml"><img src="https://github.com/CochraneK/ARIS4C/actions/workflows/build-public-pdfs.yml/badge.svg" alt="Bilingual PDFs"></a>
  <a href="https://github.com/CochraneK/ARIS4C/actions/workflows/sync-paper-handoffs.yml"><img src="https://github.com/CochraneK/ARIS4C/actions/workflows/sync-paper-handoffs.yml/badge.svg" alt="Continuity handoffs"></a>
  <img src="https://img.shields.io/badge/ARIS-v0.4.26-475569" alt="ARIS v0.4.26">
</p>"""


def english(rows: list[dict]) -> str:
    return f"""<p align="right">
  <a href="./README.en.md"><img src="https://img.shields.io/badge/Language-English-2563eb" alt="English"></a>
  <a href="./README.md"><img src="https://img.shields.io/badge/语言-中文（默认）-dc2626" alt="中文"></a>
</p>

<p align="center">
  <img src="./docs/assets/readme/en/hero.svg" width="100%" alt="ARIS4C — Research as a living system">
</p>

<p align="center">
  <a href="https://cochranek.github.io/ARIS4C/"><img src="https://img.shields.io/badge/Open-Research_Command_Center-0f766e?style=for-the-badge" alt="Open Research Command Center"></a>
</p>

{common_badges()}

# ARIS4C

**ARIS for Cochrane** is a living research portfolio for papers developed through the [ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) workflow.

ARIS is the research engine. **ARIS4C is the canonical research system around it:** numbered papers, evidence, code, bilingual manuscripts, adaptive figures and tables, review gates, public PDFs, portfolio state, and enough handoff context for another computer, account, agent, or collaborator to continue the work from Git.

> **One repository, one canonical state, many research threads.**

## Start here

| I want to… | Go to |
|---|---|
| Take over portfolio control as another agent/account/computer | **[`000/README.md`](000/README.md)** |
| See the whole portfolio visually | **[Research Command Center](https://cochranek.github.io/ARIS4C/)** |
| Read completed papers | See **Publication-ready outputs** below |
| Continue one paper on another machine / account / agent | Open that paper's **`handoff/README.md`** |
| Check current portfolio state | [`papers/dashboard.json`](papers/dashboard.json) |
| Understand final-output requirements | [`ARIS4C_OUTPUT_STANDARD.md`](ARIS4C_OUTPUT_STANDARD.md) |
| Understand continuity requirements | [`ARIS4C_CONTINUITY_STANDARD.md`](ARIS4C_CONTINUITY_STANDARD.md) |
| Understand portfolio activity states | [`ARIS4C_STATUS_MODEL.md`](ARIS4C_STATUS_MODEL.md) |
| Understand 000 scheduling / checkpoint rules | [`ARIS4C_OPERATING_MODEL.md`](ARIS4C_OPERATING_MODEL.md) |

## Portfolio at a glance

<p align="center">
  <img src="./docs/assets/readme/en/portfolio-status.svg" width="100%" alt="ARIS4C portfolio status">
</p>

<p align="center">
  <img src="./docs/assets/readme/en/portfolio-maturity.svg" width="100%" alt="ARIS4C paper maturity chart">
</p>

<p align="center">
  <img src="./docs/assets/readme/en/delivery-readiness.svg" width="100%" alt="ARIS4C delivery and continuity readiness">
</p>

> Progress is a **portfolio-management estimate**, not a scientific result. `100%` means the repository-level final output contract is satisfied. Live execution uses four states: **Finish** = final/output contract complete; **Active** = meaningful research is moving now; **Wait** = the next step can be done but is not currently being advanced; **Block** = an external/human/data/review dependency prevents progress.

## Publication-ready outputs

{ready_papers(rows)}

## The {len(rows)}-paper portfolio

| ID | Project | State | Progress | Continue from |
|---|---|---:|---:|---|
{paper_rows(rows)}

## How ARIS4C works

<p align="center">
  <img src="./docs/assets/readme/en/architecture.svg" width="100%" alt="ARIS4C research system architecture">
</p>

The key distinction is intentional:

- **ARIS** supplies the research workflow.
- **Each numbered paper** owns its scientific evidence and decisions.
- **ARIS4C 000 / dashboard** manages the portfolio without becoming a second scientific truth.
- **`handoff/`** preserves the context needed to resume work across sessions and agents.
- **Git history** preserves superseded states rather than erasing how a paper evolved.

## Common structure of every Paper

<p align="center">
  <img src="./docs/assets/readme/en/paper-structure.svg" width="100%" alt="Common structure of an ARIS4C paper project">
</p>

Every numbered Paper follows the same repository contract, while its scientific design, data, analyses, figures, and review gates remain project-specific.

## Lifecycle of a Paper

<p align="center">
  <img src="./docs/assets/readme/en/paper-lifecycle.svg" width="100%" alt="Lifecycle of an ARIS4C paper">
</p>

## Final-paper contract

A submission-ready/final ARIS4C paper is expected to provide:

| Layer | Requirement |
|---|---|
| Manuscript | English full paper + Chinese full paper |
| Public delivery | English PDF + Chinese PDF |
| Visuals | Figure/table package chosen for the actual inferential structure — **no fixed “3 figures” quota** |
| Evidence | Traceable empirical / synthetic / conceptual provenance |
| Review | Required scientific / reproducibility / independent-review gates |
| Continuity | `handoff/` package with status, TODO, decisions, context, chat log, agent handoff, and session log |
| Public surface | Current links on the Research Command Center |

See [**ARIS4C Final Output Standard · v3**](ARIS4C_OUTPUT_STANDARD.md).

## Cross-agent continuity

<p align="center">
  <img src="./docs/assets/readme/en/handoff-package.svg" width="100%" alt="Cross-agent handoff package">
</p>

Every numbered paper has the same cold-start package:

```text
papers/00X-project/
└── handoff/
    ├── README.md
    ├── STATUS.md
    ├── TODO.md
    ├── DECISIONS.md
    ├── CONTEXT.md
    ├── CHATLOG.md
    ├── AGENT_HANDOFF.md
    └── SESSION_LOG.md
```

A new executor should be able to start with:

> **Read `papers/00X-.../handoff/README.md` and continue from the current repository state.**

The public repository stores **public-safe conversation summaries**, not credentials, private personal material, or hidden model chain-of-thought.

## Repository anatomy

```text
ARIS4C/
├── 000/                           # Git-resident portfolio controller handoff
├── papers/
│   ├── dashboard.json             # portfolio source of truth
│   └── 00X-project/
│       ├── paper.json             # paper metadata
│       ├── manuscript/            # EN / ZH manuscripts
│       ├── figures/ + tables/     # scientific visuals
│       ├── code/ + data/          # analysis / provenance
│       ├── process/               # design, gates, frozen decisions
│       └── handoff/               # cross-agent continuity
├── docs/                          # GitHub Pages + public PDFs
├── tools/                         # generators and audits
├── ARIS4C_OUTPUT_STANDARD.md
├── ARIS4C_CONTINUITY_STANDARD.md
├── ARIS4C_STATUS_MODEL.md
├── ARIS4C_OPERATING_MODEL.md
└── aris.lock.json                 # pinned ARIS lineage
```

## Rebuild and audit

```bash
python tools/build_papers_index.py
python tools/build_readme_assets.py
python tools/build_readme.py
python tools/audit_paper_outputs.py
python tools/audit_paper_handoffs.py
python tools/sync_paper_handoffs.py
python tools/portfolio_queue.py
```

## Design principles

1. **One canonical source of truth.** Parallel chats and agents can explore; Git decides what became canonical.
2. **Falsification before narrative.** Stronger methods are allowed to replace weaker claims.
3. **Visualize the evidence, not a quota.** Figures are chosen for information gain, not template compliance.
4. **Bilingual by default at completion.** Final public delivery is English + Chinese and PDF-first.
5. **Research must be resumable.** A project that another agent cannot safely continue is operationally incomplete.
6. **Anomalies are not verdicts.** Forensics-oriented projects preserve human review and explicit uncertainty.
7. **Finish what is closest first.** 000 continues genuine Active work first, then promotes the highest-progress Wait paper, with bounded-unit Git checkpoints before switching.

---

Maintainer: **Cochrane Kang**  
Research hub: **https://cochranek.github.io/ARIS4C/**
"""


def chinese(rows: list[dict]) -> str:
    return f"""<p align="right">
  <a href="./README.en.md"><img src="https://img.shields.io/badge/Language-English-2563eb" alt="English"></a>
  <a href="./README.md"><img src="https://img.shields.io/badge/语言-中文（默认）-dc2626" alt="中文"></a>
</p>

<p align="center">
  <img src="./docs/assets/readme/zh/hero.svg" width="100%" alt="ARIS4C — Research as a living system">
</p>

<p align="center">
  <a href="https://cochranek.github.io/ARIS4C/"><img src="https://img.shields.io/badge/打开-Research_Command_Center-0f766e?style=for-the-badge" alt="打开 Research Command Center"></a>
</p>

{common_badges()}

# ARIS4C

**ARIS for Cochrane** 是一个通过 [ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) 持续推进论文的长期研究组合与 canonical 仓库。

ARIS 是研究引擎；**ARIS4C 是围绕论文建立的完整研究系统**：编号项目、证据、代码、中英文稿、针对性图表、审查门、公开 PDF、portfolio 状态，以及让另一台电脑、另一个账号、另一个 Agent 或协作者可以直接从 Git 接管研究所需的上下文。

> **一个仓库，一个 canonical state，多条并行研究线程。**

## 从这里开始

| 你想做什么 | 入口 |
|---|---|
| 让另一个 Agent / 账号 / 电脑接管总控 | **[`000/README.md`](000/README.md)** |
| 可视化查看全部项目 | **[Research Command Center](https://cochranek.github.io/ARIS4C/)** |
| 阅读已完成论文 | 见下方 **已达到公开交付状态的论文** |
| 换电脑 / 账号 / Agent 继续某篇论文 | 打开该项目的 **`handoff/README.md`** |
| 查看当前 portfolio 状态 | [`papers/dashboard.json`](papers/dashboard.json) |
| 查看最终输出标准 | [`ARIS4C_OUTPUT_STANDARD.md`](ARIS4C_OUTPUT_STANDARD.md) |
| 查看跨 Agent 接管标准 | [`ARIS4C_CONTINUITY_STANDARD.md`](ARIS4C_CONTINUITY_STANDARD.md) |
| 查看项目状态分类规则 | [`ARIS4C_STATUS_MODEL.md`](ARIS4C_STATUS_MODEL.md) |
| 查看 000 调度 / 落盘规则 | [`ARIS4C_OPERATING_MODEL.md`](ARIS4C_OPERATING_MODEL.md) |

## 当前研究组合

<p align="center">
  <img src="./docs/assets/readme/zh/portfolio-status.svg" width="100%" alt="ARIS4C portfolio status">
</p>

<p align="center">
  <img src="./docs/assets/readme/zh/portfolio-maturity.svg" width="100%" alt="ARIS4C paper maturity chart">
</p>

<p align="center">
  <img src="./docs/assets/readme/zh/delivery-readiness.svg" width="100%" alt="ARIS4C delivery and continuity readiness">
</p>

> Progress 是**项目管理估计**，不是科学结果。`100%` 表示仓库层面的最终输出契约已经满足。实时执行状态固定为四类：**Finish / 完成** = 已满足当前 final/output contract；**Active / 正在推进** = 近期确实有实质研究推进或 research job 正在运行；**Wait / 待推进** = 下一步可以做，但当前没有实际推进；**Block / 阻塞** = 必须等待外部、人类、独立审查、数据传输等依赖。

## 已达到公开交付状态的论文

{ready_papers(rows, zh=True)}

## {len(rows)} 个 Paper

| ID | 项目 | 状态 | 进度 | 接管入口 |
|---|---|---:|---:|---|
{paper_rows(rows, zh=True)}

## ARIS4C 如何运作

<p align="center">
  <img src="./docs/assets/readme/zh/architecture.svg" width="100%" alt="ARIS4C research system architecture">
</p>

关键分工：

- **ARIS** 提供研究流程。
- **每一个 numbered paper** 拥有自己的科学证据和决策。
- **ARIS4C 000 / dashboard** 管 portfolio，但不成为第二套科学真相。
- **`handoff/`** 保存跨对话、跨账号、跨 Agent 继续研究所需的上下文。
- **Git history** 保存被替代的旧版本，而不是抹掉研究如何演化。

## 每篇 Paper 的通用结构

<p align="center">
  <img src="./docs/assets/readme/zh/paper-structure.svg" width="100%" alt="ARIS4C 单篇 Paper 项目的通用结构">
</p>

所有编号项目遵循同一套仓库结构与交付契约；真正的研究设计、数据、分析、图表和审查门则由各自科学问题决定。

## 一篇 Paper 的生命周期

<p align="center">
  <img src="./docs/assets/readme/zh/paper-lifecycle.svg" width="100%" alt="ARIS4C 单篇 Paper 的生命周期">
</p>

## Final Paper 标准

一个 submission-ready / final 的 ARIS4C Paper 默认需要：

| 层 | 要求 |
|---|---|
| 论文 | 英文完整论文 + 中文完整论文 |
| 公开交付 | English PDF + 中文 PDF |
| 图表 | 根据论文真正的推断结构设计，**不固定 3 张图，也不固定图型** |
| 证据 | empirical / synthetic / conceptual provenance 可追踪 |
| 审查 | 对应的科学、复现、独立 review gate |
| 连续性 | `handoff/` 包含状态、TODO、决策、上下文、对话记录、Agent 接管说明和 session log |
| 公开入口 | Research Command Center 中的链接保持最新 |

详见 [**ARIS4C Final Output Standard · v3**](ARIS4C_OUTPUT_STANDARD.md)。

## 跨电脑 / 账号 / Agent 连续性

<p align="center">
  <img src="./docs/assets/readme/zh/handoff-package.svg" width="100%" alt="ARIS4C 跨 Agent 接管包">
</p>

每一个编号项目现在都有统一目录：

```text
papers/00X-project/
└── handoff/
    ├── README.md
    ├── STATUS.md
    ├── TODO.md
    ├── DECISIONS.md
    ├── CONTEXT.md
    ├── CHATLOG.md
    ├── AGENT_HANDOFF.md
    └── SESSION_LOG.md
```

新的执行者原则上只需要：

> **先读 `papers/00X-.../handoff/README.md`，然后从当前 Git 状态继续。**

公开仓库里的 CHATLOG 保存的是 **public-safe 的研究对话摘要**，不会写入 API key、私密凭证、不必要的个人敏感信息或模型隐藏 chain-of-thought。

## 仓库结构

```text
ARIS4C/
├── papers/
│   ├── dashboard.json             # portfolio canonical state
│   └── 00X-project/
│       ├── paper.json             # paper metadata
│       ├── manuscript/            # 中英文论文
│       ├── figures/ + tables/     # 科学图表
│       ├── code/ + data/          # 分析 / provenance
│       ├── process/               # 设计、gate、冻结决策
│       └── handoff/               # 跨 Agent continuity
├── docs/                          # GitHub Pages + public PDFs
├── tools/                         # generators + audits
├── ARIS4C_OUTPUT_STANDARD.md
├── ARIS4C_CONTINUITY_STANDARD.md
├── ARIS4C_STATUS_MODEL.md
└── aris.lock.json
```

## 重建与审计

```bash
python tools/build_papers_index.py
python tools/build_readme_assets.py
python tools/build_readme.py
python tools/audit_paper_outputs.py
python tools/audit_paper_handoffs.py
python tools/sync_paper_handoffs.py
```

## 设计原则

1. **唯一 canonical source of truth。** 多个对话框和 Agent 可以并行探索，但 Git 决定什么真正进入 main。
2. **先可证伪，再讲故事。** 更强的方法可以替代更弱的旧结论。
3. **图表服务证据，不服务配额。** 不固定 3 张图，以信息增益决定图型和数量。
4. **完成时默认双语。** Final public delivery 使用 English + 中文，并优先 PDF。
5. **研究必须可接管。** 如果换一个 Agent 就无法继续，这个项目在 operational 层面就还没完成。
6. **异常不是定罪。** Forensics 类项目保留 human review、证据边界和明确的不确定性。
7. **优先完成最接近完成的项目。** 000 先续跑真正的 Active；有空闲槽位时，从 Wait 中按进度从高到低启动，并在切换 Paper 前完成 bounded-unit Git checkpoint。

---

维护者：**Cochrane Kang**  
Research hub：**https://cochranek.github.io/ARIS4C/**
"""


def main() -> int:
    _, rows = load()
    zh_text = chinese(rows).rstrip() + "\n"
    en_text = english(rows).rstrip() + "\n"
    (ROOT / "README.md").write_text(zh_text, encoding="utf-8")
    (ROOT / "README.en.md").write_text(en_text, encoding="utf-8")
    # Legacy Chinese path stays valid for old links.
    (ROOT / "README.zh-CN.md").write_text(zh_text, encoding="utf-8")
    print(f"README generated for {len(rows)} papers.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
