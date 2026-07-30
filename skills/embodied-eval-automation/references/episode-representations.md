# Episode representations and schema evolution

## One rollout, three views

Use one real closed-loop rollout as the atomic source:

### `official-native`

Preserve official benchmark writer output and complete model-native responses. Do not drop future predictions, values, action distributions, latent candidates, or model-specific diagnostics merely because a shared schema lacks them.

### `embodied-eval-current`

Atomically derive the currently approved cross-model representation from the rollout source. It is the comparison truth for the current study.

### `embodied-eval-candidate`

Retain current comparable fields and add typed structures for newly observed model capabilities. Mark it candidate until the pilot report and explicit user approval promote it.

All three share:

- `rollout_id`;
- benchmark/suite/task/init/seed/repetition identity;
- initial-state fingerprint;
- environment fact hashes;
- source lineage.

They use different `representation_id` values, manifests, paths, and validation results.

## Field provenance

Label fields as:

- `benchmark_observed`: actual environment observation, reward, done, success;
- `model_native`: unmodified model output;
- `adapter_computed`: deterministic transform or statistic;
- `unsupported`: capability absent from the model or benchmark.

Use capability flags for unsupported outputs. Use quality flags when an expected item is missing, degraded, or reconstructed from legacy data.

Never:

- substitute predicted observations for actual environment observations;
- copy adjacent frames to fill a missing frame;
- truncate a raw action chunk and present it as the full model response;
- invent a value/reward/confidence field;
- rewrite native output to resemble another model.

## Paired comparison invariants

For `T` executed environment transitions:

- observations contain the reset observation plus every post-action observation: length `T+1`;
- actions, rewards, done, and success have length `T`;
- `policy_queries` has length `Q`, the number of real model calls.

Each query records:

- query/step index and timing;
- input references or hashes;
- complete `action_chunk_raw`;
- raw valid mask/length;
- executed prefix length or mask;
- model-native predictions, values, confidence, or diagnostics;
- request/response hashes and error state.

`transitions/action_executed` contains only actions actually sent to the environment.

Use:

```text
pair_key=<benchmark>/<suite>/task=<task_id>/init=<init_state_id>/seed=<seed>
```

Different models are comparable only when pair key, initial-state fingerprint, and required environment facts match.

## Candidate format decision

At G6, produce:

- field-difference matrix;
- provenance map;
- converter and validator requirements;
- unsupported/missing fields;
- storage and migration cost;
- static side-by-side visualization.

At G7, measure:

- conversion loss;
- current/candidate same-rollout equality for shared facts;
- model-specific field coverage;
- pair coverage and initial-state equality;
- downstream impact.

Promote the candidate only after explicit user approval. Preserve rejected candidate evidence without changing the current standard.

## Storage guidance

- Keep summaries and indexes in JSON/JSONL.
- Use array or dataset-oriented chunk formats for large tensors.
- Store videos and images as referenced artifacts with hashes.
- Write to a temporary directory, close/fsync as appropriate, create the summary, then atomically rename.
- Every representation manifest names its schema version, source rollout, derived-from chain, file list, sizes, and hashes.
