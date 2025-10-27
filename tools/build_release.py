"""Utility for packaging Echoes of the Ruin into a distributable archive.

This script bundles the project source, assets, and documentation into a
versioned ZIP file inside the ``dist`` directory.  It also emits a small HTML
page that exposes a download link you can host locally with ``python -m
http.server``.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import sys
import zipfile
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
DIST_DIR = ROOT / "dist"
DEFAULT_VERSION = "0.1.0"
ARCHIVE_TEMPLATE = "echoes-of-the-ruin-{version}.zip"
INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"utf-8\" />
    <title>Echoes of the Ruin Download</title>
    <style>
        body {{font-family: 'Segoe UI', Roboto, sans-serif; background: #0f1119; color: #edf2ff; display: flex; min-height: 100vh; align-items: center; justify-content: center; margin: 0;}}
        .card {{background: #191c2b; padding: 2.5rem 3rem; border-radius: 18px; box-shadow: 0 32px 80px rgba(0,0,0,0.45); max-width: 520px; text-align: center;}}
        h1 {{margin-top: 0; font-size: 1.9rem; letter-spacing: 0.04em;}}
        a.download {{display: inline-block; margin-top: 1.8rem; padding: 0.9rem 1.6rem; background: #536dfe; color: white; text-decoration: none; border-radius: 999px; font-weight: 600; transition: transform 0.2s ease, box-shadow 0.2s ease;}}
        a.download:hover {{transform: translateY(-2px); box-shadow: 0 12px 28px rgba(83,109,254,0.45);}}
        .meta {{margin-top: 1.5rem; font-size: 0.9rem; color: rgba(237,242,255,0.78); line-height: 1.5;}}
    </style>
</head>
<body>
    <div class=\"card\">
        <h1>Echoes of the Ruin Build</h1>
        <p>Download the latest packaged prototype, ready to unzip and play.</p>
        <a class=\"download\" href=\"{archive_name}\">Download v{version}</a>
        <div class=\"meta\">
            <div>Archive size: {size_mb:.2f} MB</div>
            <div>Build timestamp: {timestamp}</div>
        </div>
    </div>
</body>
</html>
"""


def discover_paths() -> list[Path]:
    """Return all project files that must be part of the release archive."""
    includes: list[Path] = [
        ROOT / "README.md",
        ROOT / "requirements.txt",
        ROOT / "main.py",
    ]
    game_dir = ROOT / "game"
    if not game_dir.exists():
        raise SystemExit("Missing 'game' package – ensure you are running inside the project root.")
    includes.append(game_dir)
    return includes


def add_path(zip_file: zipfile.ZipFile, source: Path, base_dir: Path) -> None:
    """Append files from *source* to *zip_file*, preserving relative paths."""
    if source.is_file():
        arcname = source.relative_to(base_dir)
        zip_file.write(source, arcname)
        return

    for entry in source.rglob("*"):
        if entry.is_file():
            arcname = entry.relative_to(base_dir)
            zip_file.write(entry, arcname)


def write_manifest(zip_path: Path, version: str) -> None:
    manifest = {
        "name": "Echoes of the Ruin",
        "version": version,
        "generated": datetime.utcnow().isoformat() + "Z",
        "archive": zip_path.name,
        "size_bytes": zip_path.stat().st_size,
        "contents": [
            "README.md",
            "requirements.txt",
            "main.py",
            "game/",
        ],
    }
    manifest_path = zip_path.with_suffix(".json")
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def write_index(zip_path: Path, version: str) -> None:
    size_mb = zip_path.stat().st_size / (1024 * 1024)
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%SZ")
    index_html = INDEX_TEMPLATE.format(
        archive_name=zip_path.name,
        version=version,
        size_mb=size_mb,
        timestamp=timestamp,
    )
    (zip_path.parent / "index.html").write_text(index_html, encoding="utf-8")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Package the Echoes of the Ruin prototype")
    parser.add_argument("--version", default=DEFAULT_VERSION, help="Version label embedded into the archive name")
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Remove the dist directory before building a new release",
    )
    return parser.parse_args(argv)


def ensure_dist(clean: bool) -> None:
    if clean and DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    DIST_DIR.mkdir(parents=True, exist_ok=True)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    ensure_dist(args.clean)

    release_paths = discover_paths()
    archive_name = ARCHIVE_TEMPLATE.format(version=args.version)
    archive_path = DIST_DIR / archive_name

    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in release_paths:
            add_path(archive, path, ROOT)

    write_manifest(archive_path, args.version)
    write_index(archive_path, args.version)

    print(f"Release created: {archive_path}")
    print(f"Manifest created: {archive_path.with_suffix('.json')}")
    print(f"Serve dist directory with 'python -m http.server --directory dist' for a clickable download page.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
