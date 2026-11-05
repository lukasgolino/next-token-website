#!/usr/bin/env python3
"""Sanity checks on site/ (no build step, so this runs on the committed files): every local href/src resolves to a
file inside site/."""
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

SITE = Path(__file__).resolve().parent.parent / "site"
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

for e in errors:
    print(f"check_site: {e}", file=sys.stderr)
if errors:
    sys.exit(1)
print(f"check_site: {len(PAGES)} pages, all local links resolve")
