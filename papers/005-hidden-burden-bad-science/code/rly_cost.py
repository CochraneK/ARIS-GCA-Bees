#!/usr/bin/env python3
"""Fail-closed Researcher-Life-Years calculator for ARIS4C005.

The calculator accepts only explicitly parameterized time components. Context
anchors such as global peer-review hours, participant counts, citation penalties
or financial costs do not enter RLY unless an explicit attributable-time model
is supplied.

Every time parameter is represented as low/central/high. Empirical totals include
only EMPIRICALLY_CALIBRATED components and require an empirically calibrated
hours-per-research-year conversion. Scenario totals may include partially
calibrated/scenario components but are always labelled non-empirical.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

COMPONENTS = {"RLY-P", "RLY-D", "RLY-C", "RLY-I"}
STATUSES = {
    "EMPIRICALLY_CALIBRATED",
    "PARTIALLY_CALIBRATED",
    "SCENARIO_ONLY",
    "NOT_IDENTIFIED",
}


def triple(obj: Any, name: str) -> dict[str, float]:
    if not isinstance(obj, dict):
        raise ValueError(f"{name} must be an object with low/central/high")
    out = {}
    for key in ("low", "central", "high"):
        if key not in obj:
            raise ValueError(f"{name} missing {key}")
        value = float(obj[key])
        if value < 0:
            raise ValueError(f"{name}.{key} must be >=0")
        out[key] = value
    if not (out["low"] <= out["central"] <= out["high"]):
        raise ValueError(f"{name} must satisfy low <= central <= high")
    return out


def multiply_triples(*values: dict[str, float]) -> dict[str, float]:
    return {
        "low": _product(v["low"] for v in values),
        "central": _product(v["central"] for v in values),
        "high": _product(v["high"] for v in values),
    }


def divide_triples(
    numerator: dict[str, float],
    denominator: dict[str, float],
) -> dict[str, float]:
    if denominator["low"] <= 0:
        raise ValueError("hours_per_research_year.low must be >0")
    # Conservative interval arithmetic for positive values.
    return {
        "low": numerator["low"] / denominator["high"],
        "central": numerator["central"] / denominator["central"],
        "high": numerator["high"] / denominator["low"],
    }


def _product(values) -> float:
    out = 1.0
    for value in values:
        out *= value
    return out


def add_triples(values: list[dict[str, float]]) -> dict[str, float]:
    if not values:
        return {"low": 0.0, "central": 0.0, "high": 0.0}
    return {
        key: sum(v[key] for v in values)
        for key in ("low", "central", "high")
    }


def estimate_component(component: dict[str, Any]) -> dict[str, Any]:
    cid = str(component.get("component_id") or "").strip()
    if not cid:
        raise ValueError("component_id required")

    rly_component = str(component.get("rly_component") or "").strip()
    if rly_component not in COMPONENTS:
        raise ValueError(f"{cid}: invalid rly_component {rly_component!r}")

    status = str(component.get("calibration_status") or "").strip()
    if status not in STATUSES:
        raise ValueError(f"{cid}: invalid calibration_status {status!r}")

    result = {
        "component_id": cid,
        "rly_component": rly_component,
        "calibration_status": status,
        "overlap_group": str(component.get("overlap_group") or "").strip(),
        "evidence_id": str(component.get("evidence_id") or "").strip(),
        "identified": status != "NOT_IDENTIFIED",
    }

    if status == "NOT_IDENTIFIED":
        result["reason_not_identified"] = str(
            component.get("reason_not_identified") or ""
        )
        return result

    affected = triple(component.get("affected_units"), f"{cid}.affected_units")
    hours = triple(component.get("hours_per_unit"), f"{cid}.hours_per_unit")
    attribution = triple(
        component.get("attribution_fraction"),
        f"{cid}.attribution_fraction",
    )
    if attribution["high"] > 1:
        raise ValueError(f"{cid}: attribution_fraction cannot exceed 1")

    attributed_hours = multiply_triples(affected, hours, attribution)
    result.update(
        {
            "affected_units": affected,
            "hours_per_unit": hours,
            "attribution_fraction": attribution,
            "attributed_hours": attributed_hours,
        }
    )
    return result


def calculate(config: dict[str, Any]) -> dict[str, Any]:
    components_raw = config.get("components")
    if not isinstance(components_raw, list) or not components_raw:
        raise ValueError("components must be a non-empty list")

    conversion = config.get("hours_per_research_year")
    if not isinstance(conversion, dict):
        raise ValueError("hours_per_research_year object required")
    conversion_status = str(conversion.get("calibration_status") or "").strip()
    if conversion_status not in STATUSES:
        raise ValueError("invalid hours_per_research_year calibration_status")
    conversion_values = triple(conversion.get("value"), "hours_per_research_year.value")
    if conversion_values["low"] <= 0:
        raise ValueError("hours_per_research_year must be >0")

    estimated = [estimate_component(c) for c in components_raw]

    ids = [c["component_id"] for c in estimated]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate component_id")

    overlap: dict[str, list[str]] = {}
    for c in estimated:
        group = c.get("overlap_group") or ""
        if group:
            overlap.setdefault(group, []).append(c["component_id"])
    overlap_conflicts = {
        group: members
        for group, members in overlap.items()
        if len(members) > 1
    }

    empirical_eligible = [
        c
        for c in estimated
        if c.get("identified")
        and c["calibration_status"] == "EMPIRICALLY_CALIBRATED"
    ]
    scenario_eligible = [
        c
        for c in estimated
        if c.get("identified")
        and c["calibration_status"] in {
            "EMPIRICALLY_CALIBRATED",
            "PARTIALLY_CALIBRATED",
            "SCENARIO_ONLY",
        }
    ]

    empirical_hours = add_triples(
        [c["attributed_hours"] for c in empirical_eligible]
    )
    scenario_hours = add_triples(
        [c["attributed_hours"] for c in scenario_eligible]
    )

    empirical_total_allowed = (
        conversion_status == "EMPIRICALLY_CALIBRATED"
        and not overlap_conflicts
        and len(empirical_eligible) > 0
    )

    output: dict[str, Any] = {
        "classification": "RLY_COMPONENT_MODEL",
        "components": estimated,
        "hours_per_research_year": {
            "value": conversion_values,
            "calibration_status": conversion_status,
            "evidence_id": conversion.get("evidence_id", ""),
        },
        "overlap_conflicts": overlap_conflicts,
        "empirical_total_allowed": empirical_total_allowed,
        "empirical_attributed_hours": empirical_hours,
        "scenario_attributed_hours": scenario_hours,
        "scenario_rly": divide_triples(scenario_hours, conversion_values),
        "scenario_label": "SCENARIO_NOT_EMPIRICAL_ESTIMATE",
        "warnings": [
            "Participant counts, financial costs and citation penalties are not converted to RLY unless explicit time parameters are supplied.",
            "Scenario totals may combine uncertain assumptions and are never promoted to empirical findings.",
            "Overlapping components block the empirical total until double-counting is resolved.",
        ],
    }

    if empirical_total_allowed:
        output["empirical_rly"] = divide_triples(
            empirical_hours,
            conversion_values,
        )
    else:
        reasons = []
        if conversion_status != "EMPIRICALLY_CALIBRATED":
            reasons.append("RESEARCH_YEAR_CONVERSION_NOT_EMPIRICALLY_CALIBRATED")
        if overlap_conflicts:
            reasons.append("OVERLAP_DOUBLE_COUNT_RISK")
        if not empirical_eligible:
            reasons.append("NO_EMPIRICALLY_CALIBRATED_COMPONENTS")
        output["empirical_rly_blocked_reasons"] = reasons

    central_scenario_rly = output["scenario_rly"]["central"]
    output["scenario_equivalents"] = {
        "five_year_phd_equivalents": central_scenario_rly / 5.0,
        "forty_year_research_careers": central_scenario_rly / 40.0,
        "classification": "ARITHMETIC_COMMUNICATION_ONLY",
    }
    return output


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("config_json", type=Path)
    p.add_argument("output_json", type=Path)
    args = p.parse_args()

    config = json.loads(args.config_json.read_text(encoding="utf-8"))
    result = calculate(config)
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
