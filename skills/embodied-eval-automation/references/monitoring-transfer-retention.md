# Monitoring, transfer, and retention

## Three layers

1. **Remote supervisor/worker** keeps model service and collection alive and writes real-time heartbeat/state.
2. **Independent controller** checks remote state, transfers closed scopes, validates locally, acknowledges, and notifies.
3. **Periodic agent automation** wakes on a schedule, reconciles remote and local evidence, stays silent during healthy progress, reports anomalies/completion, then pauses itself.

The periodic checker is not real-time supervision. If it is absent, do not promise that chat will notify the user later.

## Required state

Remote:

- `progress.json`;
- heartbeat timestamp;
- supervisor/worker/model/collector status;
- append-only event or lifecycle ledger;
- scope-complete markers and package manifests;
- disk/GPU/process snapshots.

Local:

- controller process and progress;
- transferred archives and hashes;
- local validation reports;
- acknowledgements and cleanup receipts;
- final audit.

Update JSON atomically through a temporary file and replacement.

## Lifecycle

Use:

```text
planned -> running -> complete -> packaged -> transferred -> locally_verified -> remote_pruned
```

Resume from the ledger and expected IDs, not from the set of remote episode directories. Otherwise safely pruned episodes may be regenerated.

## Scope closure

Package only a closed task/suite/shard:

1. expected IDs frozen;
2. every episode atomically complete or explicitly failed;
3. scope audit reconciled;
4. `scope_complete` marker written;
5. no writer owns a path in the scope.

Packaging may run in parallel with collection of the next scope only when disk and I/O budgets allow.

## Disk thresholds

Derive thresholds from a medium-batch measurement and approve them with the user. Check both remote and local destinations.

Reserve at least:

- one maximum-scope archive;
- temporary packaging and transfer files;
- model/benchmark runtime cache;
- safety margin for the current episode.

At warning, prioritize transfer. At pause, do not start a new scope. At emergency, prevent expansion and finish only the safest bounded action.

## Transfer

- finalize remote package before transfer;
- use resumable `.part`/`.partial` destinations;
- compare remote/local size and SHA256;
- inspect archive paths to prevent traversal;
- validate episode summaries and expected IDs;
- atomically rename after verification;
- write `locally_verified` acknowledgement.

## Remote pruning

Prune only when:

- local immutable copy exists;
- hashes match;
- archive is readable;
- scope audit passes;
- target resolves inside the approved run root and is not the root itself;
- approval covers this run/scope/path;
- ledger already records `locally_verified`.

Write a `remote_pruned` receipt with targets, sizes, hashes, timestamp, and approval ID. Retain global manifests, ledgers, expected IDs, and final reports until the run is fully delivered.

## Automation anomaly conditions

Notify on:

- paused or failed state;
- stale heartbeat;
- unexpected process exit;
- stopped controller with unverified scopes;
- disk/GPU/cost boundary violation;
- unauthorized GPU/concurrency;
- transfer/hash/validation failure;
- local acknowledgement without matching approved prune receipt.

Completion notification requires the full completion gate, not merely `state=complete`.
