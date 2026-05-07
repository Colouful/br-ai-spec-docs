\
#!/usr/bin/env python3
"""
Append a structured bugfix record to a markdown log.

Example:
  python3 scripts/record_bugfix.py \
    --log docs/component-refactor/bugfix-log.md \
    --issue-type form-backfill-bug \
    --page2 src/views/foo/bar2 \
    --summary "Edit modal values did not backfill" \
    --root-cause "Backfill ran before async options loaded" \
    --fix "Moved setFieldsValue after options resolved" \
    --prevention "For edit ProModalForm, verify async options before backfill"
"""
import argparse
from pathlib import Path
from datetime import datetime

VALID_TYPES = {
    "component-api-mismatch",
    "request-params-mismatch",
    "response-mapping-mismatch",
    "pagination-reset-bug",
    "sorting-filter-bug",
    "query-cache-bug",
    "slot-scope-bug",
    "permission-visibility-bug",
    "action-behavior-bug",
    "modal-lifecycle-bug",
    "form-backfill-bug",
    "form-validation-bug",
    "form-layout-bug",
    "modal-title-policy-bug",
    "drawer-over-customization-bug",
    "date-format-bug",
    "amount-precision-bug",
    "dictionary-render-bug",
    "empty-loading-error-state-bug",
    "route2-registration-bug",
    "reference-source-bug",
    "style-regression",
    "build-type-lint-bug",
    "unknown",
}

def main():
    parser = argparse.ArgumentParser(description="Append a component-refactor bugfix record.")
    parser.add_argument("--log", default="docs/component-refactor/bugfix-log.md")
    parser.add_argument("--issue-type", required=True, choices=sorted(VALID_TYPES))
    parser.add_argument("--page1", default="")
    parser.add_argument("--page2", required=True)
    parser.add_argument("--route2", default="")
    parser.add_argument("--severity", default="medium", choices=["blocker", "high", "medium", "low"])
    parser.add_argument("--summary", required=True)
    parser.add_argument("--root-cause", required=True)
    parser.add_argument("--fix", required=True)
    parser.add_argument("--verification", default="")
    parser.add_argument("--prevention", required=True)
    parser.add_argument("--files-changed", default="")
    args = parser.parse_args()

    log_path = Path(args.log)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    if not log_path.exists():
        log_path.write_text("# Component Refactor Bugfix Log\n\n", encoding="utf-8")

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    entry = f"""
## {now} - {args.issue_type}

| Item | Value |
| --- | --- |
| Severity | {args.severity} |
| Page1 | {args.page1} |
| Page2 | {args.page2} |
| Route2 | {args.route2} |
| Summary | {args.summary} |
| Files changed | {args.files_changed} |

### Root Cause

{args.root_cause}

### Fix

{args.fix}

### Verification

{args.verification or "Not provided"}

### How to Avoid Next Time

{args.prevention}

---
"""

    with log_path.open("a", encoding="utf-8") as f:
        f.write(entry)

    print(f"Bugfix record appended: {log_path}")

if __name__ == "__main__":
    main()
