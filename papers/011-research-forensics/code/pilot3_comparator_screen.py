#!/usr/bin/env python3
"""Secondary negative-screen for ARIS4C011 development comparators.

Inputs are provisional same-journal/date candidates. A candidate advances only
when:
1) Crossref returns zero works that update the candidate DOI; and
2) PubMed resolves exactly one record for the DOI and that original record has
   no correction/retraction/expression-of-concern/update relationship.

Passing this screen still does NOT prove absence of errors or concerns. The
paper remains artifact-qualification pending and cannot be called "clean".
"""

from __future__ import annotations

import argparse
import json
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

USER_AGENT = "ARIS4C011-comparator-screen/0.1 (https://github.com/CochraneK/ARIS4C)"

NOTICE_REF_TYPES = {
    "ErratumIn",
    "ExpressionOfConcernIn",
    "RetractionIn",
    "UpdateIn",
    "CorrectedandRepublishedIn",
    "RetractedandRepublishedIn",
}
NOTICE_PUBLICATION_TYPES = {
    "Retracted Publication",
}


def request_bytes(url: str, *, attempts: int = 4) -> bytes:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "*/*",
        },
    )
    last: Exception | None = None
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                return response.read()
        except Exception as exc:
            last = exc
            if attempt + 1 >= attempts:
                raise
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(last)


def get_json(url: str) -> dict[str, Any]:
    return json.loads(request_bytes(url).decode("utf-8"))


def crossref_updates(doi: str) -> dict[str, Any]:
    params = urllib.parse.urlencode(
        {
            "filter": f"updates:{doi}",
            "rows": "20",
        }
    )
    url = f"https://api.crossref.org/works?{params}"
    payload = get_json(url)
    message = payload.get("message") or {}
    total = int(message.get("total-results") or 0)
    items = message.get("items") or []
    return {
        "query": "Crossref works filter=updates:<candidate_doi>",
        "total_results": total,
        "update_records": [
            {
                "doi": str(item.get("DOI") or "").lower(),
                "title": (
                    str((item.get("title") or [""])[0])
                    if isinstance(item.get("title"), list)
                    else str(item.get("title") or "")
                ),
                "update_to": item.get("update-to") or [],
            }
            for item in items
        ],
    }


def pubmed_ids_for_doi(doi: str) -> list[str]:
    term = f'"{doi}"[AID]'
    params = urllib.parse.urlencode(
        {
            "db": "pubmed",
            "term": term,
            "retmode": "json",
            "retmax": "5",
            "tool": "aris4c011",
        }
    )
    payload = get_json(
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?"
        + params
    )
    return [
        str(x)
        for x in ((payload.get("esearchresult") or {}).get("idlist") or [])
    ]


def pubmed_notice_relations(pmid: str) -> dict[str, Any]:
    params = urllib.parse.urlencode(
        {
            "db": "pubmed",
            "id": pmid,
            "retmode": "xml",
            "tool": "aris4c011",
        }
    )
    raw = request_bytes(
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?"
        + params
    )
    root = ET.fromstring(raw)

    relations = []
    for node in root.findall(".//CommentsCorrections"):
        ref_type = str(node.attrib.get("RefType") or "")
        relations.append(
            {
                "ref_type": ref_type,
                "ref_source": (node.findtext("RefSource") or "").strip(),
                "linked_pmid": (node.findtext("PMID") or "").strip(),
            }
        )

    publication_types = sorted(
        {
            (node.text or "").strip()
            for node in root.findall(".//PublicationType")
            if (node.text or "").strip()
        }
    )
    notice_relations = [
        row for row in relations if row["ref_type"] in NOTICE_REF_TYPES
    ]
    notice_pubtypes = [
        x for x in publication_types if x in NOTICE_PUBLICATION_TYPES
    ]
    return {
        "pmid": pmid,
        "comments_corrections": relations,
        "notice_relations": notice_relations,
        "publication_types": publication_types,
        "notice_publication_types": notice_pubtypes,
    }


def screen_candidate(row: dict[str, Any]) -> dict[str, Any]:
    doi = str(row["candidate_doi"]).lower()
    cr = crossref_updates(doi)
    time.sleep(0.36)
    pmids = pubmed_ids_for_doi(doi)
    time.sleep(0.36)

    pm = None
    if len(pmids) == 1:
        pm = pubmed_notice_relations(pmids[0])
        time.sleep(0.36)

    crossref_negative = cr["total_results"] == 0
    pubmed_resolved = len(pmids) == 1
    pubmed_negative = (
        pm is not None
        and len(pm["notice_relations"]) == 0
        and len(pm["notice_publication_types"]) == 0
    )
    passed = crossref_negative and pubmed_resolved and pubmed_negative

    return {
        **row,
        "crossref_update_screen": cr,
        "pubmed_exact_doi_pmids": pmids,
        "pubmed_notice_screen": pm,
        "crossref_notice_negative": crossref_negative,
        "pubmed_resolved_exactly_once": pubmed_resolved,
        "pubmed_notice_negative": pubmed_negative,
        "notice_negative_screen_pass": passed,
        "screen_state": (
            "NOTICE_NEGATIVE_SCREEN_PASS_ARTIFACT_PENDING"
            if passed
            else "NOTICE_SCREEN_UNRESOLVED_OR_POSITIVE"
        ),
    }


def screen(payload: dict[str, Any]) -> dict[str, Any]:
    if payload.get("secondary_screen_required") is not True:
        raise ValueError("Input is not a provisional comparator candidate set")

    screened = [screen_candidate(row) for row in payload.get("matches", [])]

    selected = []
    target_ids = [str(x["target_id"]) for x in payload.get("targets", [])]
    for target_id in target_ids:
        eligible = [
            x for x in screened
            if x["target_id"] == target_id
            and x["notice_negative_screen_pass"] is True
        ]
        eligible.sort(
            key=lambda x: (
                int(x["match_rank"]),
                int(x["date_distance_days"]),
                str(x["candidate_doi"]),
            )
        )
        if eligible:
            selected.append(
                {
                    **eligible[0],
                    "development_comparator_role": (
                        "NO_KNOWN_INTEGRITY_CONCERN_COMPARATOR"
                    ),
                    "artifact_qualification_required": True,
                }
            )

    return {
        "analysis": "ARIS4C011 comparator secondary notice screen",
        "claim_boundary": (
            "A negative Crossref/PubMed notice screen means no indexed "
            "correction/retraction/expression-of-concern/update was found in "
            "these sources at retrieval time. It does not prove that the "
            "article is error-free or free of integrity concerns and does not "
            "support a specificity estimate."
        ),
        "notice_ref_types_checked": sorted(NOTICE_REF_TYPES),
        "notice_publication_types_checked": sorted(NOTICE_PUBLICATION_TYPES),
        "input_candidate_count": len(screened),
        "screen_pass_count": sum(
            1 for x in screened if x["notice_negative_screen_pass"]
        ),
        "selected_count": len(selected),
        "selected_target_ids": [x["target_id"] for x in selected],
        "artifact_qualification_required": True,
        "screened_candidates": screened,
        "selected_development_comparators": selected,
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()

    payload = json.loads(args.input.read_text(encoding="utf-8"))
    result = screen(payload)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "input_candidate_count": result["input_candidate_count"],
                "screen_pass_count": result["screen_pass_count"],
                "selected_count": result["selected_count"],
                "selected_target_ids": result["selected_target_ids"],
                "artifact_qualification_required": True,
            },
            indent=2,
        )
    )

    expected = len(payload.get("targets", []))
    if result["selected_count"] != expected:
        raise SystemExit(
            "Could not select one notice-negative candidate for every target; "
            "retain unresolved screen output and expand candidates."
        )


if __name__ == "__main__":
    main()
