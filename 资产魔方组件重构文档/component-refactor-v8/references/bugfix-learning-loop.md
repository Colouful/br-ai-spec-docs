# Bugfix Learning Loop

This reference defines how the agent must handle bugs discovered after a component refactor.

## Goal

Every post-refactor bug fix must produce reusable learning:

1. What broke?
2. Why did it break?
3. How was it fixed?
4. How can the same class of bug be prevented next time?
5. Should the migration checklist, validation script, or mapping rule be updated?

## When to Use

Use this loop whenever the user says:

- 修复这个 bug
- 页面2有问题
- 迁移后报错
- ProTable 搜索不对
- ProModalForm 回填不对
- ProActions 按钮不对
- 路由打不开
- 权限不对
- 表单校验不对
- 导出参数不对
- 下次避免
- 记录问题

## Required Bugfix Workflow

### Step 1: Reproduce

Before changing code, identify:

- affected page
- Page1 behavior
- Page2 behavior
- reference behavior, if available
- exact operation that triggers the bug
- console/network error, if any

### Step 2: Classify

Pick one primary issue type:

| Type | Meaning |
| --- | --- |
| component-api-mismatch | New component API differs from old component behavior |
| request-params-mismatch | API request params changed unintentionally |
| response-mapping-mismatch | Response records/total/success mapping wrong |
| pagination-reset-bug | pageNo/pageSize/reset behavior differs |
| sorting-filter-bug | sorter/filter params differ |
| query-cache-bug | search cache or initial query restore differs |
| slot-scope-bug | row/record or slot name migration issue |
| permission-visibility-bug | auth visible/disabled behavior differs |
| action-behavior-bug | ProActions order/dropdown/confirm/click behavior differs |
| modal-lifecycle-bug | open/close/destroy/reset timing differs |
| form-backfill-bug | edit initial value/backfill timing wrong |
| form-validation-bug | rules, trigger, message, required behavior wrong |
| form-layout-bug | popup ProModalForm fields not one-row-per-field |
| modal-title-policy-bug | ProModalForm/Arco Modal titleAlign missing or wrong |
| drawer-over-customization-bug | unnecessary Drawer title alignment/style override |
| date-format-bug | date range/value format differs |
| amount-precision-bug | amount precision or display differs |
| dictionary-render-bug | status/dictionary label/color differs |
| empty-loading-error-state-bug | empty/loading/error UI differs |
| route2-registration-bug | Page2 route module/index registration wrong |
| reference-source-bug | wrong baseline/reference code used |
| style-regression | visual layout issue only |
| build-type-lint-bug | build/type/lint issue |
| unknown | not enough information yet |

### Step 3: Fix Minimally

Rules:

- Fix only the smallest affected Page2/local route/report area.
- Do not change original Page1.
- Do not change business semantics.
- Do not “improve” unrelated code.
- Do not modify shared API/store/permission logic unless explicitly approved.

### Step 4: Verify

Run relevant checks:

```bash
python3 scripts/validate_refactor.py --page2 <page2> --original <page1>
python3 scripts/check_route2.py --route2 <route2-file> --router-index src/router/index.js --expected-route-fragment <route2-fragment>
```

Also run project-level lint/typecheck/build/test if available.

### Step 5: Record

Append a bugfix record to:

```text
docs/component-refactor/bugfix-log.md
```

If the project does not have this directory, create it.

For page-level tracking, optionally also create:

```text
src/views/<module>/<page2>/__migration__/bugfix-log.md
```

Use `assets/bugfix-record-template.md`.

### Step 6: Prevention Rule

Every record must include at least one prevention rule.

Examples:

- “When migrating ProTable slots, always replace `{ row }` with `{ record }`.”
- “When migrating ProModalForm edit modal, verify backfill after async options resolve.”
- “When creating Page2, always create route2 and register in router/index.js.”
- “For popup ProModalForm, set `formProps.layout.columns=[1]` or `takeFullRow: true`.”
- “For ProActions, set `max-visible-count=2` unless exception is documented.”

### Step 7: Feed Back Into Future Tasks

If the issue is likely to repeat, update one of:

- `assets/edge-case-register-template.md`
- `assets/acceptance-report-template.md`
- `references/component-mapping.md`
- `references/page2-strategy.md`
- validation scripts

Do not modify the skill itself during a normal project migration unless the user explicitly asks to update the skill package.
