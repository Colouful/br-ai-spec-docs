
# component-refactor Skill v1.7.0

项目专用组件重构 Skill，用于：

```text
/Users/lizhenwei/workspace/vueworkspace/bairong/asset-cube-html
```

## v1.3.0 更新

- 固化本地迁移项目路径。
- 增加 `src/views/disposalTool` 已经提前替换过一次的风险提示。
- 要求优先使用未重构分支复制出来的参考目录进行旧逻辑对比。
- 新建 Page2 后必须同步新建 route2。
- route2 文件位于：`src/router/modules/`。
- route2 文件名、访问地址、组件路径、路由 name 都需要加 `2` 或唯一后缀。
- route2 必须注册到：`src/router/index.js`。
- 增加本地 Arco 文档路径：`/Users/lizhenwei/workspace/vueworkspace/bairong/arco-design-vue/packages/web-vue/components/xxx/README.zh-CN.md`。
- 保留 `ProModalForm type="modal"` 使用 `:modal-props="{ titleAlign: 'start' }"`。
- 保留 Arco Modal 使用 `title-align="start"` / `titleAlign: 'start'`。
- Drawer 默认标题居左，不额外改。
- 保留 `ProActions` 默认 `max-visible-count="2"`。

## 安装位置

```text
.agents/skills/component-refactor/
```

或 Hermes：

```text
~/.hermes/skills/component-refactor/
```

## v1.4.0 新增规则

- 弹窗里的 `ProModalForm` 表单项必须独占一行。
- 适用范围：`ProModalForm type="modal"`、`ProModalForm type="drawer"`、Modal/Drawer 包裹的 ProModalForm。
- 推荐实现：
  - `formProps.layout.columns: [1]`
  - 或字段级 `takeFullRow: true`
- 不允许为了布局改变字段名、校验规则、提交 payload、API 参数、字段联动逻辑。
- 例外情况必须写入验收报告。

## v1.5.0 新增规则：Bugfix Learning Loop

当 AI 迁移后出现 bug，并完成修复时，必须记录：

- 问题类型
- 问题现象
- 根因
- 修复办法
- 验证结果
- 下次如何避免
- 是否需要更新检查清单/脚本/组件映射

默认记录到：

```text
docs/component-refactor/bugfix-log.md
```

可使用脚本：

```bash
python3 scripts/record_bugfix.py \
  --issue-type form-backfill-bug \
  --page2 src/views/example/page2 \
  --summary "编辑弹窗回填失败" \
  --root-cause "异步 options 未加载完成就执行回填" \
  --fix "将回填移动到 options 加载完成后执行" \
  --prevention "迁移 ProModalForm 编辑弹窗时必须检查异步 options 与回填顺序"
```

## v1.6.0 新增规则：Changed Files ESLint Gate

每次 AI 修改代码后，必须对本次修改的文件执行 ESLint 校验。

推荐命令：

```bash
python3 scripts/check_changed_eslint.py
```

如果 Skill 安装在项目内：

```bash
python3 .agents/skills/component-refactor/scripts/check_changed_eslint.py
```

如果已知修改文件：

```bash
python3 scripts/check_changed_eslint.py \
  --files src/views/example/page2/index.vue src/router/modules/example2.js
```

规则：

- 每完成一个区域就跑一次，不要等到最后。
- 只 lint 本次变更文件，减少噪音。
- ESLint 失败必须先修复，再继续。
- 不能为了 ESLint 修改业务逻辑。
- 最终验收报告必须记录 ESLint 结果。


## v1.7.0 新增规则：Bugfix Memory + ex-ux-kit 本地源码/文档优先

### 强化禁止修改业务逻辑

Skill 明确要求：只能做 UI 组件迁移，不允许修改已有业务逻辑、API 语义、权限、store、校验意图、导出/批量参数等。

### 迁移前读取历史问题记录

每次迁移或修 bug 前先读取：

```text
docs/component-refactor/bugfix-log.md
docs/component-refactor/known-issues-prevention.md
src/views/<module>/<page2>/__migration__/bugfix-log.md
```

可使用：

```bash
python3 scripts/read_bugfix_memory.py
```

### 遇到组件问题优先读 ex-ux-kit 文档和源码

本地组件库源码：

```text
/Users/lizhenwei/workspace/vueworkspace/bairong/ex-ux-kit/packages/component/src
```

本地组件库文档：

```text
/Users/lizhenwei/workspace/vueworkspace/bairong/ex-ux-kit/packages/component/docs
```

演示项目源码：

```text
/Users/lizhenwei/workspace/vueworkspace/bairong/ex-ux-kit/playground/arco
```

遇到 ProTable / ProModalForm / ProActions / ProDescriptions 等问题时，优先读取文档、源码和 playground，再做最小修复。
