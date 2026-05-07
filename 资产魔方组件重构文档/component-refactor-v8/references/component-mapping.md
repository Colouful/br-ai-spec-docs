
# Component Mapping Reference

## Priority

1. Prefer `@ex/ux-comp` Pro components.
2. Use `@arco-design/web-vue` for fallback components.
3. Do not use `@koi-design/*`.

## Arco Documentation

Prefer local Arco Design Vue docs:

```text
/Users/lizhenwei/workspace/vueworkspace/bairong/arco-design-vue/packages/web-vue/components/xxx/README.zh-CN.md
```

Fallback online docs:

```text
https://arco.design/vue/component/xxx
```

## Mapping Table

| Old implementation | New implementation | Notes |
| --- | --- | --- |
| `DynamicsFilter + u-table` | `ProTable` with `search` | Merge search fields and table columns into one `columns` array |
| `u-table + pagination` | `ProTable` | Preserve `rowKey`, page size, selection, sorter |
| `usePageList` | `ProTable.request` | Return `{ data, total, success }`; preserve API params |
| `useStorageQuery` | `queryData` + local storage/session adapter | Preserve query cache and restore behavior |
| `ColumnsSetting` | ProTable built-in column setting | Do not duplicate column setting UI unless required |
| `TableHeader` | `title` + `searchToolBarActions` | Preserve toolbar permissions and loading states |
| `UModal + DynamicsForm` | `ProModalForm type="modal"` | Preserve fields, rules, initial values, submit behavior; use `:modal-props="{ titleAlign: 'start' }"` |
| `EditDrawer` | `ProModalForm type="drawer"` | Preserve drawer width and lifecycle; do not add title alignment override by default |
| page inline form | `ProModalForm type="form"` or Arco form | Pick least invasive option |
| `ViewContent` / `OneLineText` | `ProDescriptions` | Preserve formatter and empty text |
| table row operation links | `ProActions type="link"` with `max-visible-count="2"` | Preserve auth/disabled/popconfirm behavior; more than 2 actions fold by default |
| simple confirmation modal | Arco `Modal.confirm` / `a-modal` | Use `titleAlign: 'start'` / `title-align="start"` |

## v1.4.0 ProModalForm Popup One-Row Layout Rule

For popup form scenarios:

- `ProModalForm type="modal"`
- `ProModalForm type="drawer"`
- ProModalForm inside Modal / Drawer wrapper

Every form item must occupy one full row.

Preferred form-level pattern:

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

Preferred field-level pattern:

```ts
const fields = [
  {
    label: '字段名',
    field: 'fieldName',
    valueType: 'input',
    takeFullRow: true,
  },
];
```

Rules:

- Preserve field order.
- Preserve validation rules.
- Preserve backend field mapping.
- Preserve dynamic show/disabled logic.
- Preserve submit payload and API parameters.
- Record any exception in the acceptance report.
