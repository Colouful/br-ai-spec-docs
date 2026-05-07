---
name: component-refactor
description: "Examples-first Vue component migration: @koi-design → @ex/ux-comp Pro + @arco-design/web-vue fallback. 19 anti-patterns, gold-standard templates, auto-audit."
license: Proprietary
metadata:
  author: lizhenwei
  version: "2.0.0"
  domain: vue-financial-middle-platform-component-migration
  primary_strategy: examples-first-page2-shadow-refactor
  local_project_root: /Users/lizhenwei/workspace/vueworkspace/bairong/asset-cube-html
  local_router_modules: /Users/lizhenwei/workspace/vueworkspace/bairong/asset-cube-html/src/router/modules
  local_router_index: /Users/lizhenwei/workspace/vueworkspace/bairong/asset-cube-html/src/router/index.js
  local_arco_docs_root: /Users/lizhenwei/workspace/vueworkspace/bairong/arco-design-vue/packages/web-vue/components
allowed-tools: Read Write Edit Bash(git:*) Bash(grep:*) Bash(python:*) Bash(npm:*) Bash(pnpm:*) Bash(find:*) Bash(ls:*) Bash(cat:*)
---

# Component Refactor Skill v2.0

## 核心理念: Examples-First, Rules-Second

旧版 v1.x 用 170+ 行规则描述迁移方法，AI 仍然反复犯同样的错。
根本原因：规则是抽象的，代码是具体的。

v2.0 设计：
1. **先看真实代码模板** → 知道"正确长什么样"
2. **再看反模式** → 知道"什么绝对不能做"
3. **每步验证** → 不等到最后才发现问题
4. **自动审计** → 脚本生成 diff 报告

## 前置必读（按顺序）

迁移开始前，必须按此顺序阅读：

```
1. references/gold-standard-examples.md    ← 先看正确代码长什么样
2. references/anti-patterns.md             ← 再看19个血泪教训
3. references/component-mapping.md         ← 组件映射速查表
4. references/audit-checklist.md           ← 验证清单
```

---

## Phase 0: 接收任务

**输入**: 用户告知要迁移的页面路径，例如 `src/views/disposalTool/xxxManagement`

**输出**: 确认以下信息后开始

| 项目 | 必须确认 |
|------|----------|
| Page1 源路径 | `src/views/disposalTool/<page>/` |
| Page2 目标路径 | `src/views/disposalTool2/<page>/` |
| 参考文件（如有） | `src/views/disposalTool2/disposalManagement/` |
| 路由模块文件 | `src/router/modules/<route>.js` |
| 已有 Page2 是否已存在 | 如存在则增量更新 |

**STOP 条件**:
- Page1 路径不存在 → 报错退出
- 路由模块文件不存在 → 报错退出

---

## Phase 1: 扫描（Scan）

扫描 Page1 所有 `.vue` 文件，识别需要替换的旧组件。

### 扫描清单

```bash
# 自动扫描旧组件
grep -rn "@koi-design\|DynamicsFilter\|DynamicsForm\|u-table\|UModal\|EditDrawer\|ViewContent\|u-tooltip\|u-tag\|OneLineText\|usePageList\|useStorageQuery\|ColumnsSetting\|TableHeader" src/views/disposalTool/<page>/
```

### 组件映射（速查，详见 references/component-mapping.md）

| 旧组件 | 新组件 | 关键注意 |
|--------|--------|----------|
| DynamicsFilter + u-table | ProTable + search | 搜索+表格合并到 columns |
| u-table + pagination | ProTable | 保留 rowKey, selection, sorting |
| usePageList | ProTable.request | return {data, total, success} |
| UModal + DynamicsForm | ProModalForm type="modal" | **必须** :modal-props="{titleAlign:'start'}" |
| EditDrawer | ProModalForm type="drawer" | **不要** titleAlign |
| ViewContent / u-info-view | ProDescriptions | columns: [{title, dataIndex}] |
| table row links | ProActions type="link" | :max-visible-count="2" |
| u-tooltip | Tooltip from @arco-design/web-vue | 直接替换 |
| u-tag | Tag from @arco-design/web-vue | 直接替换 |
| simple confirm modal | Modal.confirm | titleAlign: 'start' |

**STOP 条件**:
- 发现无法映射的旧组件 → 记录并报告用户
- 旧组件来自项目私有封装而非 @koi-design → 报告用户

---

## Phase 2: 复制（Copy）

### 2.1 创建 Page2 目录
```bash
cp -r src/views/disposalTool/<page> src/views/disposalTool2/<page>
```

### 2.2 创建 Route2 模块
```bash
cp src/router/modules/<route>.js src/router/modules/<route>2.js
```

Route2 修改规则：
```js
// 原版
path: '/disposalTool/xxx',
name: 'Xxx',
component: () => import('@/views/disposalTool/xxx/index.vue')

// Page2
path: '/disposalTool/xxx2',
name: 'Xxx2',
component: () => import('@/views/disposalTool2/xxx/index.vue')
```

### 2.3 注册路由

在 `src/router/index.js` 中添加 route2 import 和注册。

**STOP 条件**:
- `router/index.js` 注册模式无法识别 → 报告用户
- Page2 目录已存在且有未提交改动 → 报告用户

---

## Phase 3: 重构（Refactor）

**核心原则：每个文件重构时，先打开 gold-standard-examples.md 中对应的模板，严格对照。**

### 3.1 Tab 容器页（index.vue）

**模板**: 见 `references/gold-standard-examples.md` → "Tab 容器模板"

关键点：
- 使用 `Tabs` + `TabPane` from `@arco-design/web-vue`
- `provide('tabIndex', tabIndex)` 给子组件
- 监听路由 query 同步 tab 状态

### 3.2 ProTable 列表页（todoList.vue, completedList.vue 等）

**模板**: 见 `references/gold-standard-examples.md` → "ProTable 列表模板"

关键点：
- `tableProps = { scroll: { x: 'max-content', y: 500 } }` ← **必须包含 y**
- `saveQueryData` 前**必须排除分页参数**: `const { pageNo, pageSize, ...queryOnly } = params`
- `handleRequest` 返回 `{ data, total, success }`
- GET API 使用 `params` 不是 `data`

### 3.3 ProModalForm 弹窗组件

**模板**: 见 `references/gold-standard-examples.md` → "ProModalForm 弹窗模板"

**这是最容易出错的地方，必须严格对照模板！**

关键点（来自 19 个真实 bug）：
1. **必须** `emit('update:visible', false)` 在 handleFinish 成功路径
2. **必须** `:modal-props="{ titleAlign: 'start' }"` 对于 type="modal"
3. **所有字段必须** `takeFullRow: true`
4. **onChange 必须**在异步操作前同步更新 `model.xxx`
5. **onChange 必须**添加 `instanceof Event` 类型守卫
6. **只读字段**用 `valueType: 'input'` + `fieldProps: { disabled: true }`，**不要用** `valueType: 'text'`

### 3.4 ProDescriptions 详情页

**模板**: 见 `references/gold-standard-examples.md` → "ProDescriptions 详情模板"

关键点：
- `columns: [{ title: '机构编号', dataIndex: 'orgNo' }]`
- 不要使用 `ViewContent` 或 `u-info-view`

### 3.5 ProActions 行操作

```vue
<ProActions
  type="link"
  :max-visible-count="2"
  :is-open-dropdown="false"
  :items="getRowActions(record)"
  :comp-props="{ underline: false }"
/>
```

---

## Phase 4: 验证（Verify）

### 4.1 反模式检查（逐条）

对照 `references/anti-patterns.md` 中的 10 大类反模式，逐条检查：

```
□ AP-01: ProModalForm onFinish 是否包含 emit('update:visible', false)
□ AP-02: ProModalForm 是否传递 :form-model="model"
□ AP-03: ProModalForm 所有字段是否有 takeFullRow: true
□ AP-04: onChange 是否在异步操作前同步 model.xxx
□ AP-05: onChange 是否有 instanceof Event 守卫
□ AP-06: ProTable tableProps.scroll 是否包含 y: 500
□ AP-07: saveQueryData 是否排除了 pageNo/pageSize
□ AP-08: 列配置是否有多余 push（死代码列）
□ AP-09: GET API 是否使用 params 而非 data
□ AP-10: 只读字段是否用 valueType:'input'+disabled 而非 valueType:'text'
```

### 4.2 ESLint 检查

```bash
python3 scripts/check_changed_eslint.py
```

### 4.3 自动审计脚本

```bash
python3 scripts/audit_refactor.py \
  --page1 src/views/disposalTool/<page> \
  --page2 src/views/disposalTool2/<page>
```

### 4.4 审查清单

完整审查清单见 `references/audit-checklist.md`

**STOP 条件**:
- 反模式检查发现 AP-01 ~ AP-10 任一命中 → 必须修复后继续
- ESLint 有 error 级别问题 → 必须修复
- 审计脚本报 blocker → 必须修复

---

## Phase 5: 报告（Report）

生成审计报告，格式见 `references/audit-report-template.md`

```bash
python3 scripts/audit_refactor.py \
  --page1 src/views/disposalTool/<page> \
  --page2 src/views/disposalTool2/<page> \
  --output docs/component-refactor/audit-report-<page>.md
```

报告必须包含：
- 文件变更清单
- 组件映射结果
- 反模式检查结果
- ESLint 结果
- 边界逻辑对比
- 验收结论（Pass / Conditional Pass / Fail）

---

## 硬性规则（不可违反）

1. **不修改 Page1 原文件**
2. **不修改共享 API/Store/权限逻辑**（除非用户明确批准）
3. **不修改组件库源码**（发现问题报告用户）
4. **业务逻辑零变更**：参数名、返回值处理、权限判断、金额/日期/状态语义
5. **每个 ProModalForm onFinish 成功路径必须有 `emit('update:visible', false)`**
6. **每个 ProTable 必须有 `scroll: { x: 'max-content', y: 500 }`**
7. **每个 saveQueryData 必须排除分页参数**
8. **GET API 必须使用 params 不是 data**
9. **弹窗表单字段必须 takeFullRow: true**
10. **只读字段用 valueType:'input' + disabled:true，不用 valueType:'text'**

---

## Stop Conditions（整体停止条件）

遇到以下情况**停止并报告用户**：

- 需要修改组件库代码
- 需要修改共享业务逻辑
- API 参数语义不明确
- 旧组件行为无法推断
- 权限逻辑混入 UI 配置
- Page2 路由无法安全添加
- 新组件缺少等价行为
- 参考文件不可靠

---

## 可用脚本

| 脚本 | 用途 |
|------|------|
| `scripts/check_changed_eslint.py` | ESLint 检查变更文件 |
| `scripts/audit_refactor.py` | 自动生成迁移审计报告 |

---

## Bugfix 学习循环

每次修 bug 后：
1. 记录到 `docs/component-refactor/bugfix-log.md`
2. 如果是新模式，更新 `references/anti-patterns.md`
3. 更新 `references/audit-checklist.md`

详见当前 bugfix-log 已有 19 条记录。
