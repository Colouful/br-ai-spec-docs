# Audit Checklist

> 逐项检查，每项必须 Pass 或记录 Exception。
> 检查顺序：先反模式（阻塞），再结构（警告），最后样式（建议）。

---

## 一、反模式检查（BLOCKER）

任一 FAIL 必须修复后才能继续。

| # | 检查项 | 命中 Bug | 检查方法 | 结果 |
|---|--------|----------|----------|------|
| AP-01 | ProModalForm onFinish 成功路径有 `emit('update:visible', false)` | #1,5,6 | 搜索 handleFinish/handleSubmit，检查成功分支 | □ |
| AP-02 | formFields computed 依赖动态 ref 时，onChange 先同步 model | #9,10,12,13,14,16 | 检查 formFields 是否引用 `xxxOptions.value` | □ |
| AP-03 | ProModalForm 所有字段有 `takeFullRow: true` | #11 | 检查每个字段定义 | □ |
| AP-04 | onChange 中 `model.xxx = val` 在所有 `await` 之前 | #9,12,13,14 | 检查每个 onChange 函数体 | □ |
| AP-05 | onChange 有 `instanceof Event` 守卫 | #15 | 检查每个 onChange 函数体 | □ |
| AP-06 | ProTable tableProps.scroll 包含 `y: 500`（详情 `y: 400`） | #18 | 搜索 `scroll` 配置 | □ |
| AP-07 | saveQueryData 传入前排除了 pageNo/pageSize | #19 | 搜索 saveQueryData 调用 | □ |
| AP-08 | proColumns 列配置与参考文件一致，无多余列 | #2,3,7,8 | 对比列配置 | □ |
| AP-09 | GET API 使用 `params` 而非 `data` | #17 | 搜索 `method: 'get'` | □ |
| AP-10 | 只读字段用 `valueType:'input' + disabled:true` | 经验 | 搜索 `valueType: 'text'` | □ |

---

## 二、组件替换检查

| # | 检查项 | 结果 |
|---|--------|------|
| C-01 | 无 `@koi-design/vix-components` 导入 | □ |
| C-02 | 无 `@koi-design/uxd-ui` 中的 `u-*` 组件导入（u-tooltip, u-tag 等） | □ |
| C-03 | 无 `DynamicsFilter` 使用 | □ |
| C-04 | 无 `DynamicsForm` 使用 | □ |
| C-05 | 无 `u-table` 使用 | □ |
| C-06 | 无 `UModal` 使用（非 Arco Modal） | □ |
| C-07 | 无 `EditDrawer` 使用 | □ |
| C-08 | 无 `ViewContent` / `u-info-view` 使用 | □ |
| C-09 | 无 `OneLineText` 使用 | □ |
| C-10 | 无 `usePageList` 使用 | □ |
| C-11 | ProTable 引入自 `@ex/ux-comp` | □ |
| C-12 | ProModalForm 引入自 `@ex/ux-comp` | □ |
| C-13 | ProActions 引入自 `@ex/ux-comp` | □ |
| C-14 | ProDescriptions 引入自 `@ex/ux-comp`（如使用） | □ |
| C-15 | Tooltip/Tag 引入自 `@arco-design/web-vue` | □ |

---

## 三、titleAlign 检查

| # | 检查项 | 结果 |
|---|--------|------|
| T-01 | ProModalForm type="modal" 有 `:modal-props="{ titleAlign: 'start' }"` | □ |
| T-02 | ProModalForm type="drawer" 无 titleAlign | □ |
| T-03 | Arco Modal 有 `title-align="start"` 或 `titleAlign: 'start'` | □ |
| T-04 | Modal.confirm 有 `titleAlign: 'start'` | □ |
| T-05 | Arco Drawer 无 titleAlign | □ |

---

## 四、ProActions 检查

| # | 检查项 | 结果 |
|---|--------|------|
| A-01 | ProActions 有 `:max-visible-count="2"` | □ |
| A-02 | 行操作权限使用 `accessible: hasAuth(AUTH.XXX)` | □ |
| A-03 | 行操作顺序与原版一致 | □ |
| A-04 | disabled 状态与原版一致 | □ |
| A-05 | confirm/popconfirm 行为保留 | □ |

---

## 五、路由检查

| # | 检查项 | 结果 |
|---|--------|------|
| R-01 | route2 文件已创建于 `src/router/modules/` | □ |
| R-02 | route2 path 添加了 `2` 后缀 | □ |
| R-03 | route2 name 唯一 | □ |
| R-04 | route2 component 指向 Page2 | □ |
| R-05 | router/index.js 已注册 route2 | □ |
| R-06 | 原 route 文件未修改 | □ |

---

## 六、业务逻辑保护检查

| # | 检查项 | 结果 |
|---|--------|------|
| B-01 | API 调用参数名不变 | □ |
| B-02 | API 返回值处理不变 | □ |
| B-03 | 权限判断逻辑不变 | □ |
| B-04 | 金额/日期/状态格式化不变 | □ |
| B-05 | 分页参数映射正确（pageNo → pageNum） | □ |
| B-06 | 查询缓存行为保留 | □ |
| B-07 | 批量操作选择逻辑保留 | □ |
| B-08 | 排序逻辑保留 | □ |
| B-09 | 空值/边界值处理保留 | □ |

---

## 七、代码质量检查

| # | 检查项 | 结果 |
|---|--------|------|
| Q-01 | ESLint 通过（`python3 scripts/check_changed_eslint.py`） | □ |
| Q-02 | 无未使用的 import | □ |
| Q-03 | 无未使用的变量/函数 | □ |
| Q-04 | 无死代码（旧版遗留的 slot/函数） | □ |
| Q-05 | Prettier 格式正确 | □ |
| Q-06 | 无 `console.log` 调试代码（除必要的错误日志） | □ |

---

## 八、Page1 保护检查

| # | 检查项 | 结果 |
|---|--------|------|
| P-01 | Page1 文件无任何修改（`git diff` 验证） | □ |
| P-02 | 共享 API 模块无修改 | □ |
| P-03 | Store 模块无修改 | □ |
| P-04 | 权限常量无修改 | □ |
