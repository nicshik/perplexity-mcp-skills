# Changelog

All notable changes to this repository should be documented in this file.

## Unreleased

_No unreleased changes._

## 0.2.0 — 2026-05-10

- Added an npm/npx CLI installer with `install`, `doctor`, `sync`, and `uninstall` commands for Codex, Windsurf, Cursor, Claude Code, and all-target setup.
- Added TypeScript packaging, npm package validation, release notes, and a GitHub Actions release workflow for npm Trusted Publishing.
- Updated English and Russian quick starts to make `npx perplexity-mcp-skills ...` the primary install path while keeping shell installers as legacy clone-based fallbacks.
- Added repository-level support artifacts for Cursor, Claude Code, and Antigravity-style AGENTS workflows.
- Added `.cursor/mcp.json`, `.cursor/rules/perplexity.mdc`, `.mcp.json`, `.claude/skills/`, and `AGENTS.md`.
- Expanded README and repository checks to cover Cursor, Claude Code, and Antigravity guidance.
- Productized repository docs for Codex and Windsurf with a clearer first screen, compatibility matrix, troubleshooting, and job-to-be-done examples.
- Added offline-safe smoke verification via `scripts/check.sh`.
- Added GitHub Actions CI for compile and smoke checks.
- Added contribution guidance and lightweight repository consistency checks.
