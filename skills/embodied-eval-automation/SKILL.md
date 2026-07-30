---
name: embodied-eval-automation
description: Plan, build, run, monitor, validate, transfer, and audit reproducible batch episode collection for policy, VLA, world-model, or hybrid models on embodied benchmarks and simulators. Use when a user provides or wants to connect a local/SSH/cloud GPU host, reuse existing model or benchmark assets, obtain GitHub or Hugging Face resources, compare native and unified episode formats, create adapters and validators, stage single-request through batch runs, recover interrupted jobs, manage disk and GPU limits, or deliver auditable episode datasets and reports.
---

# Embodied Eval Automation

Treat every run as a resumable, evidence-backed state machine. Do not equate a live process, installed environment, or successful import with completed episode collection. The user-approved scope, not a full benchmark by default, defines completion.

## Start with safe intake

1. Read applicable repository instructions and existing task records.
2. Confirm the local workspace, remote data root, expected output destination, and whether either location already contains relevant assets.
   - Never treat the skill installation directory, plugin repository, current working directory, home directory, or filesystem root as an approved run workspace.
   - If the user does not know where data should live, perform only approved read-only capacity discovery, propose one or two bounded code/data layouts with tradeoffs, and wait for workspace approval before writing.
3. Ask only for missing facts needed to continue. Never ask the user to paste a password, token, private key, recovery code, or session cookie into chat.
4. Separate permissions for:
   - read-only inspection;
   - local or remote writes;
   - package installation and downloads;
   - uploads or external transfers;
   - paid compute or added concurrency;
   - deletion or retention changes;
   - Git commits, pushes, or pull requests;
   - external notifications or messages.
5. Record approved actions, paths, hosts, time/scope boundaries, pause thresholds, and forbidden actions in an approval receipt.

Read [onboarding-and-permissions.md](references/onboarding-and-permissions.md) for the intake questions and approval matrix. Read [provider-connections.md](references/provider-connections.md) before configuring SSH, cloud access, GitHub, or Hugging Face.

## Establish the run contract

Before installation or downloads, freeze:

- model family and role: policy, VLA, world model, world-action model, or combination;
- benchmark/simulator and online closed-loop versus offline mode;
- repository commits, checkpoint revisions, dataset versions, and artifact hashes;
- suite/task/init-state/seed/repetition set and deterministic episode ID rule;
- observation, action, reward, termination, success, prediction, and video requirements;
- local/remote disk budgets, GPU allocation, cost ceiling, and pause thresholds;
- output representations, validators, visualizations, transfer, retention, and completion criteria.

Copy the templates in `assets/templates/` into the approved run workspace and fill them with evidence. Use `scripts/create_run_workspace.py` only after the workspace write boundary is approved.

## Follow the G0-G9 gates

Do not expand scale while the previous gate is incomplete.

### G0 - Access, host, and asset preflight

- Establish a safe connection method and verify host identity.
- Inspect OS, GPU, driver, memory, disk, network, ports, containers, and render capability.
- Inventory existing benchmark repositories, model repositories, environments, checkpoints, datasets, caches, adapters, and prior runs read-only.
- Record purpose, size, version evidence, active-process status, and potential reuse. A matching directory name is not reuse evidence.
- Stop before install, download, upload, deletion, or paid-compute changes.

### G1 - Official understanding, source lock, and reuse decision

- Read primary official documentation and pin source/artifact versions.
- Produce a user-facing technical report:
  - benchmark capabilities, task/data scale, reset/step/success workflow, observations supplied, and actions/results consumed;
  - model principle, inputs, internal inference/generation process, native outputs, limitations, licenses, and changes needed for comparable episode data.
- Compare every official requirement with the G0 inventory.
- Classify assets as `reuse`, `reuse-readonly`, `rebuild`, or `missing`, with evidence.
- Verify gated licenses and terms before downloading.

Read [asset-reuse-and-environments.md](references/asset-reuse-and-environments.md).

### G2 - Environment layout

- Reuse a verified benchmark environment read-only and freeze its fingerprint.
- Isolate model and benchmark dependencies by default.
- Connect them through a loopback protocol such as HTTP, WebSocket, or RPC on `127.0.0.1`.
- Never modify an existing working environment merely to save setup time.

### G3 - Missing resource acquisition

- Acquire only resources classified `rebuild` or `missing`.
- Prefer the official source, fixed revision, resumable partial files, and hash verification.
- Benchmark transfer speed before changing route.
- Escalate from remote direct download to mirror to user-controlled local download/upload only within approved boundaries.

### G4 - Runtime validation

Verify imports, GPU backend, headless rendering, task enumeration, environment construction, `reset`, one safe `step`, model-service health, and schema compatibility. Capture structured results.

### G5 - One real model request

Use one genuine observation and obtain one valid native model response. Validate shapes, ranges, latency, units, normalization, and error handling. Do not call `env.step` unless G5 explicitly includes that permission.

### G6 - One closed-loop episode and three representations

Before the first full episode, design the field mapping and loss analysis for:

1. `official-native`: official benchmark/model artifacts without deleting model-specific outputs;
2. `embodied-eval-current`: the currently approved comparable representation;
3. `embodied-eval-candidate`: an extension that retains current comparable fields and exposes new model-native capabilities.

Generate all three from the same real rollout. Share a `rollout_id`, task identity, initial-state fingerprint, and environment-fact hashes; use distinct `representation_id` values and manifests. Return all three plus a static side-by-side visualization and a source/transform/missing-field report.

Read [episode-representations.md](references/episode-representations.md) and [adapter-contract.md](references/adapter-contract.md).

### G7 - Pilot, format decision, and medium batch

- Run a small pilot across multiple tasks and initial states.
- Validate schema, same-rollout derivation, expected IDs, duplicates, pairing, initial-state fingerprints, and conversion loss.
- Report whether the candidate format, model-specific converter, and shared validator should be adopted.
- Wait for explicit user approval before promoting the candidate to current or entering a medium batch.
- Expand one experimental dimension at a time: task/init, then seed, then suite, unless the run contract justifies otherwise.

For paired comparisons, enforce:

```text
pair_key=<benchmark>/<suite>/task=<task_id>/init=<init_state_id>/seed=<seed>
```

The key excludes model identity. Require equal initial-state fingerprints across models, `T+1` observations for `T` transitions, every real model call in `policy_queries`, complete raw action chunks, and separately stored executed actions.

### G8 - Approved scale

- Freeze the expected episode/pair ID set before launch.
- Use a remote supervisor/worker that survives SSH disconnects.
- Use an independent controller for transfer, local validation, acknowledgements, and notifications.
- When the product supports recurring automation, create a periodic checker that stays silent during normal progress, reports anomalies or complete evidence, and pauses itself after completion.
- State honestly whether the remote worker, local controller, and periodic checker are alive. A chat response is not continuous monitoring.
- Pause before crossing approved disk, GPU, cost, or scope boundaries.

Read [monitoring-transfer-retention.md](references/monitoring-transfer-retention.md).

### G9 - Audit and delivery

- Rebuild the global index from episode summaries and lifecycle records.
- Compare expected versus actual IDs; report missing, duplicate, corrupt, failed, and excluded items.
- Verify hashes, schema versions, representation lineage, pair identities, initial states, transitions, policy queries, and videos.
- Deliver manifests, commands, environment fingerprints, reports, static visualizations, failure lists, and a reproducibility package.
- Scan the delivery for secrets, private hosts, personal paths, restricted assets, and unsupported claims.

## Implement the adapters

Each new model + benchmark integration must provide:

- model adapter: start, health, observation transform, infer, native response, action schema, stop;
- benchmark adapter: enumerate, construct, reset, step, close, observation/action schemas, success;
- episode writer: atomic writes, native/current/candidate derivation, summaries, hashes, lineage;
- run controller: expected IDs, progress, heartbeat, resume, audit, transfer;
- resource manifest: repository, checkpoint, dataset, tokenizer, environment, and large binary provenance.

Never fabricate unsupported fields. Use capability flags for unsupported model outputs and quality flags for incomplete or degraded collection.

## Protect transfers and deletion

Write archives to partial names, verify size and SHA256 at both ends, inspect archive members, validate the scope, and then atomically finalize. Remote pruning requires all of:

- locally verified immutable copy;
- matching remote/local hash;
- readable archive and complete scope audit;
- target resolved inside the approved run root;
- explicit cleanup authorization;
- durable `locally_verified` and `remote_pruned` receipts.

Read [security-and-approvals.md](references/security-and-approvals.md) before any high-impact action.

## Use bundled scripts

- `scripts/create_run_workspace.py`: create a minimal run workspace and run contract after write approval.
- `scripts/validate_run_contract.py`: validate the run contract and reject secret-like keys.
- `scripts/validate_repository.py`: validate this distributed skill/plugin package.

Run scripts with `--help` before use. Do not edit user data merely to make validation pass.

## Stop and ask

Stop before proceeding when:

- connection identity or workspace boundary is unclear;
- official source, checkpoint license, or required revision is unresolved;
- a requested action needs an unapproved permission category;
- a credential would have to be exposed;
- disk/GPU/cost crosses the approved threshold;
- G5, G6, or G7 evidence fails;
- monitoring is absent for a long batch;
- transfer or deletion preconditions are incomplete;
- the user changes or terminates scope.

## Completion standard

Complete only when the approved expected set equals the audited delivered set, permitted failures are documented, manifests and hashes resolve, representations and pairings validate, static outputs open independently, and another operator can reproduce or resume the run without relying on chat history.
