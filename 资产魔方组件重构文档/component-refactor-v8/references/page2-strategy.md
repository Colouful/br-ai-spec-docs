
# Page2 Shadow Refactor Strategy

## Reference source selection

If a target page is under:

```text
src/views/disposalTool
```

the current code may already be migrated once. Do not use it as old-logic baseline without verification.

Preferred baseline order:

1. Separate pre-refactor reference directory created from the unrefactored branch.
2. Original Page1 only if confirmed still legacy.
3. Existing migrated sample only for migration pattern, not old business behavior.

## Route2 requirement

Creating Page2 is not enough.

Also create:

```text
src/router/modules/<route-file>2.js
```

Then register it in:

```text
src/router/index.js
```

Route2 must add `2` to route path, name/key, component file path, and route module file name.

## Visual Consistency Policy

- `ProModalForm type="modal"` must pass `:modal-props="{ titleAlign: 'start' }"`.
- Arco Modal must use `title-align="start"` or `titleAlign: 'start'`.
- Drawer title is already left-aligned by default; do not add unnecessary title alignment override.
- `ProActions` must use `max-visible-count="2"` by default.

## v1.4.0 Popup Form Layout Policy

For Page2 popup forms using `ProModalForm`:

- every form item must occupy one full row;
- prefer `formProps.layout.columns: [1]`;
- use field `takeFullRow: true` when necessary;
- do not change validation, payload, API parameters, or field dependency logic for layout;
- record exceptions in the acceptance report.
