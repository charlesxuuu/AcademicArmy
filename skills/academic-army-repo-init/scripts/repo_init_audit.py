#!/usr/bin/env python3
"""Static audit for an Academic Army initialized research repository."""

from __future__ import annotations

import ast
import json
import re
import sys
import tomllib
from pathlib import Path
from typing import Any

REQUIRED_TOP_LEVEL = [
    "data",
    "output",
    "results",
    "harness",
    "test",
    "README.md",
    "FRAMEWORK.md",
    "FRAMEWORK.zh-CN.md",
]


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: repo_init_audit.py <target-repo>", file=sys.stderr)
        return 2

    root = Path(argv[1]).resolve()
    report = audit(root)
    print(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False))
    return 0 if not report["errors"] else 1


def audit(root: Path) -> dict[str, Any]:
    errors: list[str] = []
    required_paths = {path: (root / path).exists() for path in REQUIRED_TOP_LEVEL}
    for path, exists in required_paths.items():
        if not exists:
            errors.append(f"missing required path: {path}")

    audit_path = root / "output" / "repo-init-self-audit.json"
    self_audit: dict[str, Any] = {}
    if audit_path.exists():
        try:
            self_audit = json.loads(audit_path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"self-audit json parse failed: {exc}")
    else:
        errors.append("missing self-audit: output/repo-init-self-audit.json")

    documented_missing = documented_path_errors(root, self_audit)
    errors.extend(documented_missing)

    docs = [root / "README.md", root / "FRAMEWORK.md", root / "FRAMEWORK.zh-CN.md"]
    docs_relative = docs_have_relative_paths(docs)
    if not docs_relative:
        errors.append("docs contain absolute-looking local paths")

    readme_short = readme_is_short(root / "README.md")
    if not readme_short:
        errors.append("README.md is not concise")

    framework_coverage = framework_docs_cover_required_topics(root)
    for topic, ok in framework_coverage.items():
        if not ok:
            errors.append(f"framework docs missing topic: {topic}")

    syntax = syntax_checks(root)
    errors.extend(syntax["errors"])

    test_config_ok = test_directory_configured(root)
    if not test_config_ok:
        errors.append("test discovery does not clearly target top-level test/")

    redundancy = redundancy_checks(root, self_audit)
    errors.extend(redundancy["errors"])

    return {
        "root": str(root),
        "required_paths": required_paths,
        "readme_concise": readme_short,
        "docs_repo_relative_paths": docs_relative,
        "framework_coverage": framework_coverage,
        "documented_paths_missing": documented_missing,
        "test_directory_configured": test_config_ok,
        "python_files_checked": syntax["python_files_checked"],
        "yaml_files_checked": syntax["yaml_files_checked"],
        "toml_files_checked": syntax["toml_files_checked"],
        "self_audit_status": self_audit.get("static_validation", {}).get("status"),
        "duplication_pass_status": self_audit.get("duplication_pass", {}).get("status"),
        "redundancy_flags": redundancy["flags"],
        "errors": errors,
    }


def documented_path_errors(root: Path, self_audit: dict[str, Any]) -> list[str]:
    missing: list[str] = []
    documented = self_audit.get("documented_paths", {})
    if isinstance(documented, dict):
        for rel_path in documented:
            if not (root / rel_path).exists():
                missing.append(f"documented path missing: {rel_path}")
    elif isinstance(documented, list):
        for rel_path in documented:
            if isinstance(rel_path, str) and not (root / rel_path).exists():
                missing.append(f"documented path missing: {rel_path}")
    elif documented:
        missing.append("documented_paths must be a mapping or list")
    return missing


def docs_have_relative_paths(paths: list[Path]) -> bool:
    absolute = re.compile(r"([A-Za-z]:\\|(?<![A-Za-z0-9_])/(?:Users|home|mnt|tmp|var|etc|opt|workspace)/)")
    for path in paths:
        if path.exists() and absolute.search(path.read_text(encoding="utf-8")):
            return False
    return True


def readme_is_short(path: Path) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")
    return len(text.splitlines()) <= 80


def framework_docs_cover_required_topics(root: Path) -> dict[str, bool]:
    combined = ""
    for rel_path in ["FRAMEWORK.md", "FRAMEWORK.zh-CN.md"]:
        path = root / rel_path
        if path.exists():
            combined += "\n" + path.read_text(encoding="utf-8")
    text = combined.lower()
    required_all = {
        "fixed_directories": ["data/", "output/", "results/", "harness/", "test/"],
        "core_modules": ["src/", "interface"],
        "harnesses": ["harness/"],
        "tests": ["test/"],
        "raw_artifacts": ["raw", "artifact"],
        "placeholders": ["placeholder"],
    }
    required_any = {
        "dependencies": ["dependency", "dependencies", "依赖"],
        "attribution": ["attribution", "license", "许可证"],
    }
    coverage = {name: all(token in text for token in tokens) for name, tokens in required_all.items()}
    coverage.update({name: any(token in text for token in tokens) for name, tokens in required_any.items()})
    return coverage


def syntax_checks(root: Path) -> dict[str, Any]:
    errors: list[str] = []
    python_files_checked = 0
    yaml_files_checked = 0
    toml_files_checked = 0

    for path in root.rglob("*.py"):
        python_files_checked += 1
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError as exc:
            errors.append(f"python syntax failed: {path.relative_to(root)}: {exc}")

    for path in root.rglob("*.toml"):
        toml_files_checked += 1
        try:
            tomllib.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"toml parse failed: {path.relative_to(root)}: {exc}")

    try:
        import yaml  # type: ignore[import-not-found]
    except Exception:
        yaml = None

    for path in root.rglob("*.yaml"):
        yaml_files_checked += 1
        if yaml is None:
            continue
        try:
            yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"yaml parse failed: {path.relative_to(root)}: {exc}")

    return {
        "errors": errors,
        "python_files_checked": python_files_checked,
        "yaml_files_checked": yaml_files_checked,
        "toml_files_checked": toml_files_checked,
    }


def test_directory_configured(root: Path) -> bool:
    pyproject = root / "pyproject.toml"
    if pyproject.exists():
        text = pyproject.read_text(encoding="utf-8")
        if 'testpaths = ["test"]' in text or "testpaths = ['test']" in text:
            return True
    return (root / "test").exists() and not (root / "tests").exists()


def redundancy_checks(root: Path, self_audit: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    flags: dict[str, Any] = {
        "empty_files": [],
        "generic_infrastructure": [],
        "duplication_pass_recorded": bool(self_audit.get("duplication_pass")),
    }

    allowed_empty = {".gitkeep", "py.typed"}
    for path in root.rglob("*"):
        if path.is_file() and path.stat().st_size == 0 and path.name not in allowed_empty:
            rel_path = path.relative_to(root).as_posix()
            flags["empty_files"].append(rel_path)
            errors.append(f"empty file without declared contract: {rel_path}")

    generic_dirs = [
        ".github",
        "dashboard",
        "dashboards",
        "web",
        "website",
        "service",
        "services",
        "database",
        "db",
        "deploy",
        "deployment",
    ]
    for rel_path in generic_dirs:
        if (root / rel_path).exists():
            flags["generic_infrastructure"].append(rel_path)
            errors.append(f"generic infrastructure present without audit justification: {rel_path}")

    if not flags["duplication_pass_recorded"]:
        errors.append("self-audit missing duplication_pass status")

    return {"errors": errors, "flags": flags}


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
