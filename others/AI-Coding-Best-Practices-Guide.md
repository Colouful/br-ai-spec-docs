# AI Coding 最佳操作开发指南

> 整合自 obra/superpowers、mattpocock/skills、addyosmani/agent-skills、forrestchang/andrej-karpathy-skills 四大开源项目
> 
> 版本: 1.0 | 更新: 2026-05-07

---

## 目录

1. [核心哲学](#1-核心哲学)
2. [开发全流程总览](#2-开发全流程总览)
3. [Phase 1: DEFINE — 定义阶段](#3-phase-1-define--定义阶段)
4. [Phase 2: PLAN — 计划阶段](#4-phase-2-plan--计划阶段)
5. [Phase 3: BUILD — 构建阶段](#5-phase-3-build--构建阶段)
6. [Phase 4: VERIFY — 验证阶段](#6-phase-4-verify--验证阶段)
7. [Phase 5: REVIEW — 评审阶段](#7-phase-5-review--评审阶段)
8. [Phase 6: SHIP — 交付阶段](#8-phase-6-ship--交付阶段)
9. [调试方法论](#9-调试方法论)
10. [Agent 沟通策略](#10-agent-沟通策略)
11. [反模式与红线](#11-反模式与红线)
12. [工具链与命令速查](#12-工具链与命令速查)
13. [场景实操速查](#13-场景实操速查) — 什么场景用什么 Skill / 命令
14. [参考来源](#14-参考来源)

**快速跳转 → 按场景找答案:** [场景索引](#场景索引)

---

## 1. 核心哲学

### 四大原则 (Karpathy)

| # | 原则 | 一句话 |
|---|------|--------|
| 1 | **先思考再编码** | 不要假设，不要隐藏困惑，暴露权衡 |
| 2 | **简洁优先** | 最少代码解决问题，不做投机性设计 |
| 3 | **外科手术式修改** | 只碰必须碰的，只清理自己制造的 |
| 4 | **目标驱动执行** | 定义成功标准，循环直到验证通过 |

### 三条底线 (Superpowers)

- **测试驱动** — 永远先写测试
- **系统化优于临时应对** — 流程优于猜测
- **证据优于声明** — "看起来对了" 不够，必须有证据

### 四个失败模式 (Matt Pocock)

| # | 病症 | 解药 |
|---|------|------|
| 1 | Agent 没做我想要的事 | `/grill-me` — 开工前详细提问 |
| 2 | Agent 废话太多 | CONTEXT.md 共享语言 |
| 3 | 代码跑不起来 | TDD + 类型系统 + 自动化测试 |
| 4 | 代码变成烂泥球 | `/improve-codebase-architecture` 定期清理 |

---

## 2. 开发全流程总览

```
DEFINE → PLAN → BUILD → VERIFY → REVIEW → SHIP
/spec    /plan   /build   /test    /review   /ship
```

每个阶段有明确的输入、输出和质量门禁。不允许跳阶段。

---

## 3. Phase 1: DEFINE — 定义阶段

> **📌 实操场景:** [场景 1: 模糊想法](#场景-1-有个模糊想法不知道怎么做) | [场景 2: 需求明确要开工](#场景-2-需求明确要开工)

### 3.1 Idea Refine（想法精炼）

**触发条件:** 你有一个模糊的想法，还不确定要做什么

**流程:**
1. 发散思考 — 列出所有可能的方向
2. 收敛思考 — 用约束条件筛选
3. 形成具体提案 — 包含目标、范围、边界

**输出:** 一页纸的提案文档

### 3.2 Spec-Driven Development（规格驱动开发）

**核心思想:** 先写规格，再写代码

**PRD 必须覆盖:**
- 目标 (Objectives) — 为什么做
- 命令 (Commands) — 怎么运行
- 结构 (Structure) — 代码组织
- 代码风格 (Code Style) — 规范
- 测试 (Testing) — 怎么验证
- 边界 (Boundaries) — 不做什么

### 3.3 Grill Session（深度质询）

**两种模式:**
- `/grill-me` — 非代码场景，Agent 反复提问直到完全理解你的意图
- `/grill-with-docs` — 工程场景，挑战你的计划，产出 CONTEXT.md 和 ADR

**为什么必须 Grill:**
Agent 会默默做出错误假设然后一路跑偏。Grill 强制它在动手前把所有不确定暴露出来。

**输出:** 
- 清晰的需求文档
- CONTEXT.md（项目术语表）
- ADR（架构决策记录）

---

## 4. Phase 2: PLAN — 计划阶段

> **📌 实操场景:** [场景 2: 需求明确要开工](#场景-2-需求明确要开工) | [场景 7: 拆成 Issue](#场景-7-要把需求拆成-issue) | [场景 9: 重构模块](#场景-9-要重构一个模块)

### 4.1 Planning & Task Breakdown（任务分解）

**规则:**
- 每个任务 2-5 分钟可完成
- 包含精确文件路径
- 包含完整代码片段
- 包含验证步骤

**任务格式:**
```
## Task N: [标题]
- 文件: src/path/to/file.ts
- 做什么: [具体修改]
- 验证: [如何确认完成]
- 依赖: [前置任务]
```

### 4.2 写计划的技巧 (Superpowers)

**关键原则:**
- 计划要清晰到 "一个没有判断力、没有项目上下文、讨厌写测试的热心初级工程师" 都能执行
- 每个步骤都要有明确的输入/输出
- 不要假设 Agent 知道隐含的上下文

**输出:** `.hermes/plans/` 或项目根目录下的 PLAN.md

### 4.3 To Issues（拆分为 Issue）

将计划/规格/PRD 拆分为可独立领取的 GitHub Issue:
- 使用垂直切片 (Vertical Slices)
- 每个 Issue 独立可交付
- 包含验收标准

---

## 5. Phase 3: BUILD — 构建阶段

> **📌 实操场景:** [场景 3: 开始写代码](#场景-3-开始写代码) | [场景 10: API 设计](#场景-10-要做-api--接口设计) | [场景 11: 前端 UI](#场景-11-要做前端-ui)

### 5.1 Test-Driven Development（测试驱动开发）

**这是整个方法论的核心。没有 TDD，其他一切都是空谈。**

**RED-GREEN-REFACTOR 循环:**

```
RED:   写一个失败的测试 → 确认它确实失败
GREEN: 写最少的代码让测试通过 → 确认它通过
REFACTOR: 清理代码 → 确认测试仍然通过
COMMIT: 提交
```

**TDD 规则:**
1. 不写产品代码，除非是为了让失败的测试通过
2. 不写更多测试代码，刚好够一个失败即可
3. 刚好够让当前失败测试通过的最少产品代码

**测试金字塔 (Addy Osmani):**
- 80% 单元测试 — 快、隔离、多
- 15% 集成测试 — 验证模块交互
- 5% E2E 测试 — 关键路径覆盖

**测试风格:**
- DAMP (Descriptive And Meaningful Phrases) 优于 DRY
- Beyonce Rule: 如果你写了代码但没写测试，你对它不够负责
- 测试名要描述行为，不是方法名

### 5.2 Incremental Implementation（增量实现）

**垂直切片法:**
```
一次做一条完整的切片:
  API → 逻辑 → UI → 测试 → 验证 → 提交

而不是:
  所有 API → 所有逻辑 → 所有 UI → 所有测试 (禁止!)
```

**每次提交:**
- 最小可运行的增量
- 包含测试
- 附带验证证据
- 使用 Feature Flag 支持回滚

### 5.3 Subagent-Driven Development（子代理驱动开发）

**流程 (Superpowers):**
1. 为每个工程任务分派一个干净的子代理
2. 子代理只看到当前任务的上下文
3. 完成后进行两阶段审查:
   - 阶段 1: 是否符合规格
   - 阶段 2: 代码质量

**适用场景:**
- 任务可以并行
- 每个任务有明确的边界
- 需要长时间自主工作

### 5.4 Context Engineering（上下文工程）

**核心:** 在正确的时间给 Agent 正确的信息

**实践:**
- 维护 rules 文件（项目规范）
- 上下文打包（把相关文件一起给）
- MCP 集成（连接外部工具）
- 不要让 Agent 在信息不足时猜测

### 5.5 Source-Driven Development（源码驱动开发）

**原则:** 决策必须基于官方文档，而非记忆

- 查阅官方文档再做决定
- 引用来源
- 验证假设

---

## 6. Phase 4: VERIFY — 验证阶段

> **📌 实操场景:** [场景 5: 提交前评审](#场景-5-代码写完了要提交) | [场景 13: 性能优化](#场景-13-性能优化)

### 6.1 Verification Before Completion（完成前验证）

**铁律:** "看起来对了" 不等于 "确实对了"

**验证清单:**
- [ ] 所有测试通过
- [ ] 类型检查通过
- [ ] Lint 通过
- [ ] 没有 console.log / print 残留
- [ ] 边界情况覆盖
- [ ] 性能没有退化

### 6.2 Browser Testing with DevTools

**使用 Chrome DevTools MCP:**
- DOM 检查 — 元素是否正确渲染
- Console 日志 — 是否有错误
- Network 追踪 — API 调用是否正确
- 性能面板 — 是否有卡顿

### 6.3 测试模式速查

```
✅ 好的测试:
- 测试行为，不测试实现
- 一个测试一个断言主题
- 测试名读起来像句子
- 独立运行，不依赖执行顺序

❌ 坏的测试:
- 测试私有方法
- 共享可变状态
- Mock 一切
- "因为它能跑" 就通过
```

---

## 7. Phase 5: REVIEW — 评审阶段

> **📌 实操场景:** [场景 5: 代码评审](#场景-5-代码写完了要提交) | [场景 6: 代码变烂泥球](#场景-6-代码变成烂泥球) | [场景 12: 安全审计](#场景-12-安全审计)

### 7.1 Code Review（代码评审）

**五轴评审法 (Addy Osmani):**

| 轴 | 检查点 |
|----|--------|
| 正确性 | 逻辑是否正确，边界是否处理 |
| 可读性 | 其他人能否理解 |
| 可维护性 | 修改是否容易 |
| 性能 | 是否有明显瓶颈 |
| 安全性 | 是否有漏洞 |

**变更大小:** 约 100 行为佳，超过 200 行必须拆分

**严重程度标签:**
- 🔴 BLOCKER — 必须修复才能合并
- 🟡 IMPORTANT — 应该修复
- 🟢 NITPICK — 可选改进

### 7.2 Code Simplification（代码简化）

**Chesterton's Fence（柴斯特顿栅栏）:**
在删除/修改代码前，先理解它为什么存在

**Rule of 500:**
如果一个文件超过 500 行，考虑拆分

**简化策略:**
- 减少复杂度但不改变行为
- 提取函数 → 提取模块 → 提取服务
- 每一步都要确保测试通过

### 7.3 Security & Hardening

**OWASP Top 10 必检:**
- 注入攻击 (SQL, NoSQL, Command)
- 身份认证缺陷
- 敏感数据暴露
- XSS

**三层边界系统:**
1. 输入验证 — 所有外部输入都是不可信的
2. 业务规则 — 权限检查
3. 数据访问 — 参数化查询

---

## 8. Phase 6: SHIP — 交付阶段

> **📌 实操场景:** [场景 14: 部署上线](#场景-14-要部署上线) | [场景 15: 废弃旧代码](#场景-15-要废弃旧代码)

### 8.1 Git Workflow

**Trunk-Based Development（主干开发）:**
- 短命分支（最多 1-2 天）
- 频繁合并
- 原子提交（每个提交独立可理解）

**提交规范:**
```
<type>(<scope>): <subject>

类型: feat, fix, refactor, test, docs, chore
范围: 影响的模块
主题: 一句话描述
```

### 8.2 CI/CD

**Shift Left（左移）:**
- 在开发阶段就跑测试
- Pre-commit hooks: lint, type check, format
- PR 自动化: 测试 + 审查 + 部署预览

**Feature Flag 生命周期:**
```
创建 → 开发 → 灰度 → 全量 → 清理
```
每个 flag 都必须有清理日期。

### 8.3 Documentation & ADR

**ADR（架构决策记录）格式:**
```markdown
# ADR-NNN: [标题]
## 状态: 提议/接受/废弃
## 上下文: [为什么需要做这个决定]
## 决定: [我们选择什么]
## 后果: [正面和负面影响]
```

---

## 9. 调试方法论

> **📌 实操场景:** [场景 4: 代码跑不通](#场景-4-agent-写的代码跑不通) | [场景 13: 性能优化](#场景-13-性能优化)

### Systematic Debugging（系统化调试）

**四阶段法 (Superpowers):**

```
1. 理解 — 理解问题，不急着修
2. 复现 — 写一个最小复现用例
3. 定位 — 二分法定位问题源头
4. 修复 — 修复 + 回归测试
```

### Diagnose Loop（诊断循环，Matt Pocock）

```
复现 (Reproduce)
  ↓
最小化 (Minimise)
  ↓
假设 (Hypothesise)
  ↓
检测 (Instrument)
  ↓
修复 (Fix)
  ↓
回归测试 (Regression Test)
```

**关键原则:**
- 不要在不理解问题的情况下修复
- 先写能复现 bug 的测试
- 修复后确认测试通过
- 清理你引入的调试代码

---

## 10. Agent 沟通策略

> **📌 实操场景:** [场景 8: Agent 跑偏](#场景-8-agent-废话太多跑偏了)

### 10.1 给 Agent 成功标准，而非指令

**Karpathy 的洞察:**
> LLM 非常擅长循环直到满足特定目标。不要告诉它做什么，给它成功标准然后看着它跑。

**弱标准 (禁止):**
```
"把这个功能做出来"
"让代码跑起来"
"修一下这个 bug"
```

**强标准 (推荐):**
```
"添加输入验证，为无效输入写测试，然后让它们通过"
"写一个能复现这个 bug 的测试，然后让它通过"
"重构 X，确保重构前后测试都通过"
```

### 10.2 多步骤任务的计划格式

```
1. [步骤] → 验证: [检查点]
2. [步骤] → 验证: [检查点]
3. [步骤] → 验证: [检查点]
```

### 10.3 CONTEXT.md（项目共享语言）

**为什么需要:**
Agent 刚进入项目时会用 20 个词表达 1 个意思

**内容:**
- 项目术语表
- 命名约定
- 常用模式
- 架构决策摘要

### 10.4 Caveman Mode（原始人模式）

**用途:** 大幅压缩 token 使用（约减少 75%）

**规则:**
- 最少文字表达最多信息
- 不要寒暄
- 代码 > 描述

---

## 11. 反模式与红线

### 🔴 绝对禁止

| 反模式 | 为什么 |
|--------|--------|
| 不写测试就写代码 | 没有测试 = 没有证据 |
| 一次性改 500+ 行 | 无法审查，容易引入 bug |
| "看起来能跑就行" | "看起来" 不等于 "确实" |
| 投机性抽象 | 为假想的未来需求设计 |
| 一次性重构整个文件 | 一步一步来，每步验证 |
| Agent 假设后直接执行 | 必须先确认再动手 |

### 🟡 警告信号

| 信号 | 行动 |
|------|------|
| Agent 没问任何问题就开始写代码 | 强制它先提问 |
| 测试全绿但行为不对 | 检查测试是否测了正确的东西 |
| 代码量远超预期 | 重写，追求最少代码 |
| 相邻代码被"顺便"改了 | 回滚无关修改 |
| 新增了"灵活性"但没被要求 | 删除多余抽象 |

### Karpathy 八条戒律

1. **不要假设** — 不确定就问
2. **不要隐藏困惑** — 把不确定说出来
3. **不要沉默选择** — 有多种解法就都列出来
4. **不要过度设计** — 最少代码解决问题
5. **不要做多余的事** — 不被要求的就不做
6. **不要改不该改的** — 只碰你必须碰的
7. **不要删不理解的** — 不确定就问
8. **不要留下烂摊子** — 清理你引入的无用代码

---

## 12. 工具链与命令速查

### Superpowers 命令

```bash
# 头脑风暴
> 先别写代码，帮我想清楚这个需求

# 创建工作区
> 用 git worktree 创建隔离工作区

# 写计划
> 把这个需求拆成 2-5 分钟的任务

# 子代理执行
> 用子代理按计划执行每个任务

# TDD
> 用 TDD 方式实现：先写失败测试

# 代码评审
> 评审这个分支的代码
```

### Matt Pocock 命令

```bash
# 安装
npx skills@latest add mattpocock/skills

# 深度质询
/grill-me          # 非代码场景
/grill-with-docs   # 工程场景

# TDD
/tdd

# 诊断
/diagnose

# 拆分 Issue
/to-issues

# 写 PRD
/to-prd

# 代码架构
/improve-codebase-architecture

# 全局视角
/zoom-out

# 原始人模式
/caveman
```

### Addy Osmani 命令

```bash
# 完整流程
/spec    → /plan  → /build  → /test  → /review  → /ship

# 单独使用
/spec              # 写规格
/plan              # 拆分任务
/build             # 增量构建
/test              # TDD
/review            # 代码评审
/code-simplify     # 简化代码
/ship              # 交付
```

### Karpathy 原则检查

每次编码前过一遍:
```
□ 我是否理解了真实需求？
□ 我的方案是否最简？
□ 我只改了必须改的？
□ 我有明确的成功标准？
□ 我的修改是否每个都可追溯到需求？
```

---

---

## 13. 场景实操速查

> **完整方法论见上方各章节，本节按场景聚合，告诉你什么情况用什么 Skill 和命令。**

### 场景索引

| # | 场景 | 关键 Skill | 跳转 |
|---|------|-----------|------|
| 1 | 有个模糊想法，不知道怎么做 | grill-me + idea-refine | [→](#场景-1-有个模糊想法不知道怎么做) |
| 2 | 需求明确，要开工 | spec + grill-with-docs | [→](#场景-2-需求明确要开工) |
| 3 | 开始写代码 | tdd + incremental-implementation | [→](#场景-3-开始写代码) |
| 4 | Agent 写的代码跑不通 | diagnose + systematic-debugging | [→](#场景-4-agent-写的代码跑不通) |
| 5 | 代码写完了，要提交 | code-review + code-simplify | [→](#场景-5-代码写完了要提交) |
| 6 | 代码变成烂泥球 | improve-codebase-architecture | [→](#场景-6-代码变成烂泥球) |
| 7 | 要把需求拆成 Issue | to-issues | [→](#场景-7-要把需求拆成-issue) |
| 8 | Agent 废话太多/跑偏了 | caveman + CONTEXT.md | [→](#场景-8-agent-废话太多跑偏了) |
| 9 | 要重构一个模块 | zoom-out + plan + tdd | [→](#场景-9-要重构一个模块) |
| 10 | 要做 API/接口设计 | api-and-interface-design | [→](#场景-10-要做-api--接口设计) |
| 11 | 要做前端 UI | frontend-ui-engineering | [→](#场景-11-要做前端-ui) |
| 12 | 安全审计 | security-and-hardening | [→](#场景-12-安全审计) |
| 13 | 性能优化 | performance-optimization | [→](#场景-13-性能优化) |
| 14 | 要部署上线 | ship + ci-cd | [→](#场景-14-要部署上线) |
| 15 | 要废弃旧代码 | deprecation-and-migration | [→](#场景-15-要废弃旧代码) |

---

### 场景 1: 有个模糊想法，不知道怎么做

**典型对话:** "我想给系统加个 XX 功能" / "这个东西能不能做成 XX"

**问题:** 需求不清晰，方向不明确，直接开写会返工

**操作步骤:**
```
Step 1: 发散思考
  命令: /grill-me (Matt Pocock)    ← 方法论详见 [3.3 Grill Session](#33-grill-session深度质询)
  或者: "先别写代码，帮我想清楚这个需求"
  效果: Agent 反复提问，逼你把模糊想法变具体

Step 2: 精炼想法
  命令: /idea-refine (Addy Osmani)  ← 方法论详见 [3.1 Idea Refine](#31-idea-refine想法精炼)
  或者: "用结构化方式帮我整理这个想法"
  效果: 发散→收敛，产出具体提案

产出: 一页纸提案（目标、范围、边界）+ 电梯 pitch
```

**判断完成的标志:** 你能用一句话说清楚 "我要做什么，为什么做，不做什么"

---

### 场景 2: 需求明确，要开工

**典型对话:** "我要实现一个 XX 功能，需求如下..." / "这个 PRD 帮我拆一下"

**操作步骤:**
```
Step 1: 深度质询 + 建文档
  命令: /grill-with-docs (Matt Pocock)  ← [3.3 Grill Session](#33-grill-session深度质询)
  效果: Agent 挑战你的方案，产出 CONTEXT.md + ADR

Step 2: 写规格
  命令: /spec (Addy Osmani)              ← [3.2 Spec-Driven Dev](#32-spec-driven-development规格驱动开发)
  效果: 完整 PRD（目标/结构/测试/边界）

Step 3: 拆分任务
  命令: /plan (Addy Osmani)              ← [4.1 Task Breakdown](#41-planning--task-breakdown任务分解)
  效果: 2-5 分钟任务 + 文件路径 + 验证步骤

Step 4: (可选) 拆为 Issue
  命令: /to-issues (Matt Pocock)         ← [4.3 To Issues](#43-to-issues拆分为-issue)
```

**判断完成的标志:** 每个任务都有精确文件路径、具体修改内容、验证方式

---

### 场景 3: 开始写代码

**典型对话:** "按计划开始实现" / "先做第一个任务"

**操作步骤:**
```
Step 1: TDD 循环
  命令: /tdd                            ← [5.1 TDD](#51-test-driven-development测试驱动开发)
  循环: RED → GREEN → REFACTOR → COMMIT

Step 2: 增量构建
  命令: /build (Addy Osmani)            ← [5.2 增量实现](#52-incremental-implementation增量实现)
  原则: 一次一个垂直切片

Step 3: (复杂任务) 子代理
  命令: 子代理模式 (Superpowers)         ← [5.3 Subagent-Driven Dev](#53-subagent-driven-development子代理驱动开发)
  适用: 任务可并行、边界清晰
```

**关键提醒:**
```
✗ 一次写 500 行再测试
✓ 写 10 行测试 → 写 5 行代码 → 测试通过 → 提交 → 循环
```

---

### 场景 4: Agent 写的代码跑不通

**典型对话:** "测试报错了" / "运行结果不对" / "报了 XX 异常"

**操作步骤:**
```
Step 1: 系统化诊断
  命令: /diagnose (Matt Pocock)         ← [9. 调试方法论](#9-调试方法论)
  循环: 复现 → 最小化 → 假设 → 检测 → 修复 → 回归测试

Step 2: 如果 Agent 直接上手改 → 阻止它!
  命令: "先别改，用四阶段法理解问题"    ← [四阶段法](#systematic-debugging系统化调试)
  流程: 理解 → 复现 → 定位 → 修复

Step 3: 写回归测试
  "写一个测试确保这个 bug 不会再出现"
```

**关键提醒:**
```
✗ "报了个错，帮我修一下" → Agent 直接猜着改
✓ "报了个错，先帮我复现，再定位原因，最后再修"
```

---

### 场景 5: 代码写完了，要提交

**典型对话:** "这个任务做完了" / "帮我 review 一下" / "准备提 PR"

**操作步骤:**
```
Step 1: 代码评审
  命令: /review (Addy Osmani)           ← [7.1 Code Review](#71-code-review代码评审)
  五轴: 正确性 / 可读性 / 可维护性 / 性能 / 安全

Step 2: 简化代码
  命令: /code-simplify (Addy Osmani)    ← [7.2 Code Simplification](#72-code-simplification代码简化)

Step 3: 提交前检查
  命令: requesting-code-review          ← [6.1 验证清单](#61-verification-before-completion完成前验证)
  检查: 测试✓ 类型✓ Lint✓ 无残留✓ < 200行✓

Step 4: 提交
  命令: /ship (Addy Osmani)             ← [8.1 Git Workflow](#81-git-workflow)
```

---

### 场景 6: 代码变成烂泥球

**典型对话:** "这代码越改越乱" / "架构需要整理" / "技术债太多了"

**操作步骤:**
```
Step 1: 全局视角
  命令: /zoom-out (Matt Pocock)
  效果: 看清全局，识别问题区域

Step 2: 架构改进
  命令: /improve-codebase-architecture (Matt Pocock)
  输入: CONTEXT.md + ADR
  输出: 改进计划

Step 3: 逐步重构 (每步 TDD)
  命令: /tdd                            ← [5.1 TDD](#51-test-driven-development测试驱动开发)
  禁止: 一次性重写整个模块
```

**频率建议:** 每 3-5 天做一次架构审视

---

### 场景 7: 要把需求拆成 Issue

**典型对话:** "PRD 写好了，拆成 GitHub Issue"

```
命令: /to-issues (Matt Pocock)           ← [4.3 To Issues](#43-to-issues拆分为-issue)
输入: PRD / 规格 / 计划
原则: 垂直切片，每个 Issue 独立可交付

每个 Issue 必须包含:
  - 描述 (做什么)
  - 验收标准 (怎么算完成)
  - 技术要点 (怎么做)
  - 依赖关系 (前置 Issue)
```

---

### 场景 8: Agent 废话太多/跑偏了

**典型对话:** "Agent 说了一堆没用的" / "它自己改了一堆不该改的"

```
情况 A: 废话太多
  命令: /caveman (Matt Pocock)          ← [10.4 Caveman Mode](#104-caveman-mode原始人模式)
  效果: Token 减少约 75%

情况 B: 跑偏了
  命令: "停下来。你偏离了需求。回到原始目标"
  预防: 开工前必须 /grill-me

情况 C: 顺便改了不该改的
  命令: "回滚所有不在需求范围内的修改"
  预防: Karpathy 原则 — "只碰必须碰的"   ← [11. 反模式](#11-反模式与红线)

长期解决:
  /grill-with-docs → 建 CONTEXT.md      ← [10.3 CONTEXT.md](#103-contextmd项目共享语言)
```

---

### 场景 9: 要重构一个模块

**典型对话:** "XX 模块需要重构" / "把旧 API 换成新 API"

```
Step 1: 理解现状
  命令: /zoom-out (Matt Pocock)
  或者: "先帮我分析这个模块的结构和依赖"

Step 2: 写重构计划
  命令: /plan                           ← [4.1 Task Breakdown](#41-planning--task-breakdown任务分解)
  原则: 每步 < 5 分钟，每步有测试

Step 3: 确保现有测试覆盖
  如果没有测试 → 先补测试，再重构

Step 4: 逐步执行 (每步 TDD)             ← [5.1 TDD](#51-test-driven-development测试驱动开发)
  循环: 写测试覆盖当前行为 → 做小改动 → 测试仍通过 → 提交
```

---

### 场景 10: 要做 API / 接口设计

**典型对话:** "设计一个 XX API" / "这个接口怎么定义"

```
Step 1: 接口设计
  Skill: api-and-interface-design (Addy Osmani)
  原则: Contract-First / Hyrum's Law / One-Version Rule / 错误语义

Step 2: 写规格
  命令: /spec                           ← [3.2 Spec-Driven Dev](#32-spec-driven-development规格驱动开发)

Step 3: TDD 实现
  命令: /tdd → 先写 API 测试 → 实现接口 → 验证
```

---

### 场景 11: 要做前端 UI

**典型对话:** "做一个 XX 页面" / "实现这个组件"

```
Step 1: 组件架构
  Skill: frontend-ui-engineering (Addy Osmani)
  覆盖: 组件架构 / 设计系统 / 状态管理 / WCAG 2.1 AA

Step 2: 写规格 + 设计
  命令: /spec

Step 3: 增量实现
  命令: /build → 一次一个组件，从叶子组件开始

Step 4: 浏览器验证
  Skill: browser-testing-with-devtools (Addy Osmani)
  工具: Chrome DevTools MCP → DOM / Console / Network / Performance
```

---

### 场景 12: 安全审计

**典型对话:** "检查一下安全性" / "有没有漏洞"

```
Step 1: 安全审计
  Skill: security-and-hardening (Addy Osmani)  ← [7.3 Security](#73-security--hardening)
  检查: OWASP Top 10 / 认证 / 密钥 / 三层边界

Step 2: 代码扫描
  命令: requesting-code-review

Step 3: 修复 (TDD)
  先写安全测试 → 修复 → 测试通过
```

---

### 场景 13: 性能优化

**典型对话:** "页面加载太慢" / "API 响应太慢" / "内存泄漏"

```
Step 1: 先测量
  Skill: performance-optimization (Addy Osmani)
  原则: Measure-First — 没有数据就没有优化

Step 2: 定位瓶颈
  命令: /diagnose                       ← [9. 调试方法论](#9-调试方法论)

Step 3: 优化 + 验证 (TDD)
  写性能测试 → 优化 → 确认改善 → 不影响功能
```

---

### 场景 14: 要部署上线

**典型对话:** "准备部署" / "发布新版本" / "配 CI/CD"

```
Step 1: CI/CD 配置
  Skill: ci-cd-and-automation (Addy Osmani)  ← [8.2 CI/CD](#82-cicd)
  原则: Shift Left / Faster is Safer / Feature Flags

Step 2: 提交前检查
  命令: /ship                           ← [8. Phase 6: SHIP](#8-phase-6-ship--交付阶段)
  清单: 测试✓ 类型✓ 安全✓ 文档✓ ADR✓

Step 3: 发布
  Skill: shipping-and-launch → Staged Rollout → 监控 → 回滚准备
```

---

### 场景 15: 要废弃旧代码

**典型对话:** "这个模块不用了" / "旧 API 要下线" / "迁移旧代码"

```
Step 1: 评估
  Skill: deprecation-and-migration (Addy Osmani)
  原则: Code is Liability / Compulsory vs Advisory / Zombie Code

Step 2: 迁移计划
  命令: /plan → 迁移路径 + 兼容期 + 回滚方案

Step 3: 执行迁移 (TDD)
  写迁移测试 → 迁移 → 验证 → 清理旧代码
```

---

### 命令速查表 (按来源)

#### Matt Pocock Skills

| 命令 | 场景 | 一句话 |
|------|------|--------|
| `/grill-me` | 需求不清 | Agent 反复提问逼你理清思路 |
| `/grill-with-docs` | 开工前 | 挑战方案，产出 CONTEXT.md + ADR |
| `/tdd` | 写代码 | RED-GREEN-REFACTOR |
| `/diagnose` | 代码报错 | 复现→最小化→假设→检测→修复 |
| `/to-issues` | 拆任务 | PRD → 独立 GitHub Issues |
| `/to-prd` | 写 PRD | 对话 → PRD → GitHub Issue |
| `/improve-codebase-architecture` | 架构清理 | 定期拯救泥球代码 |
| `/zoom-out` | 全局理解 | 看不清全貌时用 |
| `/caveman` | 压缩输出 | 省 token，少废话 |
| `/prototype` | 探索方案 | 一次性原型验证可行性 |

#### Addy Osmani Skills

| 命令 | 场景 | 一句话 |
|------|------|--------|
| `/spec` | 写规格 | PRD: 目标/结构/测试/边界 |
| `/plan` | 拆任务 | 小任务 + 验收标准 |
| `/build` | 写代码 | 一次一个垂直切片 |
| `/test` | 测试 | TDD + 测试金字塔 |
| `/review` | 审代码 | 五轴评审 |
| `/code-simplify` | 简化 | Chesterton's Fence |
| `/ship` | 交付 | 检查清单 + 发布 |

#### Superpowers

| 命令 | 场景 | 一句话 |
|------|------|--------|
| "先想清楚" | 需求不清 | 头脑风暴，不急着写代码 |
| "写计划" | 拆任务 | 2-5 分钟任务 + 精确路径 |
| "子代理执行" | 大任务 | 分派子代理，两阶段审查 |
| "TDD" | 写代码 | 先写失败测试 |
| "评审" | 提交前 | 安全扫描 + 质量门禁 |
| "系统化调试" | 报错 | 理解→复现→定位→修复 |

---

### 组合技: 典型工作流

**工作流 A: 小功能 (1-2 小时)**
```
grill-me → spec → tdd → review → ship
   5min    10min  持续   10min    5min
```

**工作流 B: 中等功能 (半天)**
```
grill-with-docs → spec → plan → to-issues
     15min        20min  15min    10min
→ [逐个 Issue: tdd → build → review] × N
→ ship
```

**工作流 C: 大功能/重构 (1-3 天)**
```
grill-with-docs → spec → plan → to-issues → [逐个 Issue: zoom-out → tdd → build → review] × N
→ improve-codebase-architecture (中间穿插)
→ security-and-hardening
→ ship
```

**工作流 D: 紧急修复 (30 min)**
```
diagnose → tdd (写回归测试) → fix → review → ship
  10min         5min          5min   5min     5min
```

**工作流 E: 探索性开发 (时间不定)**
```
idea-refine → prototype → [决定是否继续]
    10min       30min
→ 如果继续: spec → plan → tdd → ...
→ 如果放弃: 记录学到的东西
```

> **核心原则:** 不管什么场景，TDD 是贯穿始终的。没有测试的代码不算完成。

---

## 14. 参考来源

| 项目 | 星标 | 链接 | 核心价值 |
|------|------|------|----------|
| obra/superpowers | 181k | https://github.com/obra/superpowers | 完整开发方法论，子代理驱动 |
| mattpocock/skills | 64k | https://github.com/mattpocock/skills | 实战工程技能，修复四大失败模式 |
| addyosmani/agent-skills | 32k | https://github.com/addyosmani/agent-skills | 全生命周期 21 个技能，Google 工程文化 |
| forrestchang/andrej-karpathy-skills | — | https://github.com/forrestchang/andrej-karpathy-skills | Karpathy 四原则，简洁至上 |

### 延伸阅读

- *Software Engineering at Google* — 工程文化与实践
- Hyrum's Law — API 的隐式契约
- Chesterton's Fence — 修改前先理解
- Beyonce Rule — 没测试就别碰
- Trunk-Based Development — https://trunkbaseddevelopment.com

---

## 附录 A: 快速启动 Checklist

第一次使用 AI Coding Agent 时:

```
□ 1. 安装 skills (选一个源):
     - npx skills@latest add mattpocock/skills
     - 或 clone obra/superpowers
     - 或 clone addyosmani/agent-skills

□ 2. 创建 CONTEXT.md (项目术语表)

□ 3. 建立 .claude/CLAUDE.md 或等效配置文件

□ 4. 第一次用 /grill-me 熟悉 Agent 的提问能力

□ 5. 用 /spec 写你的第一个规格

□ 6. 用 /plan 拆分任务

□ 7. 用 /tdd 开始编码

□ 8. 用 /review 审查

□ 9. 用 /ship 交付
```

## 附录 B: 每日工作流模板

```markdown
## 今日目标
[一句话描述]

## 成功标准
- [ ] [具体可验证的标准 1]
- [ ] [具体可验证的标准 2]

## 计划
1. [任务] → 验证: [检查点]
2. [任务] → 验证: [检查点]

## 上下文
- 相关文件: [列表]
- 依赖: [列表]
- 约束: [列表]
```

---

> **记住:** 这些方法论的共同点是 — **先想清楚，再动手；先写测试，再写代码；先有证据，再说完成。**
>
> Agent 再强大，也需要你给出清晰的成功标准。不要假设它知道你想要什么。
