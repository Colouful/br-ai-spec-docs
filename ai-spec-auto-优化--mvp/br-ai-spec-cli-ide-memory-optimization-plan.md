# br-ai-spec CLI IDE Memory & Frontend Real-Project Optimization Plan

> 文件名：`br-ai-spec-cli-ide-memory-optimization-plan.md`  
> 适用项目：`Colouful/br-ai-spec` / `ai-spec-auto`  
> 目标阶段：只优化 `br-ai-spec` CLI，不依赖 `skill-q-platform` 与 `br-ai-spec-visual` 后续功能  
> 目标场景：Vue / React 前端真实项目接入、真实需求开发前的 IDE 规则注入与上下文索引优化  
> 推荐执行方式：交给 Codex / Cursor / Claude Code 作为一轮可完成任务执行

---

## 0. 最高结论

本轮优化必须做，但边界要收窄。

### 0.1 必须做的能力

1. 在 `br-ai-spec` CLI 中补齐统一的 IDE 集成层。
2. 在 `.cursor` / `.claude` 中写入“轻量指针文件”，不要复制完整规则正文。
3. 在 `AGENTS.md` / `CLAUDE.md` / `memory.md` 中引入“Pointer-only 注册表索引锚点”。
4. 让 Cursor / Claude Code 能稳定知道：
   - 当前项目使用了哪些 Rule。
   - 当前项目使用了哪些 Skill。
   - 当前项目使用了哪些 Command。
   - 当前项目的 Manifest / Lock / ContextIndex 在哪里。
   - Vue / React 项目开发时应该优先读取哪些前端资产。
5. 支持真实 Vue / React 项目执行：
   - `scan`
   - `init --recommend --dry-run`
   - `init --recommend --yes`
   - `ide sync`
   - `check`
   - `context`
   - `/spec-start`

### 0.2 不应该做的能力

本轮不做：

1. Hub 生产化功能。
2. Visual 看板功能。
3. 后端 Java / Python / Go / Rust 资产体系。
4. AI 工程资产生成器。
5. Codex / Cursor / Claude Code 真实自动编码执行器。
6. OpenClaw / 钉钉机器人。
7. 多团队 RBAC。
8. 远程任务调度。
9. 自动 PR / merge。
10. 改业务代码。

---

## 1. 背景与当前问题

`br-ai-spec` 当前已经具备以下基础：

1. `.agents/`：存放项目规则、技能、专家资产。
2. `.ai-spec/`：存放项目配置、锁文件、上下文索引、运行状态。
3. `.cursor/` / `.claude/`：用于 IDE / Agent 适配。
4. `AGENTS.md`：通用 Agent 入口。
5. `CLAUDE.md`：Claude Code 入口。
6. `scan` / `init` / `sync` / `check` / `context` / `spec-start` 等 CLI 基础命令。
7. Vue / React 当前是主场景。

但真实项目使用时会遇到一个关键问题：

> 规则、技能、命令、上下文索引虽然安装到了项目里，但不同 IDE / Agent 不一定知道应该优先读哪个入口。

因此必须补齐一个“IDE Memory Pointer 层”。

---

## 2. 核心产品决策

### 2.1 是否需要在 `memory.md` / `CLAUDE.md` / `AGENTS.md` 中引入注册表？

结论：需要。

但不能写入完整规则和技能正文。

必须采用：

```text
Pointer-only 模式
```

也就是只写“索引指针”和“读取顺序”，不写大段业务规则。

### 2.2 为什么不能把完整 Rule / Skill 写进 memory 文件？

原因：

1. 容易过期。
2. 容易重复。
3. 容易和 `.agents/registry` 冲突。
4. 容易导致上下文膨胀。
5. 修改成本高。
6. 多 IDE 之间难以保持一致。

### 2.3 推荐模型

```text
.agents/                       资产正文
  rules/
  skills/
  commands/
  registry/
    registry.index.json        资产注册表
    ide-registry.json          IDE 可消费索引

.ai-spec/                      项目状态
  project.json
  workspace.json
  policy.json
  ai-spec.lock.json
  context-index.json           上下文索引
  history/

.cursor/                       Cursor 指针层
  rules/
    ai-spec-auto.mdc
  commands/
    spec-start.md
    spec-update.md
    spec-status.md

.claude/                       Claude 指针层
  commands/
    spec-start.md
    spec-update.md
    spec-status.md
  ai-spec-auto.md

AGENTS.md                      通用 Agent 指针入口
CLAUDE.md                      Claude Code 指针入口
memory.md                      跨会话记忆指针入口
```

---

## 3. 本轮技术目标

### 3.1 一句话目标

让 `br-ai-spec` 在 Vue / React 真实项目中安装后，Cursor / Claude Code 可以稳定读取统一规则、技能、命令和上下文索引，并且整个过程可检查、可修复、可回滚、可测试。

### 3.2 功能目标

本轮交付以下能力：

1. `ide sync`
2. `ide doctor`
3. `ide repair`
4. IDE 指针文件生成器。
5. `AGENTS.md` / `CLAUDE.md` / `memory.md` 锚点注入。
6. `.cursor` / `.claude` 指针层生成。
7. symlink / copy 双模式。
8. Vue / React 前端资源优先级写入。
9. 幂等更新。
10. 不破坏用户已有文件。
11. 不扫描和上传业务源码。
12. 完整测试。
13. 真实 Vue / React 项目 dry-run 验证。

---

## 4. CLI 命令设计

### 4.1 新增命令

```bash
ai-spec-auto ide sync .
ai-spec-auto ide doctor .
ai-spec-auto ide repair .
```

### 4.2 参数

```bash
ai-spec-auto ide sync . \
  --ide cursor,claude \
  --profile react \
  --link-mode auto \
  --write-memory-anchor \
  --write-agent-anchor \
  --dry-run

ai-spec-auto ide sync . \
  --ide cursor,claude \
  --profile vue \
  --link-mode copy \
  --yes
```

### 4.3 参数说明

| 参数 | 说明 | 默认值 |
|---|---|---|
| `--ide` | 目标 IDE，支持 `cursor`、`claude` | `cursor,claude` |
| `--profile` | 技术栈，支持 `react`、`vue`、`auto` | `auto` |
| `--link-mode` | 指针写入模式，支持 `auto`、`copy`、`symlink` | `auto` |
| `--write-memory-anchor` | 是否写入 `memory.md` AI 锚点 | true |
| `--write-agent-anchor` | 是否写入 `AGENTS.md` / `CLAUDE.md` AI 锚点 | true |
| `--dry-run` | 只输出计划，不写文件 | false |
| `--yes` | 直接执行写入 | false |

### 4.4 link-mode 策略

```text
auto：
  优先 symlink。
  如果失败，自动降级 copy。
  降级时输出中文提示。

copy：
  直接复制轻量指针文件。
  推荐默认用于团队项目，兼容性最好。

symlink：
  强制使用软链接。
  如果失败则报错，不自动降级。
```

### 4.5 为什么默认建议 `auto`，真实项目建议 `copy`

symlink 在 macOS / Linux 上体验好，但在 Windows、权限受限目录、某些 IDE 沙箱中容易失败。

本轮目标是让前端真实项目先用起来，所以策略是：

```text
CLI 默认 auto
团队推荐 copy
高级用户可显式 symlink
```

---

## 5. 文件写入策略

### 5.1 允许写入的文件

本轮仅允许写入以下范围：

```text
.agents/registry/ide-registry.json
.ai-spec/ide-integration.json
.cursor/rules/ai-spec-auto.mdc
.cursor/commands/spec-start.md
.cursor/commands/spec-update.md
.cursor/commands/spec-status.md
.claude/ai-spec-auto.md
.claude/commands/spec-start.md
.claude/commands/spec-update.md
.claude/commands/spec-status.md
AGENTS.md
CLAUDE.md
memory.md
```

### 5.2 禁止写入的文件

禁止写入：

```text
src/
app/
pages/
components/
views/
package.json
pnpm-lock.yaml
package-lock.json
yarn.lock
vite.config.*
webpack.config.*
tsconfig.json
.env
.env.*
```

除非用户明确执行未来的开发命令，本轮 `ide sync` 阶段绝不改业务代码。

### 5.3 锚点注入方式

所有 root markdown 只能更新 AI 管理区块：

```md
<!-- AI-SPEC-AUTO:START -->
...
<!-- AI-SPEC-AUTO:END -->
```

规则：

1. 区块不存在则追加到文件末尾。
2. 区块存在则替换区块内部内容。
3. 区块外内容绝不修改。
4. 文件原本不存在则创建。
5. 所有提示文案使用中文。

---

## 6. Pointer-only 锚点模板

### 6.1 `AGENTS.md`

```md
<!-- AI-SPEC-AUTO:START -->
# ai-spec-auto 项目规范入口

本项目已接入 `ai-spec-auto`。执行任何需求开发前，必须先读取以下索引文件，不要直接全量扫描项目。

## 必读顺序

1. `.ai-spec/project.json`：项目基本信息。
2. `.ai-spec/workspace.json`：工作区与包结构。
3. `.ai-spec/policy.json`：执行策略与安全边界。
4. `.ai-spec/ai-spec.lock.json`：已锁定资产版本。
5. `.agents/registry/registry.index.json`：Rule / Skill / Command 注册表。
6. `.agents/registry/ide-registry.json`：IDE 指针索引。
7. `.ai-spec/context-index.json`：上下文分级索引。

## 执行原则

- 不要跳过注册表直接猜测规则。
- 不要一次性读取所有 Rule / Skill 正文。
- 先读索引，再按任务阶段读取需要的资产。
- 不要上传源码、原始提示词、原始响应、绝对路径或密钥。
- Vue / React 项目优先读取前端实现相关 Rule / Skill。
<!-- AI-SPEC-AUTO:END -->
```

### 6.2 `CLAUDE.md`

```md
<!-- AI-SPEC-AUTO:START -->
# Claude Code 执行入口

你正在一个已接入 `ai-spec-auto` 的项目中工作。

## 启动前必须读取

1. `.agents/registry/ide-registry.json`
2. `.agents/registry/registry.index.json`
3. `.ai-spec/context-index.json`
4. `.ai-spec/ai-spec.lock.json`

## 常用命令

- `/project-init`：初始化项目规范。
- `/spec-start`：启动新需求。
- `/spec-update`：补充或修正当前需求。
- `/spec-status`：查看当前状态。
- `/spec-continue`：继续当前 run。

## 上下文策略

只读取当前阶段需要的 Rule / Skill，不要全量展开全部资产。
<!-- AI-SPEC-AUTO:END -->
```

### 6.3 `memory.md`

```md
<!-- AI-SPEC-AUTO:START -->
# ai-spec-auto 记忆锚点

本文件只保存长期稳定的项目规范指针，不保存业务实现细节。

## 稳定索引

- 项目配置：`.ai-spec/project.json`
- 工作区配置：`.ai-spec/workspace.json`
- 策略配置：`.ai-spec/policy.json`
- 资产锁文件：`.ai-spec/ai-spec.lock.json`
- IDE 注册表：`.agents/registry/ide-registry.json`
- 资产注册表：`.agents/registry/registry.index.json`
- 上下文索引：`.ai-spec/context-index.json`

## 禁止写入

- 不要把源码片段写入 memory。
- 不要把接口密钥写入 memory。
- 不要把一次性执行日志写入 memory。
- 不要把完整 Rule / Skill 正文写入 memory。
<!-- AI-SPEC-AUTO:END -->
```

---

## 7. IDE Registry 设计

### 7.1 文件路径

```text
.agents/registry/ide-registry.json
```

### 7.2 示例

```json
{
  "schemaVersion": "1.0.0",
  "generatedBy": "ai-spec-auto",
  "updatedAt": "2026-04-27T00:00:00.000Z",
  "project": {
    "profile": "react",
    "framework": "React",
    "language": ["TypeScript", "JavaScript"],
    "packageManager": "pnpm"
  },
  "ide": {
    "enabled": ["cursor", "claude"],
    "linkMode": "auto",
    "anchors": {
      "agentsMd": true,
      "claudeMd": true,
      "memoryMd": true
    }
  },
  "indexes": {
    "assetRegistry": ".agents/registry/registry.index.json",
    "lockFile": ".ai-spec/ai-spec.lock.json",
    "contextIndex": ".ai-spec/context-index.json",
    "projectConfig": ".ai-spec/project.json",
    "workspaceConfig": ".ai-spec/workspace.json",
    "policyConfig": ".ai-spec/policy.json"
  },
  "priorityAssets": {
    "rules": [
      "frontend-common-rule",
      "frontend-react-rule"
    ],
    "skills": [
      "frontend-implementer",
      "component-refactor",
      "route-change",
      "state-management",
      "unit-test-writer"
    ],
    "commands": [
      "project-init",
      "spec-start",
      "spec-update",
      "spec-status",
      "spec-continue"
    ]
  },
  "privacy": {
    "sourceCodeIncluded": false,
    "rawPromptIncluded": false,
    "rawResponseIncluded": false,
    "absolutePathIncluded": false
  }
}
```

### 7.3 Vue 示例差异

```json
{
  "priorityAssets": {
    "rules": [
      "frontend-common-rule",
      "frontend-vue-rule"
    ],
    "skills": [
      "frontend-implementer",
      "vue-component-implementer",
      "vite-build-checker",
      "unit-test-writer"
    ]
  }
}
```

---

## 8. `.ai-spec/ide-integration.json` 设计

### 8.1 文件路径

```text
.ai-spec/ide-integration.json
```

### 8.2 示例

```json
{
  "schemaVersion": "1.0.0",
  "profile": "react",
  "ide": {
    "cursor": {
      "enabled": true,
      "rulesFile": ".cursor/rules/ai-spec-auto.mdc",
      "commandsDir": ".cursor/commands"
    },
    "claude": {
      "enabled": true,
      "entryFile": ".claude/ai-spec-auto.md",
      "commandsDir": ".claude/commands"
    }
  },
  "memoryAnchors": {
    "AGENTS.md": true,
    "CLAUDE.md": true,
    "memory.md": true
  },
  "linkMode": "auto",
  "lastSyncAt": "2026-04-27T00:00:00.000Z"
}
```

---

## 9. Cursor 指针文件模板

### 9.1 `.cursor/rules/ai-spec-auto.mdc`

```md
---
description: ai-spec-auto 项目规范入口
alwaysApply: true
---

# ai-spec-auto Cursor 规则入口

本项目通过 `ai-spec-auto` 管理规则、技能、命令和上下文索引。

## 读取顺序

1. `.agents/registry/ide-registry.json`
2. `.agents/registry/registry.index.json`
3. `.ai-spec/context-index.json`
4. `.ai-spec/ai-spec.lock.json`

## 执行要求

- 不要跳过索引直接读取所有资产。
- 不要上传源码、原始提示词、原始响应、绝对路径或密钥。
- 先判断当前任务属于 React / Vue 前端开发、组件修改、路由修改、状态管理还是测试修复。
- 再按需读取对应 Rule / Skill。
```

### 9.2 `.cursor/commands/spec-start.md`

```md
# /spec-start

请按 `ai-spec-auto` 规范启动一个新需求。

执行前先读取：

1. `.agents/registry/ide-registry.json`
2. `.agents/registry/registry.index.json`
3. `.ai-spec/context-index.json`
4. `.ai-spec/ai-spec.lock.json`

要求：

- 先确认需求范围。
- 再判断 Vue / React 技术栈。
- 只读取必要 Rule / Skill。
- 不要直接修改业务代码，除非已经进入实现阶段。
- 所有输出使用中文。
```

---

## 10. Claude 指针文件模板

### 10.1 `.claude/ai-spec-auto.md`

```md
# ai-spec-auto Claude Code 入口

你是当前项目的 AI 开发协作者。项目规范由 `ai-spec-auto` 管理。

## 必读索引

1. `.agents/registry/ide-registry.json`
2. `.agents/registry/registry.index.json`
3. `.ai-spec/context-index.json`
4. `.ai-spec/ai-spec.lock.json`

## 原则

- 先读索引，再读资产。
- 先确认任务阶段，再进入实现。
- Vue / React 前端项目优先读取前端资产。
- 不要泄露源码、路径、密钥。
- 所有提示和错误输出必须使用中文。
```

---

## 11. 代码结构建议

### 11.1 新增目录

```text
src/ide/
  ide-command.js
  ide-service.js
  ide-plan.js
  ide-types.js

  registry/
    ide-registry-builder.js
    ide-registry-writer.js

  anchors/
    markdown-anchor-writer.js
    agents-md-writer.js
    claude-md-writer.js
    memory-md-writer.js

  adapters/
    cursor-adapter.js
    claude-adapter.js

  links/
    link-mode-resolver.js
    safe-link-writer.js

  doctor/
    ide-doctor.js
    ide-repair.js
```

### 11.2 修改文件

```text
bin/cli.js
src/init/init-service.js
src/sync/sync-service.js
src/check/check-service.js
```

### 11.3 不建议修改

```text
package.json
prisma/
skill-q-platform/
br-ai-spec-visual/
```

---

## 12. 服务设计

### 12.1 IdeService

```ts
interface IdeSyncOptions {
  rootDir: string;
  ide: Array<"cursor" | "claude">;
  profile: "auto" | "react" | "vue";
  linkMode: "auto" | "copy" | "symlink";
  writeMemoryAnchor: boolean;
  writeAgentAnchor: boolean;
  dryRun: boolean;
  yes: boolean;
}

interface IdeSyncResult {
  writtenFiles: string[];
  skippedFiles: string[];
  repairedFiles: string[];
  linkModeUsed: "copy" | "symlink";
  warnings: string[];
}
```

### 12.2 IdeRegistryBuilder

职责：

1. 读取 `.ai-spec/project.json`。
2. 读取 `.ai-spec/workspace.json`。
3. 读取 `.ai-spec/ai-spec.lock.json`。
4. 读取 `.agents/registry/registry.index.json`。
5. 根据 profile 生成 IDE 消费索引。
6. 不读取业务源码正文。

### 12.3 MarkdownAnchorWriter

职责：

1. 只更新 `AI-SPEC-AUTO` 管理区块。
2. 保留用户原始内容。
3. 幂等写入。
4. 支持 dry-run。
5. 支持中文 diff 摘要。

### 12.4 SafeLinkWriter

职责：

1. 尝试 symlink。
2. 失败自动 copy。
3. 禁止覆盖非 AI 管理文件。
4. 记录降级原因。
5. 所有错误中文化。

---

## 13. 执行流程

### 13.1 `init --recommend --yes`

```text
1. 扫描项目技术栈。
2. 判断 React / Vue。
3. 写入 .ai-spec/project.json。
4. 写入 .ai-spec/workspace.json。
5. 写入 .ai-spec/policy.json。
6. 写入 .ai-spec/ai-spec.lock.json。
7. 写入 .agents/registry/registry.index.json。
8. 调用 ide sync。
9. 写入 .agents/registry/ide-registry.json。
10. 写入 .ai-spec/ide-integration.json。
11. 写入 .cursor / .claude 指针文件。
12. 写入 AGENTS.md / CLAUDE.md / memory.md 锚点。
13. 输出中文总结。
```

### 13.2 `ide sync`

```text
1. 校验项目是否已 init。
2. 校验 lock / registry / context-index 是否存在。
3. 生成 ide-registry。
4. 生成 cursor 指针。
5. 生成 claude 指针。
6. 注入 markdown anchors。
7. 校验所有路径存在。
8. 输出同步结果。
```

### 13.3 `ide doctor`

```text
1. 检查 .agents/registry/registry.index.json。
2. 检查 .agents/registry/ide-registry.json。
3. 检查 .ai-spec/context-index.json。
4. 检查 .ai-spec/ai-spec.lock.json。
5. 检查 .cursor/rules/ai-spec-auto.mdc。
6. 检查 .claude/ai-spec-auto.md。
7. 检查 AGENTS.md / CLAUDE.md / memory.md 锚点。
8. 输出缺失项和修复建议。
```

### 13.4 `ide repair`

```text
1. 执行 doctor。
2. 对缺失的 AI 管理文件执行补齐。
3. 不覆盖用户文件。
4. 输出修复结果。
```

---

## 14. Vue / React 真实项目接入策略

### 14.1 React 项目

建议验证项目：

```text
/Users/lizhenwei/workspace/reactworkspace/tian-zhi/bulldog
```

执行：

```bash
cd /Users/lizhenwei/workspace/vueworkspace/bairong/br-ai-spec

AI_SPEC_SKIP_LAUNCHER_SYNC=1 node bin/cli.js scan /Users/lizhenwei/workspace/reactworkspace/tian-zhi/bulldog --json

AI_SPEC_SKIP_LAUNCHER_SYNC=1 node bin/cli.js init /Users/lizhenwei/workspace/reactworkspace/tian-zhi/bulldog --recommend --dry-run

AI_SPEC_SKIP_LAUNCHER_SYNC=1 node bin/cli.js init /Users/lizhenwei/workspace/reactworkspace/tian-zhi/bulldog --recommend --yes

AI_SPEC_SKIP_LAUNCHER_SYNC=1 node bin/cli.js ide sync /Users/lizhenwei/workspace/reactworkspace/tian-zhi/bulldog --ide cursor,claude --profile react --link-mode auto --yes

AI_SPEC_SKIP_LAUNCHER_SYNC=1 node bin/cli.js ide doctor /Users/lizhenwei/workspace/reactworkspace/tian-zhi/bulldog
```

### 14.2 Vue 项目

建议验证项目：

```text
/Users/lizhenwei/workspace/vueworkspace/bairong/asset-cube-html
```

执行：

```bash
cd /Users/lizhenwei/workspace/vueworkspace/bairong/br-ai-spec

AI_SPEC_SKIP_LAUNCHER_SYNC=1 node bin/cli.js scan /Users/lizhenwei/workspace/vueworkspace/bairong/asset-cube-html --json

AI_SPEC_SKIP_LAUNCHER_SYNC=1 node bin/cli.js init /Users/lizhenwei/workspace/vueworkspace/bairong/asset-cube-html --recommend --dry-run

AI_SPEC_SKIP_LAUNCHER_SYNC=1 node bin/cli.js init /Users/lizhenwei/workspace/vueworkspace/bairong/asset-cube-html --recommend --yes

AI_SPEC_SKIP_LAUNCHER_SYNC=1 node bin/cli.js ide sync /Users/lizhenwei/workspace/vueworkspace/bairong/asset-cube-html --ide cursor,claude --profile vue --link-mode auto --yes

AI_SPEC_SKIP_LAUNCHER_SYNC=1 node bin/cli.js ide doctor /Users/lizhenwei/workspace/vueworkspace/bairong/asset-cube-html
```

---

## 15. 测试设计

### 15.1 单元测试

新增：

```text
tests/ide/ide-registry-builder.test.js
tests/ide/markdown-anchor-writer.test.js
tests/ide/cursor-adapter.test.js
tests/ide/claude-adapter.test.js
tests/ide/link-mode-resolver.test.js
tests/ide/ide-doctor.test.js
tests/ide/ide-sync.test.js
```

覆盖：

1. 生成 React ide-registry。
2. 生成 Vue ide-registry。
3. AGENTS.md 锚点幂等写入。
4. CLAUDE.md 锚点幂等写入。
5. memory.md 锚点幂等写入。
6. 不修改锚点外内容。
7. symlink 成功。
8. symlink 失败自动 copy。
9. copy 模式不创建 symlink。
10. Cursor 指针文件生成。
11. Claude 指针文件生成。
12. doctor 检出缺失文件。
13. repair 补齐缺失文件。
14. dry-run 不写文件。
15. 所有输出中文。

### 15.2 集成测试

新增：

```text
tests/ide/ide-sync-integration.test.js
tests/ide/react-real-project-fixture.test.js
tests/ide/vue-real-project-fixture.test.js
```

覆盖：

1. `init --recommend --yes` 后自动生成 IDE 指针。
2. `ide sync` 可重复执行。
3. `ide doctor` 通过。
4. `ide repair` 可修复被删除的指针文件。
5. React 项目 profile 正确。
6. Vue 项目 profile 正确。
7. 不修改业务源码。
8. 不修改 package.json。
9. 不写入敏感路径。
10. 不把完整 Rule / Skill 写入 memory。

---

## 16. 验收清单

```md
- [ ] 新增 `ide sync` 命令。
- [ ] 新增 `ide doctor` 命令。
- [ ] 新增 `ide repair` 命令。
- [ ] 生成 `.agents/registry/ide-registry.json`。
- [ ] 生成 `.ai-spec/ide-integration.json`。
- [ ] 生成 `.cursor/rules/ai-spec-auto.mdc`。
- [ ] 生成 `.cursor/commands/spec-start.md`。
- [ ] 生成 `.claude/ai-spec-auto.md`。
- [ ] 生成 `.claude/commands/spec-start.md`。
- [ ] `AGENTS.md` 支持 AI 锚点注入。
- [ ] `CLAUDE.md` 支持 AI 锚点注入。
- [ ] `memory.md` 支持 AI 锚点注入。
- [ ] 锚点写入幂等。
- [ ] 锚点外内容不被修改。
- [ ] 支持 `link-mode=auto`。
- [ ] 支持 `link-mode=copy`。
- [ ] 支持 `link-mode=symlink`。
- [ ] symlink 失败可自动降级 copy。
- [ ] React 项目可成功 `ide sync`。
- [ ] Vue 项目可成功 `ide sync`。
- [ ] `ide doctor` 可检查缺失项。
- [ ] `ide repair` 可修复缺失项。
- [ ] 不修改业务源码。
- [ ] 不修改 package.json。
- [ ] 不写入 sourceCode / rawPrompt / rawResponse / 绝对路径。
- [ ] 所有 CLI 输出中文。
- [ ] npm test 通过。
- [ ] node --check 通过。
```

---

## 17. Codex 一次性开发指令

```md
你现在是 `br-ai-spec` 项目的高级架构开发 Agent。

只修改项目：

/Users/lizhenwei/workspace/vueworkspace/bairong/br-ai-spec

目标：

只针对 `br-ai-spec` CLI 做 IDE Memory Pointer 与 Vue / React 真实项目前端接入优化。

本轮不修改：

1. skill-q-platform
2. br-ai-spec-visual
3. Hub 生产化功能
4. Visual 看板功能
5. AI 工程资产生成器
6. 后端多技术栈资产
7. 真实 Codex / Cursor / Claude Code 自动编码执行器

请实现：

1. 新增 `ide sync` 命令。
2. 新增 `ide doctor` 命令。
3. 新增 `ide repair` 命令。
4. 生成 `.agents/registry/ide-registry.json`。
5. 生成 `.ai-spec/ide-integration.json`。
6. 生成 `.cursor/rules/ai-spec-auto.mdc`。
7. 生成 `.cursor/commands/spec-start.md`。
8. 生成 `.cursor/commands/spec-update.md`。
9. 生成 `.cursor/commands/spec-status.md`。
10. 生成 `.claude/ai-spec-auto.md`。
11. 生成 `.claude/commands/spec-start.md`。
12. 生成 `.claude/commands/spec-update.md`。
13. 生成 `.claude/commands/spec-status.md`。
14. 在 `AGENTS.md` 写入 AI-SPEC-AUTO 管理锚点。
15. 在 `CLAUDE.md` 写入 AI-SPEC-AUTO 管理锚点。
16. 在 `memory.md` 写入 AI-SPEC-AUTO 管理锚点。
17. 所有锚点必须是 Pointer-only，不允许写入完整 Rule / Skill 正文。
18. 支持 `--link-mode auto|copy|symlink`。
19. 支持 `--ide cursor,claude`。
20. 支持 `--profile auto|react|vue`。
21. 支持 `--dry-run`。
22. 支持 `--yes`。
23. 所有输出、错误、提示必须为中文。
24. 不修改业务源码。
25. 不修改目标项目 package.json。
26. 不上传源码、原始提示词、原始响应、绝对路径或密钥。

建议新增目录：

src/ide/
  ide-command.js
  ide-service.js
  ide-plan.js
  ide-types.js
  registry/
  anchors/
  adapters/
  links/
  doctor/

必须补测试：

tests/ide/ide-registry-builder.test.js
tests/ide/markdown-anchor-writer.test.js
tests/ide/cursor-adapter.test.js
tests/ide/claude-adapter.test.js
tests/ide/link-mode-resolver.test.js
tests/ide/ide-doctor.test.js
tests/ide/ide-sync.test.js
tests/ide/ide-sync-integration.test.js

必须执行：

cd /Users/lizhenwei/workspace/vueworkspace/bairong/br-ai-spec

node --check bin/cli.js
find src bin tests -name "*.js" -print0 | xargs -0 -n1 node --check

node tests/ide/ide-registry-builder.test.js
node tests/ide/markdown-anchor-writer.test.js
node tests/ide/cursor-adapter.test.js
node tests/ide/claude-adapter.test.js
node tests/ide/link-mode-resolver.test.js
node tests/ide/ide-doctor.test.js
node tests/ide/ide-sync.test.js
node tests/ide/ide-sync-integration.test.js

npm test

真实项目前端验证：

AI_SPEC_SKIP_LAUNCHER_SYNC=1 node bin/cli.js scan /Users/lizhenwei/workspace/reactworkspace/tian-zhi/bulldog --json
AI_SPEC_SKIP_LAUNCHER_SYNC=1 node bin/cli.js init /Users/lizhenwei/workspace/reactworkspace/tian-zhi/bulldog --recommend --dry-run
AI_SPEC_SKIP_LAUNCHER_SYNC=1 node bin/cli.js ide sync /Users/lizhenwei/workspace/reactworkspace/tian-zhi/bulldog --ide cursor,claude --profile react --link-mode auto --dry-run

AI_SPEC_SKIP_LAUNCHER_SYNC=1 node bin/cli.js scan /Users/lizhenwei/workspace/vueworkspace/bairong/asset-cube-html --json
AI_SPEC_SKIP_LAUNCHER_SYNC=1 node bin/cli.js init /Users/lizhenwei/workspace/vueworkspace/bairong/asset-cube-html --recommend --dry-run
AI_SPEC_SKIP_LAUNCHER_SYNC=1 node bin/cli.js ide sync /Users/lizhenwei/workspace/vueworkspace/bairong/asset-cube-html --ide cursor,claude --profile vue --link-mode auto --dry-run

完成后输出：

1. 修改文件列表。
2. 新增文件列表。
3. 新增 CLI 命令。
4. 新增 IDE 指针文件。
5. AGENTS.md / CLAUDE.md / memory.md 注入策略。
6. 是否修改 package.json。
7. 是否修改业务源码。
8. 测试命令。
9. 测试结果。
10. 真实 React 项目 dry-run 结果。
11. 真实 Vue 项目 dry-run 结果。
12. 是否可以进入真实项目 `init --yes` 试点。
```

---

## 18. 最终判断

这轮优化做完后，`br-ai-spec` 才真正适合先在 Vue / React 前端真实项目中使用。

它解决的是：

```text
资产已经装进项目，但 IDE / Agent 不知道怎么稳定读取的问题。
```

本轮不追求自动编码闭环，而是先把：

```text
规则入口统一
技能入口统一
命令入口统一
记忆入口统一
上下文索引统一
```

这五件事做好。
