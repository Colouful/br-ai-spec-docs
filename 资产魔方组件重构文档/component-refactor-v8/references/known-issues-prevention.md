
# Known Issues Prevention

This file is the stable summary of repeated migration bugs and prevention rules.

Agents must read this before starting a new migration or bug fix if it exists in the project at:

```text
docs/component-refactor/known-issues-prevention.md
```

## Format

| Issue type | Symptom | Prevention rule | Related check |
| --- | --- | --- | --- |
| slot-scope-bug | Table cell data not displayed | ProTable scoped slots use `{ record }`, not `{ row }` | inspect table slots |
| route2-registration-bug | Page2 route cannot open | Create route2 file and register it in `src/router/index.js` | `check_route2.py` |
| form-layout-bug | Popup form fields render two columns | Popup ProModalForm fields must occupy one full row | `check_promodalform_one_row.sh` |
| modal-title-policy-bug | Modal title centered | ProModalForm modal uses `modalProps.titleAlign='start'`; Arco Modal uses `titleAlign='start'` | inspect modal props |
| action-behavior-bug | Too many row actions visible | ProActions uses `max-visible-count=2` unless exception documented | inspect ProActions |
| build-type-lint-bug | ESLint fails after AI edit | Run changed-files ESLint after every meaningful edit | `check_changed_eslint.py` |

When a new bug class repeats, add a new row.
