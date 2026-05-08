# AI Coding Skills / 插件安装与自定义命令使用指南

> 作为《AI Coding 最佳实践操作指南》的补充章节。  
> 重点解决两个问题：  
> 1. 这些 Skills / 插件怎么安装、怎么接入不同工具。  
> 2. 单个自定义命令应该怎么设计、什么时候用、怎么写。

---

# 1. 先理解：Skill、Plugin、Command、Rule 的区别

| 名称 | 中文理解 | 作用 | 典型载体 |
|---|---|---|---|
| Skill | 技能 / 工作流能力 | 让 AI 按一套步骤完成某类任务 | `SKILL.md`、插件市场、skills 目录 |
| Plugin | 插件包 | 一组 Skills、命令、Hook、规则的集合 | Claude Code Plugin、Codex Plugin |
| Command | 自定义命令 | 用 `/xxx` 触发固定流程 | `.claude/commands`、工具命令系统 |
| Rule | 规则 | 长期约束 AI 的行为 | `CLAUDE.md`、`AGENTS.md`、`.cursor/rules/*.mdc` |
| Hook | 自动门禁 | 在工具调用、提交、结束前自动检查 | Claude Hooks、Git Hooks、CI |
| Memory | 记忆 / 经验库 | 沉淀项目事实、踩坑、团队纪律 | `.ai-spec/memory`、`MEMORY.md` |

推荐理解：

```text
Rule 负责长期约束
Skill 负责按需执行
Command 负责快速触发
Hook 负责自动兜底
Memory 负责经验复用
Plugin 负责批量安装
```

---

# 2. 四类参考 Skills 的定位

## 2.1 obra/superpowers

定位：

```text
完整的软件开发方法论插件包。
```

核心特点：

- 不让 Agent 一上来就写代码。
- 先通过 brainstorming 澄清需求。
- 再写详细计划。
- 再按 TDD 与子代理流程执行。
- 最后 Review、验证、收尾。

适合：

- Claude Code / Codex / Cursor 等 Agent 工作流增强。
- 想要一套完整“需求 → 设计 → 计划 → TDD → Review → 交付”的团队。
- 希望减少 AI 乱跑、漏测试、跳 Review 的情况。

优先练习：

| Skill | 作用 |
|---|---|
| brainstorming | 写代码前澄清需求 |
| writing-plans | 把设计拆成可执行任务 |
| test-driven-development | 红绿重构 |
| subagent-driven-development | 子代理执行与双阶段评审 |
| requesting-code-review | 提交前审查 |
| systematic-debugging | 系统化调试 |
| finishing-a-development-branch | 收尾、合并、清理工作区 |

---

## 2.2 mattpocock/skills

定位：

```text
真实工程师日常使用的小而美 Skills。
```

核心特点：

- 小、独立、可组合。
- 解决 AI Coding 中最常见的失败模式。
- 强调先质询、建立项目共享语言、TDD、诊断、架构整理。

适合：

- TypeScript / React / 前端工程师。
- 已经用 Cursor / Claude Code，但发现 Agent 经常跑偏。
- 想先从几个高频命令开始练习的人。

优先练习：

| Command / Skill | 作用 |
|---|---|
| `/setup-matt-pocock-skills` | 初始化仓库级配置 |
| `/grill-me` | 非代码场景深度质询 |
| `/grill-with-docs` | 工程场景深度质询，并沉淀 CONTEXT.md / ADR |
| `/tdd` | TDD 开发 |
| `/diagnose` | 系统化诊断 |
| `/to-prd` | 对话转 PRD |
| `/to-issues` | PRD / 计划转 Issue |
| `/zoom-out` | 从全局理解代码 |
| `/improve-codebase-architecture` | 改善架构、治理烂泥球 |
| `/caveman` | 压缩沟通，降低废话 |

---

## 2.3 addyosmani/agent-skills

定位：

```text
覆盖完整研发生命周期的生产级 Agent Skills。
```

核心特点：

- 把开发流程拆成 DEFINE → PLAN → BUILD → VERIFY → REVIEW → SHIP。
- 提供 7 个主命令。
- 内置 20 个工程 Skill。
- 适合企业团队把 AI Coding 变成标准交付流程。

优先练习 7 个命令：

| Command | 阶段 | 作用 |
|---|---|---|
| `/spec` | DEFINE | 定义要做什么 |
| `/plan` | PLAN | 拆分任务 |
| `/build` | BUILD | 增量实现 |
| `/test` | VERIFY | 验证功能 |
| `/review` | REVIEW | 评审质量 |
| `/code-simplify` | REVIEW | 简化代码 |
| `/ship` | SHIP | 发布上线 |

---

## 2.4 forrestchang/andrej-karpathy-skills

定位：

```text
一套极简但关键的 AI Coding 行为准则。
```

核心原则：

| 原则 | 说明 |
|---|---|
| Think Before Coding | 先想清楚再写，不隐藏困惑 |
| Simplicity First | 简洁优先，不做过度抽象 |
| Surgical Changes | 外科手术式修改，只动必要代码 |
| Goal-Driven Execution | 用成功标准驱动 AI 循环验证 |

适合：

- 放到全局 `CLAUDE.md`、`AGENTS.md` 或 Cursor Rule。
- 作为所有 AI Coding 的底层纪律。
- 防止 AI 过度设计、乱改无关代码、隐藏不确定性。

---

# 3. 安装方式总览

## 3.1 Claude Code 安装

### 3.1.1 安装 Superpowers

方式一：官方插件市场

```bash
/plugin install superpowers@claude-plugins-official
```

方式二：Superpowers Marketplace

```bash
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace
```

适用场景：

```text
你希望 Claude Code 自动拥有完整工程工作流：
brainstorming → writing-plans → TDD → subagent → review → finish branch
```

---

### 3.1.2 安装 Addy Osmani Agent Skills

```bash
/plugin marketplace add addyosmani/agent-skills
/plugin install agent-skills@addy-agent-skills
```

如果 SSH 克隆失败，可以使用 HTTPS：

```bash
/plugin marketplace add https://github.com/addyosmani/agent-skills.git
/plugin install agent-skills@addy-agent-skills
```

适用场景：

```text
你希望在 Claude Code 里直接使用：
/spec
/plan
/build
/test
/review
/code-simplify
/ship
```

---

### 3.1.3 安装 Matt Pocock Skills

```bash
npx skills@latest add mattpocock/skills
```

安装后运行：

```bash
/setup-matt-pocock-skills
```

它会询问：

```text
1. 使用 GitHub、Linear，还是本地文件作为任务系统。
2. triage 标签怎么设置。
3. 文档要保存到哪里。
```

适用场景：

```text
你想优先使用 /grill-me、/grill-with-docs、/tdd、/diagnose、/to-prd、/to-issues。
```

---

### 3.1.4 安装 Karpathy Guidelines

方式一：作为 Claude Code 插件

```bash
/plugin marketplace add forrestchang/andrej-karpathy-skills
/plugin install andrej-karpathy-skills@karpathy-skills
```

方式二：直接写入项目 `CLAUDE.md`

```bash
curl -o CLAUDE.md https://raw.githubusercontent.com/forrestchang/andrej-karpathy-skills/main/CLAUDE.md
```

已有项目追加：

```bash
echo "" >> CLAUDE.md
curl https://raw.githubusercontent.com/forrestchang/andrej-karpathy-skills/main/CLAUDE.md >> CLAUDE.md
```

适用场景：

```text
你想让 AI 默认遵守：
先思考、保持简单、外科手术式修改、目标驱动验证。
```

---

## 3.2 Cursor 接入方式

Cursor 不一定需要“插件安装”，更常用的是把 Skill 内容转成 Rules。

推荐目录：

```text
.cursor/
└── rules/
    ├── ai-coding-workflow.mdc
    ├── tdd.mdc
    ├── sdd.mdc
    ├── code-review.mdc
    ├── security.mdc
    ├── frontend.mdc
    └── backend.mdc
```

### 方式一：安装 Superpowers

在 Cursor Agent Chat 中：

```text
/add-plugin superpowers
```

或在插件市场搜索：

```text
superpowers
```

### 方式二：手动接入 Addy / Matt / Karpathy

把对应的 `SKILL.md` 内容复制到：

```text
.cursor/rules/
```

例如：

```text
.cursor/rules/tdd.mdc
.cursor/rules/spec-driven-development.mdc
.cursor/rules/code-review.mdc
.cursor/rules/karpathy-guidelines.mdc
```

建议规则：

```markdown
---
description: 当用户要求实现功能、修复 Bug、重构、评审代码时，必须遵守该规则。
alwaysApply: false
---

# AI Coding Workflow

非简单任务必须遵守：

DEFINE → PLAN → BUILD → VERIFY → REVIEW → SHIP

实现前先输出计划。
复杂逻辑优先 TDD。
提交前必须 Review Diff。
禁止修改无关代码。
```

---

## 3.3 Codex 接入方式

### 3.3.1 安装 Superpowers

在 Codex CLI 中：

```bash
/plugins
```

搜索：

```text
superpowers
```

选择安装。

### 3.3.2 通用接入方式

如果某个 Skill 没有 Codex 插件形态，可以使用：

```text
AGENTS.md
.ai-spec/skills/
.ai-spec/rules/
```

推荐结构：

```text
project-root/
├── AGENTS.md
└── .ai-spec/
    ├── skills/
    │   ├── tdd/
    │   ├── spec/
    │   ├── review/
    │   └── ship/
    └── rules/
```

---

## 3.4 Gemini CLI 接入方式

### 安装 Superpowers

```bash
gemini extensions install https://github.com/obra/superpowers
```

更新：

```bash
gemini extensions update superpowers
```

### 安装 Addy Agent Skills

```bash
gemini skills install https://github.com/addyosmani/agent-skills.git --path skills
```

本地安装：

```bash
gemini skills install ./agent-skills/skills/
```

---

## 3.5 GitHub Copilot CLI 接入方式

### 安装 Superpowers

```bash
copilot plugin marketplace add obra/superpowers-marketplace
copilot plugin install superpowers@superpowers-marketplace
```

### 手动接入规则

可以把团队规则写入：

```text
.github/copilot-instructions.md
```

适合内容：

```markdown
# Copilot Instructions

所有非简单任务必须：
1. 先分析需求。
2. 再输出计划。
3. 再小步实现。
4. 最后补测试并说明验证方式。

禁止：
- 跳过测试。
- 修改无关代码。
- 生成明文密钥。
- 未确认接口契约直接改前后端字段。
```

---

## 3.6 OpenClaw / OpenCode / 其他 Agent 接入方式

推荐统一使用：

```text
AGENTS.md
.ai-spec/manifest.md
.ai-spec/rules/
.ai-spec/skills/
.ai-spec/commands/
```

推荐加载逻辑：

```text
1. 启动时读取 AGENTS.md
2. 读取 .ai-spec/manifest.md
3. 根据任务类型按需加载 skill
4. 执行命令时读取 .ai-spec/commands/{command}.md
5. 结束前执行 review / test / hook
```

---

# 4. 安装后如何验证是否生效

## 4.1 验证 Superpowers

输入：

```text
我要开发一个用户批量导入功能，先别写代码。
```

预期行为：

```text
Agent 不应直接写代码。
它应该先进入 brainstorming / 需求澄清，询问目标、边界、数据、异常、测试。
```

## 4.2 验证 Addy Agent Skills

输入：

```text
/spec 我想新增一个订单批量审核功能
```

预期行为：

```text
Agent 应输出 Spec / PRD 风格内容，而不是直接实现。
```

## 4.3 验证 Matt Pocock Skills

输入：

```text
/grill-with-docs 我想重构订单模块
```

预期行为：

```text
Agent 应持续质询你，挑战方案，并尝试沉淀 CONTEXT.md / ADR。
```

## 4.4 验证 Karpathy Guidelines

输入：

```text
帮我顺便把这个模块重构一下
```

预期行为：

```text
Agent 应该拒绝“顺便大改”，或者提醒只做与目标直接相关的外科手术式修改。
```

---

# 5. 单个自定义命令设计方法

## 5.1 自定义命令应该解决什么问题

自定义命令不是“短 Prompt”，而是：

```text
把一个高频、稳定、可复用的工程动作封装成标准流程。
```

适合做成命令的场景：

| 场景 | 是否适合命令 |
|---|---|
| 每次新需求都要写 Spec | 适合 |
| 每次提交前都要 Review | 适合 |
| 每次 Bug 都要诊断 | 适合 |
| 偶尔问一个概念 | 不适合 |
| 临时讨论方案 | 不一定适合 |
| 需要严格格式输出 | 适合 |
| 需要质量门禁 | 适合 |

---

## 5.2 命令文件推荐结构

如果工具支持自定义 Slash Command，推荐一个命令一个文件：

```text
.claude/commands/
├── spec-start.md
├── spec-plan.md
├── tdd-implement.md
├── bug-diagnose.md
├── review-diff.md
├── ship-check.md
└── memory-add.md
```

通用命令模板：

```markdown
---
name: spec-start
description: 启动一个新需求的 SDD 流程，先澄清需求、输出 Spec，不直接写代码。
---

# 角色

你是高级软件工程师和需求澄清专家。

# 使用场景

当用户提出新需求、新功能、模块改造时使用。

# 输入

用户提供的需求描述。

# 执行流程

1. 复述需求。
2. 识别不确定点。
3. 输出待确认问题。
4. 明确目标与非目标。
5. 输出初版 Spec。
6. 不允许写代码。

# 输出格式

## 需求复述
## 目标
## 非目标
## 关键规则
## 待确认问题
## 初版 Spec
## 下一步建议
```

---

# 6. 推荐自定义命令清单

## 6.1 `/spec-start`：启动新需求

### 使用场景

```text
用户只有一个需求想法，还没有完整设计。
```

### 适合输入

```text
/spec-start 我想给系统加一个批量导入用户功能
```

### 命令效果

```text
不写代码，先澄清需求，输出目标、边界、待确认问题、初版 Spec。
```

### 命令内容

```markdown
你现在启动 SDD 新需求流程。

规则：
1. 不允许直接写代码。
2. 先复述需求。
3. 再输出业务目标、技术目标、非目标。
4. 列出不确定点和待确认问题。
5. 输出初版 Spec。
6. 如果是存量项目，必须提示用户提供旧接口、旧表、旧模块路径。

输出格式：
## 需求复述
## 业务目标
## 技术目标
## 非目标
## 现状信息缺口
## 待确认问题
## 初版 Spec
## 下一步
```

---

## 6.2 `/existing-analyze`：存量项目现状分析

### 使用场景

```text
已有项目新增需求、修改旧接口、改老表、重构模块。
```

### 适合输入

```text
/existing-analyze 这是订单模块代码，请先分析现状
```

### 命令效果

```text
先分析旧模块、旧表、旧接口，不允许按新项目设计。
```

### 命令内容

```markdown
你现在进行存量项目现状分析。

规则：
1. 不允许输出最终实现方案。
2. 不允许默认重构。
3. 必须先识别已有模块、类、接口、表、配置、缓存、消息、定时任务。
4. 必须标注：复用、修改、新增、保持不变。
5. 必须列出风险和禁止改动范围。

输出格式：
## 当前模块结构
## 当前类职责
## 当前接口
## 当前数据库
## 当前配置 / 缓存 / 消息 / 任务
## 可复用内容
## 需要修改内容
## 禁止改动内容
## 风险点
## 需要用户补充的信息
```

---

## 6.3 `/spec-plan`：Spec 转任务计划

### 使用场景

```text
Spec 已经确认，需要拆成 AI 可执行任务。
```

### 适合输入

```text
/spec-plan 根据这个 Spec 拆开发任务
```

### 命令效果

```text
把需求拆成小任务，每个任务有文件路径、修改点、验证方式。
```

### 命令内容

```markdown
请根据已确认的 Spec 生成实现计划。

规则：
1. 每个任务必须足够小。
2. 每个任务必须有明确输入、输出、文件路径和验证方式。
3. 优先按垂直切片拆分。
4. 不允许一次性大改。
5. 如果某个任务依赖其他任务，必须标注依赖。

输出格式：
## 实现顺序
## 任务清单
### Task 1: 标题
- 文件：
- 修改内容：
- 验证方式：
- 依赖：
- 风险：
## 里程碑
## 暂停 Review 点
```

---

## 6.4 `/tdd-implement`：TDD 实现

### 使用场景

```text
实现业务逻辑、修复 Bug、修改校验、状态机、工具函数。
```

### 适合输入

```text
/tdd-implement 实现订单状态流转校验
```

### 命令效果

```text
先写失败测试，再写最小实现，再重构。
```

### 命令内容

```markdown
你现在按 TDD 流程实现。

规则：
1. 先不要写业务实现。
2. 先列出测试场景。
3. 先写一个失败测试。
4. 确认失败原因正确。
5. 写最小实现让测试通过。
6. 重构。
7. 再次运行测试。
8. 输出验证证据。
9. 不允许为了通过测试硬编码。

输出格式：
## 测试场景清单
## RED：失败测试
## GREEN：最小实现
## REFACTOR：重构说明
## 验证结果
## 未覆盖风险
```

---

## 6.5 `/bug-diagnose`：系统化诊断

### 使用场景

```text
测试失败、构建失败、线上异常、接口行为不符合预期。
```

### 适合输入

```text
/bug-diagnose 这个接口返回 500，日志如下...
```

### 命令效果

```text
不直接修，先复现、缩小范围、提出假设、验证假设、再修复。
```

### 命令内容

```markdown
请按系统化调试流程处理。

规则：
1. 不允许直接修改代码。
2. 先复述错误现象。
3. 给出最小复现路径。
4. 列出可能原因并按概率排序。
5. 为每个原因设计验证方法。
6. 定位明确后再提出修复方案。
7. 修复后必须补回归测试。

输出格式：
## 错误现象
## 最小复现
## 可能原因
## 验证计划
## 根因定位
## 修复方案
## 回归测试
## 防复发建议
```

---

## 6.6 `/review-diff`：提交前 Review

### 使用场景

```text
代码写完准备提交或提 PR。
```

### 适合输入

```text
/review-diff 请 review 当前改动
```

### 命令效果

```text
按正确性、可读性、可维护性、性能、安全性五轴检查 diff。
```

### 命令内容

```markdown
请对当前 diff 做提交前代码评审。

规则：
1. 只评审本次改动。
2. 不泛泛而谈。
3. 按 BLOCKER / IMPORTANT / NIT 分级。
4. 每个问题必须包含文件、位置、原因、建议。
5. 必须判断是否可以提交。
6. 必须检查是否影响旧逻辑。

检查维度：
- 正确性
- 可读性
- 可维护性
- 性能
- 安全性
- 测试覆盖
- 兼容性

输出格式：
## 总体结论
## BLOCKER
## IMPORTANT
## NIT
## 测试建议
## 是否可以提交
```

---

## 6.7 `/security-check`：安全审计

### 使用场景

```text
接口、权限、登录、支付、上传、导出、敏感数据处理。
```

### 适合输入

```text
/security-check 请审计这个接口是否有越权和敏感信息泄露
```

### 命令效果

```text
检查 SQL 注入、XSS、越权、敏感信息、硬编码密钥、日志泄露。
```

### 命令内容

```markdown
请对当前代码进行安全审计。

重点检查：
1. SQL 注入。
2. XSS。
3. 越权访问。
4. 权限绕过。
5. 敏感信息明文返回。
6. 日志泄露手机号、身份证、Token。
7. 硬编码密钥。
8. 文件上传风险。
9. 导出数据越权。
10. 第三方依赖安全风险。

输出格式：
## 安全结论
## 高危问题
## 中危问题
## 低危问题
## 修复建议
## 是否阻塞上线
```

---

## 6.8 `/ship-check`：上线检查

### 使用场景

```text
提测、发版、上线前、灰度前。
```

### 适合输入

```text
/ship-check 这个需求准备上线，帮我生成上线检查清单
```

### 命令效果

```text
输出发布步骤、配置、SQL、灰度、监控、回滚。
```

### 命令内容

```markdown
请生成上线检查与回滚方案。

必须包含：
1. 上线前检查。
2. SQL 执行顺序。
3. 配置项与默认值。
4. 灰度范围。
5. 发布步骤。
6. 线上验证步骤。
7. 监控指标。
8. 回滚步骤。
9. 回滚后验证。
10. 风险清单。

输出格式：
## 上线前检查
## 发布步骤
## 配置项
## 数据库变更
## 灰度策略
## 监控指标
## 回滚方案
## 上线后验证
## 风险与应对
```

---

## 6.9 `/memory-add`：沉淀经验

### 使用场景

```text
同一个问题被纠正两次、踩坑、事故复盘、团队约定变更。
```

### 适合输入

```text
/memory-add 以后不要再建议使用 Flyway，我们项目禁用了
```

### 命令效果

```text
把纠正沉淀为 Memory，后续 AI 自动遵守。
```

### 命令内容

```markdown
请把这次纠正沉淀为 Memory。

规则：
1. 不要只记一句话。
2. 必须写清 Why。
3. 必须写清 How to apply。
4. 必须写清触发场景。
5. 必须写清禁止事项。
6. 生成文件名建议。
7. 更新 MEMORY.md 索引建议。

输出格式：
## 文件名
## 类型
## 背景
## 规则
## Why
## How to apply
## 禁止事项
## MEMORY.md 索引行
```

---

# 7. 建议先安装和练习顺序

## 第一阶段：个人熟练，先别装太多

建议先练 5 个：

```text
/grill-with-docs
/spec
/plan
/tdd
/review
```

目标：

```text
先做到：不清楚不开写，写之前有 Spec，实现时有测试，提交前有 Review。
```

---

## 第二阶段：加入调试和上线

继续练：

```text
/diagnose
/ship
/security-check
/code-simplify
```

目标：

```text
能处理 Bug、上线、质量、复杂度。
```

---

## 第三阶段：团队工程化

沉淀：

```text
CLAUDE.md
AGENTS.md
.cursor/rules
.ai-spec/skills
.ai-spec/memory
hooks
ci
```

目标：

```text
让规则从“人提醒”变成“机制自动执行”。
```

---

# 8. 最推荐的落地组合

## 8.1 Cursor 项目

```text
Karpathy Guidelines → 放 .cursor/rules/karpathy.mdc
Addy Agent Skills → 选 spec、plan、build、test、review 规则化
Matt Skills → 重点抄 grill-with-docs、tdd、diagnose
Superpowers → 如果插件可用，用作完整工作流增强
```

## 8.2 Claude Code 项目

```text
Superpowers → 完整工作流
Matt Skills → 补充 grill、diagnose、architecture
Addy Skills → 生命周期命令
Karpathy Guidelines → 全局 CLAUDE.md 底层纪律
```

## 8.3 企业内部规范中心

```text
外部 Skills 不直接照搬。
先学习，再内化，再沉淀成团队版：
.ai-spec/skills/
.ai-spec/rules/
.ai-spec/commands/
.ai-spec/memory/
```

---

# 9. 团队版命令最小集

建议你的团队先做这 8 个命令：

```text
/spec-start          启动需求
/existing-analyze    存量现状分析
/spec-plan           拆计划
/tdd-implement       TDD 实现
/bug-diagnose        Bug 诊断
/review-diff         提交前评审
/ship-check          上线检查
/memory-add          经验沉淀
```

这 8 个命令基本覆盖：

```text
需求 → 现状 → 设计 → 实现 → 调试 → 评审 → 上线 → 沉淀
```

---

# 10. 最终建议

不要一开始就装满所有 Skills。

推荐策略：

```text
先用外部插件建立感觉
再抽象出团队常用命令
最后沉淀到 br-ai-spec / .ai-spec 体系
```

最小路径：

```text
第 1 周：练 /grill-with-docs、/spec、/tdd
第 2 周：加入 /review、/diagnose
第 3 周：加入 /ship、/memory-add
第 4 周：把高频流程固化成团队自定义 commands
```

最终目标不是“命令多”，而是：

> 每一个命令都代表团队的一条确定性工程流程。
