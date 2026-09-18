#!/usr/bin/env python3
"""Download public source files used by ARIS4C007.

Network access is intentionally isolated in this script. Analysis scripts
consume local immutable files. Re-run only when intentionally updating source
versions.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import urllib.request
import zipfile
from pathlib import Path


SOURCES = {
    "anage": {
        "url": "https://genomics.senescence.info/species/dataset.zip",
        "filename": "anage_dataset.zip",
    },
    "peron2019_s5": {
        "url": "https://doi.org/10.1371/journal.pbio.3000432.s005",
        "filename": "peron2019_s5.xlsx",
    },
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def download(url: str, dest: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": "ARIS4C007/1.0"})
    with urllib.request.urlopen(req, timeout=120) as response, dest.open("wb") as out:
        out.write(response.read())


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
        download(spec["url"], dest)
        manifest[key] = {
            "url": spec["url"],
            "file": str(dest),
            "bytes": dest.stat().st_size,
            "sha256": sha256(dest),
        }

        if key == "anage":
            with zipfile.ZipFile(dest) as zf:
                members = zf.namelist()
                if "anage_data.txt" not in members:
                    raise RuntimeError(f"Unexpected AnAge archive contents: {members}")
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
