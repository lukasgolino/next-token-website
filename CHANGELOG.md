# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- CI checks run once per PR, when it's marked ready for review just before merge (and on demand), to save Actions
  minutes.
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

[Unreleased]: https://github.com/lukasgolino/next-token-website/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/lukasgolino/next-token-website/releases/tag/v0.1.0
