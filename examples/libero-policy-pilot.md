# Example: policy + LIBERO pilot

## User request

> Use `$embodied-eval-automation` to generate a small online closed-loop LIBERO pilot for my policy checkpoint on an existing GPU server. I have a redacted SSH command and password-interactive access. First check whether the server already has a compatible LIBERO environment and checkpoint cache. Do not ask me to paste the password. Do not modify the existing benchmark environment. Stop after one request, one episode with three representations, and a 10-pair pilot report.

## Expected skill behavior

1. Confirm local/remote roots, read-only boundary, disk thresholds, GPU ID, and target tasks/init states/seeds.
2. Ask the user to enter the password in an interactive terminal.
3. If unattended operation is needed, request separate permission for a dedicated SSH key and public-key installation.
4. Inventory the existing benchmark environment, policy source, checkpoint/cache, adapters, and prior runs.
5. Pin official LIBERO and policy versions and write a reuse matrix.
6. Reuse a verified LIBERO environment read-only; isolate the policy service.
7. Validate one policy request without stepping the environment.
8. Run one real rollout and derive:
   - benchmark/policy native artifacts;
   - current comparable episode;
   - candidate episode preserving policy-native fields.
9. Visualize and explain the three views.
10. Run a 10-pair pilot only after the single episode passes.
11. Stop with a schema/pair audit and recommendation. Do not enter a larger batch without approval.

## Expected evidence

- approval receipt;
- host/asset inventory;
- official source and artifact manifests;
- reuse compatibility matrix;
- model/benchmark technical report;
- G4/G5/G6 validation reports;
- three representation manifests with one rollout lineage;
- 10 expected pair keys and pilot audit;
- static comparison page;
- no password, private key, checkpoint, or generated episode committed to Git.
