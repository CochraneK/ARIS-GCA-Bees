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
import unicodedata
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


def _parse_locale_decimal(value: Any) -> Tuple[float, str]:
    """Parse a simple decimal token without treating locale style as an anomaly.

    Accepted forms include ordinary point decimals (0.943), comma decimals
    (0,943), optional surrounding whitespace and a leading sign. Thousands
    separators or mixed comma/point tokens are intentionally rejected because
    their interpretation is ambiguous without an explicit locale.
    """
    token = unicodedata.normalize("NFKC", str(value or "")).strip()
    if not token:
        raise ValueError("empty numeric token")
    if "," in token and "." in token:
        raise ValueError("mixed comma/point numeric token is ambiguous")
    if token.count(",") > 1 or token.count(".") > 1:
        raise ValueError("numeric token contains multiple decimal separators")

    normalized = token.replace(",", ".")
    if not re.fullmatch(r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)", normalized):
        raise ValueError(f"unsupported numeric token: {value!r}")
    return float(normalized), normalized


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

                elif kind == "numeric_range":
                    raw_value = record["reported_value"]
                    parsed, normalized = _parse_locale_decimal(raw_value)
                    lower = float(record["min_value"])
                    upper = float(record["max_value"])
                    if lower > upper:
                        raise ValueError("min_value exceeds max_value")
                    lower_inclusive = bool(record.get("lower_inclusive", True))
                    upper_inclusive = bool(record.get("upper_inclusive", True))
                    lower_ok = parsed >= lower if lower_inclusive else parsed > lower
                    upper_ok = parsed <= upper if upper_inclusive else parsed < upper
                    ok = lower_ok and upper_ok
                    evidence = {
                        "reported_value": str(raw_value),
                        "normalized_numeric_token": normalized,
                        "parsed_value": parsed,
                        "min_value": lower,
                        "max_value": upper,
                        "lower_inclusive": lower_inclusive,
                        "upper_inclusive": upper_inclusive,
                        "decimal_separator_style": (
                            "comma" if "," in str(raw_value) else "point"
                        ),
                    }
                    claim_pass = (
                        "Reported numeric token is unambiguously parseable under a "
                        "standard decimal-separator convention and lies within the "
                        "prespecified valid range."
                    )
                    claim_flag = (
                        "Reported numeric token is parseable but lies outside the "
                        "prespecified valid range."
                    )

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

                elif kind == "row_completeness":
                    rows = record["rows"]
                    required_fields = [str(x) for x in record["required_fields"]]
                    if not required_fields:
                        raise ValueError("required_fields must be non-empty")
                    missing_by_row = []
                    duplicate_keys = []
                    row_key = str(record.get("row_key", "row_id"))
                    seen_keys = set()

                    for row_index, row in enumerate(rows):
                        key_value = row.get(row_key, row_index)
                        if key_value in seen_keys:
                            duplicate_keys.append(key_value)
                        seen_keys.add(key_value)

                        missing_fields = []
                        for field_name in required_fields:
                            value = row.get(field_name)
                            if value is None:
                                missing_fields.append(field_name)
                            elif isinstance(value, str) and not value.strip():
                                missing_fields.append(field_name)
                            elif isinstance(value, (list, tuple, dict, set)) and len(value) == 0:
                                missing_fields.append(field_name)

                        if missing_fields:
                            missing_by_row.append({
                                "row_key": key_value,
                                "missing_fields": missing_fields,
                            })

                    ok = not missing_by_row and not duplicate_keys
                    evidence = {
                        "row_key": row_key,
                        "required_fields": required_fields,
                        "row_count": len(rows),
                        "missing_by_row": missing_by_row,
                        "duplicate_keys": duplicate_keys,
                    }
                    claim_pass = "Every displayed row contains the required table fields and row keys are unique."
                    claim_flag = "At least one displayed row is missing a required field or duplicates a row key."
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


def _field_values_equal(left: Any, right: Any, field_type: str = "auto") -> bool:
    """Compare source-verified fields without semantic inference."""
    kind = str(field_type or "auto").strip().lower()
    if kind in {"numeric", "auto"}:
        try:
            return Decimal(str(left).strip()) == Decimal(str(right).strip())
        except Exception:
            if kind == "numeric":
                return False
    norm = lambda v: re.sub(r"\s+", " ", str(v or "")).strip().casefold()
    return norm(left) == norm(right)


class CrossSourceFieldConsistencyDetector:
    """Compare a target summary with a source available at target-publication time."""

    detector_id = "cross_source_field_consistency"
    detector_version = "pilot2b-0.1.0"
    family = "citation_forensics"

    def applicability(self, context: ForensicContext) -> Applicability:
        records = context.content.get("cross_source_records") or []
        if not records:
            return Applicability(False, "No structured cross-source comparison records were supplied.")
        return Applicability(True, "At least one source-anchored cross-source comparison record is available.")

    def run(self, context: ForensicContext) -> Sequence[Finding]:
        findings: List[Finding] = []
        for i, record in enumerate(context.content.get("cross_source_records") or []):
            locator = str(record.get("source_locator") or f"cross_source_records[{i}]")
            target_locator = str(record.get("target_source_locator") or locator)
            comparison_locator = str(record.get("comparison_source_locator") or "")
            target_fields = record.get("target_fields")
            source_fields = record.get("source_fields")
            compare_fields = record.get("fields_to_compare")
            field_types = record.get("field_types") or {}
            source_doi = normalize_doi(record.get("source_doi", ""))

            missing = []
            if not target_locator:
                missing.append("target_source_locator")
            if not comparison_locator:
                missing.append("comparison_source_locator")
            if not isinstance(target_fields, dict):
                missing.append("target_fields")
            if not isinstance(source_fields, dict):
                missing.append("source_fields")
            if not isinstance(compare_fields, list) or not compare_fields:
                missing.append("fields_to_compare")
            if record.get("source_available_at_target_time") is not True:
                missing.append("source_available_at_target_time=true")
            if record.get("provenance_verified") is not True:
                missing.append("provenance_verified=true")

            if missing:
                findings.append(Finding(
                    detector_id=self.detector_id,
                    detector_version=self.detector_version,
                    family=self.family,
                    applicable=False,
                    applicability_reason="Cross-source provenance or comparison inputs are incomplete.",
                    status="ABSTAIN",
                    evidence_class="E0",
                    claim="Cross-source comparison was not executed.",
                    source_locator=locator,
                    evidence={"missing_requirements": missing, "source_doi": source_doi},
                    reproducible="yes",
                    benign_explanations=[],
                    dependency_group=f"cross-source:{source_doi or locator}",
                    next_action="Verify both source locations and contemporaneous availability.",
                    misconduct_inference=False,
                ))
                continue

            mismatches = []
            matches = []
            absent_fields = []
            for field_name in compare_fields:
                if field_name not in target_fields or field_name not in source_fields:
                    absent_fields.append(str(field_name))
                    continue
                kind = str(field_types.get(field_name, "auto"))
                left, right = target_fields[field_name], source_fields[field_name]
                if _field_values_equal(left, right, kind):
                    matches.append(str(field_name))
                else:
                    mismatches.append({
                        "field": str(field_name),
                        "target_value": left,
                        "source_value": right,
                        "field_type": kind,
                    })

            if absent_fields:
                findings.append(Finding(
                    detector_id=self.detector_id,
                    detector_version=self.detector_version,
                    family=self.family,
                    applicable=False,
                    applicability_reason="One or more requested comparison fields are absent.",
                    status="ABSTAIN",
                    evidence_class="E0",
                    claim="Cross-source comparison could not be completed for all prespecified fields.",
                    source_locator=locator,
                    evidence={
                        "missing_fields": absent_fields,
                        "matched_fields": matches,
                        "mismatches_observed_before_abstention": mismatches,
                        "target_source_locator": target_locator,
                        "comparison_source_locator": comparison_locator,
                        "source_doi": source_doi,
                    },
                    reproducible="yes",
                    benign_explanations=[],
                    dependency_group=f"cross-source:{source_doi or locator}",
                    next_action="Re-extract and verify every prespecified field from both sources.",
                    misconduct_inference=False,
                ))
                continue

            ok = not mismatches
            findings.append(Finding(
                detector_id=self.detector_id,
                detector_version=self.detector_version,
                family=self.family,
                applicable=True,
                applicability_reason="Both source locations and all prespecified fields were verified and contemporaneously available.",
                status="PASS" if ok else "FLAG",
                evidence_class="E2",
                claim=(
                    "Target-paper summary agrees with the contemporaneously available cited source on all prespecified fields."
                    if ok else
                    "Target-paper summary disagrees with the contemporaneously available cited source on one or more prespecified fields."
                ),
                source_locator=target_locator,
                evidence={
                    "source_doi": source_doi,
                    "target_source_locator": target_locator,
                    "comparison_source_locator": comparison_locator,
                    "matched_fields": matches,
                    "mismatches": mismatches,
                    "target_fields": target_fields,
                    "source_fields": source_fields,
                },
                reproducible="yes",
                benign_explanations=[] if ok else [
                    "The target table may summarize a different analysis, subsample, or model than the cited source.",
                    "The target table may contain a transcription or summarization error.",
                    "One structured extraction may still require rechecking.",
                ],
                dependency_group=f"cross-source:{source_doi or locator}",
                next_action=None if ok else "Open both source locations and adjudicate each mismatched field.",
                misconduct_inference=False,
            ))
        return findings


def _normalize_category(value: Any) -> str:
    """Minimal deterministic normalization for explicit categorical aliases."""
    text = unicodedata.normalize("NFKD", str(value or ""))
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return re.sub(r"\s+", " ", text).strip().casefold()


class CategoricalAggregateRecomputeDetector:
    """Recompute a reported category count/proportion from deposited raw-data counts.

    The adapter consumes a complete source-verified frequency table rather than
    participant-level rows. Alias rules are explicit and deterministic.
    """

    detector_id = "categorical_aggregate_recompute"
    detector_version = "pilot3b-0.1.0"
    family = "table_consistency"

    def applicability(self, context: ForensicContext) -> Applicability:
        records = context.content.get("categorical_aggregate_checks") or []
        if not records:
            return Applicability(False, "No categorical aggregate recomputation records were supplied.")
        return Applicability(True, "At least one source-verified categorical aggregate record is available.")

    def run(self, context: ForensicContext) -> Sequence[Finding]:
        findings: List[Finding] = []
        for i, record in enumerate(context.content.get("categorical_aggregate_checks") or []):
            locator = str(record.get("source_locator") or f"categorical_aggregate_checks[{i}]")
            target_locator = str(record.get("target_source_locator") or locator)
            data_locator = str(record.get("comparison_source_locator") or "")
            raw_counts = record.get("raw_value_counts")
            aliases = record.get("aliases")
            missing = []

            if not target_locator:
                missing.append("target_source_locator")
            if not data_locator:
                missing.append("comparison_source_locator")
            if not isinstance(raw_counts, dict) or not raw_counts:
                missing.append("raw_value_counts")
            if not isinstance(aliases, list) or not aliases:
                missing.append("aliases")
            if record.get("raw_value_counts_complete") is not True:
                missing.append("raw_value_counts_complete=true")
            if record.get("source_available_at_target_time") is not True:
                missing.append("source_available_at_target_time=true")
            if record.get("provenance_verified") is not True:
                missing.append("provenance_verified=true")
            if record.get("sample_size") is None:
                missing.append("sample_size")
            if record.get("reported_count") is None and record.get("reported_percent") is None:
                missing.append("reported_count or reported_percent")
            digest = str(record.get("data_sha256") or "").strip().lower()
            if not re.fullmatch(r"[0-9a-f]{64}", digest):
                missing.append("valid data_sha256")
            if not str(record.get("data_created_at") or "").strip():
                missing.append("data_created_at")

            if missing:
                findings.append(Finding(
                    detector_id=self.detector_id,
                    detector_version=self.detector_version,
                    family=self.family,
                    applicable=False,
                    applicability_reason="Raw-data aggregate provenance or required inputs are incomplete.",
                    status="ABSTAIN",
                    evidence_class="E0",
                    claim="Categorical aggregate recomputation was not executed.",
                    source_locator=locator,
                    evidence={"missing_requirements": missing},
                    reproducible="yes",
                    benign_explanations=[],
                    dependency_group=f"rawdata:{digest or locator}",
                    next_action="Verify the complete source frequency table, digest, dates, alias rule, and target table location.",
                    misconduct_inference=False,
                ))
                continue

            try:
                n = int(record["sample_size"])
                if n <= 0:
                    raise ValueError("sample_size must be positive")

                parsed_counts: Dict[str, int] = {}
                for raw_value, raw_count in raw_counts.items():
                    count = int(raw_count)
                    if count < 0:
                        raise ValueError("raw category counts cannot be negative")
                    parsed_counts[str(raw_value)] = count

                source_total = sum(parsed_counts.values())
                if source_total != n:
                    raise ValueError(
                        f"complete raw_value_counts sum to {source_total}, expected sample_size {n}"
                    )

                alias_set = {_normalize_category(x) for x in aliases}
                matched_variants = [
                    {"value": raw_value, "count": count}
                    for raw_value, count in sorted(parsed_counts.items())
                    if _normalize_category(raw_value) in alias_set
                ]
                recomputed_count = sum(item["count"] for item in matched_variants)
                recomputed_percent = (100.0 * recomputed_count) / n

                checks: Dict[str, bool] = {}
                if record.get("reported_count") is not None:
                    checks["count"] = int(record["reported_count"]) == recomputed_count
                if record.get("reported_percent") is not None:
                    checks["percent"] = _rounded_equal(
                        recomputed_percent, str(record["reported_percent"])
                    )

                ok = all(checks.values())
                reported_percent = record.get("reported_percent")
                rounded_percent = None
                if reported_percent is not None:
                    rounded_percent = str(
                        _round_half_up(
                            recomputed_percent,
                            _decimal_places(str(reported_percent)),
                        )
                    )

                findings.append(Finding(
                    detector_id=self.detector_id,
                    detector_version=self.detector_version,
                    family=self.family,
                    applicable=True,
                    applicability_reason="Complete source frequency counts, explicit aliases, time-safe provenance, and target values were supplied.",
                    status="PASS" if ok else "FLAG",
                    evidence_class="E1",
                    claim=(
                        "Reported category aggregate is compatible with deterministic recomputation from the deposited source data."
                        if ok else
                        "Reported category aggregate is incompatible with deterministic recomputation from the deposited source data under the explicit alias rule."
                    ),
                    source_locator=target_locator,
                    evidence={
                        "category_label": record.get("category_label"),
                        "aliases": list(aliases),
                        "normalization": "NFKD strip-diacritics + whitespace-collapse + casefold",
                        "sample_size": n,
                        "source_total": source_total,
                        "matched_variants": matched_variants,
                        "recomputed_count": recomputed_count,
                        "recomputed_percent": recomputed_percent,
                        "recomputed_percent_rounded": rounded_percent,
                        "reported_count": record.get("reported_count"),
                        "reported_percent": reported_percent,
                        "checks": checks,
                        "data_sha256": digest,
                        "data_created_at": record.get("data_created_at"),
                        "comparison_source_locator": data_locator,
                    },
                    reproducible="yes",
                    benign_explanations=[] if ok else [
                        "The published table may have applied an undocumented recoding or exclusion rule.",
                        "The deposited data may represent a different analysis snapshot or subset despite the recorded provenance.",
                        "The target table or deposited source values may contain a transcription/reporting error.",
                    ],
                    dependency_group=f"rawdata:{digest}",
                    next_action=None if ok else "Re-run the prespecified category normalization directly on the deposited data and compare with the historical table.",
                    misconduct_inference=False,
                ))
            except (TypeError, ValueError, ArithmeticError) as exc:
                findings.append(Finding(
                    detector_id=self.detector_id,
                    detector_version=self.detector_version,
                    family=self.family,
                    applicable=False,
                    applicability_reason=f"Categorical aggregate inputs failed validation: {exc}",
                    status="ABSTAIN",
                    evidence_class="E0",
                    claim="Categorical aggregate recomputation could not be validly completed.",
                    source_locator=locator,
                    evidence={"record": dict(record)},
                    reproducible="yes",
                    benign_explanations=[],
                    dependency_group=f"rawdata:{digest or locator}",
                    next_action="Repair the structured aggregate record and verify completeness against the deposited data.",
                    misconduct_inference=False,
                ))
        return findings


def _normalize_scope_label(value: Any) -> str:
    return re.sub(r"\s+", "_", str(value or "").strip().casefold())


class CrossSectionScopeCoherenceDetector:
    """Check whether a table caption covers analysis scope explicitly attributed to it.

    The detector consumes source-verified canonical scope labels rather than
    inferring scientific semantics itself. It is intended for contradictions
    within the same time-safe historical artifact.
    """

    detector_id = "cross_section_scope_coherence"
    detector_version = "pilot3c-0.1.0"
    family = "methods_results_coherence"

    def applicability(self, context: ForensicContext) -> Applicability:
        records = context.content.get("cross_section_scope_checks") or []
        if not records:
            return Applicability(False, "No cross-section scope checks were supplied.")
        return Applicability(True, "At least one source-verified body-to-caption scope check is available.")

    def run(self, context: ForensicContext) -> Sequence[Finding]:
        findings: List[Finding] = []
        for i, record in enumerate(context.content.get("cross_section_scope_checks") or []):
            locator = str(record.get("source_locator") or f"cross_section_scope_checks[{i}]")
            body_locator = str(record.get("body_source_locator") or "")
            caption_locator = str(record.get("caption_source_locator") or "")
            body_labels = record.get("body_scope_labels")
            caption_labels = record.get("caption_scope_labels")
            missing_requirements: List[str] = []

            if not body_locator:
                missing_requirements.append("body_source_locator")
            if not caption_locator:
                missing_requirements.append("caption_source_locator")
            if not isinstance(body_labels, list) or not body_labels:
                missing_requirements.append("body_scope_labels")
            if not isinstance(caption_labels, list) or not caption_labels:
                missing_requirements.append("caption_scope_labels")
            if record.get("body_points_to_target") is not True:
                missing_requirements.append("body_points_to_target=true")
            if record.get("same_historical_artifact") is not True:
                missing_requirements.append("same_historical_artifact=true")
            if record.get("labels_source_verified") is not True:
                missing_requirements.append("labels_source_verified=true")
            if record.get("provenance_verified") is not True:
                missing_requirements.append("provenance_verified=true")

            if missing_requirements:
                findings.append(Finding(
                    detector_id=self.detector_id,
                    detector_version=self.detector_version,
                    family=self.family,
                    applicable=False,
                    applicability_reason="Cross-section scope evidence is incomplete or not source-verified.",
                    status="ABSTAIN",
                    evidence_class="E0",
                    claim="Body-to-caption scope coherence was not evaluated.",
                    source_locator=locator,
                    evidence={"missing_requirements": missing_requirements},
                    reproducible="yes",
                    benign_explanations=[],
                    dependency_group=f"scope:{locator}",
                    next_action="Verify the body/table link, both source locations, and canonical scope labels from the same historical artifact.",
                    misconduct_inference=False,
                ))
                continue

            body_set = {_normalize_scope_label(x) for x in body_labels}
            caption_set = {_normalize_scope_label(x) for x in caption_labels}
            missing_scope = sorted(body_set - caption_set)
            ok = not missing_scope

            findings.append(Finding(
                detector_id=self.detector_id,
                detector_version=self.detector_version,
                family=self.family,
                applicable=True,
                applicability_reason="The body explicitly points to the target table and both scope labels were source-verified within the same historical artifact.",
                status="PASS" if ok else "FLAG",
                evidence_class="E1",
                claim=(
                    "The target caption covers all source-verified analysis scopes that the body explicitly attributes to the table."
                    if ok else
                    "The body explicitly attributes an analysis scope to the table that is not represented in the historical table caption."
                ),
                source_locator=caption_locator,
                evidence={
                    "body_source_locator": body_locator,
                    "caption_source_locator": caption_locator,
                    "body_scope_labels": sorted(body_set),
                    "caption_scope_labels": sorted(caption_set),
                    "missing_scope_labels": missing_scope,
                    "body_excerpt": record.get("body_excerpt"),
                    "caption_excerpt": record.get("caption_excerpt"),
                },
                reproducible="yes",
                benign_explanations=[] if ok else [
                    "The body-to-table citation may itself be wrong.",
                    "The caption may intentionally describe only one panel of a multi-panel table.",
                    "The canonical scope labels may have been extracted or adjudicated incorrectly.",
                    "The discrepancy may be a caption or layout error rather than an analysis error.",
                ],
                dependency_group=f"scope:{locator}",
                next_action=None if ok else "Inspect the historical body citation and table caption together, then verify whether the table contains the omitted analysis scope.",
                misconduct_inference=False,
            ))
        return findings


DEFAULT_DETERMINISTIC_DETECTORS = [
    NHSTConsistencyDetector(),
    GRIMItemMeanDetector(),
    DebitStyleBinaryDetector(),
    TableArithmeticDetector(),
    ReferenceMetadataDetector(),
    CrossSourceFieldConsistencyDetector(),
    CategoricalAggregateRecomputeDetector(),
    CrossSectionScopeCoherenceDetector(),
]
