"""Deterministic detector adapters for ARIS4C011 Pilot 1.

These adapters intentionally operate on already-structured inputs. Extraction
from arbitrary PDFs is a separate stage and must preserve source locators.

Dependencies:
    scipy (NHST recomputation only)

No adapter infers misconduct or intent.
"""

from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP
import math
import re
from typing import Any, Dict, List, Optional, Sequence, Tuple

from orchestrator import Applicability, Finding, ForensicContext


def _decimal_places(text: str) -> int:
    token = str(text).strip().lower()
    if "e" in token:
        return max(0, -Decimal(token).as_tuple().exponent)
    return len(token.split(".", 1)[1]) if "." in token else 0


def _round_half_up(value: float, decimals: int) -> Decimal:
    q = Decimal(1).scaleb(-decimals)
    return Decimal(str(value)).quantize(q, rounding=ROUND_HALF_UP)


def _rounded_equal(computed: float, reported: str) -> bool:
    target = Decimal(str(reported).strip())
    dp = _decimal_places(str(reported))
    return _round_half_up(computed, dp) == target


_P_RE = re.compile(r"^\s*(?:p\s*)?([<>=]?)\s*(0?(?:\.\d+)|1(?:\.0+)?)\s*$", re.I)


def parse_reported_p(text: str) -> Tuple[str, float, int]:
    """Parse p=.032, .032, <.001, >.10 or =.05."""
    m = _P_RE.match(str(text))
    if not m:
        raise ValueError(f"Unsupported reported p format: {text!r}")
    op = m.group(1) or "="
    num = m.group(2)
    if num.startswith("."):
        num = "0" + num
    return op, float(num), _decimal_places(num)


def p_is_consistent(computed: float, reported: str) -> bool:
    op, value, decimals = parse_reported_p(reported)
    if op == "<":
        return computed < value
    if op == ">":
        return computed > value

    quantum = 10 ** (-decimals)
    lower = max(0.0, value - 0.5 * quantum)
    upper = min(1.0, value + 0.5 * quantum)
    # Half-open upper bound reflects ordinary rounding intervals.
    return lower <= computed < upper or math.isclose(computed, value, abs_tol=1e-15)


def recompute_p(record: Dict[str, Any]) -> float:
    try:
        from scipy import stats
    except ImportError as exc:
        raise RuntimeError("scipy is required for NHST recomputation") from exc

    kind = str(record.get("test_type", "")).strip().lower()
    stat = float(record["statistic"])
    alternative = str(record.get("alternative", "two-sided")).lower()

    if kind == "t":
        df = float(record["df"])
        if alternative == "two-sided":
            return float(2 * stats.t.sf(abs(stat), df))
        if alternative == "greater":
            return float(stats.t.sf(stat, df))
        if alternative == "less":
            return float(stats.t.cdf(stat, df))
        raise ValueError(f"Unsupported alternative: {alternative}")

    if kind in {"z", "normal"}:
        if alternative == "two-sided":
            return float(2 * stats.norm.sf(abs(stat)))
        if alternative == "greater":
            return float(stats.norm.sf(stat))
        if alternative == "less":
            return float(stats.norm.cdf(stat))
        raise ValueError(f"Unsupported alternative: {alternative}")

    if kind in {"chi2", "chisq", "chi-square"}:
        return float(stats.chi2.sf(stat, float(record["df"])))

    if kind == "f":
        return float(stats.f.sf(stat, float(record["df1"]), float(record["df2"])))

    raise ValueError(f"Unsupported test_type: {kind}")


class NHSTConsistencyDetector:
    detector_id = "nhst_recompute"
    detector_version = "pilot1-0.1.0"
    family = "statistical_inference"

    def applicability(self, context: ForensicContext) -> Applicability:
        records = context.content.get("nhst_tests") or []
        if not records:
            return Applicability(False, "No structured NHST records were supplied.")
        return Applicability(
            True,
            "At least one supported structured NHST result is available for recomputation.",
        )

    def run(self, context: ForensicContext) -> Sequence[Finding]:
        findings: List[Finding] = []
        for i, record in enumerate(context.content.get("nhst_tests") or []):
            locator = str(record.get("source_locator") or f"nhst_tests[{i}]")
            try:
                computed = recompute_p(record)
                reported = str(record["reported_p"])
                ok = p_is_consistent(computed, reported)
                findings.append(Finding(
                    detector_id=self.detector_id,
                    detector_version=self.detector_version,
                    family=self.family,
                    applicable=True,
                    applicability_reason="Supported test type and sufficient parameters were supplied.",
                    status="PASS" if ok else "FLAG",
                    evidence_class="E1",
                    claim=(
                        "Reported p value is compatible with recomputation and stated rounding."
                        if ok else
                        "Reported p value is incompatible with recomputation under the stated test assumptions."
                    ),
                    source_locator=locator,
                    evidence={
                        "test_type": record.get("test_type"),
                        "statistic": record.get("statistic"),
                        "df": record.get("df"),
                        "df1": record.get("df1"),
                        "df2": record.get("df2"),
                        "alternative": record.get("alternative", "two-sided"),
                        "reported_p": reported,
                        "recomputed_p": computed,
                    },
                    reproducible="yes",
                    benign_explanations=[] if ok else [
                        "The manuscript may have used a multiplicity or sphericity correction not represented in the structured record.",
                        "The test may have been one-sided rather than the supplied alternative.",
                        "The statistic, degrees of freedom, or p value may have been extracted incorrectly.",
                        "The discrepancy may be a reporting or transcription error.",
                    ],
                    dependency_group=f"nhst:{locator}",
                    next_action=None if ok else "Verify the source statistic, degrees of freedom, tail, and any correction, then recompute manually.",
                    misconduct_inference=False,
                ))
            except (KeyError, TypeError, ValueError) as exc:
                findings.append(Finding(
                    detector_id=self.detector_id,
                    detector_version=self.detector_version,
                    family=self.family,
                    applicable=False,
                    applicability_reason=f"Record is incomplete or unsupported: {exc}",
                    status="ABSTAIN",
                    evidence_class="E0",
                    claim="NHST record could not be validly recomputed.",
                    source_locator=locator,
                    evidence={"record": dict(record)},
                    reproducible="yes",
                    benign_explanations=[],
                    dependency_group=f"nhst:{locator}",
                    next_action="Supply a supported test type with the required statistic and degrees of freedom.",
                    misconduct_inference=False,
                ))
        return findings


def _integer_mean_compatible(
    reported_mean: str, n: int, scale_min: int, scale_max: int
) -> Tuple[bool, List[str]]:
    target = Decimal(str(reported_mean))
    dp = _decimal_places(str(reported_mean))
    quantum = Decimal(1).scaleb(-dp)
    dn = Decimal(n)
    possible: List[str] = []
    for total in range(n * scale_min, n * scale_max + 1):
        exact = Decimal(total) / dn
        if exact.quantize(quantum, rounding=ROUND_HALF_UP) == target:
            possible.append(str(exact))
    return bool(possible), possible[:10]


class GRIMItemMeanDetector:
    detector_id = "grim_item_mean"
    detector_version = "pilot1-0.1.0"
    family = "numerical_forensics"

    def applicability(self, context: ForensicContext) -> Applicability:
        records = context.content.get("discrete_means") or []
        eligible = [
            r for r in records
            if r.get("integer_valued") is True
            and r.get("n") is not None
            and r.get("scale_min") is not None
            and r.get("scale_max") is not None
        ]
        if not eligible:
            return Applicability(
                False,
                "No discrete-mean record explicitly satisfied integer-valued and denominator/scale requirements.",
            )
        return Applicability(True, "At least one GRIM-compatible discrete-mean record is available.")

    def run(self, context: ForensicContext) -> Sequence[Finding]:
        findings: List[Finding] = []
        for i, record in enumerate(context.content.get("discrete_means") or []):
            locator = str(record.get("source_locator") or f"discrete_means[{i}]")
            if record.get("integer_valued") is not True:
                findings.append(Finding(
                    detector_id=self.detector_id,
                    detector_version=self.detector_version,
                    family=self.family,
                    applicable=False,
                    applicability_reason="Outcome was not explicitly verified as integer-valued.",
                    status="ABSTAIN",
                    evidence_class="E0",
                    claim="GRIM-style feasibility was not applied.",
                    source_locator=locator,
                    evidence={"record": dict(record)},
                    reproducible="yes",
                    benign_explanations=[],
                    dependency_group=f"mean:{locator}",
                    misconduct_inference=False,
                ))
                continue

            try:
                n = int(record["n"])
                smin = int(record["scale_min"])
                smax = int(record["scale_max"])
                if n <= 0 or smin > smax:
                    raise ValueError("invalid N or scale bounds")
                reported = str(record["reported_mean"])
                ok, preview = _integer_mean_compatible(reported, n, smin, smax)
                findings.append(Finding(
                    detector_id=self.detector_id,
                    detector_version=self.detector_version,
                    family=self.family,
                    applicable=True,
                    applicability_reason="Integer-valued item, valid N, and scale bounds were supplied.",
                    status="PASS" if ok else "FLAG",
                    evidence_class="E1",
                    claim=(
                        "Reported mean is compatible with at least one legal integer total."
                        if ok else
                        "No legal integer total produces the reported rounded mean under the stated assumptions."
                    ),
                    source_locator=locator,
                    evidence={
                        "reported_mean": reported,
                        "n": n,
                        "scale_min": smin,
                        "scale_max": smax,
                        "compatible_exact_means_preview": preview,
                    },
                    reproducible="yes",
                    benign_explanations=[] if ok else [
                        "The denominator may differ from the stated N.",
                        "The score may be composite, weighted, imputed, or non-integer.",
                        "A different rounding convention may have been used.",
                        "The value may contain a transcription error.",
                    ],
                    dependency_group=f"mean:{locator}",
                    next_action=None if ok else "Verify denominator, scoring granularity, and rounding from the original analysis.",
                    misconduct_inference=False,
                ))
            except (KeyError, TypeError, ValueError, ArithmeticError) as exc:
                findings.append(Finding(
                    detector_id=self.detector_id,
                    detector_version=self.detector_version,
                    family=self.family,
                    applicable=False,
                    applicability_reason=f"Insufficient/invalid GRIM inputs: {exc}",
                    status="ABSTAIN",
                    evidence_class="E0",
                    claim="GRIM-style feasibility could not be evaluated.",
                    source_locator=locator,
                    evidence={"record": dict(record)},
                    reproducible="yes",
                    benign_explanations=[],
                    dependency_group=f"mean:{locator}",
                    misconduct_inference=False,
                ))
        return findings


def _binary_compatible(
    reported_mean: str,
    reported_sd: str,
    n: int,
    *,
    sample_sd: bool,
) -> Tuple[bool, List[Dict[str, float]]]:
    if n <= 0:
        raise ValueError("N must be positive")
    if sample_sd and n < 2:
        raise ValueError("sample SD requires N >= 2")

    compatible: List[Dict[str, float]] = []
    for successes in range(n + 1):
        mean = successes / n
        variance = mean * (1 - mean)
        if sample_sd:
            variance *= n / (n - 1)
        sd = math.sqrt(max(0.0, variance))
        if _rounded_equal(mean, reported_mean) and _rounded_equal(sd, reported_sd):
            compatible.append({"successes": successes, "mean": mean, "sd": sd})
    return bool(compatible), compatible[:10]


class DebitStyleBinaryDetector:
    """Conservative DEBIT-style feasibility check; not a code port of scrutiny."""

    detector_id = "binary_mean_sd_feasibility"
    detector_version = "pilot1-0.1.0"
    family = "numerical_forensics"

    def applicability(self, context: ForensicContext) -> Applicability:
        records = context.content.get("binary_summaries") or []
        if not records:
            return Applicability(False, "No binary mean/SD summary records were supplied.")
        return Applicability(True, "At least one binary summary record is available.")

    def run(self, context: ForensicContext) -> Sequence[Finding]:
        findings: List[Finding] = []
        for i, record in enumerate(context.content.get("binary_summaries") or []):
            locator = str(record.get("source_locator") or f"binary_summaries[{i}]")
            if record.get("binary") is not True:
                findings.append(Finding(
                    detector_id=self.detector_id,
                    detector_version=self.detector_version,
                    family=self.family,
                    applicable=False,
                    applicability_reason="Variable was not explicitly verified as binary.",
                    status="ABSTAIN",
                    evidence_class="E0",
                    claim="Binary mean/SD feasibility was not applied.",
                    source_locator=locator,
                    evidence={"record": dict(record)},
                    reproducible="yes",
                    benign_explanations=[],
                    dependency_group=f"binary:{locator}",
                    misconduct_inference=False,
                ))
                continue
            try:
                n = int(record["n"])
                mean = str(record["reported_mean"])
                sd = str(record["reported_sd"])
                sample_sd = bool(record.get("sample_sd", True))
                ok, candidates = _binary_compatible(mean, sd, n, sample_sd=sample_sd)
                findings.append(Finding(
                    detector_id=self.detector_id,
                    detector_version=self.detector_version,
                    family=self.family,
                    applicable=True,
                    applicability_reason="Binary variable, N, mean and SD were supplied.",
                    status="PASS" if ok else "FLAG",
                    evidence_class="E1",
                    claim=(
                        "At least one binary sample is compatible with the reported rounded mean and SD."
                        if ok else
                        "No binary sample is compatible with the reported rounded mean and SD under the stated SD convention."
                    ),
                    source_locator=locator,
                    evidence={
                        "n": n,
                        "reported_mean": mean,
                        "reported_sd": sd,
                        "sample_sd": sample_sd,
                        "compatible_candidates_preview": candidates,
                    },
                    reproducible="yes",
                    benign_explanations=[] if ok else [
                        "The reported SD may use a different sample/population convention.",
                        "The variable may not actually be binary.",
                        "The denominator may differ because of missingness.",
                        "The summary values may have been extracted or transcribed incorrectly.",
                    ],
                    dependency_group=f"binary:{locator}",
                    next_action=None if ok else "Confirm binary coding, denominator, SD convention, and original unrounded summaries.",
                    misconduct_inference=False,
                ))
            except (KeyError, TypeError, ValueError, ArithmeticError) as exc:
                findings.append(Finding(
                    detector_id=self.detector_id,
                    detector_version=self.detector_version,
                    family=self.family,
                    applicable=False,
                    applicability_reason=f"Insufficient/invalid binary-summary inputs: {exc}",
                    status="ABSTAIN",
                    evidence_class="E0",
                    claim="Binary mean/SD feasibility could not be evaluated.",
                    source_locator=locator,
                    evidence={"record": dict(record)},
                    reproducible="yes",
                    benign_explanations=[],
                    dependency_group=f"binary:{locator}",
                    misconduct_inference=False,
                ))
        return findings


class TableArithmeticDetector:
    detector_id = "table_arithmetic"
    detector_version = "pilot1-0.1.0"
    family = "table_consistency"

    def applicability(self, context: ForensicContext) -> Applicability:
        if not (context.content.get("table_checks") or []):
            return Applicability(False, "No structured table arithmetic checks were supplied.")
        return Applicability(True, "At least one structured table arithmetic check is available.")

    def run(self, context: ForensicContext) -> Sequence[Finding]:
        findings: List[Finding] = []
        for i, record in enumerate(context.content.get("table_checks") or []):
            locator = str(record.get("source_locator") or f"table_checks[{i}]")
            kind = str(record.get("check_type", "")).lower()
            try:
                if kind == "percentage":
                    num = float(record["numerator"])
                    den = float(record["denominator"])
                    if den == 0:
                        raise ValueError("denominator is zero")
                    computed = 100.0 * num / den
                    reported = str(record["reported_percent"])
                    ok = _rounded_equal(computed, reported)
                    evidence = {
                        "numerator": num,
                        "denominator": den,
                        "reported_percent": reported,
                        "computed_percent": computed,
                    }
                    claim_pass = "Reported percentage is arithmetically compatible with numerator and denominator."
                    claim_flag = "Reported percentage is not arithmetically compatible with numerator and denominator."

                elif kind == "sum":
                    parts = [float(x) for x in record["parts"]]
                    computed = sum(parts)
                    reported = str(record["reported_total"])
                    ok = _rounded_equal(computed, reported)
                    evidence = {
                        "parts": parts,
                        "reported_total": reported,
                        "computed_total": computed,
                    }
                    claim_pass = "Reported total is compatible with the displayed components."
                    claim_flag = "Reported total is not compatible with the displayed components."

                elif kind == "rank_sequence":
                    ranks = sorted(int(x) for x in record["observed_ranks"])
                    expected_start = int(record.get("expected_start", ranks[0]))
                    expected_end = int(record["expected_end"])
                    expected = list(range(expected_start, expected_end + 1))
                    missing = sorted(set(expected) - set(ranks))
                    extra = sorted(set(ranks) - set(expected))
                    ok = not missing and not extra and len(ranks) == len(set(ranks))
                    evidence = {
                        "observed_ranks": ranks,
                        "expected_start": expected_start,
                        "expected_end": expected_end,
                        "missing_ranks": missing,
                        "out_of_range_ranks": extra,
                        "duplicate_count": len(ranks) - len(set(ranks)),
                    }
                    claim_pass = "Displayed rank sequence is complete and unique."
                    claim_flag = "Displayed rank sequence contains a gap, duplicate, or out-of-range rank."
                else:
                    raise ValueError(f"unsupported check_type: {kind!r}")

                findings.append(Finding(
                    detector_id=self.detector_id,
                    detector_version=self.detector_version,
                    family=self.family,
                    applicable=True,
                    applicability_reason=f"Supported table check type: {kind}.",
                    status="PASS" if ok else "FLAG",
                    evidence_class="E1",
                    claim=claim_pass if ok else claim_flag,
                    source_locator=locator,
                    evidence=evidence,
                    reproducible="yes",
                    benign_explanations=[] if ok else [
                        "Different denominator or analysis population.",
                        "Rounding convention.",
                        "A display-only transcription or omission error.",
                        "Extraction error from the source table.",
                    ],
                    dependency_group=f"table:{locator}",
                    next_action=None if ok else "Inspect the original table and recalculate from the displayed cells and stated denominator.",
                    misconduct_inference=False,
                ))
            except (KeyError, TypeError, ValueError, ArithmeticError) as exc:
                findings.append(Finding(
                    detector_id=self.detector_id,
                    detector_version=self.detector_version,
                    family=self.family,
                    applicable=False,
                    applicability_reason=f"Unsupported or incomplete table record: {exc}",
                    status="ABSTAIN",
                    evidence_class="E0",
                    claim="Table arithmetic check could not be applied.",
                    source_locator=locator,
                    evidence={"record": dict(record)},
                    reproducible="yes",
                    benign_explanations=[],
                    dependency_group=f"table:{locator}",
                    misconduct_inference=False,
                ))
        return findings


_DOI_RE = re.compile(r"^10\.\d{4,9}/\S+$", re.I)


def normalize_doi(value: str) -> str:
    text = str(value or "").strip().lower()
    text = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", text)
    text = re.sub(r"^doi:\s*", "", text)
    return text.strip().rstrip(".,;)")


class ReferenceMetadataDetector:
    """Consumes externally verified DOI-resolution records.

    Network retrieval is intentionally outside this deterministic adapter so the
    evidence record can include resolver provenance and retrieval timestamp.
    """

    detector_id = "reference_metadata"
    detector_version = "pilot1-0.1.0"
    family = "citation_forensics"

    def applicability(self, context: ForensicContext) -> Applicability:
        records = context.content.get("doi_resolutions") or []
        if not records:
            return Applicability(False, "No externally verified DOI-resolution records were supplied.")
        return Applicability(True, "At least one DOI-resolution record with provenance is available.")

    def run(self, context: ForensicContext) -> Sequence[Finding]:
        findings: List[Finding] = []
        for i, record in enumerate(context.content.get("doi_resolutions") or []):
            locator = str(record.get("source_locator") or f"doi_resolutions[{i}]")
            doi = normalize_doi(record.get("reported_doi", ""))
            verified_at = str(record.get("verified_at") or "")
            resolver = str(record.get("resolver") or "")
            if not verified_at or not resolver:
                findings.append(Finding(
                    detector_id=self.detector_id,
                    detector_version=self.detector_version,
                    family=self.family,
                    applicable=False,
                    applicability_reason="Resolver provenance or verification timestamp is missing.",
                    status="ABSTAIN",
                    evidence_class="E0",
                    claim="DOI metadata verification was not accepted as provenance-complete.",
                    source_locator=locator,
                    evidence={"reported_doi": doi, "resolver": resolver, "verified_at": verified_at},
                    reproducible="yes",
                    benign_explanations=[],
                    dependency_group=f"doi:{locator}",
                    misconduct_inference=False,
                ))
                continue

            syntax_ok = bool(_DOI_RE.match(doi))
            exists = record.get("exists")
            metadata_match = record.get("metadata_match")

            if not syntax_ok:
                ok = False
                claim = "Reported DOI does not match the canonical DOI syntax expected by this adapter."
                evidence_class = "E1"
            elif exists is False:
                ok = False
                claim = "Reported DOI did not resolve in the recorded external verification."
                evidence_class = "E2"
            elif exists is True and metadata_match is False:
                ok = False
                claim = "Reported DOI resolves, but the verified bibliographic metadata does not match the cited work."
                evidence_class = "E2"
            elif exists is True and metadata_match is True:
                ok = True
                claim = "Reported DOI resolves and verified bibliographic metadata matches the cited work."
                evidence_class = "E2"
            else:
                findings.append(Finding(
                    detector_id=self.detector_id,
                    detector_version=self.detector_version,
                    family=self.family,
                    applicable=False,
                    applicability_reason="Resolution outcome is incomplete.",
                    status="ABSTAIN",
                    evidence_class="E0",
                    claim="DOI verification outcome was incomplete.",
                    source_locator=locator,
                    evidence={"reported_doi": doi, "record": dict(record)},
                    reproducible="yes",
                    benign_explanations=[],
                    dependency_group=f"doi:{locator}",
                    misconduct_inference=False,
                ))
                continue

            findings.append(Finding(
                detector_id=self.detector_id,
                detector_version=self.detector_version,
                family=self.family,
                applicable=True,
                applicability_reason="Resolver provenance and a complete resolution outcome were supplied.",
                status="PASS" if ok else "FLAG",
                evidence_class=evidence_class,
                claim=claim,
                source_locator=locator,
                evidence={
                    "reported_doi": doi,
                    "exists": exists,
                    "metadata_match": metadata_match,
                    "resolver": resolver,
                    "verified_at": verified_at,
                    "resolved_title": record.get("resolved_title"),
                },
                reproducible="yes",
                benign_explanations=[] if ok else [
                    "The reference may contain a typographical DOI error.",
                    "The resolver may have had incomplete or temporarily unavailable metadata.",
                    "The cited bibliographic fields may have been transcribed incorrectly.",
                ],
                dependency_group=f"doi:{doi or locator}",
                next_action=None if ok else "Open the DOI and compare title, authors, year, and venue with the cited reference.",
                misconduct_inference=False,
            ))
        return findings


DEFAULT_DETERMINISTIC_DETECTORS = [
    NHSTConsistencyDetector(),
    GRIMItemMeanDetector(),
    DebitStyleBinaryDetector(),
    TableArithmeticDetector(),
    ReferenceMetadataDetector(),
]
