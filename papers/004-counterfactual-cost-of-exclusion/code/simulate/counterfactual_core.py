#!/usr/bin/env python3
"""Minimal temporal counterfactual core for ARIS4C004.

This is a *validation scaffold*, not the final historical simulator. It encodes
three design invariants early so later implementations cannot silently drift:

1. intervention is temporal: work before t0 is never directly removed;
2. M1/M2 respect alternative precursor paths instead of deleting all descendants;
3. CPE is sign-neutral: adaptive entry may make a counterfactual metric exceed
   the observed metric.

The graph is a DAG-like temporal influence graph of works. Edges are
(predecessor -> downstream work). Cycles or backwards-time edges are rejected.
"""

from __future__ import annotations

import argparse
import csv
import json
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Work:
    work_id: str
    year: int
    producer_id: str
    value: float = 1.0


@dataclass
class SimulationResult:
    observed_value: float
    counterfactual_value: float
    cpe: float
    directly_removed: list[str]
    dependency_lost: list[str]
    adaptively_recovered: list[str]
    model: str
    seed: int

    def as_dict(self) -> dict:
        return {
            "observed_value": self.observed_value,
            "counterfactual_value": self.counterfactual_value,
            "cpe": self.cpe,
            "directly_removed": self.directly_removed,
            "dependency_lost": self.dependency_lost,
            "adaptively_recovered": self.adaptively_recovered,
            "model": self.model,
            "seed": self.seed,
        }


class TemporalGraph:
    def __init__(self, works: Iterable[Work], edges: Iterable[tuple[str, str]]) -> None:
        self.works = {work.work_id: work for work in works}
        if len(self.works) == 0:
            raise ValueError("graph needs at least one work")
        self.incoming: dict[str, set[str]] = {wid: set() for wid in self.works}
        self.outgoing: dict[str, set[str]] = {wid: set() for wid in self.works}
        for source, target in edges:
            if source not in self.works or target not in self.works:
                raise ValueError(f"edge references unknown work: {source}->{target}")
            if self.works[source].year > self.works[target].year:
                raise ValueError(f"future-to-past edge forbidden: {source}->{target}")
            if source == target:
                raise ValueError("self edges are not allowed")
            self.outgoing[source].add(target)
            self.incoming[target].add(source)
        # This also checks acyclicity and ensures same-year edges are ordered by
        # dependency, not accidentally by lexical work ID.
        self.topological_order()

    def topological_order(self) -> list[str]:
        indegree = {node: len(parents) for node, parents in self.incoming.items()}
        ready = [node for node, degree in indegree.items() if degree == 0]
        order: list[str] = []

        def sort_key(wid: str) -> tuple[int, str]:
            return self.works[wid].year, wid

        ready.sort(key=sort_key, reverse=True)
        while ready:
            node = ready.pop()
            order.append(node)
            for child in sorted(self.outgoing[node], key=sort_key):
                indegree[child] -= 1
                if indegree[child] == 0:
                    ready.append(child)
                    ready.sort(key=sort_key, reverse=True)

        if len(order) != len(self.works):
            raise ValueError("graph contains a cycle")
        return order

    def descendants(self, starts: set[str]) -> set[str]:
        seen = set(starts)
        frontier = list(starts)
        while frontier:
            node = frontier.pop()
            for child in self.outgoing[node]:
                if child not in seen:
                    seen.add(child)
                    frontier.append(child)
        return seen


def choose_direct_removals(
    graph: TemporalGraph,
    focal_person: str,
    t0: int,
    attenuation: float,
    rng: random.Random,
) -> set[str]:
    if not 0.0 <= attenuation <= 1.0:
        raise ValueError("attenuation must be in [0,1]")
    candidates = [
        work.work_id
        for work in graph.works.values()
        if work.producer_id == focal_person and work.year >= t0
    ]
    return {wid for wid in candidates if rng.random() < attenuation}


def simulate(
    graph: TemporalGraph,
    focal_person: str,
    t0: int,
    attenuation: float,
    model: str,
    seed: int = 20260918,
    replacement_probability: float = 0.5,
    recovery_value_multiplier: float = 1.0,
) -> SimulationResult:
    """Run one draw of M0, M1, or M2 on a temporal work graph.

    M0: naïve — all descendants reachable from directly removed focal works vanish.
    M1: redundancy-aware — a downstream work is lost only when *all* observed
        incoming precursor paths have been lost.
    M2: M1 plus probabilistic adaptive recovery of dependency-lost downstream
        work. Recovery uses no future candidate identity information; it is a
        bounded process parameter to be calibrated later. A multiplier >1 can
        represent outsider entry yielding greater value than the observed path.
    """
    if model not in {"M0", "M1", "M2"}:
        raise ValueError("model must be M0, M1, or M2")
    if not 0.0 <= replacement_probability <= 1.0:
        raise ValueError("replacement_probability must be in [0,1]")
    if recovery_value_multiplier < 0:
        raise ValueError("recovery_value_multiplier must be >=0")

    rng = random.Random(seed)
    direct = choose_direct_removals(graph, focal_person, t0, attenuation, rng)
    observed = sum(work.value for work in graph.works.values())

    if not direct:
        return SimulationResult(observed, observed, 0.0, [], [], [], model, seed)

    lost: set[str] = set(direct)
    dependency_lost: set[str] = set()
    recovered: set[str] = set()
    recovered_value: dict[str, float] = {}

    if model == "M0":
        lost = graph.descendants(direct)
        dependency_lost = lost - direct
    else:
        for wid in graph.topological_order():
            if wid in direct:
                continue
            parents = graph.incoming[wid]
            if not parents:
                continue
            # At least one surviving/recovered precursor keeps the observed path alive.
            live_parent_exists = any(parent not in lost or parent in recovered for parent in parents)
            if live_parent_exists:
                continue

            dependency_lost.add(wid)
            if model == "M2" and rng.random() < replacement_probability:
                recovered.add(wid)
                recovered_value[wid] = graph.works[wid].value * recovery_value_multiplier
            else:
                lost.add(wid)

    counterfactual = 0.0
    for wid, work in graph.works.items():
        if wid in direct:
            continue
        if wid in lost and wid not in recovered:
            continue
        if wid in recovered:
            counterfactual += recovered_value[wid]
        else:
            counterfactual += work.value

    # Adaptive entry can plausibly create *additional* value relative to the observed
    # path. The multiplier expresses that sign-neutral possibility; no clipping at 0.
    cpe = observed - counterfactual
    return SimulationResult(
        observed_value=observed,
        counterfactual_value=counterfactual,
        cpe=cpe,
        directly_removed=sorted(direct),
        dependency_lost=sorted(dependency_lost),
        adaptively_recovered=sorted(recovered),
        model=model,
        seed=seed,
    )


def load_graph(nodes_csv: Path, edges_csv: Path) -> TemporalGraph:
    works: list[Work] = []
    with nodes_csv.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            works.append(
                Work(
                    work_id=row["work_id"],
                    year=int(row["year"]),
                    producer_id=row["producer_id"],
                    value=float(row.get("value") or 1.0),
                )
            )
    edges: list[tuple[str, str]] = []
    with edges_csv.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            edges.append((row["source_work_id"], row["target_work_id"]))
    return TemporalGraph(works, edges)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--nodes", type=Path, required=True)
    parser.add_argument("--edges", type=Path, required=True)
    parser.add_argument("--focal-person", required=True)
    parser.add_argument("--t0", type=int, required=True)
    parser.add_argument("--attenuation", type=float, required=True)
    parser.add_argument("--model", choices=["M0", "M1", "M2"], required=True)
    parser.add_argument("--seed", type=int, default=20260918)
    parser.add_argument("--replacement-probability", type=float, default=0.5)
    parser.add_argument("--recovery-value-multiplier", type=float, default=1.0)
    args = parser.parse_args()

    graph = load_graph(args.nodes, args.edges)
    result = simulate(
        graph,
        focal_person=args.focal_person,
        t0=args.t0,
        attenuation=args.attenuation,
        model=args.model,
        seed=args.seed,
        replacement_probability=args.replacement_probability,
        recovery_value_multiplier=args.recovery_value_multiplier,
    )
    print(json.dumps(result.as_dict(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
