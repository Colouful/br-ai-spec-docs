# Audit Report Template

> 自动生成于 Phase 5。使用 `scripts/audit_refactor.py` 生成。
> 如需手写，按此格式填写。

---

# 迁移审计报告

## 基本信息

| 项目 | 值 |
|------|-----|
| 迁移页面 | `<page-name>` |
| Page1 路径 | `src/views/disposalTool/<page>/` |
| Page2 路径 | `src/views/disposalTool2/<page>/` |
| 路由模块 | `src/router/modules/<route>2.js` |
| 审计时间 | `YYYY-MM-DD HH:mm` |
| 审计人 | AI / 手动 |

---

## 文件变更清单

| 文件 | 操作 | 说明 |
|------|------|------|
| `src/views/disposalTool2/<page>/index.vue` | 新增/修改 | Tab 容器 |
| `src/views/disposalTool2/<page>/todoList.vue` | 新增/修改 | ProTable 列表 |
| `src/views/disposalTool2/<page>/components/xxx.vue` | 新增/修改 | ProModalForm 弹窗 |
| `src/router/modules/<route>2.js` | 新增 | 路由模块 |
| `src/router/index.js` | 修改 | 注册 route2 |

---

## 组件映射结果

| 旧组件 | 新组件 | 文件 | 状态 |
|--------|--------|------|------|
| DynamicsFilter + u-table | ProTable | todoList.vue | ✅ |
| UModal + DynamicsForm | ProModalForm | approve.vue | ✅ |
| ViewContent | ProDescriptions | detail.vue | ✅ |
| u-tooltip | Tooltip | completedList.vue | ✅ |

---

## 反模式检查结果

| 编号 | 检查项 | 结果 | 备注 |
|------|--------|------|------|
| AP-01 | onFinish emit('update:visible', false) | ✅/❌ | |
| AP-02 | onChange 先同步 model | ✅/❌ | |
| AP-03 | takeFullRow: true | ✅/❌ | |
| AP-04 | onChange await 前同步 model | ✅/❌ | |
| AP-05 | Event 守卫 | ✅/❌ | |
| AP-06 | scroll.y 存在 | ✅/❌ | |
| AP-07 | saveQueryData 排除分页 | ✅/❌ | |
| AP-08 | 无多余列 | ✅/❌ | |
| AP-09 | GET API 用 params | ✅/❌ | |
| AP-10 | 只读字段用 input+disabled | ✅/❌ | |

**反模式通过率**: X/10

---

## ESLint 检查结果

```
（粘贴 check_changed_eslint.py 输出）
```

**结果**: PASS / FAIL

---

## 路由检查

| 项目 | 结果 | 证据 |
|------|------|------|
| route2 文件 | ✅ | `src/router/modules/<route>2.js` |
| path 添加 2 | ✅ | `path: 'xxx2'` |
| name 唯一 | ✅ | `name: 'Xxx2'` |
| component 指向 Page2 | ✅ | `import('@/views/disposalTool2/...')` |
| router/index.js 注册 | ✅ | 已添加 import |

---

## titleAlign 检查

| 场景 | 结果 |
|------|------|
| ProModalForm type="modal" | ✅ titleAlign: 'start' |
| ProModalForm type="drawer" | ✅ 无 titleAlign |
| Arco Modal | ✅ titleAlign: 'start' |

---

## ProActions 检查

| 项目 | 结果 |
|------|------|
| max-visible-count="2" | ✅ |
| 权限保留 | ✅ |
| 操作顺序 | ✅ |

---

## 业务逻辑保护

| 项目 | 结果 |
|------|------|
| API 参数不变 | ✅ |
| 返回值处理不变 | ✅ |
| 权限逻辑不变 | ✅ |
| 金额/日期格式不变 | ✅ |

---

## Page1 保护

| 项目 | 结果 |
|------|------|
| Page1 无修改 | ✅ |
| API 模块无修改 | ✅ |
| Store 无修改 | ✅ |

---

## 验收结论

- [ ] ✅ Pass — 所有检查通过
- [ ] ⚠️ Conditional Pass — 存在已记录的 Exception，不影响核心功能
- [ ] ❌ Fail — 存在 BLOCKER，需修复

### Exception 记录

（如有）

---

## 风险与后续

（记录潜在风险和后续优化项）
