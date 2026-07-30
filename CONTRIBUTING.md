# Contributing

Thank you for helping make embodied evaluation more reproducible.

## Good contributions

- provider-neutral SSH or cloud access patterns;
- new model/benchmark adapter contracts;
- episode schema validators and conversion-loss checks;
- monitoring, transfer, and recovery playbooks;
- security improvements and secret-leak prevention;
- realistic activation and boundary tests.

Do not contribute model weights, private datasets, credentials, proprietary infrastructure details, or files whose license does not permit redistribution.

## Development setup

Python 3.10 or newer is recommended. Runtime validation uses only the standard library.

```bash
python skills/embodied-eval-automation/scripts/validate_repository.py .
python -m unittest discover -s tests -v
```

## Pull requests

1. Explain the user scenario and failure mode.
2. Keep `SKILL.md` concise; place detailed material in one-level-deep references.
3. Add or update a forward-test prompt when behavior changes.
4. Run repository validation and tests.
5. Confirm that examples contain no secrets or private paths.
6. Update `CHANGELOG.md` under **Unreleased**.

## Commit scope

Keep changes focused. Do not include generated episodes, checkpoints, archives, videos, caches, virtual environments, or terminal logs.

## Language

The primary skill and README are English for portability. Chinese documentation may be updated in parallel. Other translations are welcome when maintainers can review them.
