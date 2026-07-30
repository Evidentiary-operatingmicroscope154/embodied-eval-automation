# Model, benchmark, and episode adapter contract

## Model adapter

Provide:

- `start(config, checkpoint)`;
- `health()` including model identity and lightweight request;
- `transform_observation(observation)`;
- `infer(request)` returning native response plus normalized action view;
- `action_schema()` with dimensions, units, bounds, timestep, normalization;
- `capabilities()` for actions, futures, values, rewards, confidence, video, latents;
- `stop()` scoped to the current run.

Preserve the complete native response before deriving shared fields.

## Benchmark adapter

Provide:

- suite/task/init-state/seed enumeration;
- environment construction and headless rendering;
- `reset`, `step`, `close`;
- observation and action schemas;
- reward, termination, truncation, and success semantics;
- deterministic expected ID and initial-state fingerprint;
- benchmark-native episode writer integration when available.

## Loopback service

Version the request/response protocol. Include:

- request ID and timestamp;
- model/checkpoint identity;
- observation schema version;
- image/state/language/history references;
- native response;
- normalized action view;
- timing and structured errors.

Bind to `127.0.0.1` by default. Do not expose an inference port publicly without an explicit network and authentication design.

## Episode writer

Write:

- rollout identity and configuration;
- atomic environment facts and all model queries;
- official-native artifacts;
- current and candidate representations;
- per-file size/hash and lineage;
- episode summary and validation result.

Partial episodes must not appear complete. Use temporary paths and atomic finalization.

## Run controller

Provide:

- expected episode/pair IDs;
- progress and heartbeat;
- lifecycle ledger;
- resume from ledger;
- scope closure and packaging;
- transfer and local verification acknowledgements;
- final index and audit.

## Minimum episode summary

```json
{
  "episode_id": "...",
  "rollout_id": "...",
  "representation_id": "...",
  "pair_key": "...",
  "model": {"name": "...", "revision": "..."},
  "benchmark": {"name": "...", "revision": "..."},
  "task": {"suite": "...", "task_id": "...", "init_state_id": "...", "seed": 0},
  "initial_state_sha256": "...",
  "transition_count": 0,
  "observation_count": 1,
  "policy_query_count": 0,
  "success": false,
  "termination_reason": "...",
  "schema_version": "...",
  "files": [],
  "quality_flags": []
}
```

## Validator requirements

Validate:

- schema and array lengths;
- value shapes, units, bounds, NaN/Inf policy;
- native/current/candidate lineage;
- expected IDs and duplicate IDs;
- pair keys and initial-state fingerprints;
- transition/query invariants;
- file sizes and hashes;
- capability and quality flags;
- no predicted-as-observed or raw-as-executed substitution.
