#!/usr/bin/env python3
"""Freeze full-text provenance for ARIS4C011 development comparators.

This is a development-only negative-side provenance step. Selected papers have
already passed a Crossref + PubMed notice-negative screen. We retrieve the
current PubMed Central JATS article, verify identity, check the retrieved XML
for explicit correction/retraction relations, and record only metadata + hash.

The full text is NOT committed. The resulting record does not prove a paper is
error-free or free of integrity concerns and must not be used to estimate
specificity. It simply freezes what version was evaluated on the negative side
of Pilot 3.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Callable

USER_AGENT = "ARIS4C011-comparator-freeze/0.1 (https://github.com/CochraneK/ARIS4C)"

NOTICE_REL_TYPES = {
    "corrected-article",
    "retracted-article",
    "expression-of-concern",
    "addendum",
    "erratum",
    "correction",
    "retraction",
}


def request_bytes(url: str, *, attempts: int = 4) -> bytes:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": "*/*"},
    )
    last: Exception | None = None
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(req, timeout=45) as response:
                return response.read()
        except Exception as exc:
            last = exc
            if attempt + 1 >= attempts:
                raise
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(last)


def efetch_url(db: str, record_id: str) -> str:
    params = urllib.parse.urlencode(
        {
            "db": db,
            "id": record_id,
            "retmode": "xml",
            "tool": "aris4c011",
        }
    )
    return "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?" + params


def text_content(node: ET.Element | None) -> str:
    if node is None:
        return ""
    return " ".join("".join(node.itertext()).split())


def pubmed_to_pmcid(raw: bytes, *, expected_doi: str) -> str:
    root = ET.fromstring(raw)
    doi = expected_doi.lower()
    main_ids = root.findall(
        ".//PubmedData/ArticleIdList/ArticleId"
    )
    found_dois = {
        (n.text or "").strip().lower()
        for n in main_ids
        if n.attrib.get("IdType") == "doi" and (n.text or "").strip()
    }
    if doi not in found_dois:
        raise ValueError(f"PubMed identity mismatch: expected DOI {doi}")

    pmcids = [
        (n.text or "").strip()
        for n in main_ids
        if n.attrib.get("IdType") == "pmc" and (n.text or "").strip()
    ]
    if len(set(pmcids)) != 1:
        raise ValueError(
            f"Expected exactly one PMCID for {doi}; found {sorted(set(pmcids))}"
        )
    return pmcids[0]


def inspect_pmc_jats(raw: bytes, *, expected_doi: str) -> dict[str, Any]:
    root = ET.fromstring(raw)
    doi = expected_doi.lower()
    article_dois = {
        (n.text or "").strip().lower()
        for n in root.findall(".//article-id[@pub-id-type='doi']")
        if (n.text or "").strip()
    }
    if doi not in article_dois:
        raise ValueError(
            f"PMC JATS identity mismatch: expected DOI {doi}; "
            f"found {sorted(article_dois)}"
        )

    title = text_content(root.find(".//article-title"))
    body = root.find(".//body")
    if body is None or not text_content(body):
        raise ValueError(f"PMC JATS has no non-empty article body for {doi}")

    relation_rows = []
    for node in root.findall(".//related-article"):
        rel_type = str(node.attrib.get("related-article-type") or "").strip()
        relation_rows.append(
            {
                "related_article_type": rel_type,
                "href": str(
                    node.attrib.get("{http://www.w3.org/1999/xlink}href")
                    or node.attrib.get("href")
                    or ""
                ).strip(),
            }
        )
    explicit_notice_relations = [
        r for r in relation_rows
        if r["related_article_type"].lower() in NOTICE_REL_TYPES
    ]

    status_text = " ".join(
        [
            title,
            text_content(root.find(".//article-categories")),
            text_content(root.find(".//custom-meta-group")),
        ]
    ).lower()
    status_marker_terms = [
        term for term in
        ["retracted article", "expression of concern", "correction", "erratum"]
        if term in status_text
    ]

    return {
        "article_title": title,
        "article_dois": sorted(article_dois),
        "article_body_present": True,
        "related_article_rows": relation_rows,
        "explicit_notice_relations": explicit_notice_relations,
        "status_marker_terms": status_marker_terms,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "byte_length": len(raw),
    }


def qualify_selected(
    payload: dict[str, Any],
    *,
    fetcher: Callable[[str], bytes] = request_bytes,
    retrieved_at_utc: str | None = None,
) -> dict[str, Any]:
    selected = payload.get("selected_development_comparators") or []
    if not selected:
        raise ValueError("No selected development comparators to freeze")

    frozen = []
    for row in selected:
        if row.get("notice_negative_screen_pass") is not True:
            raise ValueError("Comparator must pass the notice-negative screen")
        doi = str(row["candidate_doi"]).lower()
        pmid = str((row.get("pubmed_notice_screen") or {}).get("pmid") or "")
        if not pmid:
            raise ValueError(f"Missing PubMed PMID for {doi}")

        pubmed_raw = fetcher(efetch_url("pubmed", pmid))
        pmcid = pubmed_to_pmcid(pubmed_raw, expected_doi=doi)
        time.sleep(0.34)
        pmc_url = efetch_url("pmc", pmcid)
        pmc_raw = fetcher(pmc_url)
        inspected = inspect_pmc_jats(pmc_raw, expected_doi=doi)

        pass_fulltext = (
            inspected["article_body_present"]
            and not inspected["explicit_notice_relations"]
            and not inspected["status_marker_terms"]
        )
        frozen.append(
            {
                "target_id": row["target_id"],
                "target_doi": row["target_doi"],
                "target_published": row["target_published"],
                "candidate_doi": doi,
                "candidate_title_from_screen": row["candidate_title"],
                "candidate_published": row["candidate_published"],
                "date_distance_days": row["date_distance_days"],
                "pubmed_pmid": pmid,
                "pmc_id": pmcid,
                "pmc_jats_source": pmc_url,
                "retrieved_article_title": inspected["article_title"],
                "fulltext_sha256": inspected["sha256"],
                "fulltext_byte_length": inspected["byte_length"],
                "explicit_notice_relations_in_frozen_jats": inspected[
                    "explicit_notice_relations"
                ],
                "status_marker_terms_in_frozen_jats": inspected[
                    "status_marker_terms"
                ],
                "development_fulltext_freeze_pass": pass_fulltext,
                "development_comparator_role": (
                    "NO_KNOWN_INTEGRITY_CONCERN_COMPARATOR"
                ),
                "qualification_state": (
                    "FROZEN_NOTICE_NEGATIVE_FULLTEXT"
                    if pass_fulltext
                    else "FULLTEXT_FREEZE_REVIEW_REQUIRED"
                ),
            }
        )
        time.sleep(0.34)

    timestamp = retrieved_at_utc or (
        dt.datetime.now(dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )
    passed = [x for x in frozen if x["development_fulltext_freeze_pass"]]
    return {
        "analysis": "ARIS4C011 development comparator full-text freeze",
        "retrieved_at_utc": timestamp,
        "input_selected_count": len(selected),
        "frozen_pass_count": len(passed),
        "all_selected_frozen": len(passed) == len(selected),
        "selection_independent_of_detector_output": True,
        "full_text_committed": False,
        "claim_boundary": (
            "These are matched no-known-integrity-concern development "
            "comparators whose notice-negative current full texts were frozen "
            "by cryptographic hash at retrieval. This does not establish that "
            "they are error-free or integrity-concern-free and does not support "
            "specificity, false-positive-rate, or superiority estimates."
        ),
        "confirmatory_eligibility": (
            "DEVELOPMENT_ONLY_UNTIL_BROADER_CORPUS_AND_PROTOCOL_FREEZE"
        ),
        "frozen_comparators": frozen,
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()

    payload = json.loads(args.input.read_text(encoding="utf-8"))
    result = qualify_selected(payload)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "input_selected_count": result["input_selected_count"],
                "frozen_pass_count": result["frozen_pass_count"],
                "all_selected_frozen": result["all_selected_frozen"],
                "confirmatory_eligibility": result["confirmatory_eligibility"],
            },
            indent=2,
        )
    )
    if not result["all_selected_frozen"]:
        raise SystemExit(
            "At least one comparator full-text freeze requires review"
        )


if __name__ == "__main__":
    main()
