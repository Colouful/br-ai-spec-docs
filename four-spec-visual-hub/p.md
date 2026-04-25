需要**分批给 Codex 指令**，不要一次性把所有事情塞进一个总指令里。

你的项目现在已经有 7 份超长文档，如果一次性让 Codex“全部开发完成”，很容易出现：范围失控、实现半截、跳过测试、目录乱、接口不一致。正确做法是：

```text
一个总控指令
+
按阶段分批执行指令
```

Codex 的推理强度可以在配置里设置，例如 `model_reasoning_effort = "high"`；官方也建议 medium 作为多数交互式编码的均衡默认，高或更高强度用于最难任务。Codex Subagents 也支持按子代理配置 `model_reasoning_effort`，其中 high 适合复杂逻辑、边界情况、安全审查，medium 适合多数代理，low 适合简单任务。([OpenAI 开发者][1])

关于“Codex 能不能自动切换智能模式”：**不要依赖它自动切换**。你可以把每一批任务手动设置成合适模式，或者在 Codex 配置 / 子代理配置里指定 reasoning effort。Codex 可能在特定场景提示切换到更省额度的模型，但这不等于它会根据你每个开发阶段自动在“中 / 高 / 超高”之间切换。([OpenAI Help Center][2])

---

## 一、智能模式选择建议

| 阶段                                            |  建议模式 | 原因                 |
| --------------------------------------------- | ----: | ------------------ |
| 读取 7 份文档、做差距分析                                |     高 | 需要理解全局架构，但暂不写复杂代码  |
| ConfigLoader / Scanner / Detector             |     高 | 复杂度高，但可控           |
| StateMachine / Escape Hatch / Worktree        |    超高 | 高风险核心模块            |
| Executor Adapter：Codex / Cursor / Claude Code |    超高 | 涉及抽象边界、降级、超时、结果标准化 |
| Hub CRUD / Manifest API                       |     高 | 业务结构复杂，但主要是数据模型和接口 |
| Visual Collector / 报表                         | 高 / 中 | 采集链路用高，普通页面用中      |
| 补测试 / 修 lint / 文档调整                           |     中 | 成本低、效率高            |
| 改文案、补注释、格式化                                   | 低 / 中 | 不需要高推理             |

我的建议：

```text
默认选择：高
核心难点：超高
收尾修补：中
不要用低做核心开发
```

---

# 二、先给 Codex 的总控指令

这条只需要发一次，建议你在 Codex 第一个任务里使用。

```md
你现在是本项目的高级架构开发 Agent。请严格按照仓库中的 `第二大阶段/` 目录下 7 份 Markdown 文档进行开发。

## 一、唯一事实源

开发前必须优先阅读以下文档：

1. `第二大阶段/1-AI 工程资产操作系统：指令级 PRD 与技术蓝图.md`
2. `第二大阶段/2-物理工程结构与目录树.md`
3. `第二大阶段/3-核心数据模型与数据库设计.md`
4. `第二大阶段/4-API 契约与核心接口定义.md`
5. `第二大阶段/5-超详细的功能实现路线图.md`
6. `第二大阶段/6-极度严苛的测试验证清单.md`
7. `第二大阶段/7-最终交付验收清单.md`

## 二、项目边界

本系统涉及三个项目：

- `br-ai-spec`：本地 CLI / 技术栈扫描 / 项目初始化 / 状态机 / 执行器适配 / Worktree 隔离
- `skill-q-platform`：资产 Hub / Manifest / Agent Profile / Asset Factory / 审核发布
- `br-ai-spec-visual`：运行态可视化 / Collector API / 运行事件 / 治理报表

如果当前仓库只包含其中一个项目，请只在当前项目范围内实现对应能力，不要强行创建另外两个项目。

## 三、最高约束

必须遵守：

1. 不允许删除既有业务逻辑。
2. 不允许跳过文档要求。
3. 不允许一次性实现全部内容。
4. 不允许扫描阶段写业务项目。
5. 不允许上传目标项目源码。
6. 不允许绕过 `.ai-spec/ai-spec.lock.json`。
7. 不允许修改 Hub 已发布资产正文。
8. 不允许把 Codex / Cursor / Claude Code 写死为唯一执行器。
9. 不允许状态机无限重试。
10. 不允许在原始工作区直接修改业务代码。
11. 所有英文提示、错误提示、CLI 输出提示必须使用中文。
12. 所有核心数据结构必须有类型定义。
13. 所有 JSON 配置必须有 schema 校验。
14. 所有核心模块必须补测试。

## 四、执行方式

请采用“虚拟子代理模式”，但不要创建失控的并发 Agent。

每个任务必须按以下角色顺序执行：

1. 架构审查子代理：确认本次改动范围、目录、边界、风险。
2. 实现子代理：只实现当前任务要求的代码。
3. 测试子代理：补充单元测试和必要集成测试。
4. 安全审计子代理：检查隐私、源码上传、checksum、防篡改、执行器权限。
5. 回归审查子代理：确认不破坏既有功能。

## 五、全局开发顺序

必须按以下顺序推进，不允许跳级：

1. ConfigLoader
2. TechScannerEngine
3. InitPlan / InitApplier
4. `ai-spec.lock.json` / `registry.index.json` / `context-index.json`
5. GlobalCache / Sync
6. AssetTamperChecker
7. Branch / Worktree
8. StateMachine / CircuitBreaker / EscapeHatch
9. ContextBuilder
10. PrivacyFilter / Telemetry
11. Hub Asset / Manifest API
12. Agent Profile
13. Executor Adapter：Codex / Cursor / Claude Code
14. Visual Collector
15. Asset Factory

## 六、当前任务要求

先不要直接大规模写代码。第一步只做代码盘点和开发计划。

请完成：

1. 阅读 `第二大阶段/` 下 7 份文档。
2. 识别当前仓库结构。
3. 判断当前代码已经实现了哪些能力。
4. 判断当前代码缺失哪些能力。
5. 输出 `docs/implementation-gap-analysis.md`。
6. 输出 `docs/p0-implementation-plan.md`。

## 七、输出文件

只允许新增或更新：

1. `docs/implementation-gap-analysis.md`
2. `docs/p0-implementation-plan.md`

## 八、禁止行为

- 不要删除文件。
- 不要修改现有业务逻辑。
- 不要安装依赖。
- 不要直接开始实现 P0。
- 不要创建无关目录。
- 不要修改 package.json。
- 不要实现 Hub API。
- 不要实现 Visual API。
- 不要实现执行器 Provider。
- 不要上传、打印或记录源码正文到外部服务。

## 九、最终输出

完成后请输出：

1. 已创建或修改的文件列表。
2. 当前代码缺失能力 Top 20。
3. P0 第一批建议开发任务。
4. 风险点。
5. 需要我确认的事项。
```

这条建议使用：**高**。

---

# 三、第二条：正式开发 P0 第一批

等 Codex 输出差距分析之后，再发这一条。

````md
请基于以下文档继续开发：

- `docs/implementation-gap-analysis.md`
- `docs/p0-implementation-plan.md`
- `第二大阶段/1-AI 工程资产操作系统：指令级 PRD 与技术蓝图.md`
- `第二大阶段/2-物理工程结构与目录树.md`
- `第二大阶段/3-核心数据模型与数据库设计.md`
- `第二大阶段/4-API 契约与核心接口定义.md`
- `第二大阶段/5-超详细的功能实现路线图.md`
- `第二大阶段/6-极度严苛的测试验证清单.md`
- `第二大阶段/7-最终交付验收清单.md`

## 当前任务

只实现 P0 第一批能力，优先修改 `br-ai-spec` 项目。

本批只允许实现：

1. ConfigLoader
2. TechScannerEngine 基础骨架
3. Scanner 类型定义
4. BoundaryResolver 基础实现
5. FactExtractor 基础实现
6. DetectorRegistry
7. DetectionAggregator
8. NextJsDetector
9. ReactViteDetector
10. VueViteDetector
11. SpringBootDetector
12. `scan` CLI 命令
13. 对应单元测试

## 必须新增或完善的目录

请根据当前项目实际结构创建或补齐：

```text
src/config/
src/scanner/
src/scanner/boundary/
src/scanner/facts/
src/scanner/detectors/
src/scanner/aggregator/
src/cli/commands/
tests/unit/scanner/
tests/unit/config/
tests/fixtures/
````

如果项目已有类似目录，请优先复用，不要重复创建平行结构。

## 具体实现要求

### 1. ConfigLoader

实现配置优先级：

1. CLI 参数
2. 当前 run 配置
3. `.ai-spec/policy.json`
4. `.ai-spec/project.json`
5. `.ai-spec/workspace.json`
6. Agent Profile
7. `~/.ai-spec-auto/config.json`
8. 系统默认值

隐私策略必须强制关闭：

```json
{
  "uploadSourceCode": false,
  "uploadRawPrompt": false,
  "uploadRawResponse": false,
  "uploadAbsolutePath": false,
  "uploadUserName": false
}
```

### 2. TechScannerEngine

必须采用四层架构：

```text
BoundaryResolver
FactExtractor
DetectorRegistry
DetectionAggregator
```

扫描阶段必须只读，不允许写任何业务项目文件。

### 3. Detector 输出结构

每个 Detector 必须返回：

```ts
{
  detector: string;
  domain: 'frontend' | 'backend' | 'mobile' | 'fullstack' | 'devops' | 'data' | 'unknown';
  language: string[];
  frameworks: string[];
  buildTool?: string;
  confidence: number;
  tags: string[];
  manifestSlug?: string;
  reasons: string[];
}
```

### 4. DetectorRegistry

不能只保留最高分，必须保留：

* primary
* candidates
* tags
* reasons

### 5. scan CLI

实现命令：

```bash
ai-spec-auto scan .
ai-spec-auto scan . --explain
```

输出必须使用中文。

## 测试要求

必须新增或完善：

```text
tests/unit/scanner/tech-scanner-engine.test.ts
tests/unit/scanner/detector-registry.test.ts
tests/unit/config/config-loader.test.ts
```

至少覆盖：

1. Next.js 识别。
2. React Vite 识别。
3. Vue Vite 识别。
4. Spring Boot 识别。
5. DetectorRegistry 保留 candidates。
6. 扫描阶段不得写文件。
7. CLI 参数优先级高于 policy。
8. 隐私策略强制关闭源码上传。

## 严格禁止

* 不允许实现 P1 / P2 / P3。
* 不允许实现 Hub API。
* 不允许实现 Visual API。
* 不允许实现 Codex / Cursor / Claude Code Provider。
* 不允许修改业务源码。
* 不允许删除现有代码。
* 不允许全量 AST 解析。
* 不允许在扫描阶段写文件。
* 不允许为了测试大量改动项目配置。

## 完成后输出

请输出：

1. 修改文件列表。
2. 新增文件列表。
3. 测试命令。
4. 已通过的测试。
5. 未完成项。
6. 下一步建议。

````

这条建议使用：**高**。

---

# 四、第三条：P0 第二批，Init / Lock / Registry / Context Index

```md
请继续实现 P0 第二批能力。

## 前置要求

必须基于上一批已经完成的：

- ConfigLoader
- TechScannerEngine
- DetectorRegistry
- scan CLI

## 当前任务范围

只允许实现：

1. InitPlan
2. InitService
3. InitApplier
4. ManifestInstaller 基础结构
5. `.ai-spec/project.json` 写入
6. `.ai-spec/policy.json` 写入
7. `.ai-spec/ai-spec.lock.json` 写入
8. `.agents/registry.index.json` 写入
9. `.ai-spec/context-index.json` 写入
10. IDE 指针文件注入：
    - `.codex/instructions.md`
    - `.cursor/rules/ai-spec-auto.mdc`
    - `CLAUDE.md`
    - `memory.md`

## 最高约束

1. `init plan` 阶段不得写入任何文件。
2. 只有 `init apply` 且用户确认后才能写文件。
3. 不允许写入完整 Rule / Skill 正文。
4. `registry.index.json` 只保存索引，不保存正文。
5. `context-index.json` 必须支持 progressive 加载。
6. 已存在 `CLAUDE.md`、`.cursor`、`.codex` 时，只能更新 AI-SPEC-AUTO 管理区块。
7. 所有 CLI 输出必须是中文。

## 测试要求

必须新增或完善：

```text
tests/unit/init/init-service.test.ts
tests/unit/project/lock-file.test.ts
tests/unit/project/registry-index.test.ts
tests/unit/project/context-index.test.ts
tests/unit/init/ide-injector.test.ts
````

至少覆盖：

1. init plan 不写文件。
2. apply 写入 project.json。
3. apply 写入 policy.json。
4. apply 写入 ai-spec.lock.json。
5. apply 写入 registry.index.json。
6. apply 写入 context-index.json。
7. registry 不包含完整 content。
8. context-index 包含 planning / implementation / diagnosing 阶段加载规则。
9. IDE 文件只写指针。
10. 已存在文件时只更新管理区块。

## 禁止行为

* 不允许实现状态机。
* 不允许实现 Worktree。
* 不允许实现 Executor Provider。
* 不允许实现 Hub 后端 API。
* 不允许实现 Visual 后端 API。

完成后请输出：

1. 修改文件列表。
2. 新增文件列表。
3. 测试命令。
4. 测试结果。
5. 下一步建议。

````

这条建议使用：**高**。

---

# 五、第四条：P0 第三批，Sync / Cache / Check / Guard

```md
请继续实现 P0 第三批能力。

## 当前任务范围

只允许实现：

1. GlobalCache
2. AssetCache
3. ManifestCache
4. AgentProfileCache
5. HubClient 基础封装
6. sync 命令
7. check 命令
8. guard assets 命令
9. AssetTamperChecker
10. checksum 工具

## 实现要求

1. 资产正文必须缓存到 `~/.ai-spec-auto/cache/assets/<checksum>/content.md`。
2. metadata 必须缓存到 `~/.ai-spec-auto/cache/assets/<checksum>/metadata.json`。
3. Agent Profile 必须缓存到 `~/.ai-spec-auto/cache/agent-profiles/`。
4. cache 命中时不请求 Hub。
5. cache 缺失时请求 Hub。
6. checksum 不一致必须阻断。
7. check 必须校验 lock、registry、cache、overlay。
8. guard assets 必须适合作为 Git hook / CI 检查命令。
9. 所有错误提示必须使用中文。
10. 不允许上传源码。

## 测试要求

必须新增或完善：

```text
tests/unit/cache/asset-cache.test.ts
tests/unit/security/checksum.test.ts
tests/unit/security/asset-tamper-checker.test.ts
tests/integration/security/tamper-check.test.ts
````

必须覆盖：

1. cache 命中。
2. cache miss。
3. Hub 返回 checksum 不一致。
4. 标准资产被篡改。
5. registry 与 lock 不一致。
6. overlay checksum 变化。
7. sync 恢复被篡改 cache。
8. guard assets 返回正确退出码。

完成后输出：

1. 修改文件列表。
2. 新增文件列表。
3. 测试命令。
4. 测试结果。
5. 下一步建议。

````

这条建议使用：**高**。

---

# 六、第五条：P0 第四批，Worktree / StateMachine / ContextBuilder

这批是核心难点，建议使用**超高**。

```md
请继续实现 P0 第四批核心能力。

## 智能模式建议

本任务涉及状态机、熔断、Git Worktree、上下文构建，属于高风险核心模块。请使用最高可用推理强度执行。

## 当前任务范围

只允许实现：

1. DirtyChecker
2. DirtyStrategyHandler
3. BranchManager
4. WorktreeManager
5. MultiRepoWorktreePlan 基础结构
6. StateMachine
7. TransitionGuard
8. RunService
9. CircuitBreaker
10. EscapeHatch
11. IncidentWriter
12. ContextBuilder
13. ContextPlanner
14. ContextLoader
15. ContextBudget

## 实现要求

### Git / Worktree

1. `/spec-start` 默认创建 branch。
2. `/spec-start` 默认创建 worktree。
3. 默认 dirtyStrategy 必须是 `block`。
4. 不允许默认自动 stash。
5. dirtyStrategy 支持：
   - block
   - wip-commit
   - patch-snapshot
   - ignore
6. 原始工作区不得被 AI 修改。
7. 多仓库部分失败时必须回滚已创建 worktree。

### StateMachine

必须支持状态：

```text
initialized
planning
branch_preparing
context_building
executing
verifying
diagnosing
recovering
human_review
suspended
completed
archived
failed
cancelled
````

必须阻断非法状态流转。

### CircuitBreaker

必须支持：

1. Token 超预算熔断。
2. 同一文件重复修改超过阈值熔断。
3. 阶段失败超过阈值熔断。
4. 执行器超时熔断。
5. 自动修复超过次数进入 human_review。

### ContextBuilder

必须按阶段渐进式加载：

* planning：Role / Flow
* implementation：Rule / Skill / Agent Profile
* verification：验证规则和测试命令
* review：Review Rule
* diagnosing：Diagnostic Agent

不允许全量加载所有资产。

## 测试要求

必须新增或完善：

```text
tests/unit/git/dirty-strategy.test.ts
tests/unit/git/worktree-manager.test.ts
tests/unit/state-machine/state-machine.test.ts
tests/unit/state-machine/circuit-breaker.test.ts
tests/unit/context/context-builder.test.ts
tests/integration/spec-start/spec-start-worktree.test.ts
tests/integration/state-machine/escape-hatch.test.ts
```

必须覆盖：

1. dirtyStrategy=block。
2. dirtyStrategy=patch-snapshot。
3. dirtyStrategy=wip-commit。
4. worktree 创建。
5. branch 创建。
6. 多仓库失败回滚。
7. 非法状态流转。
8. executor 失败进入 diagnosing。
9. token 超预算进入 suspended。
10. ContextBuilder 按阶段加载。
11. shared contract 缺失时跨端需求阻断。

## 禁止行为

* 不允许实现 Codex / Cursor / Claude Code Provider。
* 不允许实现 Hub API。
* 不允许实现 Visual API。
* 不允许直接修改原始工作区。
* 不允许无限重试。
* 不允许上传源码。

完成后输出：

1. 修改文件列表。
2. 新增文件列表。
3. 测试命令。
4. 测试结果。
5. 已知风险。
6. 下一步建议。

````

---

# 七、第六条：P2 执行器适配层

这批也建议使用**超高**。

```md
请继续实现 Executor Adapter Layer。

## 当前任务范围

只允许实现：

1. IExecutorProvider
2. ExecutorRegistry
3. ExecutorSelector
4. ExecutorRunner
5. CodexExecutorProvider
6. CursorExecutorProvider
7. ClaudeCodeExecutorProvider
8. Executor timeout / retry
9. 执行器结果标准化

## 最高约束

1. Codex / Cursor / Claude Code 必须是并列执行器。
2. 状态机只能依赖 IExecutorProvider。
3. 不允许把某一个执行器写死为唯一执行器。
4. CLI 显式指定 executor 优先级最高。
5. Agent Profile 推荐 executor 优先于 policy。
6. policy defaultExecutor 优先于 global config。
7. local-assisted 默认优先 Cursor。
8. local-auto 默认优先 Codex。
9. remote-orchestrated 默认优先 Codex。
10. 所有执行器不可用时抛出 EXECUTOR_NOT_AVAILABLE。
11. 所有执行器必须支持 timeout。
12. 所有执行器输出必须标准化为 ExecutorExecutionResult。
13. 所有英文提示必须使用中文。

## Codex Provider

实现：

- checkAvailability
- prepare
- execute
- verify 可选
- cleanup 可选

Codex 适合 local-auto 和 remote-orchestrated。

## Cursor Provider

实现：

- checkAvailability
- prepare
- execute

Cursor 适合 local-assisted。如果当前环境不支持 headless，必须返回 EXECUTOR_PERMISSION_DENIED，并提示切换 Codex 或 Claude Code。

## Claude Code Provider

实现：

- checkAvailability
- prepare
- execute
- verify

Claude Code 适合复杂改造和长任务。

## 测试要求

必须新增或完善：

```text
tests/unit/executor/executor-selector.test.ts
tests/unit/executor/providers/codex-provider.test.ts
tests/unit/executor/providers/cursor-provider.test.ts
tests/unit/executor/providers/claude-code-provider.test.ts
tests/integration/executor/executor-switch.test.ts
````

必须覆盖：

1. CLI 指定 codex。
2. CLI 指定 cursor。
3. CLI 指定 claude-code。
4. policy 默认 cursor。
5. Agent Profile 默认 claude-code。
6. fallback 机制。
7. 所有执行器不可用。
8. Codex 超时。
9. Cursor 不支持 headless。
10. Claude Code 输出解析。
11. 执行器输出不合法。

完成后输出：

1. 修改文件列表。
2. 新增文件列表。
3. 测试命令。
4. 测试结果。
5. 下一步建议。

````

---

# 八、总策略

你现在最适合的执行方式是：

```text
第 1 轮：总控指令，做差距分析，高
第 2 轮：ConfigLoader + Scanner，高
第 3 轮：Init / Lock / Registry / ContextIndex，高
第 4 轮：Sync / Cache / Check / Guard，高
第 5 轮：Worktree / StateMachine / ContextBuilder，超高
第 6 轮：Executor Adapter，超高
第 7 轮：Hub API / Visual Collector，高
第 8 轮：补测试 / 修 lint / 修类型，中
````

不要让 Codex 一次性开发全部。你现在可以先复制**第二部分的总控指令**，模式选**高**。

[1]: https://developers.openai.com/codex/config-basic?utm_source=chatgpt.com "Config basics – Codex"
[2]: https://help.openai.com/zh-hant-hk/articles/9624314-model-release-notes?utm_source=chatgpt.com "Model Release Notes"
