#!/usr/bin/env bash
set -euo pipefail
TARGET="${1:-}"
if [[ -z "$TARGET" ]]; then
  echo "Usage: $0 <page2-path>" >&2
  exit 2
fi
if [[ ! -d "$TARGET" ]]; then
  echo "Target directory not found: $TARGET" >&2
  exit 2
fi
FILES=$(grep -Rsl "ProModalForm" "$TARGET" --include='*.vue' --include='*.js' --include='*.ts' || true)
STATUS=0
for f in $FILES; do
  if grep -Eq "type=['\"](modal|drawer)['\"]" "$f"; then
    if ! grep -Eq "columns:[[:space:]]*\[[[:space:]]*1[[:space:]]*\]|columns:[[:space:]]*\[1\]|takeFullRow:[[:space:]]*true|take-full-row" "$f"; then
      echo "WARN: $f uses popup ProModalForm but one-row layout is not obvious. Prefer formProps.layout.columns=[1] or field takeFullRow=true."
      STATUS=1
    fi
  fi
done
exit $STATUS
