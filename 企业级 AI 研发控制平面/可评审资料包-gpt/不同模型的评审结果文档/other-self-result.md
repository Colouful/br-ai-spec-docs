# 一、评审结论摘要

**结论：有条件通过，不建议直接进入大规模推广。**

这套 **Enterprise AI Control Plane V0.1 / 企业级 AI 研发控制平面** 的方向是成立的，而且抓住了 AI 编码在企业落地中的关键问题：上下文失控、AI 乱改、缺少验收证据、多 Agent 并行不可控、企业规范无法资产化、运行过程不可审计等。PRD 中对这些痛点的识别比较准确，方案也明确不是单一 Prompt 仓库，而是围绕规范资产、OpenSpec、Task DAG、Git worktree、Hook、Test Gate、Evidence、Visual 观测构建统一控制体系。

但当前方案最大的问题是：**V0.1 同时引入了过多企业级概念和执行机制，容易从“最小可落地控制平面”膨胀成“三仓 + 多 Agent + 多门禁 + 多协议 + 可视化 + 资产治理”的大型平台工程。** 对一个 V0.1 来说，目标闭环是清楚的，但建设范围偏重，尤其是 `skill-q-platform`、`br-ai-spec-visual`、多 Agent、Git worktree、Evidence、OpenSpec 全部同时推进，会带来较高实现复杂度和团队接入成本。

我的判断是：

> **可以作为企业级 AI 研发控制平面的架构方向通过；但 V0.1 必须收敛为“本地控制闭环 + 单样板链路验证”，暂缓复杂 Hub、复杂 Visual、复杂 RBAC、多租户、多模型治理、Agent 市场等能力。**

总体评分：**7.1 / 10**
建议状态：**有条件通过**

---

# 二、关键优点

## 1. 产品定位是清晰的

方案明确要解决的不是“让 AI 多写点代码”，而是把 AI IDE 纳入企业研发流程，让 AI 开发变得**可控、可验证、可审计、可恢复**。这一点方向正确，而且比单纯做 Prompt、规则库、Agent 编排更有企业价值。

## 2. 三层控制思路基本合理

当前架构把系统拆成：

* `br-ai-spec`：本地控制器
* `skill-q-platform`：资产治理中心
* `br-ai-spec-visual`：运行观测中心
* Cursor / Claude Code / Codex 等 AI IDE：执行器

这个边界设计总体合理，尤其是把真正改代码的能力放在本地控制器，而不是让平台直接接触业务源码，是一个正确的低侵入方向。

## 3. “Graph-Governed Multi-Agent” 比普通多 Agent 更靠谱

方案没有走“多 Agent 聊天室”的路线，而是强调：

* Graph 管流程
* Agent 管专业判断
* Executor 管代码变更
* Hook 管约束
* Test Gate 管真实性
* Evidence 管审计
* Visual 管观测

这个设计思想是对的。企业级 AI 协作不能只靠 Agent 自由发挥，必须有图、契约、门禁、证据。

## 4. Git worktree 用于执行隔离是亮点

用 **一个可独立交付 Task 对应一个 worktree / task branch / patch bundle / evidence**，可以有效降低多 Agent 并行修改造成的污染和冲突。这个设计比“多个 Agent 在同一工作区并发写文件”可靠得多。

## 5. Evidence 证据落盘非常值得保留

L2 / L3 需求强制保留 OpenSpec、测试计划、测试结果、验收清单、diff summary、final report 等证据，这一点非常适合企业内部评审、质量追溯、AI 交付复盘。

## 6. 渐进式资产披露设计正确

方案明确禁止一次性把所有 Rule、Skill、Memory、历史 Run 日志塞给模型，而是通过 Manifest、索引、摘要、任务视图逐步加载。这一点能有效降低上下文膨胀、幻觉和模型误读风险。

---

# 三、关键问题

## 1. V0.1 范围偏大

V0.1 同时包含项目初始化、OpenSpec、Context Pack、Task DAG、Git worktree、Executor Pool、Hook、Test Gate、Evidence、Resume、Visual 上报，还涉及 Hub 资产治理和三仓联调。虽然路线图中强调 V0.1 聚焦本地闭环，但实际 P0 能力已经非常重。

**风险：** 如果团队人数不多，V0.1 很容易变成“协议写得很好，但样板链路跑不稳”。

## 2. `br-ai-spec` 承担职责过多

`br-ai-spec` 同时负责 CLI、项目扫描、OpenSpec、资产加载、上下文压缩、DAG 规划、worktree 管理、Executor 调度、Hook、Test Gate、Evidence、Visual 上报等。这个本地控制器是核心，但也最容易变成巨型复杂模块。

**建议：** V0.1 需要把 `br-ai-spec` 内部再分为最小核心和可插拔扩展，否则后续维护压力会很大。

## 3. AI 模型适配层缺失

方案适配的是 Cursor、Claude Code、Codex 等 **AI IDE**，但没有看到明确的 **LLM Gateway / Model Gateway** 设计。也就是说，它更多是“AI IDE 控制平面”，还不是完整的“多模型 AI 原生控制平面”。文档明确不把 Cursor、Claude、Codex 任一工具作为唯一标准，但没有进一步给出多模型路由、fallback、成本治理、Prompt 版本治理、模型审计的独立模块。

**影响：** 面向未来 AI 模型快速演进时，这一层会成为架构短板。

## 4. 权限与安全治理还不够企业级

方案有 Scope Guard、Secret Guard、Dangerous File Guard、Manual Approval Gate 等安全门禁，但资料里没有看到完整的 RBAC / ABAC、组织空间、资源权限、审批流、审计策略、敏感数据分级、Prompt 注入防护、工具调用沙箱等企业级设计。当前 PRD 也明确 V0.1 暂不支持完整多租户权限。

**结论：** V0.1 可做试点，但不能宣称已具备完整企业级安全治理能力。

## 5. 开发者上手成本偏高

业务开发者要理解 OpenSpec、Task DAG、writeSet、lockKeys、Context Pack、Evidence、Hook、Test Gate、worktree、Agent Profile、Manifest 等概念。虽然这些概念对平台治理有价值，但对普通业务团队来说门槛较高。术语体系本身比较完整，但也说明认知负担不低。

**建议：** 必须设计“极简路径”：`init → plan → run → verify → report`，普通业务开发者不应该先学习完整平台模型。

---

# 四、分维度详细评审

## 1. 整体架构合理性

### 判断

整体架构方向合理，边界基本清晰，但 V0.1 的架构颗粒度过细，平台化倾向偏强。

方案采用“资产治理中心 + 本地控制器 + AI IDE 执行器 + 运行观测中心”的结构，这个大边界是清楚的。`br-ai-spec` 在业务项目本地执行，`skill-q-platform` 管理企业 AI 资产，`br-ai-spec-visual` 负责运行观测，AI IDE 作为实际执行环境，职责划分整体成立。

### 优点

* 本地控制器模式降低了业务源码上传和平台直接改代码的风险。
* Hub 只做资产治理，Visual 只做观测，职责边界相对清晰。
* Graph + Agent + Hook + Test + Evidence 的组合比纯 Agent 编排更适合企业级落地。
* OpenSpec 作为需求事实源，有利于需求、设计、实现、测试、验收统一闭环。

### 风险

* `br-ai-spec` 过重，未来可能变成“本地小平台”，维护难度高。
* 三仓同时推进，联调成本高。
* 架构层次还缺少明确的“模型适配层 / 工具适配层 / 权限治理层 / 策略引擎层”。
* 当前更像研发流程控制器，还不是完整 AI 应用平台或 Agent 平台底座。

### 不合理之处

最大的不合理不是方向，而是 **V0.1 的复杂度与验证目标不匹配**。如果目标只是跑通“中台金融系统新增产品配置管理模块”，完全不需要在第一阶段实现完整 Hub、完整 Visual、复杂多 Agent 分层和复杂资产生命周期。

### 推荐目标架构方向

建议调整为五层：

1. **接入层**：CLI、IDE Adapter、CI Adapter、Webhook。
2. **控制编排层**：OpenSpec、Task DAG、Run State、Checkpoint、Policy Engine。
3. **执行隔离层**：worktree、Executor Adapter、Patch Bundle、Merge。
4. **质量治理层**：Hook、Test Gate、Evidence、Approval Gate。
5. **平台治理层**：Asset Hub、Model Gateway、Visual、Metrics、Audit。

---

## 2. 目标设计是否合理

### 判断

目标本身合理，但 V0.1 目标过满。

PRD 明确 V0.1 要跑通一条从自然语言需求到 OpenSpec、Context Pack、Task DAG、worktree 执行、Test Gate、Evidence、Visual、Final Report 的完整企业级闭环。这个闭环清晰、可验证，也能回应 AI 编码在企业中的核心痛点。

### 应保留目标

* 跑通一个真实中台金融系统样板需求。
* L2 / L3 需求强制 OpenSpec。
* Context Pack 和渐进式资产加载。
* Task DAG + worktree 隔离。
* Hook + Test Gate。
* Evidence + final report。
* Resume / checkpoint。

### 应降低优先级

* Hub 完整资产 CRUD 和审核发布。
* Visual 完整页面。
* 多 Agent 全角色分层。
* 跨 IDE 完整适配。
* 复杂 RBAC。
* 多项目、多团队、多租户。
* 资产市场、Agent Hub、资源中心。

### 需要补充量化指标

当前成功指标有“标准 L2 需求完整跑通 100%、证据落盘完整率 100%、越权文件修改拦截 100%”等，这些指标方向正确。 但还应增加：

| 指标                 |       建议目标 |
| ------------------ | ---------: |
| 从需求到 Task DAG 生成耗时 |    ≤ 10 分钟 |
| L2 样板需求人工干预次数      |      ≤ 3 次 |
| Patch 合并冲突率        |      ≤ 20% |
| Test Gate 误拦截率     |      ≤ 10% |
| 普通开发者首次完成接入耗时      |    ≤ 30 分钟 |
| 单次 Run 可恢复成功率      |      ≥ 90% |
| 上下文压缩后关键事实丢失率      | 0 个关键验收点丢失 |

---

## 3. 面向未来 AI 大模型发展的适应性

### 评分：6.5 / 10

### 判断

当前方案对 **AI IDE 演进** 有适配性，但对 **多模型原生治理** 适配不足。

方案强调不绑定 Cursor、Claude、Codex 任一工具，并计划后续生成 Cursor Rules、Claude 配置、Codex `AGENTS.md` 等 IDE Adapter，这是正确方向。 但资料中没有看到独立的 Model Gateway、模型路由、模型 fallback、模型成本控制、Prompt 版本管理、模型输出审计等模块。

### 容易被未来模型能力替代的部分

* 过细的专家 Agent 分层：未来模型更强后，Frontend Expert、Backend Expert、Architect Agent 可能不需要常驻分离。
* 复杂 Prompt / Skill 层：部分能力可能被模型原生工具调用、代码理解和长期记忆替代。
* 过重的 OpenSpec 生成流程：未来模型可以从需求、代码、历史变更中自动生成更轻量的规格视图。

### 不容易被替代的部分

* Evidence 证据。
* Test Gate。
* Hook / Scope Guard。
* Git worktree 隔离。
* 审计。
* 权限。
* 需求事实源。
* 任务依赖与写入范围约束。

这些属于企业治理能力，不会因为模型变强而消失。

### 建议补充

必须增加 **AI Model Adapter / LLM Gateway**：

| 能力        | 说明                                                    |
| --------- | ----------------------------------------------------- |
| 模型抽象      | OpenAI / Claude / Gemini / Qwen / DeepSeek / 本地模型统一接入 |
| 路由策略      | 按任务类型、成本、上下文长度、敏感等级选择模型                               |
| fallback  | 模型失败、超时、限流时切换                                         |
| 灰度        | 新模型按项目、团队、任务类型灰度                                      |
| 成本控制      | Run / Task / Agent 级 token 与费用预算                      |
| Prompt 版本 | Prompt、System Instruction、Tool Schema 版本化             |
| 输出审计      | 模型输出、工具调用、拒绝、异常统一记录                                   |
| 安全策略      | Prompt 注入检测、敏感信息检测、工具调用授权                             |

---

## 4. 开发者上手难度

### 评分：5.8 / 10

### 判断

对平台团队可接受，对普通业务开发者偏难。

方案中概念体系非常完整：OpenSpec、Manifest、Rule、Skill、Agent Profile、Hook Spec、Test Gate、Context Pack、Task DAG、writeSet、lockKeys、Executor Pool、Patch Bundle、Evidence 等都有清晰定义。 但完整不等于易用。普通业务开发者第一次接入会有明显学习压力。

### 高认知成本概念

建议合并或弱化以下概念：

| 当前概念                                    | 建议处理                      |
| --------------------------------------- | ------------------------- |
| Manifest / Rule / Skill / Agent Profile | 对普通开发者隐藏为“规范包”            |
| writeSet / readSet / lockKeys           | 在 UI 或 CLI 中自动生成，只在高级模式暴露 |
| Evidence / final-report / artifacts     | 统一叫“交付证据”                 |
| Task DAG                                | 普通用户看到“任务清单”，高级用户看到 DAG   |
| Hook / Test Gate / Guard                | 统一叫“质量门禁”                 |
| OpenSpec View / Context Pack            | 默认自动生成，不要求业务开发者理解细节       |

### 推荐最小接入路径

```bash
br-spec init
br-spec plan "新增产品配置管理模块"
br-spec run
br-spec verify
br-spec report
```

普通开发者只需要理解 5 个动作：

1. 初始化项目。
2. 描述需求。
3. 查看任务计划。
4. 执行。
5. 看报告和证据。

其他能力应该作为高级配置存在。

---

## 5. 对业务项目的入侵性

### 评分：7.5 / 10

### 判断

源码入侵性较低，但流程入侵性中等偏高。

方案明确业务项目只新增 `openspec/`、`.ai-spec/`、`.ai-spec-local/`，业务源码保持原样，`.ai-spec-local/` 不入 Git，worktree 可放项目外部。这是低源码侵入设计。

但另一方面，强制 L2 完整 OpenSpec、强制 Evidence、强制 Test Gate、强制 worktree，会改变业务团队开发流程，因此 **流程侵入性不低**。

### 高入侵风险点

| 风险点               | 说明                       |
| ----------------- | ------------------------ |
| `openspec/` 入 Git | 团队可能不愿把需求规格放进代码仓库        |
| `.ai-spec/` 入 Git | 会引入平台配置和规范资产，影响仓库结构      |
| L2 强制完整 OpenSpec  | 小中型需求可能觉得流程过重            |
| Git worktree 强制   | 对不熟悉 Git worktree 的团队有门槛 |
| Test Gate 强制      | 测试薄弱项目接入困难               |
| Evidence 强制       | 会增加交付流程成本                |

### 推荐低入侵接入方式

应支持三种模式：

| 模式                      | 适用场景                  | 侵入程度 |
| ----------------------- | --------------------- | ---- |
| Shadow Mode             | 只生成计划、报告，不实际改代码       | 最低   |
| Assist Mode             | 生成 patch，由人手动应用       | 低    |
| Controlled Execute Mode | worktree 执行、门禁、证据完整闭环 | 中    |

V0.1 应优先支持 **Assist Mode + Controlled Execute Mode**，而不是一开始就要求所有项目完整接入。

---

## 6. 系统可靠性与稳定性

### 评分：6.7 / 10

### 判断

可靠性设计有框架，但缺少工程级细节。

方案已有 Resume、run.log.jsonl、checkpoint、worktree-index、Evidence、Repair Limit Guard、Test Gate、Scope Guard 等机制，说明可靠性意识是比较强的。

但资料中没有充分展开：

* 超时策略
* 重试策略
* 幂等键
* Agent 调用失败恢复
* 模型调用失败 fallback
* IDE Adapter 失败处理
* 命令执行 sandbox
* 长任务心跳
* Run 状态机
* 失败分类
* 中断恢复的一致性校验
* Visual 上报失败后的本地缓冲

### 单点故障风险

| 单点                | 风险                |
| ----------------- | ----------------- |
| `run.bundle.json` | 当前任务状态总账，一旦损坏影响恢复 |
| Task DAG 生成器      | DAG 不准会导致后续全部偏离   |
| Merge Agent       | 合并策略错误可能引入隐性缺陷    |
| Test Gate 配置      | 测试命令错误会误判交付质量     |
| worktree 清理       | 清理策略错误可能丢失排查现场    |
| Visual 上报         | 如果同步阻塞执行，会影响本地闭环  |

### 必须补充的可靠性设计

1. Run 状态机：`created → planned → running → verifying → repairing → completed / failed / cancelled`。
2. 幂等 runId / taskId / patchId / evidenceId。
3. 每个命令执行必须有 timeout、exit code、stdout、stderr、artifact path。
4. Visual 上报必须异步，不得阻塞本地执行。
5. `run.bundle.json` 应有备份和校验摘要。
6. Repair 必须限定 diff 范围和次数。
7. worktree clean 必须先确认 task status 和 merge status。
8. Test Gate 必须支持 flaky test 标记，但不能绕过关键测试。

---

## 7. 安全性、权限与治理能力

### 评分：5.6 / 10

### 判断

V0.1 有安全门禁雏形，但未达到完整企业级治理成熟度。

方案中已有 Scope Guard、Secret Guard、Dangerous File Guard、Manual Approval Gate、Evidence Gate 等，这是不错的起点。 但 PRD 明确完整多租户权限暂不支持，说明目前还不是企业级安全治理闭环。

### 当前不足

| 能力          | 当前判断                             |
| ----------- | -------------------------------- |
| 身份认证        | 资料不足                             |
| RBAC / ABAC | 资料不足                             |
| 资源级权限       | 资料不足                             |
| 动作级权限       | 资料不足                             |
| 多租户隔离       | V0.1 暂不支持                        |
| 环境隔离        | 资料不足                             |
| 敏感数据分级      | 资料不足                             |
| Prompt 注入防护 | 未看到系统设计                          |
| 工具调用沙箱      | 未看到系统设计                          |
| 审批流         | 只有 Manual Approval Gate 方向，缺流程细节 |
| 审计查询        | Visual 有事件和证据，但缺审计模型             |

### 必须补充的治理能力

* 企业 SSO / 用户身份。
* 项目、团队、仓库、资产、Run、Evidence 的权限模型。
* Agent 权限模型：能读什么、能写什么、能执行什么命令。
* Tool allowlist / denylist。
* Secret 扫描和脱敏。
* Prompt Injection 检测策略。
* 高风险操作审批：数据库、权限、MQ、缓存、资金、风控。
* 审计日志不可篡改策略。

---

## 8. 可维护性与工程复杂度

### 评分：6.4 / 10

### 判断

模块边界有设计，但整体复杂度偏高。

代码实现设计中，`br-ai-spec` 被拆分为 cli、config、project-scanner、openspec、context、assets、agents、task-dag、scheduler、worktree、patch、merge、hooks、test-gates、evidence、visual-client、resume、shared 等模块。这个拆分完整，但实现量很大。

### 容易成为技术债的地方

| 技术债点            | 原因                |
| --------------- | ----------------- |
| Task DAG 自动生成   | 需求理解错误会传导到执行阶段    |
| lockKeys 设计     | 不同业务域的资源冲突很难自动判断  |
| Context 压缩      | 压缩错误会丢失关键事实       |
| Agent Profile   | 过多角色会导致维护成本高      |
| Hook DSL        | 如果过早自定义，后续兼容困难    |
| Evidence Schema | 一旦不稳定，历史报告难以兼容    |
| 多 IDE Adapter   | 各 IDE 能力变化快，适配成本高 |

### 推荐工程治理方案

* V0.1 只冻结核心 JSON Schema：Run、Task、Evidence、Asset、Hook、TestGate。
* 先实现本地文件资产，不强依赖 Hub。
* 先实现单 Agent / 少量 Executor，再扩展多 Agent。
* DAG 必须支持人工编辑。
* 所有协议文件必须有版本号。
* 所有 CLI 命令必须具备 dry-run。
* 所有危险操作必须有 `--force` 或审批确认。

---

## 9. 扩展性与复用性

### 评分：7.2 / 10

### 判断

扩展性设计方向较好，但目前协议偏私有，需要增强标准化接口。

资产治理中心管理 Manifest、Rule、Skill、Agent Profile、Hook Spec、Test Gate、Context Policy、Evidence Policy，具备未来资源中心、模板中心、Agent Hub 的基础。

但当前资料主要是私有协议，并未看到对 MCP、OpenAPI、JSON Schema Registry、标准 Tool Schema、标准 Trace Schema 的明确兼容策略。

### 推荐增强

* 所有 Tool / Skill 尽量兼容 MCP Tool Schema 或 OpenAPI。
* Visual Trace 尽量兼容 OpenTelemetry 思路。
* Evidence Schema 应可导出给 CI/CD、测试平台、研发效能平台。
* Asset Bundle 应支持离线包、本地文件、Hub API 三种来源。
* IDE Adapter 应作为插件，不应写死在核心流程中。

---

## 10. 成本与投入产出比

### 判断：中高成本，中长期 ROI 有潜力

这个方案不是小工具，而是企业级研发控制体系。它的收益主要来自：

* 降低 AI 乱改风险。
* 提升复杂需求交付稳定性。
* 沉淀企业规范资产。
* 提供可审计证据。
* 支撑未来团队级 AI 研发标准化。

但它的成本也明显：

* 平台研发成本高。
* 规范制定成本高。
* 业务团队学习成本高。
* 测试补齐成本高。
* Visual 和 Hub 运维成本高。
* 多 IDE 适配成本持续存在。

### 建议优先建设

1. `br-spec init / plan / run / verify / report`
2. OpenSpec View
3. Task DAG
4. worktree 隔离
5. Hook + Test Gate
6. Evidence
7. Resume

### 建议暂缓建设

1. 完整 Hub 审核流
2. 完整 Visual 大屏
3. 复杂 RBAC
4. 多租户
5. Agent 市场
6. 自动上线
7. 全技术栈覆盖
8. 多模型复杂调度

路线图中其实也建议第一阶段不要追求平台完整，而要先跑通真实中台金融系统需求闭环，这一点非常正确。

---

# 五、风险清单

| 风险编号 | 风险类型    | 风险描述                                       | 严重程度 | 发生概率 | 影响范围        | 建议措施                           |
| ---- | ------- | ------------------------------------------ | ---- | ---- | ----------- | ------------------------------ |
| R-01 | 架构风险    | V0.1 范围过大，三仓、本地控制、Visual、Hub、Evidence 同时推进 | 高    | 高    | 交付周期、质量     | V0.1 收敛为 br-ai-spec 本地闭环       |
| R-02 | 工程风险    | `br-ai-spec` 职责过重，容易形成巨型 CLI               | 高    | 中    | 长期维护        | 拆为 core + plugins + adapters   |
| R-03 | 开发者体验风险 | 概念过多，普通业务开发者学习成本高                          | 高    | 高    | 推广 adoption | 提供极简命令路径和模板                    |
| R-04 | 稳定性风险   | Task DAG 自动生成不准会导致执行偏离                     | 高    | 中    | 代码质量        | DAG 支持人工确认和编辑                  |
| R-05 | 工程风险    | lockKeys 难以自动覆盖真实业务冲突                      | 中高   | 高    | 并行执行        | 默认保守并行，高风险资源不并行                |
| R-06 | 安全风险    | 缺少完整 RBAC、Prompt 注入防护、工具沙箱                 | 高    | 中    | 企业合规        | V0.2 前补安全基线                    |
| R-07 | 模型风险    | 缺少 Model Gateway，未来多模型治理不足                 | 中高   | 高    | AI 演进能力     | 增加 LLM Gateway / Model Adapter |
| R-08 | 业务风险    | L2 强制完整 OpenSpec 可能被业务团队认为过重               | 中    | 高    | 接入意愿        | L2 分为 L2-lite 和 L2-full        |
| R-09 | 运维风险    | worktree 清理、分支管理、patch 合并复杂                | 中高   | 中    | 本地环境        | 提供状态索引、保护锁、dry-run clean       |
| R-10 | 数据风险    | Evidence 可能包含敏感日志、截图、配置                    | 高    | 中    | 安全合规        | Evidence 脱敏、分类、保留策略            |
| R-11 | 成本风险    | 多 Agent + 多轮修复 + 多测试导致模型和时间成本高             | 中    | 高    | 研发效率        | 分级启用多 Agent，控制预算               |
| R-12 | 未来演进风险  | 过多私有协议可能限制接入 MCP、CI/CD、研发效能平台              | 中    | 中    | 平台扩展        | 协议尽量标准化，开放 Schema              |

---

# 六、评分表

| 评审维度       |  分数 | 评价                                          |
| ---------- | --: | ------------------------------------------- |
| 整体架构合理性    | 7.5 | 大方向正确，三仓边界清晰，但 V0.1 偏重                      |
| 目标清晰度      | 8.0 | 闭环目标明确，可验证，但范围需要收敛                          |
| 企业级成熟度     | 6.8 | 有企业级治理意识，但安全、权限、审计还不完整                      |
| AI 未来演进适配性 | 6.5 | IDE 适配较好，模型网关和模型治理不足                        |
| 开发者上手难度    | 5.8 | 对平台团队友好，对普通业务开发者偏复杂                         |
| 业务项目入侵性    | 7.5 | 源码侵入低，流程侵入中等偏高                              |
| 系统可靠性      | 6.7 | 有 checkpoint、Evidence、Gate，但缺超时、重试、幂等、状态机细节 |
| 安全与权限治理    | 5.6 | Guard 有雏形，但 RBAC、多租户、Prompt 安全不足            |
| 可维护性       | 6.4 | 模块拆分清晰，但实现面大，CLI 容易膨胀                       |
| 扩展性        | 7.2 | 资产化和插件化方向好，但标准协议兼容不足                        |
| 成本可控性      | 6.2 | 长期 ROI 有潜力，短期投入偏大                           |
| 落地可行性      | 7.0 | 若收敛 MVP 可落地，若全量推进风险较高                       |

**总体评分：7.1 / 10**

---

# 七、是否建议通过

## 结论：有条件通过

### 通过的部分

可以通过以下方向：

* 企业级 AI 研发控制平面的产品定位。
* `br-ai-spec` 本地控制器作为核心。
* OpenSpec 作为需求事实源。
* Context Pack + 渐进式资产披露。
* Task DAG + worktree 隔离。
* Hook + Test Gate。
* Evidence 证据落盘。
* Visual 作为后续观测中心。

### 不建议直接通过的部分

不建议 V0.1 直接全量建设：

* 完整三仓平台化。
* 完整 Hub 审核发布流。
* 完整 Visual 大屏。
* 复杂多 Agent 角色体系。
* 复杂 RBAC / 多租户。
* 多模型治理。
* Agent 市场 / 资源中心。
* 自动上线。

### 通过条件

1. V0.1 明确只交付 **br-ai-spec 本地闭环**。
2. Hub V0.1 只支持本地资产文件或最小 Bundle API。
3. Visual V0.1 只做 JSON mock 或最小 Run Event 接收。
4. Task DAG 必须支持人工确认和编辑。
5. 补充 Run 状态机、错误码、重试、超时、幂等、恢复机制。
6. 补充安全最小基线：Secret 脱敏、命令白名单、工具权限、Evidence 脱敏。
7. 提供普通开发者 30 分钟内可完成的接入路径。

---

# 八、修改建议优先级

## P0：必须修改，否则不建议进入开发

1. **收敛 V0.1 范围**
   V0.1 只做本地闭环：`init / plan / run / verify / report / resume / clean / worktree`，Hub 和 Visual 降级为 mock 或最小接口。

2. **补 Run 状态机和异常恢复协议**
   明确 Run、Task、Patch、Evidence 的状态、失败原因、重试策略、恢复策略。

3. **Task DAG 支持人工确认和编辑**
   不允许 AI 自动生成 DAG 后直接执行。尤其金融中台场景，API、DB、MQ、权限、缓存相关任务必须人工确认。

4. **补安全基线**
   包括 Secret Guard 具体规则、命令执行白名单、敏感 Evidence 脱敏、工具调用权限、L3 人工审批。

5. **简化开发者路径**
   必须把普通用户路径压缩为 5 个命令，并提供样板项目模板。

## P1：重要优化，建议 V0.1 后半段或 V0.2 完成

1. 把 `br-ai-spec` 拆成 core / plugin / adapter。
2. 定义 Asset Bundle Schema。
3. 定义 Evidence Schema 版本兼容策略。
4. Visual 上报异步化、本地缓存化。
5. 增加 `br-spec doctor` 检查项目环境、Git、Node、Maven、测试脚本。
6. 支持 Shadow Mode 和 Assist Mode。
7. 补充成本预算：每个 Run 的最大模型调用次数、最大修复次数、最大测试耗时。

## P2：后续平台化阶段再做

1. 完整 Hub 审核流。
2. 完整 Visual 分析面板。
3. 多租户。
4. 复杂 RBAC。
5. 多模型路由和模型市场。
6. Agent Hub。
7. 自动上线。
8. 跨技术栈全覆盖。

---

# 九、推荐优化后的架构方向

## 1. 推荐系统定位

建议把当前方案定位调整为：

> **面向企业研发流程的 AI 执行控制平面，先解决 AI 编码从需求到交付的可控、可验证、可恢复、可审计问题，再逐步扩展为企业 AI 研发资产治理平台。**

不要一开始就定位成完整 Agent 平台、工作流平台、低代码平台或多模型平台。

## 2. 推荐架构分层

```text
接入层
- CLI
- IDE Adapter
- CI Adapter
- Webhook

控制编排层
- Requirement Classifier
- OpenSpec Manager
- Task DAG Planner
- Run State Machine
- Policy Engine

执行隔离层
- Worktree Manager
- Executor Adapter
- Patch Bundle Manager
- Merge Manager

质量治理层
- Scope Guard
- Secret Guard
- Dangerous File Guard
- Test Gate
- Evidence Gate
- Approval Gate

资产与模型层
- Local Asset Bundle
- Hub Asset Sync
- Skill / Rule / Agent Profile
- Model Gateway
- Tool Registry

观测审计层
- Run Log
- Evidence Index
- Trace Event
- Visual Dashboard
- Audit Log
```

## 3. 推荐核心模块

V0.1 只保留：

* CLI
* OpenSpec Manager
* Context Pack Builder
* Task DAG Planner
* Worktree Manager
* Executor Adapter
* Hook Runner
* Test Gate Runner
* Evidence Writer
* Resume Manager
* Local Visual Mock

## 4. 推荐能力边界

`br-ai-spec` 不应该做：

* 用户组织管理
* 完整 RBAC
* 资产市场
* 模型供应商管理
* 大屏分析
* 自动上线
* 生产数据库执行

`br-ai-spec` 应该专注：

* 本地协议目录
* 本地任务编排
* 本地执行隔离
* 本地质量门禁
* 本地证据落盘
* 本地恢复与报告

## 5. 推荐接入方式

按侵入程度分层：

| 接入方式               | 能力                            | 适用对象  |
| ------------------ | ----------------------------- | ----- |
| Shadow Mode        | 只分析，不改代码                      | 初次试点  |
| Assist Mode        | 生成 OpenSpec、DAG、Patch 建议      | 谨慎团队  |
| Controlled Execute | worktree 执行 + Gate + Evidence | 成熟团队  |
| CI Integrated      | 接入 CI/CD 和审批                  | 企业级推广 |

## 6. 推荐开发者使用路径

普通开发者：

```bash
br-spec init
br-spec plan "需求描述"
br-spec run --mode assist
br-spec verify
br-spec report
```

平台开发者：

```bash
br-spec sync
br-spec plan --level L2
br-spec run --mode controlled
br-spec resume <runId>
br-spec worktree list
br-spec report --archive
```

## 7. 推荐权限与门禁审批设计

最小权限模型：

| 对象       | 权限                                   |
| -------- | ------------------------------------ |
| Project  | read / write / admin                 |
| Asset    | use / edit / publish                 |
| Run      | create / execute / approve / archive |
| Task     | execute / repair / merge             |
| Evidence | read / export / delete               |
| Tool     | invoke / approve                     |
| Model    | use / restricted-use                 |

高风险审批：

* L3 需求。
* 数据库 migration。
* 权限模型变更。
* MQ Consumer。
* Redis Key 变更。
* 涉及资金、授信、风控。
* 修改 CI/CD、部署脚本、环境配置。
* Secret 读取或疑似泄露。

## 8. 推荐可靠性设计

* Run 状态机。
* Task 状态机。
* Command Execution Record。
* Checkpoint。
* Retry Policy。
* Timeout Policy。
* Idempotency Key。
* Patch 校验。
* Evidence 校验。
* Visual 异步上报。
* 本地恢复命令。
* `doctor` 环境诊断命令。

## 9. 推荐可观测性设计

每个 Run 必须能回答：

* 谁发起？
* 需求是什么？
* 使用了哪些规范资产？
* 生成了哪些 Task？
* 哪个 Agent 执行了哪个 Task？
* 改了哪些文件？
* 是否越权？
* 跑了哪些测试？
* 哪些测试失败？
* 修复了几轮？
* 最终证据在哪里？
* 是否可恢复？
* 是否可复盘？

## 10. 推荐 AI 模型适配策略

新增 `model-gateway` 设计，但不要在 V0.1 完整实现。

抽象接口：

```text
ModelProvider
ModelProfile
PromptTemplate
ToolSchema
CostPolicy
FallbackPolicy
SafetyPolicy
AuditPolicy
```

短期先支持 IDE Adapter，长期再支持模型直连。

---

# 十、分阶段落地路线

## 阶段一：MVP 验证阶段

### 目标

跑通一个真实中台金融系统 L2 需求，从需求输入到 OpenSpec、Task DAG、worktree 执行、Test Gate、Evidence、Final Report 的本地闭环。

### 范围

只做 `br-ai-spec` 本地闭环。

### 必须建设能力

* `br-spec init`
* `br-spec plan`
* `br-spec run`
* `br-spec verify`
* `br-spec report`
* `br-spec resume`
* OpenSpec View
* Context Pack
* Task DAG
* worktree
* Patch Bundle
* Scope Guard
* Secret Guard
* Test Gate
* Evidence
* Final Report

### 不建议建设能力

* 完整 Hub
* 完整 Visual
* 完整 RBAC
* 多租户
* Agent 市场
* 自动上线
* 多模型治理

### 验收标准

* “新增产品配置管理模块”完整跑通。
* 至少 3 个 Task 可通过 worktree 隔离执行。
* 测试失败能进入最多 3 轮修复。
* 生成完整 `final-report.md` 和 `evidence-index.json`。
* 越权文件修改能被 Scope Guard 拦截。
* `.ai-spec-local/` 不入 Git。

---

## 阶段二：平台化建设阶段

### 目标

把本地闭环沉淀为团队可复用的平台能力。

### 范围

建设最小 `skill-q-platform` 和最小 `br-ai-spec-visual`。

### 核心能力

* Manifest 管理。
* Rule 管理。
* Skill 管理。
* Agent Profile 管理。
* Hook Spec 管理。
* Test Gate 管理。
* CLI 资产同步。
* Run Event 接收。
* Run 详情查看。
* Evidence 查看。

### 治理能力

* 资产版本锁定。
* 资产审核发布。
* 资产变更审计。
* 项目级规范包。
* 失败样本沉淀。

### 扩展能力

* IDE Adapter 模板。
* 多项目规范复用。
* 本地资产和远程 Hub 双模式。

---

## 阶段三：企业级规模化阶段

### 目标

支持多个项目、多个团队规模化接入。

### 范围

从样板项目扩展到 2-5 个真实业务项目。

### 稳定性

* Run 状态机成熟。
* Visual 可追踪失败。
* Evidence 可检索。
* Test Gate 可配置。
* Resume 可恢复。

### 安全性

* 企业 SSO。
* RBAC。
* 项目权限。
* 资产权限。
* 工具调用权限。
* 敏感数据脱敏。
* 审计日志。

### 多团队协作

* 团队规范包。
* 项目规范包。
* 资产继承。
* 资产灰度。
* 失败样本反哺。

### 成本治理

* Run 成本统计。
* 模型调用预算。
* 测试耗时统计。
* Agent 执行耗时统计。
* 修复轮次统计。

---

## 阶段四：AI 原生演进阶段

### 目标

从“AI IDE 控制平面”演进为“AI 原生研发控制平台”。

### 范围

引入多模型、多工具、多 Agent、多 Workflow、多模态、多项目智能运维。

### 多模型

* Model Gateway。
* 模型路由。
* 模型 fallback。
* 模型灰度。
* 成本控制。
* 模型输出审计。

### Agent

* Agent Profile 版本化。
* Agent 权限。
* Agent 评估。
* Agent 执行质量统计。
* Agent 与 Skill 解耦。

### Workflow

* 支持可视化 Task DAG 编辑。
* 支持人工审批节点。
* 支持 CI/CD 节点。
* 支持测试平台节点。
* 支持安全扫描节点。

### MCP / Tool

* Tool Registry。
* MCP Tool 接入。
* Tool 权限。
* Tool 调用审计。
* Tool 沙箱。

### 自动化研发

* 自动生成变更方案。
* 自动补测试。
* 自动生成回滚方案。
* 自动复盘失败 Run。
* 自动推荐 Rule / Skill 优化。

### 智能运维

* Run 异常分析。
* 失败模式聚类。
* 质量趋势。
* 成本趋势。
* 团队 AI 研发效能报告。

---

# 最终建议

这套方案最值得保留的 5 个设计：

1. **企业级 AI 研发控制平面定位。**
2. **OpenSpec + Context Pack + 渐进式披露。**
3. **Task DAG + writeSet + lockKeys。**
4. **Git worktree 隔离执行。**
5. **Hook / Test Gate / Evidence 闭环。**

当前最应该优先修改的 5 个问题：

1. **V0.1 范围过大，必须收敛。**
2. **补 Run / Task 状态机、异常恢复、幂等和超时。**
3. **补安全最小基线。**
4. **降低普通开发者上手成本。**
5. **增加未来 Model Gateway 的架构预留。**

一句话评审结论：

> **架构方向值得做，但 V0.1 必须从“完整平台方案”收敛为“本地控制闭环验证”。先跑通一个真实需求，再平台化；先证明 AI 能按企业流程稳定交付，再谈多团队、多模型、多租户和资产市场。**
