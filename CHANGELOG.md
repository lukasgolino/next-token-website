# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- CHANGELOG.md, a check workflow (`tools/check_site.py`: pages parse, local links resolve) on pushes to main and
  every PR, and a release workflow that publishes a GitHub release for each `vX.Y.Z` tag, with that version's
  CHANGELOG section as the notes ([#5](https://github.com/lukasgolino/next-token-website/issues/5)).
