# 全球脏话的“语法”：
## 跨语言禁忌表达中的测量等价、词汇稳定性与社区差异

**中文工作稿 · ARIS4C016 · 2026-09-19**

### 摘要

禁忌语言几乎遍布所有人类社会，但跨语言比较首先面临一个基础性的
测量问题：不同研究地点所理解、收集和标注的“脏话”未必是同一种
测量对象。本文以 Sulpizio 等（2024）公开的多实验室数据库为起点。
该数据包含 18 个社区样本、17 个国家和 13 种语言。我们不直接把各地
词表做成“世界脏话排行榜”，而是先检验跨社区测量是否可比。

对 Study 1 的 8,190 行词汇数据进行结构审计后，我们发现各站点在
平均产出量、主类别缺失率和多标签使用率上存在巨大差异；原始
`category` 字段还混合了不同逻辑层级，例如 sexual/scatological
主要是语义来源，insult 更接近语用功能，而 slur 更接近社会指向/
身份贬损类型。因而，未经修正的类别比例既可能反映真实语言差异，
也可能只是实验室标注习惯。

为此，我们提出保留原始来源的正交多轴 ontology，将语义来源、攻击
对象、语用功能、社会身份指向、禁忌/贬损机制和语言形式分开编码。
进一步将 18 个社区样本链接到 Glottolog 后发现，它们实际上只代表
13 种语言和 5 个顶层语系，其中 8/13 为印欧语，因此当前数据不足以
支持强意义上的“全球普遍规律”。

最强的现有比较来自英语重复样本。Study 2 中共有 139 个词至少同时
出现在两个英语社区；使用词项固定效应后，community 对 tabooness
剩余方差的 partial R² 为 .0265，对 offensiveness 为 .0361。说明词本身
仍是主要稳定来源，但社区调节并非为零。与此同时，中性 filler 的
稀疏负对照显示 community effect 反而更大，提示当前社区效应不能被
直接解释为“脏话文化效应”，其中可能包含评分尺度、样本构成、程序
和一般语义判断差异。

因此，本文提出“**稳定核心 + 情境调节**”框架，并把可靠性、缺失、
词项身份和语言谱系视为建立全球禁忌语言图谱之前必须通过的测量
关卡。我们已经冻结一份 300 行的独立双编码审计样本；真正的
measurement-corrected Taboo Fingerprint 将在独立 Coder A/B 与母语
复核通过后生成。

**关键词：** 禁忌语言；脏话；辱骂；跨语言比较；测量等价；社会语言学；
语言类型学；文化演化

---

## 1. 引言

脏话并不是语言系统之外的“噪音”。人们会用禁忌表达传递愤怒、疼痛、
亲密、团结、攻击、身份和立场。同一个词在不同语境里可以是直接
侮辱、程度强化、感叹，也可以成为朋友之间的玩笑。因此，“脏话”
并不是单纯的词汇表问题，而同时涉及语义学、语用学、社会语言学、
心理语言学与语言人类学。

跨语言比较的诱惑很大：如果我们收集足够多国家和语言的禁忌表达，
似乎就可以观察不同社会“最忌讳什么”。但这种推理很容易过早。
观测差异至少可能来自四个来源：

1. 真实的社区/社会差异；
2. 语言结构差异；
3. 语言亲缘与历史传播；
4. 收集和标注程序本身。

尤其当某种语言在多个国家被重复采样，而另一种语言只出现一次，
同时各实验室又使用不同程度的类别标签时，“国家差异”“语言差异”
和“标注差异”会混在一起。

Sulpizio 等（2024）的开放多实验室项目为解决这个问题提供了非常
好的基础。其优点不仅是覆盖多语言，更重要的是公开了原始数据和
分析脚本。因此，ARIS4C016 首先提出一个比“哪里的人怎么骂人”
更基础的问题：

> 当不同社区的禁忌词表看起来不一样时，有多少差异来自现象本身，
> 又有多少差异来自测量系统？

本文采取 measurement-first 路线。我们先审计原始标注的等价性，再
分离 lexical item、community、language 与 language family，最后利用
相同英语词项跨社区重复出现这一设计，在固定词项身份后估计社区相关
变化。

我们的核心假设不是“脏话完全普遍”或“脏话完全文化相对”，而是
**稳定核心 + 情境调节（stable core + contextual modulation）**：
词汇本身和反复出现的禁忌来源提供稳定结构，社区、语境、历史与
社会规范则在这一结构上产生调节。

![图1：从多实验室原始数据到可靠性门控全球图谱的 measurement-first 路线。](../figures/Figure1_measurement_pipeline.svg)

**图1。** Measurement-first 研究流程。标注体系、ontology 可靠性、
词项身份与语言谱系必须先成为明确的推断关卡，之后才进入跨社区图谱。

---

## 2. 既有研究与创新边界

跨文化脏话研究并不是新领域。Ljung（2011）已经提出系统的语言学
分类并比较英语与二十余种语言。Jay（2009）从神经—心理—社会框架
讨论禁忌词的普遍性与功能。Allan（2019）主编的 *Oxford Handbook of
Taboo Words and Language* 更明确强调，禁忌不是字符串固有属性，而是
随社区、语境和时间变化的语言行为。

Lev-Ari 与 McKay（2023）还提出了一个跨语言音系候选规律：脏话中
approximants（近音）可能相对少见，并通过伪词判断实验获得支持。
Sulpizio 等（2024）则提供了与本研究最直接相关的开放多实验室词汇/
评分数据库。

因此，本研究**不**把以下内容当作原创发现：

- 世界各地都有脏话；
- 可以给脏话做一般性分类；
- 禁忌具有语境依赖性；
- approximant 假说；
- 英语/西班牙语相同词项可以做跨社区相关。

候选创新点是方法学整合：在同一框架中明确区分

- 原始标注行为；
- 正交 ontology；
- lexical item identity；
- community；
- language；
- genealogy；
- 以及后续文化解释变量。

---

## 3. 数据与 Phase 0 设计

### 3.1 数据来源

Phase 0 使用 Sulpizio 等（2024）的公开 OSF 数据。

Study 1：
- 1,046 名参与者；
- 18 个 community sample；
- 8,190 行清洗后的词汇记录。

Study 2：
- 4,240 行词项级汇总评分；
- 包含 tabooness、offensiveness、valence、arousal、
  concreteness、age of acquisition 与 corpus frequency 等变量。

为保证可复现性，ARIS4C016 不直接修改第三方原始数据，而记录 OSF
GUID、下载入口和 SHA-256，并在脚本中下载后校验哈希。

### 3.2 为什么是 18 个社区而不是 18 种语言

Glottolog 映射后，18 个社区只对应 13 种语言：

- English：5 个社区（AU、CA、GB、SG、US）；
- Spanish：2 个社区（CL、ES）；
- 中国包含 Cantonese/Yue 与 Mandarin 两个语言样本；
- 总计仅 5 个顶层语系；
- 13 种语言中 8 种属于 Indo-European。

因此，把 18 个 sample 当作 18 个独立语言会重复计算 English，并严重
低估谱系依赖。

---

## 4. Study 1：测量审计

### 4.1 产出量不能直接解释为“更爱骂人”

不同站点平均每名参与者产生的表达数量差异极大。例如：

- Mandarin (CN)：约 9.3；
- Spanish (CL)：约 12.5；
- English (CA)：约 13.4；
- Dutch (BE)：约 29.6；
- German (DE)：约 52.9。

这些差异可能来自任务理解、词形生产力、清洗规则、参与程度以及
“禁忌/粗鲁/侮辱”边界差异。因此原始词数不能直接成为文化
“swearing propensity”指标。

### 4.2 标注缺失与多标签行为高度异质

主类别缺失率的极端例子：

- Setswana (BW)：约 67.6%；
- Spanish (ES)：约 80.4%。

多标签行比例也从 Spanish (ES) 的约 2.7% 到 English (CA) 的约 77.3%
不等。

这意味着所谓“某国 sexual 类更多”在未经修正时，完全可能只是
不同研究站点的 annotation policy 不同。

### 4.3 原始类别不在同一逻辑层级

原始标签同时出现：

- sexual / scatological / blasphemy；
- insult；
- slur；
- medical / political / family / animal 等；
- 各种本地标签与拼写变体。

其中：
- sexual 更像 semantic source；
- insult 更像 pragmatic function；
- slur 更像 social-indexical/targeted derogation；
- blasphemy 同时涉及 sacred domain 与 transgression mechanism。

因此，这些标签不应该被强迫放在一个互斥类别表中。

### 4.4 多轴 ontology

Ontology v0 分为：

1. semantic taboo source；
2. target；
3. pragmatic function；
4. social-indexical basis；
5. taboo/derogation mechanism；
6. linguistic form。

每个表达可在多个轴上同时取值，并附 HIGH / MEDIUM / LOW /
UNRESOLVED 置信等级。原始 category 永久保留，不会被“清洗后覆盖”。

---

## 5. 失败的朴素 Taboo Fingerprint

我们尝试只利用高置信度自动映射构造 semantic fingerprint，结果首先
得到的是一个**测量失败结果**。

不同社区能够恢复 semantic source 的行比例差异非常大：

- Cantonese (CN)：70.7%；
- English (US)：66.4%；
- Finnish (FI)：64.8%；
- German (DE)：27.9%；
- Thai (TH)：26.8%；
- Setswana (BW)：20.7%；
- Spanish (ES)：10.9%。

![图2：18 个社区中高置信度 semantic-source 标注覆盖率。](../figures/Figure2_semantic_coverage.svg)

**图2。** Ontology v0 下可恢复 semantic source 的行覆盖率。如此大的
站点差异意味着原始类别比例不能被直接解释成文化差异。

此外，当前可映射集合看起来由 sexual 类占主导，但这也不能直接成为
“全球脏话约六成与性有关”之类的结论。原因是 sexual 本来就是一个
显式 semantic label，而大量只标为 insult/slur 的行并没有告诉我们其
语义内容究竟来自性、亲属、智力、动物化、外貌、身份还是其他领域。
可恢复 semantic subset 因而并非随机样本。

真正的 Taboo Fingerprint 必须依赖正交轴重新编码，而不是对原始标签
改名。

---

## 6. Study 2：相同词项的跨社区变化

### 6.1 为什么 repeated-item 更强

大多数跨语言比较同时改变“词是什么”和“社区在哪里”，因此无法判断
差异来自词汇还是社区。

英语数据提供了更强的设计：同一个 lexical form 在多个英语社区中被
独立评分。

非 filler 的 Study 2 数据中，有 139 个英语词至少出现在两个社区；
其中 23 个在全部五个英语社区中都有评分。

### 6.2 描述性稳定性

相同英语词项的 tabooness 跨社区相关通常较高，但不是 1。例如：

- AU–US：r ≈ .89；
- CA–US：r ≈ .87；
- CA–SG：r ≈ .67。

因此词项具有强稳定性，同时保留社区差异。

### 6.3 Item-fixed-effects 模型

我们使用 Frisch–Waugh–Lovell 固定效应分解：

1. 先移除 lexical-item fixed effects；
2. 再在残差上估计 community indicator；
3. 以 item-only model 为基线计算 partial R²；
4. 对 lexical item 进行 bootstrap。

139 个共享词形成 417 个 item × community 观察：

| Outcome | Community partial R² | item-bootstrap 95% CI |
|---|---:|---:|
| Tabooness | .0265 | .0095–.0837 |
| Offensiveness | .0361 | .0125–.1045 |
| Valence | .0446 | .0173–.1150 |
| Arousal | .0827 | .0384–.1689 |
| Concreteness | .2112 | .1198–.3105 |
| Age of acquisition | .0874 | .0347–.1783 |

对于本项目最核心的两个结果，community 在固定词项之后仍解释约
2.7% 的 tabooness 剩余变异和 3.6% 的 offensiveness 剩余变异。
这支持“稳定核心 + 情境调节”，但 community effect 远小于词项结构。

### 6.4 五社区平衡子集

只保留五个英语社区都共有的 23 个 taboo item 后：

- tabooness partial R² = .0537；
- offensiveness partial R² = .0532。

结果方向保持，但 bootstrap 区间明显变宽，因此它是 robustness check，
不是更精确的主效应估计。

### 6.5 Filler 负对照

对 shared filler 使用完全相同的 item-FE 分析：

- 35 个共享 filler；
- 73 个 item × community 观察；
- 没有任何 filler 同时覆盖全部五个社区。

结果反而显示更大的 community partial R²：

- filler tabooness rating：.2965；
- filler offensiveness rating：.1583；
- valence：.2021；
- arousal：.2404；
- concreteness：.2129；
- AoA：.1933。

![图3：shared taboo 与 filler 的 community partial R²。](../figures/Figure3_community_control.svg)

**图3。** 固定 lexical item 后的 community-associated residual variation。
Filler 样本很稀疏且不平衡，因此不能据此断言 filler “更受文化影响”；
但它足以作为负对照，说明当前 community effect **尚不能被认定为
taboo-specific**。

这一步显著收紧了本文结论。当前数据能够支持：

> 相同词项的评分具有社区敏感性。

但暂时不能支持：

> 社区差异特异地反映了禁忌文化。

真正的确认性设计需要构造覆盖相同社区、频率/长度/词类相匹配的
taboo 与 neutral items，并直接检验 taboo-status × community interaction。

---

## 7. Ontology 可靠性关卡

真正进行 semantic prevalence 比较之前，我们冻结了一份约 300 行的
多语言审计样本。

最终冻结样本正好 300 行：

- 普通站点每个 15 行；
- Setswana (BW) 30 行；
- Spanish (ES) 30 行。

分层包含：

- primary category 缺失：42；
- unresolved label：116；
- multi-label：61；
- random/backfill：81。

公开 manifest 只包含 sample、源 row index、row hash 与抽样层，不公开
具体禁忌词。确定性 manifest SHA-256 为：

`48c58f91901e8c2a1aab01958e95ea28afaf0f33e7a98677f98e58b8a412c9b4`

Coder A 与 Coder B 必须独立完成，不允许根据彼此结果修改第一轮标签。
需要母语知识或文化语境的词项应优先选择 UNRESOLVED /
CONTEXT_REQUIRED，而不是猜测。

计划报告：

- exact-set agreement；
- Jaccard similarity；
- 各 label 的二元 agreement；
- 在 prevalence 足够时计算 Cohen's kappa；
- 必要时使用更抗 prevalence paradox 的系数；
- unresolved agreement。

只有可靠性通过的 axis 才进入 confirmatory fingerprint。

---

## 8. 音系验证路线

原始数据的 `transcription` 并不是全球统一的 IPA 层。几乎只有
Cantonese 和 Mandarin 有高覆盖，其他 16 个社区基本为空，因此不能
直接用这一字段做全球音系检验。

后续将构造独立 pronunciation layer：

- 语言特定 G2P / Epitran；
- PHOIBLE 用于 inventory / feature 标准化；
- 母语/来源语言抽样验证；
- 明确记录 slang、错拼、code-switching 与 multiword 的失败率。

首要 confirmatory phonology test 是复现 Lev-Ari 与 McKay 的
approximant hypothesis。其他音类只做探索，除非另行 preregister。

---

## 9. 讨论

### 9.1 稳定核心与情境调节并存

Repeated-item 结果不支持“完全普遍”与“完全文化相对”的二分法。
同一 taboo item 在不同英语社区具有明显稳定排序，但评分并不完全相同。

更合适的理论结构是：

[
Observed taboo judgement =
Lexical structure +
Community/context +
Measurement +
Noise
]

当前数据已经表明 lexical structure 很重要，也表明 community-associated
variation 存在；但 filler negative control 进一步提醒我们，community
项并不自动等于 taboo culture。

### 9.2 Annotation 本身属于 data-generating process

本项目最重要的方法学结果之一是：标注不是数据产生之后才附加的
“整理步骤”，而是数据生成机制的一部分。

如果一个站点主要使用 semantic label，另一个站点主要使用 pragmatic
label，第三个站点大量留空，那么直接比较 category proportions 得到的
可能是“研究流程地图”，而不是“文化禁忌地图”。

### 9.3 “全球”需要谱系多样性

13 种语言比单一英语研究丰富得多，但仍只有 5 个顶层语系且明显
偏向 Indo-European。强意义上的 universality 需要：

- 更多独立 language family；
- held-out family replication；
- 同一语言跨多个国家；
- 同一国家内多语言；
- 更接近 crossed language × community 的设计。

扩展样本的优化目标应是**可识别性和谱系多样性**，而不是简单追求
“100 languages”这样的标题数字。

### 9.4 Atlas 应是证据界面而不是装饰

未来 Global Swearing Atlas 应同时显示：

- 已观察到什么；
- annotation coverage；
- uncertainty；
- unresolved share；
- language/community provenance；
- 哪些结论当前不能识别。

它不应该用漂亮地图掩盖数据缺失，也不应该制造“哪个国家最脏”
之类缺乏测量基础的排名。

---

## 10. 当前限制

- 尚未完成真正独立的 Coder A/B ontology 结果；
- 需要多语言/母语复核；
- community sample 的人口结构和程序并不完全一致；
- Study 2 当前使用的是 item-level aggregate ratings；
- repeated-language identification 主要依赖 English；
- family diversity 有限；
- 原始 flat taxonomy 无法恢复大量 insult/slur 行的 semantic source；
- filler negative control 稀疏且不是专门匹配设计；
- phonology 仍需新建统一 pronunciation layer。

---

## 11. 下一阶段

1. 执行被冻结的 300 行独立双编码；
2. 计算 ontology axis / label-level reliability；
3. 冻结 A/B 原始结果后再 adjudicate；
4. 生成第一版 measurement-corrected semantic fingerprints；
5. 运行 ontology-domain × community repeated-item 模型；
6. 构建 purpose-built matched taboo/neutral control；
7. 完成 G2P/IPA approximant replication；
8. 冻结确认性假设；
9. 设计 crossed language × country 扩展样本。

---

## 参考文献（工作集）

Allan, K. (Ed.). (2019). *The Oxford Handbook of Taboo Words and Language*.
Oxford University Press.

Crespo-Fernández, E. (2025). Taboo language research in the new millennium:
A literature review. *Complutense Journal of English Studies, 33*.
https://doi.org/10.5209/cjes.102066

Jay, T. (2009). The utility and ubiquity of taboo words.
*Perspectives on Psychological Science, 4*(2).
https://doi.org/10.1111/j.1745-6924.2009.01115.x

Lev-Ari, S., & McKay, R. (2023). The sound of swearing: Are there universal
patterns in profanity? *Psychonomic Bulletin & Review, 30*, 1103–1114.
https://doi.org/10.3758/s13423-022-02202-0

Ljung, M. (2011). *Swearing: A Cross-Cultural Linguistic Study*.
Palgrave Macmillan.

Miller, L. (2022). Bad Mouths: Taboo and Transgressive Language.
*Annual Review of Anthropology, 51*, 17–30.

Sulpizio, S., et al. (2024). Taboo language across the globe: A multi-lab
study. *Behavior Research Methods, 56*, 3794–3813.
https://doi.org/10.3758/s13428-024-02376-6
