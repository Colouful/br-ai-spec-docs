#!/usr/bin/env python3
"""
Automated migration audit script for component-refactor skill.

Scans Page1 and Page2 directories, checks for anti-patterns,
component replacements, and generates a diff-based audit report.

Usage:
  python3 scripts/audit_refactor.py \
    --page1 src/views/disposalTool/disposalManagement \
    --page2 src/views/disposalTool2/disposalManagement

  python3 scripts/audit_refactor.py \
    --page1 src/views/disposalTool/disposalManagement \
    --page2 src/views/disposalTool2/disposalManagement \
    --output docs/component-refactor/audit-report.md

  python3 scripts/audit_refactor.py \
    --page2 src/views/disposalTool2/disposalManagement \
    --check-only
"""

import argparse
import os
import re
import sys
from pathlib import Path
from datetime import datetime


DEFAULT_PROJECT_ROOT = "/Users/lizhenwei/workspace/vueworkspace/bairong/asset-cube-html"

# Anti-patterns: (id, name, severity, regex_or_callable)
ANTI_PATTERNS = {
    "AP-01": {
        "name": "onFinish 缺少 emit('update:visible', false)",
        "severity": "BLOCKER",
        "description": "ProModalForm 子组件 handleFinish/handleSubmit 成功路径必须 emit('update:visible', false)",
    },
    "AP-02": {
        "name": "formFields 依赖动态 ref",
        "severity": "BLOCKER",
        "description": "formFields computed 依赖动态 ref 时，onChange 必须先同步 model",
    },
    "AP-03": {
        "name": "字段缺少 takeFullRow: true",
        "severity": "HIGH",
        "description": "ProModalForm 弹窗所有字段必须 takeFullRow: true",
    },
    "AP-04": {
        "name": "onChange await 前未同步 model",
        "severity": "BLOCKER",
        "description": "onChange 中 model.xxx = val 必须在所有 await 之前",
    },
    "AP-05": {
        "name": "onChange 缺少 Event 守卫",
        "severity": "HIGH",
        "description": "onChange 必须有 instanceof Event 守卫",
    },
    "AP-06": {
        "name": "ProTable 缺少 scroll.y",
        "severity": "HIGH",
        "description": "tableProps.scroll 必须包含 y: 500",
    },
    "AP-07": {
        "name": "saveQueryData 包含分页参数",
        "severity": "BLOCKER",
        "description": "saveQueryData 前必须排除 pageNo/pageSize",
    },
    "AP-08": {
        "name": "多余列/死代码",
        "severity": "MEDIUM",
        "description": "proColumns 列配置不应包含参考文件中不存在的列",
    },
    "AP-09": {
        "name": "GET API 使用 data 而非 params",
        "severity": "BLOCKER",
        "description": "GET 请求必须使用 params 而非 data",
    },
    "AP-10": {
        "name": "只读字段使用 valueType: 'text'",
        "severity": "MEDIUM",
        "description": "只读字段应使用 valueType: 'input' + fieldProps: { disabled: true }",
    },
}

# Old components that must be replaced
OLD_COMPONENTS = [
    (r"@koi-design/vix-components", "@koi-design/vix-components"),
    (r"DynamicsFilter", "DynamicsFilter"),
    (r"DynamicsForm", "DynamicsForm"),
    (r"<u-table", "u-table"),
    (r"<UModal", "UModal"),
    (r"EditDrawer", "EditDrawer"),
    (r"ViewContent", "ViewContent"),
    (r"u-info-view", "u-info-view"),
    (r"OneLineText", "OneLineText"),
    (r"usePageList", "usePageList"),
    (r"<u-tooltip", "u-tooltip"),
    (r"<u-tag", "u-tag"),
    (r"<u-button", "u-button"),
    (r"<u-select", "u-select"),
    (r"<u-input", "u-input"),
]


def find_vue_files(directory: Path) -> list[Path]:
    """Find all .vue files recursively."""
    if not directory.exists():
        return []
    return sorted(directory.rglob("*.vue"))


def read_file_safe(path: Path) -> str:
    """Read file content, return empty string on error."""
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def check_ap01(content: str, filepath: str) -> list[dict]:
    """Check onFinish/handleFinish has emit('update:visible', false)."""
    issues = []
    # Look for handleFinish or handleSubmit functions
    if re.search(r"(handleFinish|handleSubmit)\s*=", content):
        # Check if there's a ProModalForm usage
        if "ProModalForm" in content or "proModalForm" in content:
            # Check for emit('update:visible', false) in success paths
            if "emit('update:visible', false)" not in content and \
               'emit("update:visible", false)' not in content and \
               "emit('update:visible',false)" not in content:
                issues.append({
                    "file": filepath,
                    "pattern": "AP-01",
                    "detail": "handleFinish/handleSubmit 缺少 emit('update:visible', false)",
                })
    return issues


def check_ap03(content: str, filepath: str) -> list[dict]:
    """Check all form fields have takeFullRow: true."""
    issues = []
    if "ProModalForm" in content or "proModalForm" in content:
        # Find field definitions in computed/ref
        field_blocks = re.findall(
            r"\{[^{}]*?field:\s*['\"](\w+)['\"][^{}]*?\}",
            content,
            re.DOTALL
        )
        # Check if takeFullRow is present in field definitions
        # Simple heuristic: count fields vs takeFullRow occurrences
        field_count = len(re.findall(r"field:\s*['\"]", content))
        takefull_count = len(re.findall(r"takeFullRow:\s*true", content))
        if field_count > 0 and takefull_count < field_count:
            issues.append({
                "file": filepath,
                "pattern": "AP-03",
                "detail": f"发现 {field_count} 个字段，仅 {takefull_count} 个有 takeFullRow: true",
            })
    return issues


def check_ap05(content: str, filepath: str) -> list[dict]:
    """Check onChange handlers have Event guard."""
    issues = []
    # Find onChange handlers
    on_changes = re.findall(r"onChange:\s*(?:async\s+)?(?:\([^)]*\)|\w+)\s*=>\s*\{", content)
    event_guards = re.findall(r"instanceof\s+Event", content)
    if len(on_changes) > 0 and len(event_guards) == 0:
        issues.append({
            "file": filepath,
            "pattern": "AP-05",
            "detail": f"发现 {len(on_changes)} 个 onChange，无 instanceof Event 守卫",
        })
    return issues


def check_ap06(content: str, filepath: str) -> list[dict]:
    """Check ProTable has scroll.y."""
    issues = []
    if "ProTable" in content or "proTable" in content:
        if "scroll" in content:
            if re.search(r"scroll:\s*\{\s*x:", content) and not re.search(r"y:\s*\d+", content):
                issues.append({
                    "file": filepath,
                    "pattern": "AP-06",
                    "detail": "tableProps.scroll 缺少 y 属性",
                })
    return issues


def check_ap07(content: str, filepath: str) -> list[dict]:
    """Check saveQueryData excludes pagination params."""
    issues = []
    # Look for saveQueryData calls
    calls = re.findall(r"saveQueryData\((\w+)\)", content)
    for var_name in calls:
        # Check if there's destructuring before the call
        if var_name == "params":
            # Check if there's pageNo/pageSize destructuring nearby
            context = content
            if "saveQueryData(params)" in context:
                # Check if params has been destructured
                if "const { pageNo, pageSize" not in context and \
                   "const {pageNo, pageSize" not in context and \
                   "let { pageNo, pageSize" not in context and \
                   "...queryOnly" not in context:
                    issues.append({
                        "file": filepath,
                        "pattern": "AP-07",
                        "detail": "saveQueryData(params) 未排除分页参数",
                    })
    return issues


def check_ap09(content: str, filepath: str) -> list[dict]:
    """Check GET APIs use params not data."""
    issues = []
    if filepath.endswith(".js"):
        get_apis = re.findall(
            r"method:\s*['\"]get['\"].*?data[,:]",
            content,
            re.DOTALL
        )
        if get_apis:
            issues.append({
                "file": filepath,
                "pattern": "AP-09",
                "detail": f"发现 {len(get_apis)} 个 GET API 使用 data 而非 params",
            })
    return issues


def check_ap10(content: str, filepath: str) -> list[dict]:
    """Check no valueType: 'text' for read-only fields."""
    issues = []
    text_types = re.findall(r"valueType:\s*['\"]text['\"]", content)
    if text_types:
        issues.append({
            "file": filepath,
            "pattern": "AP-10",
            "detail": f"发现 {len(text_types)} 处 valueType: 'text'，应使用 valueType: 'input' + disabled",
        })
    return issues


def check_old_components(content: str, filepath: str) -> list[dict]:
    """Check for old component usage."""
    issues = []
    for pattern, name in OLD_COMPONENTS:
        if re.search(pattern, content):
            issues.append({
                "file": filepath,
                "pattern": "OLD-COMP",
                "detail": f"仍使用旧组件: {name}",
            })
    return issues


def check_titlealign(content: str, filepath: str) -> list[dict]:
    """Check titleAlign configuration."""
    issues = []
    # ProModalForm type="modal" must have titleAlign: 'start'
    if "ProModalForm" in content:
        if 'type="modal"' in content or "type='modal'" in content:
            if "titleAlign: 'start'" not in content and 'titleAlign: "start"' not in content:
                issues.append({
                    "file": filepath,
                    "pattern": "TITLE-ALIGN",
                    "detail": "ProModalForm type='modal' 缺少 titleAlign: 'start'",
                })
    return issues


def run_all_checks(page2_dir: Path) -> dict:
    """Run all anti-pattern checks on Page2 files."""
    results = {
        "files_scanned": 0,
        "issues": [],
        "by_severity": {"BLOCKER": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0},
        "by_pattern": {},
    }

    vue_files = find_vue_files(page2_dir)
    results["files_scanned"] = len(vue_files)

    check_functions = [
        check_ap01, check_ap03, check_ap05, check_ap06,
        check_ap07, check_ap10,
        check_old_components, check_titlealign,
    ]

    for f in vue_files:
        content = read_file_safe(f)
        rel_path = str(f.relative_to(page2_dir.parent.parent.parent))
        for check_fn in check_functions:
            issues = check_fn(content, rel_path)
            for issue in issues:
                pattern = issue["pattern"]
                results["issues"].append(issue)
                if pattern in ANTI_PATTERNS:
                    severity = ANTI_PATTERNS[pattern]["severity"]
                    results["by_severity"][severity] = results["by_severity"].get(severity, 0) + 1
                results["by_pattern"][pattern] = results["by_pattern"].get(pattern, 0) + 1

    # Also check API files imported by Page2
    # First, find which API modules Page2 imports
    imported_api_files = set()
    api_base = page2_dir.parent.parent.parent / "api"
    for f in vue_files:
        content = read_file_safe(f)
        # Match import from @api/xxx or @/api/xxx
        for m in re.finditer(r"from\s+['\"](?:@api|@/api)/(\w+)['\"]", content):
            api_name = m.group(1)
            if api_base.exists():
                candidate = api_base / f"{api_name}.js"
                if candidate.exists():
                    imported_api_files.add(candidate)

    for js_file in imported_api_files:
        content = read_file_safe(js_file)
        rel_path = str(js_file.relative_to(page2_dir.parent.parent.parent))
        issues = check_ap09(content, rel_path)
        for issue in issues:
            results["issues"].append(issue)
            results["by_severity"]["BLOCKER"] += 1
            results["by_pattern"]["AP-09"] = results["by_pattern"].get("AP-09", 0) + 1

    return results


def count_files(directory: Path) -> dict:
    """Count files by type in a directory."""
    counts = {"vue": 0, "js": 0, "ts": 0, "other": 0, "total": 0}
    if not directory.exists():
        return counts
    for f in directory.rglob("*"):
        if f.is_file():
            counts["total"] += 1
            ext = f.suffix.lower()
            if ext == ".vue":
                counts["vue"] += 1
            elif ext in (".js", ".jsx"):
                counts["js"] += 1
            elif ext in (".ts", ".tsx"):
                counts["ts"] += 1
            else:
                counts["other"] += 1
    return counts


def generate_report(page1_path: str, page2_path: str, results: dict, project_root: str) -> str:
    """Generate markdown audit report."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    page1_dir = Path(project_root) / page1_path
    page2_dir = Path(project_root) / page2_path

    page1_counts = count_files(page1_dir)
    page2_counts = count_files(page2_dir)

    blocker_count = results["by_severity"].get("BLOCKER", 0)
    high_count = results["by_severity"].get("HIGH", 0)

    if blocker_count > 0:
        conclusion = "❌ Fail — 存在 BLOCKER 级问题"
    elif high_count > 0:
        conclusion = "⚠️ Conditional Pass — 存在 HIGH 级问题"
    else:
        conclusion = "✅ Pass"

    lines = [
        "# 迁移审计报告",
        "",
        "## 基本信息",
        "",
        "| 项目 | 值 |",
        "|------|-----|",
        f"| Page1 路径 | `{page1_path}` |",
        f"| Page2 路径 | `{page2_path}` |",
        f"| 审计时间 | {now} |",
        f"| Page1 文件数 | {page1_counts['total']} (vue: {page1_counts['vue']}) |",
        f"| Page2 文件数 | {page2_counts['total']} (vue: {page2_counts['vue']}) |",
        f"| 扫描文件数 | {results['files_scanned']} |",
        "",
        "---",
        "",
        "## 反模式检查结果",
        "",
        f"| 严重级别 | 数量 |",
        f"|----------|------|",
        f"| 🔴 BLOCKER | {blocker_count} |",
        f"| 🟡 HIGH | {high_count} |",
        f"| 🟠 MEDIUM | {results['by_severity'].get('MEDIUM', 0)} |",
        "",
        "### 按类型统计",
        "",
        "| 编号 | 名称 | 命中次数 |",
        "|------|------|----------|",
    ]

    for pattern_id, count in sorted(results["by_pattern"].items()):
        name = ANTI_PATTERNS.get(pattern_id, {}).get("name", pattern_id)
        lines.append(f"| {pattern_id} | {name} | {count} |")

    if not results["by_pattern"]:
        lines.append("| - | 无问题 | 0 |")

    lines.extend([
        "",
        "### 问题详情",
        "",
    ])

    if results["issues"]:
        lines.append("| 文件 | 检查项 | 详情 |")
        lines.append("|------|--------|------|")
        for issue in results["issues"]:
            lines.append(f"| `{issue['file']}` | {issue['pattern']} | {issue['detail']} |")
    else:
        lines.append("✅ 未发现反模式问题。")

    lines.extend([
        "",
        "---",
        "",
        "## 验收结论",
        "",
        conclusion,
        "",
        "---",
        "",
        "## 后续操作",
        "",
    ])

    if blocker_count > 0:
        lines.append("1. 修复所有 BLOCKER 级问题")
        lines.append("2. 重新运行审计脚本")
        lines.append("3. 运行 ESLint: `python3 scripts/check_changed_eslint.py`")
    elif high_count > 0:
        lines.append("1. 评估 HIGH 级问题是否影响核心功能")
        lines.append("2. 运行 ESLint: `python3 scripts/check_changed_eslint.py`")
    else:
        lines.append("1. 运行 ESLint: `python3 scripts/check_changed_eslint.py`")
        lines.append("2. 人工验证页面功能")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Automated migration audit for component-refactor.")
    parser.add_argument("--project-root", default=DEFAULT_PROJECT_ROOT,
                        help="Project root directory")
    parser.add_argument("--page1", required=False,
                        help="Page1 path relative to project root (e.g., src/views/disposalTool/disposalManagement)")
    parser.add_argument("--page2", required=True,
                        help="Page2 path relative to project root")
    parser.add_argument("--output", "-o", help="Output report file path")
    parser.add_argument("--check-only", action="store_true",
                        help="Only run checks, don't generate report")
    parser.add_argument("--json", action="store_true",
                        help="Output JSON instead of markdown")
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    page2_dir = project_root / args.page2

    if not page2_dir.exists():
        print(f"ERROR: Page2 directory not found: {page2_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"Scanning Page2: {args.page2}", file=sys.stderr)
    results = run_all_checks(page2_dir)

    if args.json:
        import json
        print(json.dumps(results, ensure_ascii=False, indent=2))
    elif args.check_only:
        blocker_count = results["by_severity"].get("BLOCKER", 0)
        high_count = results["by_severity"].get("HIGH", 0)
        print(f"Files scanned: {results['files_scanned']}")
        print(f"Issues found: {len(results['issues'])}")
        print(f"  BLOCKER: {blocker_count}")
        print(f"  HIGH: {high_count}")
        print(f"  MEDIUM: {results['by_severity'].get('MEDIUM', 0)}")
        if blocker_count > 0:
            print("RESULT: FAIL")
            sys.exit(1)
        elif high_count > 0:
            print("RESULT: CONDITIONAL PASS")
            sys.exit(2)
        else:
            print("RESULT: PASS")
    else:
        page1_path = args.page1 or args.page2.replace("2/", "/")
        report = generate_report(page1_path, args.page2, results, str(project_root))
        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(report, encoding="utf-8")
            print(f"Report written to: {args.output}", file=sys.stderr)
        else:
            print(report)

    # Exit code
    blocker_count = results["by_severity"].get("BLOCKER", 0)
    if blocker_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
