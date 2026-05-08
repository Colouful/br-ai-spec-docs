# AI Coding 最佳实践操作指南：本机全局安装低心智版

> 版本：V3.0  
> 修正重点：安装到用户电脑本地，不安装到具体项目目录。  
> 目标：Claude Code 和 Cursor 都可以复用同一套本机 AI Coding Skill 资产。  
> 使用方式：复制本文中的“AI 可执行指令”给 Claude Code / Cursor Agent / Codex / Gemini CLI，让 AI 自己完成本机安装与配置。  

---

## 0. 这版解决什么问题

之前版本更偏“项目目录初始化”，这版改成“用户电脑本机全局安装”。

也就是说，最终目标不是：

```text
某个业务项目/
└── .ai-coding/
```

而是：

```text
你的电脑用户目录/
└── ~/.ai-coding-skills/
    ├── vendor/
    │   ├── superpowers/
    │   ├── mattpocock-skills/
    │   ├── addyosmani-agent-skills/
    │   └── andrej-karpathy-skills/
    ├── shared/
    │   ├── ai-coding-global-rules.md
    │   ├── claude-user-rules.md
    │   ├── cursor-user-rules.md
    │   └── common-prompts.md
    ├── workflows/
    └── reports/
```

这样做的好处：

| 目标 | 说明 |
|---|---|
| 一次安装 | 四个项目只下载一次 |
| 多项目复用 | 不同业务项目都能复用同一套规范 |
| Claude 可用 | Claude Code 可以读取本机全局规则 |
| Cursor 可用 | Cursor 可以读取同一份全局规则，也可以复制到 User Rules |
| 不污染业务项目 | 默认不往项目目录写任何文件 |
| 低心智 | 用户只需要复制一条指令给 AI |

---

# 1. 本机全局安装：复制给 AI 一键执行

> 下面这段才是你要的“AI 可以一键执行的指令”。  
> 它不是让用户手动跑脚本，而是让 AI Agent 自己完成本机安装、下载、生成规则和输出报告。  
> 复制给 Claude Code、Cursor Agent、Codex 或 Gemini CLI 都可以。

```markdown
你现在是“AI Coding 本机全局安装助手”。

请在我的电脑用户目录下安装一套 Claude Code 和 Cursor 都能复用的 AI Coding Skill 资产。

重要说明：
1. 这是用户电脑本机全局安装，不是安装到当前项目目录。
2. 默认不要修改当前业务项目源码。
3. 默认不要在当前项目中创建 .ai-coding 目录。
4. 默认不要自动提交 Git。
5. 所有说明、报告、提示内容都使用中文。
6. 如果你需要执行终端命令，可以直接执行。
7. 如果某个工具的全局配置无法通过文件稳定写入，请生成对应的本机说明文件，并告诉我在哪里复制。

请严格按以下步骤执行。

---

## 第一步：识别本机环境

请识别并输出：

1. 当前操作系统。
2. 当前用户名。
3. 当前用户目录路径。
4. 当前是否能访问终端。
5. 当前是否安装 git。
6. 当前是否安装 node。
7. 当前是否能访问 GitHub。
8. 当前更适合使用 Claude Code、Cursor、Codex 还是其他 Agent。

不要修改业务源码。

---

## 第二步：创建本机全局目录

请在我的用户目录创建以下目录结构：

~/.ai-coding-skills/
├── vendor/
├── shared/
├── workflows/
├── prompts/
├── adapters/
└── reports/

目录说明：

1. vendor：存放四个 GitHub 项目的本地副本。
2. shared：存放 Claude 和 Cursor 都能复用的通用规则。
3. workflows：存放新需求、Bug 修复、重构、上线等流程。
4. prompts：存放可复制给 AI 的中文指令。
5. adapters：存放不同工具的接入说明，例如 Claude、Cursor。
6. reports：存放安装报告。

---

## 第三步：下载或更新四个 GitHub 项目到本机

请把以下四个项目下载或更新到 ~/.ai-coding-skills/vendor/：

1. Superpowers
   仓库地址：https://github.com/obra/superpowers
   本地目录：~/.ai-coding-skills/vendor/superpowers

2. Matt Pocock Skills
   仓库地址：https://github.com/mattpocock/skills
   本地目录：~/.ai-coding-skills/vendor/mattpocock-skills

3. Addy Osmani Agent Skills
   仓库地址：https://github.com/addyosmani/agent-skills
   本地目录：~/.ai-coding-skills/vendor/addyosmani-agent-skills

4. Karpathy Guidelines
   仓库地址：https://github.com/forrestchang/andrej-karpathy-skills
   本地目录：~/.ai-coding-skills/vendor/andrej-karpathy-skills

执行要求：

1. 如果本地目录不存在，请 clone。
2. 如果本地目录已存在且是 Git 仓库，请 pull 更新。
3. 如果网络失败，不要中断整个任务，请记录失败原因。
4. 不要下载到当前项目目录。
5. 不要修改当前业务项目。

---

## 第四步：生成 Claude 和 Cursor 共用的全局规则

请生成文件：

~/.ai-coding-skills/shared/ai-coding-global-rules.md

内容要求：

# AI Coding 全局规则

## 核心原则

1. 先澄清，再编码。
2. 先写 Spec，再写实现。
3. 先写测试，再写业务代码。
4. 一次只做一个小任务。
5. 只修改和任务直接相关的代码。
6. 不允许无关重构。
7. 不允许删除不理解的代码。
8. 不允许硬编码 localhost、127.0.0.1、Token、密钥、生产地址。
9. 所有用户可见英文提示必须改为中文。
10. 完成前必须运行验证命令。
11. 最终输出必须包含修改范围、验证结果、风险点、回滚方式。

## 默认开发流程

需求澄清 → Spec → Plan → TDD → 实现 → 验证 → Review → 交付。

## 默认 Bug 修复流程

复现 → 最小化 → 定位 → 回归测试 → 最小修复 → 验证 → 复盘。

## 默认重构流程

理解现状 → 锁定行为 → 补测试 → 小步重构 → 验证 → 评审。

## 默认上线流程

质量检查 → 风险确认 → 回滚方案 → 上线验证 → 监控观察。

## 引用的本机 Skill 资产

- ~/.ai-coding-skills/vendor/superpowers
- ~/.ai-coding-skills/vendor/mattpocock-skills
- ~/.ai-coding-skills/vendor/addyosmani-agent-skills
- ~/.ai-coding-skills/vendor/andrej-karpathy-skills

---

## 第五步：生成 Claude Code 用户级规则

请生成文件：

~/.ai-coding-skills/shared/claude-user-rules.md

内容要求：

1. 面向 Claude Code。
2. 告诉 Claude Code 每次进入研发任务前，先读取：
   ~/.ai-coding-skills/shared/ai-coding-global-rules.md
3. 告诉 Claude Code 优先参考以下本机 Skill：
   - Superpowers：完整开发流程。
   - Matt Pocock Skills：grill-with-docs、tdd、diagnose、zoom-out、improve-codebase-architecture。
   - Addy Osmani Agent Skills：spec、plan、build、test、review、ship。
   - Karpathy Guidelines：先思考、简洁优先、外科手术式修改、目标驱动执行。
4. 输出一段可追加到 ~/.claude/CLAUDE.md 的中文规则。

然后请检查 ~/.claude/CLAUDE.md：

1. 如果 ~/.claude 目录不存在，请创建。
2. 如果 ~/.claude/CLAUDE.md 不存在，请创建。
3. 如果 ~/.claude/CLAUDE.md 已存在，请先备份为 ~/.claude/CLAUDE.md.bak-当前时间。
4. 在 ~/.claude/CLAUDE.md 末尾追加一个“AI Coding 本机全局规则”章节。
5. 追加内容必须指向：
   ~/.ai-coding-skills/shared/ai-coding-global-rules.md
   ~/.ai-coding-skills/shared/claude-user-rules.md

注意：
1. 不要覆盖用户原有 Claude 配置。
2. 只追加，不删除。
3. 最后告诉我 Claude Code 如何验证是否生效。

---

## 第六步：生成 Cursor 用户级规则

请生成文件：

~/.ai-coding-skills/shared/cursor-user-rules.md

内容要求：

1. 面向 Cursor。
2. 这份内容用于放到 Cursor 的 User Rules 中。
3. 内容必须是中文。
4. 内容必须简短、强约束、低心智。
5. 告诉 Cursor 每次开发任务都遵守本机全局规则：
   ~/.ai-coding-skills/shared/ai-coding-global-rules.md
6. 告诉 Cursor 优先参考本机 Skill 目录：
   ~/.ai-coding-skills/vendor/

请额外生成文件：

~/.ai-coding-skills/adapters/cursor-接入说明.md

说明内容必须包含：

1. Cursor 若支持读取本地文件，可在对话中引用：
   ~/.ai-coding-skills/shared/cursor-user-rules.md

2. Cursor 若需要配置 User Rules，请把：
   ~/.ai-coding-skills/shared/cursor-user-rules.md
   的内容复制到 Cursor Settings → Rules → User Rules。

3. 不建议把四个 Skill 仓库复制进每个业务项目。
4. 如需某个项目单独加强规则，只在该项目增加很薄的一层 .cursor/rules/project.mdc，引用本机全局规则即可。

注意：
1. 不要默认往当前业务项目写 .cursor/rules。
2. 不要污染业务项目。
3. Cursor 全局规则如果无法通过文件直接写入，请明确告诉我这是工具限制，并给出手动复制入口。

---

## 第七步：生成低心智使用指令

请生成以下文件：

1. ~/.ai-coding-skills/prompts/新需求开发指令.md
2. ~/.ai-coding-skills/prompts/Bug修复指令.md
3. ~/.ai-coding-skills/prompts/代码评审指令.md
4. ~/.ai-coding-skills/prompts/前端页面开发指令.md
5. ~/.ai-coding-skills/prompts/API接口开发指令.md
6. ~/.ai-coding-skills/prompts/上线前检查指令.md

要求：
1. 每份文件都是“可以直接复制给 AI 的中文指令”。
2. 不讲复杂概念。
3. 每份指令都要求 AI 读取本机全局规则：
   ~/.ai-coding-skills/shared/ai-coding-global-rules.md
4. 每份指令都要求最终输出：
   修改范围、验证结果、风险点、回滚方式。

---

## 第八步：生成工作流文档

请生成以下文件：

1. ~/.ai-coding-skills/workflows/新需求开发流程.md
2. ~/.ai-coding-skills/workflows/Bug修复流程.md
3. ~/.ai-coding-skills/workflows/重构流程.md
4. ~/.ai-coding-skills/workflows/上线交付流程.md

要求：
1. 每份文档都要简短。
2. 每份文档都要写清楚 AI 应该按什么顺序做。
3. 每份文档都要写清楚用户什么时候需要确认。
4. 不要写成长篇理论文档。

---

## 第九步：生成安装报告

请生成文件：

~/.ai-coding-skills/reports/local-install-report.md

报告内容必须包含：

1. 本机环境识别结果。
2. 四个 GitHub 项目的下载结果。
3. 本机目录结构。
4. Claude Code 配置结果。
5. Cursor 配置结果。
6. 生成了哪些 prompts。
7. 生成了哪些 workflows。
8. 如果有失败项，说明原因和修复方式。
9. 下一步我该怎么验证 Claude 可用。
10. 下一步我该怎么验证 Cursor 可用。

---

## 第十步：最终输出给我

最终请只用中文输出：

1. 本机安装是否完成。
2. 四个项目是否下载成功。
3. Claude Code 是否已经接入本机规则。
4. Cursor 需要我是否手动复制 User Rules。
5. 我下一条可以直接复制使用的“新需求开发指令”路径。
6. 我下一条可以直接复制使用的“Bug 修复指令”路径。

请不要输出太长。
```

---

# 2. 安装完成后，Claude 和 Cursor 怎么使用

## 2.1 Claude Code 使用方式

安装完成后，Claude Code 会优先通过用户级文件使用：

```text
~/.claude/CLAUDE.md
```

该文件会指向：

```text
~/.ai-coding-skills/shared/ai-coding-global-rules.md
~/.ai-coding-skills/shared/claude-user-rules.md
```

以后在任意项目中，你可以直接对 Claude Code 说：

```markdown
请先读取并遵守我的本机全局 AI Coding 规则：

~/.ai-coding-skills/shared/ai-coding-global-rules.md

然后帮我处理下面这个需求：

【粘贴需求】
```

也可以使用更短版本：

```markdown
请按我的本机 AI Coding 全局规则处理这个需求：

【粘贴需求】
```

---

## 2.2 Cursor 使用方式

Cursor 的全局 User Rules 通常需要在应用设置里配置。  
因此本机安装指令会先生成：

```text
~/.ai-coding-skills/shared/cursor-user-rules.md
```

然后你有两种用法。

### 用法一：复制到 Cursor User Rules

打开：

```text
Cursor Settings → Rules → User Rules
```

复制以下文件内容进去：

```text
~/.ai-coding-skills/shared/cursor-user-rules.md
```

之后 Cursor 在任意项目里都能使用这套规则。

### 用法二：在 Cursor 对话中引用本机规则

在 Cursor Agent 中输入：

```markdown
请读取并遵守这个本机规则文件：

~/.ai-coding-skills/shared/cursor-user-rules.md

然后帮我处理下面这个需求：

【粘贴需求】
```

---

# 3. 新需求开发：低心智指令

> 安装完成后，开发新需求只复制这一段。

```markdown
请先读取并遵守我的本机全局 AI Coding 规则：

~/.ai-coding-skills/shared/ai-coding-global-rules.md

然后帮我完成下面这个需求：

【粘贴需求】

请按以下流程执行：

1. 先澄清需求，不要直接写代码。
2. 如果有关键不确定性，最多问我 5 个问题。
3. 信息足够后，生成简洁 Spec。
4. 再拆分 Plan，每个任务必须有文件路径和验证方式。
5. 实现时一次只做一个任务。
6. 优先使用 TDD。
7. 不允许无关重构。
8. 不允许删除不理解的代码。
9. 不允许硬编码敏感信息。
10. 所有用户可见英文提示必须改为中文。
11. 完成后运行项目验证命令。
12. 最终输出修改范围、验证结果、风险点和回滚方式。
```

---

# 4. Bug 修复：低心智指令

```markdown
请先读取并遵守我的本机全局 AI Coding 规则：

~/.ai-coding-skills/shared/ai-coding-global-rules.md

然后修复下面这个 Bug：

【粘贴 Bug 描述、报错日志、截图说明】

请按以下流程执行：

1. 先不要直接改代码。
2. 先复现问题。
3. 再缩小问题范围。
4. 给出可能原因。
5. 通过测试、日志或代码阅读验证根因。
6. 找到根因后，先补回归测试。
7. 再做最小修复。
8. 不允许顺手重构。
9. 不允许删除不理解的代码。
10. 所有用户可见英文提示必须改为中文。
11. 修复后运行验证命令。
12. 最终输出根因、修改范围、验证结果、风险点和回滚方式。
```

---

# 5. 代码评审：低心智指令

```markdown
请先读取并遵守我的本机全局 AI Coding 规则：

~/.ai-coding-skills/shared/ai-coding-global-rules.md

请评审当前分支的代码变更。

重点检查：

1. 是否满足需求。
2. 是否存在逻辑错误。
3. 是否遗漏边界场景。
4. 是否缺少测试。
5. 是否存在安全风险。
6. 是否存在性能风险。
7. 是否存在无关重构。
8. 是否存在硬编码敏感信息。
9. 是否存在用户可见英文提示。
10. 是否影响兼容性。

请按以下格式输出：

1. 阻塞问题：必须修复后才能合并。
2. 重要问题：建议本次修复。
3. 优化建议：可以后续处理。
4. 最终结论：是否建议合并。
```

---

# 6. 前端页面开发：低心智指令

```markdown
请先读取并遵守我的本机全局 AI Coding 规则：

~/.ai-coding-skills/shared/ai-coding-global-rules.md

请实现下面的前端页面需求：

【粘贴页面需求】

要求：

1. 先分析组件结构、状态流、接口依赖和权限规则。
2. 不要一上来直接写代码。
3. 必须覆盖加载中、空数据、错误状态。
4. 表单必须有校验和提交中状态。
5. 接口调用必须走项目已有 API 封装。
6. 类型定义必须清晰。
7. 所有用户可见英文提示必须改为中文。
8. 一次只做一个垂直切片。
9. 完成后检查页面交互、接口请求和边界状态。
10. 最终输出修改范围、验证结果、风险点和回滚方式。
```

---

# 7. API 接口开发：低心智指令

```markdown
请先读取并遵守我的本机全局 AI Coding 规则：

~/.ai-coding-skills/shared/ai-coding-global-rules.md

请实现下面的接口需求：

【粘贴接口需求】

要求：

1. 先设计接口契约，不要直接实现。
2. 明确请求方法、接口路径、请求参数、响应结构。
3. 明确错误码、权限规则、幂等策略和兼容策略。
4. 先写接口测试或契约测试。
5. 再实现接口逻辑。
6. 不允许为了当前实现随意改变已有契约。
7. 不允许硬编码环境地址、Token、密钥。
8. 所有用户可见英文提示必须改为中文。
9. 完成后运行测试和构建。
10. 最终输出接口契约、修改范围、验证结果、风险点和回滚方式。
```

---

# 8. 安装边界说明

## 8.1 本机全局安装和项目接入的区别

| 类型 | 写入位置 | 作用 |
|---|---|---|
| 本机全局安装 | `~/.ai-coding-skills/` | 四个 Skill 项目只下载一次，所有项目共用 |
| Claude 用户级接入 | `~/.claude/CLAUDE.md` | Claude Code 全局读取规则 |
| Cursor 用户级接入 | Cursor User Rules | Cursor 全局读取规则 |
| 项目级接入 | `.cursor/rules/`、`CLAUDE.md` | 某个项目单独增强规则 |

本版重点是前三个，不默认做项目级接入。

## 8.2 为什么 Cursor 可能需要手动复制一次

Claude Code 的用户级规则可以通过本地文件追加。  
Cursor 的 User Rules 往往由应用设置管理，不同版本和系统的存储方式不完全一致。为了避免误写配置，本指南采用更稳妥方式：

```text
AI 负责生成 ~/.ai-coding-skills/shared/cursor-user-rules.md
用户复制到 Cursor User Rules
```

这一步只需要做一次。

## 8.3 如果仍然希望当前项目自动接入

可以在任意项目中对 AI 说：

```markdown
请不要复制四个 Skill 仓库到当前项目。

只在当前项目生成一层很薄的接入规则：

1. 如果是 Cursor 项目，生成 .cursor/rules/use-local-ai-coding.mdc。
2. 如果是 Claude Code 项目，检查当前项目 CLAUDE.md。
3. 规则内容只引用我的本机全局规范：
   ~/.ai-coding-skills/shared/ai-coding-global-rules.md
4. 不要修改业务源码。
5. 不要自动提交 Git。
```

---

# 9. 推荐使用顺序

第一次安装：

```text
复制第 1 节给 AI。
```

Claude Code 日常使用：

```text
直接在任意项目中说：请按我的本机 AI Coding 全局规则处理这个需求。
```

Cursor 日常使用：

```text
先把 ~/.ai-coding-skills/shared/cursor-user-rules.md 复制到 Cursor User Rules。
之后直接在任意项目中说：请按我的本机 AI Coding 全局规则处理这个需求。
```

新需求：

```text
复制第 3 节。
```

Bug 修复：

```text
复制第 4 节。
```

提交前 Review：

```text
复制第 5 节。
```

---

# 10. 最终目标

最终你电脑上只有一套 AI Coding Skill 资产：

```text
~/.ai-coding-skills/
```

Claude Code、Cursor、Codex 或其他 Agent 都围绕这套资产工作。

这样团队成员不用理解太多概念，只需要知道：

```text
先本机安装一次。
开发时复制标准指令。
提交前让 AI Review。
踩坑后把规则沉淀进本机全局规则。
```
