# Asset reuse and environment layout

## G0 inventory

Inventory these candidates read-only:

- benchmark/simulator source, task definitions, assets, datasets, and environments;
- model source, service scripts, configs, tokenizer, normalizers, and environments;
- checkpoints, base models, caches, archives, wheels, containers, and prior runs;
- adapters, schema validators, visualization tools, and run controllers.

For each candidate record:

```json
{
  "kind": "benchmark_env|model_repo|checkpoint|dataset|cache|adapter|run",
  "path": "...",
  "size_bytes": 0,
  "purpose": "...",
  "version_evidence": {"commit": "...", "revision": "...", "sha256": "..."},
  "active_process": false,
  "evidence_level": "name_only|metadata|runtime_verified|hash_verified",
  "candidate_for_reuse": true,
  "cleanup_recommendation": "keep|review|safe_after_approval"
}
```

Do not hash every large file blindly. Start with metadata, then hash only reuse candidates and required artifacts.

## G1 reuse matrix

Classify every requirement:

- `reuse`: verified and safe to consume;
- `reuse-readonly`: verified but must not be modified;
- `rebuild`: present but incompatible, incomplete, or contaminated;
- `missing`: no adequate candidate exists.

Require evidence such as:

- source commit or immutable archive hash;
- interpreter and environment lock/fingerprint;
- package versions;
- checkpoint revision, size, and hash;
- benchmark task enumeration, headless render, reset/step smoke test;
- action/observation schema compatibility;
- before/after environment fingerprint.

A directory name, symlink, cache hit, or import alone is insufficient.

## Environment policy

- Keep the benchmark client and model service isolated by default.
- Reuse a verified benchmark environment without modifying it.
- Create a separate model environment when Python, Torch/JAX, CUDA, MuJoCo, or rendering dependencies differ.
- Connect environments through `127.0.0.1` with a versioned protocol.
- Separate source, environment, vendor wheels, checkpoints, caches, run data, and temporary files.
- Put large assets on an approved data volume.

## Resource acquisition

- Acquire only `rebuild` and `missing` items.
- Keep fixed commits/revisions; if `git clone` is unreliable, use an archive for the same commit.
- Derive large wheel URLs, versions, sizes, and hashes from the lock file when possible.
- Download to `.part`/`.partial`, validate, then atomically rename.
- Do not run concurrent installers against the same environment or cache.

## Diagnosis order

Classify failures before retrying:

1. host capability: namespace, mount, GPU runtime, system restriction;
2. dependency resolution: Python version, ABI, lock conflict;
3. transfer: TLS, Git, package index, object storage;
4. resource: disk, RAM, VRAM;
5. runtime: headless render, model backend, protocol, schema.

Only transfer failures are likely to improve by changing mirrors. Never change dependency versions merely to make a download succeed.

## Reuse report

Explain to the user:

- what already exists and its size/purpose;
- what is safe to reuse and why;
- what must remain read-only;
- what is incompatible and why;
- what is missing and estimated download/storage cost;
- what can be cleaned later, only after approval.
