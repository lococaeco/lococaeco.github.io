#!/usr/bin/env python3
"""
Notion markdown image localizer for Jekyll.

It does three things:
1) Find local image links in a markdown post.
2) Copy source images from a Notion export directory into assets/images/posts/<post-slug>/.
3) Rewrite image URLs in the markdown to the copied location.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, Tuple
from urllib.parse import unquote


MD_IMAGE_RE = re.compile(r"!\[(?P<alt>[^\]]*)\]\((?P<target>[^)]+)\)")
HTML_IMAGE_RE = re.compile(
    r'(?P<prefix><img\b[^>]*?\bsrc=["\'])(?P<src>[^"\']+)(?P<suffix>["\'][^>]*>)',
    re.IGNORECASE,
)
MD_TARGET_PATH_RE = re.compile(r'^(?P<path>\S+)(?:\s+["\'][^"\']*["\'])?$')


@dataclass
class Stats:
    found: int = 0
    rewritten: int = 0
    copied: int = 0
    skipped_remote: int = 0
    skipped_not_found: int = 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Copy Notion-exported images and rewrite markdown image links."
    )
    parser.add_argument("--post", required=True, type=Path, help="Path to post markdown file.")
    parser.add_argument(
        "--notion-dir",
        required=True,
        type=Path,
        help="Directory where Notion export images are located.",
    )
    parser.add_argument(
        "--dest-root",
        type=Path,
        default=Path("assets/images/posts"),
        help="Destination root for copied images. Default: assets/images/posts",
    )
    parser.add_argument(
        "--slug",
        default="",
        help="Optional destination slug. Default: from post filename.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without copying or writing files.",
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Do not create <post>.bak before writing.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print per-file logs.",
    )
    return parser.parse_args()


def is_remote_or_root(path_text: str) -> bool:
    lower = path_text.lower()
    return lower.startswith(("http://", "https://", "data:", "//", "/"))


def parse_md_target_path(target: str) -> str:
    text = target.strip()
    if text.startswith("<") and text.endswith(">"):
        return text[1:-1].strip()
    match = MD_TARGET_PATH_RE.match(text)
    if match:
        return match.group("path").strip()
    return text


def post_slug_from_filename(post_path: Path) -> str:
    name = post_path.stem
    match = re.match(r"^\d{4}-\d{2}-\d{2}-(?P<slug>.+)$", name)
    slug = match.group("slug") if match else name
    slug = re.sub(r"[^a-zA-Z0-9._-]+", "-", slug).strip("-").lower()
    return slug or "post"


def sanitize_filename(filename: str) -> str:
    path = Path(filename)
    stem = re.sub(r"[^a-zA-Z0-9._-]+", "-", path.stem).strip("-").lower()
    ext = path.suffix.lower()
    if not stem:
        stem = "image"
    return f"{stem}{ext}"


def resolve_source_image(notion_dir: Path, raw_path: str, by_name_cache: Dict[str, Optional[Path]]) -> Optional[Path]:
    decoded = unquote(raw_path)
    candidates = [
        (notion_dir / decoded),
        (notion_dir / raw_path),
    ]

    for candidate in candidates:
        if candidate.exists() and candidate.is_file():
            return candidate.resolve()

    basename = Path(decoded).name
    if basename:
        if basename not in by_name_cache:
            matches = [p for p in notion_dir.rglob("*") if p.is_file() and p.name == basename]
            by_name_cache[basename] = matches[0].resolve() if matches else None
        return by_name_cache[basename]
    return None


def unique_dest_path(dest_dir: Path, src_name: str, used: Dict[Path, Path]) -> Path:
    safe_name = sanitize_filename(src_name)
    candidate = dest_dir / safe_name
    index = 2
    while True:
        if candidate not in used.values():
            return candidate
        candidate = dest_dir / f"{Path(safe_name).stem}-{index}{Path(safe_name).suffix}"
        index += 1


def main() -> int:
    args = parse_args()
    repo_root = Path.cwd()
    post_path = args.post.resolve()
    notion_dir = args.notion_dir.resolve()
    dest_root = (repo_root / args.dest_root).resolve() if not args.dest_root.is_absolute() else args.dest_root.resolve()

    if not post_path.exists():
        print(f"Post file not found: {post_path}", file=sys.stderr)
        return 1
    if not notion_dir.exists() or not notion_dir.is_dir():
        print(f"Notion export directory not found: {notion_dir}", file=sys.stderr)
        return 1

    slug = args.slug.strip() or post_slug_from_filename(post_path)
    dest_dir = dest_root / slug

    text = post_path.read_text(encoding="utf-8")
    stats = Stats()
    source_to_dest: Dict[Path, Path] = {}
    by_name_cache: Dict[str, Optional[Path]] = {}

    def localize(raw_path: str) -> Optional[str]:
        stats.found += 1
        if is_remote_or_root(raw_path):
            stats.skipped_remote += 1
            return None

        src = resolve_source_image(notion_dir, raw_path, by_name_cache)
        if not src:
            stats.skipped_not_found += 1
            if args.verbose:
                print(f"[skip:not_found] {raw_path}")
            return None

        if src not in source_to_dest:
            dest = unique_dest_path(dest_dir, src.name, source_to_dest)
            source_to_dest[src] = dest
        else:
            dest = source_to_dest[src]

        rel = "/" + dest.relative_to(repo_root).as_posix()
        return rel

    def replace_md(match: re.Match[str]) -> str:
        target = match.group("target")
        path_part = parse_md_target_path(target)
        new_url = localize(path_part)
        if not new_url:
            return match.group(0)
        stats.rewritten += 1
        return f"![{match.group('alt')}]({new_url})"

    def replace_html(match: re.Match[str]) -> str:
        src = match.group("src")
        new_url = localize(src)
        if not new_url:
            return match.group(0)
        stats.rewritten += 1
        return f"{match.group('prefix')}{new_url}{match.group('suffix')}"

    rewritten = MD_IMAGE_RE.sub(replace_md, text)
    rewritten = HTML_IMAGE_RE.sub(replace_html, rewritten)

    if args.dry_run:
        print(f"[dry-run] post={post_path}")
        print(f"[dry-run] notion_dir={notion_dir}")
        print(f"[dry-run] dest_dir={dest_dir}")
        for src, dest in source_to_dest.items():
            print(f"[dry-run] copy {src} -> {dest}")
    else:
        dest_dir.mkdir(parents=True, exist_ok=True)
        for src, dest in source_to_dest.items():
            shutil.copy2(src, dest)
            stats.copied += 1
            if args.verbose:
                print(f"[copied] {src} -> {dest}")

        if not args.no_backup:
            backup = post_path.with_suffix(post_path.suffix + ".bak")
            shutil.copy2(post_path, backup)
            if args.verbose:
                print(f"[backup] {backup}")

        post_path.write_text(rewritten, encoding="utf-8")
        print(f"Wrote post: {post_path}")
        print(f"Copied images to: {dest_dir}")

    print(
        "Summary: "
        f"found={stats.found}, rewritten={stats.rewritten}, copied={stats.copied}, "
        f"remote_skipped={stats.skipped_remote}, not_found={stats.skipped_not_found}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

