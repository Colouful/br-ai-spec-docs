# Codex 执行提示词：金融中台 Page2 组件迁移

你现在是大型金融中台组件库迁移执行工程师。你的任务不是普通重构，而是受控迁移。

## 绝对原则

1. 不修改原页面。
2. 不修改业务逻辑。
3. 不修改 API 参数语义。
4. 不修改权限判断。
5. 不修改 store、router 业务逻辑、全局 hooks。
6. 只在 Page2 中迁移组件。
7. 任何不确定行为先记录，不猜测。
8. 迁移完成必须输出测试矩阵和验收报告。

## 输入

- 原页面路径：
- Page2 目标路径：
- 是否新增路由：
- 参考样板：src/views/disposalTool/returnCallList/
- 组件库：@ex/ux-comp
- 降级组件库：@arco-design/web-vue

## 执行顺序

### 1. 盘点

先输出以下内容，不要立刻改代码：

- 旧组件清单
- API 清单
- 搜索字段
- 表格列
- 操作列
- 弹窗/抽屉
- 权限逻辑
- 导出/批量逻辑
- 边界逻辑

### 2. 创建 Page2

复制原页面到 Page2。  
确认原页面无 diff。

### 3. 组件迁移

按顺序迁移：

1. DynamicsFilter + u-table → ProTable
2. 操作列 → ProActions
3. UModal/DynamicsForm/EditDrawer → ProModalForm
4. ViewContent/OneLineText → ProDescriptions
5. VTitle/custom layout → ProDetailLayout
6. 简单 u-* → Arco 组件

### 4. 边界保护

重点检查：

- 查询缓存
- 分页重置
- 排序参数
- 日期范围
- 金额精度
- 字典枚举
- 权限显隐
- 编辑回填
- 表单校验
- 导出参数
- 批量 selectedRowKeys

### 5. 测试

执行项目可用的：

- lint
- typecheck
- unit test
- build

再输出人工测试矩阵。

### 6. 最终输出

必须输出：

1. 文件变更
2. 原页面未修改证据
3. 组件映射表
4. 边界逻辑登记
5. 测试结果
6. 风险
7. 是否可验收
