# Research Forensics Agent Skill

This directory is a reusable Agent Skills-compatible implementation of ARIS4C011.

## Entry point

Read SKILL.md.

## Design

The skill performs:
1. artifact/provenance preflight;
2. detector applicability routing;
3. deterministic and model-based checks;
4. critic/reproduction pass;
5. dependency-aware evidence fusion;
6. human-review triage.

It never emits an automated misconduct or fraud verdict.

## Bundled reference implementation

scripts/orchestrator.py is dependency-free and intentionally small. It provides the safety and orchestration layer, not all detector implementations. Specialized detectors can be wrapped behind the detector contract without changing report semantics.

## Schemas

assets/finding.schema.json and assets/report.schema.json define portable outputs for other agents, services, or UI layers.

## Relationship to the paper

The empirical ARIS4C011 benchmark tests whether this architecture improves issue-type coverage and reviewer efficiency while resisting shortcut learning and false escalation.
