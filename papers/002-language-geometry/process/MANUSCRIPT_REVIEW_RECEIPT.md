# Paper 002 Manuscript Review Receipt

## Reviewer identity
- provider/app: WorkBuddy platform（非 primary manuscript writer 的 OpenAI GPT / ChatGPT 族）
- exact model: hy3（WorkBuddy 默认模型族）
- model family: 非 OpenAI GPT 族（STATUS.md 记录为 Tencent Hunyuan；primary manuscript writer 为 OpenAI GPT）
- independent from primary manuscript writer: YES
- fresh session: YES（本审阅在独立新会话中完成，无 primary-executor 上下文延续）
- trace/session ID: ARIS4C-paper002-manuscript-review-workbuddy-hy3
- timestamp: 2026-09-18T07:31:00Z
- literature search cutoff: 2026-09-18（已通过 WebSearch 独立检索）

## Verdict
**PASS_SUBMISSION_PREP**

> 本审阅由非 OpenAI GPT 族的 WorkBuddy/hy3 独立完成，满足 ARIS 对 manuscript-stage「different model family」的独立性要求。若日后披露本模型底层实际属于 OpenAI GPT 族，integrator 须重新评估独立性。

## Executive assessment

Draft v1 是一份纪律良好的诊断性（约束性）论文草稿。它完整兑现了 idea-stage 二级审阅施加的五条强制边界（bootstrap 仅量化分割敏感性、Stage 1–1I 标 exploratory、保留 WALS vs TLI/GBI 地理矛盾、仅测「简单全局圆」强形式、报告每阶段 N/特征/效应量），数值在 DRAFT/TABLES 与源报告及 MANUSCRIPT_AUDIT 之间一致，方法学描述与 `stage1*.py` 实现对齐，且我在独立文献检索下未发现致命新颖性碰撞。论文未出现任何越界的因果/普遍/「语言是树」/「周期性被全盘否定」表述。剩余仅为编辑/排版层面工作，故给出 `PASS_SUBMISSION_PREP`，授权进入目标期刊格式化阶段。

## Novelty and literature

独立 WebSearch（2026-09-18）确认：
- **Kemp (2026, Nat Commun 17:358)** 测的是**特定语义域**（季节、月相、方位）内的对称/双分圆结构，与本文「跨语法/词汇/音系异构结构特征的单一全局圆」是不同科学层次；本文已在 Intro/Discussion 显式区分「domain-grounded circularity」与「global feature-space circularity」。无碰撞。
- 其余命中（generative-syntax「cyclicity」理论、低质量 general typology 分类文、Linguasphere 编目）均不构成「全局圆 vs 树/图/低秩/空的跨样本预测竞争」。
- 与既有 WORKBUDDY 侧 2026-09-18 文献重扫结论一致：**NO_NEW_FATAL_COLLISION_FOUND**，新颖性楔子（显式全局圆压力测试 + 直接闭合/环形诊断 + 多表示复制）未被占据。

## Methods-to-code fidelity

核对 `ideas/language-periodic-system/` 源脚本：
- `stage1.py`：N_FEATURES=60、MIN_FEATURE_OBS=180、MAX_CARDINALITY=15、MIN_PAIR_OBS=60、先按 coverage 后按 lower-cardinality 排序、`average_method="arithmetic"`（NMI 算术归一化）、环形核 `cos(d)+cos(2d)`、tree=average linkage + cophenet。与 §2.1/§2.3 一致。
- `stage1b.py`：直接 (n−1) 角优化、feature 0 固定为 0 去除旋转不可辨识、L-BFGS-B、两谐波。与 §2.3「直接优化」描述一致。
- `stage1c.py` 第 228 行域级局部周期门：`periodic≥0.15 and periodic≥best−0.03 and stability≥0.40`，与 §2.6 / Table 4 完全一致。
- 说明：`stage1.py` 第 414 行的 `0.35` 是主全局屏中的**独立预备内部检查**，并非 Stage 1C 域门（后者用 0.40）；两者针对不同分析，不影响 Table 4 分类结论，故不构成结果级不一致。

## Results-to-source fidelity

DRAFT/TABLES 关键数与源报告及 MANUSCRIPT_AUDIT 交叉一致：
- TLI：tree 0.182 vs circle 0.109，Δ+0.073，split-bootstrap CI [0.055,0.092]，20/20 树胜；low-rank 也胜圆（Δ+0.046 CI[0.033,0.061]）。
- GBI：tree 0.122 vs circle 0.073，12/12。
- WALS：tree 0.603 vs circle 0.410，8/8；macroarea transfer 0.634±0.075。
- 60 特征闭合比 0.037（弱 wrap-around 闭合）；40 特征 0.608±0.764（SD 极大，非信息性估计）。
- Stage 1 单次分割 tree 0.178 vs Stage 1F 20 分割均值 0.182 的差异已在文中以不同 stage 标签区分，无混淆。

## Statistical/reporting adequacy

- bootstrap 在 §2.9、§3.6、Table 1 注释、Figure 2 图注均明确「量化分割敏感性，非系统发育不确定性」。✓
- Stage 1–1I 多重性在 §1.2、§2.5、§5.1 披露，未主张族-wise 校正错误率。✓
- 每阶段 N、特征数、选择规则、效应量与 CI 在 Table 6 与正文报告。✓
- 20 分割偏少（STATUS 已列为可选）；非阻断。

## Claim-boundary audit

- 允许的中心结论在 §1.2 与 §6 逐字复现，未扩大。
- 未出现：语言是树、所有周期性不可能、地理异质性普遍化、统计几何证明普遍语法/因果、家族保留去除谱系/接触依赖。
- 标题「Predictive Evidence Favors Non-Circular Structure」是允许的负向/约束结论的合理标题化；虽轻微偏向（证据偏向非圆**模型**而非断言语言具非圆**本体结构**），但摘要与结论措辞严谨，不构成越界。列为可选收紧（见下）。

## Figures/tables audit

- Figure 1/2/3 图注均明确「绝对值不应跨数据集直接比较」「bootstrap 区间为分割敏感性非系统发育不确定性」。✓（直接回应 handoff §11）
- Table 2/5 均含「勿直接跨行比较绝对效应量」警告。✓
- 三张 SVG 已在 CI 中重新生成，manifest/claim 边界受 GitHub Actions 校验（STATUS 记录 CI SUCCESS）。✓

## Blocking scientific changes
（无）

## Blocking manuscript changes
（无）

## Optional improvements
- 标题「Predictive Evidence Favors Non-Circular Structure」可微调以避免被读作「语言是非圆形的本体断言」（证据偏向非圆模型胜过被测全局圆；结论为负向/约束）。例如改为强调「…Does Not Support a Global Circular Organization」。非阻断。
- 在 `stage1.py` 第 414 行附近加一行注释，说明 `0.35` 内部预备屏与 Stage 1C 的 `0.40` 门为不同分析（纯代码可读性，无结果影响）。
- 40 特征闭合比 0.608±0.764（SD>均值）建议在正文更显式标注为「不稳定/非信息性估计」而非可比较数值。
- 可选（非要求）：50–100 家族保留分割 或 系统发育敏感性补充（STATUS 已列可选）。

## Maximum permitted claim
> The global-circle form of the language periodic-table hypothesis tested here is not supported by predictive and held-out circularity evidence; hierarchical/non-circular models provide stronger family-held-out benchmarks across TLI, GBI, and WALS, without establishing one universal tree geometry.

## Submission-prep authorization
**AUTHORIZED**

## Evidence inspected
- papers/002-language-geometry/manuscript/DRAFT.md
- papers/002-language-geometry/manuscript/TABLES.md
- papers/002-language-geometry/manuscript/FIGURE_CAPTIONS.md
- papers/002-language-geometry/process/CLAIMS_EVIDENCE_MATRIX.md
- papers/002-language-geometry/process/REVIEW_REQUIREMENTS.md
- papers/002-language-geometry/process/DATA_PROVENANCE.md
- papers/002-language-geometry/process/MANUSCRIPT_AUDIT.md
- papers/002-language-geometry/process/LITERATURE_RESCAN_2026-09-18.md
- papers/002-language-geometry/process/STATUS.md
- papers/002-language-geometry/process/WORKBUDDY_MANUSCRIPT_REVIEW.md
- papers/002-language-geometry/process/SECONDARY_REVIEW_RECEIPT.md
- ideas/language-periodic-system/stage1.py, stage1b.py, stage1c.py, stage1d.py, stage1i.py
- 独立 WebSearch 2026-09-18（periodic table of languages circular geometry predictive; language periodic hypothesis circular typology held-out prediction tree vs circle; Kemp 2026 symmetry categories）

## Reviewer integrity statement
我在独立新会话中审阅了本手稿，独立重跑了针对性文献检索，并对照源脚本核查了方法学—代码一致性。我不属于撰写手稿的 OpenAI GPT 模型族。本审阅不是对 primary executor 摘要的简单认可，而是基于证据给出 PASS_SUBMISSION_PREP，并将两条轻微可选改进（标题措辞、0.35/0.40 注释）与若干可选增强分开列出。
