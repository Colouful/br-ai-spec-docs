
# ex-ux-kit Local Sources Reference

## Purpose

Use this reference whenever `@ex/ux-comp` behavior is unclear.

Do not guess Pro component APIs, passthrough props, slots, table request behavior, form layout behavior, or ProActions behavior.

## Local paths

### Component source

```text
/Users/lizhenwei/workspace/vueworkspace/bairong/ex-ux-kit/packages/component/src
```

### Component documentation

```text
/Users/lizhenwei/workspace/vueworkspace/bairong/ex-ux-kit/packages/component/docs
```

### Arco playground / demo source

```text
/Users/lizhenwei/workspace/vueworkspace/bairong/ex-ux-kit/playground/arco
```

## Lookup order

1. Read documentation first.
2. Read source implementation second.
3. Read playground examples third.
4. Read Arco docs when the Pro component passes through Arco props.

## Common lookup hints

| Topic | Prefer reading |
| --- | --- |
| `ProTable.request` params/result | docs + source for ProTable |
| table slots and `{ record }` | docs + playground examples |
| `ProModalForm modalProps` | docs + source for ProModalForm |
| one-row popup form layout | docs + source for ProModalForm fields/layout |
| `ProActions max-visible-count` | docs + source for ProActions |
| Arco Modal `titleAlign` passthrough | ProModalForm source + Arco modal docs |
| Drawer behavior | ProModalForm drawer source + Arco drawer docs |

## Rules

- Treat these paths as read-only references.
- Never modify component library source unless the user explicitly asks.
- Record consulted docs/source files in the final report.
- If source and docs differ, source behavior wins.
