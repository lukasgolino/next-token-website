#!/usr/bin/env python3
"""Sanity checks on site/ (no build step, so this runs on the committed files): every local href/src resolves to a
file inside site/, the
sitemap lists exactly the pages, and robots.txt points to it."""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

SITE = Path(__file__).resolve().parent.parent / "site"
ORIGIN = "https://next-token.dev/"
PAGES = sorted(p for p in SITE.glob("*.html"))  # site/game/ is the exported Godot build, not ours to lint
errors = []


class Refs(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []

    def handle_starttag(self, tag, attrs):
        for k, v in attrs:
            if k in ("href", "src") and v:
                self.refs.append(v)


for page in PAGES:
    parser = Refs()
    parser.feed(page.read_text(encoding="utf-8"))
    for ref in parser.refs:
        u = urlsplit(ref)
        if u.scheme or u.netloc or ref.startswith(("#", "mailto:", "data:")):
            continue
        path = unquote(u.path)
        target = (SITE / path.lstrip("/")) if path.startswith("/") else (page.parent / path)
        if target.is_dir():
            target = target / "index.html"
        if not target.resolve().is_relative_to(SITE):
            errors.append(f"{page.relative_to(SITE)}: {ref} points outside site/")
        elif not target.exists():
            errors.append(f"{page.relative_to(SITE)}: broken link {ref}")

def url_of(page):
    return ORIGIN + ("" if page.name == "index.html" else page.name)


listed = re.findall(r"<loc>([^<]+)</loc>", (SITE / "sitemap.xml").read_text(encoding="utf-8"))
pages = {url_of(p) for p in PAGES}
errors += [f"sitemap.xml: {u} is not a page" for u in listed if u not in pages]
errors += [f"sitemap.xml: missing {u}" for u in sorted(pages - set(listed))]
if f"Sitemap: {ORIGIN}sitemap.xml" not in (SITE / "robots.txt").read_text(encoding="utf-8").splitlines():
    errors.append("robots.txt: no Sitemap line for sitemap.xml")

for e in errors:
    print(f"check_site: {e}", file=sys.stderr)
if errors:
    sys.exit(1)
print(f"check_site: {len(PAGES)} pages, links resolve, sitemap.xml and robots.txt match")
