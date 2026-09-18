"""Citation-history reconstruction utilities for ARIS4C015.

The OpenAlex Work counts_by_year field is useful for recent activity but does
not provide a complete decades-long citation history. Historical Sleeping
Beauty analysis therefore reconstructs annual counts from citation edges and
the publication years of citing works (or uses an equivalent complete source).
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class CitationHistory:
    publication_year: int
    end_year: int
    counts: tuple[int, ...]
    valid_edges: int
    invalid_prepublication_edges: int

    @property
    def total_citations(self) -> int:
        return sum(self.counts)

    def as_dict(self) -> dict:
        return {
            "publication_year": self.publication_year,
            "end_year": self.end_year,
            "counts": list(self.counts),
            "valid_edges": self.valid_edges,
            "invalid_prepublication_edges": self.invalid_prepublication_edges,
            "total_citations": self.total_citations,
        }


def citation_history_from_citing_years(
    publication_year: int,
    citing_years: Iterable[int],
    *,
    end_year: int | None = None,
    strict: bool = False,
) -> CitationHistory:
    """Reconstruct a zero-filled annual citation history.

    Parameters
    ----------
    publication_year:
        Year of the cited paper.
    citing_years:
        Publication years of papers that cite the target paper.
    end_year:
        Optional observation endpoint. If omitted, use the latest valid citing
        year, or publication_year when there are no valid citations.
    strict:
        If True, a citation edge whose citing year predates the cited paper
        raises ValueError. If False, such edges are counted as invalid metadata
        and excluded.

    Returns
    -------
    CitationHistory
        Counts are indexed by paper age: counts[0] corresponds to the
        publication year.
    """
    if publication_year < 0:
        raise ValueError("publication_year must be non-negative")

    years = [int(y) for y in citing_years]
    invalid = [y for y in years if y < publication_year]

    if invalid and strict:
        raise ValueError(
            f"{len(invalid)} citing-year values predate publication_year"
        )

    valid = [y for y in years if y >= publication_year]

    inferred_end = max(valid, default=publication_year)
    if end_year is None:
        resolved_end = inferred_end
    else:
        resolved_end = int(end_year)
        if resolved_end < publication_year:
            raise ValueError("end_year cannot predate publication_year")
        if valid and max(valid) > resolved_end:
            raise ValueError("end_year truncates observed citation edges")

    by_year = Counter(valid)
    counts = tuple(
        by_year.get(year, 0)
        for year in range(publication_year, resolved_end + 1)
    )

    return CitationHistory(
        publication_year=publication_year,
        end_year=resolved_end,
        counts=counts,
        valid_edges=len(valid),
        invalid_prepublication_edges=len(invalid),
    )


def truncate_history(history: CitationHistory, cutoff_year: int) -> CitationHistory:
    """Return the portion of a history visible at or before cutoff_year."""
    if cutoff_year < history.publication_year:
        raise ValueError("cutoff_year cannot predate publication_year")

    resolved_cutoff = min(int(cutoff_year), history.end_year)
    length = resolved_cutoff - history.publication_year + 1
    counts = history.counts[:length]

    return CitationHistory(
        publication_year=history.publication_year,
        end_year=resolved_cutoff,
        counts=counts,
        valid_edges=sum(counts),
        invalid_prepublication_edges=history.invalid_prepublication_edges,
    )
