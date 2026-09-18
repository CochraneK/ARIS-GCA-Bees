"""Schema-tolerant local SciSciNet-v2 adapter for ARIS4C015.

SciSciNet-v2 is large enough that ARIS4C015 should not assume a full local
download. This module deliberately works on *local slices* exported from
Parquet/BigQuery/GCS and accepts configurable column mappings.

The adapter does not hard-code undocumented v2 column names. A caller provides
or infers the minimal fields needed for a pilot:
- paper identifier
- paper publication year
- citing paper identifier
- cited paper identifier

Historical reconstruction is cutoff-safe: when end_year is supplied, citation
edges whose citing paper was published after that year are excluded before
building the annual trajectory.

Parquet support is optional and loaded lazily through pandas.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Iterator, Mapping

from citation_history import CitationHistory, citation_history_from_citing_years


@dataclass(frozen=True)
class ColumnMap:
    paper_id: str = "paper_id"
    paper_year: str = "publication_year"
    citing_id: str = "citing_paper_id"
    cited_id: str = "cited_paper_id"


@dataclass(frozen=True)
class PaperRecord:
    paper_id: str
    publication_year: int


def _rows(path: str | Path) -> Iterator[Mapping[str, Any]]:
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix in {".csv", ".tsv"}:
        delimiter = "\t" if suffix == ".tsv" else ","
        with path.open("r", encoding="utf-8", newline="") as handle:
            yield from csv.DictReader(handle, delimiter=delimiter)
        return

    if suffix in {".parquet", ".pq"}:
        try:
            import pandas as pd  # type: ignore
        except ImportError as exc:
            raise RuntimeError(
                "Parquet input requires pandas plus a parquet engine "
                "(pyarrow or fastparquet). CSV/TSV needs no extra dependency."
            ) from exc
        frame = pd.read_parquet(path)
        for row in frame.to_dict(orient="records"):
            yield row
        return

    raise ValueError(f"Unsupported table format: {path.suffix}")


def _require_columns(
    row: Mapping[str, Any],
    columns: Iterable[str],
    *,
    table_name: str,
) -> None:
    missing = [name for name in columns if name not in row]
    if missing:
        raise KeyError(f"{table_name} missing required columns: {missing}")


def load_paper_years(
    paper_table: str | Path,
    *,
    columns: ColumnMap = ColumnMap(),
) -> dict[str, int]:
    """Load {paper_id: publication_year} from a local SciSciNet slice."""
    result: dict[str, int] = {}
    first = True
    for row in _rows(paper_table):
        if first:
            _require_columns(
                row,
                [columns.paper_id, columns.paper_year],
                table_name="paper_table",
            )
            first = False
        paper_id = str(row[columns.paper_id])
        year_raw = row[columns.paper_year]
        if year_raw in (None, ""):
            continue
        result[paper_id] = int(year_raw)
    return result


def iter_citation_edges(
    citation_table: str | Path,
    *,
    columns: ColumnMap = ColumnMap(),
) -> Iterator[tuple[str, str]]:
    """Yield (citing_id, cited_id) citation edges."""
    first = True
    for row in _rows(citation_table):
        if first:
            _require_columns(
                row,
                [columns.citing_id, columns.cited_id],
                table_name="citation_table",
            )
            first = False
        citing = row[columns.citing_id]
        cited = row[columns.cited_id]
        if citing in (None, "") or cited in (None, ""):
            continue
        yield str(citing), str(cited)


def _visible_citing_year(
    citing_id: str,
    *,
    paper_years: Mapping[str, int],
    end_year: int | None,
) -> int | None:
    """Return citing year if known and visible at the historical cutoff."""
    year = paper_years.get(citing_id)
    if year is None:
        return None
    year = int(year)
    if end_year is not None and year > int(end_year):
        return None
    return year


def reconstruct_target_history(
    target_paper_id: str,
    *,
    paper_years: Mapping[str, int],
    citation_edges: Iterable[tuple[str, str]],
    end_year: int | None = None,
) -> CitationHistory:
    """Reconstruct one target paper's annual citations from a local slice.

    When end_year is supplied, future citing works are excluded before history
    construction. Pre-publication edges remain visible to the generic history
    validator so metadata anomalies are counted rather than silently erased.
    """
    if target_paper_id not in paper_years:
        raise KeyError(f"Missing target publication year: {target_paper_id}")

    citing_years: list[int] = []
    for citing_id, cited_id in citation_edges:
        if cited_id != target_paper_id:
            continue
        year = _visible_citing_year(
            citing_id,
            paper_years=paper_years,
            end_year=end_year,
        )
        if year is not None:
            citing_years.append(year)

    return citation_history_from_citing_years(
        int(paper_years[target_paper_id]),
        citing_years,
        end_year=end_year,
        strict=False,
    )


def cohort_histories(
    target_ids: Iterable[str],
    *,
    paper_years: Mapping[str, int],
    citation_edges: Iterable[tuple[str, str]],
    end_year: int | None = None,
) -> dict[str, CitationHistory]:
    """Reconstruct histories for multiple targets in one pass over edges.

    The same historical cutoff is applied to all citing works in the cohort.
    """
    targets = set(target_ids)
    missing_targets = sorted(targets.difference(paper_years))
    if missing_targets:
        raise KeyError(
            "Missing target publication years: "
            + ", ".join(missing_targets[:10])
        )

    years_by_target: dict[str, list[int]] = {pid: [] for pid in targets}
    for citing_id, cited_id in citation_edges:
        if cited_id not in targets:
            continue
        citing_year = _visible_citing_year(
            citing_id,
            paper_years=paper_years,
            end_year=end_year,
        )
        if citing_year is not None:
            years_by_target[cited_id].append(citing_year)

    return {
        target: citation_history_from_citing_years(
            int(paper_years[target]),
            years_by_target[target],
            end_year=end_year,
            strict=False,
        )
        for target in targets
    }
