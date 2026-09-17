<p align="right">
  <a href="./README.md"><img src="https://img.shields.io/badge/Language-English-blue" alt="English"></a>
  <a href="./README.zh-CN.md"><img src="https://img.shields.io/badge/语言-中文-red" alt="中文"></a>
</p>

<div align="center">

# ARIS4C

**ARIS for Cochrane · 持续使用 ARIS 产出论文的长期研究母仓库**

[**论文总览**](docs/index.html) · [**论文注册表**](papers/) · [**Paper 001**](docs/paper/zh/main.html) · [**English**](README.md)

</div>

## ARIS4C 是什么？

**ARIS4C = ARIS for Cochrane。** 它是用于长期保存和展示通过 [ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) 方法持续完成的研究与论文的母仓库。

这个仓库最初从 GCA × Bees 的理论建模与计算模拟项目开始，现在扩展为后续论文统一使用的长期研究空间。

核心原则是把“研究引擎”和“研究资产”分开：

- **ARIS 是研究引擎**，可以持续跟随上游升级；
- **ARIS4C 是研究档案与论文展示层**，用于保存 Cochrane 的 ARIS 辅助研究；
- **每篇论文记录实际使用的 ARIS 版本或 commit**，以后升级 ARIS 不会篡改旧论文的历史；
- **公开 HTML 首页从论文 manifest 自动生成**，不再手工维护论文卡片。

## 仓库模型

```text
ARIS4C/
├── papers/
│   ├── 001-gca-bees/
│   │   └── paper.json           # 第一篇论文的 manifest
│   └── 002-next-paper/
│       ├── paper.json
│       ├── code/
│       ├── data/
│       ├── figures/
│       ├── manuscript/
│       └── process/
├── docs/
│   └── index.html               # 自动生成的论文总览页
├── tools/
│   ├── new_paper.py             # 一键创建下一篇论文
│   ├── build_papers_index.py    # 生成论文总览 HTML
│   └── sync_aris.ps1            # Windows 下同步最新版 ARIS
├── aris.lock.json               # 仓库级 ARIS 更新策略
├── code/                        # Paper 001 的旧代码位置
├── process/                     # Paper 001 的旧 ARIS 过程记录
└── simulation_results*.json     # Paper 001 的旧输出
```

为了不打断现有论文内部链接，Paper 001 暂时保留原来的根目录结构；从 Paper 002 开始直接使用新的编号式结构。

## 开始下一篇论文

```bash
python tools/new_paper.py "你的论文标题" --slug short-name
```

脚本会自动分配下一个论文编号，并创建标准研究目录。正式运行 ARIS 前，把当时实际使用的 ARIS tag 和 commit 写入该论文的 `paper.json`。

## 如何持续同步最新版 ARIS

ARIS 本体**不复制进 ARIS4C**。Windows 下建议把 ARIS 保存在独立位置，并运行：

```powershell
./tools/sync_aris.ps1
```

这个脚本会自动 clone 或 pull ARIS 上游、记录当前 tag/commit；如果检测到 Bash，还会走 ARIS 官方的 smart update 路径。所有本机 ARIS 状态均被 `.gitignore` 排除。

当前 `aris.lock.json` 推荐版本为 **ARIS v0.4.26**。旧论文不会因为升级而被重新标成新版本。

## 自动更新 HTML 论文总览

手动执行：

```bash
python tools/build_papers_index.py
```

此外已经加入 GitHub Action：当 `main` 上的论文 manifest 变化时，会自动重建 `docs/index.html`。因此以后增加 Paper 002、003、004……时，不需要再手工改首页。

## Paper 001 · GCA × Bees

**A Unified Predictive Coding Account of Functional Self-Awareness in Bees: Analytically Derived Precision Trade-offs Across Four Behavioral Domains**

目前仍属于理论 + 模拟阶段。模型中的关系、方向变化与预测是计算生成的假设，不是蜜蜂具备某种自我意识或相关神经机制已经被实证证明的证据。

- [中文论文](docs/paper/zh/main.html)
- [English manuscript](docs/paper/en/main.html)
- [研究流程报告](process/RESEARCH_PIPELINE_REPORT.md)
- [Idea Report](process/IDEA_REPORT.md)
- [Auto Review](process/AUTO_REVIEW.md)

## 原则

> 升级研究引擎，但保留研究历史。

维护者：**Cunyi Kang**
