# Security policy

## Supported versions

Security fixes are applied to the latest tagged release and the default branch.

## Reporting a vulnerability

Do not include credentials, private infrastructure addresses, proprietary logs, or exploitable details in a public issue.

Before this repository is published, the maintainer should enable GitHub private vulnerability reporting. After publication, use the repository’s **Security → Report a vulnerability** flow. If that flow is unavailable, contact the maintainer through the private contact method listed on the maintainer’s GitHub profile.

Include:

- affected version and file;
- minimal reproduction with secrets removed;
- expected impact;
- suggested mitigation, if known.

## Credential handling

The skill must never request or persist:

- SSH passwords or private-key contents;
- GitHub, Hugging Face, cloud, webhook, or email tokens;
- session cookies, recovery codes, or password-manager data.

Authentication should happen in an interactive terminal, credential manager, SSH agent, provider CLI, or managed connector. Public keys, key fingerprints, account names, repository names, and non-secret resource identifiers may be recorded when needed.

## High-impact actions

Installations, uploads, paid compute, permission changes, deletion, Git writes, and external messages require separate, bounded user approval. A completion notification is not authorization for the next phase.

## Data handling

Generated episodes may contain images, language instructions, environment state, and metadata. Before public sharing:

- verify benchmark and model licenses;
- remove credentials, personal paths, private hosts, and institutional identifiers;
- confirm whether task observations contain personal or confidential content;
- document transforms and redactions in the artifact manifest.
