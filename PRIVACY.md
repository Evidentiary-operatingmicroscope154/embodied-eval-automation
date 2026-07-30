# Privacy

## Project behavior

This repository contains instructions, templates, and local standard-library scripts. It has no hosted service, telemetry, analytics, account system, or automatic data upload.

## Data processed during use

When an agent applies the skill, it may process information selected by the user, including:

- local and remote paths;
- server capability and process metadata;
- repository and checkpoint identifiers;
- benchmark observations, actions, rewards, success labels, predictions, and videos;
- manifests, hashes, logs, and validation reports.

Where that data is stored depends on the user-approved workspace and tools. The project itself does not receive it.

## Third-party services

GitHub, Hugging Face, cloud providers, model registries, notification services, and benchmark/model repositories have their own privacy and retention policies. Use the smallest required access scope and review those policies before authentication or upload.

## User responsibilities

Before collecting or publishing episodes, confirm:

- authority to use the server, model, benchmark, and data;
- applicable licenses, research/organizational policy, and privacy requirements;
- whether observations contain people, private environments, confidential text, or identifying metadata;
- a retention, redaction, and deletion policy.

Do not publish raw run artifacts merely because schema validation passes.
