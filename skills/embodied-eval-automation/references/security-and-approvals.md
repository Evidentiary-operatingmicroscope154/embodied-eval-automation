# Security and approval boundaries

## Never persist secrets

Do not write passwords, private keys, access tokens, application passwords, webhook URLs, cookies, or recovery codes to:

- commands or shell history;
- Markdown, JSON, YAML, TOML, `.env`, or logs;
- Git remotes;
- episode metadata or reports;
- chat notifications.

Use interactive login, credential managers, SSH agents, provider CLIs, environment injection from a secret store, or managed connectors.

## Host identity

Verify an SSH host key through a trusted out-of-band source before unattended automation. Do not automatically accept a changed fingerprint. Record the fingerprint, not credentials.

## Separate approvals

Require exact targets and actions for:

- system/package installation;
- permission and IAM changes;
- browser/computer control;
- upload or publication;
- paid compute or concurrency changes;
- deletion or retention changes;
- Git commit/push/PR/release;
- external messages and webhooks.

A broad statement such as “continue” does not authorize a new high-impact category. A previous approval does not apply to a different run, host, root, provider, or time window.

## Browser and computer control

Before controlling a browser or desktop, state:

- applications and domains;
- local directories;
- clicks, inputs, downloads, uploads, or submissions;
- forbidden actions;
- stop condition.

Wait for explicit approval. Login, gated-license acceptance, file upload, deletion, payment, permission changes, and sensitive reads require renewed confirmation.

## Cloud and cost

- Inspect identity, instance, GPU, and current billing state read-only first.
- Do not provision, resize, extend reservations, expose ports, or modify firewall/IAM without approval.
- Keep the run within approved GPU IDs, concurrency, time, and cost.
- Pause when evidence cannot prove the boundary is still satisfied.

## Notification is not authorization

Email, webhook, chat, or mobile notification may report status. Do not treat a notification reply as destructive authorization unless an authenticated, signed, expiring approval protocol was deliberately designed.

## Public-delivery scan

Before Git push, release, or dataset publication, scan for:

- secrets and credential-shaped strings;
- private hostnames/IPs and local user paths;
- proprietary task names, images, language, or institutional identifiers;
- model weights, datasets, videos, archives, and caches;
- license notices and gated/restricted artifacts;
- claims not supported by manifests or reports.

## Incident response

If a secret appears:

1. stop output and external writes;
2. do not repeat the secret;
3. tell the user which credential type and location were exposed;
4. recommend revocation/rotation through the provider;
5. remove it only with authorization and preserve a redacted audit trail;
6. scan history and artifacts for additional copies.
