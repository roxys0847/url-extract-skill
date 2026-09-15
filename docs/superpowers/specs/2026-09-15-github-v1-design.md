# URL-Extract Skill GitHub V1.0 Design

## Goal

Publish a private GitHub repository named `url-extract-skill` and a Windows-only
V1.0 release. The repository must explain how the Codex skill helps an AI obtain
the audio and visual material behind supported public links, and how the
standalone Python file parses and downloads that material.

## Repository contents

- Chinese `README.md` as the default landing page.
- English `README_EN.md`, cross-linked from the Chinese page.
- A portable `skill/url-extract` package with no user-specific absolute paths.
- The reviewed Windows single-file downloader in `dist/` and in the skill's
  `scripts/` directory.
- Release notes for `URL-Extract for Windows V1.0`.
- No macOS build, virtual environment, browser profile, cookies, downloaded
  media, caches, or local project files.

## Release

- Repository: `roxys0847/url-extract-skill`.
- Visibility: private.
- License: none for V1.0.
- Tag: `v1.0`.
- Release title: `URL-Extract for Windows V1.0`.
- Release asset: `url-extract for Windows.py` only.

## Documentation requirements

Both languages describe supported platforms, AI-assisted audio/visual reading,
manual Skill installation, Release download, Python 3.11+ usage, automatic and
fixed-version dependencies, first-run restart behavior, output locations,
environment checks, network/proxy troubleshooting, and public/authorized-use
boundaries.

## Verification

Before publishing, compile and self-test both tracked copies, compare their
SHA-256 hashes, validate Skill metadata, scan for secrets and user-specific
paths, and confirm the GitHub release exposes only the Windows Python asset.

