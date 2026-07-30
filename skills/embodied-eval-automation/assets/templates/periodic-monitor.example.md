# Periodic monitor contract

- Automation ID:
- Run ID:
- Check interval:
- Remote connection:
- Remote run root:
- Local artifact root:

## Inspect

- remote progress and heartbeat;
- supervisor/worker/model/collector status;
- scope and package lifecycle;
- remote disk and authorized GPUs;
- local controller process;
- transfer, local validation, acknowledgement, and prune receipts;
- final global audit.

## Notify immediately

- paused or failed;
- heartbeat stale beyond the approved interval;
- unexpected process exit;
- stopped controller with unverified scopes;
- disk/GPU/cost violation;
- transfer/hash/validation failure;
- local acknowledgement without approved prune receipt.

## Completion

Notify completion only when the complete gate passes. Summarize counts, success/failure metrics, missing/duplicate/corrupt IDs, transitions/queries, storage, cleanup receipts, and data locations. Pause this monitor after the notification.

Normal healthy progress should not generate user messages.
