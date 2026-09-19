# From General Learning Ability to Uncertainty Monitoring in Honey Bees

## A quantitative synthesis and falsifiable model-comparison framework

**Cochrane Kang**  
ARIS4C001 · Final manuscript · 18 September 2026

**Target journal:** Frontiers in Psychology — Comparative Psychology  
**Target article type:** Hypothesis and Theory  
**Main-text word count (approx.):** 3001  
**Figures:** 5  
**Tables:** 3

### Abstract

Honey bees (*Apis mellifera*) provide a tractable system for asking whether stable individual differences in cognition reflect a domain-general ability, narrower specializations, or task-local learning. Two relevant literatures are usually treated separately. Learning batteries show positive individual covariation across simple discrimination, reversal learning, and negative patterning, whereas opt-out experiments show adaptive avoidance of difficult choices. Here I synthesize these literatures while separating covariance from mechanism. A descriptive Fisher-z synthesis of the two free-flying learning conditions reported by Finke et al. (2023) yields cross-condition correlations of approximately 0.56 for initial discrimination versus reversal learning, 0.44 for initial discrimination versus negative patterning, and 0.23 for reversal learning versus negative patterning. Factor-loading vectors reported by Peñaherrera-Aguirre et al. (2024) are nearly perfectly congruent across visual and olfactory conditions (Tucker congruence = 0.99996), supporting a reproducible statistical structure in learning performance. However, the learning and opt-out studies use different animals and inferential targets, so they do not establish that a single latent process links learning ability to uncertainty-sensitive choice. I formalize five competing models: one general factor, two correlated factors, two independent factors, a trial-local associative model, and a hybrid model. A transparent synthetic recovery diagnostic further shows why small samples are poorly suited to distinguish subtle latent alternatives. The strongest current conclusion is therefore narrower than either general intelligence or metacognition: honey bees show replicable individual cognitive covariation and adaptive difficulty-sensitive choice, but the coupling and mechanism connecting these phenomena remain unmeasured. I specify a decisive same-individual experiment that can test that bridge.

**Keywords:** *Apis mellifera*; general cognitive ability; individual differences; uncertainty monitoring; metacognition; associative learning; comparative cognition; latent-variable models

---

## 1. Introduction

Individual differences are not merely noise around a species mean. Across animal cognition, stable between-individual variation can reveal how cognitive traits are organized, constrained, and potentially selected (Boogert et al., 2018; Cauchoix et al., 2018). Honey bees are particularly useful because the same individual can be followed through controlled learning tasks that differ in sensory modality and cognitive demand, while large bodies of neurobiological and behavioral work provide mechanistic hypotheses.

The central psychometric question is whether performance covaries because individuals possess a relatively domain-general cognitive resource, because narrower abilities are correlated, or because superficially similar tasks share motivation, perception, reinforcement history, or procedural demands. In honey bees, evidence has accumulated on both sides. Finke et al. (2021) reported stable proficiency within the visual domain but no corresponding prediction from visual to olfactory elemental learning, supporting specialization. Finke et al. (2023), however, found positive individual covariation among simple discrimination, reversal learning, and negative patterning within visual and olfactory free-flying protocols. Peñaherrera-Aguirre et al. (2024) reanalyzed those data with parallel analysis and exploratory factor analysis (EFA), reporting one general factor in each sensory condition.

A second literature asks a different question: whether bees respond adaptively to their own uncertainty. Perry and Barron (2013) trained free-flying honey bees in a discrimination task with an opt-out route. Bees opted out more often when choices were difficult, and performance improved when opting out was available. Four of ten bees that completed the long protocol opted out on the first presentation of a novel confusing stimulus, suggesting some transfer. Yet the authors explicitly retained an associative explanation in which difficult stimuli acquire lower expected value and the opt-out response acquires avoidance value. This interpretive tension remains central to comparative metacognition (Smith et al., 2014, 2016).

The temptation is to connect the two literatures immediately: perhaps a single “precision,” “confidence,” or general cognitive factor explains both learning ability and uncertainty-sensitive choice. That move is premature. Covariance across learning tasks and adaptive opting out are empirically established in different datasets. No published dataset considered here measures the relevant learning/GCA and opt-out phenotypes in the same bees. A single mechanism therefore cannot be inferred from their coexistence at the species level.

This paper makes four contributions. First, it gives a conservative evidence synthesis that keeps learning covariance, metacognitive interpretation, associative alternatives, and consciousness claims separate. Second, it performs a reproducible summary-statistic synthesis of the two free-flying learning conditions and quantifies cross-modality similarity in the published factor structures. Third, it formalizes mutually competing models rather than treating one preferred mechanism as the data-generating truth. Fourth, it specifies a same-individual experiment capable of discriminating those models.

The goal is not to prove or disprove insect metacognition by terminology. It is to define the empirical observation that would make a stronger inference possible.

---

## 2. Evidence base and construct boundaries

### 2.1 Individual cognitive consistency in honey bees

Finke et al. (2021) tested whether individual performance generalized across task complexity and sensory modality. Performance was stable over time and some bees performed consistently well across visual tasks of different complexity, but elemental visual proficiency did not predict equivalent elemental olfactory proficiency. This result is important because it prevents “positive manifold” from being treated as an inevitable property of any bee cognitive battery.

Finke et al. (2023) extended the question with learning batteries including the first phase of reversal learning (here treated as an initial discrimination/associative-learning indicator, AL), the second reversal phase (RL), and negative patterning (NP). In free-flying visual conditions, reported Spearman correlations were 0.53 for AL–RL (n = 27), 0.42 for AL–NP (n = 33), and 0.25 for RL–NP (n = 27). In free-flying olfactory conditions, the corresponding correlations were 0.60 (n = 20), 0.46 (n = 22), and 0.19 (n = 20). The first two relations were statistically significant in each modality; RL–NP was positive but not significant. Importantly, inclusion in second-phase reversal analyses depended on successful acquisition of the initial association, which changes sample composition and should be treated as a selection feature rather than ignored.

Peñaherrera-Aguirre et al. (2024) applied factor-analytic methods to these matrices. They reported factor loadings of 0.944 (AL), 0.562 (RL), and 0.445 (NP) for the visual condition and 0.997, 0.601, and 0.461 for the olfactory condition. The factors accounted for 46.8% and 52.3% of performance variance, respectively. These are strong indications that the covariance is structured, but a three-indicator one-factor solution is not equivalent to demonstrating a biologically unitary cognitive mechanism.

A later free-flying study adds an important constraint. Kuklovsky et al. (2026) found that visual learning proficiency was not correlated with sucrose responsiveness or phototactic responsiveness under their free-flying conditions, while emphasizing that relationships between responsiveness and learning are context dependent. Thus, simple sensory or reward responsiveness cannot automatically be assumed to explain all individual cognitive covariation, but neither can those variables be ignored across contexts.

### 2.2 Uncertainty-sensitive choice

Perry and Barron (2013) showed that honey bees adapt their use of an opt-out response to trial difficulty. Of 23 bees that completed the earlier training stages, 16 returned for the long difficulty stage and 10 completed all 50 trials. At the group level, those 10 bees opted out more on difficult than easy trials and performed better on unforced hard trials—where opting out was possible—than on forced hard trials. In a later transfer test, four of the ten opted out on the first presentation of a novel confusing stimulus and at least three of five confusing-stimulus trials.

These findings establish difficulty-sensitive decision avoidance. They do not uniquely identify its computation. Perry and Barron explicitly contrasted an uncertainty-monitoring interpretation with associative accounts in which reinforcement history and stimulus generalization determine response strength. The broader animal-metacognition literature has likewise shown that opt-out paradigms can entangle possible metacognitive monitoring with learned contingencies (Smith et al., 2014, 2016).

Accordingly, this paper uses **uncertainty-sensitive choice** for the behavioral phenomenon and reserves **metacognition** for an explanatory interpretation that requires evidence against lower-level alternatives.

### 2.3 Consciousness and self-awareness are separate questions

Recent reviews consider prediction, attention, emotion-like states, self-related processing, and metacognition relevant to the study of insect consciousness, while emphasizing that no single behavioral assay establishes subjective experience (Chittka et al., 2025). The present analysis therefore makes no inference from learning covariance or opt-out behavior to phenomenal consciousness or self-awareness.

Similarly, complex social learning in bumblebees—such as acquisition of a two-step puzzle-box behavior from trained demonstrators (Bridges et al., 2024)—is evidence about social learning and cultural transmission, not direct evidence of tool use, self-awareness, or a shared “precision” variable.

---

## 3. Quantitative synthesis of published learning covariance

### 3.1 Data

The analysis uses only published summary statistics, making the calculation transparent and independent of access to raw files. For each of the two free-flying conditions in Finke et al. (2023), the three reported Spearman correlations and pairwise sample sizes were transcribed from the article. Factor loadings and variance accounted for were transcribed from Table 1 of Peñaherrera-Aguirre et al. (2024).

This is a **descriptive cross-condition synthesis**, not a population meta-analysis. There are only two sensory conditions, both derived from the same research program, and pairwise sample sizes differ because reversal learning was evaluated only after initial acquisition.

### 3.2 Cross-condition correlation synthesis

For each task pair, correlations were Fisher-z transformed and combined using weights n − 3. Approximate 95% intervals were calculated on the z scale and transformed back to r. The procedure treats the visual and olfactory samples as independent conditions.

| Task pair | Visual rho (n) | Olfactory rho (n) | Descriptive pooled r | Approx. 95% interval |
|---|---:|---:|---:|---:|
| AL–RL | 0.53 (27) | 0.60 (20) | **0.560** | 0.316 to 0.735 |
| AL–NP | 0.42 (33) | 0.46 (22) | **0.436** | 0.185 to 0.633 |
| RL–NP | 0.25 (27) | 0.19 (20) | **0.225** | −0.077 to 0.489 |

The pattern is asymmetric: initial discrimination performance is moderately related to both reversal and negative patterning, whereas reversal and negative patterning show a weaker relation. This matters for interpretation. A positive manifold exists, but it is not an exchangeable “all tasks correlate equally” pattern.

![Figure 1. Published learning covariance](../figures/figure1_published_learning_covariance.svg)

**Figure 1. Published learning covariance.** Descriptive Fisher-z synthesis across the visual and olfactory free-flying conditions. Points are pooled correlations and horizontal intervals are approximate 95% intervals. This is not a population meta-analysis.

### 3.3 Cross-modality factor congruence

The visual loading vector reported by Peñaherrera-Aguirre et al. (2024) is ((0.944, 0.562, 0.445)), and the olfactory vector is ((0.997, 0.601, 0.461)). Their Tucker congruence coefficient is **0.99996**, indicating nearly identical relative loading structure across modalities. In both conditions, the initial discrimination/AL indicator anchors the factor most strongly, followed by reversal learning and then negative patterning.

| Indicator | Visual loading | Olfactory loading |
|---|---:|---:|
| Initial discrimination / AL | 0.944 | 0.997 |
| Reversal learning / RL | 0.562 | 0.601 |
| Negative patterning / NP | 0.445 | 0.461 |
| Variance accounted for | 46.8% | 52.3% |

![Figure 2. Cross-modality factor loading structure](../figures/figure2_factor_loading_congruence.svg)

**Figure 2. Cross-modality factor loading structure.** Published one-factor loadings reported by Peñaherrera-Aguirre et al. (2024). Statistical congruence does not establish a unitary biological mechanism.

The one-factor loadings almost perfectly reproduce the three visual correlations. For the olfactory condition, the loading products reproduce AL–RL and AL–NP closely but imply an RL–NP correlation of about 0.277 compared with the observed 0.19; the off-diagonal root-mean-square residual is approximately 0.050. This discrepancy is not a rejection of the EFA solution. It simply illustrates that a compact factor can summarize covariance without uniquely explaining every pairwise relation or establishing a single underlying biological cause.

### 3.4 Interpretation

Three points follow.

First, the positive learning covariance is not a simulation artifact. It is visible in empirical bee data and replicates in broad form across visual and olfactory conditions.

Second, the factor structure is strikingly similar across the two conditions. That is meaningful evidence for a common *statistical organization* of the three learning indicators.

Third, statistical generality is not mechanistic generality. The dominant loading of initial discrimination, small samples, selection into reversal analyses, and the cross-sensory dissociation observed in earlier work all leave open whether the factor reflects a broad cognitive resource, shared task demands, a narrower learning-efficiency trait, or correlated domain-specific processes.

![Figure 4. Evidence boundary between the two literatures](../figures/figure4_evidence_boundary.svg)

**Figure 4. Evidence boundary between the two literatures.** Existing studies establish structured learning covariance and difficulty-sensitive opt-out behavior separately. The scientifically decisive missing edge is same-individual coupling; one mechanism, metacognition, consciousness, or a shared precision/confidence variable therefore cannot be inferred from species-level coexistence.

---

## 4. Competing models

A useful theory must be able to lose. Five models are therefore treated as genuine competitors.

**M1: single general factor.** All learning and uncertainty-sensitive indicators load on one latent factor. It predicts positive cross-domain covariance after accounting for task reliability, modality, motivation, and colony.

**M2: two correlated factors.** Learning indicators load on a learning/GCA factor G; uncertainty-control indicators load on an uncertainty-sensitive factor U. The correlation rho(G,U) is estimated rather than assumed.

**M3: two independent factors.** The measurement structure is identical to M2 but rho(G,U)=0.

**M4: task-local associative model.** Opt-out choice is generated from stimulus difficulty, recent reward and punishment, generalized stimulus values, learned value of the exit response, and decision noise. No metacognitive state is required.

**M5: hybrid model.** A stable individual factor influences baseline learning efficiency or decision quality, while trial-by-trial opt-out behavior is produced by associative value computations.

A predictive-precision or confidence-like latent variable remains exploratory. It receives no privileged status, no fixed optimum, no preregistered sign for its relation to learning performance, and no assumed neural location.

| Model | Core assumption | Evidence that would favor it | Strong falsifier / challenge |
|---|---|---|---|
| M1 · single general factor | Learning and uncertainty-sensitive indicators share one latent factor | Positive cross-domain covariance and superior held-out prediction from one factor | Reliable uncertainty variation but near-zero coupling to learning/GCA |
| M2 · two correlated factors | Learning factor G and uncertainty factor U are distinct but correlated | Stable non-zero rho(G,U) with better prediction than M1/M3 | rho(G,U) near zero or one-factor prediction is equally good |
| M3 · two independent factors | Learning and uncertainty factors are separable | Reliable within-domain structure but little cross-domain covariance | Stable cross-domain covariance after nuisance control |
| M4 · task-local associative | Opt-out follows learned stimulus/response values and reinforcement history | Associative model predicts trial-level opt-out and transfer as well as richer models | Generalization not predicted by value history/similarity |
| M5 · hybrid | Stable individual differences coexist with associative trial-level choice | Individual factor and associative history both add held-out predictive value | One component adds no predictive information |

---

## 5. Model-recovery diagnostic

Before collecting a definitive dataset, it is useful to ask whether the proposed latent structures can be distinguished at realistic sample sizes. A synthetic model-recovery simulation generates six standardized indicators from two latent factors with loading 0.65 and factor correlation 0.35. One-factor, two-correlated-factor, and two-independent-factor covariance models are then compared by BIC across 200 replications at N = 60, 90, 120, and 160.

This diagnostic is **not evidence about bees**. Its sole purpose is experimental design.

Under the chosen scenario, the one-factor model is rarely selected because the synthetic data are intentionally generated from two factors. The harder discrimination is between correlated and independent two-factor models. The correlated model is selected in roughly 49% of replications at N = 60, 59.5% at N = 90, 62.5% at N = 120, and 79.5% at N = 160. These values are not universal power estimates; they depend on the assumed loading, factor correlation, scoring, and model family. They show why samples of approximately 20–30 individuals, while sufficient to reveal some pairwise associations, are unlikely to settle a subtle latent-coupling question.

![Figure 3. Synthetic model-recovery diagnostic](../figures/figure3_model_recovery.svg)

**Figure 3. Synthetic model-recovery diagnostic.** BIC model-selection rates across 200 synthetic replications at each sample size under a two-correlated-factor data-generating model (loading = 0.65; latent-factor correlation = 0.35). This is an experimental-design diagnostic only and is **not empirical evidence about bees**.

---

## 6. A decisive same-individual experiment

The critical experiment must measure learning covariance and uncertainty-sensitive choice in the **same identified bees**. A compact battery should include initial discrimination, reversal learning, negative patterning, an opt-out difficulty slope, the improvement in hard-trial accuracy when opting out is available, and transfer/generalization of the opt-out strategy.

At least six colonies should contribute individuals. Colony, task order, stimulus identity, reward sensitivity, decision latency, and attrition should be retained. Task order should be randomized or counterbalanced. A planned-missingness design is preferable to uncontrolled attrition if completing the full battery is too burdensome.

The existing literature shows why selection matters. Finke et al. (2023) conditioned second-phase reversal analyses on successful first-phase acquisition, while Perry and Barron (2013) experienced substantial attrition across a long protocol. The new study should distinguish failure to learn, failure to return, loss of motivation, procedural exclusion, and missingness by design. Where possible, trial-level hierarchical models should replace dichotomizing bees into “learners” and “non-learners.”

The confirmatory analysis should compare M1–M5 using held-out predictive performance, calibration, and posterior predictive checks. For opt-out behavior, a hierarchical logistic model can estimate the effect of difficulty and reinforcement history while allowing bee- and colony-level variation. A latent uncertainty term should be added only after the associative baseline is specified.

Strong falsifiers are straightforward. The single-general-factor model is weakened if uncertainty indicators show reliable individual variation but near-zero latent correlation with learning/GCA. A pure associative opt-out model is weakened if bees generalize uncertainty-sensitive control in ways that learned values and stimulus similarity do not predict. A broad GCA interpretation is weakened if positive covariance disappears across modalities or contexts after reliability and selection are controlled. A unitary precision account is weakened if different tasks require different latent parameters or simpler models predict equally well.

![Figure 5. Decisive same-individual experiment](../figures/figure5_same_individual_experiment.svg)

**Figure 5. Decisive same-individual experiment.** The proposed design measures learning and uncertainty-sensitive choice in the same identified bees, retains key nuisance variables, and compares the five competing models using held-out prediction, reliability, calibration, and transfer. The figure visualizes the inferential bridge that is absent from the current literature.

---

## 7. Discussion

### 7.1 What the current evidence supports

The strongest current evidence supports **structured individual variation in honey-bee cognition**. Across two free-flying sensory conditions, initial discrimination performance correlates moderately with both reversal learning and negative patterning. A one-factor summary of these learning measures has highly congruent loading structure across the two conditions. These facts make it unreasonable to dismiss individual learning covariance as random noise.

The evidence also supports **adaptive difficulty-sensitive choice**. Bees in the Perry and Barron paradigm changed their use of an opt-out response with task difficulty, benefited from that option on hard trials, and showed some transfer to novel ambiguous stimuli.

These are two substantive findings. The scientific mistake would be to turn them into a third finding that has not been measured: that the same individual-level mechanism causes both.

### 7.2 Why “GCA” should remain a statistical hypothesis, not a mechanism label

The 2024 EFA results are informative, especially the near-perfect congruence of loading profiles across modalities. Yet a general factor can arise from several causal architectures: a single common resource, multiple correlated processes, developmental quality, motivational stability, shared task structure, or mixtures of these. Factor analysis organizes covariance; it does not by itself identify its biological source.

The 2021 cross-sensory dissociation is especially valuable. If an individual can be consistently strong across visual tasks while that strength does not generalize to an equivalent olfactory task, any account of “general” ability must specify the level at which generality is expected. The 2026 free-flying study similarly shows that sensory and sucrose responsiveness do not trivially explain visual learning proficiency in that context, but also emphasizes context dependence.

A productive interpretation is therefore hierarchical rather than binary: bees may possess stable individual differences broader than single tasks but narrower than a universal cognitive factor.

### 7.3 Why opt-out behavior should not be called metacognition by default

The behavioral criteria in Perry and Barron are impressive, particularly selective opting out and transfer. But those results were designed in a literature where associative and metacognitive interpretations are explicitly competing. Calling the phenomenon “metacognition” before fitting the associative alternative changes the question by definition rather than evidence.

This is not an argument that bees lack metacognition. It is an argument for a stronger test. A same-individual design adds a dimension that trial-level associative models do not automatically predict: stable covariance between uncertainty-sensitive control and independent measures of cognitive performance. Even that covariance would not prove introspection, but it would constrain plausible mechanisms.

### 7.4 Implications for insect consciousness

The present synthesis is compatible with, but does not establish, broader claims about insect consciousness. Chittka et al. (2025) review converging evidence across multiple domains and explicitly frame consciousness as an inference from a constellation of cognitive and neural features rather than a single test. Learning covariance, uncertainty-sensitive choice, self-related processing, social learning, and subjective experience should not be collapsed into a single axis.

### 7.5 What survives from a predictive-coding idea

A precision-like interpretation remains scientifically interesting if reformulated as a risky model rather than an explanatory default. It could predict how confidence, learning rate, choice stochasticity, and opt-out behavior covary across tasks. But its parameters must be estimated from data, its predictions compared with simpler associative and latent-factor models, and neural localization independently tested.

In this form, predictive coding becomes a hypothesis generator rather than a circular explanation.

---

## 8. Limitations

First, the quantitative analysis uses published summary correlations and published factor loadings rather than an independently downloaded and reprocessed copy of the Finke raw dataset. The original raw data are publicly archived, and Peñaherrera-Aguirre et al. (2024) report reproducing the correlations from those files, but the calculations here are explicitly summary-statistic based.

Second, the descriptive pooling contains only two sensory conditions from a related experimental program. The approximate Fisher-z intervals quantify sampling uncertainty under standard assumptions but should not be read as a meta-analytic estimate of all honey-bee cognition.

Third, the three-indicator learning batteries are small for latent-variable inference. A broader battery, repeated measures, and explicit reliability estimates would make distinctions among GCA, correlated abilities, and shared task demands more credible.

Fourth, no existing dataset in this synthesis measures learning/GCA and opt-out uncertainty in the same individual. Consequently, this paper does not estimate rho(G,U) and does not report a bee-level effect linking the two constructs.

Fifth, the model-recovery exercise is conditional on a deliberately simple synthetic scenario. It illustrates identification difficulty; it is not a power analysis for a specific biological experiment.

---

## 9. Conclusion

Honey bees provide evidence for two forms of cognitive structure: reproducible individual covariation across learning tasks and adaptive sensitivity to decision difficulty. The published learning data show a positive but uneven correlation pattern, and reported factor loadings are remarkably congruent across visual and olfactory conditions. The opt-out literature shows that bees can avoid difficult choices adaptively, while leaving open whether the computation is metacognitive or associative.

What is missing is the bridge between them.

The next decisive step is not another mechanism-first simulation. It is a same-individual, multi-task experiment in which general learning structure and uncertainty-sensitive control are measured together and competing latent and associative models are forced to predict held-out behavior. Until that bridge is measured, “general cognitive ability,” “metacognition,” “precision,” and “self-awareness” should remain distinct hypotheses rather than interchangeable labels.

That narrower conclusion is also the stronger one: it identifies exactly what is known, exactly what is not known, and the observation that would change the answer.

---

## Data, code, and reproducibility

No new animal data were collected. The summary-statistic synthesis, factor-congruence calculation, and synthetic model-recovery diagnostic are available in the ARIS4C001 repository. Published numerical inputs are encoded with source notes so each value can be audited.

The public raw data underlying Finke et al. (2023) are reported by the authors as available at Figshare (doi:10.6084/m9.figshare.20473113.v). The present paper does not claim an independent raw-data replication.

## Ethics statement

No new animal experiments were conducted.

## Competing interests

The author declares no competing interests.

## Funding

No specific funding is reported for this synthesis.

## Author contributions

C.K.: conceptualization, evidence synthesis, methodology, quantitative summary analysis, model specification, writing, and repository curation.

---

## References

Barron, A. B., & Klein, C. (2016). What insects can tell us about the origins of consciousness. *PNAS*, 113, 4900–4908. https://doi.org/10.1073/pnas.1520084113

Boogert, N. J., Madden, J. R., Morand-Ferron, J., & Thornton, A. (2018). Measuring and understanding individual differences in cognition. *Philosophical Transactions B*, 373, 20170280. https://doi.org/10.1098/rstb.2017.0280

Bridges, A. D., Royka, A., Wilson, T., et al. (2024). Bumblebees socially learn behaviour too complex to innovate alone. *Nature*, 627, 572–578. https://doi.org/10.1038/s41586-024-07126-4

Cauchoix, M., Chow, P. K. Y., van Horik, J. O., et al. (2018). The repeatability of cognitive performance: a meta-analysis. *Philosophical Transactions B*, 373, 20170281. https://doi.org/10.1098/rstb.2017.0281

Chittka, L., Skeels, S., Dyakova, O., & Janbon, M. (2025). The exploration of consciousness in insects. *Philosophical Transactions B*, 380, 20240302. https://doi.org/10.1098/rstb.2024.0302

Finke, V., Baracchi, D., Giurfa, M., Scheiner, R., & Avarguès-Weber, A. (2021). Evidence of cognitive specialization in an insect: proficiency is maintained across elemental and higher-order visual learning but not between sensory modalities in honey bees. *Journal of Experimental Biology*, 224, jeb242470. https://doi.org/10.1242/jeb.242470

Finke, V., Scheiner, R., Giurfa, M., & Avarguès-Weber, A. (2023). Individual consistency in the learning abilities of honey bees: cognitive specialization within sensory and reinforcement modalities. *Animal Cognition*, 26, 909–928. https://doi.org/10.1007/s10071-022-01741-2

Kuklovsky, V., Avarguès-Weber, A., Giurfa, M., et al. (2026). Visual learning performance in free-flying honey bees is independent of sucrose and light responsiveness and depends on training context. *Scientific Reports*, 16, 1319. https://doi.org/10.1038/s41598-025-34900-9

Peñaherrera-Aguirre, M., Sarraf, M. A., Woodley of Menie, M. A., & Figueredo, A.-J. (2024). Possible evidence for the Law of General Intelligence in honeybees (*Apis mellifera*). *Intelligence*, 106, 101856. https://doi.org/10.1016/j.intell.2024.101856

Perry, C. J., & Barron, A. B. (2013). Honey bees selectively avoid difficult choices. *PNAS*, 110, 19155–19159. https://doi.org/10.1073/pnas.1314571110

Smith, J. D., Couchman, J. J., & Beran, M. J. (2014). Animal metacognition: a tale of two comparative psychologies. *Journal of Comparative Psychology*, 128, 115–131. https://doi.org/10.1037/a0033105

Smith, J. D., Zakrzewski, A. C., & Church, B. A. (2016). Formal models in animal-metacognition research: the problem of interpreting animals’ behavior. *Psychonomic Bulletin & Review*, 23, 1341–1353.
