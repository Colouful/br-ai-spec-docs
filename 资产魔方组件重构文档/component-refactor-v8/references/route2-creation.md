
# Route2 Creation Reference

When creating a Page2 page, also create a matching route2 module.

## Required paths

Route modules directory:

```text
/Users/lizhenwei/workspace/vueworkspace/bairong/asset-cube-html/src/router/modules/
```

Router index registration file:

```text
/Users/lizhenwei/workspace/vueworkspace/bairong/asset-cube-html/src/router/index.js
```

## Procedure

1. Find the existing route module for the original page.
2. Copy the route module file.
3. Rename the copied file by adding `2`.
4. In the copied route module:
   - add `2` to route `path`;
   - add `2` to route `name` or use a unique suffix;
   - update component path to point to Page2;
   - preserve permission meta unless explicitly making a dev-only route;
   - optionally add `Page2` / `组件重构对照页` to title metadata.
5. Register the new route2 module in `src/router/index.js`.
6. Do not mutate or remove the original route module/import/registration.
