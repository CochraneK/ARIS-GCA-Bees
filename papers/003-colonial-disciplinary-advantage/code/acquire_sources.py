#!/usr/bin/env python3
"""Reproducible acquisition helper for ARIS4C003 public/locally held sources.

Principles:
- no paid LLM API;
- no silent redistribution of restricted third-party data;
- every acquired/registered file gets a SHA-256 and provenance record;
- OpenAlex public snapshot access uses anonymous S3, not the paid daily API.

This script intentionally does not commit raw data. See repository .gitignore.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

PAPER = Path(__file__).resolve().parents[1]
RAW = PAPER / "data" / "raw"
SNAPSHOTS = PAPER / "data" / "snapshots"
MANIFESTS = PAPER / "data" / "manifests"
MANIFEST = MANIFESTS / "source_manifest.json"

SOURCES = {
    "openalex": {
        "landing": "https://help.openalex.org/access/snapshot/",
        "works_manifest": "https://openalex.s3.amazonaws.com/data/parquet/works/manifest.json",
        "s3_prefix": "s3://openalex/data/parquet/works",
        "license": "CC0/public OpenAlex metadata; verify bundled LICENSE.txt for the downloaded release",
        "redistribution": "record manifest/checksums; do not commit the hundreds-of-GB snapshot",
    },
    "coldat_years": {
        "landing": "https://ourworldindata.org/grapher/years-colonized",
        "csv": "https://ourworldindata.org/grapher/years-colonized.csv?v=1&csvType=full&useColumnShortNames=false",
        "metadata": "https://ourworldindata.org/grapher/years-colonized.metadata.json?v=1&csvType=full&useColumnShortNames=false",
        "source": "Bastian Becker, Colonial Dates Dataset (COLDAT) 3.0, processed by Our World in Data",
        "license": "OWID chart data marked CC BY; preserve original-source and OWID citations",
        "redistribution": "raw local copy may be reconstructed from official URL; commit only compact derived tables/manifests",
    },
    "coldat_colonizer_year": {
        "landing": "https://ourworldindata.org/grapher/european-overseas-colonies-and-their-colonizers",
        "csv": "https://ourworldindata.org/grapher/european-overseas-colonies-and-their-colonizers.csv?v=1&csvType=full&useColumnShortNames=false",
        "metadata": "https://ourworldindata.org/grapher/european-overseas-colonies-and-their-colonizers.metadata.json?v=1&csvType=full&useColumnShortNames=false",
        "source": "Bastian Becker, Colonial Dates Dataset (COLDAT) 3.0, processed by Our World in Data",
        "license": "OWID chart data marked CC BY; preserve original-source and OWID citations",
        "redistribution": "raw local copy may be reconstructed from official URL; commit only compact derived tables/manifests",
    },
    "coldat_empire_counts": {
        "landing": "https://ourworldindata.org/grapher/european-overseas-colonies-by-colonizer",
        "csv": "https://ourworldindata.org/grapher/european-overseas-colonies-by-colonizer.csv?v=1&csvType=full&useColumnShortNames=false",
        "metadata": "https://ourworldindata.org/grapher/european-overseas-colonies-by-colonizer.metadata.json?v=1&csvType=full&useColumnShortNames=false",
        "source": "Bastian Becker COLDAT 3.0 plus Gapminder Population v7, processed by Our World in Data",
        "license": "OWID page is CC BY; preserve underlying-provider citations and terms",
        "redistribution": "raw local copy may be reconstructed from official URL; commit only compact derived tables/manifests",
    },
    "coldat_original": {
        "landing": "https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/T9SDEW",
        "download": "https://dataverse.harvard.edu/api/access/datafile/7416946?format=original",
        "file": "COLDAT_colonies.tab",
        "version": "COLDAT 3.0 source file as distributed by Harvard Dataverse",
        "license": "CC0 1.0",
        "redistribution": "CC0; raw remains gitignored by project convention; record checksum/provenance",
    },
    "icow": {
        "landing": "https://www.paulhensel.org/icowcol.html",
        "download": "https://www.paulhensel.org/Data/colhist.zip",
        "version": "1.1 (official page current as checked 2026-09-18)",
        "license_note": "free download with explicit request not to redistribute; direct users to official site",
        "redistribution": "DO NOT COMMIT OR REDISTRIBUTE RAW ICOW ARCHIVE",
    },
    "cepii_gravity": {
        "landing": "https://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=8",
        "download": "https://www.cepii.fr/DATA_DOWNLOAD/gravity/data/Gravity_csv_V202211.zip",
        "version": "202211",
        "license": "Etalab 2.0",
        "redistribution": "follow Etalab 2.0; raw zip remains gitignored; keep exact checksum/version in manifest",
    },
    "leiden_open_2025_results": {
        "landing": "https://open.leidenranking.com/resources",
        "doi": "https://doi.org/10.5281/zenodo.17473224",
        "license": "CC0",
        "redistribution": "CC0; retain source DOI/version/checksum",
    },
    "leiden_open_2025_data": {
        "landing": "https://open.leidenranking.com/resources",
        "doi": "https://doi.org/10.5281/zenodo.17471989",
        "license": "CC0",
        "redistribution": "CC0; retain source DOI/version/checksum",
    },
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def load_manifest() -> dict:
    if MANIFEST.exists():
        return json.loads(MANIFEST.read_text(encoding="utf-8"))
    return {
        "schema_version": 1,
        "paper": "ARIS4C003",
        "created_utc": utc_now(),
        "sources": {},
    }


def save_manifest(obj: dict) -> None:
    MANIFESTS.mkdir(parents=True, exist_ok=True)
    obj["updated_utc"] = utc_now()
    MANIFEST.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def record(source: str, path: Path | None, **extra: object) -> None:
    obj = load_manifest()
    entry = {
        "source_metadata": SOURCES[source],
        "recorded_utc": utc_now(),
        **extra,
    }
    if path is not None:
        entry.update(
            {
                "local_path": str(path.relative_to(PAPER) if path.is_relative_to(PAPER) else path),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )
    obj["sources"][source] = entry
    save_manifest(obj)


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "ARIS4C003-reproducibility/1.0"})
    with urllib.request.urlopen(req, timeout=120) as r, dest.open("wb") as f:
        shutil.copyfileobj(r, f)


def cmd_init(_: argparse.Namespace) -> None:
    obj = load_manifest()
    for key, meta in SOURCES.items():
        obj["sources"].setdefault(key, {"source_metadata": meta, "status": "not_acquired"})
    save_manifest(obj)
    print(MANIFEST)


def cmd_openalex_manifest(_: argparse.Namespace) -> None:
    dest = MANIFESTS / "openalex_works_manifest.json"
    download(SOURCES["openalex"]["works_manifest"], dest)
    parsed = json.loads(dest.read_text(encoding="utf-8"))
    record(
        "openalex",
        dest,
        status="manifest_acquired_snapshot_not_downloaded",
        openalex_manifest_meta={
            key: parsed.get(key)
            for key in ("meta", "content_length", "record_count")
            if key in parsed
        },
    )
    print(dest)


def cmd_openalex_snapshot(args: argparse.Namespace) -> None:
    if not args.confirm_huge_download:
        raise SystemExit(
            "Refusing large download. OpenAlex Works Parquet is hundreds of GB. "
            "Re-run with --confirm-huge-download only on a machine with sufficient disk/network."
        )
    if shutil.which("aws") is None:
        raise SystemExit("AWS CLI not found. Install it first; no AWS account is required.")
    dest = SNAPSHOTS / "openalex" / "parquet" / "works"
    dest.mkdir(parents=True, exist_ok=True)
    command = [
        "aws", "s3", "sync", SOURCES["openalex"]["s3_prefix"], str(dest),
        "--no-sign-request", "--delete",
    ]
    print("Running:", " ".join(command))
    subprocess.run(command, check=True)
    record("openalex", None, status="snapshot_synced", local_path=str(dest.relative_to(PAPER)), command=command)


def cmd_coldat(args: argparse.Namespace) -> None:
    plans = {
        "coldat_years": RAW / "coldat" / "years-colonized.csv",
        "coldat_colonizer_year": RAW / "coldat" / "colonizer-by-country-year.csv",
        "coldat_empire_counts": RAW / "coldat" / "colonies-by-colonizer.csv",
    }
    if not args.execute:
        for source, dest in plans.items():
            print(source, SOURCES[source]["csv"], "->", dest)
        return
    for source, dest in plans.items():
        download(SOURCES[source]["csv"], dest)
        metadata_dest = dest.with_suffix(".metadata.json")
        download(SOURCES[source]["metadata"], metadata_dest)
        record(
            source,
            dest,
            status="acquired_local",
            metadata_local_path=str(metadata_dest.relative_to(PAPER)),
            metadata_sha256=sha256(metadata_dest),
        )
        print(dest)


def cmd_cepii(args: argparse.Namespace) -> None:
    dest = RAW / "cepii" / "Gravity_csv_V202211.zip"
    if not args.execute:
        print("Dry run. Official CEPII download:", SOURCES["cepii_gravity"]["download"])
        print("Target:", dest)
        return
    download(SOURCES["cepii_gravity"]["download"], dest)
    if dest.stat().st_size < 100_000_000:
        raise SystemExit(
            f"CEPII archive unexpectedly small ({dest.stat().st_size} bytes); "
            "possible error page or truncated download"
        )
    record("cepii_gravity", dest, status="acquired_local")
    print(dest)


def cmd_icow(args: argparse.Namespace) -> None:
    dest = RAW / "icow" / "colhist_v1.1.zip"
    if not args.execute:
        print("Dry run. Official download:", SOURCES["icow"]["download"])
        print("Target:", dest)
        return
    download(SOURCES["icow"]["download"], dest)
    record("icow", dest, status="acquired_local_only")
    print(dest)


def cmd_register(args: argparse.Namespace) -> None:
    path = Path(args.file).expanduser().resolve()
    if not path.exists() or not path.is_file():
        raise SystemExit(f"File not found: {path}")
    if args.source not in SOURCES:
        raise SystemExit(f"Unknown source: {args.source}")
    record(args.source, path, status="registered_local_file")
    print(f"Registered {args.source}: {path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("init", help="create/update source manifest without downloading raw data")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("openalex-manifest", help="download only the small public Works manifest")
    p.set_defaults(func=cmd_openalex_manifest)

    p = sub.add_parser("openalex-snapshot", help="sync the full public Works Parquet snapshot")
    p.add_argument("--confirm-huge-download", action="store_true")
    p.set_defaults(func=cmd_openalex_snapshot)

    p = sub.add_parser("coldat", help="download OWID-processed COLDAT primary exposure files")
    p.add_argument("--execute", action="store_true")
    p.set_defaults(func=cmd_coldat)

    p = sub.add_parser("cepii", help="download CEPII Gravity V202211 CSV zip")
    p.add_argument("--execute", action="store_true")
    p.set_defaults(func=cmd_cepii)

    p = sub.add_parser("icow", help="download ICOW locally from its official site")
    p.add_argument("--execute", action="store_true")
    p.set_defaults(func=cmd_icow)

    p = sub.add_parser("register", help="register/checksum a manually downloaded official file")
    p.add_argument("--source", required=True, choices=sorted(SOURCES))
    p.add_argument("--file", required=True)
    p.set_defaults(func=cmd_register)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
