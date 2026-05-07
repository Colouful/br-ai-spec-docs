# Component Mapping Reference

## 优先级

1. `@ex/ux-comp` Pro 组件（首选）
2. `@arco-design/web-vue` 回退组件
3. **绝不使用** `@koi-design/*`

## 完整映射表

| 旧组件/模式 | 新组件 | 关键注意 |
|-------------|--------|----------|
| DynamicsFilter + u-table | `ProTable` + `search` 属性 | 搜索字段和表格列合并到同一个 `columns` 数组；搜索字段用 `hideInTable: true` |
| u-table + pagination | `ProTable` | 保留 `rowKey`, selection, sorting, page-size-options |
| usePageList | `ProTable.request` | 返回 `{ data, total, success }`；`pageNo` → `pageNum` 参数映射 |
| useStorageQuery | sessionStorage 手动读写 | 参见 gold-standard 的 `getStoredQueryData` / `saveQueryData` 模式 |
| ColumnsSetting | ProTable 内置列设置 | 不要重复添加列设置 UI |
| TableHeader | ProTable `title` + `searchToolBarActions` | 保留 toolbar 权限和 loading 状态 |
| UModal + DynamicsForm | `ProModalForm type="modal"` | **必须** `:modal-props="{ titleAlign: 'start' }"` |
| EditDrawer | `ProModalForm type="drawer"` | **不要** titleAlign（Drawer 默认左对齐） |
| 页面内表单 | `ProModalForm type="form"` 或 Arco Form | 选择侵入性最小的方案 |
| ViewContent / u-info-view | `ProDescriptions` | `columns: [{ title: 'xxx', dataIndex: 'xxx' }]` |
| OneLineText | ProDescriptions 内置格式化 | 保留 formatter 和空值占位 |
| table row links | `ProActions type="link"` | `:max-visible-count="2"`；保留 auth/disabled/popconfirm |
| u-tooltip | `Tooltip` from `@arco-design/web-vue` | `import { Tooltip } from '@arco-design/web-vue'` |
| u-tag | `Tag` from `@arco-design/web-vue` | `import { Tag } from '@arco-design/web-vue'` |
| simple confirm modal | `Modal.confirm` | `titleAlign: 'start'` |
| Tabs/TabPane | `Tabs` + `TabPane` from `@arco-design/web-vue` | 参见 gold-standard Tab 容器模板 |
| u-button | `a-button` from `@arco-design/web-vue` | 直接替换 |
| u-select | `a-select` from `@arco-design/web-vue` | 注意 `mode` 属性差异 |
| u-input | `a-input` from `@arco-design/web-vue` | 直接替换 |
| u-date-picker | `a-date-picker` from `@arco-design/web-vue` | 注意 format 属性差异 |
| u-checkbox | `a-checkbox` from `@arco-design/web-vue` | 直接替换 |
| u-radio | `a-radio` from `@arco-design/web-vue` | 直接替换 |

## ViewContent → ProDescriptions 迁移详解

旧写法：
```vue
<ViewContent :columns="3">
  <u-info-view label="机构编号">{{ model.orgNo }}</u-info-view>
  <u-info-view label="机构名称">{{ model.orgName }}</u-info-view>
</ViewContent>
```

新写法：
```vue
<ProDescriptions :columns="descColumns" :data="model" />
```

```js
const descColumns = [
  { title: '机构编号', dataIndex: 'orgNo' },
  { title: '机构名称', dataIndex: 'orgName' },
];
```

## ProModalForm 弹窗单行布局规则

弹窗内所有表单项必须独占一行：

**表单级布局（首选）**：
```vue
<ProModalForm
  type="modal"
  :modal-props="{ titleAlign: 'start' }"
  :form-props="{
    layout: {
      mode: 'grid',
      columns: [24, 24, 24, 24],
      totalColumns: 24,
      gutter: 16
    },
    bordered: false
  }"
  :fields="fields"
/>
```

**字段级布局（兜底）**：
```js
const fields = [
  {
    label: '字段名',
    field: 'fieldName',
    valueType: 'input',
    takeFullRow: true,  // ← 必须
  },
];
```

## ProActions 标准写法

```vue
<ProActions
  type="link"
  :max-visible-count="2"
  :is-open-dropdown="false"
  :items="getRowActions(record)"
  :comp-props="{ underline: false }"
/>
```

## titleAlign 规则速查

| 场景 | 必须设置 |
|------|----------|
| ProModalForm type="modal" | `:modal-props="{ titleAlign: 'start' }"` |
| ProModalForm type="drawer" | **不要**设置 titleAlign |
| Arco Modal / a-modal | `title-align="start"` 或 `titleAlign: 'start'` |
| Modal.confirm | `titleAlign: 'start'` |
| Arco Drawer | **不要**设置 titleAlign（默认左对齐） |

## Arco 文档查找

本地文档（优先）：
```
/Users/lizhenwei/workspace/vueworkspace/bairong/arco-design-vue/packages/web-vue/components/xxx/README.zh-CN.md
```

在线文档（备选）：
```
https://arco.design/vue/component/xxx
```
