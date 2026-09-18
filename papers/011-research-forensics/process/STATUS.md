# STATUS — ARIS4C011

Updated: 2026-09-18

## State

**FIRST SAFE_EXACT REAL MANUSCRIPT RUN · EXTRACTION GUARD ADDED**

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
- paper-level qualification rules and code: COMPLETE;\n- object/modality-level role qualification: COMPLETE;\n- archive candidate discovery utility: COMPLETE;
- acquire and verify historical-equivalent full texts: IN PROGRESS;
- quantify SAFE_EXACT vs PROXY_ONLY vs BLOCKED attrition;
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

1. Scale object-level historical-artifact qualification beyond the six-record source-anatomy seed.
2. Acquire SAFE_EXACT body/table/reference/image objects for a pilot subset and freeze hashes/provenance.
3. Run deterministic adapters only where their required artifact roles are SAFE_EXACT; treat missing inputs as ABSTAIN rather than failures.
4. Quantify extraction error, applicability, alert yield, and human verification time; first real extraction-error case is now recorded.
5. Add image/text/semantic modules only after deterministic real-manuscript validation.
