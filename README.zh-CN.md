<p align="right">
  <a href="./README.md"><img src="https://img.shields.io/badge/Language-English-blue" alt="English"></a>
  <a href="./README.zh-CN.md"><img src="https://img.shields.io/badge/语言-中文-red" alt="中文"></a>
</p>

<div align="center">

# ARIS4C

**ARIS for Cochrane · 使用 ARIS 持续推进论文的长期研究母仓库**

[**论文总览**](docs/index.html) · [**论文注册表**](papers/) · [**Paper 001**](docs/paper/zh/main.html) · [**English**](README.md)

</div>

## ARIS4C 是什么？

ARIS 是研究引擎；ARIS4C 是论文注册表、证据链、代码与公开展示层。每一篇正式论文都在 papers/ 下拥有独立编号目录，并记录实际使用的 ARIS 版本与 commit。

## Paper 001 已完全重构

**Uncertainty Monitoring and Cross-Task Cognitive Covariation in Honey Bees**  
**蜜蜂的不确定性监测与跨任务认知协变**

2026-09-18 起，001 不再以旧版“单一 precision → 自我意识”模拟作为 canonical 论文。旧代码中通过同一个手工设定的 latent 参数生成多个变量，再用这些变量之间的高相关作为模型验证，这种证据链已被废弃。

新版 001 改为可证伪的模型比较：

1. 单一一般因子；
2. 学习/GCA 与不确定性控制两个相关因子；
3. 两个独立因子；
4. 纯任务局部的联结学习模型；
5. 个体稳定差异 + trial-level 联结过程的混合模型。

precision、预测编码、central complex、自我意识等解释只保留为探索性候选，必须在真实同个体数据上优于更简单模型后才能升级为结论。

- [中文研究设计](docs/paper/zh/main.html)
- [English research design](docs/paper/en/main.html)
- [001 canonical 目录](papers/001-gca-bees/)
- [当前状态与研究门](papers/001-gca-bees/process/STATUS.md)

## 当前 ARIS

仓库当前推荐 **ARIS v0.4.26**。新版 001 使用 commit 951654847b015585385b2448c5667dcd04e7b56b。

## 原则

> 研究引擎可以升级；当明确决定重构一篇论文时，更强的方法也可以替换旧的 canonical 结论。旧版本仍可由 Git 历史追溯。

维护者：**Cunyi Kang**
