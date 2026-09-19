"""ARIS4C004 second-review blind evidence packet builder.

Legal inputs only (per process/IDENTITY_SECOND_REVIEW_HANDOFF.md):
  - data/derived/identity_second_review_blind_assignment.csv  (40 frozen cases)
  - data/derived/science_candidates_frozen.csv                (candidate frame metadata)
  - public OpenAlex author records + works
  - public Wikidata entity claims

Deliberately never read here: identity_decisions_100.csv,
identity_second_review_selection.csv, and any exposure/mental-health file.
"""

from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path

import requests


_PAPER_DIR = os.environ.get("ARIS4C_PAPER_DIR")
PAPER = Path(_PAPER_DIR) if _PAPER_DIR else Path(__file__).resolve().parents[2]
DERIVED = PAPER / "data" / "derived"
OUT = Path(__file__).resolve().parent

API = "https://api.openalex.org"
WD = "https://www.wikidata.org/w/api.php"
KEY = os.getenv("OPENALEX_API_KEY")
UA = {"User-Agent": "ARIS4C004-identity-second-review/1.0 (research retrieval; github.com/CochraneK/ARIS4C)"}

AUTHOR_SELECT = ",".join(
    [
        "id", "display_name", "orcid", "ids", "works_count", "cited_by_count",
        "summary_stats", "last_known_institutions", "topics", "relevance_score",
    ]
)
FORBIDDEN = ("identity_decisions_100.csv", "identity_second_review_selection.csv")


def oa(path: str, params: dict, cache: dict, tries: int = 4):
    params = dict(params)
    if KEY:
        params["api_key"] = KEY
    url = API + path
    cache_key = url + "?" + "&".join(f"{k}={v}" for k, v in sorted(params.items()))
    if cache_key in cache:
        return cache[cache_key]
    for i in range(tries):
        try:
            r = requests.get(url, params=params, headers=UA, timeout=60)
            if r.status_code == 200:
                cache[cache_key] = r.json()
                time.sleep(0.15)
                return cache[cache_key]
            if r.status_code == 404:
                cache[cache_key] = None
                return None
            err = f"{r.status_code} {r.text[:160]}"
            if r.status_code not in (429, 500, 502, 503, 504):
                raise RuntimeError(f"openalex rejected {url}: {err}")
            time.sleep(2 ** i * 3)
        except RuntimeError:
            raise
        except Exception as e:  # noqa: BLE001
            err = f"{type(e).__name__} {e}"
            time.sleep(2 ** i * 3)
    raise RuntimeError(f"openalex failed: {url} ({err})")


def local_name(a_id: str) -> str:
    return (a_id or "").rsplit("/", 1)[-1]


def author_profile(a_id: str, cache: dict) -> dict | None:
    raw = oa(f"/authors/{local_name(a_id)}", {"select": AUTHOR_SELECT}, cache)
    if not raw:
        return None
    return summarize_author(raw, cache)


def summarize_author(raw: dict, cache: dict) -> dict:
    affs = [
        {"institution": (a.get("institution") or {}).get("display_name"),
         "country": a.get("country_code")}
        for a in (raw.get("last_known_institutions") or [])[:3]
    ]
    topics = [
        {"name": t.get("display_name"), "score": round(t.get("score", 0), 3)}
        for t in (raw.get("topics") or [])[:3]
    ]
    return {
        "author_id": local_name(raw.get("id", "")),
        "display_name": raw.get("display_name"),
        "orcid": raw.get("orcid"),
        "ids": {k: v for k, v in (raw.get("ids") or {}).items()},
        "works_count": raw.get("works_count"),
        "cited_by_count": raw.get("cited_by_count"),
        "h_index": (raw.get("summary_stats") or {}).get("h_index"),
        "relevance_score": raw.get("relevance_score"),
        "affiliations": affs,
        "topics": topics,
        "sample_works": works_for(raw.get("id", ""), cache),
    }


def works_for(author_uri: str, cache: dict, n: int = 6) -> list[dict]:
    name = local_name(author_uri)
    raw = oa(
        "/works",
        {
            "filter": f"author.id:{name}",
            "sort": "cited_by_count:desc",
            "per-page": n,
            "select": "id,title,publication_year,doi,cited_by_count,authorships",
        },
        cache,
    )
    out = []
    for w in (raw or {}).get("results", []):
        authors = [
            (a.get("author") or {}).get("display_name")
            for a in (w.get("authorships") or [])[:6]
        ]
        out.append({
            "title": w.get("title"),
            "year": w.get("publication_year"),
            "doi": (w.get("doi") or "").replace("https://doi.org/", ""),
            "cited_by": w.get("cited_by_count"),
            "authors": authors,
        })
    return out


def wikidata(qid: str, cache: dict) -> dict:
    url = WD + "?" + qid
    if url in cache:
        return cache[url]
    for attempt in range(6):
        try:
            return _wikidata_fetch(qid, url, cache)
        except requests.HTTPError as e:
            if e.response is not None and e.response.status_code not in (429, 500, 502, 503, 504):
                raise
            time.sleep(8 + attempt * 6)
    raise RuntimeError(f"wikidata unavailable for {qid}")


def _wikidata_fetch(qid: str, url: str, cache: dict) -> dict:
    r = requests.get(
        WD,
        params={
            "action": "wbgetentities", "ids": qid, "props": "claims|labels|descriptions|sitelinks",
            "format": "json",
        },
        headers=UA,
        timeout=60,
    )
    r.raise_for_status()
    ent = (r.json().get("entities") or {}).get(qid, {})

    def vals(pid):
        out = []
        for c in (ent.get("claims") or {}).get(pid, []):
            dv = ((c.get("mainsnak") or {}).get("datavalue") or {}).get("value")
            if isinstance(dv, dict):
                if dv.get("id"):
                    out.append(dv["id"])
                elif dv.get("time"):
                    out.append(dv["time"][:11])
                elif dv.get("text"):
                    out.append(dv["text"])
            elif dv is not None:
                out.append(str(dv))
        return out

    res = {
        "qid": qid,
        "label": (ent.get("labels") or {}).get("en", {}).get("value"),
        "description": (ent.get("descriptions") or {}).get("en", {}).get("value"),
        "place_of_birth": vals("P19"),
        "occupations": vals("P106"),
        "field_of_work": vals("P101"),
        "employer": vals("P108"),
        "educated_at": vals("P69"),
        "notable_work": vals("P800"),
        "openalex_id": vals("P10289"),
        "viaf": vals("P214"),
        "isni": vals("P213"),
        "lcnaf": vals("P244"),
        "wiki_en": (ent.get("sitelinks") or {}).get("enwiki", {}).get("title"),
    }
    res["_qids"] = sorted({q for v in QID_FIELDS for q in (res.get(v) or []) if q.startswith("Q")})
    cache[url] = res
    time.sleep(0.15)
    return res


QID_FIELDS = ["place_of_birth", "occupations", "field_of_work", "employer", "educated_at", "notable_work"]


def resolve_labels(qids: list[str], cache: dict) -> dict:
    todo = [q for q in qids if q not in cache]
    for i in range(0, len(todo), 40):
        r = requests.get(
            WD,
            params={"action": "wbgetentities", "ids": "|".join(todo[i : i + 40]),
                    "props": "labels", "format": "json"},
            headers=UA, timeout=60,
        )
        r.raise_for_status()
        for qid, ent in (r.json().get("entities") or {}).items():
            cache[qid] = (ent.get("labels") or {}).get("en", {}).get("value") or qid
        time.sleep(0.15)
    return {q: cache.get(q, q) for q in qids}


def build(max_cases: int, out_path: Path) -> None:
    import csv

    with (DERIVED / "identity_second_review_blind_assignment.csv").open(
        encoding="utf-8-sig", newline=""
    ) as fh:
        cases = list(csv.DictReader(fh))
    with (DERIVED / "science_candidates_frozen.csv").open(encoding="utf-8-sig", newline="") as fh:
        frame = {r["person_id"]: r for r in csv.DictReader(fh)}
    guard = " ".join(cases[0]).lower()
    assert "identity_decisions" not in guard and "first_review_status" not in guard

    cache: dict = {}
    labels: dict = {}
    packets: list = []
    if out_path.exists():
        packets = [json.loads(l) for l in out_path.read_text(encoding="utf-8").splitlines() if l.strip()]
        have = {p["person_id"] for p in packets}
        cases = [c for c in cases if c["person_id"] not in have]
        print(f"resuming with {len(packets)} packets already built", flush=True)
    for case in cases[:max_cases]:
        pid = case["person_id"]
        fr = frame.get(pid, {})
        name = case["canonical_name"]
        search = oa(
            "/authors",
            {
                "search": name,
                "per-page": 8,
                "select": AUTHOR_SELECT,
            },
            cache,
        )
        hits = []
        for raw in (search or {}).get("results", []):
            hits.append(summarize_author(raw, cache))
        seen = {h["author_id"] for h in hits}
        frame_author = None
        if fr.get("openalex_author_id"):
            aid = local_name(fr["openalex_author_id"])
            if aid not in seen:
                frame_author = author_profile(fr["openalex_author_id"], cache)
        wd_res = wikidata(fr["wikidata_qid"], cache) if fr.get("wikidata_qid") else None
        if wd_res:
            names = resolve_labels(wd_res.get("_qids") or [], labels)
            for field in QID_FIELDS:
                wd_res[field] = [names.get(q, q) for q in wd_res.get(field) or []]
            wd_res["openalex_id"] = local_name(wd_res.get("openalex_id") or "")
            wd_res.pop("_qids", None)
        packet = {
            "person_id": pid,
            "canonical_name": name,
            "birth_year": case["birth_year"],
            "death_year": case["death_year"],
            "frame_wikidata_qid": fr.get("wikidata_qid"),
            "frame_orcid": fr.get("orcid"),
            "frame_openalex_author_id": local_name(fr.get("openalex_author_id", "")),
            "frame_occupation": [fr.get("level1_main_occ"), fr.get("level2_main_occ"), fr.get("level3_main_occ")],
            "frame_region": fr.get("region"),
            "wikidata": wd_res,
            "openalex_search_candidates": hits,
            "frame_author_profile": frame_author,
        }
        packets.append(packet)
        with out_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(packet, ensure_ascii=False) + chr(10))
        print(
            f"{pid} {name.encode('ascii', 'replace').decode()}: {len(hits)} hits "
            f"+ frame_author={'y' if frame_author else 'n'}",
            flush=True,
        )
    out_path.write_text(
        "\n".join(json.dumps(p, ensure_ascii=False) for p in packets) + "\n", encoding="utf-8"
    )
    print(f"wrote {len(packets)} packets -> {out_path}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-cases", type=int, default=40)
    ap.add_argument("--output", type=Path, default=OUT / "second_review_evidence_packet.jsonl")
    a = ap.parse_args()
    build(a.max_cases, a.output)
