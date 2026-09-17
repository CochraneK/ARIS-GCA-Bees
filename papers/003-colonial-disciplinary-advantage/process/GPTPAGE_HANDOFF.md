# GPTPAGE HANDOFF — ARIS4C003

This project must remain runnable without a paid LLM API. When an ARIS research/reviewer stage would normally require an unavailable API, use the relevant prompt packet below in a GPT web page and save the returned text under `process/gptpage/YYYY-MM-DD_<stage>.md`.

## Rules

1. Paste the **current frozen project files** or direct the GPT page to the repository before asking for review.
2. Do not let a GPTPage answer silently alter confirmatory hypotheses after outcome inspection.
3. Every handoff output must state the model/date if known, sources consulted, and unresolved uncertainty.
4. Treat GPTPage output as advisory evidence; verify factual claims with primary literature/data documentation.
5. If a prompt asks for literature searching, require DOI/title/source links and distinguish verified papers from suggested search leads.

---

## Packet A — novelty / closest-prior-work review

**Goal:** identify prior studies close enough to threaten novelty.

Prompt:

> You are an adversarial science-of-science reviewer. Review ARIS4C003, "Colonial Legacies and the Global Geography of Disciplinary Advantage." Search for published studies that quantitatively connect colonial/imperial history to present-day cross-national disciplinary specialization, bibliometric comparative advantage, citation impact, university subject performance, or scientific collaboration networks. Prioritize exact or near-exact predecessors over broad decolonization literature. For every close paper, return: full citation/DOI, unit of analysis, historical exposure, outcome, disciplines, years, identification method, main finding, and exactly how much it overlaps ARIS4C003. End with: (1) novelty still defensible, (2) novelty must be narrowed, or (3) project is substantially duplicated. Do not infer novelty merely because search results are sparse.

Expected output file: `process/gptpage/<date>_novelty.md`

---

## Packet B — discipline-entanglement evidence pack

**Goal:** generate historical evidence without peeking at modern outcome patterns.

Prompt:

> Build a historical evidence dossier for the following disciplines: Anthropology, Archaeology, Geography, Development Studies, Linguistics, Tropical Medicine/Public Health, Agriculture & Forestry, Geology/Earth-resource sciences, Sociology, Political Science/IR, Law, Economics, Public Administration/Social Policy, Education, History, Demography/Population Studies, Mathematics, Physics, Chemistry, Computer Science, and selected modern engineering/materials sciences. For each discipline, search credible histories of science/discipline sources and extract evidence for 11 predefined imperial-entanglement dimensions: colonial administration; mapping/survey; population/people/language classification; overseas field sites; extraction/resource survey; colonial health; agriculture/forestry transfer; legal/education transplantation; museums/archives/specimens; missionary/linguistic networks; postwar development administration. Do NOT use present-day ranking/bibliometric performance in scoring. Return evidence citations and a provisional 0–3 score for each dimension with uncertainty. Flag disciplines where a single global score is historically misleading because national traditions differ sharply.

Expected output: `process/gptpage/<date>_entanglement-evidence.md`

---

## Packet C — causal/DAG review

Prompt:

> Review the proposed causal story for ARIS4C003. Separate: pre-exposure confounders, historical mediators, modern mediators, colliders, measurement variables, and outcomes. Assess whether GDP, R&D spending, university age, common language, modern institutional quality, and present-day international collaboration should be controlled in each estimand. Produce at least three candidate DAG interpretations: total long-run association, mediated historical-knowledge-capital pathway, and prestige/network persistence. Identify controls that would create overcontrol bias. Recommend wording for causal claims that matches the design.

Expected output: `process/gptpage/<date>_dag-review.md`

---

## Packet D — preregistration adversary

Prompt:

> Act as a hostile but constructive preregistration reviewer. Your job is to find researcher degrees of freedom in ARIS4C003 before outcome inspection. Review exposure coding, discipline selection, entanglement scoring, field taxonomy, bibliometric windows, counting method, minimum-volume threshold, outcome transformations, fixed effects, small-country handling, missingness, multiple testing, ranking use, and leave-one-empire-out analyses. Return a table with: decision point, current ambiguity, how it could bias results, exact rule to freeze, and whether it belongs in confirmatory or exploratory analysis. End with a preregistration-ready checklist.

Expected output: `process/gptpage/<date>_prereg-review.md`

---

## Packet E — data acquisition / licensing review

Prompt:

> For ARIS4C003, verify the current documentation, licensing/redistribution constraints, fields, temporal coverage, and reproducible acquisition route for: ICOW Colonial History, COLDAT or equivalent colonial-duration datasets, CEPII GeoDist/Gravity, OpenAlex, Leiden Ranking Open Edition, QS subject rankings, THE subject rankings, Shanghai GRAS, World Bank/UNESCO/OECD controls. Prefer bulk downloads/snapshots and official public files over scraping. Identify any source that should not be committed to a public repository and propose a reconstruction script/instruction instead. Separate "free to access" from "free to redistribute." Do not invent permissions.

Expected output: `process/gptpage/<date>_data-licensing.md`

---

## Packet F — statistical design reviewer

Prompt:

> Review ARIS4C003 as a quantitative methods reviewer. Evaluate the country×discipline×time interaction design, country-year and discipline-year fixed effects, RCA/symmetric-RCA outcomes, fractional counting, top-paper shares, dyadic collaboration gravity models, and ranking/prestige residual models. Identify non-identification, mechanical correlations, denominator problems, dependence/clustering, sparse-field instability, and inappropriate causal language. Propose a minimal primary model and a bounded robustness set rather than an unlimited specification garden.

Expected output: `process/gptpage/<date>_methods-review.md`

---

## Packet G — full-paper red team

Use only after results exist.

Prompt:

> Red-team the full ARIS4C003 manuscript. Assume the preferred result could be spurious. Try to explain it with general scientific wealth, old universities, Anglophone indexing, field taxonomy, one dominant empire, migration of scientists, Cold War investment, ranking reputation inertia, denominator artifacts, and selective discipline choice. Identify which critiques are already empirically ruled out and which remain live. Recommend claim downgrades where evidence is associative rather than causal. Do not optimize for acceptance; optimize for epistemic reliability.

Expected output: `process/gptpage/<date>_full-red-team.md`
