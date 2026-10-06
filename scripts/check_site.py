#!/usr/bin/env python3
"""Validate a generated Jekyll site without network requests or dependencies.

Run after ``bundle exec jekyll build``. This checks the generated output, not
Google's indexing state. It never changes source files or generated files.
"""
from __future__ import annotations

import argparse
from collections import Counter
import datetime as dt
from html.parser import HTMLParser
import json
from pathlib import Path
import posixpath
import re
import sys
from urllib.parse import unquote, urljoin, urlsplit
import xml.etree.ElementTree as ET
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


class Document(HTMLParser):
    def __init__(self, path: Path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.lang = ""
        self.title = ""
        self.in_title = False
        self.meta: dict[str, list[str]] = {}
        self.canonical: list[str] = []
        self.references: list[tuple[str, str]] = []
        self.ids: list[str] = []
        self.h1 = 0
        self.main = 0
        self.images: list[dict[str, str]] = []
        self.structured: list[str] = []
        self.json_buffer: list[str] | None = None
        self.feed(path.read_text(encoding="utf-8"))
        self.close()

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if attrs.get("id"):
            self.ids.append(attrs["id"])
        if tag == "html":
            self.lang = attrs.get("lang", "")
        elif tag == "title":
            self.in_title = True
        elif tag == "meta":
            key = attrs.get("name") or attrs.get("property")
            if key:
                self.meta.setdefault(key.lower(), []).append(attrs.get("content", ""))
        elif tag == "link" and "canonical" in attrs.get("rel", "").split():
            self.canonical.append(attrs.get("href", ""))
        elif tag == "h1":
            self.h1 += 1
        elif tag == "main" or attrs.get("role") == "main":
            self.main += 1
        elif tag == "img":
            self.images.append(attrs)
        elif tag == "script" and attrs.get("type", "").lower() == "application/ld+json":
            self.json_buffer = []
        for attribute in ("href", "src", "poster"):
            if attrs.get(attribute):
                self.references.append((tag + "[" + attribute + "]", attrs[attribute]))

    handle_startendtag = handle_starttag

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        if tag == "script" and self.json_buffer is not None:
            self.structured.append("".join(self.json_buffer))
            self.json_buffer = None

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        if self.json_buffer is not None:
            self.json_buffer.append(data)

    @property
    def noindex(self):
        values = self.meta.get("robots", []) + self.meta.get("googlebot", [])
        return any("noindex" in re.split(r"[\s,]+", value.lower()) for value in values)


def strip_frontmatter(text: str) -> str:
    return re.sub(r"\A---\r?\n.*?\r?\n---(?:\r?\n|$)", "", text, count=1, flags=re.S)


def simple_value(text, key):
    """Read a single-line scalar used by this site's publication settings.

    This is deliberately not a general YAML parser. The Jekyll build remains
    responsible for validating YAML; complex/custom URL schemas need their own
    check instead of inferring a post's output path from its filename.
    """
    match = re.search(r"^" + re.escape(key) + r"\s*:\s*(.*?)\s*$", text, re.M)
    if not match:
        return None
    value = re.split(r"\s+#", match[1], maxsplit=1)[0].strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    if value.lower() in ("true", "false"):
        return value.lower() == "true"
    return value


def schema_nodes(value):
    if isinstance(value, list):
        for item in value:
            yield from schema_nodes(item)
    elif isinstance(value, dict):
        if "@type" in value:
            yield value
        for child in value.values():
            if isinstance(child, (dict, list)):
                yield from schema_nodes(child)


def has_schema_type(node, wanted):
    value = node.get("@type", [])
    return wanted in (value if isinstance(value, list) else [value])


class SiteCheck:
    def __init__(self, source: Path, site: Path, base_url: str):
        self.source, self.site = source.resolve(), site.resolve()
        self.base = base_url.rstrip("/")
        self.origin = urlsplit(self.base)
        self.errors: list[str] = []
        self.checks = 0
        self.documents: dict[Path, Document] = {}
        self.schemas: dict[Path, list[dict]] = {}
        self.sitemap_urls: set[str] = set()
        self.public_posts: list[Path] = []
        self.private_slugs: list[str] = []
        self.scheduled_slugs: list[str] = []
        self.sitemap_excluded_posts: set[Path] = set()
        config = (self.source / "_config.yml").read_text(encoding="utf-8")
        try:
            self.timezone = ZoneInfo(simple_value(config, "timezone") or "UTC")
        except ZoneInfoNotFoundError:
            self.timezone = dt.timezone.utc
        self.build_time = dt.datetime.now(self.timezone)
        self.include_future = simple_value(config, "future") is True
        self.verifications = {path.name for pattern in ("google*.html", "naver*.html", "BingSiteAuth.xml") for path in source.glob(pattern)}

    def require(self, condition, message):
        self.checks += 1
        if not condition:
            self.errors.append(message)

    def relative(self, path):
        return path.relative_to(self.site).as_posix()

    def local_target(self, value, current_url):
        """Return an output path for a same-site URL, or None for external URLs."""
        parsed = urlsplit(urljoin(current_url, value))
        if parsed.scheme not in ("http", "https") or parsed.netloc != self.origin.netloc:
            return None
        decoded = unquote(parsed.path)
        base_path = self.origin.path.rstrip("/")
        if base_path and not (decoded == base_path or decoded.startswith(base_path + "/")):
            return self.site / "__outside_site_base_path__"
        decoded = decoded[len(base_path):] if base_path else decoded
        relative = posixpath.normpath("/" + decoded.lstrip("/")).lstrip("/")
        target = self.site / relative
        candidates = [target, target / "index.html"]
        if not target.suffix:
            candidates.append(target.with_suffix(".html"))
        for candidate in candidates:
            if candidate.is_file():
                return candidate.resolve()
        return target

    def default_url(self, path):
        relative = self.relative(path)
        if relative == "index.html":
            relative = ""
        elif relative.endswith("/index.html"):
            relative = relative[:-10]
        return self.base + "/" + relative

    def check_documents(self):
        for path in sorted(self.site.rglob("*.html")):
            if path.name in self.verifications:
                continue
            name = self.relative(path)
            try:
                document = Document(path)
            except (OSError, UnicodeError) as error:
                self.require(False, f"{name}: cannot parse HTML: {error}")
                continue
            self.documents[path.resolve()] = document
            self.require(bool(document.lang), f"{name}: missing HTML language")
            self.require(bool(document.title.strip()), f"{name}: missing page title")
            self.require(document.h1 > 0, f"{name}: missing h1 heading")
            self.require(document.main == 1, f"{name}: expected one main landmark, found {document.main}")
            self.require("load" not in document.ids, f"{name}: blocking loading overlay remains")
            duplicates = [key for key, count in Counter(document.ids).items() if count > 1]
            self.require(not duplicates, f"{name}: duplicate IDs: {', '.join(duplicates[:5])}")
            description = document.meta.get("description", [])
            self.require(len(description) == 1 and bool(description[0].strip()), f"{name}: expected one nonempty meta description")
            self.require(len(document.canonical) == 1, f"{name}: expected one canonical URL")
            canonical = document.canonical[0] if document.canonical else self.default_url(path)
            parsed = urlsplit(canonical)
            self.require(parsed.scheme == "https" and parsed.netloc == self.origin.netloc and not parsed.query and not parsed.fragment,
                         f"{name}: invalid canonical URL: {canonical}")
            self.require(self.local_target(canonical, canonical) == path.resolve(), f"{name}: canonical points to a different or missing file: {canonical}")
            for key in ("og:title", "og:description", "og:url", "og:type", "twitter:card"):
                self.require(len(document.meta.get(key, [])) == 1 and bool(document.meta[key][0]), f"{name}: missing/duplicate/empty {key}")
            self.require(document.meta.get("og:url") == [canonical], f"{name}: og:url and canonical differ")
            for values in (document.meta.get("og:image", []), document.meta.get("twitter:image", [])):
                for value in values:
                    target = self.local_target(value, canonical)
                    self.require(target is None or target.is_file(), f"{name}: social image does not exist: {value}")
            for image in document.images:
                self.require("alt" in image, f"{name}: image is missing alt attribute: {image.get('src', '(no src)')}")
            nodes = []
            for raw in document.structured:
                try:
                    nodes.extend(schema_nodes(json.loads(raw)))
                except (TypeError, ValueError) as error:
                    self.require(False, f"{name}: invalid JSON-LD: {error}")
            self.schemas[path.resolve()] = nodes
            if name == "index.html":
                self.require(any(has_schema_type(node, "WebSite") for node in nodes), "Homepage is missing WebSite structured data")
            for kind, value in document.references:
                if value.startswith("#"):
                    continue
                target = self.local_target(value, canonical)
                self.require(target is None or target.is_file(), f"{name}: broken local {kind}: {value}")
        self.require(bool(self.documents), "No generated HTML pages were found")

    def check_posts(self):
        for source in sorted((self.source / "_posts").rglob("*")):
            if source.suffix.lower() not in (".md", ".markdown", ".mkd", ".mkdn", ".mkdown"):
                continue
            text = source.read_text(encoding="utf-8")
            match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, flags=re.S)
            header = match[1] if match else ""
            slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", source.stem)
            matches = [path for path in self.documents if (path.name == "index.html" and path.parent.name == slug) or path.stem == slug]
            hidden = bool(re.search(r"^published:\s*false\s*(?:#.*)?$", header, flags=re.M | re.I))
            if hidden:
                self.private_slugs.append(slug)
                self.require(not matches, f"Private post was generated: {source.relative_to(self.source)}")
                continue
            date_value = simple_value(header, "date") or source.name[:10]
            try:
                normalized = re.sub(r"\s+([+-]\d{2}:?\d{2})$", r"\1", str(date_value)).replace("Z", "+00:00")
                post_date = dt.datetime.fromisoformat(normalized)
                if post_date.tzinfo is None:
                    post_date = post_date.replace(tzinfo=self.timezone)
            except ValueError:
                post_date = None  # Non-ISO YAML dates are outside this small checker.
            if not self.include_future and post_date and post_date > self.build_time:
                self.scheduled_slugs.append(slug)
                self.require(not matches, f"Scheduled post was generated before its date: {source.relative_to(self.source)}")
                continue
            self.require(len(matches) == 1, f"Public post must have one generated document: {source.relative_to(self.source)} (found {len(matches)})")
            for path in matches:
                self.public_posts.append(path)
                document = self.documents[path]
                intentional_noindex = simple_value(header, "noindex") is True
                self.require(document.noindex == intentional_noindex, f"Post noindex does not match its front matter: {self.relative(path)}")
                if intentional_noindex or simple_value(header, "sitemap") is False:
                    self.sitemap_excluded_posts.add(path)
                articles = [node for node in self.schemas[path] if has_schema_type(node, "BlogPosting") or has_schema_type(node, "Article")]
                self.require(bool(articles), f"Public post lacks Article/BlogPosting structured data: {self.relative(path)}")
                for article in articles:
                    for field in ("headline", "datePublished", "dateModified", "author"):
                        self.require(bool(article.get(field)), f"{self.relative(path)}: Article is missing {field}")

    def check_xml_and_indexing(self):
        sitemap = self.site / "sitemap.xml"
        try:
            tree = ET.parse(sitemap)
            urls = [node.text or "" for node in tree.getroot().iter() if node.tag.rsplit("}", 1)[-1] == "loc"]
            self.sitemap_urls = set(urls)
            self.require(bool(urls), "sitemap.xml is empty")
            self.require(len(urls) == len(set(urls)), "sitemap.xml contains duplicate URLs")
            for url in urls:
                target = self.local_target(url, self.base + "/")
                self.require(target is not None and target.is_file(), f"Sitemap URL does not resolve locally: {url}")
                if target in self.documents:
                    document = self.documents[target]
                    self.require(not document.noindex, f"noindex page is included in sitemap: {url}")
                    self.require(document.canonical == [url], f"Sitemap URL differs from canonical: {url}")
        except (OSError, ET.ParseError) as error:
            self.require(False, f"Invalid/missing sitemap.xml: {error}")
        for path in self.public_posts:
            document = self.documents[path]
            if path in self.sitemap_excluded_posts:
                self.require(not document.canonical or document.canonical[0] not in self.sitemap_urls, f"Intentionally excluded post is in sitemap: {self.relative(path)}")
            else:
                self.require(bool(document.canonical) and document.canonical[0] in self.sitemap_urls, f"Public post is missing from sitemap: {self.relative(path)}")
        for path, document in self.documents.items():
            if path.stem in ("search", "404") or path.parent.name == "search":
                self.require(document.noindex, f"Utility page should be noindex: {self.relative(path)}")
        try:
            feed = ET.parse(self.site / "feed.xml")
            self.require(feed.getroot().tag.rsplit("}", 1)[-1] in ("rss", "feed"), "feed.xml has an unexpected root element")
        except (OSError, ET.ParseError) as error:
            self.require(False, f"Invalid/missing feed.xml: {error}")
        try:
            robots = (self.site / "robots.txt").read_text(encoding="utf-8")
            self.require(f"Sitemap: {self.base}/sitemap.xml" in robots, "robots.txt must advertise this site's sitemap")
            self.require(not re.search(r"^\s*Disallow:\s*/\s*$", robots, re.M | re.I), "robots.txt disallows the entire website")
        except OSError as error:
            self.require(False, f"Missing robots.txt: {error}")
        for filename in ("sitemap.xml", "feed.xml", "search.json"):
            path = self.site / filename
            text = path.read_text(encoding="utf-8") if path.is_file() else ""
            for slug in self.private_slugs + self.scheduled_slugs:
                self.require(not re.search(r"/" + re.escape(slug) + r"(?:/|\.html)", text), f"Unpublished post URL leaked into {filename}: {slug}")

    def check_search(self):
        try:
            records = json.loads((self.site / "search.json").read_text(encoding="utf-8"))
            self.require(isinstance(records, list), "search.json must contain an array")
            if not isinstance(records, list):
                return
            seen = []
            for record in records:
                self.require(isinstance(record, dict), "search.json contains a non-object record")
                if not isinstance(record, dict):
                    continue
                target = self.local_target(record.get("url", ""), self.base + "/")
                self.require(target in self.public_posts, f"Search result does not point to a public post: {record.get('url')}")
                seen.append(target)
                if record.get("teaser"):
                    teaser = self.local_target(record["teaser"], self.base + "/")
                    self.require(teaser is None or teaser.is_file(), f"Search result image does not exist: {record['teaser']}")
            self.require(set(seen) == set(self.public_posts), "search.json does not match the set of public posts")
            self.require(len(seen) == len(set(seen)), "search.json contains duplicate posts")
        except (OSError, ValueError, TypeError) as error:
            self.require(False, f"Invalid/missing search.json: {error}")

    def check_preservation_and_exclusions(self):
        self.require(bool(self.verifications), "No source ownership verification files found")
        for filename in sorted(self.verifications):
            original = strip_frontmatter((self.source / filename).read_text(encoding="utf-8")).strip()
            output = self.site / filename
            self.require(output.is_file(), f"Ownership verification file is missing: {filename}")
            if output.is_file():
                self.require(output.read_text(encoding="utf-8").strip() == original, f"Ownership verification content changed: {filename}")
            self.require(self.base + "/" + filename not in self.sitemap_urls, f"Verification file should not be in sitemap: {filename}")
        forbidden = {"tools", ".blog-studio", ".git", ".github", "scripts", "_posts", "node_modules", "vendor", "__pycache__"}
        for path in self.site.rglob("*"):
            relative = path.relative_to(self.site)
            self.require(not any(part in forbidden for part in relative.parts), f"Private/development artifact was published: {relative.as_posix()}")
            if path.is_file():
                self.require(path.name not in ("blog-studio.sh", "blog-studio.cmd", "Gemfile", "Gemfile.lock", "package.json", "package-lock.json"), f"Development file was published: {relative.as_posix()}")

    def run(self):
        self.check_documents()
        self.check_posts()
        self.check_xml_and_indexing()
        self.check_search()
        self.check_preservation_and_exclusions()
        return not self.errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    root = Path(__file__).resolve().parents[1]
    parser.add_argument("--source", type=Path, default=root, help="Jekyll source repository")
    parser.add_argument("--site", type=Path, default=root / "_site", help="Generated Jekyll output directory")
    parser.add_argument("--base-url", help="Canonical site base URL; default: url in _config.yml")
    args = parser.parse_args(argv)
    if not args.site.is_dir():
        parser.error(f"Generated site not found: {args.site}. Run the Jekyll build first.")
    base = args.base_url
    if not base:
        config = (args.source / "_config.yml").read_text(encoding="utf-8")
        match = re.search(r"^url\s*:\s*['\"]?([^'\"\s#]+)", config, flags=re.M)
        if not match:
            parser.error("Set url in _config.yml or provide --base-url")
        base = match[1]
        base_match = re.search(r"^baseurl\s*:\s*['\"]?([^'\"\s#]+)", config, flags=re.M)
        if base_match:
            base = base.rstrip("/") + "/" + base_match[1].strip("/")
    check = SiteCheck(args.source, args.site, base)
    passed = check.run()
    if passed:
        print(f"PASS: {check.checks} checks; {len(check.documents)} HTML pages; {len(check.public_posts)} public posts; {len(check.private_slugs)} private and {len(check.scheduled_slugs)} scheduled posts excluded.")
        print("Validated metadata, canonical URLs, JSON-LD, sitemap/feed/search, local assets, accessibility structure, ownership files, and private artifact exclusion.")
        print("This is a local build check, not a claim of Google indexing or production deployment.")
        return 0
    errors = list(dict.fromkeys(check.errors))
    print(f"FAIL: {len(errors)} issue(s) in {check.checks} checks:", file=sys.stderr)
    for error in errors[:80]:
        print("- " + error, file=sys.stderr)
    if len(errors) > 80:
        print(f"- ... {len(errors) - 80} more", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
