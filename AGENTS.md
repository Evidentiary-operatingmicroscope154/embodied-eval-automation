# Repository agent guidance

This repository contains a public, provider-neutral Agent Skill and skills-only Codex plugin.

## Rules

- Keep the installable skill under `skills/embodied-eval-automation/`.
- Keep `SKILL.md` concise and link every detailed reference directly from it.
- Never commit credentials, private hosts, institutional identifiers, model weights, datasets, generated episodes, videos, caches, or run logs.
- Use standard-library Python for bundled validation scripts unless a dependency is essential and documented.
- Treat installation, upload, paid compute, permission changes, deletion, Git writes, and external messaging as separate approval boundaries.
- Do not hardcode a user’s operating system, drive letter, home path, server provider, model, or benchmark.
- Record newly added repository files in `log/file_description.md`.
- Run the repository validator and unit tests before handoff.
