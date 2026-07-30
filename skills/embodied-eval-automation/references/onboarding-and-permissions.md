# Onboarding and permission intake

Use this reference at G0 or whenever the user changes hosts, workspaces, providers, or scope.

## Ask in small groups

Do not dump every question at once. Start with the smallest blocking set and infer safe facts from existing configuration when possible.

### Task identity

- Which model/checkpoint and benchmark/simulator?
- Online closed-loop, offline conversion, or both?
- What suite/task/init-state/seed/repetition set is desired?
- What must each episode contain?
- Is a full run required, or is a pilot/approved partial scope sufficient?

### Workspace

- What local project root should contain code, manifests, reports, and transferred data?
- What remote data root may be written?
- Are there paths that must remain read-only or untouched?
- Where should large downloads, caches, checkpoints, and episodes live?
- What free-space threshold should warn, pause, and stop the run?

Before writing, resolve the absolute paths, confirm they are not a home/system/root directory, inspect existing contents, and state exactly which new directories will be created.

Do not infer the run workspace from the skill/plugin installation path or the agent's current working directory. When the user is unsure:

1. ask where code and large data are normally stored;
2. use approved read-only checks to compare candidate volumes;
3. propose a bounded code root and a separate large-data root when useful;
4. explain free space, portability, backup, and cleanup tradeoffs;
5. wait for explicit path approval before creating anything.

### Connection

- Is there an existing shell or provider connector?
- If SSH, what is the redacted command containing user, host, and port?
- Is authentication password-interactive, SSH key, SSH agent, certificate, or provider identity?
- How will the user verify the first host fingerprint?
- Must the workflow survive disconnects?

Never request a password or private-key body. If the user has only a password, ask them to type it directly into an interactive terminal. For unattended operation, ask whether a dedicated key may be created and whether its public key may be added to the server.

### External sources

- Are repository and model resources public, private, or gated?
- Is GitHub access read-only, or will branches/issues/releases be written?
- Is Hugging Face access read-only, and has the user personally accepted any gated license?
- Which cache/download directory is approved?

### Compute and retention

- Which GPU IDs and concurrency are allowed?
- What time/cost budget is approved?
- What may be transferred, retained, compressed, or removed?
- May the controller prune only verified scope data, or must all remote data remain?
- Where should completion/anomaly notifications go?

## Permission matrix

Record `approved`, `denied`, or `not_requested` for each category:

| Category | Examples | Default |
|---|---|---|
| Read inspection | list files, versions, disk/GPU, process status | ask once for named hosts/roots |
| Workspace writes | create run directories, manifests, adapters | ask with exact roots |
| Installation | packages, drivers, containers, environment changes | separate approval |
| Download | repositories, wheels, checkpoints, datasets | separate approval |
| Upload/transfer | local-to-server, object storage, dataset publication | separate approval |
| Paid compute | new instance, extra GPU, concurrency, longer reservation | separate approval |
| Permission change | `authorized_keys`, IAM, ACL, chmod/chown | separate approval |
| Deletion | caches, partial downloads, verified remote scopes | separate approval |
| Git write | commit, push, PR, release | separate approval |
| External message | email, webhook, Slack/Teams/Feishu | separate approval |

Approval expires when its run, host, path, action category, or time boundary changes.

## Approval receipt

Use a structured receipt:

```json
{
  "approval_id": "approval-...",
  "run_id": "...",
  "approved_at": "...",
  "category": "read|write|install|download|upload|compute|permission|delete|git|notify",
  "targets": ["host/path/resource"],
  "allowed_actions": ["..."],
  "forbidden_actions": ["..."],
  "expires_when": "stage complete or explicit timestamp",
  "evidence": "user message or operator record"
}
```

Do not put secrets or full private host details in a public deliverable.

## Minimum G0 handoff

G0 is ready only when it has:

- confirmed local/remote roots;
- connection method and host verification plan;
- permission matrix;
- host capability summary;
- asset inventory;
- disk/GPU/cost thresholds;
- unresolved blockers and next approval required.
