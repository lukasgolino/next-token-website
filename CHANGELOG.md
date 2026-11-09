# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.0] - 2026-11-09

### Added

- Umami analytics alongside Cloudflare Web Analytics: cookieless, so still no consent banner, and it adds
  per-visit page journeys (entry page, pages in order, exit), which Cloudflare's aggregate counts can't show.
  All our sites share one Umami website; the Host filter separates them.

## [0.2.0] - 2026-11-06

### Added

- A standard icon set: `favicon.ico` (16/32/48 px), a 96 px icon, a 180 px apple-touch icon and `site.webmanifest`
  with 192/512 px and maskable icons, so search results, tabs, bookmarks and home-screen shortcuts all show the
  icon ([#10](https://github.com/lukasgolino/next-token-website/issues/10)).
- schema.org structured data (JSON-LD) on the home page, an `llms.txt` summary for AI assistants, and robots.txt
  content signals allowing search and AI use; the home page title names what the site is for
  ([#11](https://github.com/lukasgolino/next-token-website/issues/11)).

### Changed

- CI checks are cheap, so they run on every push (and on demand).
  Deploys skip pushes that only touch the changelog, README or CI-only workflows.

## [0.1.0] - 2026-11-05

### Added

- Cloudflare Web Analytics beacon on every page and on the standalone game page (cookieless; `update_game.sh`
  re-tags the game after each export). `check_site.py` checks each loads it exactly once
  ([#4](https://github.com/lukasgolino/next-token-website/issues/4)).
- Canonical links and `og:url` on every page; `og:image` is now absolute. `check_site.py` checks that each page's
  canonical matches its sitemap URL ([#3](https://github.com/lukasgolino/next-token-website/issues/3)).
- `sitemap.xml` and `robots.txt`; `check_site.py` checks that the sitemap lists exactly the pages
  ([#2](https://github.com/lukasgolino/next-token-website/issues/2)).
- CHANGELOG.md, a check workflow (`tools/check_site.py`: local links resolve inside site/) on pushes to main and
  every PR, and a release workflow that publishes a GitHub release for each `vX.Y.Z` tag, with that version's
  CHANGELOG section as the notes ([#5](https://github.com/lukasgolino/next-token-website/issues/5)).

[Unreleased]: https://github.com/lukasgolino/next-token-website/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/lukasgolino/next-token-website/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/lukasgolino/next-token-website/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/lukasgolino/next-token-website/releases/tag/v0.1.0
