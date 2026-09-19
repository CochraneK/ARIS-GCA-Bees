# STATUS — ARIS4C011

Updated: 2026-09-19

## State

**THIRD PRE-OUTCOME REAL TRUE-POSITIVE · ISSUE DECOMPOSITION DEMONSTRATED**

The conceptual framework is no longer only an idea/outline. ARIS4C011 now has a reusable Agent Skills-compatible skill, machine-readable finding/report schemas, a reference orchestrator, an implementation/defect registry, a full methods manuscript draft, and a real-data source-anatomy seed. Confirmatory detector-performance results are still pending and no superiority claims are permitted.

## Completed

- 10-family detector taxonomy.
- Evidence-class and dependency-aware evidence-graph semantics.
- Track A time-safe content-only vs Track B open-world benchmark.
- Issue-level ground-truth tiers and P/E/C benchmark strata.
- Shortcut-stress-test plan including BMMDetect-like retraction classifiers.
- Pilot 0 deterministic GRIM-style and N-consistency checks.
- Benchmark-v0 manifest builder with explicit Track A allow-list.
- Crossref assertion/event adapter.
- Live Crossref target-metadata and source-anatomy audit.
- Real-data seed with three heterogeneous official retraction cases.
- Metadata-leakage guard for current RETRACTED title markers.
- Track A fail-closed title-history and clean-document gates.
- Reusable research-forensics Agent Skill using the Agent Skills SKILL.md structure.
- JSON finding and report schemas.
- Dependency-free reference orchestrator with applicability, abstention and review-priority logic.
- Detector implementation/defect registry.
- Known GRIMMER implementation warning recorded and prevented from silently entering confirmatory evidence.
- Full English methods/benchmark manuscript draft in manuscript/DRAFT.md.
- GT-B correction/corrigendum honest-error stress seed with figure-panel, scientific-figure, and ranked-table errors.
- Pilot 1 deterministic detector adapters for F1/F2/F3/F5.
- Record-level ABSTAIN semantics hardened in the orchestrator so one applicable detector can still abstain on individual records.
- Pilot 1 passed dedicated CI and was promoted to main.
- Time-safe artifact qualification implemented with SAFE_EXACT / PROXY_ONLY / BLOCKED states.
- Six-record current-artifact seed audit added; no current representation is assumed Track-A-safe without historical proof.
- First pre-outcome historical publisher-page snapshot verified for PLOS target 10.1371/journal.pone.0161231 (Wayback 2022-05-20).
- Object/modality-level eligibility added: historical HTML is SAFE_EXACT for text/caption roles, while Figure 1 remains BLOCKED because no independent pre-correction image capture was found.
- Track A eligibility is now defined at paper × issue × required artifact role, not paper alone.
- Real SAGE correction case revealed that rank presence is insufficient: row 14 existed conceptually but its article-information cell was the documented omission.
- F3 table checks now include row_completeness in addition to rank_sequence.
- Wayback/CDX candidate discovery helper added with strict pre-event filtering.
- PLOS SAFE_EXACT body-text smoke test correctly abstained for F1/GRIM because required recomputation inputs were absent.
- First exact historical publisher PDF recovered: J-STAGE 10.1538/expanim.54.1, captured 2018-07-25 before the 2022 retraction.
- Pilot 1C real-manuscript run: all currently implemented deterministic families correctly ABSTAIN on this review; review priority NONE.
- Real extractor QA failure documented: automated extraction confused 2004 received/accepted dates with publication year and misreported pages as 1-8 instead of 1-6.
- Track A now fails closed when any supplied structured detector record lacks source_locator or provenance_verified=true.
- CDX query builder fixed to end on event_date - 1 day rather than querying the outcome day.
- Archive wildcard identity-collision guard added after J-STAGE prefix search returned neighbouring article IDs.
- Six-seed source-candidate registry and reproducible artifact-search manifest builder added.
- Six issues now have explicit Track A content-eligibility / artifact-role requirements.
- Pilot 2 seed acquisition result quantified: 3 content-eligible, 2 content-ineligible process/authorship issues, 1 adjudication-required issue.
- Two of six targets have at least one SAFE_EXACT historical object, but 0/3 content-eligible issues are currently SAFE_EXACT-ready at their required artifact role.
- Acquisition readiness is now reported separately from detector performance.
- Expanded Pilot 2B adds PLOS DOI 10.1371/journal.pone.0258910 with a SAFE_EXACT pre-correction PDF captured 2022-01-14.
- New F5 cross_source_field_consistency adapter compares source-verified target fields with a contemporaneously available cited source.
- First real Track A true-positive: N matched, while RMSEA, CFI and best-fitting-model fields disagreed with Harper & Rhodes (2021); the later 2024 correction independently confirms these same errors.
- The first true-positive is a pipeline demonstration only, not a performance estimate.
- Pilot 3 candidate prioritisation is now code-driven rather than manual, with PRIORITY / SECONDARY / CONTROL / DEFER / COMPLETE states.
- Seven documented PLOS correction candidates have been triaged plus the completed Pilot 2B case.
- Exact pre-correction PLOS PDF recovered for 10.1371/journal.pone.0263337 (Wayback 2022-02-09, digest JH73D3J2WEFFQC75H7OUERJ74OJMJZKP); retained as a formatting/honest-error CONTROL rather than a scientific true-positive.
- Publication-day institutional copy of PLOS DOI 10.1371/journal.pone.0293412 verified byte-identical to the PLOS printable PDF (SHA-256 95460abea1594e8f8f1aec4e8fb029df0e0faacf4e7244ba7ddb25dc7eefe60b).
- Contemporaneous OSF survey1_ratings.csv verified as current_version=1, created/modified 2023-07-28, N=353, SHA-256 90f86ae54abb67e980a3379bfc95ab796fb9ebfe1ea9580fa4afde8743a035bb.
- New F3 categorical_aggregate_recompute adapter added with complete-frequency-table, hash, date, alias and provenance requirements.
- Second real Track A true-positive: historical Table 1 reports Mexico 16 / 4.5%, while case/diacritic-normalized deposited data deterministically yield 17 / 4.8%; the 2025 official correction independently confirms those values.
- The same historical table remains internally arithmetic-consistent because Mexico -1 is compensated by Other +1; this is a real complementarity example where within-table arithmetic can PASS while raw-data-to-table consistency FLAGs.
- Third real Track A true-positive: PLOS 10.1371/journal.pone.0180906 has a SAFE_EXACT 2017-07-24 publisher HTML snapshot whose Results text attributes multiple-analysis findings to Table 1 while the same historical Table 1 caption describes only univariate logistic regression.
- New F8 cross_section_scope_coherence adapter flags that body-to-caption scope mismatch as E1 / MODERATE; the 2018 correction later independently confirms that the Table 1 caption was erroneous.
- The same correction's two-missing-columns sub-issue remains BLOCKED because the historical Table 1 image object was not archived. One correction notice is now explicitly decomposed into independently eligible/ineligible sub-issues.

## Critical design findings already established

1. **Current metadata is outcome-contaminated in some cases.** Track A must use time-safe artifacts, not simply remove a retraction-reason column.
2. **Retraction is not one forensic label.** The seed spans manuscript-validity concerns, gift authorship, and manipulated peer review.
3. **Not every official issue is content-detectable.** Detector applicability and overall coverage must be reported separately.
4. **Integrated systems inherit component defects.** Detector versions and known bugs are first-class provenance; the current documented GRIMMER test-3 false-positive warning is the first registry example.
5. **Integration alone is not the novelty.** STM Integrity Hub and prior multimodal classifiers already occupy that space; 011 targets issue-level benchmarking, time safety, applicability/abstention, evidence dependencies, shortcut audits, correction controls, and human review burden.

## Locked decisions

- Unit of truth: issue-level evidence, not author-level misconduct labels.
- Automated output: anomaly/evidence/review priority, never intent or guilt.
- Primary benchmark: time-safe content-only Track A.
- Secondary benchmark: open-world triage Track B.
- Primary endpoint: eligible issue-type recall at a prespecified false-alert burden.
- Core comparison: integrated framework vs detector families vs LLM-only and retraction-classifier baselines.
- Required analysis: leave-one-family-out ablation and shortcut stress tests.
- Applicability/abstention and detector coverage are mandatory metrics.
- Fairness audit required; geography, nationality, name origin and institutional prestige cannot be operational suspicion features.
- No-known-notice comparators are never called clean controls.
- Detector versions/known defects are frozen before confirmatory scoring.

## Gates remaining

### Gate 1 — scale benchmark provenance
- scale assertion/event/target ingestion;
- add correction/corrigendum stress set;
- complete issue adjudication;
- quantify historical-artifact availability;
- freeze target metadata completeness criteria.

### Gate 2 — time-safe Track A corpus
- paper-level qualification rules and code: COMPLETE;
- object/modality-level role qualification: COMPLETE;
- archive candidate discovery utility: COMPLETE;
- archive identity/collision guard + source-candidate manifest: COMPLETE;
- acquire and verify historical-equivalent full texts: IN PROGRESS;
- quantify SAFE_EXACT vs PROXY_ONLY vs BLOCKED attrition: SEED PILOT COMPLETE; scale-up IN PROGRESS;
- build grouped and temporal split manifests;
- verify no label-bearing metadata reaches model features.

### Gate 3 — detector adapters
- implement/wrap confirmatory versions of F1-F10 modules;
- freeze each detector contract/version/applicability rule;
- validate known bugs and calibration.

### Gate 4 — confirmatory freeze and run
- freeze metrics, alert burden, splits, models, thresholds and subgroup analyses;
- run benchmark once under the frozen protocol;
- perform human-review experiment;
- fill manuscript Results and Discussion with empirical estimates.

## Immediate next execution

1. Work the updated Pilot 3 queue with the adaptive-p-value correction as active rank 1.
2. Run the construction decimal-separator CONTROL through the same reporting stack and verify it is not escalated as a scientific contradiction.
3. Begin a small no-known-concern matched comparator set now that three substantive SAFE_EXACT_READY development cases exist.
4. Quantify descriptive detector-family yield only as a development summary; do not estimate confirmatory sensitivity/precision from Pilot 3.
5. Keep Pilot 3 explicitly separate from the later frozen confirmatory cohort.
