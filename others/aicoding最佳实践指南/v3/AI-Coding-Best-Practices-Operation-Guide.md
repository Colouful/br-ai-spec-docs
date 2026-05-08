# AI Coding 最佳实践操作指南

> 版本：V1.0  
> 适用对象：前端、后端、全栈、测试、架构、技术负责人  
> 适用工具：Claude Code、Cursor、Codex、GitHub Copilot、Gemini CLI、OpenCode、Windsurf  
> 参考体系：Superpowers、Matt Pocock Skills、Addy Osmani Agent Skills、Andrej Karpathy Guidelines、SDD、TDD、SPEC、Harness Engineering

---

## 1. 总体定位

AI Coding 的核心不是“让 AI 替你写代码”，而是建立一套可复用、可验证、可审计、可沉淀的工程协作机制。

推荐总流程：

```text
需求澄清 → Spec 规格 → Plan 计划 → TDD 实现 → Verify 验证 → Review 评审 → Ship 交付 → 经验沉淀
```

这套方法建议由四层组成：

| 层级 | 解决问题 | 核心产物 |
|---|---|---|
| SDD / SPEC | 让 AI 明确做什么、不做什么、如何验收 | PRD、Spec、Design、Tasks |
| TDD | 让 AI 生成的代码可验证、可回归 | 单测、集成测试、回归测试 |
| Skill | 把高频研发动作封装为可复用工作流 | `/spec`、`/plan`、`/tdd`、`/review` |
| Harness | 把规则固化到工程机制中 | CLAUDE.md、Rules、Hooks、CI 门禁 |

一句话总结：

> AI Coding 的最佳实践不是让 AI 更自由，而是让 AI 在 Spec、TDD、Skill、Hook、CI 的约束下更稳定地交付。

---

## 2. 四个 GitHub 项目的定位

| 项目 | 推荐用途 | 适合阶段 |
|---|---|---|
| `obra/superpowers` | 完整 AI Coding 工作流，强调 brainstorming、plan、TDD、subagent、review | 团队主流程 |
| `mattpocock/skills` | 面向真实工程师的轻量 Skill，强调 grill、diagnose、tdd、architecture | 日常研发 |
| `addyosmani/agent-skills` | 全生命周期工程 Skill，覆盖 define、plan、build、verify、review、ship | 企业级规范库 |
| `forrestchang/andrej-karpathy-skills` | Karpathy 风格 AI 代码行为约束，强调先思考、少改动、可验证目标 | 全局基础规则 |

推荐组合方式：

```text
Superpowers：作为主流程底座
Matt Pocock Skills：作为日常研发高频工具
Addy Osmani Agent Skills：作为企业级生命周期 Skill 库
Karpathy Guidelines：作为全局行为规则
```

---

## 3. 安装与初始化

---

## 3.0 四个项目 Skill 一键下载与安装指令

> 本节用于快速把四个 AI Coding 相关项目下载到本地，并按不同 Agent 工具完成 Skill / Plugin 安装。  
> 推荐先执行“本地下载脚本”，再根据你使用的工具执行 Claude Code、Cursor、Codex 或 Gemini 对应安装指令。

### 3.0.1 本地一键下载四个项目

适用场景：

```text
1. 想先把四个项目完整下载到本地学习
2. 想把 Skill 内容纳入团队规范中心
3. 想从本地复制 SKILL.md 到 .cursor/rules/、CLAUDE.md、AGENTS.md
4. 想后续统一维护自己的 AI Coding Skill 仓库
```

直接复制到终端执行：

```bash
#!/usr/bin/env bash
set -euo pipefail

SKILL_HOME="${HOME}/.ai-coding-skills"

echo "正在创建 AI Coding Skill 本地目录：${SKILL_HOME}"
mkdir -p "${SKILL_HOME}"
cd "${SKILL_HOME}"

clone_or_update() {
  local repo_url="$1"
  local dir_name="$2"

  if [ -d "${dir_name}/.git" ]; then
    echo "正在更新：${dir_name}"
    git -C "${dir_name}" pull --ff-only
  else
    echo "正在下载：${dir_name}"
    git clone --depth=1 "${repo_url}" "${dir_name}"
  fi
}

clone_or_update "https://github.com/obra/superpowers.git" "superpowers"
clone_or_update "https://github.com/mattpocock/skills.git" "mattpocock-skills"
clone_or_update "https://github.com/addyosmani/agent-skills.git" "addyosmani-agent-skills"
clone_or_update "https://github.com/forrestchang/andrej-karpathy-skills.git" "andrej-karpathy-skills"

echo ""
echo "四个项目已经下载完成。"
echo "本地目录：${SKILL_HOME}"
echo ""
echo "目录清单："
ls -la "${SKILL_HOME}"
```

下载完成后的本地目录：

```text
~/.ai-coding-skills/
├── superpowers/
├── mattpocock-skills/
├── addyosmani-agent-skills/
└── andrej-karpathy-skills/
```

后续更新四个项目：

```bash
cd ~/.ai-coding-skills

for dir in superpowers mattpocock-skills addyosmani-agent-skills andrej-karpathy-skills; do
  if [ -d "${dir}/.git" ]; then
    echo "正在更新：${dir}"
    git -C "${dir}" pull --ff-only
  fi
done

echo "全部更新完成。"
```

---

### 3.0.2 Claude Code 推荐安装指令

适用场景：

```text
你主要使用 Claude Code 进行真实项目开发，希望直接安装可用的 Plugin / Skill。
```

在 Claude Code 中逐条执行：

```text
/plugin install superpowers@claude-plugins-official
```

```text
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace
```

```text
/plugin marketplace add addyosmani/agent-skills
/plugin install agent-skills@addy-agent-skills
```

如果 Addy Osmani Agent Skills 因 SSH 拉取失败，改用 HTTPS：

```text
/plugin marketplace add https://github.com/addyosmani/agent-skills.git
/plugin install agent-skills@addy-agent-skills
```

```text
/plugin marketplace add forrestchang/andrej-karpathy-skills
/plugin install andrej-karpathy-skills@karpathy-skills
```

Matt Pocock Skills 推荐通过 `npx skills` 安装：

```bash
npx skills@latest add mattpocock/skills
```

安装时务必选择：

```text
/setup-matt-pocock-skills
```

然后在 Claude Code 中执行：

```text
/setup-matt-pocock-skills
```

推荐安装后的 Claude Code 使用顺序：

```text
/grill-with-docs
→ /spec
→ /plan
→ /tdd
→ /build
→ /test
→ /review
→ /ship
```

---

### 3.0.3 Cursor 推荐安装指令

适用场景：

```text
你主要使用 Cursor，希望把 Skill 固化为项目规则。
```

先在 Cursor Agent 中安装 Superpowers：

```text
/add-plugin superpowers
```

然后在项目根目录执行：

```bash
mkdir -p .cursor/rules

cp ~/.ai-coding-skills/andrej-karpathy-skills/.cursor/rules/karpathy-guidelines.mdc .cursor/rules/karpathy-guidelines.mdc 2>/dev/null || true

cp ~/.ai-coding-skills/addyosmani-agent-skills/skills/spec-driven-development/SKILL.md .cursor/rules/spec-driven-development.mdc
cp ~/.ai-coding-skills/addyosmani-agent-skills/skills/planning-and-task-breakdown/SKILL.md .cursor/rules/planning-and-task-breakdown.mdc
cp ~/.ai-coding-skills/addyosmani-agent-skills/skills/test-driven-development/SKILL.md .cursor/rules/test-driven-development.mdc
cp ~/.ai-coding-skills/addyosmani-agent-skills/skills/frontend-ui-engineering/SKILL.md .cursor/rules/frontend-ui-engineering.mdc
cp ~/.ai-coding-skills/addyosmani-agent-skills/skills/api-and-interface-design/SKILL.md .cursor/rules/api-and-interface-design.mdc
cp ~/.ai-coding-skills/addyosmani-agent-skills/skills/code-review-and-quality/SKILL.md .cursor/rules/code-review-and-quality.mdc

echo "Cursor Rules 已写入 .cursor/rules/"
```

建议额外创建项目主规则：

```bash
cat > .cursor/rules/project-ai-coding.mdc <<'EOF'
---
description: 项目 AI Coding 主规则
alwaysApply: true
---

# 项目 AI Coding 主规则

## 核心原则

1. 先澄清，再编码。
2. 先写 Spec，再写实现。
3. 先写测试，再写业务代码。
4. 只修改和任务直接相关的代码。
5. 不允许无关重构。
6. 不允许硬编码环境地址、Token、密钥。
7. 所有用户可见英文提示必须改为中文。
8. 完成前必须运行验证命令。

## 标准流程

需求澄清 → Spec 规格 → Plan 计划 → TDD 实现 → Verify 验证 → Review 评审 → Ship 交付。

## 前端要求

1. 页面必须覆盖 Loading、Empty、Error 状态。
2. 表单必须有校验规则和提交中状态。
3. API 类型必须单独定义。
4. 接口调用必须走统一 API 封装。
5. 禁止在组件内散落接口路径。
6. 禁止直接在业务组件中写复杂数据转换逻辑。

## 验证要求

完成前必须根据项目技术栈运行对应命令，例如：

```bash
pnpm lint
pnpm typecheck
pnpm test
pnpm build
```
EOF

echo "项目 AI Coding 主规则已创建：.cursor/rules/project-ai-coding.mdc"
```

---

### 3.0.4 Codex 推荐安装与使用指令

适用场景：

```text
你主要使用 Codex CLI / Codex App，希望先启用 Superpowers，再通过 AGENTS.md 统一项目规则。
```

在 Codex CLI 中执行：

```text
/plugins
```

搜索并安装：

```text
superpowers
```

然后在项目根目录创建 `AGENTS.md`：

```bash
cat > AGENTS.md <<'EOF'
# 项目 AI Coding 规则

## 工作方式

你是一个受工程规范约束的 AI Coding Agent。你不能直接进入编码阶段，必须先完成需求澄清、规格设计、任务拆分和验证方案。

## 必须遵守

1. 先澄清，再编码。
2. 先写 Spec，再写实现。
3. 先写测试，再写业务代码。
4. 只修改与当前任务直接相关的代码。
5. 不允许无关重构。
6. 不允许硬编码 localhost、127.0.0.1、Token、密钥。
7. 所有用户可见英文提示必须改为中文。
8. 完成前必须运行测试、类型检查、Lint 和构建。

## 推荐流程

/grill-with-docs
→ /spec
→ /plan
→ /tdd
→ /build
→ /test
→ /review
→ /ship
EOF

echo "AGENTS.md 已创建完成。"
```

---

### 3.0.5 Gemini CLI 推荐安装指令

适用场景：

```text
你使用 Gemini CLI，希望安装 Addy Osmani Agent Skills 和 Superpowers。
```

安装 Superpowers：

```bash
gemini extensions install https://github.com/obra/superpowers
```

更新 Superpowers：

```bash
gemini extensions update superpowers
```

安装 Addy Osmani Agent Skills：

```bash
gemini skills install https://github.com/addyosmani/agent-skills.git --path skills
```

如果已经执行过本地下载，也可以从本地安装：

```bash
gemini skills install ~/.ai-coding-skills/addyosmani-agent-skills/skills/
```

---

### 3.0.6 项目级一键初始化脚本

适用场景：

```text
你已经下载四个项目，现在希望在当前业务项目里快速初始化 AI Coding 规范文件。
```

在业务项目根目录执行：

```bash
#!/usr/bin/env bash
set -euo pipefail

echo "正在初始化项目级 AI Coding 规范..."

mkdir -p .cursor/rules
mkdir -p docs/specs
mkdir -p docs/adr
mkdir -p docs/ai-coding

if [ ! -f "CLAUDE.md" ]; then
  cat > CLAUDE.md <<'EOF'
# 项目 AI Coding 规则

## 核心原则

1. 先澄清，再编码。
2. 先写 Spec，再写实现。
3. 先写测试，再写业务代码。
4. 只修改和任务直接相关的代码。
5. 不允许无关重构。
6. 不允许硬编码环境地址、Token、密钥。
7. 所有用户可见英文提示必须改为中文。
8. 完成前必须运行验证命令。

## 标准流程

需求澄清 → Spec 规格 → Plan 计划 → TDD 实现 → Verify 验证 → Review 评审 → Ship 交付。

## 验证要求

根据项目技术栈执行对应验证命令：

- 前端：pnpm lint、pnpm typecheck、pnpm test、pnpm build
- Java：mvn test、mvn verify
- Go：go test ./...
- Rust：cargo test、cargo clippy -- -D warnings
- Python：pytest、ruff check .、mypy .
EOF
fi

if [ ! -f "CONTEXT.md" ]; then
  cat > CONTEXT.md <<'EOF'
# 项目上下文

## 业务背景

请在这里补充项目的业务背景。

## 领域术语

| 术语 | 含义 |
|---|---|
| 示例术语 | 示例说明 |

## 技术栈

| 模块 | 技术 |
|---|---|
| 前端 | 待补充 |
| 后端 | 待补充 |
| 数据库 | 待补充 |
| 中间件 | 待补充 |

## 常见约束

1. 待补充。
EOF
fi

if [ ! -f "AGENTS.md" ]; then
  cat > AGENTS.md <<'EOF'
# Agent 协作规则

## 角色定位

你是项目中的 AI Coding Agent，必须严格遵守项目规范、测试策略和质量门禁。

## 禁止事项

1. 禁止在没有 Spec 的情况下直接实现复杂需求。
2. 禁止无关重构。
3. 禁止删除不理解的代码。
4. 禁止引入未知依赖。
5. 禁止跳过测试。
6. 禁止硬编码敏感配置。

## 完成标准

1. 需求符合 Spec。
2. 测试通过。
3. 类型检查通过。
4. Lint 通过。
5. 构建通过。
6. 输出影响范围和回滚方案。
EOF
fi

cat > .cursor/rules/project-ai-coding.mdc <<'EOF'
---
description: 项目 AI Coding 主规则
alwaysApply: true
---

# 项目 AI Coding 主规则

1. 先澄清，再编码。
2. 先写 Spec，再写实现。
3. 先写测试，再写业务代码。
4. 只修改和任务直接相关的代码。
5. 不允许无关重构。
6. 所有用户可见英文提示必须改为中文。
7. 完成前必须运行验证命令。
EOF

cat > docs/ai-coding/workflow.md <<'EOF'
# AI Coding 标准工作流

```text
需求澄清 → Spec 规格 → Plan 计划 → TDD 实现 → Verify 验证 → Review 评审 → Ship 交付 → 经验沉淀
```

## 新需求

```text
/grill-with-docs
→ /spec
→ /plan
→ /tdd
→ /build
→ /test
→ /review
→ /ship
```

## Bug 修复

```text
/diagnose
→ 写回归测试
→ 最小修复
→ /test
→ /review
→ /ship
```

## 重构

```text
/zoom-out
→ /improve-codebase-architecture
→ /plan
→ /tdd
→ /review
```
EOF

echo "项目级 AI Coding 规范初始化完成。"
echo "已生成：CLAUDE.md、CONTEXT.md、AGENTS.md、.cursor/rules/project-ai-coding.mdc、docs/ai-coding/workflow.md"
```

---

### 3.0.7 推荐执行顺序

```text
第一步：执行 3.0.1，本地下载四个项目
第二步：根据使用工具执行 3.0.2 / 3.0.3 / 3.0.4 / 3.0.5
第三步：进入业务项目根目录，执行 3.0.6 初始化项目规则
第四步：新需求统一走 /grill-with-docs → /spec → /plan → /tdd → /review
第五步：把真实踩坑继续沉淀进 CLAUDE.md、CONTEXT.md、.cursor/rules 和 docs/ai-coding
```



### 3.1 安装 Superpowers

#### Claude Code 官方市场安装

```bash
/plugin install superpowers@claude-plugins-official
```

#### Claude Code 自定义市场安装

```bash
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace
```

#### Cursor 安装

```bash
/add-plugin superpowers
```

#### Codex CLI 安装

```text
在 Codex CLI 中执行 /plugins，然后搜索 superpowers 并安装
```

---

### 3.2 安装 Matt Pocock Skills

```bash
npx skills@latest add mattpocock/skills
```

安装时选择需要安装到哪些 coding agent，并确保选择：

```bash
/setup-matt-pocock-skills
```

安装完成后，在 Agent 中执行：

```bash
/setup-matt-pocock-skills
```

初始化会询问：

```text
1. 使用 GitHub、Linear 还是本地文件作为任务系统
2. triage 标签如何设置
3. CONTEXT.md、ADR、Issue 文档存放在哪里
```

---

### 3.3 安装 Addy Osmani Agent Skills

#### Claude Code Marketplace 安装

```bash
/plugin marketplace add addyosmani/agent-skills
/plugin install agent-skills@addy-agent-skills
```

#### SSH 不可用时使用 HTTPS

```bash
/plugin marketplace add https://github.com/addyosmani/agent-skills.git
/plugin install agent-skills@addy-agent-skills
```

#### 本地开发方式

```bash
git clone https://github.com/addyosmani/agent-skills.git
claude --plugin-dir /path/to/agent-skills
```

#### Cursor 使用方式

```text
将需要的 SKILL.md 复制到 .cursor/rules/，或在 Cursor 规则中引用 skills 目录。
```

---

### 3.4 安装 Karpathy Guidelines

#### Claude Code 插件方式

```bash
/plugin marketplace add forrestchang/andrej-karpathy-skills
/plugin install andrej-karpathy-skills@karpathy-skills
```

#### 单项目 CLAUDE.md 方式

新项目：

```bash
curl -o CLAUDE.md https://raw.githubusercontent.com/forrestchang/andrej-karpathy-skills/main/CLAUDE.md
```

已有项目追加：

```bash
echo "" >> CLAUDE.md
curl https://raw.githubusercontent.com/forrestchang/andrej-karpathy-skills/main/CLAUDE.md >> CLAUDE.md
```

---

## 4. 推荐项目目录结构

```text
project-root/
├── CLAUDE.md
├── CONTEXT.md
├── AGENTS.md
├── .cursor/
│   └── rules/
│       ├── project.mdc
│       ├── frontend.mdc
│       └── testing.mdc
├── docs/
│   ├── specs/
│   │   └── feature-x/
│   │       ├── 01-proposal.md
│   │       ├── 02-design.md
│   │       ├── 03-tasks.md
│   │       └── 04-acceptance.md
│   ├── adr/
│   │   └── 0001-xxx.md
│   └── ai-coding/
│       ├── best-practices.md
│       ├── prompts.md
│       └── scenarios.md
├── scripts/
│   ├── ai-quality-check.js
│   └── check-no-debug-code.js
└── .github/
    └── workflows/
        └── quality-gate.yml
```

目录职责说明：

| 文件 / 目录 | 作用 |
|---|---|
| `CLAUDE.md` | Claude Code 项目级规则 |
| `CONTEXT.md` | 业务术语、领域语言、常见缩写 |
| `AGENTS.md` | 通用 Agent 指令，可兼容 Codex / OpenCode |
| `.cursor/rules/*.mdc` | Cursor 项目规则 |
| `docs/specs/` | 每个需求的规格、设计、任务和验收文档 |
| `docs/adr/` | 架构决策记录 |
| `scripts/` | 自动化质量检查脚本 |
| `.github/workflows/` | CI 质量门禁 |

---

## 5. 命令与 Skill 模块速查

### 5.1 需求澄清类

| 命令 / Skill | 来源 | 使用场景 |
|---|---|---|
| `/grill-me` | Matt Pocock | 想法模糊，需要 Agent 反复追问 |
| `/grill-with-docs` | Matt Pocock | 工程需求澄清，同时生成 CONTEXT.md 和 ADR |
| `idea-refine` | Addy Osmani | 从发散想法收敛为具体提案 |
| `/spec` | Addy Osmani | 生成 PRD / Spec / 边界 / 验收标准 |

推荐提示词：

```markdown
你先不要写代码。

请先以资深技术负责人视角，围绕这个需求进行澄清。
要求：
1. 每次只问一个关键问题
2. 优先追问业务目标、边界、不做什么、异常情况、验收标准
3. 问完后生成一份 Spec 文档
4. Spec 必须包含目标、范围、非目标、用户流程、数据结构、接口契约、测试策略、验收标准

需求如下：
【粘贴需求】
```

---

### 5.2 计划拆分类

| 命令 / Skill | 来源 | 使用场景 |
|---|---|---|
| `/plan` | Addy Osmani | 将 Spec 拆成小任务 |
| `writing-plans` | Superpowers | 写详细执行计划 |
| `/to-issues` | Matt Pocock | 将需求拆成 GitHub / Linear / 本地 Issue |
| `using-git-worktrees` | Superpowers | 为任务创建隔离分支 / worktree |

任务拆分标准：

```text
每个任务 2 - 5 分钟可完成
每个任务必须有明确文件路径
每个任务必须有验证方式
每个任务必须能独立提交
禁止一个任务横跨过多模块
```

任务模板：

```markdown
## Task 1：新增事件字典查询接口

### 修改文件
- src/api/eventDictionary.ts
- src/types/eventDictionary.ts

### 修改内容
- 新增查询接口封装
- 定义请求参数和响应类型
- 统一错误处理

### 验证方式
- pnpm test src/api/eventDictionary.test.ts
- pnpm typecheck
- pnpm lint

### 验收标准
- 能根据 websiteId 查询事件字典
- 空数据返回空数组
- 接口异常有统一错误提示
```

---

### 5.3 编码实现类

| 命令 / Skill | 来源 | 使用场景 |
|---|---|---|
| `/tdd` | Matt / Addy / Superpowers | 新功能、Bug 修复、行为变更 |
| `/build` | Addy Osmani | 增量实现，一个垂直切片一次提交 |
| `subagent-driven-development` | Superpowers | 可并行任务，多 Agent 分工 |
| `context-engineering` | Addy Osmani | 上下文不足、输出质量下降、跨文件修改 |

TDD 标准循环：

```text
RED：先写失败测试
GREEN：写最少代码让测试通过
REFACTOR：重构但不改变行为
COMMIT：小步提交
```

TDD 提示词：

```markdown
请严格按照 TDD 执行。

要求：
1. 先写一个失败测试，不允许直接写实现代码
2. 运行测试，确认失败原因符合预期
3. 只写让当前测试通过的最小实现
4. 测试通过后再进行必要重构
5. 每一步都说明验证命令和结果
```

---

### 5.4 验证评审类

| 命令 / Skill | 来源 | 使用场景 |
|---|---|---|
| `/test` | Addy Osmani | 证明功能可运行 |
| `/diagnose` | Matt Pocock | Bug、构建失败、性能回退 |
| `systematic-debugging` | Superpowers | 四阶段根因分析 |
| `/review` | Addy Osmani | 合并前质量评审 |
| `/code-simplify` | Addy Osmani | 代码过度复杂，需要简化 |
| `/ship` | Addy Osmani | 发布上线前最终检查 |

验证清单：

```text
□ 单元测试通过
□ 集成测试通过
□ 类型检查通过
□ Lint 通过
□ 构建通过
□ 无 console.log / debugger
□ 无硬编码地址、Token、密钥
□ 边界场景覆盖
□ 错误场景覆盖
□ 回归测试覆盖
```

---

## 6. 标准开发流程

### 6.1 阶段一：DEFINE，定义需求

适合场景：

```text
“我要做一个 XX 功能”
“这个页面想优化一下”
“这个接口要支持新的业务规则”
```

操作流程：

```text
/grill-me
→ /grill-with-docs
→ /spec
```

产出物：

```text
docs/specs/feature-x/01-proposal.md
docs/specs/feature-x/02-design.md
CONTEXT.md
docs/adr/0001-feature-x.md
```

---

### 6.2 阶段二：PLAN，拆分计划

操作流程：

```text
/spec
→ /plan
→ /to-issues
```

计划文档必须包含：

```text
1. 需求背景
2. 当前系统现状
3. 修改范围
4. 不修改范围
5. 任务拆分
6. 文件路径
7. 验证命令
8. 风险点
9. 回滚方案
```

---

### 6.3 阶段三：BUILD，TDD 实现

标准要求：

```text
1. 不写产品代码，除非是为了让失败的测试通过
2. 不写更多测试代码，刚好够一个失败即可
3. 只写刚好够让当前失败测试通过的最少产品代码
4. 每次改动必须能验证
5. 每个垂直切片完成后提交
```

---

### 6.4 阶段四：VERIFY，验证功能

前端场景增加：

```text
□ 浏览器 Console 无错误
□ Network 请求符合预期
□ 页面刷新、返回、权限变化正常
□ Loading / Empty / Error 状态完整
□ 表单校验完整
□ 移动端或低版本浏览器兼容性确认
```

后端场景增加：

```text
□ 接口契约未漂移
□ 错误码语义明确
□ 权限校验完整
□ 幂等处理完整
□ 数据库事务边界清晰
□ 日志不包含敏感信息
□ 慢查询风险已评估
```

---

### 6.5 阶段五：REVIEW，评审代码

评审维度：

| 维度 | 检查内容 |
|---|---|
| 正确性 | 是否满足 Spec，边界是否完整 |
| 可读性 | 命名、结构、注释是否清晰 |
| 可维护性 | 是否引入不必要复杂度 |
| 安全性 | 是否有注入、越权、密钥泄露 |
| 性能 | 是否有明显重复请求、重复渲染、大对象拷贝 |
| 兼容性 | 是否影响旧业务、旧数据、旧浏览器 |
| 可回滚 | 是否有灰度、开关、兼容策略 |

---

### 6.6 阶段六：SHIP，交付上线

发布前要求：

```text
□ PR 描述清楚
□ 关联 Spec / Issue / ADR
□ 测试截图或测试日志完整
□ 数据库变更已审查
□ 配置变更已审查
□ 回滚方案明确
□ 监控指标明确
□ 上线后验证步骤明确
```

发布说明模板：

```markdown
## 本次变更

### 需求背景
【说明为什么做】

### 核心改动
- 【改动 1】
- 【改动 2】

### 影响范围
- 页面：
- 接口：
- 数据表：
- 配置项：

### 验证记录
- 单元测试：
- 类型检查：
- 构建：
- 手工验证：

### 回滚方案
【说明如何回滚】

### 风险点
【说明潜在风险和观察指标】
```

---

## 7. 真实开发场景操作手册

### 场景一：模糊想法变成可开发需求

典型输入：

```text
我想做一个 AI 埋点查询功能，用户可以自然语言查询页面浏览量。
```

推荐流程：

```text
/grill-me
→ idea-refine
→ /spec
→ /plan
```

提示词：

```markdown
你先不要直接写方案。

请通过连续追问帮我把这个想法变成可开发需求。
重点追问：
1. 用户是谁
2. 要解决什么业务问题
3. 输入是什么
4. 输出是什么
5. 哪些情况不做
6. 成功标准是什么
7. 第一版最小可交付范围是什么
```

---

### 场景二：前端页面开发

适合：

```text
Vue 3 + Vite + Arco Design 页面
React + Ant Design 页面
后台管理列表页
表单弹窗
详情页
```

推荐流程：

```text
/spec
→ frontend-ui-engineering
→ /plan
→ /build
→ browser-testing-with-devtools
→ /review
```

页面 Spec 必须包含：

```text
组件树
状态流
接口依赖
权限规则
Loading / Empty / Error
分页 / 排序 / 筛选
表单校验
埋点要求
浏览器验证方式
```

前端提示词：

```markdown
请按企业级前端开发标准实现该页面。

要求：
1. 先输出组件结构和状态设计，不要直接写代码
2. 明确接口请求、错误处理、空状态、加载状态
3. 明确表单校验和权限控制
4. 按垂直切片实现，每次只实现一个可验证的小功能
5. 所有英文提示文案改为中文
6. 最后输出验证命令和浏览器验证清单
```

---

### 场景三：API / 接口设计

推荐流程：

```text
api-and-interface-design
→ /spec
→ /tdd
→ /review
```

接口 Spec 必须包含：

```text
接口路径
请求方法
请求参数
响应结构
错误码
权限规则
幂等策略
限流策略
兼容策略
测试用例
```

提示词：

```markdown
请按 Contract-First 方式设计接口。

要求：
1. 先定义请求和响应契约
2. 明确错误码和错误语义
3. 明确权限、幂等、限流、兼容策略
4. 先写接口测试，再实现接口
5. 不允许为了当前实现随意改变契约
```

---

### 场景四：Bug 修复

错误做法：

```text
报错了，帮我修一下。
```

正确做法：

```text
/diagnose
→ 复现
→ 最小化
→ 定位
→ 写回归测试
→ 修复
→ 验证
```

提示词：

```markdown
请先不要修改代码。

请按系统化调试流程处理：
1. 复现问题
2. 最小化问题范围
3. 提出可能原因
4. 通过日志、断点或测试验证假设
5. 找到根因后，先写一个失败的回归测试
6. 再写最小修复代码
7. 最后运行完整验证
```

---

### 场景五：重构一个模块

推荐流程：

```text
/zoom-out
→ /improve-codebase-architecture
→ /spec
→ /plan
→ /tdd
→ /review
```

重构前必须确认：

```text
当前行为是什么
有哪些测试保护
哪些代码不能碰
是否需要兼容旧接口
是否需要迁移数据
是否可分阶段上线
```

提示词：

```markdown
请先从系统视角解释这个模块。

要求：
1. 说明当前模块职责、依赖关系和数据流
2. 找出复杂度最高的部分
3. 给出不改变外部行为的重构方案
4. 每一步都必须有测试保护
5. 禁止顺手重构无关代码
6. 每次改动控制在一个小提交内
```

---

### 场景六：多栈协同开发

适合：

```text
前端 React / Vue
后端 Java / Go / Python / Rust
数据库 MySQL / PostgreSQL
中间件 Redis / Kafka / Nacos
```

推荐机制：

```text
CONTEXT.md 统一业务语言
OpenAPI / JSON Schema 统一接口契约
CLAUDE.md 统一项目规则
Sub-agent 并行审查不同栈
Hook / CI 检查契约漂移
```

多栈开发需要重点防范：

```text
1. 注意力被切碎
2. 跨栈契约漂移
3. 同一个坑重复踩
4. 长任务中途断档
5. 多 Agent 并发修改冲突
```

---

### 场景七：紧急热修复

热修复不适合完整大流程，但不能无规范。

推荐轻量流程：

```text
diagnose
→ 写回归测试
→ 最小修复
→ review
→ ship
→ 事后补 Spec
```

提示词：

```markdown
这是一个紧急修复任务，请使用轻量流程。

要求：
1. 先定位根因
2. 只修改导致问题的最小代码
3. 禁止顺手重构
4. 必须补一个回归测试
5. 输出上线验证步骤和回滚方案
6. 修复后补充 Spec 记录
```

---

## 8. 团队级质量门禁

### 8.1 AI 开发前门禁

```text
□ 当前分支干净
□ 需求已经有 Spec
□ 禁止修改范围已声明
□ 验收标准已明确
□ 测试命令已明确
□ 风险等级已判断
```

风险分级建议：

| 风险等级 | 适合方式 | 示例 |
|---|---|---|
| 低风险 | Agent 主导 | UI 样式、CRUD 页面、文案调整 |
| 中风险 | AI 辅助，人主导审查 | 业务接口、状态流、权限判断 |
| 高风险 | 人主导，AI 辅助参考 | 支付、认证、加密、数据迁移、权限系统 |

---

### 8.2 AI 开发中门禁

```text
□ 一次只做一个任务
□ 一次只做一个垂直切片
□ 不允许无关重构
□ 不允许删除不理解的代码
□ 不允许引入未知依赖
□ 不允许硬编码环境地址
□ 不允许跳过测试
```

---

### 8.3 AI 开发后门禁

前端项目：

```bash
pnpm lint
pnpm typecheck
pnpm test
pnpm build
```

Java 项目：

```bash
mvn test
mvn verify
```

Go 项目：

```bash
go test ./...
```

Rust 项目：

```bash
cargo test
cargo clippy -- -D warnings
```

Python 项目：

```bash
pytest
ruff check .
mypy .
```

PR 必须包含：

```text
Spec 链接
变更摘要
影响范围
测试结果
风险说明
回滚方案
截图或日志
```

---

## 9. CLAUDE.md / Cursor Rules 推荐内容

```markdown
# 项目 AI Coding 规则

## 一、核心原则

1. 先澄清，再编码
2. 先写 Spec，再写实现
3. 先写测试，再写业务代码
4. 只修改和任务直接相关的代码
5. 不允许无关重构
6. 不允许硬编码环境地址、Token、密钥
7. 所有用户可见英文提示必须改为中文
8. 所有接口调用必须走统一 API 封装
9. 所有错误必须有明确中文提示
10. 完成前必须运行验证命令

## 二、前端规则

1. Vue 组件使用组合式 API
2. React 组件优先函数组件和 Hooks
3. 表格页面必须包含 Loading、Empty、Error 状态
4. 表单必须有校验规则和提交中状态
5. API 类型必须单独定义
6. 禁止在组件内散落接口路径
7. 禁止直接在业务组件中写复杂数据转换逻辑

## 三、测试规则

1. 行为变更必须补测试
2. Bug 修复必须先补回归测试
3. 测试名称必须描述业务行为
4. 不测试实现细节
5. 不为了通过测试删除有效断言

## 四、提交规则

1. 小步提交
2. 每个提交必须可构建
3. PR 必须说明影响范围和验证结果
4. 涉及配置、权限、数据库、接口契约的变更必须单独说明
```

---

## 10. Git Hooks 与 CI 门禁示例

### 10.1 pre-commit 示例

```bash
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

echo "正在执行 AI Coding 提交前质量检查..."

pnpm lint
pnpm typecheck
pnpm test

node scripts/check-no-debug-code.js

echo "质量检查通过，可以提交。"
```

### 10.2 禁止调试代码脚本示例

```js
const fs = require('fs')
const path = require('path')

const ROOT = process.cwd()
const EXTENSIONS = ['.js', '.jsx', '.ts', '.tsx', '.vue']
const FORBIDDEN_PATTERNS = [
  'console.log',
  'debugger',
  '127.0.0.1',
  'localhost'
]

function walk(dir, files = []) {
  const entries = fs.readdirSync(dir, { withFileTypes: true })

  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name)

    if (entry.isDirectory()) {
      if (['node_modules', '.git', 'dist', 'build'].includes(entry.name)) {
        continue
      }
      walk(fullPath, files)
      continue
    }

    if (EXTENSIONS.includes(path.extname(entry.name))) {
      files.push(fullPath)
    }
  }

  return files
}

const files = walk(ROOT)
let hasError = false

for (const file of files) {
  const content = fs.readFileSync(file, 'utf8')

  for (const pattern of FORBIDDEN_PATTERNS) {
    if (content.includes(pattern)) {
      console.error(`发现禁止内容：${pattern}`)
      console.error(`文件路径：${file}`)
      hasError = true
    }
  }
}

if (hasError) {
  console.error('提交失败，请先移除调试代码或硬编码地址。')
  process.exit(1)
}

console.log('未发现调试代码或硬编码地址。')
```

### 10.3 GitHub Actions 示例

```yaml
name: 质量门禁

on:
  pull_request:
    branches:
      - main
      - master
      - dev

jobs:
  quality:
    runs-on: ubuntu-latest

    steps:
      - name: 拉取代码
        uses: actions/checkout@v4

      - name: 安装 Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20

      - name: 安装 pnpm
        uses: pnpm/action-setup@v4
        with:
          version: 9

      - name: 安装依赖
        run: pnpm install --frozen-lockfile

      - name: 执行 Lint
        run: pnpm lint

      - name: 执行类型检查
        run: pnpm typecheck

      - name: 执行测试
        run: pnpm test

      - name: 执行构建
        run: pnpm build
```

---

## 11. 一套推荐日常工作流

### 新需求

```text
/grill-with-docs
→ /spec
→ /plan
→ /tdd
→ /build
→ /test
→ /review
→ /ship
```

### Bug 修复

```text
/diagnose
→ 写回归测试
→ 最小修复
→ /test
→ /review
→ /ship
```

### 前端页面

```text
/spec
→ frontend-ui-engineering
→ /plan
→ /build
→ browser-testing-with-devtools
→ /review
```

### 接口开发

```text
api-and-interface-design
→ /spec
→ /tdd
→ /review
→ /ship
```

### 重构

```text
/zoom-out
→ /improve-codebase-architecture
→ /plan
→ /tdd
→ /review
```

### 多 Agent 并行

```text
/spec
→ /plan
→ 切分独立任务
→ 每个任务一个 Sub-agent
→ 主 Agent 汇总
→ 统一 review
→ 统一验证
```

---

## 12. 常见反模式

| 反模式 | 问题 | 正确做法 |
|---|---|---|
| 直接让 AI 写代码 | 需求模糊，容易跑偏 | 先 `/grill-me`，再 `/spec` |
| 一次让 AI 改很多文件 | 注意力衰减，容易遗漏约束 | 拆成 2 - 5 分钟任务 |
| 没有测试就接受代码 | 无法证明正确 | TDD 或至少补充回归测试 |
| Agent 报错后反复猜修 | 越改越乱 | `/diagnose` 系统化定位 |
| AI 顺手重构 | 影响范围不可控 | 外科手术式修改 |
| 文档和代码脱节 | Spec 漂移 | PR 必须同步更新 Spec |
| 依赖人肉检查 | 容易遗漏 | Hook + CI 固化门禁 |
| 只看生成速度 | 技术债累积 | 看交付质量、返工率、回归率 |

---

## 13. 团队落地路线

### 第一阶段：个人熟练使用

目标：

```text
每个开发者能够熟练使用 /grill、/spec、/plan、/tdd、/review。
```

动作：

```text
1. 安装 Matt Pocock Skills
2. 安装 Addy Osmani Agent Skills
3. 安装 Karpathy Guidelines
4. 每个需求强制产出 Spec 和 Plan
5. Bug 修复强制补回归测试
```

---

### 第二阶段：项目级规范沉淀

目标：

```text
每个项目都有统一 Agent 规则和上下文。
```

动作：

```text
1. 增加 CLAUDE.md
2. 增加 .cursor/rules/*.mdc
3. 增加 CONTEXT.md
4. 增加 docs/specs/
5. 增加 docs/adr/
6. 增加提交前质量检查脚本
```

---

### 第三阶段：团队级 Harness 固化

目标：

```text
把 AI Coding 从个人经验升级为团队工程体系。
```

动作：

```text
1. 建立统一 AI Coding 规范中心
2. 建立通用 Skill 库
3. 建立项目模板
4. 建立 Hook / CI 门禁
5. 建立度量体系
6. 建立复盘机制
```

核心度量指标：

```text
AI 代码采纳率
需求交付周期
Bug 回归率
PR 返工次数
测试覆盖率
Spec 完整率
门禁拦截次数
人工干预次数
```

---

## 14. 最终建议

建议优先按照下面顺序落地：

```text
1. 先安装并熟练使用四个开源项目的核心 Skill
2. 在一个真实项目中建立 CLAUDE.md、CONTEXT.md、docs/specs/
3. 新需求强制走 /grill-with-docs → /spec → /plan → /tdd
4. Bug 修复强制走 /diagnose → 回归测试 → 最小修复
5. 提交前强制跑 lint、typecheck、test、build
6. 将踩过的坑沉淀到 Memory、Rules、Hooks、CI
```

最终目标：

> 让 AI 不再只是会写代码，而是能在团队规则、工程纪律、质量门禁、测试验证和复盘机制下稳定交付。
