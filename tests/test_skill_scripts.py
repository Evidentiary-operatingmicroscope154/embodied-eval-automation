from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "embodied-eval-automation" / "scripts"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


create_run_workspace = load_module(
    "create_run_workspace", SCRIPTS / "create_run_workspace.py"
)
validate_run_contract = load_module(
    "validate_run_contract", SCRIPTS / "validate_run_contract.py"
)
validate_repository = load_module(
    "validate_repository", SCRIPTS / "validate_repository.py"
)


class RunWorkspaceTests(unittest.TestCase):
    def test_create_and_validate_workspace(self):
        with tempfile.TemporaryDirectory() as temp:
            run_dir = create_run_workspace.create_workspace(
                root=Path(temp),
                run_id="pilot-001",
                model="example-policy",
                model_role="vla",
                benchmark="example-benchmark",
                mode="online-closed-loop",
                approval_id="approval-write-001",
                remote_disk_pause_gib=25,
                local_disk_pause_gib=25,
            )
            contract = json.loads((run_dir / "run_contract.json").read_text(encoding="utf-8"))
            self.assertEqual([], validate_run_contract.validate_contract(contract))
            self.assertTrue((run_dir / "artifacts" / "official-native").is_dir())
            self.assertTrue(
                (run_dir / "approvals" / "approval-write-001.json").is_file()
            )

    def test_refuses_non_empty_run_directory(self):
        with tempfile.TemporaryDirectory() as temp:
            existing = Path(temp) / "pilot-001"
            existing.mkdir()
            (existing / "keep.txt").write_text("keep", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                create_run_workspace.create_workspace(
                    root=Path(temp),
                    run_id="pilot-001",
                    model="model",
                    model_role="policy",
                    benchmark="benchmark",
                    mode="online-closed-loop",
                    approval_id="approval-write-001",
                    remote_disk_pause_gib=25,
                    local_disk_pause_gib=25,
                )


class ContractValidationTests(unittest.TestCase):
    def test_rejects_secret_like_key(self):
        template = ROOT / (
            "skills/embodied-eval-automation/assets/templates/run-contract.example.json"
        )
        payload = json.loads(template.read_text(encoding="utf-8"))
        payload["password"] = "redacted"
        errors = validate_run_contract.validate_contract(payload)
        self.assertTrue(any("Secret-like key" in error for error in errors))

    def test_example_contract_is_valid(self):
        template = ROOT / (
            "skills/embodied-eval-automation/assets/templates/run-contract.example.json"
        )
        payload = json.loads(template.read_text(encoding="utf-8"))
        self.assertEqual([], validate_run_contract.validate_contract(payload))


class RepositoryValidationTests(unittest.TestCase):
    def test_repository_is_valid(self):
        errors, warnings = validate_repository.validate_repository(ROOT)
        self.assertEqual([], errors)
        self.assertEqual([], warnings)


if __name__ == "__main__":
    unittest.main()
