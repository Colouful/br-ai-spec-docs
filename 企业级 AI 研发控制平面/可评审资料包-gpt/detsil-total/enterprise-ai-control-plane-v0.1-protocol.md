# 企业级 AI 研发控制平面 V0.1 最小可落地目录结构与 JSON Schema 协议

> 适用对象：`br-ai-spec`、`skill-q-platform`、`br-ai-spec-visual`、企业级全栈业务项目、Cursor、Claude Code、Codex 等 AI IDE。  
> 第一版样板项目：中台金融系统，前端 Vue + Vite + Vuex，后端 Spring Boot + MySQL + Redis + MQ。  
> 核心目标：把 AI 从“会写代码的助手”升级为“受控、可验证、可审计、可恢复、可并行协作的企业研发执行体系”。

---

## 0. 文档结论

V0.1 采用 **Graph-Governed Multi-Agent** 架构：

```text
Graph 管流程
Agent 管专业判断
Executor 管代码变更
Git Worktree 管隔离执行
Hook 管强约束
Test Gate 管真实性
Evidence 管审计
Visual 管观测
Hub 管资产治理
```

本协议的最小落地原则是：

1. **OpenSpec 放在项目根目录 `openspec/`**，作为需求、规格、变更事实源。
2. **业务项目最小侵入**，默认只新增 `openspec/`、`.ai-spec/`、`.ai-spec-local/`。
3. **L2 标准需求也必须完整 OpenSpec**，但 AI 读取时只读任务视图，不全量喂上下文。
4. **Skill / Rule / Agent Profile 必须渐进式披露**，不能一次性把所有资产塞给模型。
5. **Context Pack 默认聚合到 `run.bundle.json`**，大附件单独放 `artifacts/`，避免大量散文件污染项目。
6. **复杂长任务使用 Task DAG 拆解**，每个可独立交付 Task 绑定独立 git worktree。
7. **多执行 Agent 允许并行**，但必须满足 `dependsOn`、`writeSet`、`lockKeys`、契约冻结和风险等级规则。
8. **所有代码修改必须通过需求主开发分支合并**，不能直接改主干。
9. **测试、验收、执行日志、修复记录必须证据落盘**，并由 `evidence-index.json` 统一索引。
10. **运行证据默认不进 Git**，由 `.ai-spec-local/` 管理，并受保留策略控制。

---

## 1. V0.1 总体目标

### 1.1 目标

V0.1 要跑通一条真实企业级全栈需求链路：

```text
自然语言需求
  ↓
OpenSpec 变更建模
  ↓
任务等级识别 L1 / L2 / L3
  ↓
上下文索引与压缩
  ↓
渐进式资产加载
  ↓
多专家 Agent 分析
  ↓
Task DAG 拆解
  ↓
多 Executor Agent + git worktree 并行执行
  ↓
Patch Bundle 合并
  ↓
Hook + Test Gate 验证
  ↓
有限自修复
  ↓
Evidence 落盘
  ↓
Visual 观测
  ↓
最终交付报告
```

### 1.2 不做什么

V0.1 明确不做以下内容：

- 不做复杂多租户商业化。
- 不做 Agent 市场。
- 不做全自动上线。
- 不做无边界自主多 Agent 聊天室。
- 不强制业务项目接入运行时 SDK。
- 不强制替换企业已有研发流程。
- 不把 Cursor、Claude、Codex 任一工具作为唯一标准。

### 1.3 第一版真实样板

```text
业务系统：中台金融系统
前端技术：Vue + Vite + Vuex
后端技术：Spring Boot
数据库：MySQL
缓存：Redis
消息：MQ
项目类型：企业级全栈业务项目
风险画像：金融中台 / 数据敏感 / 权限敏感
```

---

## 2. 三仓职责与对接边界

### 2.1 br-ai-spec：本地控制器

`br-ai-spec` 是业务项目内的本地控制器，负责把平台规范落到真实开发过程。

| 模块 | V0.1 改造内容 |
|---|---|
| CLI | 新增 `init`、`plan`、`run`、`verify`、`report`、`resume`、`clean`、`worktree` 命令 |
| 项目扫描 | 识别 Vue、Vite、Vuex、Spring Boot、MySQL、Redis、MQ、测试脚本 |
| OpenSpec Loader | 读取 `openspec/`，生成 `openspec-view`，避免全量上下文膨胀 |
| Asset Loader | 按任务类型渐进式加载 Manifest、Rule、Skill、Agent Profile |
| Context Engine | 生成 `run.bundle.json`，管理上下文预算与压缩 |
| Task Planner | 生成 Task DAG、writeSet、lockKeys、dependsOn |
| Worktree Manager | 按 Task 创建 worktree、分支、清理策略 |
| Executor Scheduler | 调度多个执行 Agent，避免冲突 |
| Hook Runner | 执行 Scope Guard、Diff Guard、Secret Guard、Test Gate、Evidence Gate |
| Evidence Writer | 写入 `evidence-index.json`、`final-report.md`、artifacts |
| Visual Reporter | 上报 Run、Task、Agent、测试、证据状态 |

### 2.2 skill-q-platform：资产治理中心

`skill-q-platform` 负责管理、审核、发布和分发企业级 AI 资产。

| 资产 | 说明 |
|---|---|
| Manifest | 规范包组合入口 |
| Rule | 工程规则和禁止项 |
| Skill | 可复用任务能力 |
| Agent Profile | 专家 Agent 职责与权限 |
| Hook Spec | 工具调用和代码变更门禁 |
| Test Gate | 测试命令、通过标准、证据要求 |
| Context Policy | 上下文预算、压缩策略、渐进披露 |
| Evidence Policy | 证据类型、保留周期、归档规则 |
| Memory Template | 项目级 Memory 模板 |
| IDE Adapter Template | Cursor、Claude、Codex 配置生成模板 |

### 2.3 br-ai-spec-visual：运行观测中心

`br-ai-spec-visual` 不负责改代码，也不上传业务源码，只负责运行态观测和治理。

| 页面 | 展示内容 |
|---|---|
| Run 列表 | 需求名称、等级、状态、开始时间、耗时、通过率 |
| Run 详情 | OpenSpec、Task DAG、Agent 轨迹、worktree 状态 |
| Task DAG | 依赖关系、并行组、阻塞点、合并状态 |
| Agent Timeline | 专家分析、执行、修复、合并、验证事件 |
| Evidence | 测试计划、测试用例、验收清单、日志、截图、报告 |
| Quality Metrics | 通过率、修复轮次、越权拦截、测试失败次数 |

---

## 3. 业务项目最小目录协议

### 3.1 项目根目录

```text
业务项目根目录
├── openspec/
│   ├── project.md
│   ├── specs/
│   ├── changes/
│   └── archive/
│
├── .ai-spec/
│   ├── manifest.lock.json
│   ├── project.config.json
│   ├── context-policy.json
│   ├── evidence-policy.json
│   ├── agents/
│   ├── rules/
│   ├── skills/
│   ├── hooks/
│   ├── test-gates/
│   ├── memory/
│   └── indexes/
│       ├── openspec-index.json
│       ├── capability-index.json
│       └── change-index.json
│
├── .ai-spec-local/
│   ├── runs/
│   ├── cache/
│   └── tmp/
│
└── 业务源码保持原样
```

### 3.2 目录职责

| 目录 | 是否进 Git | 职责 |
|---|---:|---|
| `openspec/` | 是 | 需求、规格、变更事实源 |
| `.ai-spec/` | 是 | AI 标准资产、Memory、Hook、Test Gate、索引 |
| `.ai-spec-local/` | 否 | 运行日志、上下文、证据、缓存、临时文件 |
| Worktree 外部目录 | 否 | 多执行 Agent 隔离工作区 |

### 3.3 `.gitignore`

```gitignore
.ai-spec-local/
.br-spec-worktrees/
```

---

## 4. OpenSpec 企业级读取协议

### 4.1 L2 也必须完整 OpenSpec

| 等级 | OpenSpec 要求 |
|---|---|
| L1 | 可选，允许轻量 change note |
| L2 | 强制完整 OpenSpec：proposal、design、tasks、spec delta、acceptance |
| L3 | 强制完整 OpenSpec + 风险审查 + 人工确认 + 回滚方案 |

中台金融系统中，新增页面、新增接口、新增表、新增状态流转、新增配置模块，默认都属于 L2。

涉及资金、授信、风控、权限、数据迁移、MQ 消费、缓存一致性，默认升级为 L3。

### 4.2 AI 不直接读取全量 OpenSpec

禁止默认全量读取：

```text
openspec/specs/**/*
openspec/changes/**/*
```

必须通过索引和任务视图读取：

```text
.ai-spec/indexes/openspec-index.json
.ai-spec-local/runs/{runId}/run.bundle.json 中的 openspec.view
```

### 4.3 读取阶段

| 阶段 | 读取内容 |
|---|---|
| 任务进入 | `openspec-index.json`、业务域摘要、最近相关变更摘要 |
| 方案规划 | 当前 change 的 proposal、design、tasks 摘要 |
| 代码执行 | 当前 Task 关联的 spec delta 和 acceptanceRefs |
| 测试验收 | 验收标准、测试要求、禁止越界范围 |
| 归档复盘 | 完整 change 包，用于合并长期知识 |

### 4.4 OpenSpec View

OpenSpec View 是给 Agent 的压缩视图，不是原始全文。它必须包含：

- 当前需求目标。
- 受影响能力域。
- 已冻结契约。
- 当前任务项。
- 相关 spec delta 摘要。
- 验收标准。
- 禁止修改范围。
- 必跑测试。
- 读取预算。

---

## 5. Context Pack 与压缩协议

### 5.1 默认不生成大量散文件

V0.1 默认采用：

```text
一个 run.bundle.json
一个 run.log.jsonl
一个 evidence-index.json
一个 final-report.md
一个 artifacts/ 附件目录
```

运行目录：

```text
.ai-spec-local/runs/{runId}/
├── run.bundle.json
├── run.log.jsonl
├── evidence-index.json
├── worktree-index.json
├── merge-report.json
├── final-report.md
└── artifacts/
    ├── patches/
    ├── logs/
    ├── screenshots/
    ├── test-results/
    └── reports/
```

### 5.2 `run.bundle.json` 职责

`run.bundle.json` 是当前任务的状态总账，记录任务基础信息、OpenSpec 任务视图、项目技术栈、已加载资产、Agent 分工、Task DAG、Worktree 索引摘要、验证结果摘要、证据索引摘要和 Checkpoint 摘要。

### 5.3 上下文压缩触发条件

必须触发压缩的场景：

1. 输入上下文超过阈值。
2. 阶段切换。
3. 关键决策完成。
4. 测试失败。
5. 自修复前。
6. 归档前。

压缩后必须保留：

- 已确认事实。
- 已冻结契约。
- 禁止修改范围。
- 已改文件。
- 当前失败原因。
- 下一步动作。
- 验收点状态。

### 5.4 运行数据保留策略

| Run 类型 | 默认保留 |
|---|---:|
| 成功 Run | 14 天 |
| 失败 Run | 30 天 |
| 大型附件 | 7 天 |
| 标记为重要样本 | 长期保留 |
| 已归档报告 | 长期保留 |

清理命令：

```bash
br-spec clean --before 14d
br-spec clean --failed-before 30d
br-spec clean --artifacts-before 7d
br-spec archive-run <runId>
```

---

## 6. 渐进式资产披露协议

### 6.1 加载等级

| 等级 | 名称 | 加载内容 |
|---|---|---|
| L0 | 索引 | Manifest Index、OpenSpec Index、Capability Index |
| L1 | 摘要 | Asset Summary、Project Memory Summary |
| L2 | 任务包 | 命中 Rule、Skill 摘要、Agent Profile 摘要、OpenSpec View |
| L3 | 实现细节 | 当前任务相关 Rule 详情、Skill 详情、选中文件 |
| L4 | 示例和历史 | 相似案例、失败样本、自修复历史 |

### 6.2 禁止项

- 禁止一次性加载所有 Rule。
- 禁止一次性加载所有 Skill。
- 禁止把全部 Memory 塞入 Prompt。
- 禁止让执行 Agent 自由读取全仓库。
- 禁止将历史 Run 日志默认注入当前任务。

### 6.3 资产命中逻辑

资产命中应依据任务等级、业务域、技术栈、受影响目录、受影响能力域、OpenSpec spec delta、历史失败样本和测试类型。

---

## 7. Task DAG 与多执行 Agent 协议

### 7.1 长任务拆解层级

```text
Epic
  ↓
Feature
  ↓
Change
  ↓
Task DAG
  ↓
Step
```

V0.1 的执行粒度是 Task，不是 Step。

### 7.2 Task 是执行、隔离、合并、验收单元

一个 Task 必须满足：

- 目标清晰。
- 读写范围明确。
- 有依赖关系。
- 有 lockKeys。
- 有验收点。
- 有测试命令。
- 能产出 patch bundle。
- 能被 Merge Agent 独立审查。

### 7.3 并行条件

允许并行必须同时满足：

```text
writeSet 无交集
lockKeys 无冲突
dependsOn 已完成
API / DB / 状态枚举 / 权限契约已冻结
风险等级允许并行
可在合并后统一验证
```

不能只依据“是否修改同一个文件”判断。

### 7.4 默认不可并行的资源

以下资源默认不并行，除非人工确认：

- 数据库 migration。
- Redis Key 设计。
- MQ Topic / Consumer。
- 权限码。
- 数据权限。
- 事务边界。
- 资金、授信、风控相关流程。

---

## 8. Git Worktree 执行隔离协议

### 8.1 企业级裁决

Worktree 粒度绑定 Task，不绑定 Agent，也不绑定 Step。

```text
一个可执行 Task 节点
= 一个任务分支
= 一个 git worktree
= 一个 Patch Bundle
= 一组证据
```

### 8.2 分支模型

```text
主干分支
  ↓
需求主开发分支：ai/change/{changeId}
  ↓
任务分支：ai/task/{changeId}/{taskId}
  ↓
任务 worktree
```

### 8.3 Worktree 外部目录

默认放在项目外部，降低业务项目侵入：

```text
../.br-spec-worktrees/
└── {repoName}/
    └── {runId}/
        ├── task-001-db-schema/
        ├── task-002-backend-api/
        ├── task-003-frontend-page/
        └── task-004-test-cases/
```

也可以配置到用户目录：

```text
~/.br-spec/worktrees/{repoHash}/{runId}/
```

### 8.4 执行流程

```text
1. 从主干创建 ai/change/{changeId}
2. 从需求主开发分支创建 ai/task/{changeId}/{taskId}
3. 为每个可并行 Task 创建 worktree
4. Executor Agent 只在自己的 worktree 内执行
5. 执行完成后提交 task commit
6. 生成 patch bundle 和 task evidence
7. Merge Agent 检查冲突、越权、证据完整性
8. cherry-pick 或 merge 到 ai/change/{changeId}
9. 统一 verify
10. 成功后清理 worktree
```

### 8.5 合并策略

推荐优先级：

1. Task 分支压缩成语义化 commit 后 cherry-pick。
2. `git merge --no-ff` 合并 Task 分支。
3. `git apply patch.diff` 作为兜底。

V0.1 默认使用任务分支语义化 commit + cherry-pick 到需求主开发分支。

### 8.6 清理策略

| 状态 | 清理策略 |
|---|---|
| 成功合并 | 立即 remove |
| 失败但无价值 | 3 天后清理 |
| 失败且需要排查 | lock，最多保留 14 天 |
| stale worktree | prune |

命令：

```bash
br-spec worktree list
br-spec worktree clean --run <runId>
br-spec worktree clean --stale
br-spec worktree prune --expire 7d
```

---

## 9. Agent 协议

### 9.1 Agent 分层

| 层级 | Agent |
|---|---|
| 决策层 | Orchestrator Agent |
| 分析层 | Product、Architect、Frontend Expert、Backend Expert、Database、Security |
| 执行层 | Executor Agent Pool |
| 验证层 | QA Agent、Verify Agent |
| 合并层 | Merge Agent |
| 归档层 | Docs Agent |
| 修复层 | Repair Agent |

### 9.2 改代码权限

| Agent | 是否允许改代码 |
|---|---:|
| Orchestrator | 默认不允许 |
| Expert Agents | 不允许 |
| Executor Agent | 允许，但只允许改 Task writeSet |
| Repair Agent | 允许，但只允许改失败相关范围 |
| Merge Agent | 不直接写业务逻辑，只做合并和冲突处理 |
| QA / Docs | 不允许改业务代码 |

### 9.3 Executor Pool

Executor Agent 不是长期拥有 worktree，而是临时绑定 Task：

```text
Task A → Executor Agent 1 → worktree A
Task B → Executor Agent 2 → worktree B
Task C → Executor Agent 3 → worktree C
```

完成后释放绑定关系。

---

## 10. Hook 与 Test Gate 协议

### 10.1 Hook 类型

| Hook | 触发时机 |
|---|---|
| PreRead | 读取文件前 |
| PreEdit | 修改文件前 |
| PostEdit | 修改文件后 |
| PreCommand | 执行命令前 |
| PostCommand | 执行命令后 |
| PreCommit | 提交前 |
| BeforeRunComplete | Run 完成前 |
| AfterTestFailure | 测试失败后 |
| BeforeEvidenceArchive | 证据归档前 |

### 10.2 V0.1 必须内置的 Guard

| Guard | 作用 |
|---|---|
| Scope Guard | 禁止修改 Task writeSet 外文件 |
| Dangerous File Guard | 禁止删除高风险文件 |
| Secret Guard | 禁止读取或输出敏感配置 |
| Diff Guard | 防止过度修改 |
| Worktree Guard | 禁止多个 Executor 写同一 worktree |
| Test Gate | 测试失败禁止完成 |
| Evidence Gate | 证据缺失禁止完成 |
| Repair Limit Guard | 自修复超过 3 轮停止 |
| Manual Approval Gate | L3 或高风险资源要求人工确认 |

### 10.3 Test Gate 分类

| Gate | 示例命令 |
|---|---|
| 前端 Lint | `npm run lint` |
| 前端类型检查 | `npm run typecheck` |
| 前端单测 | `npm run test:unit` |
| 后端单测 | `mvn test` |
| 接口测试 | `mvn test -Dtest=*ApiTest` 或 Apifox / Newman |
| 集成测试 | 受影响模块集成测试 |
| E2E | Playwright / Cypress |

所有测试结果必须写入 Evidence。

---

## 11. Evidence 证据协议

### 11.1 证据索引

每个 Run 必须有：

```text
.ai-spec-local/runs/{runId}/evidence-index.json
```

证据必须包含证据 ID、证据类型、关联 Task、关联 Agent、关联命令、生成时间、状态、文件路径、校验摘要和验收点引用。

### 11.2 L2 / L3 强制证据

| 证据 | L2 | L3 |
|---|---:|---:|
| OpenSpec proposal | 必须 | 必须 |
| OpenSpec design | 必须 | 必须 |
| OpenSpec tasks | 必须 | 必须 |
| 测试计划 | 必须 | 必须 |
| 测试用例 | 必须 | 必须 |
| 验收清单 | 必须 | 必须 |
| 执行日志 | 必须 | 必须 |
| diff summary | 必须 | 必须 |
| test result | 必须 | 必须 |
| self repair log | 按需 | 必须 |
| risk review | 可选 | 必须 |
| rollback plan | 可选 | 必须 |
| final delivery report | 必须 | 必须 |

---

## 12. 三仓接口契约

### 12.1 skill-q-platform → br-ai-spec

资产下发包：

```text
manifest.lock.json
rules/*.md
skills/*.md
agents/*.json
hooks/*.json
test-gates/*.json
context-policy.json
evidence-policy.json
memory/templates/*.md
ide-adapters/templates/*
```

### 12.2 br-ai-spec → br-ai-spec-visual

运行事件示例：

```json
{
  "type": "task.completed",
  "runId": "run_001",
  "changeId": "change_product_config",
  "taskId": "task_backend_api",
  "agentId": "backend_executor_01",
  "status": "passed",
  "timestamp": "2026-04-28T16:00:00+08:00"
}
```

### 12.3 br-ai-spec-visual → br-ai-spec

V0.1 只读，不反向控制执行。V0.2 可考虑增加人工暂停、人工恢复、人工批准、重跑某个 Task、下载 Evidence。

---

## 13. CLI 命令协议

### 13.1 初始化

```bash
br-spec init
```

生成 `openspec/` 基础结构、`.ai-spec/project.config.json`、`.ai-spec/manifest.lock.json`、`.ai-spec/context-policy.json`、`.ai-spec/evidence-policy.json` 和 IDE Adapter 文件。

### 13.2 规划

```bash
br-spec plan "新增产品配置管理模块"
```

输出 OpenSpec change、OpenSpec View、Task DAG、Context Pack 和验收清单。

### 13.3 执行

```bash
br-spec run
```

创建 change branch、task branches、task worktrees，分发 Executor Agent，并生成 patch bundle。

### 13.4 验证

```bash
br-spec verify
```

执行 Lint、Typecheck、Unit test、API test、Integration test 和 Evidence Gate。

### 13.5 报告

```bash
br-spec report
```

生成 `final-report.md`、`evidence-index.json`、`merge-report.json`，并上报 Visual。

### 13.6 恢复

```bash
br-spec resume <runId>
```

根据 `run.bundle.json` 和 `run.log.jsonl` 恢复长任务。

---

## 14. V0.1 开发实施计划

### P0：协议固化

- 完成所有 JSON Schema。
- 完成目录生成器。
- 完成 schema 校验。
- 完成样板配置。

### P1：br-ai-spec 改造

- `init` 生成目录。
- `plan` 生成 OpenSpec + Task DAG。
- `run` 创建 worktree 并分发任务。
- `verify` 执行测试门禁。
- `report` 生成证据报告。

### P2：skill-q-platform 改造

- 新增 Hook Spec 管理。
- 新增 Test Gate 管理。
- 新增 Context Policy 管理。
- 新增 Evidence Policy 管理。
- Manifest 支持引用新增资产类型。

### P3：br-ai-spec-visual 改造

- Run 列表。
- Run 详情。
- Task DAG 视图。
- Worktree 状态。
- Evidence 视图。
- Agent Timeline。

### P4：真实中台金融系统样板链路

- 选择一个真实配置模块。
- 完整执行 L2 OpenSpec。
- 拆 Task DAG。
- 多 worktree 并行执行。
- 合并验证。
- 证据落盘。
- Visual 展示。

---

## 15. 验收标准

V0.1 只有满足以下条件，才算真正跑通：

1. 能在真实中台金融项目中初始化，不破坏原项目结构。
2. 能生成完整 `openspec/` change。
3. 能识别 Vue + Vite + Vuex + Spring Boot + MySQL + Redis + MQ。
4. 能生成 Task DAG。
5. 能按 Task 创建 git worktree。
6. 能派发多个 Executor Agent 并行执行不冲突任务。
7. 能限制 Executor 只能修改 writeSet。
8. 能拦截危险文件和越权修改。
9. 能生成测试计划、测试用例、验收清单。
10. 能执行测试门禁。
11. 能最多自修复 3 轮。
12. 能生成 evidence-index。
13. 能生成 final-report。
14. 能清理 worktree 和过期运行数据。
15. 能在 Visual 中查看 Run、Task、Agent、Evidence 状态。

---

## 16. 附录：核心 Schema 文件清单

```text
schemas/
├── agent-profile.schema.json
├── context-policy.schema.json
├── evidence-index.schema.json
├── executor-task.schema.json
├── hook-spec.schema.json
├── manifest-lock.schema.json
├── merge-report.schema.json
├── openspec-view.schema.json
├── patch-bundle.schema.json
├── project-config.schema.json
├── run-bundle.schema.json
├── task-dag.schema.json
├── test-gate.schema.json
└── worktree-index.schema.json
```

这些 Schema 是后续开发的硬契约。Codex、Claude、Cursor 开发时必须先通过这些 Schema 校验，再进入业务实现。
