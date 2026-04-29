# Enterprise AI Control Plane V0.1 企业级架构评审报告

> 评审版本：V0.1 Review Pack  
> 评审日期：2026-04-28  
> 评审依据：PRD、Architecture、Code Design、Three-Repo Plan、Sample Flow、Roadmap、Glossary、Checklist  
> 评审立场：架构委员会 + CTO 视角，兼顾 研发负责人、平台工程师、业务开发者、运维人员视角

---

# 一、评审结论摘要

**整体判断：有条件通过。**

该方案整体方向正确，核心思路——"将 AI IDE 升级为可控、可验证、可审计的企业级研发执行体系"——具备实际价值，技术路线也有一定合理性。Task DAG + Git worktree 隔离 + Test Gate + Evidence 落盘的组合设计，体现了对企业级交付质量的认真思考。

但当前方案存在**四个根本性问题**，若不在进入开发前解决，极有可能导致 V0.1 无法落地或落地后迅速成为技术债：

1. **V0.1 范围严重过大**，三仓同步推进、概念体系过重，4-6 周内无法跑通真实闭环。
2. **没有 AI 模型抽象层**，整套方案依赖 AI 模型的稳定输出，却对"用哪个模型、如何切换、如何降级、成本如何控制"完全没有设计，是核心架构盲区。
3. **开发者上手成本极高**，引入了 20+ 个新概念，缺乏最小接入路径，极有可能让业务团队望而却步。
4. **br-ai-spec 职责过重**，单仓承担了 CLI、上下文管理、多 Agent 调度、worktree 管理、测试执行、证据落盘、Visual 上报等几乎全部核心逻辑，是典型的上帝模块风险。

建议：**缩小 V0.1 范围至 br-ai-spec 本地单仓闭环，补充 AI 模型抽象层设计，删减 V0.1 中不必要的 Multi-Agent 和三仓联调内容，先跑通一个真实样板需求再扩展。**

---

# 二、关键优点

以下设计值得保留，体现了团队的工程严谨性：

1. **Task DAG 并行安全机制**（writeSet + lockKeys + dependsOn）：从文件粒度和逻辑锁双维度控制并行安全，思路正确，是该方案最核心的工程价值。
2. **Git worktree 执行隔离**：用 Git 原生能力实现多 Agent 并行隔离，避免使用复杂的沙箱或容器方案，成本低、可追溯。
3. **任务等级分层（L1/L2/L3）**：按需启用完整流程，避免轻量任务被复杂流程拖慢，体现了渐进式设计意识。
4. **Evidence 证据落盘体系**：测试结果、验收清单、交付报告的结构化落盘，是企业级合规审计的有效支撑，也是差异化能力。
5. **OpenSpec 作为需求规格事实源**：将需求、设计、任务清单统一在 openspec/ 目录，建立了 AI 执行的"事实依据"，降低幻觉风险。
6. **渐进式上下文加载（Progressive Disclosure）**：分阶段加载规范资产和上下文，避免长上下文膨胀，是解决 LLM 上下文问题的务实方案。
7. **Repair Agent 的最大轮次限制**：自修复最多 3 轮，超出则停止并上报，避免无限循环，是合理的安全设计。
8. **业务项目最小侵入原则**：仅新增 openspec/、.ai-spec/、.ai-spec-local/ 三个顶层目录，不改动业务源码，原则上正确。
9. **样板需求完整链路设计**：中台金融系统"产品配置管理模块"的端到端样例文档，为验收提供了清晰的 benchmark。
10. **错误码体系设计**：明确定义了 E_SCOPE_VIOLATION、E_REPAIR_LIMIT_EXCEEDED 等错误码，有助于可观测性建设。

---

# 三、关键问题

当前方案最严重的问题，按严重程度排序：

**P0 级（必须解决，否则方案不可落地）：**

1. **没有 AI 模型抽象层**：整套方案依赖 LLM 执行，但架构文档中对"用哪个模型、如何配置、如何切换、API Key 如何管理、调用成本如何控制、模型失败如何 fallback"完全缺失。这是最大的架构盲区。
2. **V0.1 范围过大**：三仓同时改造（br-ai-spec + skill-q-platform + br-ai-spec-visual）+ 复杂 Multi-Agent 调度 + Git worktree + 完整 Hook/Test/Evidence 体系，4-6 周内不可能全部验证，极有可能导致"整体跑不通，部分又不能用"的烂尾风险。
3. **Task DAG 生成质量无保证机制**：Task DAG 由 AI 自动生成，但没有任何机制保证生成质量（格式校验、语义校验、依赖合理性校验）。一旦 Task DAG 生成错误，整个执行链路将崩溃。
4. **br-ai-spec 职责过重**：单仓承担 CLI 框架、项目扫描、OpenSpec 构建、Context Pack、Task DAG 规划、调度器、worktree 管理、Merge Agent、Hook 引擎、Test Gate 执行、Evidence 生成、Visual 上报等 15+ 个核心模块，是典型的上帝模块，长期维护成本极高。

**P1 级（重要问题，进入 V0.2 前必须解决）：**

5. **概念体系过重**：开发者需要理解 OpenSpec、Manifest、Rule、Skill、Agent Profile、Hook Spec、Test Gate、Context Policy、Evidence Policy、Task DAG、writeSet、readSet、lockKeys、Executor Pool、worktree、Patch Bundle、Change Branch、Task Branch、Merge Agent、Repair Agent、Docs Agent、run.bundle.json、run.log.jsonl 等 20+ 个新概念，上手曲线极陡。
6. **IDE Adapter 层设计不足**：方案中多处提到"通过 IDE Adapter 下发任务上下文"，但对 Cursor / Claude Code / Codex 的适配机制几乎没有细化，这是执行链路的核心环节却是黑盒。
7. **安全设计不完整**：Agent 调用 LLM 时的 API Key 管理、Context Pack 中的敏感信息防护、Visual 上报的认证机制、三仓间通信的安全性，均缺乏具体设计。
8. **多 Agent 成本估算缺失**：L2/L3 启用完整多 Agent（10 个 Agent 角色），但没有任何 API 调用成本估算，对于金融企业而言，成本不可控是接入的重大障碍。

---

# 四、分维度详细评审

## 4.1 整体架构合理性

### 优点

- 三仓职责划分（控制器/资产治理/运行观测）的宏观分层是合理的，体现了关注点分离。
- "Graph-Governed Multi-Agent"的核心设计思路（Graph 管流程、Agent 管专业判断、Executor 管实际修改、Hook 管强约束、Test 管真实性）层次清晰。
- 分层架构已初步具备：接入层（CLI）、编排层（Task DAG/Scheduler）、执行层（Executor Pool/worktree）、观测层（Visual）、治理层（Hub/Hook）。

### 风险与不合理之处

- **缺少 AI 模型层**：在整个分层架构中，没有一个独立的"模型适配层"，LLM 调用散落在各个 Agent 的实现中，导致模型切换成本极高。
- **br-ai-spec 是上帝模块**：15+ 个子模块全部集中在同一仓库，违反了高内聚低耦合原则。建议拆分出独立的执行引擎和调度引擎。
- **三仓耦合度比预期高**：尽管逻辑上分离，但 br-ai-spec 同步依赖 skill-q-platform（资产包），上报依赖 br-ai-spec-visual，在网络不稳定或服务不可用时，本地执行能否降级是不确定的。

### 可优化建议

- 显式增加 **AI Model Gateway 层**，统一管理模型调用、路由、成本、限流、fallback。
- 将 br-ai-spec 中的调度器（Scheduler/ExecutorPool）提取为独立的 **Agent Runtime**，与 CLI 解耦。
- 在三仓设计中明确 **离线模式**：当 Hub 不可用时，br-ai-spec 能以本地资产文件运行；当 Visual 不可用时，能以本地日志代替上报。

### 推荐目标架构方向

```
CLI 接入层
  └── OpenSpec Builder / Context Pack / Task DAG Planner
AI Model Gateway（新增）
  └── 模型路由 / fallback / 成本控制 / 审计
Agent Runtime（从 br-ai-spec 拆出）
  └── Orchestrator / Expert Agents / Executor / Repair
Git Execution Layer
  └── worktree 管理 / Merge / Patch Bundle
质量验证层
  └── Hook / Test Gate / Evidence
治理层（skill-q-platform）
  └── 资产管理 / 版本 / 审核 / 分发
观测层（br-ai-spec-visual）
  └── Run 状态 / 链路追踪 / 指标
```

---

## 4.2 目标设计合理性

### 目标合理性判断

V0.1 核心目标"让一个中台金融系统 L2 需求从输入到完整交付证据全程跑通"是**合理且有价值的**，这是正确的 MVP 思路。

但 V0.1 的**实现范围**已远超这个目标，实际包含了：
- 三仓同步建设
- 完整多 Agent 体系（10 个 Agent 角色）
- Git worktree 隔离执行
- 完整 Hook/Test/Evidence
- Visual 上报
- Hub 资产治理（最小版）

一个 4-6 周的 V0.1 sprint 要验证以上所有内容，**不现实**。

### 目标优先级建议

| 目标 | 建议 |
|---|---|
| 本地控制器单仓闭环 | 保留，核心目标 |
| OpenSpec + Task DAG | 保留，核心机制 |
| Git worktree 并行执行 | 保留，核心差异化 |
| Test Gate + Evidence | 保留，核心价值 |
| Multi-Agent（10个角色） | 降低优先级，V0.1 可用 2-3 个核心角色 |
| Visual 实时观测 | 降低优先级，V0.1 用本地文件/日志代替 |
| Hub 资产治理 | 暂缓，V0.1 用本地文件模拟 |
| 三仓联调 | 暂缓，先跑通 br-ai-spec 单仓 |

### 需要补充量化指标的目标

- "证据落盘完整率 100%"：需明确哪些证据是强制的，哪些是可选的
- "自修复轮次最多 3 轮"：需明确修复成功率目标（例如：L2 需求 3 轮内修复成功率 ≥ 70%）
- "越权文件修改拦截 100%"：需明确测试场景覆盖率
- 缺少**模型调用成本**目标（例如：完成一个 L2 需求的总 Token 消耗不超过 X）

---

## 4.3 面向未来 AI 大模型快速发展的适应性

**评分：4/10（当前最大架构盲区）**

### 核心问题

整个方案的所有 Agent 实现、Context Pack 构建、Task DAG 生成、自修复逻辑，都强依赖 LLM 调用，但：

1. **没有任何模型抽象层**：哪个 Agent 调用哪个模型、用什么 Prompt、如何切换模型，文档中完全没有设计。
2. **没有多模型路由**：假设某个 Agent 用 Claude，另一个用 Qwen，当前架构无法支持。
3. **没有 fallback 策略**：模型调用失败时，整个 Task 如何处理？是重试、降级、还是人工介入？
4. **没有成本控制**：10 个 Agent 角色 + 多轮对话 + 长上下文，一个 L2 需求的 API 调用成本可能是数十到数百美元，金融企业无法接受无成本管控的系统。
5. **没有 Prompt 版本管理**：Skill 中包含 Prompt，但 Prompt 的版本化、回滚、A/B 测试完全没有设计。
6. **没有输出安全审查**：LLM 输出的代码直接写入业务项目，没有内容安全审查层。

### 哪些模块应该保持灵活

- Executor Agent 的模型选择（不同任务类型用不同模型）
- Context Pack 的 Token 预算（随模型上下文窗口能力调整）
- Task DAG 生成器（未来模型能力提升后可大幅简化）

### 哪些设计可能在未来 6-12 个月内过时

- **手工 writeSet/lockKeys 定义**：随着代码理解能力提升，模型可直接推断冲突，不需要手工声明
- **严格的 Multi-Agent 分工**：当模型能力足够强时，Orchestrator + 单个 Executor 即可，无需 10 个专家 Agent
- **分阶段的 Context Pack 压缩**：长上下文模型（200K+ token）可减少手工压缩的必要性

### 推荐的 AI 原生架构演进方向

```
Model Registry（新增）
  ├── 注册支持的模型：Claude, GPT-4o, Qwen, DeepSeek, Gemini, Local
  ├── 模型能力标签：code-gen, review, test-gen, doc-gen
  ├── 路由策略：任务类型 → 模型
  ├── fallback 链：主模型失败 → 备用模型
  └── 成本限额：per-run / per-task / per-agent

Prompt Registry（新增）
  ├── Prompt 版本化存储
  ├── 与 Skill 绑定
  ├── A/B 测试支持
  └── 效果评估指标
```

---

## 4.4 开发者上手难度

**评分：3/10（当前最大落地风险之一）**

### 新概念数量统计

从文档中统计，开发者需要理解和使用的新概念达到 **24 个**：

OpenSpec、proposal.md、design.md、tasks.md、spec delta、Manifest、Rule、Skill、Agent Profile、Hook Spec、Test Gate、Context Policy、Evidence Policy、Task DAG、writeSet、readSet、lockKeys、acceptanceRefs、Executor Pool、Git worktree、Patch Bundle、Change Branch、Task Branch、run.bundle.json、evidence-index.json、L1/L2/L3 分级

对于一个普通全栈工程师而言，这个学习曲线约等于"学一门新语言 + 一套新框架"。

### 当前方案对新人的学习成本判断

- **理解概念体系**：预计 2-3 天
- **完成第一个 L1 任务**：预计 1-2 天
- **完成第一个 L2 任务（含 OpenSpec + Task DAG + worktree）**：预计 3-5 天
- **排查一次失败任务**：预计 0.5-1 天（需要理解 run.log.jsonl、evidence-index、worktree 状态）

以上成本对于"日常提效工具"而言太高，**大多数开发者会在理解 OpenSpec + Task DAG 之前放弃**。

### 哪些概念可以合并或简化

| 可简化方向 | 建议 |
|---|---|
| proposal.md + design.md + tasks.md | 合并为单个 change.md，分 section |
| Manifest + Rule + Skill + Agent Profile | 统一为 Spec Pack，按模块区分 |
| writeSet + lockKeys | 前期可合并，由工具自动推断 lockKeys |
| Change Branch + Task Branch + worktree | 对用户屏蔽，只暴露 `br-spec run` 即可 |
| run.bundle.json + run.log.jsonl + evidence-index.json | 用统一的 run-state 概念对用户呈现 |

### 推荐的最小接入路径

```bash
# 第一步：初始化（10 分钟）
br-spec init

# 第二步：描述需求，自动生成计划（5 分钟）
br-spec plan "新增产品配置管理模块"

# 第三步：执行（无需手动操作）
br-spec run

# 第四步：查看报告
br-spec report
```

用户不应该需要手动编写 OpenSpec、手动定义 Task DAG、手动创建 worktree。这些应该是系统自动完成的，只在需要时提供确认和编辑入口。

---

## 4.5 对业务项目的入侵性

**评分：6/10（相对较好，但仍有改进空间）**

### 当前方案的侵入分析

**低侵入（正面）：**
- 只新增 3 个顶层目录，不改动业务源码
- .ai-spec-local/ 不入 Git
- 不强制修改 package.json / pom.xml
- worktree 放在项目外部（~/.br-spec/worktrees/）

**中等侵入（需注意）：**
- `openspec/` 放在项目根目录并入 Git：对于大型单仓项目，这会让非 AI 开发者感到困惑；对于已有完善文档体系的团队，可能与现有文档目录冲突。
- `.ai-spec/` 入 Git：意味着团队成员都需要理解这个目录的用途，否则会被随意修改或删除。
- 每次 `br-spec run` 都会创建 Git 分支和 worktree：对于有严格 Git 分支管理策略的团队，这可能与现有 GitFlow/TrunkBased 策略冲突。

**潜在高侵入风险：**
- **Git 历史污染**：自动创建的 `ai/change/*` 和 `ai/task/*` 分支，如果不及时清理，会让 Git 历史混乱。需要明确分支清理策略。
- **未来难以脱离平台**：一旦 OpenSpec 和 .ai-spec/ 积累了大量历史记录，业务项目会对平台形成路径依赖。

### 推荐的低侵入接入方式

建议支持以下三种接入梯度：

```
梯度 1（零侵入）：纯 CLI 模式
  - br-spec 读取现有代码目录
  - 不在业务项目中创建任何目录
  - 输出结果写入用户指定的外部目录

梯度 2（轻侵入）：当前方案
  - 新增 openspec/ + .ai-spec/ + .ai-spec-local/
  - 适合中长期深度使用

梯度 3（深度集成）：未来版本
  - 与 CI/CD 集成
  - 与代码审查平台集成
  - 与项目管理工具集成
```

---

## 4.6 系统可靠性与稳定性

**评分：5/10**

### 已有的可靠性设计（正面）

- Repair Agent 最多 3 轮限制
- 断点续跑（`br-spec resume`）
- run.log.jsonl 事件日志
- Scope Guard / Evidence Gate 等 Hook
- worktree 隔离（失败任务不污染主分支）

### 缺失的可靠性设计

| 缺失项 | 风险描述 |
|---|---|
| LLM 调用失败处理 | 模型超时/API 限流/网络中断时，Task 如何处理？ |
| Merge 冲突处理 | cherry-pick 失败时的处理策略不完整（只提到"兜底用 git apply"） |
| worktree 孤儿清理 | 进程崩溃时，worktree 残留如何发现和清理？ |
| 并发安全 | 多个 `br-spec run` 并发执行同一个项目时，lockKeys 是否能跨进程有效？ |
| Task DAG 循环依赖 | dependsOn 中若存在循环依赖，调度器是否能检测并报错？ |
| Git 仓库状态保护 | 执行前未检查 Git 工作区是否干净（E_GIT_DIRTY 只定义了错误码，未说明处理流程） |
| 长任务超时 | 单个 Task 执行多长时间后强制终止？有无超时配置？ |
| Visual 不可用降级 | Visual 服务不可用时，是否会阻塞本地执行？ |

### 推荐的可观测性方案

```
本地可观测（V0.1 必须）：
  - run.log.jsonl：结构化事件日志（已有）
  - console 输出：实时进度（已有）
  - final-report.md：执行摘要（已有）

平台可观测（V0.3 目标）：
  - OpenTelemetry 链路追踪：跨 Task/Agent/LLM 调用的完整链路
  - Prometheus 指标：任务成功率、修复率、平均执行时长
  - 告警：测试失败率超阈值、修复失败、长时间未完成
```

---

## 4.7 安全性、权限与治理能力

**安全治理成熟度评分：4/10**

### 当前已有设计

- Secret Guard：禁止读取或输出敏感配置
- Dangerous File Guard：禁止删除高风险文件
- Agent 不能访问生产环境（PRD 中提及，但无实现细节）
- Visual 只上传元数据，不上传业务源码

### 关键安全盲区

| 安全问题 | 严重程度 |
|---|---|
| **LLM API Key 管理**：Executor Agent 调用 LLM 时，API Key 如何存储、如何注入、如何防泄漏？ | 高 |
| **Prompt 注入攻击**：业务代码中的注释或字符串可能包含恶意 Prompt，影响 LLM 输出行为 | 高 |
| **LLM 输出代码安全审查**：LLM 生成的代码可能包含漏洞（SQL 注入、XSS、硬编码密钥等），没有安全扫描环节 | 高 |
| **三仓间通信认证**：br-ai-spec → skill-q-platform 和 br-ai-spec → Visual 的认证机制缺失 | 中 |
| **Context Pack 敏感信息**：run.bundle.json 中可能包含业务逻辑、API 结构、数据库设计等敏感信息，其存储和传输安全性未说明 | 中 |
| **Git worktree 权限**：worktree 创建在用户 Home 目录（~/.br-spec/），多用户环境下的文件权限隔离未设计 | 中 |
| **门禁审批缺失**：L3 高风险需求提到"需要人工确认 Gate"，但人工确认机制（由谁确认、在哪确认、如何记录）完全没有设计 | 中 |

### 必须补充的治理能力

1. **API Key 安全存储方案**（OS Keychain / 环境变量 / 密钥服务集成）
2. **LLM 输出代码安全扫描**（集成 Semgrep 或类似静态分析工具作为 Test Gate）
3. **L3 人工确认 Gate 的具体实现方案**
4. **Context Pack 中的敏感字段脱敏策略**

---

## 4.8 可维护性与工程复杂度

**可维护性评分：5/10**

### 技术债风险点

1. **br-ai-spec 模块过多**：当前设计有 15+ 个顶层模块（cli、config、project-scanner、openspec、context、assets、agents、task-dag、scheduler、worktree、patch、merge、hooks、test-gates、evidence、visual-client、resume、shared），一旦出现跨模块问题（如 Context Pack 影响 Task DAG 影响 Executor），调试难度极高。
2. **隐式状态过多**：run.bundle.json 承载了 Run 的全局状态，所有模块都读写这个文件，容易出现状态不一致。建议引入状态机设计，明确每个状态的合法转换。
3. **LLM 输出不确定性**：Task DAG 由 LLM 生成，Context Pack 由 LLM 处理，这意味着核心流程存在不确定性，难以编写稳定的单元测试和集成测试。
4. **worktree 生命周期管理**：worktree 创建/使用/清理的生命周期横跨多个模块，容易出现遗漏清理的孤儿 worktree。

### 哪些地方容易成为技术债

- `buildTaskDag.ts`：LLM 生成 + 校验逻辑混杂，未来很难替换生成策略
- `compressContext.ts`：上下文压缩的触发条件和压缩策略难以测试
- `mergePatchBundle.ts`：三种合并策略（cherry-pick / merge / apply）的选择逻辑容易出错

### 推荐的工程治理方案

- 引入**状态机**管理 Run 生命周期（planned → running → verifying → completed/failed）
- 将 LLM 调用全部封装在独立的 `llm-client/` 模块，所有业务逻辑不直接调用 LLM API
- 对 Task DAG 生成结果强制 JSON Schema 校验，并要求 LLM 在失败时提供可解析的错误说明

---

## 4.9 扩展性与复用性

**扩展性评分：7/10 | 复用性评分：6/10**

### 当前扩展性优点

- Manifest + Rule + Skill + Agent Profile 的资产体系，为跨项目复用提供了良好基础
- Hook Spec 和 Test Gate 的插件化设计，允许按项目定制门禁规则
- L1/L2/L3 分级允许不同复杂度的需求使用不同深度的流程

### 扩展性不足之处

- **多技术栈支持**：当前 project-scanner 只支持 Vue + Spring Boot 组合，扩展到 React/Next.js、Django/FastAPI、Go 等技术栈需要大量额外工作
- **多 IDE 支持**：IDE Adapter 层没有明确的插件接口定义，不同 IDE 的适配成本不透明
- **多租户支持**：当前设计是单用户本地工具，未来支持多团队共用时，需要完整的租户隔离设计

### 推荐的插件化设计

```typescript
// 建议定义 Plugin 接口
interface BrSpecPlugin {
  name: string;
  version: string;
  hooks?: HookPlugin[];
  testGates?: TestGatePlugin[];
  agents?: AgentPlugin[];
  stackDetectors?: StackDetectorPlugin[];
}
```

---

## 4.10 成本与投入产出比

### 成本风险判断

| 成本类型 | 风险等级 | 说明 |
|---|---|---|
| 平台研发成本 | 高 | 三仓同步建设 + 复杂 Multi-Agent，估计需要 3-5 名工程师 3-6 个月 |
| LLM API 调用成本 | 高 | 一个 L2 需求涉及 10 个 Agent 角色 + 多轮对话，估计单次成本 $5-$50 |
| 业务团队接入成本 | 中 | 学习曲线陡峭，首次接入预计 2-5 天 |
| 运维成本 | 中 | 三个服务需要独立部署和维护 |
| Git 历史管理成本 | 低 | 大量 ai/change 和 ai/task 分支需要定期清理 |

### 建议优先建设的能力

1. br-spec init / plan / run（本地闭环核心）
2. Task DAG 生成与校验
3. Git worktree 管理
4. Test Gate + Evidence（最直接的价值证明）

### 建议暂缓建设的能力

1. skill-q-platform 完整资产治理（V0.1 用本地文件模拟）
2. br-ai-spec-visual 实时观测（V0.1 用本地报告代替）
3. 完整 10 角色 Multi-Agent（V0.1 用 3 个核心角色）
4. IDE Adapter 多 IDE 支持（V0.1 只支持 Claude Code 或 Cursor 之一）

### MVP 建设范围建议

```
V0.1 MVP 范围（4-6 周）：
  - br-ai-spec 单仓本地闭环
  - 支持 1 种 AI IDE（Claude Code 优先）
  - 支持 1 种技术栈（Vue + Spring Boot）
  - 支持 L1 和 L2 任务（不做 L3）
  - Task DAG 支持 3-4 个并行 Task
  - Test Gate：lint + 单测（不做集成测试）
  - Evidence：evidence-index + final-report
  - 验收：样板需求跑通 + 至少 1 个真实需求跑通
```

---

# 五、风险清单

| 风险编号 | 风险类型 | 风险描述 | 严重程度 | 发生概率 | 影响范围 | 建议措施 |
|---|---|---|---|---|---|---|
| R-01 | 架构风险 | 没有 AI 模型抽象层，模型切换、成本控制、fallback 均无设计 | 严重 | 高 | 全局 | P0 优先补充 Model Gateway 设计 |
| R-02 | 工程风险 | br-ai-spec 上帝模块，15+ 子模块耦合严重 | 严重 | 高 | 长期维护 | 拆分 Agent Runtime 为独立模块 |
| R-03 | 业务风险 | V0.1 范围过大，4-6 周无法跑通三仓联调 | 严重 | 高 | 项目交付 | 立即缩小 V0.1 范围，聚焦 br-ai-spec 单仓 |
| R-04 | 开发者体验风险 | 20+ 新概念，业务团队上手成本极高，接入意愿低 | 高 | 高 | 推广落地 | 简化概念层，提供最小接入路径 |
| R-05 | 稳定性风险 | Task DAG 由 LLM 生成，质量不可控，生成失败可导致整个链路崩溃 | 高 | 中 | 核心流程 | 强制 JSON Schema 校验 + 人工确认 Gate |
| R-06 | 安全风险 | LLM API Key 管理缺失，存在密钥泄漏风险 | 高 | 中 | 生产安全 | P0 补充密钥安全管理方案 |
| R-07 | 安全风险 | Prompt 注入攻击，业务代码中恶意内容影响 LLM 行为 | 高 | 中 | 代码安全 | 增加 Prompt 输入净化和输出内容审查 |
| R-08 | 成本风险 | 多 Agent 并行调用 LLM，单次 L2 需求成本可能达 $10-$50 | 高 | 高 | 规模化推广 | 增加成本估算和限额控制 |
| R-09 | 模型风险 | 方案过度依赖当前模型能力，模型能力提升后部分设计（如复杂 Multi-Agent）将过时 | 中 | 高 | 架构演进 | 保持模型层可插拔，不硬编码 Agent 角色 |
| R-10 | 稳定性风险 | worktree 孤儿残留，进程崩溃或异常中断后 worktree 无法自动清理 | 中 | 中 | 本地资源 | 增加 worktree 健康检查和自动 prune 机制 |
| R-11 | 稳定性风险 | Merge 冲突处理策略不完整，cherry-pick 失败的兜底方案（git apply）可能导致更多冲突 | 中 | 中 | 代码质量 | 增加 Merge 冲突的结构化处理和人工介入机制 |
| R-12 | 架构风险 | Git worktree 在 Windows 上有兼容性问题，若需跨平台支持，需要额外验证 | 中 | 中 | 跨平台支持 | 明确平台支持矩阵，Windows 可降级为顺序执行 |
| R-13 | 数据风险 | .ai-spec-local/ 中的 run 数据无 retention policy，长期积累会占用大量磁盘 | 中 | 高 | 本地存储 | 明确 retention 策略，V0.1 就需支持 br-spec clean |
| R-14 | 运维风险 | 三仓各自部署，故障排查需要跨三个系统，运维成本高 | 中 | 中 | 运维效率 | V0.1 提供统一的本地诊断命令 |
| R-15 | 未来演进风险 | IDE Adapter 层设计不足，未来多 IDE 支持的改造成本不可预期 | 中 | 高 | 扩展性 | 在架构中明确 IDE Adapter 接口定义 |
| R-16 | 安全风险 | LLM 生成代码未经安全扫描直接进入业务代码，存在安全漏洞引入风险 | 中 | 中 | 代码安全 | 在 Test Gate 中集成静态安全分析（如 Semgrep） |
| R-17 | 工程风险 | 锁冲突判断（lockKeys）当前仅用字符串匹配，对于复杂依赖关系（如同一个 Vuex 模块的不同 mutation）可能漏判 | 低 | 中 | 并行正确性 | V0.2 升级为语义级冲突分析 |
| R-18 | 开发者体验风险 | 证据目录结构过于复杂（artifacts/ 下多个文件），开发者难以快速找到关键信息 | 低 | 高 | 使用体验 | 提供统一的 `br-spec status` 命令展示关键信息 |

---

# 六、评分表

| 评审维度 | 分数 | 评价 |
|---|---:|---|
| 整体架构合理性 | 6 | 分层思路正确，但 br-ai-spec 上帝模块 + 缺失模型层是核心问题 |
| 目标清晰度 | 6 | MVP 目标正确，但实现范围与目标不匹配，V0.1 范围过大 |
| 企业级成熟度 | 5 | 安全、权限、成本控制、多租户均有重大缺失 |
| AI 未来演进适配性 | 4 | 无模型抽象层，强依赖当前模型能力，是最大架构盲区 |
| 开发者上手难度 | 3 | 20+ 新概念，缺乏最小接入路径，上手门槛极高 |
| 业务项目入侵性 | 6 | 基本原则正确，但 openspec/ 入 Git + Git 分支策略有侵入风险 |
| 系统可靠性 | 5 | 有基础设计，但 LLM 调用失败处理、Merge 冲突、并发安全等有缺失 |
| 安全与权限治理 | 4 | API Key 管理、Prompt 注入、输出安全审查均缺失 |
| 可维护性 | 5 | 模块划分清晰但耦合度高，LLM 不确定性使测试困难 |
| 扩展性 | 7 | 资产体系和 Hook 插件化设计良好，多技术栈扩展有待验证 |
| 成本可控性 | 3 | 无 LLM 成本估算和控制机制，三仓建设成本过重 |
| 落地可行性 | 5 | 方向正确，但当前范围和成本下 4-6 周无法落地 |

**总体评分：5.2 / 10**

---

# 七、是否建议通过

## 结论：有条件通过

**不建议直接通过**，需要满足以下条件：

### 必须满足的条件（通过 P0 修改后再通过）

1. **补充 AI 模型抽象层设计文档**：明确模型注册、路由、fallback、成本控制、API Key 管理方案。
2. **将 V0.1 范围收缩至 br-ai-spec 单仓闭环**：删除三仓联调、V0.1 Hub 不做真实服务、Visual 用本地日志代替。
3. **补充 LLM API Key 安全管理方案**：具体到密钥存储位置、注入方式、轮换机制。
4. **简化开发者接入路径**：提供"4 步接入"最小接入路径设计，将所有内部概念对开发者屏蔽。
5. **明确 V0.1 成功验收标准**：细化到具体的测试场景（如：运行样板需求，从命令输入到 final-report 生成，成功率 ≥ 1 次）。

---

# 八、修改建议优先级

## P0（立即修改，进入开发前必须解决）

1. **新增 AI Model Gateway 设计**：定义模型抽象接口，支持 Claude / GPT / Qwen 接入，包含 fallback 和成本控制。
2. **缩小 V0.1 范围**：将 skill-q-platform 和 br-ai-spec-visual 降为 V0.1 可选/Mock，专注 br-ai-spec 本地闭环。
3. **API Key 安全方案**：明确 LLM API Key 的存储、注入和轮换机制（建议：OS Keychain + 环境变量 + .env.local 不入 Git）。
4. **定义最小接入路径**：设计面向业务开发者的 4 步接入文档，将底层机制（Task DAG、worktree、lockKeys 等）对用户透明。
5. **Task DAG 生成质量保证**：增加 JSON Schema 强制校验 + 人工确认 Gate 设计（不依赖 LLM 100% 准确）。

## P1（V0.1 Sprint 内解决）

6. **明确 LLM 调用失败处理**：定义模型调用超时、限流、网络失败的处理策略（重试 N 次 → fallback 模型 → 人工介入）。
7. **worktree 健康检查**：实现 `br-spec worktree status` 和孤儿清理机制。
8. **Git 分支命名策略**：明确 ai/change 和 ai/task 分支的保留期限和自动清理机制，避免 Git 历史污染。
9. **LLM 输出安全扫描**：在 Test Gate 中增加静态安全分析，至少扫描硬编码密钥和明显的 SQL 注入风险。
10. **IDE Adapter 接口定义**：明确 br-ai-spec 与 Cursor / Claude Code 的通信协议，而不是留作黑盒。

## P2（V0.2 前解决）

11. **开发者概念瘦身**：合并 proposal.md + design.md + tasks.md 为单文件；对外屏蔽 writeSet/lockKeys 等内部概念。
12. **Evidence 保留策略**：实现 `.ai-spec-local/` 的数据清理策略，支持 retention days 配置。
13. **并发安全设计**：明确 lockKeys 的跨进程有效性，避免多个 `br-spec run` 并发时的状态竞争。
14. **多 Agent 成本估算**：为每种任务等级（L1/L2/L3）提供参考成本范围，让业务团队做预算决策。
15. **Windows 兼容性方案**：明确 Git worktree 在 Windows 的支持情况，提供 Windows 降级方案（顺序执行模式）。

---

# 九、推荐优化后的架构方向

## 9.1 推荐系统定位

> 企业全栈项目 AI 研发执行引擎：以本地控制器为核心，通过规范资产驱动 AI IDE，将 AI 开发从"随机生成"升级为"按企业规范可控交付"。

## 9.2 推荐架构分层（优化版）

```
┌────────────────────────────────────────────────────────┐
│                  开发者接口层                           │
│  CLI (br-spec)  /  IDE Extension  /  API (未来)        │
├────────────────────────────────────────────────────────┤
│                  规划编排层                             │
│  OpenSpec Builder  /  Task DAG Planner  /  Scheduler   │
├────────────────────────────────────────────────────────┤
│              AI Model Gateway（新增）                   │
│  Model Registry  /  Router  /  Fallback  /  Cost Ctrl  │
├────────────────────────────────────────────────────────┤
│                  Agent Runtime（拆出）                  │
│  Orchestrator  /  Expert Agents  /  Executor  /  Repair │
├────────────────────────────────────────────────────────┤
│                  Git 执行层                             │
│  Worktree Manager  /  Patch Bundle  /  Merge Engine     │
├────────────────────────────────────────────────────────┤
│                  质量验证层                             │
│  Hook Engine  /  Test Gate  /  Evidence Writer          │
├────────────────────────────────────────────────────────┤
│                  资产治理层（外部服务）                  │
│  skill-q-platform（V0.2+）/ 本地文件（V0.1）           │
├────────────────────────────────────────────────────────┤
│                  观测层（外部服务）                     │
│  br-ai-spec-visual（V0.3+）/ 本地日志（V0.1）          │
└────────────────────────────────────────────────────────┘
```

## 9.3 推荐核心模块（V0.1 收缩版）

```
br-ai-spec/src/
├── cli/                    # 用户接口，命令定义
├── model-gateway/          # 新增：AI 模型抽象层（核心新增）
│   ├── registry.ts         # 模型注册
│   ├── router.ts           # 任务类型 → 模型路由
│   ├── client.ts           # 统一 LLM 调用接口
│   └── cost-tracker.ts     # 成本跟踪
├── planner/                # 合并 openspec + task-dag
│   ├── openspec-builder.ts
│   ├── task-dag-builder.ts
│   └── task-dag-validator.ts
├── context/                # Context Pack，保持现有设计
├── agent-runtime/          # 从 agents + scheduler 提取
│   ├── orchestrator.ts
│   ├── executor.ts
│   └── repair.ts
├── git-engine/             # 合并 worktree + patch + merge
├── quality/                # 合并 hooks + test-gates + evidence
├── state/                  # 新增：Run 状态机
│   └── run-state-machine.ts
└── shared/
```

## 9.4 推荐 AI 模型适配策略

```typescript
// 模型路由配置示例
const modelRoutes = {
  'task-planning': { primary: 'claude-3-5-sonnet', fallback: 'gpt-4o' },
  'code-generation': { primary: 'claude-3-5-sonnet', fallback: 'qwen-coder-plus' },
  'test-generation': { primary: 'gpt-4o-mini', fallback: 'claude-haiku' },
  'doc-generation': { primary: 'gpt-4o-mini', fallback: 'claude-haiku' },
};

// 成本限额配置
const costLimits = {
  'per-task': 2.0,     // USD
  'per-run': 10.0,     // USD
  'per-day': 100.0,    // USD
};
```

## 9.5 推荐的权限与门禁审批设计

```
L1 任务：无需审批，自动执行
L2 任务：
  - Task DAG 生成后，展示摘要，用户按回车确认后执行
  - 测试失败超过 3 轮，停止并提示人工介入
L3 任务：
  - OpenSpec 生成后，必须人工审核并签字（写入 approval-record.json）
  - 执行前需要输入确认码
  - 每次 Merge 前需要人工 review
```

---

# 十、分阶段落地路线

## 阶段一：MVP 验证阶段（4-6 周）

**目标：** 证明核心技术路线可行，跑通一个真实 L2 需求的完整链路。

**必须建设的能力：**
- br-spec init / plan / run / verify / report
- AI Model Gateway（最小版：支持 1 个主模型 + 1 个 fallback）
- OpenSpec Builder（自动生成 + 人工确认）
- Task DAG（支持 3-4 个并行 Task）
- Git worktree 管理
- Test Gate：lint + 单元测试
- Evidence：evidence-index + final-report
- 本地日志替代 Visual

**不建议建设的能力：**
- skill-q-platform 真实服务（用本地 .ai-spec/ 目录代替）
- br-ai-spec-visual 真实服务（用本地 final-report 代替）
- 完整 10 角色 Multi-Agent（用 Orchestrator + Executor + Repair 三角色）
- L3 任务支持
- 多 IDE 支持（只支持 Claude Code 或 Cursor 之一）

**验收标准：**
- "新增产品配置管理模块"样板需求能完整跑通
- 至少完成 1 个真实业务需求（非样例）
- final-report 包含完整的修改清单和测试结果
- API 成本 ≤ $15/次 L2 需求

---

## 阶段二：平台化建设阶段（6-10 周）

**目标：** 将本地闭环升级为团队共享的资产治理和观测平台。

**核心能力：**
- skill-q-platform：Manifest + Rule + Skill + Agent Profile 的 CRUD + 版本管理
- br-ai-spec-visual：Run 列表、Task DAG 可视化、Evidence 浏览
- IDE Adapter：支持 Cursor 和 Claude Code 的统一配置生成
- 多技术栈支持：增加 React + Node.js 组合
- L3 任务支持（含人工确认 Gate）

**治理能力：**
- API Key 安全管理（OS Keychain 集成）
- LLM 调用成本控制（per-run 限额）
- 资产版本锁定（manifest.lock.json 严格模式）

**扩展能力：**
- 支持自定义 Hook
- 支持自定义 Test Gate
- 支持从 Visual 下载 final-report

---

## 阶段三：企业级规模化阶段（3-6 个月）

**目标：** 支持多团队、多项目、多业务线的规模化接入。

**稳定性增强：**
- LLM 调用全链路可观测（OpenTelemetry）
- 故障自动告警（测试失败率超阈值）
- 完整的 Repair 失败分析和人工介入流程

**安全增强：**
- LLM 输出代码安全扫描（Semgrep 集成）
- Context Pack 敏感信息自动脱敏
- 三仓间通信 mTLS + API 鉴权

**多团队协作：**
- Manifest 多版本管理和灰度下发
- 跨项目 Skill 复用市场
- 团队级 AI 研发效能看板

---

## 阶段四：AI 原生演进阶段（6-18 个月）

**目标：** 随着模型能力提升，持续简化流程，向 AI 原生研发模式演进。

**多模型演进：**
- 接入更多模型（本地模型、私有化模型、专用代码模型）
- 模型能力评估 + 自动路由优化
- 模型 A/B 测试框架

**自动化演进：**
- Task DAG 自动生成质量达到 90% 以上，减少人工确认需求
- writeSet/lockKeys 自动推断（基于 AST 分析）
- 测试用例自动生成（从 OpenSpec 直接生成）

**智能运维：**
- 失败模式自动分类和根因分析
- Skill 自动优化（基于历史成功/失败数据）
- AI 辅助的架构合规检查

---

# 附录：资料不足说明

以下问题在当前资料中无法判断，建议在评审时补充：

1. **br-ai-spec 当前代码库现状**：文档中提到"如果当前 br-ai-spec 已有技术栈不同"，说明该仓库已有代码，但当前状态不明。现有代码的质量和架构对 V0.1 改造成本有重大影响。
2. **AI IDE 的实际调用机制**：方案中多处提到"通过 IDE Adapter 下发任务上下文"，但 Cursor、Claude Code 目前的 API 能力和限制没有说明，这是执行链路的核心黑盒。
3. **团队规模和分工**：不清楚负责该项目的团队规模，无法判断 4-6 周 V0.1 的人力是否足够。
4. **目标企业的合规要求**：中台金融系统的监管合规要求（如代码不能上传第三方、模型不能调用境外 API 等）可能对方案有重大约束，需要提前明确。
5. **现有 AI 工具使用情况**：团队当前是否已在使用 Cursor/Claude Code？现有使用经验会影响接入成本估算。

---

*本报告基于提供的 10 份评审资料生成，评审结论仅供参考，最终决策需结合团队实际情况综合判断。*
