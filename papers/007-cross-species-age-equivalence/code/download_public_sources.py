#!/usr/bin/env python3
"""Download public source files used by ARIS4C007 with provenance checks.

Network access is intentionally isolated here. Analysis scripts consume local
immutable files. Downloads are validated before use because some source hosts
occasionally return an HTML error/rate-limit page with HTTP 200.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
import urllib.request
import zipfile
from pathlib import Path


SOURCES = {
    "anage": {
        "urls": [
            "https://genomics.senescence.info/species/dataset.zip",
            "https://www.genomics.senescence.info/species/dataset.zip",
        ],
        "filename": "anage_dataset.zip",
        "kind": "anage_zip",
        "referer": "https://genomics.senescence.info/species/download.html",
    },
    "peron2019_s5": {
        "urls": ["https://doi.org/10.1371/journal.pbio.3000432.s005"],
        "filename": "peron2019_s5.xlsx",
        "kind": "xlsx",
        "referer": "https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.3000432",
    },
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def validate(path: Path, kind: str) -> bool:
    if not path.exists() or path.stat().st_size < 1000:
        return False
    if kind == "anage_zip":
        if not zipfile.is_zipfile(path):
            return False
        with zipfile.ZipFile(path) as zf:
            return "anage_data.txt" in zf.namelist()
    if kind == "xlsx":
        if not zipfile.is_zipfile(path):
            return False
        with zipfile.ZipFile(path) as zf:
            names = set(zf.namelist())
            return "[Content_Types].xml" in names and any(
                x.startswith("xl/worksheets/") for x in names
            )
    raise ValueError(f"unknown validation kind: {kind}")


def download_one(
    urls: list[str],
    dest: Path,
    *,
    kind: str,
    referer: str | None = None,
    attempts_per_url: int = 3,
) -> str:
    errors: list[str] = []
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; ARIS4C007/1.0; research-reproducibility)",
        "Accept": "application/zip,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,*/*;q=0.8",
    }
    if referer:
        headers["Referer"] = referer

    for url in urls:
        for attempt in range(1, attempts_per_url + 1):
            tmp = dest.with_suffix(dest.suffix + ".part")
            tmp.unlink(missing_ok=True)
            try:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=120) as response, tmp.open("wb") as out:
                    while True:
                        chunk = response.read(1024 * 1024)
                        if not chunk:
                            break
                        out.write(chunk)
                tmp.replace(dest)
                if validate(dest, kind):
                    return url
                preview = dest.read_bytes()[:80]
                errors.append(
                    f"{url} attempt {attempt}: content validation failed "
                    f"({dest.stat().st_size} bytes; prefix={preview!r})"
                )
            except Exception as exc:
                errors.append(f"{url} attempt {attempt}: {type(exc).__name__}: {exc}")
            finally:
                tmp.unlink(missing_ok=True)

            dest.unlink(missing_ok=True)
            if attempt < attempts_per_url:
                time.sleep(attempt * 2)

    raise RuntimeError("All download attempts failed:\n" + "\n".join(errors))


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--out", type=Path, default=Path("data/raw"))
    p.add_argument("--source", choices=["all", *SOURCES], default="all")
    args = p.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    selected = SOURCES if args.source == "all" else {args.source: SOURCES[args.source]}
    manifest = {}

    for key, spec in selected.items():
        dest = args.out / spec["filename"]
        selected_url = download_one(
            list(spec["urls"]),
            dest,
            kind=str(spec["kind"]),
            referer=spec.get("referer"),
        )
        manifest[key] = {
            "requested_urls": spec["urls"],
            "selected_url": selected_url,
            "file": str(dest),
            "bytes": dest.stat().st_size,
            "sha256": sha256(dest),
        }

        if key == "anage":
            with zipfile.ZipFile(dest) as zf:
                zf.extract("anage_data.txt", args.out)
                txt = args.out / "anage_data.txt"
                manifest[key]["extracted_file"] = str(txt)
                manifest[key]["extracted_sha256"] = sha256(txt)

    manifest_path = args.out / "source_manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(manifest_path)


if __name__ == "__main__":
    main()
