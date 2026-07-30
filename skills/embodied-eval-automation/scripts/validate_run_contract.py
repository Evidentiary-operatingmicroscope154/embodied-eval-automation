#!/usr/bin/env python3
"""Validate an embodied evaluation run contract without external dependencies."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Iterable

RUN_ID_RE = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9._-]{0,127}$")
SECRET_KEY_RE = re.compile(
    r"(password|passwd|private[_-]?key|access[_-]?token|secret|cookie|recovery[_-]?code)",
    re.IGNORECASE,
)
SECRET_VALUE_PATTERNS = (
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,})\b"),
    re.compile(r"\bhf_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
)
PERMISSION_STATES = {"approved", "denied", "not_requested"}
PERMISSION_KEYS = {
    "read",
    "write",
    "install",
    "download",
    "upload",
    "compute",
    "permission_change",
    "delete",
    "git",
    "notify",
}


def walk(value: Any, path: str = "$") -> Iterable[tuple[str, str | None, Any]]:
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            yield child_path, str(key), child
            yield from walk(child, child_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk(child, f"{path}[{index}]")


def validate_contract(payload: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(payload, dict):
        return ["Contract root must be a JSON object."]

    for key in (
        "schema_version",
        "run_id",
        "created_at",
        "mode",
        "model",
        "benchmark",
        "scope",
        "representations",
        "resources",
        "permissions",
        "completion",
    ):
        if key not in payload:
            errors.append(f"Missing required key: {key}")

    run_id = payload.get("run_id")
    if not isinstance(run_id, str) or not RUN_ID_RE.fullmatch(run_id):
        errors.append("run_id is missing or invalid.")

    permissions = payload.get("permissions")
    if not isinstance(permissions, dict):
        errors.append("permissions must be an object.")
    else:
        missing = sorted(PERMISSION_KEYS - set(permissions))
        extra = sorted(set(permissions) - PERMISSION_KEYS)
        if missing:
            errors.append(f"permissions missing keys: {', '.join(missing)}")
        if extra:
            errors.append(f"permissions has unknown keys: {', '.join(extra)}")
        for key, value in permissions.items():
            if value not in PERMISSION_STATES:
                errors.append(f"permissions.{key} has invalid state: {value!r}")

    representations = payload.get("representations")
    required_representations = {
        "official-native",
        "embodied-eval-current",
        "embodied-eval-candidate",
    }
    if not isinstance(representations, list):
        errors.append("representations must be an array.")
    elif not required_representations.issubset(set(representations)):
        errors.append("representations must include native, current, and candidate views.")

    resources = payload.get("resources")
    if isinstance(resources, dict):
        for key in ("remote_disk_pause_gib", "local_disk_pause_gib"):
            value = resources.get(key)
            if not isinstance(value, int) or value < 0:
                errors.append(f"resources.{key} must be a non-negative integer.")
        concurrency = resources.get("max_concurrency")
        if not isinstance(concurrency, int) or concurrency < 1:
            errors.append("resources.max_concurrency must be a positive integer.")

    for location, key, value in walk(payload):
        if key and SECRET_KEY_RE.search(key):
            errors.append(f"Secret-like key is forbidden: {location}")
        if isinstance(value, str):
            for pattern in SECRET_VALUE_PATTERNS:
                if pattern.search(value):
                    errors.append(f"Secret-like value is forbidden: {location}")
                    break

    return errors


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate an embodied run contract JSON file.")
    parser.add_argument("contract", type=Path)
    parser.add_argument("--json", action="store_true", help="Print a machine-readable result.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        payload = json.loads(args.contract.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors = [f"Cannot read valid JSON: {exc}"]
    else:
        errors = validate_contract(payload)

    if args.json:
        print(json.dumps({"status": "fail" if errors else "pass", "errors": errors}, indent=2))
    elif errors:
        for error in errors:
            print(f"ERROR: {error}")
    else:
        print("PASS")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
