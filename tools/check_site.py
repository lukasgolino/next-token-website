#!/usr/bin/env python3
"""Sanity checks on site/ (no build step, so this runs on the committed files): every local href/src resolves to a
file inside site/, each page's
canonical link is its own URL, the sitemap lists exactly those URLs, robots.txt points to it, and
every page (and game/index.html) loads the analytics beacon exactly once."""
import json
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

SITE = Path(__file__).resolve().parent.parent / "site"
ORIGIN = "https://next-token.dev/"
TOKEN = "1c2ae262b9034043ac24d179d34c8a27"  # Cloudflare Web Analytics site token
BEACON_SRC = "https://static.cloudflareinsights.com/beacon.min.js"
PAGES = sorted(p for p in SITE.glob("*.html"))  # site/game/ is the exported Godot build, not ours to lint
errors = []
canonicals = {}
og_urls = {}


class Refs(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []
        self.canonical = []
        self.og_url = []
        self.beacons = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "link" and "canonical" in (a.get("rel") or "").lower().split():
            self.canonical.append(a.get("href"))
        if tag == "script" and a.get("src") == BEACON_SRC:
            try:
                self.beacons.append(json.loads(a.get("data-cf-beacon") or "").get("token"))
            except (ValueError, AttributeError):
                self.beacons.append(None)
        if tag == "meta" and a.get("property") == "og:url":
            self.og_url.append(a.get("content"))
        if tag == "meta" and a.get("property") == "og:image" and a.get("content"):
            self.refs.append(a["content"])
        for k, v in attrs:
            if k in ("href", "src") and v:
                self.refs.append(v)


for page in PAGES:
    parser = Refs()
    parser.feed(page.read_text(encoding="utf-8"))
    if parser.beacons != [TOKEN]:
        errors.append(f"{page.name}: analytics beacons {parser.beacons}, expected exactly [{TOKEN!r}]")
    canonicals[page] = parser.canonical
    og_urls[page] = parser.og_url
    for ref in parser.refs:
        u = urlsplit(ref)
        own = ref.startswith(ORIGIN)  # absolute links to this site are checked like relative ones
        if (u.scheme or u.netloc or ref.startswith(("#", "mailto:", "data:"))) and not own:
            continue
        path = unquote(u.path)
        target = (SITE / path.lstrip("/")) if path.startswith("/") else (page.parent / path)
        if target.is_dir():
            target = target / "index.html"
        if not target.resolve().is_relative_to(SITE):
            errors.append(f"{page.relative_to(SITE)}: {ref} points outside site/")
        elif not target.exists():
            errors.append(f"{page.relative_to(SITE)}: broken link {ref}")

# The exported game page is opened on its own too ("Open it on its own page"); update_game.sh tags it.
game = Refs()
game.feed((SITE / "game" / "index.html").read_text(encoding="utf-8"))
if game.beacons != [TOKEN]:
    errors.append(f"game/index.html: analytics beacons {game.beacons}, expected exactly [{TOKEN!r}] (run tools/update_game.sh)")


def url_of(page):
    # The URL each page is known by: the sitemap entry and the page's canonical link must both be this.
    return ORIGIN + ("" if page.name == "index.html" else page.name)


NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
try:
    root = ET.parse(SITE / "sitemap.xml").getroot()
except ET.ParseError as e:
    errors.append(f"sitemap.xml: {e}")
    root = ET.Element(NS + "urlset")
if root.tag != NS + "urlset":
    errors.append(f"sitemap.xml: root is {root.tag}, not a sitemaps.org <urlset>")
for page, c in canonicals.items():
    if c != [url_of(page)]:
        errors.append(f"{page.name}: canonical is {c}, expected [{url_of(page)!r}]")
    if og_urls[page] != [url_of(page)]:
        errors.append(f"{page.name}: og:url is {og_urls[page]}, expected [{url_of(page)!r}]")

listed = [(loc.text or "").strip() for loc in root.iter(NS + "loc")]
errors += [f"sitemap.xml: {u} listed twice" for u in sorted({u for u in listed if listed.count(u) > 1})]
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
