"""Core retrospective metrics for ARIS4C015.

This module deliberately contains only transparent citation-trajectory metrics.
Prospective ranking must be implemented separately so that future information
cannot accidentally leak into discovery features.

References
----------
Ke Q, Ferrara E, Radicchi F, Flammini A. Defining and identifying Sleeping
Beauties in science. PNAS. 2015;112(24):7426-7431.
doi:10.1073/pnas.1424329112
"""

from __future__ import annotations

import math
from typing import Iterable, Sequence


def _validate(citations: Iterable[float]) -> list[float]:
    values = [float(x) for x in citations]
    if not values:
        raise ValueError("citations must be non-empty")
    if any((not math.isfinite(x)) or x < 0 for x in values):
        raise ValueError("citations must be finite and non-negative")
    return values


def peak_time(citations: Sequence[float]) -> int:
    """Return t_m, the earliest age with maximum annual citations.

    Ke et al. define t_m as the age at which annual citations are maximal.
    Published definitions do not always specify a tie policy, so ARIS4C015
    uses the earliest maximum and records that convention explicitly.
    """
    values = _validate(citations)
    return max(range(len(values)), key=lambda i: values[i])


def beauty_coefficient(citations: Sequence[float]) -> float:
    """Compute the Ke et al. (2015) Beauty Coefficient B.

    Parameters
    ----------
    citations:
        Annual citation counts ordered by paper age t=0,1,... .

    Returns
    -------
    float
        Beauty Coefficient. Large positive values indicate stronger
        delayed-recognition geometry. This function does not apply any
        threshold that declares a paper to be a Sleeping Beauty.
    """
    c = _validate(citations)
    tm = peak_time(c)

    if tm == 0:
        return 0.0

    c0 = c[0]
    ctm = c[tm]
    total = 0.0

    for t in range(tm + 1):
        reference = ((ctm - c0) / tm) * t + c0
        total += (reference - c[t]) / max(1.0, c[t])

    return total


def awakening_time(citations: Sequence[float]) -> int:
    """Compute the Ke et al. awakening time t_a.

    t_a is the paper age t <= t_m with maximum perpendicular distance
    between (t, c_t) and the line through (0, c_0) and (t_m, c_t_m).

    Ties are resolved in favor of the earliest age.
    """
    c = _validate(citations)
    tm = peak_time(c)

    if tm == 0:
        return 0

    c0 = c[0]
    ctm = c[tm]
    denominator = math.sqrt((ctm - c0) ** 2 + tm**2)

    if denominator == 0:
        return 0

    distances: list[float] = []
    for t in range(tm + 1):
        numerator = abs((ctm - c0) * t - tm * c[t] + tm * c0)
        distances.append(numerator / denominator)

    return max(range(tm + 1), key=lambda t: distances[t])


def retrospective_summary(citations: Sequence[float]) -> dict[str, float | int]:
    """Return transparent retrospective metrics without a class label."""
    c = _validate(citations)
    tm = peak_time(c)
    ta = awakening_time(c)
    return {
        "beauty_coefficient": beauty_coefficient(c),
        "peak_time": tm,
        "awakening_time": ta,
        "sleep_length": ta,
        "peak_citations": c[tm],
        "citations_at_publication_age_0": c[0],
    }
