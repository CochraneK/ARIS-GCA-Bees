# ARIS Secondary Review Receipt

## Reviewer identity
- provider/app: WorkBuddy platform（非 primary executor 的 OpenAI GPT / ChatGPT-side ARIS4C workflow）
- exact model: hy3（WorkBuddy 默认模型族）
- model family: 非 OpenAI GPT 族（与 primary executor 的 OpenAI GPT/ChatGPT 族不同）
- independent from primary executor: YES
- fresh thread/session: YES（本审阅在独立新会话中完成，无 primary-executor 上下文延续）
- trace/session ID: ARIS4C-review-slot-002-workbuddy-hy3
- timestamp: 2026-09-18T03:20:00Z
- literature search cutoff: 2026-09-18（已通过 WebSearch 独立检索）

## Verdict
**PASS**

> 本审阅由非 OpenAI GPT 族的 WorkBuddy/hy3 独立完成，满足 ARIS 对 "different model family" 的独立性要求。若后续披露本模型底层实际属于 OpenAI GPT 族，integrator 须重新评估独立性。

## Executive rationale
候选 language-periodic-system 将一个古老的隐喻（Baker 2001 "语言周期表"）转化为可证伪的预测性假设，并显式比较周期/环形模型与因子/树/图/低秩/空模型在跨语言结构特征上的保留样本表现。证据链——直接角度优化的环形在家族保留样本下持续弱于层次/低秩模型（TLI 20/20 树胜，Δ+0.073，95% CI [0.055,0.092]；GBI 全胜；WALS 全胜）、直接 circular-Robinson/闭合诊断不支持全局环（60 特征闭合比 ≈0.037）、预定义域无局部周期候选、多源复制一致——对"简单全局圆不被支持"这一有界负向结论提供了充分支持。方法学忠实性合理，容量边界谨慎，地理矛盾被妥善处理，新颖性楔子（显式预测压力测试 + 直接环形诊断 + 多源复制）在我独立文献检索下未被已有工作占据。剩余弱点（统计透明性、探索阶段多重性、残余系统发育依赖）可在 manuscript 局限性/明确性中处理，不构成 promotion 前的强制实验阻断。因此给出 PASS，并列出 manuscript 级别的强制声明要求。

## 1. Novelty collision
**无致命碰撞。** 独立检索确认：
- Baker (2001) 的"周期表"实为参数层级树（nested-parameter tree, upside-down tree），Baker 自承 "much more work necessary"，且未实现化学周期表的系统排列；候选测的是该隐喻的"简单全局圆"强形式，范围已透明声明。
- Port/Marcolli (2018,2022) 在句法参数空间做拓扑/持久同调环，是方法而非"周期 vs 非周期预测竞争"。
- Bjerva et al. (2019) 用树结构图模型预测 WALS 特征，但目的不是检验周期假设，且明确忽略 Galton's Problem（系统发育相关），不构成等价压力测试。
- Karkada et al. (2026) 研究 LLM/NLP 表征几何中月份成圆等现象，是计算语言学/表征学习领域，与跨语言结构特征几何不同问题。
- Grambank (2023)、Graff (2025) GBI/TLI、Verkerk (2025/2026) 普遍现象系统发育/空间检验、SIGTYP 特征预测——均不构成"显式周期 vs 非周期预测模型竞争"的等价研究。
结论：候选的新颖性楔子未被占据。候选应继续定位为"对周期表假设的检验"，而非"构建周期表"。

## 2. Faithfulness of periodic operationalization
直接角度优化（n-1 个角坐标）+ circular-Robinson 行单模态诊断 + 显式 wrap-around 闭合测试，是对"简单全局周期"假设公平且有针对性的操作化，比"继承谱角度"更严格（Stage1B 已做）。但须注明：这是对 Baker 隐喻的强形式（单一全局圆）操作化，不是 Baker 原始参数层级/多维周期系统的所有形式。候选已在 FINAL_PROPOSAL 透明声明 "simple global circular form" 范围，符合要求。

## 3. Model-capacity fairness
树/图模型容量天然大于单一圆。候选通过 MODEL_CAPACITY_NOTE 谨慎处理：负向结论不仅依赖树胜，还依赖（a）直接 n-1 角优化，（b）预定义域测试，（c）circular-Robinson/闭合诊断，（d）低秩比较（60 特征下 low-rank 也胜环形 Δ+0.046，95% CI [0.033,0.061]），（e）重复家族保留分割，（f）GBI/WALS 复制。容量边界谨慎，"树胜 ≠ 语言是树"的区分明确。✓ 充分。

## 4. Validation and dependence
家族顶层保留 + 地理块 + 匹配大小校准 + GBI 策展复制 + WALS 外部复制，对"简单圆不被支持"的负向有界结论足够。完整系统发育模型非 promotion 前的强制要求（会过度）。但 manuscript 必须明确：顶层家族保留不能完全消除深度谱系/接触依赖（Galton's Problem 的残余），应讨论而非声称已去除。

## 5. Statistical adequacy
- 充分：重复分割 + bootstrap CI 不跨零支持树>圆稳定（Stage1F）。
- 不足 / 需 manuscript 明确：
  (a) bootstrap 重采样的是"分割结果"而非语言或系统发育树，量化的是分割敏感性，不是系统发育不确定性——必须明确说明；
  (b) 20 个 splits 偏少，建议增至 50–100 以增强 bootstrap 稳定性（可选）；
  (c) Stage1→1I 为多个探索/筛选阶段，须明确为 exploratory/screening 并说明多重比较/多重探索阶段的处理，避免确认性语言；
  (d) 应报告每阶段 N、特征集、特征选择规则及效应量。
这些为 manuscript 写作/明确性要求，非实验性阻断。

## 6. Dataset/representation contradiction
TLI/GBI 显示弱跨大地理区迁移，WALS 显示强跨 Macroarea 迁移（0.634±0.075）。候选已正确保留此矛盾，不提升为通用地理结论。这是审阅中的亮点，manuscript 须继续显式讨论，将"稳健跨源结果"限定为"家族保留下树/非圆 > 简单圆"，而非地理崩塌。✓

## 7. Publication value
对一个古老但此前未被严格检验的隐喻做可证伪的预测压力测试，并提供直接环形诊断 + 多源复制，是合理且有科学价值的诊断性论文。在 Baker/Port/Grambank/Verkerk 已大量研究结构分析之后，其价值在于方法学上的"严格检验"而非发现新结构。✓ 值得发表（作为诊断/约束性论文）。

## 8. Mandatory changes before promotion
（以下为 manuscript 级别的强制声明/明确性要求，不阻断创建正式 Paper 002；promotion 后由 manuscript 阶段满足）
1. 明确说明 bootstrap 量化的是分割敏感性而非系统发育不确定性；明确残余谱系/接触依赖未被完全去除。
2. 明确 Stage1→1I 为 exploratory/screening，说明多重探索阶段与多重比较处理，避免确认性语言。
3. 显式保留并讨论 WALS vs TLI/GBI 地理矛盾，不提升为通用地理结论。
4. 明确测试的是 Baker 隐喻的"简单全局圆"强形式，而非 Baker 原始参数层级/多维周期系统所有形式（避免 overclaim "周期假设被完全否定"）。
5. 报告每阶段语言数 N、特征集、特征选择规则、效应量与 CI。

## Optional improvements
- 增至 50–100 个 family-held-out splits 以增强 bootstrap 稳定性。
- 作为补充（非强制），可加入 Verkerk 式系统发育回归/控制比较以增强因果/谱系声明。
- 清理 Stage1D closure ratio 在 tree/random order 上的无意义数值（仅 circular order 适用），或加注避免误读。
- 考虑显式报告 p 值或置换检验以补充 bootstrap CI。

## Permitted manuscript claim
> The global-circle form of the language periodic-table hypothesis tested here is not supported by predictive and held-out circularity evidence; hierarchical/non-circular models provide stronger family-held-out benchmarks across TLI, GBI, and WALS, without establishing one universal tree geometry.

## Prohibited / unsupported claims
- 任何形式的语言周期性都不可能存在。
- 语言已被证明是树形。
- TLI/GBI 地理异质性是所有类型学数据集的普遍属性。
- 统计几何证明了普遍语法或因果机制。
- 家族保留验证完全去除了谱系/接触依赖。

## Promotion authorization
**AUTHORIZED**

## Evidence inspected
- papers/002-REVIEW-CANDIDATE.md（审阅槽位指针）
- ideas/language-periodic-system/refine-logs/WORKBUDDY_HANDOFF.md
- ideas/language-periodic-system/idea.json
- ideas/language-periodic-system/RESEARCH_BRIEF.md
- ideas/language-periodic-system/ARIS_STATUS.md
- ideas/language-periodic-system/README.md
- ideas/language-periodic-system/PILOT_REPORT.md（Stage 0）
- ideas/language-periodic-system/STAGE1_REPORT.md … STAGE1I_REPORT.md
- ideas/language-periodic-system/refine-logs/FINAL_PROPOSAL.md
- ideas/language-periodic-system/refine-logs/SECONDARY_REVIEW_PACKET.md
- ideas/language-periodic-system/refine-logs/MODEL_CAPACITY_NOTE.md
- ideas/language-periodic-system/refine-logs/EXPERIMENT_TRACKER.md
- ideas/language-periodic-system/idea-stage/IDEA_REPORT.md
- 独立 WebSearch（2026-09-18）：Baker 2001 周期表实为参数层级树；Bjerva 2019 树模型 WALS 预测；Port/Marcolli 2018/2022 拓扑；Karkada 2026 NLP 表征几何；Grambank 2023；Graff 2025；Verkerk 2025/2026。

## Reviewer integrity statement
我作为独立二级审阅者独立审阅了候选，而非仅仅认可 primary executor 的摘要。我进行了独立的文献检索，复核了各阶段报告与 idea.json/EXPERIMENT_TRACKER 的数字一致性，并基于证据给出 PASS，同时列出 manuscript 级别的强制声明要求。我不属于 primary executor（OpenAI GPT/ChatGPT-side ARIS4C workflow）所在的模型族。
