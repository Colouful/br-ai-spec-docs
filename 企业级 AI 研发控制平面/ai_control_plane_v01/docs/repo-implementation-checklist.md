# 三仓 V0.1 改造实施清单

## 1. br-ai-spec

### P0 必做
- 新增 schema 校验模块。
- 新增 `.ai-spec/`、`.ai-spec-local/`、`openspec/` 初始化生成器。
- 新增项目扫描器，识别 Vue、Vite、Vuex、Spring Boot、MySQL、Redis、MQ。
- 新增 `project.config.json`、`manifest.lock.json`、`context-policy.json`、`evidence-policy.json` 生成逻辑。

### P1 必做
- 实现 `br-spec plan`。
- 读取 OpenSpec 索引，生成 OpenSpec View。
- 生成 Task DAG。
- 生成 acceptance checklist。

### P2 必做
- 实现 Worktree Manager。
- 实现 Task Branch Manager。
- 实现 Executor Scheduler。
- 实现 Patch Bundle Writer。

### P3 必做
- 实现 Hook Runner。
- 实现 Test Gate Runner。
- 实现 Evidence Writer。
- 实现 Resume / Clean。

## 2. skill-q-platform

### P0 必做
- Manifest 扩展到 Hook、Test Gate、Context Policy、Evidence Policy。
- Asset Factory 支持新增资产类型。
- 发布包输出 manifest.lock.json。

### P1 必做
- Rule / Skill / Agent Profile 增加 summary 字段，用于渐进披露。
- 增加资产 checksum。
- 增加版本锁定和兼容性检查。

### P2 必做
- 增加团队级规范包。
- 增加项目级覆盖规则。
- 增加审核与发布状态流转。

## 3. br-ai-spec-visual

### P0 必做
- 新增 Run 接收接口。
- 新增 Event 接收接口。
- 新增 Evidence 索引读取能力。

### P1 必做
- Run 列表。
- Run 详情。
- Task DAG 展示。
- Agent Timeline。

### P2 必做
- Worktree 状态展示。
- Test Gate 展示。
- Evidence 展示。
- 质量指标看板。
