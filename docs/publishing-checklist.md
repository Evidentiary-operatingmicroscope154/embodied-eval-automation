# Publishing and release checklist

## Before the first public push

- [ ] Replace the generic contributor identity only if the owner wants personal or organization attribution.
- [ ] Confirm the repository name and default branch.
- [ ] Review `LICENSE`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, and `CONTRIBUTING.md`.
- [ ] Enable private vulnerability reporting.
- [ ] Enable Discussions if community questions should be separate from issues.
- [ ] Run validation and tests on Windows and Linux.
- [ ] Confirm the repository contains no private hostnames, local user paths, credentials, episode data, model weights, or restricted documentation.
- [ ] Create a clean local Git history and signed or verified release tag if available.

## Suggested repository metadata

Description:

> A permission-aware Agent Skill for reproducible, auditable batch episode collection across VLA, policy, world-model, and embodied benchmark workflows.

Suggested topics:

```text
agent-skills
codex
embodied-ai
robotics
robot-learning
vla
world-model
benchmark
evaluation
dataset
automation
reproducibility
```

Topics should be lowercase and hyphenated. Keep the final set focused rather than using every possible term.

## First release

1. Set the plugin and changelog version to the same semantic version.
2. Run:

   ```bash
   python skills/embodied-eval-automation/scripts/validate_repository.py .
   python -m unittest discover -s tests -v
   ```

3. Forward-test activation, incomplete-input handling, negative activation, and approval boundaries.
4. Tag `v0.1.0`.
5. Create release notes from `CHANGELOG.md`.
6. Attach no model weights, datasets, or generated episode archives.

## Codex plugin publication

The repository is a skills-only plugin and includes `.codex-plugin/plugin.json`. Before submission:

- validate the plugin manifest with the current `plugin-creator`;
- install from a local marketplace and test in a new conversation;
- verify all bundled references resolve after installation;
- verify the starter prompts match workflows the skill can complete;
- follow the current OpenAI plugin submission documentation, because the directory process may change.

## Discoverability

- Keep the README opening outcome-oriented.
- Add a repository social preview derived from `assets/hero.svg`.
- Publish small, redacted example reports rather than private run artifacts.
- Label beginner-friendly issues with `good first issue`.
- Respond to reproducible bug reports with evidence and a bounded fix.
