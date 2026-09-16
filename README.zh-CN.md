<p align="right">
  <a href="./README.md"><img src="https://img.shields.io/badge/Language-English-blue" alt="English"></a>
  <a href="./README.zh-CN.md"><img src="https://img.shields.io/badge/语言-中文-red" alt="中文"></a>
</p>

<div align="center">

# ARIS-GCA-Bees

**蜜蜂功能性自我意识的理论建模与计算模拟项目**

<p>
  <img alt="Stage" src="https://img.shields.io/badge/阶段-理论%20%2B%20模拟-6C63FF">
  <img alt="Domain" src="https://img.shields.io/badge/方向-计算神经行为学-2F80ED">
  <img alt="Pipeline" src="https://img.shields.io/badge/流程-ARIS-27AE60">
</p>

[**网页包**](docs/index.html) · [**研究流程**](process/RESEARCH_PIPELINE_REPORT.md) · [**中文论文**](docs/paper/zh/main.html) · [**English manuscript**](docs/paper/en/main.html)

</div>

## 项目简介

ARIS-GCA-Bees 是一个通过 [ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) 自动化研究流程推进的计算神经行为学项目。

项目提出一个关于**蜜蜂功能性自我意识的预测编码解释框架**，并通过模拟探索共同潜变量 **precision（精度）** 是否能统一组织四类建模行为：

- 元认知放弃行为；
- 工具使用预期；
- 与阶层角色相符的学习；
- 一般认知能力（GCA）。

> [!IMPORTANT]
> 本仓库当前处于**理论 + 模拟**阶段。README 中的关系、符号翻转与机制解释属于模型产生的假设和预测，不是“蜜蜂已被实验证明具有某种自我意识”或“相应神经机制已被体内验证”的证据。

## 当前模型关注的预测

在当前模型中，项目主要探索：

- 元认知表现与 precision 之间可能出现倒 U 型关系；
- 某些参数条件下，更高的模型 GCA 可能伴随更差的元认知校准；
- 昼夜节律扰动可能改变模型中的元认知–GCA 关系方向。

因此，本项目更适合作为**概念形式化、计算模拟、可检验预测生成与研究流程打包**来阅读。

## 当前仓库结构

旧 README 仍描述了已经迁移掉的根目录 `paper/`、`figures/` 和 `results/`。当前真实结构为：

```text
ARIS-GCA-Bees/
├── code/                         # 模拟代码
│   ├── experiment_r2_4domain.py
│   ├── experiment_unified_selfmodel_full.py
│   └── pilot_*.py
├── docs/                         # 网页 / 论文发布包
│   ├── index.html
│   ├── zh.html
│   ├── figures/
│   └── paper/
│       ├── en/
│       ├── zh/
│       ├── sections/
│       └── references.bib
├── process/                      # 研究生成过程记录
│   ├── IDEA_REPORT.md
│   ├── AUTO_REVIEW.md
│   ├── PAPER_PLAN.md
│   └── RESEARCH_PIPELINE_REPORT.md
├── simulation_results.json
├── simulation_results_r2.json
├── README.md
└── README.zh-CN.md
```

## 从哪里开始

| 想看什么 | 入口 |
| --- | --- |
| 整个研究生成过程 | [研究流程报告](process/RESEARCH_PIPELINE_REPORT.md) |
| 最初的 idea 如何形成 | [IDEA_REPORT](process/IDEA_REPORT.md) |
| 自动评审与问题记录 | [AUTO_REVIEW](process/AUTO_REVIEW.md) |
| 中文论文 | [docs/paper/zh/main.html](docs/paper/zh/main.html) |
| 英文论文 | [docs/paper/en/main.html](docs/paper/en/main.html) |
| 网页入口包 | [docs/index.html](docs/index.html) |

## 复现主模拟

```bash
python code/experiment_r2_4domain.py
```

其他 pilot 与完整模拟脚本位于 `code/`；当前数值输出位于根目录的 `simulation_results.json` 与 `simulation_results_r2.json`。

## 研究流程

```text
想法发现
→ pilot 测试
→ 完整模拟
→ 自动评审循环
→ 论文规划
→ 论文撰写
→ 网页 / 稿件打包
```

## 工作论文

**A Unified Predictive Coding Account of Functional Self-Awareness in Bees: Analytically Derived Precision Trade-offs Across Four Behavioral Domains**

当前为研究工作稿，并非已经发表的经验研究论文。

## 引用方式

正式发表前若需引用本仓库，可暂写为：

```text
Kang, C. (2026). ARIS-GCA-Bees: A unified predictive coding account of functional self-awareness in bees. GitHub repository.
```

## 联系

维护者：**Cunyi Kang**

问题、建议或合作可通过 GitHub Issue 提交。
