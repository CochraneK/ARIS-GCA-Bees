# 方法 — 结果查看前锁定稿

**论文：** ARIS4C003《殖民遗产与全球学科优势的地理分布》  
**状态：** 研究设计已锁定、IKES 已冻结；撰写本稿时尚未查看三项 confirmatory coefficient。

## 1. 研究设计

本研究关注的不是“哪些国家科研更强”，而是历史殖民暴露是否与一个国家当代科研活动的**跨学科结构**相关，以及这种关系是否随各学科与帝国／殖民体系的历史纠缠程度系统变化。

核心解释项为：

**历史暴露 × Imperial/Colonial Knowledge Entanglement Score（IKES）**

研究严格区分三类 estimand：

1. **前殖民地国家层面：** 殖民暴露越深的国家，是否相对更集中于高 IKES 学科；
2. **国家对合作层面：** 历史上存在殖民／依附关系的国家对，是否在高 IKES 学科中保留更强的当代科研合作；
3. **八个欧洲海外殖民宗主国：** 仅作为 small-N corroboration，不把 8×21 个学科单元误当成大量独立历史处理单位。

全部分析均为关联性分析。固定效应能够吸收研究比较结构中的大量国家、学科、时期及国家对异质性，但不能使殖民经历成为外生处理。因此结果使用“相关”“预测”“与历史路径依赖一致”等表述，而不宣称已经识别“殖民主义导致当代科研优势”的因果效应。

## 2. 历史殖民暴露

### 2.1 国家层面

主要国家暴露来自 COLDAT 3.0。confirmatory exposure 为欧洲海外殖民统治累计年数；在 COLDAT 主口径中未被编码为殖民地的国家保持为 0。

COLDAT 中八个欧洲海外殖民强国——比利时、英国、法国、德国、荷兰、葡萄牙、西班牙和意大利——不进入主要 former-colony 回归，而被单独处理。

殖民年数在排除这八个宗主国后的冻结国家宇宙中进行中心化和标准化。历史管线最终解析出 **159 个当前国家**；原始累计殖民年数同时保留用于描述。

### 2.2 国家对层面

国家对历史关系来自 CEPII Gravity V202211。主要 pair exposure 为 `col_dep_ever`，表示两个当前国家之间历史上是否存在直接殖民／依附关系。

159 个冻结国家形成完整的 **12,561 个无序国家对**，其中 156 对具有 `col_dep_ever=1`。距离、共同语言等变量只作为次级或机制分析信息，不替代主殖民关系指标。

## 3. 冻结的 21 个学科与 OpenAlex crosswalk

现代结果打开前，研究冻结以下 21 个概念学科：

人类学、考古学、地理学、发展研究、语言学、热带医学／殖民健康相关公共卫生、农业与林业、地质／地球资源科学、社会学、政治学／国际关系、法学、经济学、公共管理／社会政策、教育学、历史学、人口学／人口研究、数学、物理学、化学、计算机科学和材料科学。

每个概念学科对应预先固定的 OpenAlex field 或 subfield selector。主分析依据每篇 work 唯一的 `primary_topic` roll-up 进行分类，因此一篇 work 不会同时进入多个 confirmatory 学科。基于任意 topic 命中的分类只作为敏感性分析，不替代主 crosswalk。

## 4. IKES

IKES 衡量的是：帝国／殖民体系在多大程度上实质性塑造了一个学科的制度形成、方法、研究对象与数据、训练体系、研究基础设施、职业扩张或去殖民后的连续性。

它不是：
- 学科的道德评分；
- 对个别学者政治态度的评分；
- 当代西方主导程度；
- 当前国家科研水平。

11 个冻结维度为：

1. 殖民行政需求；
2. 领土测量与制图；
3. 人口、人群或语言分类；
4. 海外田野点与远征；
5. 资源勘查与商业提取；
6. 殖民医学与卫生治理；
7. 农业、林业与生态转移；
8. 法律、教育与制度移植；
9. 博物馆、档案、收藏与标本；
10. 传教、语言与宗教网络；
11. 战后发展—行政连续性。

每个“学科 × 维度”单元按 0–3 评分；历史证据确实不足时允许 NA。2 或 3 必须得到较强的历史学术证据支持。

Coder A 首先完成 outcome-blind 历史编码。正式 Coder B 在隔离的 Qoder 上下文中完成；用户报告所用模型为 Qwen Flash 3.8。Coder B 的文件白名单明确排除了 Coder A、父项目上下文以及现代科研结果。

对未达到裁决阈值的单元，最终值固定为 A/B 的算术平均值，不允许人工覆盖。只有以下情况才允许 outcome-blind adjudication：

- 任一 coder 为 NA；
- A/B 绝对差值 ≥2。

231 个评分单元中共有 12 个达到上述条件。12 个单元均在第一次当代科研结果 materialization 之前，依据历史文献和冻结维度定义完成裁决。

最终 IKES 为 11 个可用维度的等权平均；维度中位数同时保留为预设敏感性指标。Coder A、Coder B 原始返回、证据说明、裁决表以及最终 `IKES_FROZEN.csv` 均通过 SHA-256 provenance 串联。

## 5. 当代科研数据

当代科研结果来自已固定 manifest 的 OpenAlex 公共 Parquet Works snapshot。

主要文献类型为：

- article；
- review；
- conference-paper；
- book；
- book-chapter。

排除：
- retracted works；
- `is_xpac=true` expansion corpus；
- preprint；
- dissertation；
- editorial / letter / correction / paratext；
- dataset / software 等非主要研究文献类型。

研究年份为 2007–2025。

主要成熟 confirmatory 时间窗为 **2019–2022**。

另外预先规定：

- 2007–2010；
- 2011–2014；
- 2015–2018；
- 2019–2022

用于 temporal persistence profile。

2023–2025 只作为近期**产出**敏感性窗口，不作为成熟 Top-10% impact 检验。

## 6. 国家 fractional attribution

对于每篇合格 work，先汇总其全部 authorships 中所有不同的、可识别的 OpenAlex 国家代码。

如果 work 有 (n) 个不同国家，则每个国家获得：

[
1/n
]

的 fractional credit。

关键点是：**先确定全部可识别国家的分母，再限制到冻结的 159 国分析宇宙。** 因此，如果一篇论文还包括分析宇宙外国家，留下来的国家不会被重新放大权重。

主要科研产出 outcome 为 country × discipline × period 中 fractional credit 的总和。

对一个有资格进入分析的 country-period，如果某一冻结学科真正没有产出，该单元显式补为 0，而不是删除。

## 7. 标准化影响力

主要 impact outcome 使用 OpenAlex 的：

`citation_normalized_percentile.is_in_top_10_percent`

该指标按 publication year、work type 和 primary subfield 标准化。

在每个 country × discipline × period 单元中：

- 分子 = Top-10% work 的 fractional mass；
- 分母 = 具有有效 normalized citation percentile 的 fractional work mass。

confirmatory impact model 使用 PPML rate 形式，并以：

[
log(	ext{impact denominator})
]

作为 offset。

FWCI 与 Top-1% 只作为次级指标。

## 8. 国家对合作 attribution

若一篇 work 有 (n) 个不同的可识别国家，则其总合作质量 1 平均分配给全部：

[
n(n-1)/2
]

个无序国家对，每一对获得：

[
2/[n(n-1)].
]

同样，分母必须在限制到 159 国分析宇宙**之前**确定。

这一实现细节在现代 outcome 首次 materialization 前再次审计并修正，因此含有宇宙外国家的 work 不会错误地把保留 pair 的总质量重新归一化到 1。

正合作单元随后与完整的 eligible CEPII pair × discipline × period 网格合并；真正没有合作的格子显式为 0。

## 9. 主要统计模型

### 9.1 前殖民地国家：科研产出

使用 PPML：

[
E(P_{cdt})
=
exp[
eta(Exposure_c 	imes IKES_d)
+
alpha_{c	imes t}
+
gamma_{d	imes t}
].
]

2019–2022 单一 headline 窗口中对应使用国家固定效应与学科固定效应。

PPML 在这里作为 nonnegative fractional outcome 的 quasi-maximum-likelihood estimator，能够保留真实 0；不要求 outcome 是整数，也不要求真实服从 Poisson distribution。

### 9.2 Top-10% impact

使用相同的 Exposure × IKES 交互结构，以 fractional Top-10% mass 为 outcome，并以 log eligible impact mass 为 offset。

### 9.3 历史殖民关系国家对合作

国家对模型为：

[
E(C_{ijdt})
=
exp[
eta(Tie_{ij}	imes IKES_d)
+
mu_{ij}
+
lambda_{i	imes d	imes t}
+
ho_{j	imes d	imes t}
].
]

其中：
- (mu_{ij}) = pair fixed effect；
- 两端国家 × discipline × period fixed effects 吸收广泛的国家特定学科—时期合作倾向。

核心交互检验的是：具有历史殖民关系的国家对，是否具有不同的 IKES 跨学科合作梯度。

## 10. Confirmatory family 与推断

confirmatory family 固定只有三项：

1. 2019–2022 former-colony output：Exposure × IKES；
2. 2019–2022 former-colony Top-10% impact：Exposure × IKES；
3. 2019–2022 former-colonial-tie collaboration：ColonialTie × IKES。

国家模型按 country 与 discipline 进行 multiway CRV1 clustering；国家对模型按 pair 与 discipline clustering。

由于研究学科只有 21 个，渐近标准误之外还预设 finite-field falsification。

每个 headline coefficient 必须完整报告：

- 21 次 leave-one-discipline-out；
- seed=20260918 的 999 次 IKES-label permutation；
- median-IKES 敏感性；
- 国家模型的 mapped country-period output ≥50 与 ≥200 敏感性。

任何 permutation 或 LOO refit 失败，都必须将该 robustness layer 明确标为 invalid，不允许仅保留成功的 refit。

## 11. 时间持续性

对以下成熟时期完整报告 output、Top-10% impact 与 dyad collaboration 的交互估计：

- 2007–2010；
- 2011–2014；
- 2015–2018；
- 2019–2022。

2023–2025 只报告 output。

这些 period-specific estimates 属于 secondary temporal profile，不扩展三项 confirmatory family。

## 12. 八个宗主国的 small-N corroboration

八个 COLDAT 宗主国只有 8 个独立历史单位，因此单独处理。

对每个宗主国，根据 21 个冻结学科计算 symmetric revealed comparative advantage（SRCA），并估计其 SRCA–IKES profile slope。

随后描述性考察 profile slope 与 log cumulative colony-years 的关系，并报告：

- 八国原始 profile slope；
- leave-one-empire-out；
- 999 次 IKES-label permutation。

该部分明确是 corroboration，不属于大样本因果推断。

## 13. 可复现性与首次结果锁定

研究设计、历史暴露、学科 crosswalk、IKES rubric、Coder A/B、裁决、模型 specification 和实现修正均版本化在仓库中。

第一次现代 outcome materialization 之前，strict gate 已真实返回：

- `DESIGN_LOCKED`
- `OUTCOME_UNLOCKED`
- 0 个 design problems
- 0 个 outcome problems

首次完整结果包由自动 workflow 生成；三条 headline、完整 LOO、3×999 permutation、temporal profile 和 imperial corroboration 必须全部完成后，结果文件会先计算 SHA-256 并生成 `FIRST_RESULT_LOCK.json`，随后才允许人工解释。

主图和主表也已在结果查看前冻结，因此不能因为结果为 null、方向相反或不显著而删除不利图表。
