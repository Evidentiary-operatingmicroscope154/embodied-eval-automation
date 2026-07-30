# Example: world model + embodied benchmark pilot

## User request

> Use `$embodied-eval-automation` with a video-predictive world model and an embodied benchmark. The model outputs future RGB frames and value estimates but does not directly control the robot. Help me define how those outputs coexist with benchmark observations and a policy’s executed actions. Use existing Hugging Face access if available, but stop if the checkpoint is gated and I have not accepted its license.

## Expected skill behavior

1. Identify the architecture as a world-model-assisted pipeline rather than assuming the world model is the action policy.
2. Explain benchmark inputs/outputs and the model’s prediction process using official sources.
3. Inspect Hugging Face authentication with `hf auth whoami`; never request a token in chat.
4. Stop for user license acceptance if the model is gated.
5. Pin the snapshot revision, file sizes, and hashes.
6. Design adapters for:
   - benchmark observations and actual environment transitions;
   - policy raw/executed actions, when a separate policy is present;
   - world-model future frames and values under `policy_queries/predictions`.
7. Never place predicted future frames in the true observation sequence.
8. Produce native/current/candidate views from the same rollout and report which current fields are unsupported.
9. Recommend a candidate schema only after measuring conversion loss and storage cost.

## Key invariant

For `T` environment transitions, store `T+1` benchmark observations. Future model predictions are query-scoped model-native artifacts, not additional environment observations.
