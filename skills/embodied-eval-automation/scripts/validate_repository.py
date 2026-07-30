#!/usr/bin/env python3
"""Validate this standalone skill/plugin repository with the Python standard library."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Iterable

SKILL_REL = Path("skills/embodied-eval-automation")
REQUIRED_PATHS = (
    Path(".codex-plugin/plugin.json"),
    Path("README.md"),
    Path("README.zh-CN.md"),
    Path("LICENSE"),
    Path("SECURITY.md"),
    Path("PRIVACY.md"),
    Path("CONTRIBUTING.md"),
    Path("CITATION.cff"),
    SKILL_REL / "SKILL.md",
    SKILL_REL / "LICENSE.txt",
    SKILL_REL / "agents/openai.yaml",
)
SECRET_PATTERNS = (
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,})\b"),
    re.compile(r"\bhf_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
)
PRIVATE_PATH_PATTERNS = (
    re.compile(r"[A-Za-z]:\\Users\\[^\\\s]+", re.IGNORECASE),
    re.compile(r"/home/[^/\s]+"),
)
VALIDATOR_REL = (
    SKILL_REL / "scripts" / "validate_repository.py"
)


def text_files(root: Path) -> Iterable[Path]:
    allowed = {".md", ".py", ".json", ".yaml", ".yml", ".txt", ".svg", ".gitignore", ".gitattributes"}
    for path in root.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix.lower() in allowed or path.name in {".gitignore", ".gitattributes"}:
            yield path


def validate_repository(root: Path) -> tuple[list[str], list[str]]:
    root = root.resolve()
    errors: list[str] = []
    warnings: list[str] = []

    for relative in REQUIRED_PATHS:
        if not (root / relative).is_file():
            errors.append(f"Missing required file: {relative.as_posix()}")

    skill_path = root / SKILL_REL / "SKILL.md"
    if skill_path.is_file():
        skill_text = skill_path.read_text(encoding="utf-8")
        lines = skill_text.splitlines()
        if len(lines) > 500:
            errors.append(f"SKILL.md exceeds 500 lines: {len(lines)}")
        frontmatter = re.match(r"^---\n(.*?)\n---\n", skill_text, re.DOTALL)
        if not frontmatter:
            errors.append("SKILL.md has invalid YAML frontmatter boundaries.")
        else:
            block = frontmatter.group(1)
            keys = []
            for line in block.splitlines():
                if ":" in line and not line.startswith((" ", "\t")):
                    keys.append(line.split(":", 1)[0].strip())
            if keys != ["name", "description"]:
                errors.append(f"SKILL.md frontmatter keys must be name, description; found {keys}")
            if "name: embodied-eval-automation" not in block:
                errors.append("SKILL.md name does not match the skill directory.")

        references = re.findall(r"\((references/[^)]+\.md)\)", skill_text)
        if not references:
            errors.append("SKILL.md does not link any references.")
        for reference in references:
            if not (root / SKILL_REL / reference).is_file():
                errors.append(f"Broken SKILL.md reference: {reference}")

    plugin_path = root / ".codex-plugin" / "plugin.json"
    if plugin_path.is_file():
        try:
            plugin = json.loads(plugin_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"plugin.json is invalid JSON: {exc}")
        else:
            if plugin.get("name") != "embodied-eval-automation":
                errors.append("plugin.json name mismatch.")
            if not re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?", str(plugin.get("version", ""))):
                errors.append("plugin.json version is not valid semantic version syntax.")
            if plugin.get("skills") != "./skills/":
                errors.append("plugin.json must point skills to ./skills/.")
            if plugin.get("license") != "MIT":
                errors.append("plugin.json license must match the repository MIT license.")

    openai_path = root / SKILL_REL / "agents" / "openai.yaml"
    if openai_path.is_file():
        openai_text = openai_path.read_text(encoding="utf-8")
        if "$embodied-eval-automation" not in openai_text:
            errors.append("agents/openai.yaml default prompt must mention $embodied-eval-automation.")

    for path in text_files(root):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"Text file is not UTF-8: {path.relative_to(root).as_posix()}")
            continue
        relative = path.relative_to(root).as_posix()
        if path.relative_to(root) != VALIDATOR_REL and ("[" + "TODO:") in text:
            errors.append(f"Scaffold TODO remains in {relative}")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                errors.append(f"Secret-like value found in {relative}")
                break
        if path.relative_to(root) != VALIDATOR_REL:
            for pattern in PRIVATE_PATH_PATTERNS:
                if pattern.search(text):
                    errors.append(f"Private or project-specific path found in {relative}")
                    break
        if path.stat().st_size > 5 * 1024 * 1024:
            warnings.append(f"Large text file over 5 MiB: {relative}")

    templates = root / SKILL_REL / "assets" / "templates"
    if templates.is_dir():
        for path in templates.glob("*.json"):
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                errors.append(f"Invalid JSON template {path.name}: {exc}")
    else:
        errors.append("Missing assets/templates directory.")

    return errors, warnings


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate the standalone skill/plugin repository.")
    parser.add_argument("root", type=Path, nargs="?", default=Path.cwd())
    parser.add_argument("--json", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    errors, warnings = validate_repository(args.root)
    if args.json:
        print(
            json.dumps(
                {
                    "status": "fail" if errors else "pass",
                    "errors": errors,
                    "warnings": warnings,
                },
                indent=2,
            )
        )
    else:
        for warning in warnings:
            print(f"WARNING: {warning}")
        for error in errors:
            print(f"ERROR: {error}")
        if not errors:
            print("PASS")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
