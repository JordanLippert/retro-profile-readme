# Agent notes

Tests: `python -m unittest discover -s tests` (needs pyfiglet). The seam is the build CLI: a
`profile.json` in, `README.md` and SVGs out.

## Agent skills

### Issue tracker

Local markdown under `.scratch/<feature-slug>/`. See `docs/agents/issue-tracker.md`.

### Triage labels

Default vocabulary, recorded as a `Status:` line. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: `CONTEXT.md` and `docs/adr/` at the root, created lazily. See `docs/agents/domain.md`.
