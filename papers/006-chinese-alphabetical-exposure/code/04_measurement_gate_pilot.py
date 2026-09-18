#!/usr/bin/env python3
"""ARIS4C006 — measurement-gate pilot.

Quantify whether a confirmatory China-affiliated authorship panel can use
OpenAlex for trajectories and Crossref for structured family names.
Measurement-only: no surname career-effect estimates are produced.
Only aggregate public-safe outputs are persisted.
"""
from __future__ import annotations

import argparse, csv, json, os, re, time, unicodedata, urllib.parse, urllib.request
from collections import defaultdict
from pathlib import Path

OPENALEX = "https://api.openalex.org/works"
CROSSREF = "https://api.crossref.org/works/"
USER_AGENT = "ARIS4C006/0.4.1 randomized measurement-gate pilot"
FIELD_SET = {
    20: "Economics, Econometrics and Finance",
    26: "Mathematics",
    14: "Business, Management and Accounting",
    32: "Psychology",
    27: "Medicine",
    22: "Engineering",
}
YEARS_DEFAULT = [2015, 2020, 2024]
TOKEN_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ'’-]+")

def fetch_json(url: str, retries: int = 4) -> dict | None:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                return json.loads(response.read().decode("utf-8"))
        except Exception:
            if attempt + 1 == retries:
                return None
            time.sleep(0.6 * (attempt + 1))
    return None

def norm(text: str | None) -> str:
    if not text:
        return ""
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9]", "", text.lower())

def tokens(text: str | None) -> list[str]:
    out = []
    for x in TOKEN_RE.findall(text or ""):
        nx = norm(x)
        if nx:
            out.append(nx)
    return out

def norm_orcid(text: str | None) -> str:
    if not text:
        return ""
    text = text.lower().replace("https://orcid.org/", "").replace("http://orcid.org/", "")
    return re.sub(r"[^0-9x]", "", text)

def authorship_is_cn(authorship: dict) -> bool:
    return any((i.get("country_code") == "CN") for i in (authorship.get("institutions") or [])) or "CN" in (authorship.get("countries") or [])

def openalex_cell(field_id: int, year: int, target: int):
    """Yield a reproducible random multi-author sample from the filtered cell."""
    sample_n = min(100, max(target * 2, target + 20))
    seed = int(f"{year}{field_id:02d}")
    params = {
        "filter": ",".join([
            "authorships.institutions.country_code:CN",
            f"topics.field.id:{field_id}",
            f"from_publication_date:{year}-01-01",
            f"to_publication_date:{year}-12-31",
        ]),
        "select": "id,doi,publication_year,authorships,primary_location",
        "sample": sample_n,
        "seed": seed,
        "per-page": sample_n,
    }
    if os.getenv("OPENALEX_API_KEY"):
        params["api_key"] = os.environ["OPENALEX_API_KEY"]
    if os.getenv("OPENALEX_MAILTO"):
        params["mailto"] = os.environ["OPENALEX_MAILTO"]
    payload = fetch_json(OPENALEX + "?" + urllib.parse.urlencode(params))
    if not payload:
        return
    yielded = 0
    for w in payload.get("results") or []:
        if len(w.get("authorships") or []) < 2:
            continue
        yield w
        yielded += 1
        if yielded >= target:
            break

def crossref_record(doi_url: str) -> dict | None:
    doi = doi_url.removeprefix("https://doi.org/").removeprefix("http://doi.org/")
    payload = fetch_json(CROSSREF + urllib.parse.quote(doi, safe=""))
    return (payload or {}).get("message") or None

def pair_support(oa_auth: dict, cr_auth: dict) -> dict:
    raw = oa_auth.get("raw_author_name") or (oa_auth.get("author") or {}).get("display_name") or ""
    ts = tokens(raw)
    family = norm(cr_auth.get("family") or "")
    given_tokens = tokens(cr_auth.get("given") or "")
    fam_any = bool(family and family in ts)
    fam_first = bool(ts and family and ts[0] == family)
    fam_last = bool(ts and family and ts[-1] == family)
    nonfam = [t for t in ts if t != family]
    given_ok = True
    if given_tokens:
        given_ok = any(any((g == t) or (g and t and g[0] == t[0]) for t in nonfam) for g in given_tokens)
    oa_orcid = norm_orcid((oa_auth.get("author") or {}).get("orcid"))
    cr_orcid = norm_orcid(cr_auth.get("ORCID") or cr_auth.get("orcid"))
    return {
        "cn": authorship_is_cn(oa_auth),
        "family_any": fam_any,
        "family_first": fam_first,
        "family_last": fam_last,
        "position_supported": bool(fam_any and given_ok),
        "both_orcid_present": bool(oa_orcid and cr_orcid),
        "orcid_match": bool(oa_orcid and cr_orcid and oa_orcid == cr_orcid),
        "oa_author_id": (oa_auth.get("author") or {}).get("id") or "",
        "oa_orcid": oa_orcid,
    }

def safe_rate(num: int, den: int):
    return (num / den) if den else None

def summarize_cell(field_id: int, field_name: str, year: int, works: list[dict]):
    n = len(works)
    doi_works = [w for w in works if w.get("doi")]
    cr_found = same_count = all_family = strict_works = 0
    cn_pairs = cn_family_any = cn_family_last = cn_position_supported = 0
    all_pairs = all_position_supported = both_orcid = orcid_match = 0
    observed_pairs = []
    for w in doi_works:
        cr = crossref_record(w["doi"])
        if not cr:
            continue
        cr_found += 1
        oa, ca = w.get("authorships") or [], cr.get("author") or []
        if not ca or len(oa) != len(ca):
            time.sleep(0.04)
            continue
        same_count += 1
        if all(a.get("family") for a in ca):
            all_family += 1
        supports = [pair_support(o, c) for o, c in zip(oa, ca)]
        if supports and all(s["position_supported"] for s in supports):
            strict_works += 1
        for s in supports:
            all_pairs += 1
            all_position_supported += int(s["position_supported"])
            both_orcid += int(s["both_orcid_present"])
            orcid_match += int(s["orcid_match"])
            if s["oa_orcid"] and s["oa_author_id"]:
                observed_pairs.append((s["oa_orcid"], s["oa_author_id"]))
            if s["cn"]:
                cn_pairs += 1
                cn_family_any += int(s["family_any"])
                cn_family_last += int(s["family_last"])
                cn_position_supported += int(s["position_supported"])
        time.sleep(0.04)
    row = {
        "field_id": field_id, "field_name": field_name, "year": year,
        "sampled_multi_author_works": n,
        "doi_works": len(doi_works), "doi_rate": safe_rate(len(doi_works), n),
        "crossref_found": cr_found, "crossref_found_rate_among_doi": safe_rate(cr_found, len(doi_works)),
        "same_author_count_works": same_count, "same_author_count_rate_among_crossref": safe_rate(same_count, cr_found),
        "all_family_present_works": all_family,
        "strict_position_aligned_works": strict_works,
        "strict_position_aligned_rate_among_same_count": safe_rate(strict_works, same_count),
        "aligned_author_pairs": all_pairs,
        "position_supported_rate_all": safe_rate(all_position_supported, all_pairs),
        "aligned_cn_author_pairs": cn_pairs,
        "cn_family_anywhere_rate": safe_rate(cn_family_any, cn_pairs),
        "cn_family_last_token_rate": safe_rate(cn_family_last, cn_pairs),
        "cn_position_supported_rate": safe_rate(cn_position_supported, cn_pairs),
        "both_orcid_present_pairs": both_orcid,
        "orcid_exact_match_rate": safe_rate(orcid_match, both_orcid),
        "confirmatory_use_allowed": False,
    }
    return row, observed_pairs

def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8"); return
    with path.open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--years", default=",".join(map(str, YEARS_DEFAULT)))
    p.add_argument("--per-cell", type=int, default=40)
    p.add_argument("--outdir", default="data/pilot/measurement_gate")
    a = p.parse_args()
    years = [int(x.strip()) for x in a.years.split(",") if x.strip()]
    rows = []
    orcid_to_ids, author_to_orcids = defaultdict(set), defaultdict(set)
    for year in years:
        for fid, fname in FIELD_SET.items():
            works = list(openalex_cell(fid, year, a.per_cell))
            row, pairs = summarize_cell(fid, fname, year, works)
            rows.append(row)
            for oid, aid in pairs:
                orcid_to_ids[oid].add(aid); author_to_orcids[aid].add(oid)
            print(json.dumps(row, ensure_ascii=False))
    out = Path(a.outdir)
    write_csv(out / "measurement_gate_by_field_year.csv", rows)
    manifest = {
        "script": "04_measurement_gate_pilot.py",\n        "sampling": "OpenAlex reproducible random sample via sample+seed, then multi-author conditioning",
        "years": years, "per_cell_requested": a.per_cell, "fields": FIELD_SET,
        "confirmatory_use_allowed": False,
        "purpose": "Gate DOI/Crossref surname coverage, positional author alignment, ORCID agreement, and lower-bound OpenAlex identity inconsistency.",
        "observed_orcids": len(orcid_to_ids),
        "observed_openalex_author_ids_with_orcid": len(author_to_orcids),
        "orcid_values_mapping_to_multiple_openalex_ids_lower_bound": sum(len(v) > 1 for v in orcid_to_ids.values()),
        "openalex_ids_observed_with_multiple_orcids_lower_bound": sum(len(v) > 1 for v in author_to_orcids.values()),
        "privacy": "Only aggregate summaries are persisted; no raw names/DOIs/ORCIDs are written.",
    }
    out.mkdir(parents=True, exist_ok=True)
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
