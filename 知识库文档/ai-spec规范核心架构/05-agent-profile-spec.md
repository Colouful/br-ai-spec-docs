# Agent Profile 规范文档

> 文档用途：作为扣子知识库 `hub-asset-schema` 和 `ai-spec-core-architecture` 的 Agent Profile 事实源，用于生成、审核、导入和消费执行代理画像。

---

## 1. Agent Profile 定位

Agent Profile 是 AI 工程资产系统中的执行代理画像，用于描述某一类技术栈、任务场景、执行器组合、工具权限、上下文策略和审批策略。

它解决的问题：

1. 使用哪个执行器。
2. 可回退到哪些执行器。
3. 允许使用哪些工具。
4. 禁止使用哪些工具。
5. 可以加载哪些上下文。
6. 哪些动作需要审批。
7. 出现风险时如何兜底。

---

## 2. 与执行器关系

Agent Profile 不等于执行器。

```text
Agent Profile
  ├── defaultExecutor: cursor
  ├── fallbackExecutors: claude-code / codex
  ├── allowedTools
  ├── deniedTools
  ├── contextScope
  └── approvalPolicy
```

执行器必须可插拔：

1. Codex。
2. Cursor。
3. Claude Code。

禁止将某一个执行器写死为唯一执行器。

---

## 3. 使用场景

Agent Profile 适合表达：

1. 前端开发专家。
2. 后端开发专家。
3. 全栈契约专家。
4. 诊断专家。
5. Review 专家。
6. 测试专家。
7. 文档生成专家。
8. 远程任务执行专家。

---

## 4. 命名规范

slug 示例：

```text
frontend-local-assisted-agent-profile
backend-java-spring-agent-profile
backend-python-fastapi-agent-profile
backend-rust-axum-agent-profile
fullstack-contract-agent-profile
diagnostic-agent-profile
review-agent-profile
```

---

## 5. Agent Profile Schema

```json
{
  "schemaVersion": "1.0.0",
  "kind": "agent-profile",
  "slug": "frontend-local-assisted-agent-profile",
  "name": "前端本地辅助开发执行画像",
  "description": "适用于前端本地人工辅助开发模式的执行代理画像。",
  "version": "1.0.0",
  "status": "draft",
  "scope": "platform",
  "riskLevel": "medium",
  "applicableTechStacks": [
    {
      "domain": "frontend",
      "language": ["TypeScript", "JavaScript"],
      "frameworks": ["React", "Vue", "Next.js"],
      "projectKinds": ["application", "monorepo"]
    }
  ],
  "execution": {
    "mode": "local-assisted",
    "defaultExecutor": "cursor",
    "fallbackExecutors": ["claude-code", "codex"],
    "executorSelectionStrategy": "policy-first",
    "timeoutSeconds": 1800,
    "maxRetries": 1
  },
  "allowedTools": [
    "read-file",
    "write-file",
    "run-test",
    "run-lint",
    "run-typecheck",
    "git-diff"
  ],
  "deniedTools": [
    "upload-source",
    "upload-secret",
    "deploy",
    "push",
    "merge",
    "delete-repository"
  ],
  "contextScope": {
    "allowSourceCodeUpload": false,
    "allowRawPromptUpload": false,
    "allowRawResponseUpload": false,
    "allowAbsolutePathUpload": false,
    "loadingStrategy": "progressive",
    "requiredOverlays": [],
    "allowedContextKinds": ["rule", "skill", "role", "flow", "agent-profile", "contract"],
    "deniedContextKinds": ["source-code", "secret", "env-file"]
  },
  "approvalPolicy": {
    "beforeWrite": true,
    "beforePush": true,
    "beforeMerge": true,
    "beforePublish": true,
    "beforeDeploy": true,
    "beforeInstallDependency": true
  },
  "stateMachinePolicy": {
    "onExecutorTimeout": "suspended",
    "onRepeatedFailure": "diagnosing",
    "onRiskyChange": "human-review",
    "onSecurityRisk": "block"
  },
  "telemetry": {
    "telemetryTags": ["executor-adapter", "frontend"],
    "reportUsage": true,
    "reportFailureSummary": true,
    "reportTokenSummary": true,
    "reportSourceCode": false
  },
  "quality": {
    "score": 92,
    "checks": [],
    "warnings": []
  }
}
```

---

## 6. 字段说明

### 6.1 execution

| 字段 | 说明 |
|---|---|
| mode | local-assisted / local-auto / remote-orchestrated |
| defaultExecutor | 默认执行器 |
| fallbackExecutors | 备用执行器 |
| executorSelectionStrategy | 执行器选择策略 |
| timeoutSeconds | 超时时间 |
| maxRetries | 最大重试次数 |

### 6.2 allowedTools

允许工具。

常见：

```text
read-file
write-file
run-test
run-lint
run-typecheck
git-diff
git-status
```

### 6.3 deniedTools

必须默认禁止：

```text
upload-source
upload-secret
deploy
push
merge
delete-repository
```

### 6.4 contextScope

上下文范围控制。

必须默认：

```json
{
  "allowSourceCodeUpload": false,
  "allowRawPromptUpload": false,
  "allowRawResponseUpload": false,
  "allowAbsolutePathUpload": false,
  "loadingStrategy": "progressive"
}
```

### 6.5 approvalPolicy

审批策略。

高风险操作必须审批：

1. 写文件。
2. push。
3. merge。
4. publish。
5. deploy。
6. install dependency。

---

## 7. 执行模式

### 7.1 local-assisted

适合：

1. Cursor。
2. 人工参与较多。
3. 开发者本地确认变更。

推荐：

```json
{
  "mode": "local-assisted",
  "defaultExecutor": "cursor",
  "fallbackExecutors": ["claude-code", "codex"]
}
```

### 7.2 local-auto

适合：

1. Codex。
2. 可自动执行测试。
3. 仍需本地隔离 worktree。

推荐：

```json
{
  "mode": "local-auto",
  "defaultExecutor": "codex",
  "fallbackExecutors": ["claude-code", "cursor"]
}
```

### 7.3 remote-orchestrated

适合未来 OpenClaw / 钉钉 / 远程调度入口。

推荐：

```json
{
  "mode": "remote-orchestrated",
  "defaultExecutor": "codex",
  "fallbackExecutors": ["claude-code"]
}
```

---

## 8. 默认执行器推荐

| 场景 | defaultExecutor | fallbackExecutors |
|---|---|---|
| 本地辅助开发 | cursor | claude-code, codex |
| 本地自动开发 | codex | claude-code, cursor |
| 复杂长任务 | claude-code | codex, cursor |
| 远程任务调度 | codex | claude-code |
| Review | cursor | claude-code |
| 诊断 | claude-code | codex |

---

## 9. 前端 Agent Profile 示例

```json
{
  "schemaVersion": "1.0.0",
  "kind": "agent-profile",
  "slug": "frontend-react-agent-profile",
  "name": "React 前端开发执行画像",
  "description": "适用于 React / Vite / Next.js 项目的本地辅助开发。",
  "version": "1.0.0",
  "status": "draft",
  "scope": "platform",
  "riskLevel": "medium",
  "applicableTechStacks": [
    {
      "domain": "frontend",
      "language": ["TypeScript"],
      "frameworks": ["React", "Vite", "Next.js"],
      "projectKinds": ["application", "monorepo"]
    }
  ],
  "execution": {
    "mode": "local-assisted",
    "defaultExecutor": "cursor",
    "fallbackExecutors": ["claude-code", "codex"],
    "executorSelectionStrategy": "policy-first",
    "timeoutSeconds": 1800,
    "maxRetries": 1
  },
  "allowedTools": ["read-file", "write-file", "run-test", "run-lint", "run-typecheck", "git-diff"],
  "deniedTools": ["upload-source", "upload-secret", "deploy", "push", "merge"],
  "contextScope": {
    "allowSourceCodeUpload": false,
    "allowRawPromptUpload": false,
    "allowRawResponseUpload": false,
    "allowAbsolutePathUpload": false,
    "loadingStrategy": "progressive",
    "requiredOverlays": [],
    "allowedContextKinds": ["rule", "skill", "role", "flow", "agent-profile", "contract"],
    "deniedContextKinds": ["source-code", "secret", "env-file"]
  },
  "approvalPolicy": {
    "beforeWrite": true,
    "beforePush": true,
    "beforeMerge": true,
    "beforePublish": true,
    "beforeDeploy": true,
    "beforeInstallDependency": true
  },
  "quality": {
    "score": 94,
    "checks": ["执行器可回退", "上下文策略渐进式", "安全限制完整"],
    "warnings": []
  }
}
```

---

## 10. 后端 Agent Profile 示例

```json
{
  "schemaVersion": "1.0.0",
  "kind": "agent-profile",
  "slug": "backend-python-fastapi-agent-profile",
  "name": "FastAPI 后端开发执行画像",
  "description": "适用于 Python FastAPI 后端开发的执行代理画像。",
  "version": "1.0.0",
  "status": "draft",
  "scope": "platform",
  "riskLevel": "medium",
  "applicableTechStacks": [
    {
      "domain": "backend",
      "language": ["Python"],
      "frameworks": ["FastAPI"],
      "projectKinds": ["application", "monorepo"]
    }
  ],
  "execution": {
    "mode": "local-assisted",
    "defaultExecutor": "cursor",
    "fallbackExecutors": ["claude-code", "codex"],
    "executorSelectionStrategy": "policy-first",
    "timeoutSeconds": 1800,
    "maxRetries": 1
  },
  "allowedTools": ["read-file", "write-file", "run-test", "run-lint", "git-diff"],
  "deniedTools": ["upload-source", "upload-secret", "deploy", "push", "merge"],
  "contextScope": {
    "allowSourceCodeUpload": false,
    "allowRawPromptUpload": false,
    "allowRawResponseUpload": false,
    "allowAbsolutePathUpload": false,
    "loadingStrategy": "progressive",
    "allowedContextKinds": ["rule", "skill", "role", "flow", "agent-profile", "contract"],
    "deniedContextKinds": ["source-code", "secret", "env-file"]
  },
  "approvalPolicy": {
    "beforeWrite": true,
    "beforePush": true,
    "beforeMerge": true,
    "beforePublish": true,
    "beforeDeploy": true,
    "beforeInstallDependency": true
  },
  "quality": {
    "score": 90,
    "checks": [],
    "warnings": []
  }
}
```

---

## 11. 诊断 Agent Profile 示例

```json
{
  "schemaVersion": "1.0.0",
  "kind": "agent-profile",
  "slug": "diagnostic-agent-profile",
  "name": "异常诊断执行画像",
  "description": "用于构建失败、测试失败、上下文超预算、执行器超时等异常场景的诊断。",
  "version": "1.0.0",
  "status": "draft",
  "scope": "platform",
  "riskLevel": "low",
  "applicableTechStacks": [
    {
      "domain": "fullstack",
      "language": ["JavaScript", "TypeScript", "Java", "Python", "Go", "Rust"],
      "frameworks": [],
      "projectKinds": ["application", "monorepo", "multi-project-workspace"]
    }
  ],
  "execution": {
    "mode": "local-assisted",
    "defaultExecutor": "claude-code",
    "fallbackExecutors": ["codex", "cursor"],
    "executorSelectionStrategy": "diagnostic-first",
    "timeoutSeconds": 1200,
    "maxRetries": 0
  },
  "allowedTools": ["read-file", "run-test", "run-lint", "run-typecheck", "git-diff"],
  "deniedTools": ["write-file", "upload-source", "deploy", "push", "merge"],
  "contextScope": {
    "allowSourceCodeUpload": false,
    "allowRawPromptUpload": false,
    "allowRawResponseUpload": false,
    "allowAbsolutePathUpload": false,
    "loadingStrategy": "progressive",
    "allowedContextKinds": ["rule", "skill", "flow", "agent-profile"],
    "deniedContextKinds": ["source-code", "secret", "env-file"]
  },
  "approvalPolicy": {
    "beforeWrite": true,
    "beforePush": true,
    "beforeMerge": true,
    "beforePublish": true,
    "beforeDeploy": true,
    "beforeInstallDependency": true
  },
  "quality": {
    "score": 92,
    "checks": ["禁止写文件", "禁止上传源码", "适合诊断场景"],
    "warnings": []
  }
}
```

---

## 12. 校验清单

Agent Profile 进入 Hub 审核前必须满足：

- [ ] kind = agent-profile。
- [ ] slug 合法。
- [ ] version 合法。
- [ ] status = draft。
- [ ] defaultExecutor 合法。
- [ ] fallbackExecutors 至少 1 个。
- [ ] 不把某执行器写死为唯一执行器。
- [ ] deniedTools 包含 upload-source。
- [ ] deniedTools 包含 deploy。
- [ ] deniedTools 包含 push。
- [ ] deniedTools 包含 merge。
- [ ] allowSourceCodeUpload = false。
- [ ] allowRawPromptUpload = false。
- [ ] allowRawResponseUpload = false。
- [ ] loadingStrategy = progressive。
- [ ] beforeWrite = true。
- [ ] beforePush = true。
- [ ] beforePublish = true。
- [ ] 不包含源码级业务代码。
- [ ] 质量分 >= 80。

---

## 13. 错误码

| code | 说明 | 处理建议 |
|---|---|---|
| AGENT_EXECUTOR_INVALID | defaultExecutor 非法 | 使用 cursor / claude-code / codex |
| AGENT_FALLBACK_EMPTY | fallbackExecutors 为空 | 至少配置一个备用执行器 |
| AGENT_DENIED_TOOL_MISSING | 必要禁止工具缺失 | 补充 upload-source / deploy / push / merge |
| AGENT_CONTEXT_UPLOAD_RISK | 上下文上传策略有风险 | 将源码上传相关字段改为 false |
| AGENT_LOADING_STRATEGY_INVALID | 上下文加载策略非法 | 使用 progressive |
| AGENT_APPROVAL_POLICY_WEAK | 审批策略过弱 | 补充 beforeWrite / beforePush / beforePublish |
| AGENT_SCORE_TOO_LOW | 质量分过低 | 补充字段与约束 |

---

## 14. 知识库使用建议

建议将本文放入扣子知识库：

```text
知识库名称：hub-asset-schema
文档名称：Agent Profile 规范文档
用途：供 AI Asset Factory Agent 生成 Agent Profile、检查执行器策略、生成 Hub 导入 JSON。
```
