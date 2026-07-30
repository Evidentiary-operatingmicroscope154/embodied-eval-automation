#!/usr/bin/env python3
"""Create a minimal, permission-recorded embodied evaluation run workspace."""

from __future__ import annotations

import argparse
import json
import os
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

RUN_ID_RE = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9._-]{0,127}$")


def atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(payload, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    except BaseException:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise


def validate_root(root: Path) -> Path:
    resolved = root.expanduser().resolve()
    if resolved == Path(resolved.anchor):
        raise ValueError("Refusing to use a filesystem root as the run workspace.")
    return resolved


def create_workspace(
    root: Path,
    run_id: str,
    model: str,
    model_role: str,
    benchmark: str,
    mode: str,
    approval_id: str,
    remote_disk_pause_gib: int,
    local_disk_pause_gib: int,
) -> Path:
    if not RUN_ID_RE.fullmatch(run_id):
        raise ValueError("run_id must use 1-128 letters, digits, dot, underscore, or hyphen.")
    if not approval_id.strip():
        raise ValueError("approval_id is required to record the workspace write boundary.")

    approved_root = validate_root(root)
    run_dir = (approved_root / run_id).resolve()
    try:
        run_dir.relative_to(approved_root)
    except ValueError as exc:
        raise ValueError("Resolved run directory escaped the approved root.") from exc

    if run_dir.exists() and any(run_dir.iterdir()):
        raise FileExistsError(f"Refusing to overwrite non-empty run directory: {run_dir}")

    directories = (
        "approvals",
        "manifests",
        "adapters",
        "state",
        "reports",
        "artifacts/official-native",
        "artifacts/embodied-eval-current",
        "artifacts/embodied-eval-candidate",
        "packages",
        "logs",
    )
    for relative in directories:
        (run_dir / relative).mkdir(parents=True, exist_ok=True)

    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    contract: dict[str, Any] = {
        "schema_version": "embodied-run-contract/v1",
        "run_id": run_id,
        "created_at": now,
        "mode": mode,
        "model": {
            "name": model,
            "role": model_role,
            "source_revision": "",
            "checkpoint_revision": "",
        },
        "benchmark": {"name": benchmark, "source_revision": ""},
        "scope": {
            "suites": [],
            "tasks": [],
            "init_states": [],
            "seeds": [],
            "repetitions": 1,
            "expected_episode_count": 0,
            "expected_pair_count": 0,
        },
        "representations": [
            "official-native",
            "embodied-eval-current",
            "embodied-eval-candidate",
        ],
        "resources": {
            "gpu_ids": [],
            "max_concurrency": 1,
            "remote_disk_pause_gib": remote_disk_pause_gib,
            "local_disk_pause_gib": local_disk_pause_gib,
            "cost_limit": None,
        },
        "permissions": {
            "read": "not_requested",
            "write": "approved",
            "install": "not_requested",
            "download": "not_requested",
            "upload": "not_requested",
            "compute": "not_requested",
            "permission_change": "not_requested",
            "delete": "not_requested",
            "git": "not_requested",
            "notify": "not_requested",
        },
        "approval_ids": {"write": approval_id},
        "completion": {
            "required_gates": [f"G{index}" for index in range(10)],
            "allowed_failures": [],
            "deliverables": [],
        },
    }
    receipt = {
        "approval_id": approval_id,
        "run_id": run_id,
        "approved_at": now,
        "category": "write",
        "targets": [str(run_dir)],
        "allowed_actions": ["create run workspace and initial contract"],
        "forbidden_actions": [
            "install",
            "download",
            "upload",
            "start paid compute",
            "delete",
            "git write",
        ],
        "expires_when": "initial workspace creation completes",
        "evidence": "supplied approval identifier; retain the original user approval separately",
    }
    atomic_write_json(run_dir / "run_contract.json", contract)
    atomic_write_json(run_dir / "approvals" / f"{approval_id}.json", receipt)
    return run_dir


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create a minimal embodied evaluation run workspace after write approval."
    )
    parser.add_argument("--root", type=Path, required=True, help="Approved parent directory.")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument(
        "--model-role",
        choices=("policy", "vla", "world-model", "world-action", "hybrid"),
        required=True,
    )
    parser.add_argument("--benchmark", required=True)
    parser.add_argument(
        "--mode",
        choices=("online-closed-loop", "offline", "hybrid"),
        default="online-closed-loop",
    )
    parser.add_argument(
        "--approval-id",
        required=True,
        help="Identifier of the user approval for creating this workspace.",
    )
    parser.add_argument("--remote-disk-pause-gib", type=int, default=25)
    parser.add_argument("--local-disk-pause-gib", type=int, default=25)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        path = create_workspace(
            root=args.root,
            run_id=args.run_id,
            model=args.model,
            model_role=args.model_role,
            benchmark=args.benchmark,
            mode=args.mode,
            approval_id=args.approval_id,
            remote_disk_pause_gib=args.remote_disk_pause_gib,
            local_disk_pause_gib=args.local_disk_pause_gib,
        )
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 2
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
