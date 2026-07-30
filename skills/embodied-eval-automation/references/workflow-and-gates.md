# Workflow gates and evidence

| Gate | Minimum action | Passing evidence | On failure |
|---|---|---|---|
| G0 | access, host check, read-only asset inventory | host preflight, asset inventory, approval receipt | do not install/download/delete |
| G1 | pin sources, explain systems, decide reuse | source/artifact manifests, technical report, reuse matrix | do not build environments |
| G2 | isolate and fingerprint environments | interpreter/lock/fingerprint and loopback contract | resolve boundary conflicts |
| G3 | acquire only missing/rebuild assets | size/hash/revision verified | change transfer route, not identity |
| G4 | runtime and render smoke test | structured runtime report | targeted repair |
| G5 | one observation → one model response | native response, shape/range/latency validation | fix service/adapter |
| G6 | one real closed-loop rollout | three manifests, lineage validation, static comparison | do not batch |
| G7 | pilot and schema decision | schema/pair/expected-ID audit and user approval | revise collector/schema |
| G8 | approved batch | supervisor, controller, heartbeat, ledger, thresholds | pause/recover/request approval |
| G9 | audit and delivery | expected=delivered or documented exclusions | produce missing/corrupt rerun list |

## Scale gates

- A single request validates model service semantics, not environment dynamics.
- One episode validates closed-loop interaction, not batch stability.
- A pilot spans multiple tasks and initial states.
- A medium batch measures speed, failure rate, disk growth, transfer overhead, and service stability.
- An approved large run uses evidence-derived scope sizes and thresholds.

Do not change task/init, seed, suite, concurrency, and schema simultaneously unless a written design makes the effects distinguishable.

## Technical report at G1

Explain the benchmark:

- purpose, supported robots/tasks, online/offline modes, task/data scale;
- construction, reset, observation, step, reward, termination, success;
- action dimensions, units, bounds, control frequency, and rendering;
- what it sends to the model and consumes from the model.

Explain the model:

- policy/VLA/world-model role and core algorithm at an appropriate level;
- language, image, state, history, action, noise, or latent inputs;
- preprocessing, inference/generation loop, chunking or horizon;
- native actions, future observations, videos, values, rewards, confidence, or latent outputs;
- default logging and official episode artifacts;
- license, checkpoint dependencies, hardware needs, and limitations;
- extra collection needed for a comparable schema without suppressing native outputs.

Distinguish official facts, inspected implementation facts, and inference.

## Expected IDs

Generate the expected ID set before G7/G8. Each identity should include:

- benchmark and version;
- suite/task/init-state/seed/repetition;
- model/checkpoint identity;
- rollout and representation identity.

The paired `pair_key` excludes model identity. Audit expected versus actual using summaries and the lifecycle ledger, not only directories that still exist remotely.

## Completion gate

The run is complete only when:

- approved expected count and delivered count reconcile;
- missing, duplicate, corrupt, failed, and excluded IDs are explicit;
- source/artifact manifests and hashes resolve;
- native/current/candidate lineage validates;
- paired initial states and environment facts match;
- transfers and permitted pruning have receipts;
- reports and static visualizations open independently;
- resume and reproduction instructions are present.
