#!/usr/bin/env python3
"""
Run ESLint only on changed source files.

Default project root:
  /Users/lizhenwei/workspace/vueworkspace/bairong/asset-cube-html

This script detects changed files with git and filters to:
  .js, .jsx, .ts, .tsx, .vue

Usage:
  python3 scripts/check_changed_eslint.py
  python3 scripts/check_changed_eslint.py --files src/views/foo/page2/index.vue src/router/modules/foo2.js
  python3 scripts/check_changed_eslint.py --fix
"""
import argparse
import json
import shutil
import subprocess
from pathlib import Path

DEFAULT_PROJECT_ROOT = "/Users/lizhenwei/workspace/vueworkspace/bairong/asset-cube-html"
ESLINT_EXTENSIONS = {".js", ".jsx", ".ts", ".tsx", ".vue"}

def run(cmd, cwd):
    return subprocess.run(cmd, cwd=str(cwd), text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def git_changed_files(project_root: Path):
    commands = [
        ["git", "diff", "--name-only", "--diff-filter=ACMRTUXB"],
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMRTUXB"],
        ["git", "ls-files", "--others", "--exclude-standard"],
    ]
    files, seen = [], set()
    for cmd in commands:
        proc = run(cmd, project_root)
        if proc.returncode != 0:
            continue
        for line in proc.stdout.splitlines():
            rel = line.strip()
            if rel and rel not in seen:
                seen.add(rel)
                files.append(rel)
    return files

def filter_lintable(files, project_root: Path):
    result = []
    for f in files:
        rel = str(f).replace("\\", "/")
        if rel.startswith(("node_modules/", "dist/", "coverage/")):
            continue
        p = project_root / rel
        if p.exists() and p.suffix in ESLINT_EXTENSIONS:
            result.append(rel)
    return result

def detect_eslint_command(project_root: Path, fix: bool):
    eslint_args = ["eslint"]
    if fix:
        eslint_args.append("--fix")
    if (project_root / "pnpm-lock.yaml").exists() and shutil.which("pnpm"):
        return ["pnpm", "exec"] + eslint_args
    if (project_root / "yarn.lock").exists() and shutil.which("yarn"):
        return ["yarn"] + eslint_args
    if (project_root / "package-lock.json").exists() and shutil.which("npm"):
        return ["npm", "exec", "--"] + eslint_args
    if shutil.which("pnpm"):
        return ["pnpm", "exec"] + eslint_args
    if shutil.which("npx"):
        return ["npx"] + eslint_args
    return eslint_args

def main():
    parser = argparse.ArgumentParser(description="Run ESLint on changed files only.")
    parser.add_argument("--project-root", default=DEFAULT_PROJECT_ROOT)
    parser.add_argument("--files", nargs="*", help="Explicit file list, relative or absolute.")
    parser.add_argument("--fix", action="store_true", help="Run ESLint with --fix.")
    parser.add_argument("--json-output", help="Optional JSON result output path.")
    args = parser.parse_args()

    project_root = Path(args.project_root).expanduser().resolve()
    if not project_root.exists():
        raise SystemExit(f"Project root does not exist: {project_root}")

    if args.files:
        raw_files = []
        for f in args.files:
            p = Path(f)
            if p.is_absolute():
                try:
                    raw_files.append(str(p.resolve().relative_to(project_root)))
                except ValueError:
                    raw_files.append(str(p))
            else:
                raw_files.append(f)
    else:
        raw_files = git_changed_files(project_root)

    lint_files = filter_lintable(raw_files, project_root)

    result = {
        "project_root": str(project_root),
        "raw_changed_file_count": len(raw_files),
        "lint_file_count": len(lint_files),
        "lint_files": lint_files,
        "eslint_command": None,
        "pass": True,
        "stdout": "",
        "stderr": "",
        "returncode": 0,
        "message": "",
    }

    if not lint_files:
        result["message"] = "No changed lintable files found."
        payload = json.dumps(result, ensure_ascii=False, indent=2)
        if args.json_output:
            Path(args.json_output).write_text(payload, encoding="utf-8")
        print(payload)
        return

    cmd = detect_eslint_command(project_root, args.fix) + lint_files
    result["eslint_command"] = cmd
    proc = run(cmd, project_root)
    result["returncode"] = proc.returncode
    result["stdout"] = proc.stdout[-12000:]
    result["stderr"] = proc.stderr[-12000:]
    result["pass"] = proc.returncode == 0
    result["message"] = "ESLint passed for changed files." if proc.returncode == 0 else "ESLint failed for changed files."

    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.json_output:
        Path(args.json_output).write_text(payload, encoding="utf-8")
    print(payload)

    if proc.returncode != 0:
        raise SystemExit(proc.returncode)

if __name__ == "__main__":
    main()
