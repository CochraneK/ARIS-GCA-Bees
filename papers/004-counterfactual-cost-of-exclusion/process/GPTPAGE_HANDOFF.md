# GPTPAGE HANDOFF — ARIS4C004

This project must remain runnable without a paid LLM API. When an ARIS research/reviewer stage requires an unavailable external model/API, use the prompt packets below in a GPT web page and save the returned review under `process/gptpage/YYYY-MM-DD_<stage>.md`.

## General rules

1. Review the **current repository files**, especially `README.md`, `IDEA_REPORT.md`, `AUTO_REVIEW.md`, `DATA_FEASIBILITY.md`, `EXPOSURE_CODEBOOK.md`, and `RESEARCH_PLAN.md`.
2. Do not alter exposure definitions, domains, outcomes, or substitution rules after seeing a preferred confirmatory result without labeling the change exploratory.
3. Every literature-search packet must return DOI/PMID/stable source links and distinguish verified papers from search leads.
4. Do not infer psychiatric diagnoses for living people or from artistic output/behavior alone.
5. Treat historical diagnosis as evidence-graded and uncertain.
6. Treat GPTPage output as advisory. Verify factual claims against primary literature or official data documentation before they enter the canonical plan.
7. The desired reviewer posture is adversarial epistemic reliability, not making the project look publishable at any cost.

---

## Packet A — exact novelty / predecessor review

**Goal:** determine whether the proposed combination has already been done.

Prompt:

> Act as an adversarial interdisciplinary novelty reviewer for ARIS4C004, "The Counterfactual Cost of Exclusion: Mental Health and Keystone Individuals in Human Knowledge Networks." Search across scientometrics/science of science, innovation economics, social-network analysis, historiometry/creativity research, disability studies, cultural analytics, sociology of science, and mental-health stigma/discrimination. Find exact or near-exact predecessors that combine any of: historical mental-health evidence; notable/scientific contributor sampling; node removal or participation attenuation; counterfactual downstream knowledge loss; star death/absence; adaptive replacement/rewiring; discrimination-related participation loss; cross-domain cultural influence networks. For each close paper provide full citation/DOI, population, exposure/intervention, network/data source, outcome, counterfactual method, whether adaptation is modeled, and exactly what would remain novel in ARIS4C004. Explicitly search for papers whose title does not mention mental health but whose design could subsume this project. End with one of: (1) novelty defensible as currently framed, (2) novelty requires narrowing, (3) substantially duplicated. Do not equate sparse search hits with novelty.

Expected output: `process/gptpage/<date>_novelty.md`

---

## Packet B — retrospective mental-health evidence reviewer

**Goal:** stress-test `EXPOSURE_CODEBOOK.md`.

Prompt:

> Review the ARIS4C004 historical mental-health evidence codebook as a psychiatric epidemiologist + medical historian. Identify where A1/A2/B1/B2/C/U categories could cause misclassification, presentism, diagnostic reification, or differential ascertainment by fame/era/gender/geography. Compare the protocol with methodological literature on retrospective diagnosis, psychiatric historiography, historical epidemiology, and case ascertainment. Recommend exact revisions to source hierarchy, stopping rules, coder blinding, adjudication, and sensitivity analyses. Do not provide or speculate about diagnoses of named living people. End with a minimal frozen confirmatory exposure rule.

Expected output: `process/gptpage/<date>_exposure-review.md`

---

## Packet C — causal/DAG and estimand review

Prompt:

> Review ARIS4C004's causal structure. Distinguish underlying condition, symptom burden, treatment, stigma, discrimination, formal institutional exclusion, documentation intensity, fame/notability, productive participation, network position, and downstream knowledge output. Draw at least three conceptual DAGs: (1) descriptive structural-position comparison among historically visible contributors, (2) participation-intervention simulation, and (3) discrimination-scaled scenario. Identify colliders created by conditioning on fame/notability or documentation. State which quantities are causal, descriptive, simulated, or not identified. Pay special attention to the fact that fully excluded people may be absent from the historical record. Recommend exact claim language that avoids implying that mental illness causes creativity.

Expected output: `process/gptpage/<date>_dag-estimand.md`

---

## Packet D — counterfactual simulator red team

Prompt:

> Act as a network-science and innovation-economics reviewer. Red-team ARIS4C004's M0 naive deletion, M1 observed-alternative-path recovery, M2 dynamic rewiring, and M3 alternative-precursor/discovery-delay models. Identify look-ahead bias, conservation-of-output assumptions, double counting, endogenous field growth, topic-definition leakage, unrealistic rewiring, and cases where removing a star could improve outsider entry. Use empirical star-death literature to propose plausible calibration/bounds but do not import one coefficient as universal. Recommend synthetic validation tests and negative controls that the simulator must pass before it is applied to mental-health-related scenarios.

Expected output: `process/gptpage/<date>_simulator-review.md`

---

## Packet E — science-pilot data review

Prompt:

> Audit the proposed ARIS4C004 science-first pilot. Verify current OpenAlex, Crossref, Wikidata, and candidate-frame documentation/licensing; assess historical coverage for 1900–2000; identify author-disambiguation and citation-coverage weaknesses; and propose a reproducible candidate-sampling algorithm that is independent of mental-health evidence. Compare using the Laouenan et al. cross-verified notable-person database versus an OpenAlex-derived frame or a hybrid. Recommend pilot strata, minimum publication/network thresholds, and how to prevent Wikipedia notability from becoming the sole inclusion gate. Separate what can be committed publicly from what must be reconstructed.

Expected output: `process/gptpage/<date>_science-data.md`

---

## Packet F — humanities/arts portability gate

Prompt:

> Evaluate whether ARIS4C004 can credibly extend beyond science into (a) philosophy/literature/intellectual history and (b) visual arts/music. Identify public/curated databases for people, works, teacher-student relationships, citations/references, movements, exhibitions/performances, and explicitly documented influence. Focus on whether influence edges can be reproduced with provenance rather than inferred from vague stylistic similarity. For each domain return expected coverage, licensing constraints, measurement validity, automation burden, and a GO / CONDITIONAL / NO-GO recommendation using the project's prospective feasibility gates. It is acceptable to recommend dropping a domain.

Expected output: `process/gptpage/<date>_portability.md`

---

## Packet G — matched-control / selection-bias reviewer

Prompt:

> Review ARIS4C004's comparison strategy as a causal-inference/selection-bias expert. The candidate population is historically visible contributors, mental-health documentation depends on fame and archival richness, and there is no clean "healthy" historical control. Assess collider bias from notability, documentation-dependent exposure ascertainment, common-support failure, and overmatching on network position. Compare two benchmark families: contribution-context matching without tight centrality matching and role matching including network position. Recommend exact balance diagnostics, missingness sensitivity, label-permutation rules, and language for what each comparison can and cannot identify.

Expected output: `process/gptpage/<date>_selection-review.md`

---

## Packet H — preregistration adversary

Prompt:

> Act as a hostile but constructive preregistration reviewer for ARIS4C004. Find every remaining researcher degree of freedom in: time window; candidate-frame construction; mental-health evidence tier; search stopping rules; OpenAlex identity resolution; topic/subfield definition; intervention start time; attenuation level; replacement model; rewiring strength; alternative-path definition; network value/outcomes; matching variables; documentation score; celebrity exclusions; simulation seeds; cross-domain synthesis; and discrimination parameter transport. Return a table with decision, current ambiguity, how it could bias results, exact rule to freeze, and confirmatory vs exploratory status. End with a minimum preregistration checklist.

Expected output: `process/gptpage/<date>_prereg-review.md`

---

## Packet I — stigma/discrimination parameter review

Prompt:

> Review whether and how ARIS4C004 can map mental-health stigma/discrimination into participation attenuation. Search systematic reviews, natural experiments, audit studies, longitudinal workplace studies, and historical legal/institutional evidence. Separate effects on hiring, retention, income, education/training, disclosure, institutionalization, publication/opportunity, and social inclusion. Distinguish association from causal evidence and modern from historical transportability. Recommend parameter distributions or bounds only when empirically defensible. If evidence does not support a historical causal parameter, say so and recommend scenario-only language.

Expected output: `process/gptpage/<date>_discrimination-parameters.md`

---

## Packet J — ethics / stigma-language review

Prompt:

> Review ARIS4C004 from disability-studies, psychiatric-stigma, research-ethics, and history-of-medicine perspectives. Identify wording or analytic choices that could romanticize mental illness, reinforce the "mad genius" stereotype, treat diagnoses as identities, expose sensitive information unnecessarily, or imply that disability is valuable only when it produces exceptional people. Review the deceased-only rule and use of historical medical evidence. Recommend a short ethics/language statement and any necessary design changes without requiring the project to abandon legitimate historical research.

Expected output: `process/gptpage/<date>_ethics-language.md`

---

## Packet K — full design red team

Use after pilot metrics exist but before confirmatory expansion.

Prompt:

> Red-team the full ARIS4C004 pilot as if the preferred conclusion is wrong. Try to explain any apparent exclusion cost by fame selection, archive density, OpenAlex coverage, field age, network centrality, arbitrary topic boundaries, non-independent focal subnetworks, celebrity cases, weak psychiatric evidence, unrealistic replacement rules, or generic key-node effects unrelated to mental health. Identify which critiques the pilot actually rules out and which remain live. Recommend a GO / NARROW / STOP decision for confirmatory expansion.

Expected output: `process/gptpage/<date>_pilot-red-team.md`

---

## Packet L — final manuscript red team

Use only after preregistered results exist.

Prompt:

> Review the final ARIS4C004 manuscript for overclaiming. Check every claim that moves from historical mental-health evidence to discrimination, from network simulation to real historical causality, or from historically visible contributors to society-wide opportunity cost. Verify that null/negative CPE outcomes, adaptive gains, uncertainty, and invisible excluded persons are reported. Require claim downgrades wherever the evidence supports only a scenario, descriptive contrast, or realized-contributor lower bound. Do not optimize for acceptance; optimize for epistemic reliability.

Expected output: `process/gptpage/<date>_full-red-team.md`
