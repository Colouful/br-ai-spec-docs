# AI Coding 场景实操速查手册

> 什么场景用什么 Skill，什么命令，一目了然
> 
> 更新: 2026-05-07

---

## 场景索引

| # | 场景 | 关键 Skill | 耗时预估 |
|---|------|-----------|---------|
| 1 | [有个模糊想法，不知道怎么做](#场景-1-有个模糊想法不知道怎么做) | grill-me + idea-refine | 5-15 min |
| 2 | [需求明确，要开工](#场景-2-需求明确要开工) | spec + grill-with-docs | 10-30 min |
| 3 | [开始写代码](#场景-3-开始写代码) | tdd + incremental-implementation | 持续 |
| 4 | [Agent 写的代码跑不通](#场景-4-agent-写的代码跑不通) | diagnose + systematic-debugging | 10-30 min |
| 5 | [代码写完了，要提交](#场景-5-代码写完了要提交) | code-review + code-simplify | 10-20 min |
| 6 | [代码变成烂泥球](#场景-6-代码变成烂泥球) | improve-codebase-architecture | 30-60 min |
| 7 | [要把需求拆成 Issue](#场景-7-要把需求拆成-issue) | to-issues | 10-20 min |
| 8 | [Agent 废话太多/跑偏了](#场景-8-agent-废话太多--跑偏了) | caveman + CONTEXT.md | 2 min |
| 9 | [要重构一个模块](#场景-9-要重构一个模块) | zoom-out + plan + tdd | 30-120 min |
| 10 | [要做 API/接口设计](#场景-10-要做-api--接口设计) | api-and-interface-design | 20-40 min |
| 11 | [要做前端 UI](#场景-11-要做前端-ui) | frontend-ui-engineering | 持续 |
| 12 | [安全审计](#场景-12-安全审计) | security-and-hardening | 30-60 min |
| 13 | [性能优化](#场景-13-性能优化) | performance-optimization | 30-60 min |
| 14 | [要部署上线](#场景-14-要部署上线) | ship + ci-cd-and-automation | 10-30 min |
| 15 | [要废弃旧代码](#场景-15-要废弃旧代码) | deprecation-and-migration | 20-60 min |

---

## 场景 1: 有个模糊想法，不知道怎么做

**典型对话:** "我想给系统加个 XX 功能" / "这个东西能不能做成 XX"

**问题:** 需求不清晰，方向不明确，直接开写会返工

### 操作步骤

```
Step 1: 发散思考
  命令: /grill-me (Matt Pocock)
  或者: "先别写代码，帮我想清楚这个需求"
  效果: Agent 会反复提问，逼你把模糊想法变具体

Step 2: 精炼想法
  命令: /idea-refine (Addy Osmani)
  或者: "用结构化方式帮我整理这个想法"
  效果: 发散→收敛，产出具体提案

Step 3: 产出物
  - 一页纸提案（目标、范围、边界）
  - 一句话总结（电梯 pitch）
```

**用到的 Skill:**
- `grill-me` (Matt Pocock) — 质询式提问
- `idea-refine` (Addy Osmani) — 结构化发散/收敛

**判断完成的标志:** 你能用一句话说清楚 "我要做什么，为什么做，不做什么"

---

## 场景 2: 需求明确，要开工

**典型对话:** "我要实现一个 XX 功能，需求如下..." / "这个 PRD 帮我拆一下"

**问题:** 需求有了，但还没想清楚技术方案和任务拆分

### 操作步骤

```
Step 1: 深度质询 + 建文档
  命令: /grill-with-docs (Matt Pocock)
  效果: Agent 挑战你的方案，产出 CONTEXT.md + ADR

Step 2: 写规格
  命令: /spec (Addy Osmani)
  或者: "先写一个 PRD，覆盖目标、命令、结构、测试、边界"
  效果: 完整的 PRD 文档

Step 3: 拆分任务
  命令: /plan (Addy Osmani)
  或者: "把需求拆成 2-5 分钟可完成的任务"
  效果: 任务列表，每个有文件路径 + 验证步骤

Step 4: (可选) 拆为 Issue
  命令: /to-issues (Matt Pocock)
  效果: 独立可领取的 GitHub Issues
```

**用到的 Skill:**
- `grill-with-docs` (Matt Pocock) — 工程性质询
- `spec-driven-development` (Addy Osmani) — 写 PRD
- `planning-and-task-breakdown` (Addy Osmani) — 任务拆分
- `to-issues` (Matt Pocock) — 拆分为 Issue
- `writing-plans` (Superpowers) — 写详细执行计划

**判断完成的标志:** 每个任务都有精确文件路径、具体修改内容、验证方式

---

## 场景 3: 开始写代码

**典型对话:** "按计划开始实现" / "先做第一个任务"

**问题:** 直接写代码容易失控，需要严格流程

### 操作步骤

```
Step 1: 确保有测试
  命令: /tdd (Matt Pocock / Addy Osmani)
  或者: "用 TDD 实现，先写失败测试"
  循环:
    RED   → 写失败测试 → 确认失败
    GREEN → 写最少代码 → 确认通过
    REFACTOR → 清理 → 确认仍通过
    COMMIT

Step 2: 增量构建
  命令: /build (Addy Osmani)
  或者: "一次做一个垂直切片"
  原则: API→逻辑→UI→测试→验证→提交，一次一条线

Step 3: 复杂任务用子代理
  命令: 子代理模式 (Superpowers)
  或者: "把这个任务分派给子代理执行"
  适用: 任务可并行、边界清晰、需要长时间自主工作
```

**用到的 Skill:**
- `test-driven-development` (Superpowers / Addy Osmani / Matt Pocock) — 核心
- `incremental-implementation` (Addy Osmani) — 垂直切片
- `subagent-driven-development` (Superpowers) — 子代理分派
- `context-engineering` (Addy Osmani) — 给 Agent 正确信息

**关键提醒:**
```
✗ 一次写 500 行再测试
✓ 写 10 行测试 → 写 5 行代码 → 测试通过 → 提交 → 循环
```

---

## 场景 4: Agent 写的代码跑不通

**典型对话:** "测试报错了" / "运行结果不对" / "报了 XX 异常"

**问题:** 需要定位问题，盲目修改会越改越乱

### 操作步骤

```
Step 1: 系统化诊断
  命令: /diagnose (Matt Pocock)
  或者: "用系统化方式调试这个问题"
  循环:
    复现 → 最小化 → 假设 → 检测 → 修复 → 回归测试

Step 2: 如果 Agent 直接上手改
  阻止它! 命令: "先别改，用四阶段法理解问题"
  流程 (Superpowers):
    Phase 1: 理解 — 到底发生了什么
    Phase 2: 复现 — 写最小复现用例
    Phase 3: 定位 — 二分法找源头
    Phase 4: 修复 — 修 + 回归测试

Step 3: 写回归测试
  "写一个测试确保这个 bug 不会再出现"
```

**用到的 Skill:**
- `diagnose` (Matt Pocock) — 诊断循环
- `systematic-debugging` (Superpowers) — 四阶段调试
- `debugging-and-error-recovery` (Addy Osmani) — 五步分诊

**关键提醒:**
```
✗ "报了个错，帮我修一下" → Agent 直接猜着改
✓ "报了个错，先帮我复现，再定位原因，最后再修"
```

---

## 场景 5: 代码写完了，要提交

**典型对话:** "这个任务做完了" / "帮我 review 一下" / "准备提 PR"

**问题:** 匆忙提交会留下隐患

### 操作步骤

```
Step 1: 代码评审
  命令: /review (Addy Osmani)
  或者: "评审这个分支，按五轴标准"
  五轴: 正确性 / 可读性 / 可维护性 / 性能 / 安全

Step 2: 简化代码
  命令: /code-simplify (Addy Osmani)
  或者: "这个代码能更简洁吗"
  原则: Chesterton's Fence — 先理解再简化

Step 3: 提交前检查
  命令: requesting-code-review (Superpowers)
  或者: "提交前跑安全扫描和质量门禁"
  检查:
    □ 所有测试通过
    □ 类型检查通过
    □ Lint 通过
    □ 无调试代码残留
    □ 变更 < 200 行

Step 4: 提交
  命令: /ship (Addy Osmani)
  或者: git commit + git push + PR
```

**用到的 Skill:**
- `code-review-and-quality` (Addy Osmani) — 五轴评审
- `code-simplification` (Addy Osmani) — 简化
- `requesting-code-review` (Superpowers) — 质量门禁
- `git-workflow-and-versioning` (Addy Osmani) — 提交规范

---

## 场景 6: 代码变成烂泥球

**典型对话:** "这代码越改越乱" / "架构需要整理" / "技术债太多了"

**问题:** Agent 加速了代码熵增，需要定期清理

### 操作步骤

```
Step 1: 全局视角
  命令: /zoom-out (Matt Pocock)
  或者: "给我这个模块的整体架构视角"
  效果: 看清全局，识别问题区域

Step 2: 架构改进
  命令: /improve-codebase-architecture (Matt Pocock)
  或者: "分析代码库架构，找改进机会"
  输入: CONTEXT.md + docs/adr/ 中的决策记录
  输出: 改进计划

Step 3: 逐步重构 (每个步骤都用 TDD)
  命令: /tdd (任何来源)
  原则: 每次改一小步，测试覆盖，改完验证
  禁止: 一次性重写整个模块
```

**用到的 Skill:**
- `zoom-out` (Matt Pocock) — 全局视角
- `improve-codebase-architecture` (Matt Pocock) — 架构分析
- `code-simplification` (Addy Osmani) — 简化
- `test-driven-development` — 确保重构不破坏功能

**频率建议:** 每 3-5 天做一次架构审视

---

## 场景 7: 要把需求拆成 Issue

**典型对话:** "PRD 写好了，拆成 GitHub Issue" / "帮我建几个 Issue"

### 操作步骤

```
Step 1: 拆分
  命令: /to-issues (Matt Pocock)
  输入: PRD / 规格文档 / 计划
  原则: 垂直切片，每个 Issue 独立可交付

Step 2: 补充验收标准
  每个 Issue 必须包含:
    - 描述 (做什么)
    - 验收标准 (怎么算完成)
    - 技术要点 (怎么做)
    - 依赖关系 (前置 Issue)

Step 3: 创建
  命令: /github-issues (如果装了 GitHub skill)
  或者: gh issue create
```

**用到的 Skill:**
- `to-issues` (Matt Pocock) — PRD 拆分
- `github-issues` — 创建 Issue

---

## 场景 8: Agent 废话太多 / 跑偏了

**典型对话:** "Agent 说了一堆没用的" / "它自己改了一堆不该改的"

### 紧急处理

```
情况 A: 废话太多
  命令: /caveman (Matt Pocock)
  或者: "压缩输出，最少文字"
  效果: Token 使用减少约 75%

情况 B: 跑偏了
  命令: "停下来。你偏离了需求。回到原始目标"
  预防: 开工前必须 /grill-me

情况 C: 顺便改了不该改的
  命令: "回滚所有不在需求范围内的修改"
  预防: Karpathy 原则 — "只碰必须碰的"
```

### 长期解决

```
Step 1: 建 CONTEXT.md
  命令: /grill-with-docs
  内容: 项目术语表、命名约定、架构决策

Step 2: 写 Agent 规则文件
  CLAUDE.md / .cursorrules / .claude/settings.json
  内容: 项目规范、禁止事项、必做事项
```

**用到的 Skill:**
- `caveman` (Matt Pocock) — 压缩输出
- `grill-with-docs` (Matt Pocock) — 建共享语言
- `context-engineering` (Addy Osmani) — 规则文件

---

## 场景 9: 要重构一个模块

**典型对话:** "XX 模块需要重构" / "把旧 API 换成新 API"

### 操作步骤

```
Step 1: 理解现状
  命令: /zoom-out (Matt Pocock)
  或者: "先帮我分析这个模块的结构和依赖"

Step 2: 写重构计划
  命令: /plan (Addy Osmani)
  或者: "写一个分步重构计划，每步都可验证"
  原则: 每步 < 5 分钟，每步有测试

Step 3: 确保现有测试覆盖
  "先检查现有测试覆盖率，补充缺失的测试"
  如果没有测试 → 先补测试，再重构

Step 4: 逐步执行 (每步 TDD)
  循环:
    写测试覆盖当前行为 → 做小改动 → 测试仍通过 → 提交
```

**用到的 Skill:**
- `zoom-out` (Matt Pocock) — 全局理解
- `writing-plans` (Superpowers) — 写计划
- `test-driven-development` — 每步验证
- `subagent-driven-development` (Superpowers) — 并行重构

---

## 场景 10: 要做 API / 接口设计

**典型对话:** "设计一个 XX API" / "这个接口怎么定义"

### 操作步骤

```
Step 1: 接口设计
  Skill: api-and-interface-design (Addy Osmani)
  原则:
    - Contract-First — 先定义契约，再实现
    - Hyrum's Law — 所有可观测行为都会被依赖
    - One-Version Rule — 只维护一个版本
    - 错误语义 — 错误码要明确

Step 2: 写规格
  命令: /spec
  内容: 端点定义、请求/响应格式、错误处理、限流

Step 3: TDD 实现
  命令: /tdd
  先写 API 测试 → 实现接口 → 验证
```

**用到的 Skill:**
- `api-and-interface-design` (Addy Osmani) — API 设计
- `spec-driven-development` (Addy Osmani) — 写规格
- `test-driven-development` — 测试驱动

---

## 场景 11: 要做前端 UI

**典型对话:** "做一个 XX 页面" / "实现这个组件"

### 操作步骤

```
Step 1: 组件架构
  Skill: frontend-ui-engineering (Addy Osmani)
  覆盖:
    - 组件架构
    - 设计系统
    - 状态管理
    - WCAG 2.1 AA 无障碍

Step 2: 写规格 + 设计
  命令: /spec
  内容: 组件树、状态流、交互行为

Step 3: 增量实现
  命令: /build
  原则: 一次一个组件，从叶子组件开始

Step 4: 浏览器验证
  Skill: browser-testing-with-devtools (Addy Osmani)
  工具: Chrome DevTools MCP
  检查: DOM / Console / Network / Performance
```

**用到的 Skill:**
- `frontend-ui-engineering` (Addy Osmani) — 前端工程
- `browser-testing-with-devtools` (Addy Osmani) — 浏览器测试
- `incremental-implementation` (Addy Osmani) — 增量构建

---

## 场景 12: 安全审计

**典型对话:** "检查一下安全性" / "有没有漏洞"

### 操作步骤

```
Step 1: 安全审计
  Skill: security-and-hardening (Addy Osmani)
  检查:
    - OWASP Top 10
    - 身份认证模式
    - 密钥管理
    - 三层边界系统

Step 2: 代码扫描
  命令: requesting-code-review (Superpowers)
  包含: 安全扫描 + 质量门禁

Step 3: 修复
  命令: /tdd
  原则: 先写安全测试 → 修复 → 测试通过
```

**用到的 Skill:**
- `security-and-hardening` (Addy Osmani) — 安全加固
- `requesting-code-review` (Superpowers) — 安全扫描
- Security Auditor Agent Persona (Addy Osmani) — 安全专家视角

---

## 场景 13: 性能优化

**典型对话:** "页面加载太慢" / "API 响应太慢" / "内存泄漏"

### 操作步骤

```
Step 1: 先测量
  Skill: performance-optimization (Addy Osmani)
  原则: Measure-First — 没有数据就没有优化
  工具: Core Web Vitals / Profiling / Bundle Analysis

Step 2: 定位瓶颈
  命令: /diagnose
  循环: 复现 → 测量 → 定位 → 假设 → 验证

Step 3: 优化 + 验证
  命令: /tdd
  原则: 写性能测试 → 优化 → 确认改善 → 不影响功能
```

**用到的 Skill:**
- `performance-optimization` (Addy Osmani) — 性能优化
- `diagnose` (Matt Pocock) — 诊断瓶颈
- `browser-testing-with-devtools` (Addy Osmani) — 浏览器性能分析

---

## 场景 14: 要部署上线

**典型对话:** "准备部署" / "发布新版本" / "配 CI/CD"

### 操作步骤

```
Step 1: CI/CD 配置
  Skill: ci-cd-and-automation (Addy Osmani)
  原则:
    - Shift Left — 测试尽早
    - Faster is Safer — 部署越频繁风险越低
    - Feature Flags — 灰度发布

Step 2: 提交前检查
  命令: /ship (Addy Osmani)
  清单:
    □ 所有测试通过
    □ 类型检查通过
    □ 安全扫描通过
    □ 文档更新
    □ ADR 记录

Step 3: 发布
  Skill: shipping-and-launch (Addy Osmani)
  流程: Staged Rollout → 监控 → 回滚准备
```

**用到的 Skill:**
- `ci-cd-and-automation` (Addy Osmani) — CI/CD
- `shipping-and-launch` (Addy Osmani) — 发布
- `git-workflow-and-versioning` (Addy Osmani) — 版本管理

---

## 场景 15: 要废弃旧代码

**典型对话:** "这个模块不用了" / "旧 API 要下线" / "迁移旧代码"

### 操作步骤

```
Step 1: 评估
  Skill: deprecation-and-migration (Addy Osmani)
  原则:
    - Code is Liability — 代码是负债
    - Compulsory vs Advisory — 强制 vs 建议
    - Zombie Code — 没人用的代码要删

Step 2: 迁移计划
  命令: /plan
  内容: 迁移路径、兼容期、回滚方案

Step 3: 执行迁移
  命令: /tdd
  原则: 写迁移测试 → 迁移 → 验证 → 清理旧代码
```

**用到的 Skill:**
- `deprecation-and-migration` (Addy Osmani) — 废弃策略
- `writing-plans` (Superpowers) — 迁移计划
- `test-driven-development` — 安全迁移

---

## 命令速查表 (按来源)

### Matt Pocock Skills

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

### Addy Osmani Skills

| 命令 | 场景 | 一句话 |
|------|------|--------|
| `/spec` | 写规格 | PRD: 目标/结构/测试/边界 |
| `/plan` | 拆任务 | 小任务 + 验收标准 |
| `/build` | 写代码 | 一次一个垂直切片 |
| `/test` | 测试 | TDD + 测试金字塔 |
| `/review` | 审代码 | 五轴评审 |
| `/code-simplify` | 简化 | Chesterton's Fence |
| `/ship` | 交付 | 检查清单 + 发布 |

### Superpowers (v5.1.0)

> 来源: [github.com/obra/superpowers](https://github.com/obra/superpowers)
> 安装: `/plugin install superpowers@claude-plugins-official`

**核心工作流 Skills:**

| 命令 / 触发方式 | Skill 名 | 场景 | 一句话 |
|----------------|----------|------|--------|
| "先想清楚" / 任何创意工作前 | `brainstorming` | 需求不清 | 苏格拉底式对话，探索意图和需求，产出设计文档 |
| "写计划" / 有已批准的 spec 时 | `writing-plans` | 拆任务 | 每个任务 2-5 分钟，含精确文件路径 + 完整代码 + 验证步骤 |
| "子代理执行" / 有计划时 | `subagent-driven-development` | 大任务 | 每个任务派一个子代理，两阶段审查 (规格合规 + 代码质量) |
| "并行代理" / 2+ 独立任务时 | `dispatching-parallel-agents` | 并行任务 | 每个问题域一个代理，无共享状态时并发执行 |
| "TDD" / 实现阶段 | `test-driven-development` | 写代码 | RED→GREEN→REFACTOR，先写失败测试再写代码 |
| "系统化调试" / 任何 bug 或异常 | `systematic-debugging` | 报错 | 四阶段: 理解→复现→定位→修复。铁律: 不查清根因不许修 |
| "评审" / 任务间 & 合并前 | `requesting-code-review` | 提交前 | 派子代理做代码审查，每个任务后和合并前必做 |
| "收评审" / 收到评审反馈时 | `receiving-code-review` | 收到反馈 | 技术评估而非表演性同意，禁止 "You're absolutely right!" |
| "验证" / 声称完成前 | `verification-before-completion` | 完成检查 | 先跑验证命令确认输出，再声称成功。"Evidence before assertions" |
| "完分支" / 所有任务完成时 | `finishing-a-development-branch` | 分支收尾 | 验证测试，选择合并/PR/保留/丢弃，清理 worktree |
| "用 worktree" / 设计批准后 | `using-git-worktrees` | 隔离环境 | 创建隔离工作区，运行项目初始化，验证干净测试基线 |
| "写 skill" / 创建或编辑 skill 时 | `writing-skills` | 自定义 Skill | 对流程文档做 TDD — 先写测试场景，再写 skill，验证合规 |
| "执行计划" / 无子代理支持时 | `executing-plans` | 顺序执行 | writing-plans 的替代方案，顺序执行任务 + 审查检查点 |

**默认工作流顺序:**
```
brainstorming → using-git-worktrees → writing-plans
  → subagent-driven-development (全程 test-driven-development)
  → requesting-code-review → finishing-a-development-branch
```

### oh-my-claudecode / OMC (v4.12.0)

> 来源: [github.com/Yeachan-Heo/oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode)
> 安装: 两条命令分别执行
> ```
> /plugin marketplace add https://github.com/Yeachan-Heo/oh-my-claudecode
> /plugin install oh-my-claudecode
> ```
> 备选 (npm): `npm i -g oh-my-claude-sisyphus@latest`
> 安装后需运行: `/setup` 或 `/omc-setup`

**工作流 / 编排模式:**

| 命令 / 触发词 | Skill 名 | 场景 | 一句话 |
|--------------|----------|------|--------|
| `/autopilot` | `autopilot` | 端到端开发 | 从想法到可运行代码全自动: 需求→设计→规划→并行实现→QA→验证 |
| `/ralph` | `ralph` | 持续执行 | 自引用持久循环，所有 user story 通过审查才停。含 ultrawork 并行 |
| `/ultrawork` 或 "ulw" | `ultrawork` | 高吞吐任务 | 并行执行引擎，多个代理同时处理独立任务 |
| `/team` | `team` | 多代理协作 | N 个代理共享任务列表: plan→prd→exec→verify→fix 流水线 |
| `/ccg` | `ccg` | 三模型编排 | Claude + Codex + Gemini 三模型路由，Claude 综合结果 |
| `/ultraqa` | `ultraqa` | QA 循环 | 测试→验证→修复→重复，直到目标达成 |
| `/ralplan` | `ralplan` | 共识规划 | Planner/Architect/Critic 迭代循环，RALPLAN-DR 结构化审议 |
| `/plan` (omc-plan) | `plan` | 战略规划 | 自动检测: 面试用户 or 直接规划 |
| `/deep-interview` | `deep-interview` | 需求澄清 | 苏格拉底式深度访谈 + 数学歧义门控，模糊想法→精确 spec |
| `/deep-dive` | `deep-dive` | 深度调查 | 两阶段: trace (因果调查) → deep-interview (需求结晶) |
| `/sciomc` | `sciomc` | 并行研究 | 编排并行科学家代理做综合研究，AUTO 模式 |
| `/deepinit` | `deepinit` | 代码库初始化 | 深度代码库分析，生成分层 AGENTS.md 文档 |
| `/external-context` | `external-context` | 外部搜索 | 派并行文档专家代理做外部网页搜索和文档查询 |
| "deslop" / "anti-slop" | `ai-slop-cleaner` | 清理 AI 代码 | 回归安全、删除优先的工作流清理 AI 生成的烂代码 |
| `/self-improve` | `self-improve` | 自进化改进 | 自主进化代码改进引擎，锦标赛选择 |

**实用工具:**

| 命令 | Skill 名 | 一句话 |
|------|----------|--------|
| `/ask codex` / `/ask gemini` | `ask` | 路由到 Claude/Codex/Gemini，捕获产物 |
| `/cancel` 或 "cancelomc" | `cancel` | 取消任何活跃的 OMC 模式 |
| `/verify` | `verify` | 完成前验证变更是否真正有效 |
| `/trace` | `trace` | 证据驱动的因果追踪，编排竞争假设 |
| `/wiki` | `wiki` | 跨会话持久化知识库 |
| `/remember` | `remember` | 审查可复用的项目知识，决定存到哪里 |
| `/release` | `release` | 通用发布助手，分析仓库发布规则 |
| `/skillify` | `skillify` | 从当前会话提取可复用 skill 草稿 |
| `/mcp-setup` | `mcp-setup` | 配置常用 MCP 服务器 |
| `/hud` | `hud` | 配置 HUD 显示选项 |
| `/omc-doctor` | `omc-doctor` | 诊断和修复 OMC 安装问题 |

### Everything Claude Code / ECC (v1.9.0)

> 来源: [github.com/affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> 安装:
> ```
> /plugin marketplace add affaan-m/everything-claude-code
> /plugin install everything-claude-code@everything-claude-code
> ```
> 安装后运行 `/configure-ecc` 完成规则配置

**语言模式 (按需调用):**

| 语言 | Skill | 说明 |
|------|-------|------|
| Python | `python-patterns` / `python-testing` / `python-review` | PEP 8、类型提示、测试、审查 |
| Go | `golang-patterns` / `golang-testing` / `go-review` / `go-build` | 惯用 Go、并发、测试、构建 |
| Rust | `rust-patterns` / `rust-testing` / `rust-review` / `rust-build` | 所有权、生命周期、测试、构建 |
| TypeScript | (见 superpowers rules) | 类型安全、异步正确性 |
| Kotlin | `kotlin-patterns` / `kotlin-testing` / `kotlin-build` | 协程、Compose、测试、构建 |
| Java | `java-coding-standards` / `springboot-patterns` / `springboot-tdd` | 分层架构、JPA、安全 |
| C++ | `cpp-coding-standards` / `cpp-testing` / `cpp-review` / `cpp-build` | 内存安全、现代 C++、测试 |
| Swift | `swift-concurrency-6-2` / `swiftui-patterns` | 并发、SwiftUI |
| Flutter | `flutter-dart-code-review` | Widget 最佳实践、状态管理 |
| PHP | `laravel-patterns` / `laravel-tdd` / `laravel-security` | Laravel 全套 |
| Perl | `perl-patterns` / `perl-testing` | Perl 模式和测试 |

**框架模式:** `django-*` / `laravel-*` / `springboot-*` / `nuxt4-patterns` / `nextjs-turbopack`

**质量 & 工作流:**

| Skill | 一句话 |
|-------|--------|
| `tdd` / `tdd-workflow` | TDD 工作流 (RED→GREEN→REFACTOR) |
| `code-review` | 代码审查 (严重性评级、SOLID 检查) |
| `security-review` / `security-scan` | OWASP Top 10、密钥泄露、不安全模式 |
| `refactor-clean` | 死代码清理、重复消除 |
| `verification-loop` | 完成前验证循环 |
| `quality-gate` | 质量门禁 |
| `api-design` | API 设计 (Contract-First、Hyrum's Law) |
| `database-schema-design` | 数据库 Schema 设计 |
| `mcp-server-patterns` | MCP 服务器开发模式 |
| `eval-harness` / `agent-eval` | 代理评估框架 |

---

### 插件安装速查

| 插件 | 安装命令 | 备选 |
|------|---------|------|
| **Superpowers** | `/plugin install superpowers@claude-plugins-official` | `/plugin marketplace add obra/superpowers-marketplace` → `/plugin install superpowers@superpowers-marketplace` |
| **OMC** | `/plugin marketplace add https://github.com/Yeachan-Heo/oh-my-claudecode` → `/plugin install oh-my-claudecode` | `npm i -g oh-my-claude-sisyphus@latest` → `/setup` |
| **ECC** | `/plugin marketplace add affaan-m/everything-claude-code` → `/plugin install everything-claude-code@everything-claude-code` | 安装后 `/configure-ecc` 配置规则 |

> **注意:** `/plugin` 命令需在 Claude Code 会话内执行，每条命令单独执行。
> 所有插件安装后 skill 自动可用，无需额外配置 (OMC 需运行 `/setup`)。

### Karpathy 原则 (贯穿所有场景)

| 检查项 | 何时检查 |
|--------|---------|
| 我是否理解了真实需求？ | 开工前 |
| 方案是否最简？ | 设计时 |
| 只改了必须改的？ | 每次提交 |
| 有明确成功标准？ | 写计划时 |
| 每行修改可追溯到需求？ | 代码评审 |

---

## 组合技: 典型工作流

### 工作流 A: 小功能 (1-2 小时)

```
grill-me → spec → tdd → review → ship
   5min    10min  持续   10min    5min
```

### 工作流 B: 中等功能 (半天)

```
grill-with-docs → spec → plan → to-issues
     15min        20min  15min    10min

→ [逐个 Issue: tdd → build → review] × N
→ ship
```

### 工作流 C: 大功能/重构 (1-3 天)

```
grill-with-docs → spec → plan → to-issues
     30min        30min  30min    15min

→ [逐个 Issue: zoom-out → tdd → build → review] × N
→ improve-codebase-architecture (中间穿插)
→ security-and-hardening
→ ship
```

### 工作流 D: 紧急修复 (30 min)

```
diagnose → tdd (写回归测试) → fix → review → ship
  10min         5min          5min   5min     5min
```

### 工作流 E: 探索性开发 (时间不定)

```
idea-refine → prototype → [决定是否继续]
    10min       30min

→ 如果继续: spec → plan → tdd → ...
→ 如果放弃: 记录学到的东西
```

---

> **核心原则:** 不管什么场景，TDD 是贯穿始终的。没有测试的代码不算完成。
