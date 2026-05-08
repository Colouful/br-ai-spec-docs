# AI Coding 最佳实践操作指南

> 版本：v1.0  
> 适用对象：前端、后端、全栈、Tech Lead、AI Coding 推广负责人  
> 适用工具：Cursor、Claude Code、Codex、GitHub Copilot、OpenClaw、Windsurf、Gemini CLI  
> 核心目标：把 AI Coding 从“对话式写代码”升级为“规范驱动、测试约束、可审查、可沉淀、可规模化”的工程生产方式。

---

# 0. 总纲：AI Coding 的本质

AI Coding 不是“让 AI 替你写代码”，而是把研发过程拆成：

```text
人类负责：目标、边界、规格、验收、决策、风险兜底
AI 负责：执行、补全、生成、重构、调试、重复劳动
Harness 负责：规则、上下文、测试、Hook、CI、记忆、质量门禁
```

一句话：

> AI Coding = Spec × Context × Test × Skill × Hook × Review

如果没有 Spec，AI 会猜。  
如果没有 Context，AI 会编。  
如果没有 Test，AI 会“看起来对”。  
如果没有 Hook，AI 会忘规则。  
如果没有 Review，AI 的产物无法进入生产。

---

# 1. AI Coding 方法论分层

## 1.1 从轻到重的三种模式

| 模式 | 适用场景 | 优点 | 风险 | 是否适合生产 |
|---|---|---|---|---|
| Vibe Coding | 原型、Demo、UI 草图、脚本 | 快 | 无规格、易失控 | 不能直接生产 |
| SDD | 正式需求、多人协作、存量项目改造 | 可追溯、可验证 | 前期要写规格 | 推荐主路径 |
| Harness Engineering | 团队级规模化、长期项目 | 可沉淀、可复用、可管控 | 需要建设规则体系 | 企业级必备 |

## 1.2 一句话区分

```text
Vibe Coding：我说个大概，AI 先写，边看边改。
SDD：我先定义清楚，AI 按规格执行。
TDD：我先定义测试，AI 写代码让测试通过。
Harness：我把规则、经验、测试、门禁做成机制，AI 必须遵守。
```

---

# 2. AI Coding 六阶段工作流

推荐统一使用以下 6 阶段：

```text
DEFINE → PLAN → BUILD → VERIFY → REVIEW → SHIP
定义     计划    构建    验证      评审      交付
```

对应命令或 Skill：

| 阶段 | 目标 | 推荐 Skill | 关键产物 |
|---|---|---|---|
| DEFINE | 说清楚做什么 | grill / idea-refine / spec | 需求说明、Spec、边界 |
| PLAN | 拆清楚怎么做 | plan / task-breakdown | 任务清单、文件路径、验收标准 |
| BUILD | 小步实现 | tdd / incremental-build | 代码、测试、提交 |
| VERIFY | 证明能跑 | test / diagnose / browser-test | 测试报告、验证证据 |
| REVIEW | 防止烂代码 | code-review / security / simplify | Review 结论、修复清单 |
| SHIP | 安全上线 | ship / ci-cd / rollback | 发布清单、回滚预案 |

---

# 3. 推荐优先掌握的 Skills

下面不是简单罗列，而是按真实开发顺序推荐。

---

## 3.1 第一批：开工前必用 Skills

### 1）需求质询 Skill

推荐来源：

- `mattpocock/skills`：`/grill-me`、`/grill-with-docs`
- `obra/superpowers`：`brainstorming`
- `addyosmani/agent-skills`：`idea-refine`

用途：

```text
防止 AI 在需求不清时直接开写。
```

适用场景：

- “我想做一个 XX”
- “这个需求你帮我实现一下”
- “帮我优化一下这个模块”
- “帮我新增一个功能”

输出要求：

```markdown
## 需求复述
## 关键问题
## 不确定点
## 假设前提
## 本次目标
## 本次不做
## 初步验收标准
```

推荐提示词：

```markdown
先不要写代码。请你作为资深工程负责人，对这个需求进行质询。

要求：
1. 先复述你理解的需求。
2. 找出所有不确定点。
3. 按业务、技术、数据、接口、权限、测试、上线风险分类提问。
4. 每个问题说明为什么重要。
5. 最后输出一版可进入设计阶段的需求边界。
```

---

### 2）Spec 生成 Skill

推荐来源：

- `addyosmani/agent-skills`：`spec-driven-development`
- SDD 方法论
- OpenSpec / Spec-Kit 思路

用途：

```text
把自然语言需求变成 AI 可执行合约。
```

Spec 必须包含：

| 模块 | 内容 |
|---|---|
| 背景 | 为什么做 |
| 目标 | 要达成什么 |
| 非目标 | 明确不做什么 |
| 角色 | 谁使用 |
| 流程 | 正常流程、异常流程 |
| 规则 | 业务规则、权限规则 |
| 数据 | 表、字段、状态、枚举 |
| 接口 | 入参、出参、错误码 |
| 测试 | 如何验证 |
| 风险 | 兼容、性能、安全、上线 |

推荐提示词：

```markdown
请根据下面需求生成一份 Spec 文档。

要求：
1. 这是写给 AI Agent 执行的规格，不是普通需求说明。
2. 必须包含目标、非目标、约束、边界、异常、验收标准。
3. 所有不确定内容必须放到“待确认问题”。
4. 不允许默认修改旧接口、旧表、旧逻辑。
5. 输出 Markdown。
```

---

### 3）存量项目现状分析 Skill

用途：

```text
防止 AI 在老项目里按新项目方式设计。
```

适用场景：

- 已有 Spring Boot / React / Vue 项目新增需求
- 旧接口扩展
- 老表加字段
- 组件库改造
- 多模块联动

标准输出：

```markdown
## 当前模块现状
## 当前类与职责
## 当前接口
## 当前数据库
## 当前权限
## 当前缓存 / 消息 / 定时任务
## 本次可复用内容
## 本次禁止修改内容
## 风险点
```

推荐提示词：

```markdown
你现在面对的是存量项目，不是新项目。

请先完成现状分析，不要直接给实现方案。

必须输出：
1. 已有模块、类、表、接口的现状。
2. 哪些可以复用。
3. 哪些必须修改。
4. 哪些禁止修改。
5. 本次改动可能影响哪些旧逻辑。
6. 如果信息不足，请列出需要我提供的文件路径、表结构或接口定义。
```

---

## 3.2 第二批：实现阶段必用 Skills

### 4）TDD Skill

推荐来源：

- `obra/superpowers`：`test-driven-development`
- `mattpocock/skills`：`/tdd`
- `addyosmani/agent-skills`：`test-driven-development`

核心原则：

```text
先写失败测试，再写最小实现。
```

TDD 流程：

```text
RED：写一个失败测试
  ↓
GREEN：写最少代码让测试通过
  ↓
REFACTOR：重构，保证测试仍通过
  ↓
COMMIT：提交一个小步变更
```

适合场景：

- 工具函数
- 权限判断
- 状态机
- 数据转换
- 表单校验
- 后端 Service
- SDK
- Bug 修复

推荐提示词：

```markdown
请按 TDD 方式实现。

规则：
1. 先不要写业务实现。
2. 先根据需求写测试用例。
3. 测试必须覆盖正常、异常、边界、空值、权限、幂等。
4. 先运行测试并确认失败。
5. 再写最小实现让测试通过。
6. 最后重构，并再次运行测试。
7. 输出测试覆盖说明和未覆盖风险。
```

---

### 5）增量实现 Skill

推荐来源：

- `addyosmani/agent-skills`：`incremental-implementation`
- `superpowers`：`executing-plans`、`subagent-driven-development`

核心原则：

```text
一次只做一个垂直切片。
```

错误做法：

```text
先写所有 API → 再写所有 Service → 再写所有 UI → 最后一起测试
```

正确做法：

```text
切片 1：接口 → 业务逻辑 → 测试 → 验证 → 提交
切片 2：接口 → 业务逻辑 → 测试 → 验证 → 提交
切片 3：页面 → 联调 → 测试 → 提交
```

推荐提示词：

```markdown
请按垂直切片方式实现，不要一次性大改。

要求：
1. 每次只实现一个可验证的小闭环。
2. 每个切片必须包含代码、测试、验证方式。
3. 每完成一个切片，先暂停让我 review。
4. 不允许顺手重构无关代码。
```

---

### 6）API 与接口设计 Skill

推荐来源：

- `addyosmani/agent-skills`：`api-and-interface-design`
- SDD / Contract First

接口设计必须关注：

| 维度 | 要求 |
|---|---|
| 兼容性 | 优先新增接口，谨慎改旧接口 |
| 错误码 | 统一错误码 |
| 幂等 | 写接口必须考虑 |
| 权限 | 登录、菜单、数据权限 |
| 脱敏 | PII 返回脱敏 |
| 分页 | 深度分页限制 |
| 契约 | 前后端类型一致 |
| 测试 | Apifox / 单测 / 契约测试 |

推荐提示词：

```markdown
请为该需求设计接口契约。

必须包含：
1. URL、Method、请求参数、返回参数。
2. 字段类型、是否必填、校验规则。
3. 错误码。
4. 权限要求。
5. 幂等设计。
6. 是否兼容旧接口。
7. 是否涉及敏感字段脱敏。
8. Apifox 测试用例。
```

---

## 3.3 第三批：验证与评审 Skills

### 7）系统化调试 Skill

推荐来源：

- `obra/superpowers`：`systematic-debugging`
- `mattpocock/skills`：`/diagnose`
- `addyosmani/agent-skills`：`debugging-and-error-recovery`

调试流程：

```text
复现问题
  ↓
缩小范围
  ↓
提出假设
  ↓
加日志 / 断点 / 测试验证
  ↓
修复
  ↓
补回归测试
```

禁止：

```text
看到报错直接改
没有复现就修
没有回归测试就说修好了
```

推荐提示词：

```markdown
请不要直接修复。请按系统化调试流程处理：

1. 先复述错误现象。
2. 给出最小复现路径。
3. 列出 3 个可能原因，并按概率排序。
4. 说明每个假设如何验证。
5. 只在定位明确后修改代码。
6. 修复后补一个回归测试。
```

---

### 8）代码评审 Skill

推荐来源：

- `addyosmani/agent-skills`：`code-review-and-quality`
- `superpowers`：`requesting-code-review`

五轴评审：

| 维度 | 检查内容 |
|---|---|
| 正确性 | 逻辑、边界、异常 |
| 可读性 | 命名、结构、注释 |
| 可维护性 | 职责、耦合、重复 |
| 性能 | 慢查询、重复渲染、N+1 |
| 安全性 | 注入、越权、敏感信息 |

推荐提示词：

```markdown
请按高级工程师代码评审标准 review 当前变更。

要求：
1. 按正确性、可读性、可维护性、性能、安全性五个维度检查。
2. 问题按 BLOCKER / IMPORTANT / NIT 分级。
3. 只评价本次 diff，不要泛泛而谈。
4. 每个问题必须给出文件、位置、原因和修复建议。
5. 最后判断是否可以合并。
```

---

### 9）安全加固 Skill

推荐来源：

- `addyosmani/agent-skills`：`security-and-hardening`

重点检查：

| 场景 | 检查项 |
|---|---|
| 前端 | XSS、敏感信息、localStorage token |
| 后端 | SQL 注入、越权、鉴权绕过 |
| 接口 | 参数校验、频率限制、错误信息泄露 |
| 数据库 | 敏感字段、明文存储 |
| 日志 | Token、手机号、身份证明文 |
| 配置 | API Key、密码、密钥泄露 |

推荐提示词：

```markdown
请对当前改动进行安全审计。

重点检查：
1. 是否存在 SQL 注入、XSS、越权。
2. 是否有敏感信息明文输出。
3. 是否有硬编码密钥、Token、密码。
4. 是否有未校验的用户输入。
5. 是否有过宽的权限。
6. 输出风险等级和修复建议。
```

---

### 10）性能优化 Skill

推荐来源：

- `addyosmani/agent-skills`：`performance-optimization`

前端关注：

- 首屏加载
- 包体积
- 重渲染
- 长任务
- 图片与资源
- Core Web Vitals

后端关注：

- 慢 SQL
- N+1 查询
- 深度分页
- 大事务
- 锁竞争
- 缓存穿透 / 击穿 / 雪崩
- 外部接口超时

推荐提示词：

```markdown
请对当前功能做性能风险评估。

要求：
1. 先列出关键路径。
2. 分析数据库、缓存、网络、渲染、并发风险。
3. 给出可量化指标。
4. 给出验证方法。
5. 不允许凭感觉优化，必须先测量。
```

---

## 3.4 第四批：交付与沉淀 Skills

### 11）Ship Skill

推荐来源：

- `addyosmani/agent-skills`：`shipping-and-launch`
- `ci-cd-and-automation`

上线必须包含：

```markdown
## 上线前检查
## 数据库脚本
## 配置项
## 灰度策略
## 监控指标
## 回滚方案
## 线上验证
```

推荐提示词：

```markdown
请生成上线与回滚方案。

必须包含：
1. 上线步骤。
2. 配置开关默认值。
3. 灰度范围。
4. 数据库变更顺序。
5. 监控指标。
6. 回滚步骤。
7. 回滚后验证。
```

---

### 12）Memory / Cookbook Skill

用途：

```text
把踩坑、团队约定、环境差异、已确认决策沉淀下来。
```

推荐目录：

```text
.ai-spec/
├── memory/
│   ├── MEMORY.md
│   ├── feedback/
│   ├── project/
│   ├── decision/
│   └── incident/
```

Memory 类型：

| 类型 | 内容 |
|---|---|
| feedback | 用户纠正过两次以上的规则 |
| project | 项目事实，如环境、服务、端口 |
| decision | 架构决策 |
| incident | 事故复盘和防复发规则 |
| reference | 外部文档、监控、接口地址 |

Memory 模板：

```markdown
---
name: 禁止在 pre 环境执行 Redis KEYS
type: feedback
createdAt: 2026-05-08
---

## 背景
pre 环境 Redis 是代理型，执行 KEYS / SCAN 可能触发告警或阻塞。

## 规则
AI 不允许在 pre/prod 环境执行 KEYS、SCAN 等全量扫描命令。

## 适用场景
涉及 Redis 排查、缓存分析、线上问题定位时。

## 正确做法
1. 使用业务 key 精确查询。
2. 通过监控面板查看 key 数量。
3. 必要时让人工在低峰执行白名单脚本。

## 禁止事项
不要建议执行 KEYS *。
不要生成全量扫描脚本。
```

---

# 4. 推荐项目目录结构

适合企业团队落地：

```text
project-root/
├── CLAUDE.md
├── AGENTS.md
├── .cursor/
│   └── rules/
│       ├── project.mdc
│       ├── coding-style.mdc
│       ├── testing.mdc
│       ├── security.mdc
│       └── ai-coding-workflow.mdc
├── .ai-spec/
│   ├── manifest.md
│   ├── rules/
│   ├── skills/
│   │   ├── requirement-clarify/
│   │   ├── spec-generate/
│   │   ├── tdd/
│   │   ├── code-review/
│   │   ├── security-review/
│   │   └── ship/
│   ├── specs/
│   │   └── yyyy-mm-dd-feature-name/
│   │       ├── proposal.md
│   │       ├── spec.md
│   │       ├── design.md
│   │       ├── tasks.md
│   │       ├── tests.md
│   │       └── acceptance.md
│   ├── memory/
│   │   ├── MEMORY.md
│   │   ├── feedback/
│   │   ├── project/
│   │   └── incident/
│   └── adr/
└── docs/
    ├── architecture.md
    ├── api.md
    └── release.md
```

---

# 5. IDE / Agent 接入建议

## 5.1 Cursor

建议使用：

```text
.cursor/rules/*.mdc
```

规则拆分：

```text
project.mdc              项目总览
coding-style.mdc         编码规范
frontend.mdc             前端规范
backend.mdc              后端规范
testing.mdc              测试规范
security.mdc             安全规范
ai-workflow.mdc          AI 工作流
```

使用习惯：

```text
1. 大任务必须 @ 相关文件或目录。
2. 不让 Agent 猜项目上下文。
3. 一次只处理 2-3 个相关文件。
4. 改完必须 review diff。
```

---

## 5.2 Claude Code

建议使用：

```text
CLAUDE.md
skills/
hooks/
memory/
```

三层上下文：

| 层级 | 内容 |
|---|---|
| 全局 CLAUDE.md | 个人通用规则 |
| 项目 CLAUDE.md | 仓库规则、架构、命令 |
| 子目录 CLAUDE.md | 特定模块规则 |

建议工作流：

```text
需求 → Spec → Plan Mode → 执行 → 测试 → Review Diff → Commit
```

---

## 5.3 Codex / OpenClaw / 其他 Agent

建议统一维护：

```text
AGENTS.md
.ai-spec/manifest.md
.ai-spec/skills/
.ai-spec/rules/
```

核心原则：

```text
不要把所有规则塞进一个超长 System Prompt。
使用渐进式披露：
1. 先读 manifest
2. 再按任务加载相关 skill
3. 最后只在实现时加载具体规范
```

---

# 6. 标准操作 SOP

## 6.1 新需求开发 SOP

```text
1. 开新分支
2. 需求质询
3. 生成 Spec
4. 现状分析
5. 技术设计
6. 任务拆解
7. TDD 实现
8. 小步提交
9. 自动测试
10. AI Review
11. 人工 Review
12. 发布与回滚
13. 归档 Spec
14. 沉淀 Memory
```

推荐命令：

```text
/spec-start
/spec-design
/spec-plan
/spec-tasks
/tdd
/review
/ship
/spec-archive
```

---

## 6.2 Bug 修复 SOP

```text
1. 复现问题
2. 最小复现
3. 写失败测试
4. 定位根因
5. 修复
6. 测试通过
7. 补回归用例
8. Review
9. 记录 Memory
```

提示词：

```markdown
请按系统化调试方式处理这个 Bug。

不要直接修改代码。

步骤：
1. 先复现。
2. 再最小化。
3. 写一个失败测试。
4. 定位根因。
5. 修复。
6. 运行测试。
7. 补充回归用例。
8. 说明如何防止再次发生。
```

---

## 6.3 重构 SOP

```text
1. 先说明为什么重构
2. 明确不改变外部行为
3. 补足测试
4. 小步重构
5. 每步测试通过
6. Review Diff
7. 更新 ADR
```

重构红线：

```text
不允许借重构之名改业务逻辑。
不允许顺手改无关模块。
不允许没有测试就大改。
不允许一次性大 PR。
```

---

# 7. AI Coding 红线清单

## 7.1 通用红线

```text
禁止硬编码密钥、Token、密码。
禁止硬编码 localhost / 127.0.0.1。
禁止跳过测试就提交。
禁止没有 Review 就合并。
禁止 AI 自己 push 到主分支。
禁止删除不理解的代码。
禁止顺手重构无关逻辑。
禁止引入未确认依赖。
禁止生成无法运行的伪代码却声称完成。
```

## 7.2 后端红线

```text
禁止无参数校验的接口。
禁止无权限校验的写接口。
禁止无幂等设计的写接口。
禁止无分页限制的列表接口。
禁止大表无评估直接 DDL。
禁止事务中调用慢外部接口。
禁止日志明文打印手机号、身份证、Token。
禁止只写唯一索引而不说明并发策略。
```

## 7.3 前端红线

```text
禁止直接操作后端未定义字段。
禁止绕过统一请求封装。
禁止把 Token 打印到控制台。
禁止在组件里堆复杂业务逻辑。
禁止无 Loading / Empty / Error 状态。
禁止无权限判断展示敏感操作。
禁止无测试改复杂组件。
```

---

# 8. 场景速查表

| 场景 | 先用 Skill | 后续动作 |
|---|---|---|
| 只有模糊想法 | grill-me / idea-refine | 形成 proposal |
| 需求明确 | spec | 输出 Spec |
| 存量项目改造 | existing-project-analysis | 先做现状分析 |
| 后端接口开发 | api-design + tdd | 写接口契约和测试 |
| 前端页面开发 | frontend-ui + browser-test | 组件、状态、联调 |
| Bug 修复 | diagnose + tdd | 复现、测试、修复 |
| 代码变复杂 | zoom-out + simplify | 架构分析、小步重构 |
| 上线前 | review + ship | 门禁、灰度、回滚 |
| 踩坑复发 | write-memory | 沉淀规则 |
| 多模块并行 | subagent | 分派清晰边界任务 |

---

# 9. 团队落地路线图

## 阶段一：个人熟练

目标：

```text
会用 AI，但不乱用。
```

必练：

- 需求质询
- Spec
- TDD
- Review
- Diagnose

验收：

```text
每个需求都有 Spec。
每个复杂逻辑都有测试。
每个 PR 都经过 AI Review + 人工 Review。
```

---

## 阶段二：项目规范化

目标：

```text
让项目有统一 AI 规则。
```

建设：

```text
CLAUDE.md
AGENTS.md
.cursor/rules
.ai-spec/rules
.ai-spec/skills
.ai-spec/memory
```

验收：

```text
新人拉项目后，AI 能理解项目结构和基本纪律。
AI 不再反复犯同一种错。
```

---

## 阶段三：团队规模化

目标：

```text
让 AI Coding 成为团队工程体系。
```

建设：

```text
统一 Skill 库
统一 Spec 模板
统一 Review 清单
统一 CI 门禁
统一 Memory 机制
统一度量指标
```

度量指标：

| 指标 | 说明 |
|---|---|
| AI 采纳率 | AI 产物最终保留比例 |
| Review 返工率 | PR 被打回比例 |
| 测试覆盖率 | 新增代码测试覆盖 |
| 缺陷逃逸率 | 上线后缺陷数量 |
| Spec 完整率 | 需求是否有规格文档 |
| Memory 命中率 | 历史规则是否复用 |

---

# 10. 推荐 Skill 清单

## 10.1 最小必备 12 个

```text
01 requirement-clarify
02 spec-driven-development
03 existing-project-analysis
04 planning-and-task-breakdown
05 test-driven-development
06 incremental-implementation
07 api-and-interface-design
08 frontend-ui-engineering
09 systematic-debugging
10 code-review-and-quality
11 security-and-hardening
12 shipping-and-launch
```

## 10.2 企业增强 8 个

```text
13 context-engineering
14 memory-cookbook
15 documentation-and-adrs
16 performance-optimization
17 ci-cd-and-automation
18 deprecation-and-migration
19 subagent-driven-development
20 skill-writing
```

---

# 11. Skill 编写标准

一个合格 Skill 应该包含：

```text
name
description
when_to_use
inputs
process
outputs
verification
red_flags
examples
```

模板：

```markdown
---
name: test-driven-development
description: 当需要实现业务逻辑、修复 Bug、增加行为时，指导 AI 使用 TDD 红绿重构流程。
---

# 目标

让 AI 先写测试，再写实现，最后重构，确保行为可验证。

# 何时使用

- 新增业务逻辑
- 修复 Bug
- 修改状态机
- 修改校验规则
- 修改工具函数

# 输入

- 需求描述
- 相关文件
- 测试框架
- 运行命令

# 流程

1. 理解需求。
2. 列出测试场景。
3. 写第一个失败测试。
4. 运行并确认失败。
5. 写最小实现。
6. 运行并确认通过。
7. 重构。
8. 再次运行测试。
9. 输出验证结果。

# 输出

- 测试文件
- 实现代码
- 运行结果
- 覆盖说明

# 禁止事项

- 禁止先写实现再补测试。
- 禁止硬编码通过测试。
- 禁止跳过失败测试确认。
```

---

# 12. 适合放进 CLAUDE.md / AGENTS.md 的规则

```markdown
# AI Coding Rules

## 角色

你是项目中的高级工程助手，但不是最终决策者。  
你必须按项目规范、Spec、测试和 Review 清单工作。

## 工作边界

1. 不允许在需求不清时直接写代码。
2. 不允许修改无关代码。
3. 不允许默认重构。
4. 不允许跳过测试。
5. 不允许隐藏不确定性。
6. 不允许生成无法验证的方案。
7. 不允许泄露敏感信息。
8. 不允许绕过项目统一封装。

## 工作流程

所有非简单任务必须遵循：

DEFINE → PLAN → BUILD → VERIFY → REVIEW → SHIP

## 实现要求

1. 先读 Spec。
2. 再读相关代码。
3. 输出计划。
4. 等待确认。
5. 按 TDD 或小步增量实现。
6. 每个阶段都输出验证证据。

## Review 要求

提交前必须检查：

- 测试是否通过
- 类型检查是否通过
- Lint 是否通过
- 是否有调试代码
- 是否有安全风险
- 是否影响旧逻辑
- 是否符合 Spec
```

---

# 13. 最佳实践口诀

```text
需求不清，先质询。
动手之前，先 Spec。
复杂逻辑，先测试。
存量项目，先现状。
大改之前，先计划。
写完之后，先验证。
提交之前，先 Review。
踩坑两次，写 Memory。
规则反复失效，上 Hook。
质量不可控，上 CI。
```

---

# 14. 最终推荐使用方式

## 个人开发

```text
Cursor：负责精细修改、前端联调、局部重构
Claude Code：负责端到端任务、计划、执行、Review
Codex：负责代码生成、任务执行、批量修改
ChatGPT：负责架构设计、文档、方案、Prompt、复盘
```

## 团队开发

```text
统一规则：CLAUDE.md / AGENTS.md / Cursor Rules
统一技能：skills/
统一规格：.ai-spec/specs/
统一记忆：.ai-spec/memory/
统一门禁：Hooks + CI
统一复盘：ADR + Incident + Cookbook
```

---

# 15. 结语

AI Coding 的真正分水岭不是“谁的模型更强”，而是“谁的工程约束更清楚”。

普通用法：

```text
我说一句，AI 写一堆，我再慢慢改。
```

专业用法：

```text
我定义目标、边界、规格、测试和验收；
AI 按流程执行；
Hook 和 CI 自动兜底；
Memory 把经验沉淀；
Review 决定是否进入生产。
```

最终目标：

> 让 AI 成为可管理、可审查、可验证、可复用的工程团队成员，而不是一个不稳定的代码生成器。
