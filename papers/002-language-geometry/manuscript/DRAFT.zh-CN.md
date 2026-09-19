# 检验人类语言的“周期表”假说：预测证据不支持全局环形组织

**Paper 002 · ARIS4C**  
**作者：** Cochrane Kang  
**中文稿状态：** 与英文投稿准备稿同步的完整中文版  
**独立 ARIS 审查：** PASS（WorkBuddy / Tencent Hy3）  
**实质性证据截止：** 2026-09-18

> **版本说明：** 本文为 Paper 002 英文稿的中文完整版本，用于 ARIS4C 双语交付、公开阅读与内部审查。所有统计数值、方法边界与结论强度均与英文稿保持一致；如后续英文投稿稿因期刊编辑产生纯格式调整，科学结论仍以经过独立审查冻结的 bounded claim 为准。

## 摘要

“人类语言是否存在类似元素周期表的组织方式”是一个很有吸引力的科学设想，因为它暗示看似高度多样的语法，可能由某种反复出现、相对紧凑的结构系统生成。然而，“周期表”作为隐喻本身并不是统计模型。现代语言类型学数据库使我们可以提出一个更尖锐的问题：一个简单的全局周期几何，能否比非周期替代模型更好地预测语言结构特征之间的关系？

本研究将一种强而有意受限的“周期性”操作化为：所有结构特征共同位于一个单一全局圆环上。模型仅在训练语言中估计特征—特征标准化互信息（normalized mutual information, NMI），再在留出语言中独立估计 NMI，并比较模型对该留出关联结构的预测能力。我们将圆环模型与低秩、二维欧氏、层级树、图以及零模型进行比较，并逐步加入顶层语言家族留出、预定义结构域、直接的 circular-Robinson 风格诊断、地理区块、重复划分不确定性、GBI 替代清理表示，以及单独处理的稀疏 WALS 表示。

在 20 次 TLI 家族留出划分中，层级树基线的平均 Spearman 相关为 0.182，而直接优化的圆环模型为 0.109；配对差异为 +0.073，基于划分层面的 bootstrap 95% CI 为 [0.055, 0.092]，20/20 次划分中树模型都更高。相同的定性排序也出现在 GBI（0.122 vs 0.073）和 WALS（0.603 vs 0.410）中。直接圆环诊断同样没有显示稳健的首尾闭合：在 60 个 TLI 特征时，圆环首尾边与内部相邻边的相似度比仅为 0.037。所有预定义 TLI 结构域中，也没有任何一个同时满足预测竞争力与圆环顺序稳定性的局部周期候选标准。

这些分析不能证明语言存在一个普遍树形几何，也不能排除所有可能形式的语言周期性。它们所限制的是一个明确的“单一全局圆环”版本：跨语言结构中确实存在可复现的秩序，但我们所检验的全局周期几何并不是对该秩序最有力的留出预测解释。地理可迁移性还明显依赖数据表示，这进一步说明，对“全球语言结构几何”的结论高度依赖数据库构造与抽样方式。

**关键词：** 语言类型学；圆形排序；类型学数据库；模型比较；语言共性

## 1. 引言

人类语言在语序、形态、音系、词汇结构以及语法范畴表达方式上表现出广泛差异。语言类型学长期以来一直追问：这种多样性是否占据一个受约束的“设计空间”，而不是一组彼此无关的任意可能性。

在原则与参数传统中，Baker（2001）将这一设想表达得尤其鲜明：如果语法参数具有足够稳定、反复出现的组合关系，那么最终也许可以形成一张“语言周期表”——用一个紧凑系统概括已观察到的语言，并进一步约束可能但尚未观察到的语言系统。

这一类比很有启发性，但它并不是一个单一、明确的统计假说。Baker 自己最终给出的主要结构更接近参数层级，而不是字面意义上的圆形周期表。此后的大规模定量研究已经证明，跨语言结构既不是随机的，也不是彼此独立的。Grambank 覆盖两千多种语言，展示了广泛的形态句法差异，并显示非常强的谱系结构（Skirgård et al., 2023）。Graff 等（2025）进一步构建 GBI 与 TLI，以减少结构特征之间的逻辑依赖和强统计依赖，使大规模多变量类型学分析能够在更清楚的“特征独立性”前提下进行。最近的贝叶斯时空谱系研究也表明：一些被提出的语法共性在显式控制谱系与地理后依然成立，但另一些会显著减弱（Verkerk et al., 2026）。

与此同时，许多与本研究相邻的问题已经有人做过，因此不能作为本文的新颖性来源。Port 等（2018）以及 Port、Karidi 与 Marcolli（2022）已经把持续拓扑、维度分析和层级聚类用于句法参数数据；计算类型学中，留出式预测语言类型学特征也早已成为成熟任务（如 Bjerva et al., 2019）。圆形排序本身也有成熟的方法学传统，包括基于谱与嵌入的圆形排列恢复方法（Evangelopoulos et al., 2020），以及关于严格 circular Robinson 结构的形式化算法研究（Armstrong, Guzmán, & Sing-Long, 2021）。

更直接相关的是 Kemp（2026）：他在若干明确的语义类别系统中检验了二分圆结构（bisected circular structures），例如季节、月相和方位。这项工作非常重要，因为它表明：在具有天然周期或方向关系的局部语义域中，圆形结构完全可能是一个有意义、可检验的语言学假说。但它并没有检验：由语法、词汇、音系等异质结构特征共同构成的全局类型学特征空间，是否应该形成一个单一圆环。

因此，本文的科学缺口并不是“语言能不能被聚类、降维、预测或画成圆”，而是一个更窄也更严格的问题：

> **把“语言周期表”具体化为一个可失败的全局周期模型后，它能否在留出预测中胜过非周期替代模型？**

### 1.1 对“周期性”的受限操作化

“周期表”这个隐喻并不必然意味着圆形。本文使用单一全局圆环，是把“反复出现且首尾闭合的结构”转化为一个强、最小、可证伪的操作化定义，而不是声称 Baker 本人提出了圆形几何，也不是声称所有“周期性”都能归约为一个圆。

真正的圆形系统应当具有比“稳定排序”更强的性质：相邻关系必须在整个周期上重复出现，包括最后一个点与第一个点之间的 wrap-around 边；同时，训练数据学到的排序在留出数据中应当仍表现出与圆形排序相容的距离结构。

这一点很关键，因为一个稳定排序完全可能是线性的、梯度式的或层级式的，而不是真正的周期。形式上，某些线性 Robinson 结构也可以被嵌入一个较弱的圆形解释中，因此仅仅“与某个圆形顺序相容”并不能证明首尾闭合。基于这一原因，我们把预测模型比较与直接的行级 circular-Robinson 风格诊断、以及显式的 wrap-around 闭合检验结合起来。

### 1.2 研究问题与结论边界

本文的核心问题是：

> **相对于非周期替代模型，一个简单的全局圆形几何能否对跨语言结构特征关系提供可复现的样本外组织？**

本研究明确属于探索性、筛查式研究。Stage 0 到 Stage 1I 是在研究推进过程中逐步发展出来的，而不是一个事先注册、一次性冻结的确认性协议。因此，本文重点报告效应量、留出复制、相互矛盾的结果以及结论边界，而不把整个 Stage 1–1I 序列包装成一个统一的确认性假设检验族。

在这一设计下，允许的最强结论也应当保持狭窄：

> **本文所检验的“语言周期表”的全局圆环版本，没有得到预测证据和留出圆环诊断的支持；在 TLI、GBI 和 WALS 的家族留出中，层级/非圆形模型提供了更强的预测基线，但这并不建立一个普遍的树形语言几何。**

## 2. 材料与方法

### 2.1 数据来源

#### TLI

主要分析使用 Graff 等（2025）整理的统计清理版 TLI，具体为 densified-small 全量数据。TLI 汇集 WALS、AUTOTYP、PHOIBLE 与 Lexibank 的结构信息，并通过清理降低特征之间的逻辑依赖和强统计依赖。

Stage 0 使用 644 种语言和最多 120 个特征。压缩性筛查中，缺失值按特征众数填补，类别状态做 one-hot 编码，随后用 TruncatedSVD 汇总累计解释方差；零模型在保持各特征边际分布的同时，独立打乱每个填补后的特征。另一个 Stage 0 配对 NMI 筛查，则仅使用每一对特征共同有观测的语言，并在特征对内部置换其中一个变量，构造接近“独立性”的零分布。

全局预测比较原则上使用覆盖率最高的 60 个合格特征；部分稳健性分析在 40 个特征下重复。

Stage 1 中，一个特征必须至少有 180 个语言观测，且状态数介于 2–15。合格特征先按覆盖率排序，再优先较低基数，以降低稀疏、高基数变量导致的不稳定 NMI。主分析使用排名最高的 60 个特征。

#### GBI

Stage 1H 使用 Graff 等（2025）的统计清理版 GBI。GBI 来源于 Grambank，但采用另一种特征清理策略。特征筛选标准同样为至少 180 个语言观测、2–15 个状态，随后按覆盖率与较低基数排序，保留 60 个特征。

该分析包含 1,140 种语言和 12 次有效家族留出划分。虽然 GBI 与 TLI 的底层特征来源不同，但两者共享同一套依赖清理框架，也覆盖大量重叠语言样本，因此本文保守地将 GBI 视为清理/表示稳健性检查，而不是完全独立复制。

#### WALS

Stage 1I 单独处理 CLDF WALS 作为一个稀疏表示的 sanity check。原始 pivot 包含 2,659 种语言；从中选择覆盖率最高、满足覆盖和基数规则的 30 个类别型参数。

WALS 比 TLI/GBI 稀疏得多，并且没有采用同样的依赖清理流程，因此其效应量不能与 TLI/GBI 直接数值比较。更重要的是，WALS 本身也是 TLI 的数据来源之一，因此它不是相对于 TLI 完全独立的数据源。Stage 1I 的用途只是：把 WALS 独立重构为另一种稀疏表示后，检查 family-held-out 中 tree vs circle 的排序是否会反转。

#### 家族与地理元数据

对 TLI 与 GBI，我们把 glottocode 映射到 Glottolog CLDF 的 Family_ID。没有映射到家族的条目被当作彼此独立的 isolate 组，而不是全部塞入同一个“缺失家族”类别。其 macroarea 与经纬度同样来自 Glottolog。

WALS 分析则使用 WALS CLDF 语言表中自带的 Family 与 Macroarea 字段；家族缺失值同样按独立 isolate 处理。基于经纬度的空间聚类完全不使用语言学结果来确定区块。

### 2.2 成对结构目标

对每一次 train/test 划分，我们分别在训练语言与测试语言中独立计算特征—特征关联矩阵。对有足够共同观测的特征对，以标准化互信息 NMI（arithmetic normalization）衡量关联。

主 TLI 分析中，在适用条件下，一个特征对至少需要 60 个共同训练/测试观测。

因此，模型并不是在预测“某一种语言的某一个特征值”，而是在学习特征之间关联关系的几何：模型只从训练语言中学习结构，然后去预测测试语言中重新估计出来的特征关联矩阵。

这种设计使样本外预测真正检验的是：某一种“结构组织方式”能否跨语言样本迁移，而不只是对全体语言的 pooled association matrix 进行拟合。

### 2.3 模型家族

所有候选几何只使用训练语言的关联矩阵进行拟合。

#### 零模型

所有非对角特征对都预测为训练数据非对角关联的平均值。

#### Rank-2 低秩模型

先对训练 affinity matrix 减去非对角均值，再利用绝对特征值最大的两个特征分量进行 rank-2 重构，作为一个简单的非周期低维替代模型。

#### 二维欧氏模型

从训练 affinity matrix 获得二维谱嵌入，计算特征之间的欧氏距离，再用训练特征对上的二次校准映射回预测关联强度。

#### 层级树基线

定义训练不相似度为 1 − NMI。使用 average-linkage 进行层级聚类，得到 dendrogram；特征对之间的 cophenetic distance 再通过训练集上的二次校准转换为预测关联。

这里的“树”只是一个预测基线，并不意味着我们声称语言结构字面上就是一棵谱系树。

#### 图模型

以训练不相似度构造 6-nearest-neighbor 加权无向图，用最短路径距离表示图上的结构距离，再通过训练数据上的二次校准转换为关联预测。

#### 圆环模型

最初的圆环模型先从二维谱嵌入得到角坐标，再使用前两个 cosine harmonics 建模周期关联。

Stage 1B 使用更强的直接优化版本：每个特征对应一个角坐标，固定一个特征角度为 0 以消除旋转不识别，其余 n−1 个角坐标直接优化。预测形式为：

s_hat(i,j) = beta_0 + beta_1 cos(Delta_ij) + beta_2 cos(2 Delta_ij)

其中 Delta_ij 为圆周角距离。每一步都重新拟合回归系数，并使用 L-BFGS-B 最小化训练 association matrix 上的均方误差，同时采用多个起点。

这一版本的目的，是避免把“圆环失败”简单归因于初始谱嵌入角度不好。

### 2.4 训练—测试评估

主要排名指标为：模型预测的特征关联与留出语言中独立估计关联之间的 Spearman 相关。Pearson、RMSE 与 MAE 也同时记录。

Stage 1 使用两类基础划分：

1. 随机语言留出；
2. 顶层家族留出：把完整抽中的 Glottolog 家族整体分配到测试集。

家族留出能减少直接谱系泄漏，但它不能消除所有谱系依赖或接触依赖。因此本文不把 family hold-out 当成 Galton's problem 的完整解决方案。

### 2.5 逐级稳健性分析

Stage 0–1I 是逐步发展出来的 robustness ladder：

- **Stage 0：** 检验 TLI 是否具有超越简单独立零模型的压缩性与特征间结构；
- **Stage 1：** 比较 null、low-rank、Euclidean、tree、graph 和初始 circular 模型；
- **Stage 1B：** 改善圆环模型公平性，加入 connected embedding 与直接角度优化，并在 40/60 特征下重复；
- **Stage 1C：** 只检验预先定义的 TLI 结构域，而不是事后挑选“看起来像圆”的域；
- **Stage 1D：** 检验留出数据上的 circular-Robinson 风格行单峰性与显式首尾闭合；
- **Stage 1E：** 使用 macroarea 和经纬度空间区块做地理留出，并加入 geography+family 版本；
- **Stage 1F：** 做 20 次有效家族留出，并 bootstrap 划分层面的配对性能差异；
- **Stage 1G：** 将真实地理区块与相同测试样本量的随机区块比较；
- **Stage 1H：** 用 GBI 检查清理/表示稳健性；
- **Stage 1I：** 用单独处理的稀疏 WALS 表示做 sanity check。

因为这个序列是适应性发展的，本文不声称 Stage 1–1I 构成一个统一的预注册确认性检验族。

### 2.6 预定义局部域标准

Stage 1C 使用 TLI 已发布的 grouping 元数据，构造五个 superdomain：Grammar linear order、Grammar other、Grammatical categories、Lexical 和 Phonology。

一个结构域只有同时满足以下三条，才被定义为“局部周期候选”：

1. optimized circular Spearman ≥ 0.15；
2. 与最佳非周期模型差距不超过 0.03；
3. circular-order stability ≥ 0.40。

这个联合标准的目的，是避免只因为圆环拟合“非零”就把一个子系统称为周期结构。

### 2.7 直接圆环诊断

Stage 1D 构造了一个受 circular Robinson 结构启发的 noisy-data sensitivity。对于训练语言中学出的排序，在留出 dissimilarity matrix 中，从每个焦点特征开始沿圆周读取对应一行，寻找“先升后降”的单峰序列，并计算违反这种单调结构的程度。数值越低，越接近该类型的圆形相容性。

该指标不是 Armstrong 等（2021）严格 circular-Robinson 识别算法的完整实现，而是一个面向噪声数据的敏感性诊断。

由于线性 Robinson 结构也可能被套进某种环形顺序中，仅仅“与圆相容”不足以证明真正周期闭合，因此另外定义 closure ratio：

closure ratio = 首尾 wrap-around 特征对的相似度 / 内部相邻特征对相似度的中位数。

如果真正存在稳定闭环，这一比值应接近 1；如果最后一个特征与第一个特征几乎不像，而内部相邻关系较强，那么“画成圆”更可能只是把开放顺序强行闭合。

### 2.8 地理迁移与同样本量校准

Stage 1E 根据 Glottolog macroarea 和经纬度聚类构造 outcome-blind 地理区块。Stage 1G 则对每一个地理测试区块，构造相同测试语言数量的随机对照，并比较训练 association matrix 与测试 association matrix 的相关。

该设计可以排除一个简单替代解释——“地理块表现差只是因为测试语言太少”——但不能识别因果性的区域传播，也不能把地理效应与历史相关的人群结构完全分离。

### 2.9 重复划分不确定性

Stage 1F 使用 20 个有效顶层家族留出划分。对同一个 split 计算 tree-minus-circle 等配对 Spearman 差异，再对 20 个 split-level difference 做 bootstrap 得到 95% 区间。

因此，这些区间衡量的是：结论对抽到哪些家族划分有多敏感。它们不是把语言当作独立观测后的抽样不确定性，也不包含谱系树不确定性、语言接触网络不确定性或整个模型选择流程的不确定性。

## 3. 结果

### 3.1 数据中存在真实结构，但 Stage 0 不等于周期性

TLI 的 Stage 0 压缩筛查中，mode-imputed、one-hot 后的矩阵使用 20 个 TruncatedSVD 分量可解释 0.510 的累计方差；在逐列打乱零模型中，这一数值为 0.362，超额为 +0.148。

成对关联方面，大部分特征对的 NMI 很小，但上尾明显更强：真实数据 NMI 的 99th percentile 为 0.119，而配对内部置换零模型为 0.039。

这些结果说明数据里确实存在值得建模的结构，但它们本身不提供任何周期性证据。

### 3.2 初始留出模型比较偏向非周期替代模型

在 60 个 TLI 特征上，Stage 1 家族留出中的平均 Spearman 为：

| 模型 | family-held-out Spearman |
|---|---:|
| tree | **0.178** |
| graph | 0.163 |
| low-rank (rank 2) | 0.150 |
| circular | 0.109 |

圆环排序本身并非完全随机：相对于全数据参考顺序，其平均稳定性为 0.542。但“排序可复现”并没有转化为最佳样本外预测。

随机语言划分的方向也类似：graph 0.205、tree 0.199、low-rank 0.172、circle 0.122。

### 3.3 直接优化圆环后，不能再用“圆环基线太弱”解释失败

Stage 1B 给圆环更大的拟合自由。

在 40 特征时：
- optimized circle = 0.179
- tree = 0.178
- connected Euclidean = 0.217

在 60 特征时：
- optimized circle = **0.105**
- tree = **0.147**
- low-rank = **0.153**

直接优化的 60 特征圆环顺序仍具有较高稳定性（0.628 ± 0.081），因此结果不能归因于“圆环顺序完全不稳定”。更准确的描述是：

> **圆环顺序可以稳定，但稳定本身并不足以产生最强的留出预测。**

### 3.4 没有任何预定义 TLI 结构域通过局部周期门槛

| 结构域 | 特征数 | tree | low-rank | optimized circle | circle stability | 结论 |
|---|---:|---:|---:|---:|---:|---|
| Grammar linear order | 14 | **0.494** | 0.493 | 0.401 | **0.811** | non-periodic |
| Grammar other | 38 | **0.313** | 0.243 | 0.253 | 0.274 | non-periodic |
| Grammatical categories | 23 | 0.229 | 0.125 | **0.252** | 0.373 | ambiguous，低于稳定性门槛 |
| Lexical | 18 | **0.269** | 0.220 | 0.142 | 0.057 | non-periodic |
| Phonology | 40 | **0.229** | 0.215 | 0.151 | 0.550 | non-periodic |

最有解释力的是 Grammar linear order。它的圆环稳定性高达 0.811，圆环预测也达到 0.401，说明一个可复现的结构顺序确实存在；然而 tree 与 low-rank 都接近 0.49。

这给出一个非常具体的反例：

> **稳定排序 ≠ 真正周期闭环。**

Grammatical categories 是唯一一个 optimized circle 均值（0.252）略高于 tree（0.229）的域，但其稳定性只有 0.373，低于预先规定的 0.40，因此不能晋升为局部周期候选。

### 3.5 留出 circular-Robinson 风格诊断不支持全局闭合

40 特征：
- circular order = 0.222 ± 0.012
- tree leaf order = **0.209 ± 0.011**
- random order = 0.237 ± 0.009

60 特征：
- circular order = 0.297 ± 0.009
- tree leaf order = **0.284 ± 0.010**
- random order = 0.307 ± 0.009

更直接的 closure ratio：
- 40 特征：0.608，但 SD = **0.764**，高度不稳定，因此不作为有效闭环证据；
- 60 特征：**0.037 ± 0.091**。

60 特征时，圆环“最后一个点连回第一个点”的相似关系几乎不存在。这与“存在稳定开放顺序，但并不真正闭环”的解释更一致。

### 3.6 TLI 重复家族留出中 tree-over-circle 非常稳定

| 模型 | Spearman mean ± SD | 相对 optimized circle 的配对差异 | split-bootstrap 95% CI | 胜 circle 比例 |
|---|---:|---:|---:|---:|
| tree | **0.182 ± 0.047** | **+0.073** | **[0.055, 0.092]** | **20/20** |
| low-rank (rank 2) | 0.155 ± 0.034 | +0.046 | [0.033, 0.061] | 0.95 |
| Euclidean connected | 0.110 ± 0.053 | +0.001 | [−0.020, 0.021] | 0.65 |
| circular optimized | **0.109 ± 0.030** | reference | — | — |

tree 在 20/20 个 split 都超过 optimized circle。

但 bootstrap CI 只是划分敏感性区间，不等于谱系不确定性区间。

### 3.7 TLI 跨地理区域迁移显著下降，但不能推广为普遍规律

当完整 TLI macroarea 被留出时，所有模型的预测力都明显下降。在更严格的 geography+family 条件下，最佳非周期 Spearman 约为 0.056，而 optimized circle 约为 0.000；空间 cluster+family 中，最佳非周期约 0.085、circle 约 0.039。

matched-size 校准显示：

| 测试方式 | train-test association correlation |
|---|---:|
| TLI macroarea block | 0.088 |
| 相同样本量随机 block | 0.363 |
| TLI coordinate cluster | 0.106 |
| 相同样本量随机 coordinate block | 0.351 |

10/10 个真实地理块都低于相同样本量随机对照。

然而 WALS 后续结果与此不同，因此不能把“跨区域几何必然崩溃”提升为普遍结论。

### 3.8 GBI 清理表示中 tree-over-circle 再现

GBI 使用 1,140 种语言、60 个特征、12 个有效 family-held-out split。

平均 Spearman：
- tree = **0.122 ± 0.038**
- low-rank = 0.098 ± 0.034
- optimized circle = **0.073 ± 0.036**

tree-minus-circle = +0.049，并且 12/12 个 split 都是 tree 更高。

GBI 的跨 macroarea association transfer 平均为 0.144 ± 0.043，定性上和 TLI 的弱地理迁移相似。

由于 GBI/TLI 并非完全独立数据生成过程，这说明的是对另一种清理/表示方式具有稳健性，而不是完全独立复制。

### 3.9 单独处理 WALS 后，模型排序依旧，但地理结果反转

WALS 分析使用 2,659 种语言、30 个参数、8 个有效 family-held-out split。

平均 Spearman：
- tree = **0.603 ± 0.026**
- low-rank = 0.468 ± 0.034
- optimized circle = **0.410 ± 0.050**

tree-minus-circle = +0.193，8/8 次 tree 都更高。

但 WALS 的跨 macroarea association transfer 很高：

> **0.634 ± 0.075**

因此，最稳健的跨表示结论不是“地理异质性”，而是：

> **在所检验的 family-held-out 设计中，optimized circle 没有反转 tree/non-circular 基线的优势。**

### 3.10 跨表示总结

| 表示 | 语言数 | 特征数 | tree Spearman | circular Spearman | tree > circle |
|---|---:|---:|---:|---:|---:|
| TLI repeated family hold-out | 644 | 60 | **0.182** | 0.109 | 20/20 |
| GBI curation robustness | 1,140 | 60 | **0.122** | 0.073 | 12/12 |
| separately processed WALS | 2,659 | 30 | **0.603** | 0.410 | 8/8 |

不同数据表示的覆盖率、缺失率、特征定义、筛选策略和清理方法不同，绝对 Spearman 大小不能直接跨行比较。可比较的是定性排序：在三个表示中，optimized circle 都没有超过 tree 基线。

## 4. 讨论

### 4.1 本研究真正限制了什么

“语言周期表”仍然是一个有意义的科学问题，但我们所检验的单一全局圆环版本没有成为最强预测几何。

这个结论并不只依赖“tree 的分数更高”，因为 tree 和 graph 可能具有比单圆更大的有效模型容量。更有说服力的是多项证据共同出现：

1. 圆环使用 n−1 个自由角坐标直接优化，而不是被迫继承一个弱谱排序；
2. 在重复 TLI 家族留出中，low-rank 平均也优于 circle；
3. 没有一个预定义 TLI 域通过局部周期联合门槛；
4. circular-Robinson 风格的直接留出诊断没有优于 tree leaf order；
5. 60 特征时 wrap-around closure 极弱；
6. family-held-out 的 tree-over-circle 排序在 GBI 清理表示和单独处理 WALS 中再次出现。

综合起来，一个简单全局周期环并不是当前观察到关联几何的强摘要。

### 4.2 本研究不能证明什么

第一，本研究不能证明“语言普遍是树形的”。tree 只是预测基线。它的更高分数既不能确定唯一的本体几何，也不能消除模型容量差异。

第二，本研究不能否定所有语言周期性。Baker 原始论述本身就主要是参数层级；“周期表”还可能被重新形式化为多个环、空间乘积、格点、条件参数系统或其他生成约束。这些都是新的假说，未来可以预注册并独立检验，但不应该在当前结果出来以后事后增加，只为了“救回”原假说。

第三，本研究也不声称数据库里的类型学特征就是类似化学元素的“自然种类”。这里研究的是被编码出来的类型学变量空间；它必然受到语言理论、数据库定义、状态编码和清理策略影响。

### 4.3 稳定顺序并不等于周期闭合

本文最重要的概念结果之一，是把“稳定排序”和“真正周期”分开。

Grammar linear order 的 circle stability 高达 0.811，circular prediction 也达到 0.401，但 tree/low-rank 仍约为 0.49。60 特征全局 circle 也有相当稳定的排序，却几乎没有 wrap-around closure。

因此，一个系统即使能被稳定排成某种顺序、画在圆上看起来整齐、甚至圆形 embedding 能解释一部分结构，也仍然可能本质上更接近梯度、层级或开放 manifold，而不是周期闭环。

这也是为什么 Kemp（2026）这样的局部语义域圆形结构与本研究并不矛盾：季节、月相、方向等本来就具有天然周期/方向语义，它们完全可能形成真正圆形结构；本文检验的是一个跨语法、词汇、音系等异质特征的全球单圆。

### 4.4 地理异质性只是表示依赖的次级结果

TLI 与 GBI 都显示跨大地理区块的关联结构迁移较弱，且 TLI 的 matched-size 对照说明这不是纯粹的小样本假象。

但 WALS 却显示强得多的 macroarea transfer。

这种不一致可能来自特征定义、缺失模式、域构成、清理策略、语言抽样或稀疏类别数据下 association matrix 的行为。当前研究无法确定哪一个解释正确。因此，这种矛盾应当被用来限制结论，而不是被强行解释成“地理决定语言几何”。

### 4.5 与已有研究的关系

Baker（2001）提供了“周期表”动机，但没有提供本文的预测性圆环模型。

Port 等（2018；2022）已经证明句法参数数据中存在非平凡拓扑、聚类和环结构，因此本文不能声称“第一次发现语言空间有拓扑/低维结构”。

Grambank（Skirgård et al., 2023）已经确立了大规模全球形态句法多样性及强谱系约束；Graff 等（2025）的 GBI/TLI 则提供了更适合做多特征结构比较的依赖清理表示。

计算类型学中，held-out prediction 也早已被用于探测结构信息（Bjerva et al., 2019）。

因此，本文的贡献是方法学和诊断性的：

> **把一个强版本的全球“语言周期表”隐喻转成明确的样本外竞争模型，然后让它在预测、局部域、直接圆环诊断、家族留出、地理阻断与跨表示检查中真正具备失败的可能。**

## 5. 局限

### 5.1 探索性多重性

Stage 1–1I 是逐步发展的，包含多个特征数、结构域、划分方式、指标与数据表示，因此不能把每一步 nominal comparison 当作一个预注册确认性检验族。

Stage 1F 的重复 split 和 paired bootstrap 是对一个已经经过前期探索的重点对比所做的稳健性总结，而不是事前冻结的 confirmatory test。

### 5.2 剩余谱系与接触依赖

顶层家族留出降低直接泄漏，但不能建模家族内外的连续谱系协方差、语言树本身的不确定性、接触网络或更复杂的扩散关系。

完整贝叶斯 spatiophylogenetic 模型会加强“独立于继承/接触”的普适性论证，但对于本文受限的描述性结论——“tested circle 不是最强留出基线”——不是当前发表所必需的硬门槛。

### 5.3 模型容量不匹配

tree、graph 与单一圆环具有不同有效容量，因此不能把 tree 胜出直接解释为“真实几何就是树”。

低秩比较与直接 circle diagnostics 可以部分缓解这个问题，但不能彻底消除模型复杂度差异。

### 5.4 关联指标与稀疏数据

NMI 会受到样本量、缺失和类别结构影响。虽然特征对设置了最低支持度，但 association matrix 自身的不确定性并没有完整传播到每一个模型拟合中。

WALS 尤其稀疏，因此 WALS 更大的相关数值不能与 TLI/GBI 当作同一采样过程下的同量纲效应量直接比较。

### 5.5 特征本体

本文研究的是编码后的类型学变量几何，而不是必然具有心理学或历史原初性的“语言原子”。

数据库如何定义特征、如何编码状态、如何做依赖清理，会改变被建模的空间。

### 5.6 Circular-Robinson 敏感性是近似诊断

Stage 1D 的 row-unimodality violation 受 circular-Robinson characterization 启发，但不是 Armstrong 等（2021）严格识别算法的精确实现。

closure diagnostic 的加入，正是因为 circular compatibility 本身可能包含 line-like structure。未来如果要进一步研究更复杂的周期结构，应开发或采用真正面向噪声数据的 exact/noisy circular-seriation model comparison。

## 6. 结论

“周期表”类比只有在它可能失败时，才真正具有科学信息。

在一系列逐步严格的筛查中，直接优化的全局圆环确实捕捉到可复现的语言结构，但它并没有成为对该结构最强的留出解释。TLI、GBI 与单独处理的 WALS 中，tree/non-circular 基线在 family hold-out 下都更强；预定义结构域没有产生稳健的局部周期候选；直接留出圆环诊断也没有提供令人信服的全局 wrap-around closure。

因此，本文的结论不是“语言不存在任何周期组织”，也不是“语言本质上是一棵树”。

更窄、也更有用的结论是：

> **稳定的跨语言结构本身并不意味着周期性；在我们所检验的模型与数据条件下，“语言周期表”的简单全局圆环版本，没有得到作为最佳预测几何的支持。**

下一步更有价值的问题，已经不再是“怎样把结果强行画成周期表”，而是：

- 哪些明确指定的非圆形、模块化或高维几何能跨语言域与语言群体稳定泛化？
- 哪些局部语言系统真的具有 domain-grounded circularity？
- 如果未来要重新提出更强的“周期性”版本，什么新证据才足以支持它？

## 7. 数据与代码可用性

完整分析代码、机器可读结果和 Stage 0–1I 报告保存在 ARIS4C Paper 002 的研究记录中。英文匿名投稿包另提供去身份化的脚本、JSON 输出、图生成代码与重现环境。

历史分析脚本最初从公开上游仓库的可变分支下载数据。为提高后续可复现性，稿件阶段已经记录 TLI/GBI、WALS 与 Glottolog 在冻结时间点的上游 commit SHA。需要强调的是：这些 freeze commit 为未来复现提供目标，但不能追溯性证明每一次历史 run 都使用了完全相同的字节版本。

## 参考文献

Armstrong, S., Guzmán, C., & Sing-Long, C. A. (2021). An optimal algorithm for strict circular seriation. *SIAM Journal on Mathematics of Data Science, 3*(4), 1223–1250. https://doi.org/10.1137/21M139356X

Baker, M. C. (2001). *The Atoms of Language: The Mind's Hidden Rules of Grammar*. Basic Books.

Bjerva, J., Kementchedjhieva, Y., Cotterell, R., & Augenstein, I. (2019). A probabilistic generative model of linguistic typology. In *Proceedings of NAACL-HLT 2019* (pp. 1529–1540). https://doi.org/10.18653/v1/N19-1156

Dryer, M. S., & Haspelmath, M. (Eds.). (2013). *The World Atlas of Language Structures Online*. Max Planck Institute for Evolutionary Anthropology.

Evangelopoulos, X., Brockmeier, A. J., Mu, T., & Goulermas, J. Y. (2020). Circular object arrangement using spherical embeddings. *Pattern Recognition, 103*, 107192. https://doi.org/10.1016/j.patcog.2019.107192

Graff, A., Chousou-Polydouri, N., Inman, D., et al. (2025). Curating global datasets of structural linguistic features for independence. *Scientific Data, 12*, 106. https://doi.org/10.1038/s41597-024-04319-4

Kemp, C. (2026). Symmetry in category systems across languages. *Nature Communications, 17*, 358. https://doi.org/10.1038/s41467-025-67463-4

Port, A., Gheorghita, I., Guth, D., Clark, J. M., Liang, C., Dasu, S., & Marcolli, M. (2018). Persistent topology of syntax. *Mathematics in Computer Science, 12*(1), 33–50. https://doi.org/10.1007/s11786-017-0329-x

Port, A., Karidi, T., & Marcolli, M. (2022). Topological analysis of syntactic structures. *Mathematics in Computer Science, 16*, Article 2. https://doi.org/10.1007/s11786-021-00520-5

Skirgård, H., Haynie, H. J., Blasi, D. E., et al. (2023). Grambank reveals the importance of genealogical constraints on linguistic diversity and highlights the impact of language loss. *Science Advances, 9*(16), eadg6175. https://doi.org/10.1126/sciadv.adg6175

Verkerk, A., Shcherbakova, O., Haynie, H. J., et al. (2026). Enduring constraints on grammar revealed by Bayesian spatiophylogenetic analyses. *Nature Human Behaviour, 10*, 126–136. https://doi.org/10.1038/s41562-025-02325-z
