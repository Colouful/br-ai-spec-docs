# AI Coding 最佳实践操作指南：低心智版

> 版本：V2.0  
> 定位：给真实研发项目使用的 AI Coding 操作手册  
> 核心目标：降低学习成本，让开发者只需要复制指令给 AI，AI 自动完成环境准备、Skill 引入、规则落地和开发流程执行。  
> 适用工具：Claude Code、Cursor、Codex、Gemini CLI、OpenCode、Windsurf、GitHub Copilot Agent  
> 参考项目：  
> - https://github.com/obra/superpowers  
> - https://github.com/mattpocock/skills  
> - https://github.com/addyosmani/agent-skills  
> - https://github.com/forrestchang/andrej-karpathy-skills  

---

# 0. 先记住一句话

AI Coding 不是让 AI 随便写代码，而是让 AI 按下面这条链路稳定交付：

```text
先问清楚 → 写规格 → 拆任务 → 写测试 → 小步实现 → 验证 → 评审 → 交付
```

你真正需要记住的只有三类指令：

| 你要做什么 | 复制给 AI 的指令 |
|---|---|
| 初始化项目 AI Coding 能力 | 使用本文第 1 节“一键初始化指令” |
| 开发新需求 | 使用本文第 2 节“新需求一键开发指令” |
| 修 Bug / 重构 / 上线 | 使用本文第 3 节“常见场景指令” |

---

# 1. 一键初始化指令：让 AI 自动下载四个项目并落地 Skill

> 这一节不是脚本，而是“给 AI 执行的完整指令”。  
> 你只需要把下面整段复制到 Claude Code、Cursor Agent、Codex、Gemini CLI 或其他 AI 编程 Agent 里。  
> AI 会自己判断当前项目、下载四个开源项目、建立规则文件、生成使用说明，并告诉你下一步怎么用。

## 1.1 通用版：复制给 AI 直接执行

```markdown
你现在是“AI Coding Skill 初始化执行器”。

请在当前项目根目录中完成 AI Coding 能力初始化，目标是把以下四个项目作为本项目的 AI Coding Skill 参考资产引入，并生成适合当前项目使用的规则文件、说明文档和最小使用入口。

四个参考项目如下：

1. Superpowers
   仓库：https://github.com/obra/superpowers
   用途：作为完整 AI Coding 工作流参考，覆盖需求澄清、计划、TDD、Sub-agent、代码评审和分支收尾。

2. Matt Pocock Skills
   仓库：https://github.com/mattpocock/skills
   用途：作为真实工程研发 Skill 参考，重点使用 grill-with-docs、tdd、diagnose、zoom-out、improve-codebase-architecture。

3. Addy Osmani Agent Skills
   仓库：https://github.com/addyosmani/agent-skills
   用途：作为企业级研发生命周期 Skill 参考，覆盖 spec、plan、build、test、review、ship。

4. Karpathy Guidelines
   仓库：https://github.com/forrestchang/andrej-karpathy-skills
   用途：作为 AI 编码行为准则，强调先思考、简洁优先、外科手术式修改、目标驱动执行。

请严格按以下步骤执行：

第一步：识别当前项目环境
1. 判断当前目录是否是 Git 项目。
2. 判断项目主要技术栈，例如 Vue、React、Next.js、Node.js、Java、Go、Python、Rust。
3. 判断当前 AI 编程工具更接近 Claude Code、Cursor、Codex、Gemini CLI 还是普通终端 Agent。
4. 不要修改业务代码。

第二步：创建本项目 AI Coding 资产目录
请在当前项目根目录创建以下目录：

.ai-coding/
├── vendor/
├── rules/
├── skills/
├── workflows/
└── reports/

说明：
1. vendor 用于存放四个参考项目的本地副本。
2. rules 用于存放项目级 AI 规则。
3. skills 用于存放从四个项目中提炼出来的团队常用 Skill。
4. workflows 用于存放需求开发、Bug 修复、重构、上线等标准流程。
5. reports 用于存放本次初始化报告。

第三步：下载或更新四个参考项目
请在 .ai-coding/vendor/ 目录下下载或更新以下仓库：

- superpowers
- mattpocock-skills
- addyosmani-agent-skills
- andrej-karpathy-skills

要求：
1. 如果目录不存在，就 clone。
2. 如果目录已经存在并且是 Git 仓库，就 pull 更新。
3. 如果网络失败，请不要中断整个初始化流程，需要在报告中说明失败原因和人工补救方式。
4. 下载完成后，列出每个仓库的本地路径。

第四步：生成项目级规则文件
请根据当前项目技术栈生成或更新以下文件：

1. CLAUDE.md
   用于 Claude Code 项目规则。
   如果文件已存在，不要覆盖，先备份为 CLAUDE.md.bak，然后在末尾追加“AI Coding 规范”章节。

2. AGENTS.md
   用于 Codex、OpenCode 或通用 Agent 项目规则。
   如果文件已存在，不要覆盖，先备份为 AGENTS.md.bak，然后在末尾追加“AI Coding 规范”章节。

3. .cursor/rules/project-ai-coding.mdc
   用于 Cursor 项目规则。
   如果 .cursor/rules 不存在，需要自动创建。

这些规则文件必须包含以下内容：

- 先澄清，再编码。
- 先写 Spec，再写实现。
- 先写测试，再写业务代码。
- 只修改和任务直接相关的代码。
- 不允许无关重构。
- 不允许删除不理解的代码。
- 不允许硬编码 localhost、127.0.0.1、Token、密钥。
- 所有用户可见英文提示必须改为中文。
- 完成前必须运行验证命令。
- 输出内容必须包含修改范围、验证结果、风险点和回滚方案。

第五步：生成常用工作流文档
请生成以下文件：

1. .ai-coding/workflows/新需求开发流程.md
内容包括：
需求澄清 → Spec → Plan → TDD → Build → Test → Review → Ship。

2. .ai-coding/workflows/Bug修复流程.md
内容包括：
复现 → 最小化 → 定位 → 回归测试 → 最小修复 → 验证 → 复盘。

3. .ai-coding/workflows/重构流程.md
内容包括：
理解现状 → 锁定边界 → 补测试 → 小步重构 → 验证 → 评审。

4. .ai-coding/workflows/上线交付流程.md
内容包括：
质量检查 → 影响范围 → 回滚方案 → 监控指标 → 上线后验证。

第六步：生成常用 Skill 索引
请生成 .ai-coding/skills/常用Skill索引.md。

要求按场景整理：

1. 需求不清楚
   推荐：grill-with-docs、idea-refine、spec-driven-development。

2. 需求已明确
   推荐：spec-driven-development、planning-and-task-breakdown、writing-plans。

3. 开始写代码
   推荐：test-driven-development、incremental-implementation、context-engineering。

4. Bug 修复
   推荐：diagnose、systematic-debugging、debugging-and-error-recovery。

5. 前端页面
   推荐：frontend-ui-engineering、browser-testing-with-devtools、code-review-and-quality。

6. API 设计
   推荐：api-and-interface-design、source-driven-development、test-driven-development。

7. 代码评审
   推荐：code-review-and-quality、code-simplification、requesting-code-review。

8. 上线发布
   推荐：shipping-and-launch、ci-cd-and-automation、git-workflow-and-versioning。

第七步：生成一份“给开发者看的最短使用说明”
请生成 .ai-coding/README.md。

要求：
1. 开头只保留三句话，告诉开发者怎么用。
2. 不要堆概念。
3. 给出三个可复制指令：
   - 新需求怎么让 AI 开发。
   - Bug 怎么让 AI 修。
   - 提交前怎么让 AI Review。
4. 每个指令必须是中文。
5. 每个指令必须能直接复制给 AI 使用。

第八步：输出初始化报告
请生成 .ai-coding/reports/init-report.md。

报告必须包含：
1. 当前项目技术栈判断。
2. 四个仓库下载结果。
3. 生成或修改了哪些文件。
4. 哪些文件做了备份。
5. 后续使用建议。
6. 如果有失败项，列出手动修复方式。

执行限制：
1. 不允许修改业务源码。
2. 不允许自动提交 Git。
3. 不允许自动 push。
4. 不允许删除已有文件。
5. 不允许覆盖已有规则文件，必须先备份再追加或生成新文件。
6. 所有输出说明使用中文。
7. 如果需要我确认，请只在高风险操作前询问；低风险文件创建和目录创建可以直接执行。

完成后，请用简短清单告诉我：
1. 已下载哪些项目。
2. 已生成哪些文件。
3. 我下一步应该复制哪条指令开始开发。
```

---

## 1.2 Claude Code 专用初始化指令

> 如果你明确使用 Claude Code，可以复制这一版。  
> 它会优先考虑 `CLAUDE.md`、Claude Plugin、Skill 和 Hook 的协作方式。

```markdown
你现在是 Claude Code 项目初始化助手。

请为当前项目初始化 AI Coding Skill 能力。

目标：
1. 引入以下四个参考项目：
   - https://github.com/obra/superpowers
   - https://github.com/mattpocock/skills
   - https://github.com/addyosmani/agent-skills
   - https://github.com/forrestchang/andrej-karpathy-skills
2. 在项目中生成适合 Claude Code 使用的 CLAUDE.md。
3. 生成 .ai-coding/ 目录，沉淀规则、Skill 索引、工作流和初始化报告。
4. 不修改业务代码，不提交 Git。

请执行：

1. 在 .ai-coding/vendor/ 下下载或更新四个仓库。
2. 检查当前项目是否已有 CLAUDE.md。
3. 如果已有 CLAUDE.md，先备份为 CLAUDE.md.bak，再追加“AI Coding 规范”章节。
4. 如果没有 CLAUDE.md，创建新的 CLAUDE.md。
5. CLAUDE.md 必须包含：
   - 先澄清，再编码。
   - 先写 Spec，再写实现。
   - 先写测试，再写业务代码。
   - 只做外科手术式修改。
   - 不允许无关重构。
   - 不允许删除不理解的代码。
   - 所有用户可见英文提示必须改为中文。
   - 完成前必须运行验证命令。
6. 生成 .ai-coding/README.md，里面只保留最短使用方法。
7. 生成 .ai-coding/skills/常用Skill索引.md。
8. 生成 .ai-coding/workflows/新需求开发流程.md。
9. 生成 .ai-coding/workflows/Bug修复流程.md。
10. 生成 .ai-coding/reports/init-report.md。

同时请在报告中提醒我：如果我希望安装 Claude Code Plugin，可以在 Claude Code 中手动执行以下命令：

/plugin install superpowers@claude-plugins-official
/plugin marketplace add addyosmani/agent-skills
/plugin install agent-skills@addy-agent-skills
/plugin marketplace add forrestchang/andrej-karpathy-skills
/plugin install andrej-karpathy-skills@karpathy-skills

注意：
1. 上面的 plugin 命令只写进报告，不要当成 shell 命令执行。
2. 下载仓库可以通过终端执行。
3. 不要自动提交代码。
4. 最终输出中文总结。
```

---

## 1.3 Cursor 专用初始化指令

> 如果你主要使用 Cursor，把下面这段复制给 Cursor Agent。

```markdown
你现在是 Cursor 项目规则初始化助手。

请为当前项目初始化 AI Coding Rules。

目标：
1. 下载以下四个参考项目到 .ai-coding/vendor/：
   - https://github.com/obra/superpowers
   - https://github.com/mattpocock/skills
   - https://github.com/addyosmani/agent-skills
   - https://github.com/forrestchang/andrej-karpathy-skills
2. 创建 .cursor/rules/project-ai-coding.mdc。
3. 从参考项目中提炼适合当前项目的 Cursor Rules。
4. 生成 .ai-coding/README.md，让团队成员一看就知道怎么用。

请执行：

1. 判断当前项目技术栈。
2. 创建 .ai-coding/vendor/、.ai-coding/rules/、.ai-coding/skills/、.ai-coding/workflows/、.ai-coding/reports/。
3. 下载或更新四个参考项目。
4. 创建或更新 .cursor/rules/project-ai-coding.mdc。
5. 如果当前项目已有 .cursor/rules/ 下的规则文件，不要覆盖，只新增 project-ai-coding.mdc。
6. project-ai-coding.mdc 必须包含：
   - 先澄清，再编码。
   - 先写 Spec，再写实现。
   - 先写测试，再写业务代码。
   - 只修改和任务直接相关的代码。
   - 不允许无关重构。
   - 不允许硬编码敏感信息。
   - 所有用户可见英文提示必须改为中文。
   - 完成前必须输出验证结果。
7. 生成 .ai-coding/README.md，内容必须非常短，只告诉开发者三件事：
   - 新需求复制什么指令。
   - Bug 修复复制什么指令。
   - 提交前 Review 复制什么指令。
8. 生成 .ai-coding/reports/init-report.md，记录下载结果和文件变更。

限制：
1. 不修改业务源码。
2. 不删除已有文件。
3. 不自动提交 Git。
4. 全部输出中文。
```

---

## 1.4 Codex / 通用 Agent 初始化指令

> 如果你使用 Codex、OpenCode、GitHub Copilot Agent 或其他通用 AI Agent，复制这一版。

```markdown
你现在是通用 AI Coding Agent 初始化助手。

请在当前项目中初始化 AI Coding 规范资产。

参考项目：
1. https://github.com/obra/superpowers
2. https://github.com/mattpocock/skills
3. https://github.com/addyosmani/agent-skills
4. https://github.com/forrestchang/andrej-karpathy-skills

请完成以下任务：

1. 在 .ai-coding/vendor/ 下下载或更新四个参考项目。
2. 创建 AGENTS.md，作为通用 Agent 的项目规则。
3. 如果 AGENTS.md 已存在，先备份为 AGENTS.md.bak，再追加 AI Coding 规范。
4. 创建 .ai-coding/README.md，写清楚最短使用方式。
5. 创建 .ai-coding/skills/常用Skill索引.md。
6. 创建 .ai-coding/workflows/新需求开发流程.md。
7. 创建 .ai-coding/workflows/Bug修复流程.md。
8. 创建 .ai-coding/reports/init-report.md。

AGENTS.md 必须包含以下规则：

1. 复杂需求必须先写 Spec。
2. 实现前必须拆 Plan。
3. 行为变更必须优先写测试。
4. Bug 修复必须先复现，再写回归测试。
5. 不允许无关重构。
6. 不允许删除不理解的代码。
7. 不允许硬编码敏感信息。
8. 所有用户可见英文提示必须改为中文。
9. 完成前必须运行项目验证命令。
10. 最终回复必须包含变更范围、验证结果、风险点和回滚方案。

限制：
1. 不修改业务源码。
2. 不自动提交 Git。
3. 不自动 push。
4. 不覆盖已有文件，必须备份。
5. 输出中文报告。
```

---

# 2. 新需求一键开发指令

> 初始化完成后，真实需求开发时，不需要再记一堆概念。  
> 直接复制下面这段给 AI。

```markdown
你现在是当前项目的 AI Coding 开发助手。

请基于当前项目规则、CLAUDE.md、AGENTS.md、.cursor/rules 和 .ai-coding 中的规范，帮我完成下面这个需求。

需求如下：

【在这里粘贴需求】

请严格按以下流程执行：

第一步：需求澄清
1. 先不要写代码。
2. 先指出需求中不清楚、容易误解、可能影响实现的点。
3. 如果存在关键不确定性，请最多问我 5 个问题。
4. 如果信息足够，请直接进入下一步。

第二步：生成 Spec
请生成一份简洁但可执行的 Spec，包含：
1. 需求目标。
2. 实现范围。
3. 不做什么。
4. 用户流程。
5. 数据结构。
6. 接口契约。
7. 异常场景。
8. 验收标准。

第三步：生成 Plan
请把需求拆成小任务。
每个任务必须包含：
1. 任务目标。
2. 涉及文件。
3. 修改内容。
4. 验证方式。
5. 风险点。

第四步：执行实现
1. 一次只做一个任务。
2. 优先使用 TDD。
3. 如果是 Bug 修复，必须先写回归测试。
4. 不允许无关重构。
5. 不允许删除不理解的代码。
6. 不允许硬编码敏感信息。
7. 所有用户可见英文提示必须改为中文。

第五步：验证
请根据项目技术栈运行必要验证，例如：
1. Lint。
2. 类型检查。
3. 单元测试。
4. 构建。
5. 必要的手工验证说明。

第六步：输出交付结果
最终请输出：
1. 改了哪些文件。
2. 每个文件改了什么。
3. 执行了哪些验证。
4. 还有哪些风险。
5. 如何回滚。
6. 是否需要我人工确认。
```

---

# 3. 常见场景一键指令

## 3.1 Bug 修复指令

```markdown
你现在是当前项目的 Bug 诊断与修复助手。

请修复下面的问题：

【粘贴 Bug 描述、报错信息、截图说明或日志】

要求：

1. 先不要直接改代码。
2. 先复现问题。
3. 再缩小问题范围。
4. 给出 2 到 3 个可能原因。
5. 通过日志、测试或代码阅读验证原因。
6. 找到根因后，先补一个回归测试。
7. 再做最小修复。
8. 不允许顺手重构。
9. 不允许删除不理解的代码。
10. 所有用户可见英文提示必须改为中文。
11. 修复后运行验证命令。
12. 最终输出根因、修改文件、验证结果、风险点和回滚方式。
```

---

## 3.2 前端页面开发指令

```markdown
你现在是当前项目的高级前端开发助手。

请实现下面的前端页面需求：

【粘贴页面需求】

要求：

1. 先不要直接写代码。
2. 先分析页面结构、组件拆分、状态流、接口依赖和权限规则。
3. 必须覆盖 Loading、Empty、Error 状态。
4. 表单必须包含校验规则和提交中状态。
5. 接口调用必须走项目已有 API 封装。
6. 类型定义必须清晰。
7. 所有用户可见英文提示必须改为中文。
8. 一次只做一个垂直切片。
9. 完成后检查浏览器 Console、Network、页面交互和边界状态。
10. 最终输出修改文件、验证结果、风险点和回滚方式。
```

---

## 3.3 API 接口开发指令

```markdown
你现在是当前项目的 API 设计与实现助手。

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
10. 最终输出接口契约、修改文件、验证结果、风险点和回滚方式。
```

---

## 3.4 代码评审指令

```markdown
你现在是当前项目的代码评审助手。

请评审当前分支相对于主分支的变更。

要求按以下维度检查：

1. 是否满足需求和 Spec。
2. 是否存在逻辑错误。
3. 是否存在边界场景遗漏。
4. 是否存在安全风险。
5. 是否存在性能风险。
6. 是否存在无关重构。
7. 是否存在硬编码地址、Token、密钥。
8. 是否存在用户可见英文提示。
9. 是否缺少测试。
10. 是否影响兼容性。

请按严重程度输出：

- 阻塞问题：必须修复后才能合并。
- 重要问题：建议本次修复。
- 优化建议：可以后续处理。

最终请给出是否建议合并。
```

---

## 3.5 重构指令

```markdown
你现在是当前项目的重构助手。

请分析并重构下面这个模块：

【粘贴模块路径或说明】

要求：

1. 先解释当前模块职责、依赖关系和数据流。
2. 先找出复杂度来源，不要直接改代码。
3. 明确哪些行为必须保持不变。
4. 先补充必要测试。
5. 每次只做一个小重构。
6. 不允许改变外部接口行为。
7. 不允许顺手改无关文件。
8. 所有用户可见英文提示必须改为中文。
9. 每一步都要运行验证。
10. 最终输出重构前后差异、验证结果、风险点和回滚方式。
```

---

## 3.6 上线前检查指令

```markdown
你现在是当前项目的上线前质量检查助手。

请检查当前分支是否可以上线。

要求检查：

1. 是否关联需求、Spec 或任务。
2. 是否存在未完成代码。
3. 是否存在 console.log、debugger、临时注释。
4. 是否存在硬编码环境地址、Token、密钥。
5. 是否存在用户可见英文提示。
6. 是否通过 Lint。
7. 是否通过类型检查。
8. 是否通过测试。
9. 是否通过构建。
10. 是否有回滚方案。
11. 是否有上线后验证方式。
12. 是否有监控或日志观察点。

最终请输出：
1. 是否允许上线。
2. 阻塞问题。
3. 重要风险。
4. 验证结果。
5. 回滚方案。
```

---

# 4. 四个项目到底怎么用：低心智解释

## 4.1 不需要先学完

你不需要先完整学习四个项目。  
正确方式是：先让 AI 初始化，再在真实需求中逐步使用。

| 项目 | 你可以怎么理解 |
|---|---|
| Superpowers | 给 AI 一套完整研发流程 |
| Matt Pocock Skills | 给 AI 一组真实工程常用动作 |
| Addy Osmani Agent Skills | 给 AI 一套企业级生命周期 Skill |
| Karpathy Guidelines | 给 AI 一组写代码时不能犯错的底层原则 |

## 4.2 你只需要记住 6 个动作

| 动作 | 什么时候用 | 对应指令 |
|---|---|---|
| 问清楚 | 需求模糊时 | 需求澄清 |
| 写规格 | 准备开发前 | Spec |
| 拆任务 | 需求较大时 | Plan |
| 写测试 | 行为变化时 | TDD |
| 查问题 | 出 Bug 时 | Diagnose |
| 做评审 | 提交前 | Review |

## 4.3 推荐默认流程

新需求默认：

```text
需求澄清 → Spec → Plan → TDD → 实现 → 验证 → Review
```

Bug 默认：

```text
复现 → 定位 → 回归测试 → 最小修复 → 验证
```

重构默认：

```text
理解现状 → 锁定行为 → 补测试 → 小步修改 → 验证
```

上线默认：

```text
检查风险 → 运行验证 → 写回滚 → 上线观察
```

---

# 5. 团队落地建议

## 5.1 第一天先做什么

第一天只做三件事：

```text
1. 把第 1.1 节复制给 AI，让 AI 初始化项目。
2. 把第 2 节复制给 AI，跑一个真实小需求。
3. 把第 3.4 节复制给 AI，让 AI 做一次提交前 Review。
```

不要一开始就培训所有概念。

## 5.2 第一周做到什么程度

第一周目标：

```text
1. 所有新需求都有 Spec。
2. 所有 Bug 修复都有回归测试。
3. 所有提交前都做 AI Review。
4. 所有项目都有 CLAUDE.md、AGENTS.md 或 .cursor/rules。
```

## 5.3 第一个月沉淀什么

第一个月目标：

```text
1. 沉淀团队自己的常用指令。
2. 沉淀项目级规则。
3. 沉淀踩坑清单。
4. 沉淀质量门禁。
5. 形成团队 AI Coding SOP。
```

---

# 6. 最终推荐用法

你真正需要复制使用的顺序是：

```text
第一次使用：
复制第 1.1 节给 AI。

开发新需求：
复制第 2 节给 AI。

修 Bug：
复制第 3.1 节给 AI。

提交前：
复制第 3.4 节给 AI。

上线前：
复制第 3.6 节给 AI。
```

最终目标：

> 让团队成员不需要理解所有 AI Coding 理论，也能通过复制标准指令，把 AI 稳定纳入真实研发流程。
