
---
name: component-refactor
description: Refactor Vue financial middle-platform pages in local project /Users/lizhenwei/workspace/vueworkspace/bairong/asset-cube-html from old UI components such as Koi Design, DynamicsFilter, DynamicsForm, u-table, UModal, EditDrawer, ViewContent, OneLineText, and u-* tags to @ex/ux-comp Pro components and Arco fallback components. Use for Page2 shadow refactor, route2 creation under src/router/modules, router/index.js registration, ProTable/ProModalForm/ProActions replacement, strict no-business-logic-change component restructuring, ProModalForm/Arco Modal titleAlign standardization, local Arco docs lookup, and ProActions max-visible-count standardization.
license: Proprietary
compatibility: Designed for Open Agent Skills-compatible coding agents such as OpenAI Codex, GitHub Copilot, Claude Code, Cursor, Hermes, or similar.
metadata:
  author: generated-for-tom
  version: "1.7.0"
  domain: vue-financial-middle-platform-component-migration
  primary_strategy: page2-shadow-refactor
  local_project_root: /Users/lizhenwei/workspace/vueworkspace/bairong/asset-cube-html
  local_router_modules: /Users/lizhenwei/workspace/vueworkspace/bairong/asset-cube-html/src/router/modules
  local_router_index: /Users/lizhenwei/workspace/vueworkspace/bairong/asset-cube-html/src/router/index.js
  local_arco_docs_root: /Users/lizhenwei/workspace/vueworkspace/bairong/arco-design-vue/packages/web-vue/components
allowed-tools: Read Write Edit Bash(git:*) Bash(grep:*) Bash(python:*) Bash(npm:*) Bash(pnpm:*) Bash(find:*) Bash(ls:*) Bash(cat:*)
---

# Component Refactor Skill

## Mission

Use this skill to perform a controlled UI component refactor in the local Vue financial middle-platform project:

```text
/Users/lizhenwei/workspace/vueworkspace/bairong/asset-cube-html
```

This is a reversible Page2 migration with strict business-behavior preservation.

Primary goals:

1. Create or update a Page2 shadow implementation.
2. Create a matching route2 module under `src/router/modules`.
3. Register the new route2 module in `src/router/index.js`.
4. Replace old UI components with `@ex/ux-comp` Pro components first.
5. Use `@arco-design/web-vue` only as fallback.
6. Preserve business logic, API semantics, permissions, validation intent, and edge behavior.
7. Use unrefactored reference code when available, especially for areas that were already migrated once.
8. Enforce `ProModalForm type="modal"` and Arco `Modal` title alignment through `titleAlign: 'start'`.
9. Do not add unnecessary title alignment changes for Arco `Drawer`, because Drawer title is already left-aligned by default.
10. Enforce `ProActions` visible operation count standard: `max-visible-count="2"`.
11. Produce migration inventory, route2 evidence, edge-case register, test matrix, and acceptance result.

## Local Project Context

Active project:

```text
/Users/lizhenwei/workspace/vueworkspace/bairong/asset-cube-html
```

Router modules:

```text
/Users/lizhenwei/workspace/vueworkspace/bairong/asset-cube-html/src/router/modules/
```

Router index:

```text
/Users/lizhenwei/workspace/vueworkspace/bairong/asset-cube-html/src/router/index.js
```

Local Arco docs root:

```text
/Users/lizhenwei/workspace/vueworkspace/bairong/arco-design-vue/packages/web-vue/components
```

Arco local docs pattern:

```text
/Users/lizhenwei/workspace/vueworkspace/bairong/arco-design-vue/packages/web-vue/components/xxx/README.zh-CN.md
```

Online fallback pattern:

```text
https://arco.design/vue/component/xxx
```

## Critical Reference-Code Warning

Files under this directory have already been migrated once:

```text
/Users/lizhenwei/workspace/vueworkspace/bairong/asset-cube-html/src/views/disposalTool
```

Do not assume these files still represent original legacy logic.

When migrating or comparing pages under `src/views/disposalTool`:

1. Do not use current `disposalTool` files as old-logic baseline unless verified.
2. Prefer the separate directory created from the unrefactored branch.
3. Treat the unrefactored reference directory as the source of truth for old behavior.
4. If the reference directory path appears identical to the active project path, verify file content before trusting it.
5. If no reliable reference exists, stop and report the uncertainty.

Read `references/local-project-context.md` before planning.

## Hard Rules

Never modify these unless the user explicitly approves a separate business-change task:

- original Page1 files
- shared API modules
- store modules
- router business behavior unrelated to Page2 route registration
- permission/auth logic
- domain constants or dictionaries
- backend request/response contracts
- event handler business bodies
- validation intent
- amount/date/status semantics
- export/download/batch-operation parameter semantics

Allowed changes:

- new Page2 files
- Page2 local imports, templates, styles
- copied route2 module under `src/router/modules`
- `src/router/index.js` import/registration for route2
- Page2 local adapter functions required by new component APIs
- Page2 local tests and reports

## Page2 Route Creation Rules

When creating Page2, also create a route2 module.

For a target route module under:

```text
src/router/modules/<route-file>.js
```

copy it to:

```text
src/router/modules/<route-file>2.js
```

Inside the copied route2 file:

- route `path` / access address must add `2`;
- route `name` should add `2` or another unique suffix;
- component import path must point to Page2;
- menu metadata title can add `2`, `Page2`, or `组件重构对照页`;
- preserve permission meta unless a dev-only route is intentionally used;
- do not alter the original route module.

Example:

```js
// original
path: '/disposalTool/returnCallList',
component: () => import('@/views/disposalTool/returnCallList/index.vue')

// page2
path: '/disposalTool/returnCallList2',
component: () => import('@/views/disposalTool/returnCallList2/index.vue')
```

After creating route2, register it in:

```text
src/router/index.js
```

Rules:

- import the new route2 module;
- add it to the same route collection pattern used by the project;
- do not remove or mutate the original route registration;
- keep the registration minimal and reversible.

Read `references/route2-creation.md` before editing routes.

## Arco Documentation Rule

When using Arco Design Vue fallback components, prefer local documentation first:

```text
/Users/lizhenwei/workspace/vueworkspace/bairong/arco-design-vue/packages/web-vue/components/xxx/README.zh-CN.md
```

If local docs are unavailable, use online docs:

```text
https://arco.design/vue/component/xxx
```

Supported local `xxx` values are listed in `references/arco-local-docs-index.md`.



## Absolute No Business Logic Change Rule

This skill is allowed to refactor UI component implementation only.

It must not change existing business logic.

Strictly forbidden without explicit human approval:

- changing API names, request parameters, response mapping semantics, or backend contracts;
- changing store usage or state meaning;
- changing permission/auth logic;
- changing router business behavior except adding Page2 route2 registration;
- changing event handler business body;
- changing validation intent, required rules, or validation messages;
- changing export/download/batch operation parameter semantics;
- changing amount/date/status/dictionary business meaning;
- changing computed/watch/ref/reactive business meaning;
- changing domain constants, enums, or dictionaries;
- optimizing, simplifying, or rewriting unrelated logic.

Allowed:

- UI component imports;
- Page2-only template/component replacement;
- Page2-only style/layout changes;
- Page2-only adapter code required by new component APIs;
- route2 addition and router/index.js registration for Page2;
- test/report/bugfix-log files.

If a desired fix requires changing business logic, stop and report the risk instead of editing.


## ex-ux-kit Local Source and Documentation Lookup

When encountering any issue related to `@ex/ux-comp`, Pro components, props, slots, form layout, table request behavior, modalProps passthrough, or ProActions behavior, do not guess.

Read these local sources first:

### Component source

```text
/Users/lizhenwei/workspace/vueworkspace/bairong/ex-ux-kit/packages/component/src
```

### Component documentation

```text
/Users/lizhenwei/workspace/vueworkspace/bairong/ex-ux-kit/packages/component/docs
```

### Playground / demo source

```text
/Users/lizhenwei/workspace/vueworkspace/bairong/ex-ux-kit/playground/arco
```

Priority order when debugging Pro component issues:

1. Read component docs under `packages/component/docs`.
2. Read component source under `packages/component/src`.
3. Read playground examples under `playground/arco`.
4. Read local Arco docs under `/Users/lizhenwei/workspace/vueworkspace/bairong/arco-design-vue/packages/web-vue/components/xxx/README.zh-CN.md`.
5. Only then implement the smallest Page2-local fix.

Rules:

- Treat `ex-ux-kit` as read-only reference unless the user explicitly asks to modify the component library itself.
- Do not patch component library source to fix a Page2 migration issue.
- Record consulted docs/source files in the final report when they influenced the fix.
- If docs and source conflict, source behavior wins; document the mismatch.


## Bugfix Memory Pre-Read Gate

Before starting any new migration or bug fix, read previous bugfix records and apply prevention rules.

Required sources:

```text
docs/component-refactor/bugfix-log.md
docs/component-refactor/known-issues-prevention.md
src/views/<module>/<page2>/__migration__/bugfix-log.md
```

If these files exist, read them before editing.

Required behavior:

1. Extract recurring issue types.
2. Extract prevention rules from “How to Avoid Next Time” sections.
3. Apply those rules as hard constraints for the current task.
4. Mention applied learned constraints in the inventory/final report.
5. If a similar issue is found, prioritize the known prevention rule.
6. If a new issue is fixed, append a bugfix record and add/update a prevention rule.

Use:

```bash
python3 scripts/read_bugfix_memory.py
```

or for a specific page:

```bash
python3 scripts/read_bugfix_memory.py --page2 src/views/example/page2
```

This turns past migration bugs into future migration constraints.

## UI Consistency Rules

### ProModalForm modal title alignment

Required pattern:

```vue
<ProModalForm
  type="modal"
  title="编辑"
  :modal-props="{ titleAlign: 'start' }"
/>
```

Rules:

- Use `modalProps` / `modal-props` to pass `titleAlign: 'start'`.
- Do not use CSS as the first choice when `modalProps.titleAlign` can solve the problem.
- Do not use `titleAlign: 'center'`.
- Preserve modal lifecycle and submit behavior.
- If a local wrapper hides `modalProps`, stop and report the wrapper limitation before using invasive workarounds.

### Arco Modal title alignment

Template pattern:

```vue
<a-modal
  v-model:visible="visible"
  title="提示"
  title-align="start"
>
  ...
</a-modal>
```

Programmatic pattern:

```ts
Modal.confirm({
  title: '提示',
  titleAlign: 'start',
  content: '确认操作？',
});
```

Rules:

- Use Arco Modal's `titleAlign` prop.
- Valid values are `'start'` and `'center'`.
- Use `'start'`.

### Arco Drawer title alignment

Do not add extra title alignment logic for Arco Drawer by default.

Rules:

- Drawer title is already left-aligned by default.
- Do not add `titleAlign` to Drawer.
- Do not add CSS just to align Drawer title.
- Only touch Drawer title layout if the existing page has a real visual bug or a wrapper changed the default.

### ProActions visible count

Required pattern:

```vue
<ProActions
  type="link"
  :max-visible-count="2"
/>
```

Rules:

- Preserve action order.
- Preserve permission visibility.
- Preserve disabled state.
- Preserve confirm/delete popconfirm behavior.
- More than 2 visible actions must fold into dropdown behavior if supported.
- If `isOpenDropdown=false`, no dropdown, or a different visible count is required to preserve old behavior, record the exception in the acceptance report.

## Activation Checklist

Before editing, identify:

- source Page1 path
- target Page2 path
- reference pre-refactor path, if any
- whether target is under `src/views/disposalTool`
- old UI components
- APIs and request parameters
- search fields
- table columns
- slots and scoped variables
- modals/drawers/forms
- row operations and toolbar actions
- route module file under `src/router/modules`
- target route2 file name
- `router/index.js` registration pattern
- permission/disabled/tooltip logic
- boundary logic: empty values, dates, amounts, dictionaries, sorting, pagination, query cache
- whether popup is `ProModalForm`, Arco `Modal`, or Arco `Drawer`
- whether `ProModalForm type="modal"` has `modalProps.titleAlign = 'start'`
- whether Arco `a-modal` / `Modal.confirm` has `titleAlign = 'start'`
- whether `ProActions` has `max-visible-count="2"`

Use `assets/inventory-template.md`.

## Default Strategy

1. Locate original Page1.
2. Locate pre-refactor reference code when available.
3. If Page1 is under `src/views/disposalTool`, do not trust current Page1 as original legacy behavior unless verified.
4. Copy Page1 or the pre-refactor reference page into Page2 according to task context.
5. Create matching route2 module under `src/router/modules`.
6. Register route2 in `src/router/index.js`.
7. Confirm Page2 opens before component replacement.
8. Keep Page1 unchanged.
9. Refactor components only inside Page2.
10. Compare Page1/Page2 and reference behavior.
11. Accept Page2 only after validation passes.

Read:

- `references/local-project-context.md`
- `references/page2-strategy.md`
- `references/route2-creation.md`
- `references/component-mapping.md`

## Component Priority

1. `@ex/ux-comp` Pro components
2. `@arco-design/web-vue` fallback components
3. Do not keep or introduce `@koi-design/*`

## Refactor Workflow

- [ ] Read local project context and route2 rules
- [ ] Inventory Page1 and reference source
- [ ] Create Page2 clone
- [ ] Create route2 module under `src/router/modules`
- [ ] Register route2 in `src/router/index.js`
- [ ] Confirm Page1 has no diff
- [ ] Refactor list/search/table
- [ ] Refactor row actions and toolbars; set `ProActions :max-visible-count="2"`
- [ ] Refactor modal forms; for `ProModalForm type="modal"`, pass `:modal-props="{ titleAlign: 'start' }"`
- [ ] Refactor Arco Modal; use `title-align="start"` or `titleAlign: 'start'`
- [ ] Refactor Drawer only for behavior/style needs; do not add unnecessary title alignment logic
- [ ] Refactor descriptions/detail/empty/layout areas
- [ ] Register boundary logic
- [ ] Run validation scripts
- [ ] Run changed-files ESLint using `scripts/check_changed_eslint.py`, then run project lint/typecheck/build/tests if available
- [ ] Produce acceptance report

## Available Scripts

- `scripts/scan_components.py`
- `scripts/validate_refactor.py`
- `scripts/check_route2.py`

Run examples:

```bash
python3 scripts/scan_components.py --target src/views/example/page2
python3 scripts/validate_refactor.py --page2 src/views/example/page2 --original src/views/example/page
python3 scripts/check_route2.py --route2 src/router/modules/example2.js --router-index src/router/index.js --expected-route-fragment example2
```

## Gotchas

- For `src/views/disposalTool`, current files may already be migrated; do not use them as old-logic baseline without verification.
- Always look for a pre-refactor reference directory before comparing historical logic.
- Creating Page2 is not enough; create route2 and register it in `src/router/index.js`.
- Route2 path, route name, and component path should add `2` or an equivalent unique suffix.
- ProTable slots use `{ record }`, not old `{ row }`.
- `actionRef.reload(true)` means reload and reset to page 1; use it only when old behavior did that.
- Date range fields often require adapter logic; never silently change backend parameter names.
- Amount fields must preserve precision and display fallback.
- Permission logic must be copied as-is, not simplified into UI-only assumptions.
- Query cache must be explicitly preserved when replacing `useStorageQuery`.
- Row selection and batch operation keys must use the same identity as the original table.
- For `ProModalForm type="modal"`, use `modalProps` to pass `{ titleAlign: 'start' }`.
- For Arco Modal, use `title-align="start"` or `titleAlign: 'start'`.
- Do not add Drawer title alignment changes by default.
- `ProActions` should set `max-visible-count` to `2` by default; document any exception.
- Local Arco docs path is `/Users/lizhenwei/workspace/vueworkspace/bairong/arco-design-vue/packages/web-vue/components/xxx/README.zh-CN.md`.
- Online Arco docs path is `https://arco.design/vue/component/xxx`.

## Final Output Required

When done, output:

```markdown
# Component Refactor Result

## Summary
- Project root:
- Reference source:
- Original page:
- Page2 page:
- Route2 module:
- Router index registration:
- Refactored areas:
- Not refactored areas:

## Files changed
| File | Change | Reason |
| --- | --- | --- |

## Original page protection
- Git diff result:
- Any non-Page2 changes:

## Learned constraints applied
| Source | Rule applied | Evidence |
| --- | --- | --- |

## Reference logic
- Reference path used:
- Why this reference is trustworthy:
- Whether target is under disposalTool:

## Route2
| Item | Result | Evidence |
| --- | --- | --- |
| route2 file created | | |
| route path adds 2 | | |
| component path points to Page2 | | |
| router/index.js registered | | |

## Component docs/source consulted
| Source | Why consulted | Finding |
| --- | --- | --- |

## Component mapping
| Old component | New component | Location | Notes |
| --- | --- | --- | --- |

## UI consistency
| Requirement | Result | Evidence / Exception |
| --- | --- | --- |
| ProModalForm modal uses modalProps.titleAlign='start' | | |
| Arco Modal uses titleAlign='start' | | |
| Drawer has no unnecessary title alignment override | | |
| ProActions max-visible-count=2 | | |

## Boundary logic register
| Case | Original/reference behavior | Page2 behavior | Match | Risk |
| --- | --- | --- | --- | --- |

## Tests
| Check | Command / Method | Result |
| --- | --- | --- |
| Changed-files ESLint | `python3 scripts/check_changed_eslint.py` | |

## Acceptance
- [ ] Pass
- [ ] Conditional pass
- [ ] Fail

## Bugfix learning
| Item | Result |
| --- | --- |
| Issue type | |
| Root cause | |
| Fix summary | |
| How to avoid next time | |
| Bugfix log updated | |

## Risks and follow-ups
```

## Stop Conditions

Stop and report instead of guessing if:

- the pre-refactor reference directory cannot be found for already-migrated areas
- current `src/views/disposalTool` is the only available reference for old logic
- route2 cannot be safely registered in `router/index.js`
- a change requires modifying shared business logic
- API parameter meaning is unclear
- old component behavior cannot be inferred
- permission behavior is mixed into UI config and risks changing logic
- Page2 route cannot be added safely
- new component lacks equivalent behavior
- Page1/Page2/reference behavior does not match after migration
- `ProModalForm` wrapper does not expose `modalProps`
- Arco Modal title alignment cannot be set through `titleAlign`
- `ProActions max-visible-count=2` breaks required old action behavior and needs human decision
```

## v1.4.0 Addendum: ProModalForm Popup Form Items Must Occupy One Full Row

When using `ProModalForm` inside a popup container, every form item must occupy one full row.

Applies to:

- `ProModalForm type="modal"`
- `ProModalForm type="drawer"`
- any local wrapper that renders a ProModalForm inside Modal / Drawer

Required behavior:

- Each form item is displayed on its own row.
- Do not render two or more form items in the same row inside popup forms.
- Preserve original field order.
- Preserve field names, validation rules, backend mappings, dynamic show/disabled logic, and dependency logic.

Preferred implementation:

```vue
<ProModalForm
  type="modal"
  :modal-props="{ titleAlign: 'start' }"
  :form-props="{
    layout: {
      mode: 'grid',
      columns: [1],
    },
  }"
  :fields="fields"
/>
```

Field-level fallback:

```ts
const fields = [
  {
    label: '名称',
    field: 'name',
    valueType: 'input',
    takeFullRow: true,
  },
];
```

Rules:

- Prefer form-level one-column layout: `formProps.layout.columns: [1]`.
- Use field-level `takeFullRow: true` when form-level layout is not enough.
- Do not change validation intent to achieve the layout.
- Do not change data transform, submit payload, API parameters, or field dependency behavior to achieve the layout.
- If a specific field intentionally needs custom inline layout, record the exception in the acceptance report.

Additional validation requirement:

- Final output must include evidence that popup `ProModalForm` fields occupy one full row, or explain the documented exception.


## Changed Files ESLint Gate

After every AI code modification, run ESLint on the files changed by the current task.

Required command:

```bash
python3 scripts/check_changed_eslint.py
```

If running from the project root and the skill is installed under `.agents/skills/component-refactor`:

```bash
python3 .agents/skills/component-refactor/scripts/check_changed_eslint.py
```

If the changed files are known:

```bash
python3 scripts/check_changed_eslint.py --files <file1> <file2>
```

Rules:

- Run this after each meaningful edit, not only at the end.
- Fix ESLint issues before continuing to the next migration area.
- Do not change business logic to satisfy ESLint.
- Prefer minimal import cleanup, variable cleanup, formatting, and syntax fixes.
- If `--fix` is used, inspect the diff afterward.
- Include the changed-files ESLint result in the final acceptance report.

Read `references/changed-files-eslint-gate.md` for details.

## Bugfix Learning Loop

When the user reports a bug after migration, do not only patch the code. Every bug fix must create a reusable record.

Required after each bug fix:

1. classify the issue type;
2. describe the root cause;
3. describe the minimal fix;
4. record changed files;
5. verify Page1 remains unchanged;
6. verify Page2 behavior;
7. write how to avoid the same issue next time;
8. append a record to `docs/component-refactor/bugfix-log.md`.

Use:

- `references/bugfix-learning-loop.md`
- `assets/bugfix-record-template.md`
- `scripts/record_bugfix.py`

Required issue types include:

- component-api-mismatch
- request-params-mismatch
- response-mapping-mismatch
- pagination-reset-bug
- sorting-filter-bug
- query-cache-bug
- slot-scope-bug
- permission-visibility-bug
- action-behavior-bug
- modal-lifecycle-bug
- form-backfill-bug
- form-validation-bug
- form-layout-bug
- modal-title-policy-bug
- drawer-over-customization-bug
- date-format-bug
- amount-precision-bug
- dictionary-render-bug
- empty-loading-error-state-bug
- route2-registration-bug
- reference-source-bug
- style-regression
- build-type-lint-bug
- unknown

Bugfix rules:

- Fix the smallest affected scope.
- Do not modify original Page1.
- Do not change business semantics.
- Do not change shared API/store/permission logic unless explicitly approved.
- If the same issue type appears repeatedly, suggest updating the migration checklist, validation script, or component mapping reference.

- Bug fixes must record issue type, root cause, fix, verification, and prevention rule before closure.

- Changed-files ESLint must pass before acceptance; if it fails, fix reported files before continuing.
