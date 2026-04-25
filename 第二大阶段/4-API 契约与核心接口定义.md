# 四、API 契约与核心接口定义

> 本章节定义三类接口：
>
> 1. `skill-q-platform` 对外提供的 Hub API。
> 2. `br-ai-spec-visual` 提供的运行态采集 API。
> 3. `br-ai-spec` 内部核心接口，包括 Scanner、Context Builder、State Machine、Executor Adapter。
>
> 最高约束：
>
> * REST API 返回值必须统一。
> * Error Code 必须可枚举、可定位、可修复。
> * Codex IDE、Cursor、Claude Code 必须通过统一 `IExecutorProvider` 接入。
> * API 不允许接收目标项目源码正文。
> * API 不允许接收完整 prompt / response。

---

# 4.1 全局 API 设计原则

## 4.1.1 统一响应结构

所有 REST API 必须返回统一结构：

```ts
export interface ApiResponse<T> {
  code: number;
  message: string;
  data?: T;
  error?: ApiErrorDetail;
  requestId: string;
  timestamp: string;
}
```

示例：

```json
{
  "code": 0,
  "message": "操作成功",
  "data": {},
  "requestId": "req_20260425_001",
  "timestamp": "2026-04-25T10:00:00.000Z"
}
```

错误示例：

```json
{
  "code": 400101,
  "message": "Manifest 不存在",
  "error": {
    "errorCode": "MANIFEST_NOT_FOUND",
    "details": {
      "manifestSlug": "backend-java-springboot-standard",
      "version": "1.0.0"
    },
    "suggestion": "请检查 Manifest 标识是否正确，或在 Hub 中发布该 Manifest。"
  },
  "requestId": "req_20260425_002",
  "timestamp": "2026-04-25T10:00:00.000Z"
}
```

---

## 4.1.2 Error Detail 结构

```ts
export interface ApiErrorDetail {
  errorCode: string;
  details?: Record<string, unknown>;
  suggestion?: string;
  docsUrl?: string;
}
```

---

## 4.1.3 分页结构

```ts
export interface PageRequest {
  page: number;
  pageSize: number;
}

export interface PageResponse<T> {
  list: T[];
  page: number;
  pageSize: number;
  total: number;
}
```

---

## 4.1.4 API 鉴权约定

所有 Hub / Visual API 均支持：

```http
Authorization: Bearer <token>
```

CLI 使用：

```text
~/.ai-spec-auto/config.json 中的 tokenRef
```

示例：

```json
{
  "defaultHub": {
    "url": "https://hub.example.com",
    "tokenRef": "AI_SPEC_HUB_TOKEN"
  }
}
```

实现要求：

```text
1. tokenRef 只保存环境变量名，不保存明文 token。
2. CLI 请求前从 process.env[tokenRef] 读取 token。
3. 如果 token 缺失，必须给出中文错误提示和修复建议。
```

---

# 4.2 全局 Error Codes 枚举字典

## 4.2.1 通用错误

|   Code | ErrorCode         | 说明     |
| -----: | ----------------- | ------ |
|      0 | OK                | 成功     |
| 400000 | BAD_REQUEST       | 请求参数错误 |
| 400001 | VALIDATION_FAILED | 参数校验失败 |
| 401000 | UNAUTHORIZED      | 未认证    |
| 403000 | FORBIDDEN         | 无权限    |
| 404000 | NOT_FOUND         | 资源不存在  |
| 409000 | CONFLICT          | 资源冲突   |
| 429000 | RATE_LIMITED      | 请求过于频繁 |
| 500000 | INTERNAL_ERROR    | 服务内部错误 |

---

## 4.2.2 Hub 资产错误

|   Code | ErrorCode                  | 说明                    |
| -----: | -------------------------- | --------------------- |
| 400101 | MANIFEST_NOT_FOUND         | Manifest 不存在          |
| 400102 | MANIFEST_VERSION_NOT_FOUND | Manifest 版本不存在        |
| 400103 | MANIFEST_NOT_PUBLISHED     | Manifest 未发布          |
| 400104 | MANIFEST_CHECKSUM_MISMATCH | Manifest checksum 不一致 |
| 400105 | MANIFEST_ASSET_MISSING     | Manifest 引用的资产不存在     |
| 400106 | MANIFEST_EXPORT_FAILED     | Manifest 导出失败         |
| 400201 | ASSET_NOT_FOUND            | 资产不存在                 |
| 400202 | ASSET_VERSION_NOT_FOUND    | 资产版本不存在               |
| 400203 | ASSET_NOT_PUBLISHED        | 资产未发布                 |
| 400204 | ASSET_CHECKSUM_MISMATCH    | 资产 checksum 不一致       |
| 400205 | ASSET_IMMUTABLE            | 已发布资产不可修改             |
| 400206 | ASSET_SCOPE_FORBIDDEN      | 无权访问该作用域资产            |
| 400207 | ASSET_DEPENDENCY_MISSING   | 资产依赖缺失                |
| 400208 | ASSET_QUALITY_BLOCKED      | 资产质量不达标，阻断导入          |

---

## 4.2.3 Agent Profile 错误

|   Code | ErrorCode                       | 说明                  |
| -----: | ------------------------------- | ------------------- |
| 400301 | AGENT_PROFILE_NOT_FOUND         | Agent Profile 不存在   |
| 400302 | AGENT_PROFILE_VERSION_NOT_FOUND | Agent Profile 版本不存在 |
| 400303 | AGENT_EXECUTOR_UNSUPPORTED      | Agent 指定的执行器不支持     |
| 400304 | AGENT_TOOL_DENIED               | Agent 请求了被禁用的工具     |
| 400305 | AGENT_OUTPUT_CONTRACT_INVALID   | Agent 输出不符合契约       |
| 400306 | AGENT_RISK_REQUIRES_REVIEW      | Agent 风险等级需要人工审批    |

---

## 4.2.4 CLI / 项目侧错误

|   Code | ErrorCode                 | 说明                                |
| -----: | ------------------------- | --------------------------------- |
| 410001 | PROJECT_CONFIG_NOT_FOUND  | `.ai-spec/project.json` 不存在       |
| 410002 | POLICY_CONFIG_NOT_FOUND   | `.ai-spec/policy.json` 不存在        |
| 410003 | LOCK_FILE_NOT_FOUND       | `.ai-spec/ai-spec.lock.json` 不存在  |
| 410004 | REGISTRY_INDEX_NOT_FOUND  | `.agents/registry.index.json` 不存在 |
| 410005 | CONTEXT_INDEX_NOT_FOUND   | `.ai-spec/context-index.json` 不存在 |
| 410006 | ASSET_TAMPERED            | 检测到资产被篡改                          |
| 410007 | PROJECT_OVERLAY_INVALID   | Project Overlay 不合法               |
| 410008 | SHARED_CONTRACT_NOT_FOUND | 共享业务模型规范不存在                       |
| 410009 | DIRTY_WORKING_TREE        | 当前工作区存在未提交修改                      |
| 410010 | WORKTREE_CREATE_FAILED    | Worktree 创建失败                     |
| 410011 | BRANCH_CREATE_FAILED      | 分支创建失败                            |
| 410012 | INVALID_STATE_TRANSITION  | 非法状态流转                            |
| 410013 | TOKEN_BUDGET_EXCEEDED     | Token 预算超限                        |
| 410014 | CIRCUIT_BREAKER_TRIGGERED | 熔断器触发                             |
| 410015 | EXECUTOR_NOT_AVAILABLE    | 执行器不可用                            |
| 410016 | EXECUTOR_TIMEOUT          | 执行器超时                             |
| 410017 | EXECUTOR_RESULT_INVALID   | 执行器返回结果不合法                        |
| 410018 | CONTEXT_BUILD_FAILED      | 上下文构建失败                           |
| 410019 | SCAN_LOW_CONFIDENCE       | 技术栈识别置信度过低                        |
| 410020 | SOURCE_UPLOAD_FORBIDDEN   | 禁止上传目标项目源码                        |

---

## 4.2.5 Visual 采集错误

|   Code | ErrorCode                  | 说明             |
| -----: | -------------------------- | -------------- |
| 420001 | VISUAL_WORKSPACE_NOT_FOUND | Workspace 不存在  |
| 420002 | VISUAL_PROJECT_NOT_FOUND   | Project 不存在    |
| 420003 | RUNTIME_EVENT_DUPLICATED   | 运行事件重复         |
| 420004 | RUNTIME_EVENT_INVALID      | 运行事件格式错误       |
| 420005 | PRIVACY_POLICY_VIOLATED    | 上报数据违反隐私策略     |
| 420006 | HISTORY_PAYLOAD_INVALID    | History 摘要格式错误 |
| 420007 | INCIDENT_PAYLOAD_INVALID   | Incident 格式错误  |

---

# 4.3 `skill-q-platform` Hub API 契约

---

# 4.3.1 Manifest 推荐 API

## 4.3.1.1 说明

`br-ai-spec init --recommend` 调用该接口，根据扫描结果请求 Hub 推荐 Manifest。

```http
POST /api/hub/manifests/recommend
```

---

## 4.3.1.2 Request Payload

```json
{
  "workspace": {
    "workspaceId": "ws_user_center",
    "type": "monorepo"
  },
  "projectFacts": [
    {
      "packageId": "pkg_web",
      "relativePath": "apps/web",
      "domain": "frontend",
      "language": ["TypeScript"],
      "frameworks": ["Next.js", "React"],
      "buildTool": "Next.js",
      "packageManager": "pnpm",
      "confidence": 95,
      "tags": ["app-router", "tailwind"],
      "reasons": [
        "检测到 next 依赖",
        "检测到 next.config.js",
        "检测到 src/app/layout.tsx"
      ]
    },
    {
      "packageId": "pkg_api",
      "relativePath": "services/api",
      "domain": "backend",
      "language": ["Java"],
      "frameworks": ["Spring Boot"],
      "buildTool": "Maven",
      "orm": ["MyBatis"],
      "confidence": 90,
      "tags": ["mysql", "mybatis"],
      "reasons": [
        "检测到 pom.xml",
        "检测到 spring-boot-starter-web",
        "检测到 application.yml"
      ]
    }
  ],
  "org": {
    "orgId": "org_company",
    "teamId": "team_frontend_1"
  }
}
```

---

## 4.3.1.3 Response Payload

```json
{
  "code": 0,
  "message": "推荐成功",
  "data": {
    "recommendations": [
      {
        "packageId": "pkg_web",
        "manifest": {
          "slug": "frontend-react-nextjs-standard",
          "name": "Next.js / React 标准研发方案包",
          "version": "1.0.0",
          "scope": "platform",
          "checksum": "sha256_manifest_web"
        },
        "score": 95,
        "risk": "low",
        "reasons": [
          "检测到 Next.js 依赖",
          "检测到 App Router 目录",
          "检测到 TypeScript"
        ],
        "requiresConfirmation": false
      },
      {
        "packageId": "pkg_api",
        "manifest": {
          "slug": "backend-java-springboot-standard",
          "name": "Java Spring Boot 标准研发方案包",
          "version": "1.0.0",
          "scope": "platform",
          "checksum": "sha256_manifest_api"
        },
        "score": 92,
        "risk": "low",
        "reasons": [
          "检测到 Spring Boot Web",
          "检测到 Maven",
          "检测到 MyBatis"
        ],
        "requiresConfirmation": false
      }
    ]
  },
  "requestId": "req_xxx",
  "timestamp": "2026-04-25T10:00:00.000Z"
}
```

---

## 4.3.1.4 错误码

|   Code | ErrorCode          | 说明             |
| -----: | ------------------ | -------------- |
| 400001 | VALIDATION_FAILED  | 请求参数错误         |
| 400101 | MANIFEST_NOT_FOUND | 未找到匹配 Manifest |
| 403000 | FORBIDDEN          | 无权限访问该团队资产     |

---

# 4.3.2 Manifest Export API

## 4.3.2.1 说明

`br-ai-spec init / sync` 调用该接口获取 Manifest 及其引用资产索引。

```http
GET /api/hub/manifests/:slug/export?version=1.0.0
```

---

## 4.3.2.2 Path 参数

| 参数     | 类型     | 必填 | 说明          |
| ------ | ------ | -- | ----------- |
| `slug` | string | 是  | Manifest 标识 |

---

## 4.3.2.3 Query 参数

| 参数        | 类型     | 必填 | 说明                                 |
| --------- | ------ | -- | ---------------------------------- |
| `version` | string | 否  | 版本号，不传则取 current published version |
| `scope`   | string | 否  | 资产作用域                              |
| `teamId`  | string | 否  | 团队 ID                              |

---

## 4.3.2.4 Response Payload

```json
{
  "code": 0,
  "message": "导出成功",
  "data": {
    "schemaVersion": "1.0.0",
    "exportedAt": "2026-04-25T10:00:00.000Z",
    "hub": {
      "url": "https://hub.example.com",
      "manifestExportApi": "/api/hub/manifests/backend-java-springboot-standard/export"
    },
    "manifest": {
      "slug": "backend-java-springboot-standard",
      "name": "Java Spring Boot 标准研发方案包",
      "version": "1.0.0",
      "checksum": "sha256_manifest_xxx",
      "domain": "backend",
      "language": "Java",
      "frameworks": ["Spring Boot"],
      "scenarios": ["new-rest-api", "modify-rest-api", "bugfix"]
    },
    "assets": [
      {
        "kind": "rule",
        "slug": "springboot-controller-rule",
        "name": "Spring Boot Controller 编写规范",
        "version": "1.0.0",
        "checksum": "sha256_asset_xxx",
        "contentUrl": "/api/hub/assets/springboot-controller-rule/content?version=1.0.0",
        "summary": "Controller 层只负责请求参数、响应、参数校验，不写业务逻辑。",
        "required": true,
        "loadWhen": ["implementation", "review"]
      },
      {
        "kind": "agent-profile",
        "slug": "backend-implementer-agent",
        "name": "后端实现执行代理",
        "version": "1.0.0",
        "checksum": "sha256_agent_xxx",
        "contentUrl": "/api/hub/agent-profiles/backend-implementer-agent/export?version=1.0.0",
        "summary": "使用 Claude Code / Codex 执行 Spring Boot 后端实现任务。",
        "required": true,
        "loadWhen": ["implementation"]
      }
    ],
    "installPolicy": {
      "requirePreview": true,
      "allowOverwrite": false,
      "allowLocalPatch": true,
      "defaultExecutionMode": "local-assisted",
      "defaultExecutor": "cursor"
    }
  },
  "requestId": "req_xxx",
  "timestamp": "2026-04-25T10:00:00.000Z"
}
```

---

## 4.3.2.5 错误码

|   Code | ErrorCode                  | 说明              |
| -----: | -------------------------- | --------------- |
| 400101 | MANIFEST_NOT_FOUND         | Manifest 不存在    |
| 400102 | MANIFEST_VERSION_NOT_FOUND | 指定版本不存在         |
| 400103 | MANIFEST_NOT_PUBLISHED     | Manifest 未发布    |
| 400105 | MANIFEST_ASSET_MISSING     | Manifest 引用资产缺失 |

---

# 4.3.3 Asset Content API

## 4.3.3.1 说明

`br-ai-spec sync` 根据 Manifest Export 中的 `contentUrl` 拉取资产正文并缓存到 `~/.ai-spec-auto/cache/assets/`。

```http
GET /api/hub/assets/:slug/content?version=1.0.0
```

---

## 4.3.3.2 Response Payload

```json
{
  "code": 0,
  "message": "获取资产内容成功",
  "data": {
    "kind": "rule",
    "slug": "springboot-controller-rule",
    "name": "Spring Boot Controller 编写规范",
    "version": "1.0.0",
    "contentFormat": "markdown",
    "content": "# Spring Boot Controller 编写规范\n\n## 1. 规则目的\n...",
    "checksum": "sha256_asset_xxx",
    "immutable": true,
    "dependencies": [],
    "qualityScore": 96
  },
  "requestId": "req_xxx",
  "timestamp": "2026-04-25T10:00:00.000Z"
}
```

---

## 4.3.3.3 错误码

|   Code | ErrorCode               | 说明      |
| -----: | ----------------------- | ------- |
| 400201 | ASSET_NOT_FOUND         | 资产不存在   |
| 400202 | ASSET_VERSION_NOT_FOUND | 资产版本不存在 |
| 400203 | ASSET_NOT_PUBLISHED     | 资产未发布   |
| 400206 | ASSET_SCOPE_FORBIDDEN   | 无权访问资产  |

---

# 4.3.4 Agent Profile Export API

## 4.3.4.1 说明

获取 Agent Profile 的执行配置。

```http
GET /api/hub/agent-profiles/:slug/export?version=1.0.0
```

---

## 4.3.4.2 Response Payload

```json
{
  "code": 0,
  "message": "获取 Agent Profile 成功",
  "data": {
    "kind": "agent-profile",
    "slug": "backend-implementer-agent",
    "name": "后端实现执行代理",
    "version": "1.0.0",
    "role": "backend-implementer",
    "defaultExecutor": "claude-code",
    "fallbackExecutors": ["codex", "cursor"],
    "modelPolicy": {
      "preferredProviders": ["claude", "openai", "qwen"],
      "contextStrategy": "progressive",
      "tokenBudget": 80000,
      "maxOutputTokens": 12000,
      "temperature": 0.2
    },
    "allowedTools": ["read", "write", "shell", "test"],
    "deniedTools": [
      "deploy",
      "delete-database",
      "upload-source",
      "push-without-approval"
    ],
    "contextScope": {
      "rules": [
        "backend-api-contract-rule",
        "springboot-controller-rule"
      ],
      "skills": [
        "springboot-rest-api-implementation-skill"
      ],
      "flows": [
        "springboot-new-rest-api-flow"
      ],
      "maxAssets": 8,
      "allowProjectOverlay": true,
      "allowSharedContracts": true
    },
    "approvalPolicy": {
      "beforeCodeChange": false,
      "beforeCommit": true,
      "beforePush": true,
      "beforeMerge": true
    },
    "outputContract": {
      "mustReturn": [
        "summary",
        "changedFiles",
        "testResult",
        "riskList",
        "nextActions"
      ]
    },
    "riskLevel": "L1",
    "checksum": "sha256_agent_profile_xxx"
  },
  "requestId": "req_xxx",
  "timestamp": "2026-04-25T10:00:00.000Z"
}
```

---

# 4.3.5 Install Record API

## 4.3.5.1 说明

`br-ai-spec init / sync` 成功或失败后上报安装记录。

```http
POST /api/hub/install-records
```

---

## 4.3.5.2 Request Payload

```json
{
  "projectId": "proj_8f3a9c2e",
  "workspaceId": "ws_user_center",
  "projectName": "user-api",
  "projectHash": "sha256_project_xxx",
  "packagePath": "services/user-api",
  "hubUrl": "https://hub.example.com",
  "manifestSlug": "backend-java-springboot-standard",
  "manifestVersion": "1.0.0",
  "manifestChecksum": "sha256_manifest_xxx",
  "executor": "claude-code",
  "installMode": "standard",
  "status": "succeeded",
  "metadata": {
    "domain": "backend",
    "language": "Java",
    "frameworks": ["Spring Boot"],
    "assetsCount": 18
  }
}
```

---

## 4.3.5.3 Response Payload

```json
{
  "code": 0,
  "message": "安装记录已保存",
  "data": {
    "recordId": "install_001"
  },
  "requestId": "req_xxx",
  "timestamp": "2026-04-25T10:00:00.000Z"
}
```

---

# 4.3.6 Hub Runtime Feedback API

## 4.3.6.1 说明

接收 `br-ai-spec` 或 `br-ai-spec-visual` 回流的资产使用效果。

```http
POST /api/hub/runtime-feedback
```

---

## 4.3.6.2 Request Payload

```json
{
  "eventId": "evt_20260425_001",
  "projectId": "proj_8f3a9c2e",
  "projectHash": "sha256_project_xxx",
  "manifestSlug": "backend-java-springboot-standard",
  "manifestVersion": "1.0.0",
  "assetKind": "skill",
  "assetSlug": "springboot-rest-api-implementation-skill",
  "assetVersion": "1.0.0",
  "agentProfileSlug": "backend-implementer-agent",
  "executor": "claude-code",
  "eventType": "executor_completed",
  "stage": "implementation",
  "success": true,
  "durationMs": 120000,
  "payload": {
    "changedFilesCount": 5,
    "testPassed": true,
    "autoFixCount": 0
  }
}
```

---

## 4.3.6.3 安全约束

`payload` 不允许包含：

```text
源码正文
完整 prompt
完整 response
绝对路径
用户名
密钥
Token
```

---

# 4.3.7 Asset Factory API

---

## 4.3.7.1 创建生成任务

```http
POST /api/asset-factory/jobs
```

### Request Payload

```json
{
  "name": "生成 Spring Boot 标准后端资产",
  "domain": "backend",
  "language": "Java",
  "framework": "Spring Boot",
  "scenario": "new-rest-api",
  "assetTypes": [
    "rule",
    "skill",
    "role",
    "flow",
    "manifest",
    "agent-profile"
  ],
  "qualityLevel": "enterprise",
  "provider": "coze",
  "providerConfigId": "provider_coze_001",
  "sourcePackIds": [
    "sourcepack_springboot_best_practices"
  ],
  "includeExamples": true,
  "includeBadExamples": true,
  "includeChecklists": true,
  "includeTests": true,
  "outputLanguage": "zh-CN"
}
```

### Response Payload

```json
{
  "code": 0,
  "message": "生成任务创建成功",
  "data": {
    "jobId": "job_001",
    "status": "draft"
  },
  "requestId": "req_xxx",
  "timestamp": "2026-04-25T10:00:00.000Z"
}
```

---

## 4.3.7.2 生成计划

```http
POST /api/asset-factory/jobs/:jobId/plan
```

### Response Payload

```json
{
  "code": 0,
  "message": "生成计划创建成功",
  "data": {
    "jobId": "job_001",
    "plan": {
      "roles": [
        "backend-implementer",
        "api-contract-designer",
        "backend-code-reviewer"
      ],
      "skills": [
        "springboot-rest-api-implementation-skill",
        "springboot-test-generation-skill"
      ],
      "rules": [
        "springboot-controller-rule",
        "backend-validation-rule"
      ],
      "flows": [
        "springboot-new-rest-api-flow"
      ],
      "manifests": [
        "backend-java-springboot-api-standard"
      ],
      "agentProfiles": [
        "backend-implementer-agent",
        "springboot-test-agent"
      ]
    }
  },
  "requestId": "req_xxx",
  "timestamp": "2026-04-25T10:00:00.000Z"
}
```

---

## 4.3.7.3 执行生成

```http
POST /api/asset-factory/jobs/:jobId/generate
```

### Response Payload

```json
{
  "code": 0,
  "message": "生成已开始",
  "data": {
    "jobId": "job_001",
    "status": "generating"
  },
  "requestId": "req_xxx",
  "timestamp": "2026-04-25T10:00:00.000Z"
}
```

---

## 4.3.7.4 校验生成结果

```http
POST /api/asset-factory/jobs/:jobId/validate
```

### Response Payload

```json
{
  "code": 0,
  "message": "校验完成",
  "data": {
    "jobId": "job_001",
    "averageScore": 88,
    "summary": {
      "total": 18,
      "passed": 15,
      "needFix": 2,
      "blocked": 1
    },
    "items": [
      {
        "itemId": "item_001",
        "assetKind": "rule",
        "assetSlug": "springboot-controller-rule",
        "score": 92,
        "status": "validated",
        "issues": []
      }
    ]
  },
  "requestId": "req_xxx",
  "timestamp": "2026-04-25T10:00:00.000Z"
}
```

---

## 4.3.7.5 导入草稿

```http
POST /api/asset-factory/jobs/:jobId/import
```

### Request Payload

```json
{
  "targetStatus": "draft",
  "selectedItems": [
    "item_001",
    "item_002"
  ],
  "conflictStrategy": "skip"
}
```

`conflictStrategy` 取值：

```text
skip
new_version
overwrite_draft
```

### Response Payload

```json
{
  "code": 0,
  "message": "导入完成",
  "data": {
    "imported": 12,
    "skipped": 2,
    "failed": 0,
    "conflicted": 1,
    "items": [
      {
        "itemId": "item_001",
        "assetSlug": "springboot-controller-rule",
        "importStatus": "imported",
        "assetId": "asset_001"
      }
    ]
  },
  "requestId": "req_xxx",
  "timestamp": "2026-04-25T10:00:00.000Z"
}
```

---

# 4.4 `br-ai-spec-visual` Collector API 契约

---

# 4.4.1 Project State 上报

## 4.4.1.1 说明

`br-ai-spec init / sync / check` 后上报项目状态。

```http
POST /api/collector/project-state
```

---

## 4.4.1.2 Request Payload

```json
{
  "workspaceId": "ws_user_center",
  "project": {
    "projectId": "proj_8f3a9c2e",
    "projectHash": "sha256_project_xxx",
    "projectName": "user-api",
    "repoId": "repo_backend",
    "packageId": "pkg_api",
    "relativePath": "services/user-api"
  },
  "techProfile": {
    "domain": "backend",
    "language": "Java",
    "frameworks": ["Spring Boot"],
    "buildTool": "Maven",
    "orm": ["MyBatis"],
    "databases": ["MySQL"],
    "confidence": 92,
    "reasons": [
      "检测到 pom.xml",
      "检测到 spring-boot-starter-web"
    ]
  },
  "manifest": {
    "slug": "backend-java-springboot-standard",
    "version": "1.0.0",
    "checksum": "sha256_manifest_xxx"
  },
  "assets": [
    {
      "kind": "rule",
      "slug": "springboot-controller-rule",
      "version": "1.0.0",
      "checksum": "sha256_asset_xxx"
    }
  ],
  "privacy": {
    "sourceCodeIncluded": false,
    "absolutePathIncluded": false,
    "userNameIncluded": false
  }
}
```

---

## 4.4.1.3 Response Payload

```json
{
  "code": 0,
  "message": "项目状态已接收",
  "data": {
    "projectId": "proj_8f3a9c2e",
    "saved": true
  },
  "requestId": "req_xxx",
  "timestamp": "2026-04-25T10:00:00.000Z"
}
```

---

# 4.4.2 Run Event 上报

```http
POST /api/collector/run-event
```

## Request Payload

```json
{
  "eventId": "evt_20260425_001",
  "runId": "run-20260425-001",
  "workspaceId": "ws_user_center",
  "projectId": "proj_8f3a9c2e",
  "eventType": "executor_completed",
  "stage": "implementation",
  "executor": "codex",
  "status": "succeeded",
  "success": true,
  "durationMs": 120000,
  "payload": {
    "flowSlug": "fullstack-feature-flow",
    "assetSlugs": [
      "springboot-rest-api-implementation-skill"
    ],
    "changedFilesCount": 5,
    "testPassed": true,
    "autoFixCount": 0
  },
  "privacy": {
    "sourceCodeIncluded": false,
    "rawPromptIncluded": false,
    "rawResponseIncluded": false,
    "absolutePathIncluded": false
  }
}
```

## Response Payload

```json
{
  "code": 0,
  "message": "运行事件已接收",
  "data": {
    "eventId": "evt_20260425_001"
  },
  "requestId": "req_xxx",
  "timestamp": "2026-04-25T10:00:00.000Z"
}
```

---

# 4.4.3 History 摘要上报

```http
POST /api/collector/history
```

## Request Payload

```json
{
  "historyId": "patch-20260425-001",
  "runId": "run-20260425-001",
  "workspaceId": "ws_user_center",
  "projectId": "proj_8f3a9c2e",
  "title": "修复用户列表按钮文案",
  "type": "small-change",
  "summary": "将用户列表页面的“新增”按钮改为“新增用户”。",
  "targets": [
    {
      "packageId": "pkg_web",
      "relativePath": "apps/web"
    }
  ],
  "changedFiles": [
    {
      "relativePath": "apps/web/src/pages/user/List.tsx",
      "changeType": "modified"
    }
  ],
  "assetsUsed": [
    {
      "kind": "rule",
      "slug": "react-component-rule",
      "version": "1.0.0"
    }
  ],
  "verificationSummary": {
    "typecheck": "passed",
    "build": "passed",
    "test": "skipped"
  },
  "executor": "cursor",
  "status": "succeeded",
  "privacy": {
    "sourceCodeIncluded": false,
    "rawPromptIncluded": false
  }
}
```

---

# 4.4.4 Incident 上报

```http
POST /api/collector/incident
```

## Request Payload

```json
{
  "incidentId": "incident_20260425_001",
  "runId": "run-20260425-001",
  "workspaceId": "ws_user_center",
  "projectId": "proj_8f3a9c2e",
  "stage": "implementation",
  "incidentType": "build-failed",
  "severity": "error",
  "summary": "TypeScript 类型检查失败，已连续修复 2 次仍未通过。",
  "diagnoseResult": {
    "rootCause": "接口返回字段类型与前端 User 类型不一致",
    "relatedFiles": [
      "apps/web/src/types/user.ts",
      "apps/web/src/pages/user/List.tsx"
    ],
    "suggestedAction": "进入 human-review 或执行 diagnostic-agent 修复"
  },
  "recoveryAction": "diagnostic-agent",
  "status": "diagnosing",
  "privacy": {
    "sourceCodeIncluded": false,
    "absolutePathIncluded": false
  }
}
```

---

# 4.5 `br-ai-spec` 内部接口定义

---

# 4.5.1 TechScannerEngine

## 4.5.1.1 类型定义

```ts
export interface TechScannerEngine {
  scanWorkspace(input: ScanWorkspaceInput): Promise<WorkspaceTopology>;
}

export interface ScanWorkspaceInput {
  rootDir: string;
  maxDepth?: number;
  useCache?: boolean;
  explain?: boolean;
  overrides?: ScanOverride[];
}

export interface ScanOverride {
  path: string;
  domain?: string;
  frameworks?: string[];
  manifest?: string;
}

export interface WorkspaceTopology {
  workspace: WorkspaceFacts;
  packages: PackageDetectionReport[];
}

export interface WorkspaceFacts {
  rootDir: string;
  type:
    | 'single'
    | 'pnpm-workspace'
    | 'npm-workspace'
    | 'yarn-workspace'
    | 'lerna'
    | 'turbo'
    | 'nx'
    | 'maven-multi-module'
    | 'gradle-multi-module'
    | 'go-work'
    | 'multi-repo';
  packageManager?: 'pnpm' | 'npm' | 'yarn' | 'bun' | 'maven' | 'gradle' | 'go';
  rootDependencies?: Record<string, DependencyInfo>;
}

export interface PackageDetectionReport {
  packageId: string;
  name?: string;
  path: string;
  primary: DetectionResult | null;
  candidates: DetectionResult[];
  tags: string[];
  recommendedManifest?: string;
  confidence: number;
  reasons: string[];
}

export interface DetectionResult {
  detector: string;
  domain: 'frontend' | 'backend' | 'mobile' | 'fullstack' | 'devops' | 'data' | 'unknown';
  language: string[];
  frameworks: string[];
  buildTool?: string;
  confidence: number;
  tags: string[];
  manifestSlug?: string;
  reasons: string[];
}

export interface DependencyInfo {
  name: string;
  version: string;
  source: 'local' | 'workspace-root' | 'lockfile';
}
```

---

# 4.5.2 Context Builder

```ts
export interface IContextBuilder {
  build(input: BuildContextInput): Promise<ContextBundle>;
}

export interface BuildContextInput {
  runId: string;
  stage: RunStage;
  projectRoot: string;
  targets: TargetPackage[];
  contextIndexPath: string;
  registryIndexPath: string;
  lockFilePath: string;
  tokenBudget: TokenBudget;
}

export interface TargetPackage {
  packageId: string;
  relativePath: string;
  domain: string;
  framework?: string[];
}

export interface ContextBundle {
  runId: string;
  stage: RunStage;
  targets: TargetPackage[];
  loadedAssets: LoadedAsset[];
  overlays: LoadedOverlay[];
  sharedContracts: LoadedSharedContract[];
  projectFacts: Record<string, unknown>;
  tokenEstimate: {
    inputTokens: number;
    maxTokens: number;
    warning: boolean;
  };
  privacy: {
    sourceCodeIncluded: false;
    rawPromptIncluded: false;
  };
}

export interface LoadedAsset {
  kind: AssetKind;
  slug: string;
  version: string;
  source: 'hub-cache' | 'project-overlay' | 'shared-contract';
  content: string;
  checksum: string;
}

export type RunStage =
  | 'planning'
  | 'implementation'
  | 'verification'
  | 'review'
  | 'diagnosing'
  | 'recovering';
```

---

# 4.5.3 State Machine

```ts
export interface IStateMachine {
  start(input: StartRunInput): Promise<RunResult>;
  continue(input: ContinueRunInput): Promise<RunResult>;
  transition(input: TransitionInput): Promise<RunStateSnapshot>;
}

export interface StartRunInput {
  requirement: string;
  rootDir: string;
  targets?: string[];
  executor?: ExecutorType;
  mode?: ExecutionMode;
  worktree?: boolean;
  createdBy?: string;
}

export interface ContinueRunInput {
  runId: string;
  action: 'continue' | 'retry' | 'approve' | 'reject' | 'cancel';
  comment?: string;
}

export interface TransitionInput {
  runId: string;
  from: RunState;
  to: RunState;
  reason: string;
  payload?: Record<string, unknown>;
}

export interface RunResult {
  runId: string;
  state: RunState;
  branch?: string;
  worktreePath?: string;
  reportPath?: string;
  nextActions: string[];
}

export interface RunStateSnapshot {
  runId: string;
  state: RunState;
  updatedAt: string;
}
```

---

# 4.6 `IExecutorProvider` 核心契约

> 这是本系统最重要的内部接口之一。
> Codex IDE、Cursor、Claude Code 必须全部实现该接口。
> 状态机只依赖此接口，不允许直接依赖任何单一 IDE SDK 或命令。

---

## 4.6.1 接口定义

```ts
export interface IExecutorProvider {
  /**
   * 执行器唯一标识。
   * 必须为 codex / cursor / claude-code / openclaw / coze / custom 之一。
   */
  readonly name: ExecutorType;

  /**
   * 执行器展示名称。
   */
  readonly displayName: string;

  /**
   * 能力声明。
   */
  readonly capabilities: ExecutorCapability[];

  /**
   * 检查本机或当前环境是否可用。
   */
  checkAvailability(input: ExecutorAvailabilityInput): Promise<ExecutorAvailabilityResult>;

  /**
   * 执行前准备。
   * 例如写入临时指令文件、准备上下文包、检查 CLI 是否存在。
   */
  prepare(input: ExecutorPrepareInput): Promise<ExecutorPrepareResult>;

  /**
   * 执行核心任务。
   */
  execute(input: ExecutorExecuteInput): Promise<ExecutorExecutionResult>;

  /**
   * 执行验证任务。
   * 例如运行测试、构建、类型检查、截图、API 调用。
   */
  verify?(input: ExecutorVerifyInput): Promise<ExecutorVerifyResult>;

  /**
   * 请求执行器停止。
   */
  cancel?(input: ExecutorCancelInput): Promise<ExecutorCancelResult>;

  /**
   * 清理临时文件。
   */
  cleanup?(input: ExecutorCleanupInput): Promise<ExecutorCleanupResult>;
}
```

---

## 4.6.2 ExecutorCapability

```ts
export type ExecutorCapability =
  | 'read'
  | 'write'
  | 'shell'
  | 'test'
  | 'screenshot'
  | 'api-test'
  | 'interactive'
  | 'headless'
  | 'long-running'
  | 'structured-output'
  | 'remote';
```

---

## 4.6.3 Availability

```ts
export interface ExecutorAvailabilityInput {
  projectRoot: string;
  worktreePath?: string;
  env: NodeJS.ProcessEnv;
}

export interface ExecutorAvailabilityResult {
  available: boolean;
  version?: string;
  reason?: string;
  fixSuggestion?: string;
}
```

示例：

```json
{
  "available": false,
  "reason": "未检测到 codex 命令",
  "fixSuggestion": "请安装 Codex IDE CLI，或在 .ai-spec/policy.json 中切换 defaultExecutor。"
}
```

---

## 4.6.4 Prepare

```ts
export interface ExecutorPrepareInput {
  runId: string;
  projectRoot: string;
  worktreePath: string;
  contextBundle: ContextBundle;
  agentProfile?: AgentProfileConfig;
  policy: PolicyConfig;
}

export interface ExecutorPrepareResult {
  prepared: boolean;
  executorInputPath?: string;
  instructionFilePath?: string;
  warnings?: string[];
}
```

---

## 4.6.5 Execute

```ts
export interface ExecutorExecuteInput {
  runId: string;
  taskId: string;
  stage: RunStage;
  projectRoot: string;
  worktreePath: string;
  requirement: string;
  contextBundle: ContextBundle;
  agentProfile?: AgentProfileConfig;
  timeoutMs: number;
  retry: {
    attempt: number;
    maxRetries: number;
  };
}

export interface ExecutorExecutionResult {
  success: boolean;
  status: 'succeeded' | 'failed' | 'timeout' | 'cancelled' | 'invalid-output';
  summary: string;
  changedFiles: ChangedFile[];
  riskList: RiskItem[];
  testSuggestions?: string[];
  tokenUsage?: TokenUsage;
  rawOutputStoredLocalPath?: string;
  error?: ExecutorError;
}

export interface ChangedFile {
  relativePath: string;
  changeType: 'created' | 'modified' | 'deleted' | 'renamed';
  riskLevel: 'low' | 'medium' | 'high';
}

export interface RiskItem {
  level: 'info' | 'warning' | 'error' | 'fatal';
  message: string;
  file?: string;
  suggestion?: string;
}

export interface TokenUsage {
  inputTokens?: number;
  outputTokens?: number;
  totalTokens?: number;
  estimated: boolean;
}

export interface ExecutorError {
  code:
    | 'EXECUTOR_NOT_AVAILABLE'
    | 'EXECUTOR_TIMEOUT'
    | 'EXECUTOR_FAILED'
    | 'EXECUTOR_RESULT_INVALID'
    | 'EXECUTOR_PERMISSION_DENIED'
    | 'EXECUTOR_CONTEXT_TOO_LARGE';
  message: string;
  details?: Record<string, unknown>;
}
```

---

## 4.6.6 Verify

```ts
export interface ExecutorVerifyInput {
  runId: string;
  projectRoot: string;
  worktreePath: string;
  commands: VerifyCommand[];
  timeoutMs: number;
}

export interface VerifyCommand {
  name: string;
  command: string;
  cwd?: string;
  required: boolean;
}

export interface ExecutorVerifyResult {
  success: boolean;
  results: VerifyCommandResult[];
  summary: string;
}

export interface VerifyCommandResult {
  name: string;
  command: string;
  success: boolean;
  exitCode?: number;
  durationMs: number;
  stdoutPath?: string;
  stderrPath?: string;
  summary?: string;
}
```

---

## 4.6.7 Cancel / Cleanup

```ts
export interface ExecutorCancelInput {
  runId: string;
  reason: string;
}

export interface ExecutorCancelResult {
  cancelled: boolean;
  message?: string;
}

export interface ExecutorCleanupInput {
  runId: string;
  projectRoot: string;
  worktreePath: string;
}

export interface ExecutorCleanupResult {
  cleaned: boolean;
  removedPaths?: string[];
}
```

---

# 4.7 Codex / Cursor / Claude Code Provider 实现要求

---

# 4.7.1 Codex Provider

```ts
export class CodexExecutorProvider implements IExecutorProvider {
  readonly name = 'codex';
  readonly displayName = 'Codex IDE';
  readonly capabilities: ExecutorCapability[] = [
    'read',
    'write',
    'shell',
    'test',
    'headless',
    'long-running',
    'structured-output'
  ];

  async checkAvailability(input: ExecutorAvailabilityInput): Promise<ExecutorAvailabilityResult> {
    // 检测 codex 命令是否存在
    // 检测版本
    // 检测当前环境是否允许 headless 执行
  }

  async prepare(input: ExecutorPrepareInput): Promise<ExecutorPrepareResult> {
    // 写入 .codex/tmp/<run-id>/executor-input.json
    // 写入 .codex/tmp/<run-id>/instructions.md
    // 不写入源码内容
  }

  async execute(input: ExecutorExecuteInput): Promise<ExecutorExecutionResult> {
    // 调用 codex CLI 或 Codex IDE 协议
    // 设置 timeout
    // 解析结构化输出
  }

  async verify(input: ExecutorVerifyInput): Promise<ExecutorVerifyResult> {
    // 执行测试命令
  }
}
```

---

# 4.7.2 Cursor Provider

```ts
export class CursorExecutorProvider implements IExecutorProvider {
  readonly name = 'cursor';
  readonly displayName = 'Cursor';
  readonly capabilities: ExecutorCapability[] = [
    'read',
    'write',
    'interactive',
    'structured-output'
  ];

  async checkAvailability(input: ExecutorAvailabilityInput): Promise<ExecutorAvailabilityResult> {
    // 检测 cursor 命令或 Cursor 环境
  }

  async prepare(input: ExecutorPrepareInput): Promise<ExecutorPrepareResult> {
    // 确认 .cursor/rules/ai-spec-auto.mdc 已存在
    // 写入本次 run 的任务说明文件
  }

  async execute(input: ExecutorExecuteInput): Promise<ExecutorExecutionResult> {
    // Cursor 可能偏交互式，不同环境下可降级为生成执行指令
    // 如果不支持 headless，则返回 human-review 或 interactive-required
  }
}
```

Cursor 特殊约束：

```text
1. 如果当前 Cursor 环境不支持 headless 执行，Provider 必须返回 status = failed，error.code = EXECUTOR_PERMISSION_DENIED，并提示切换 codex / claude-code。
2. Cursor 更适合 local-assisted，不建议作为 remote-orchestrated 默认执行器。
```

---

# 4.7.3 Claude Code Provider

```ts
export class ClaudeCodeExecutorProvider implements IExecutorProvider {
  readonly name = 'claude-code';
  readonly displayName = 'Claude Code';
  readonly capabilities: ExecutorCapability[] = [
    'read',
    'write',
    'shell',
    'test',
    'interactive',
    'headless',
    'long-running',
    'structured-output'
  ];

  async checkAvailability(input: ExecutorAvailabilityInput): Promise<ExecutorAvailabilityResult> {
    // 检测 claude 命令
    // 检测认证状态
  }

  async prepare(input: ExecutorPrepareInput): Promise<ExecutorPrepareResult> {
    // 确认 CLAUDE.md 存在
    // 写入本次 run 上下文摘要
  }

  async execute(input: ExecutorExecuteInput): Promise<ExecutorExecutionResult> {
    // 调用 Claude Code CLI
    // 捕获输出
    // 解析 changedFiles / riskList / summary
  }

  async verify(input: ExecutorVerifyInput): Promise<ExecutorVerifyResult> {
    // 执行测试、构建命令
  }
}
```

---

# 4.8 Executor Registry 与 Selector

## 4.8.1 ExecutorRegistry

```ts
export class ExecutorRegistry {
  private providers = new Map<ExecutorType, IExecutorProvider>();

  register(provider: IExecutorProvider): void {
    this.providers.set(provider.name, provider);
  }

  get(name: ExecutorType): IExecutorProvider | undefined {
    return this.providers.get(name);
  }

  list(): IExecutorProvider[] {
    return Array.from(this.providers.values());
  }
}
```

---

## 4.8.2 ExecutorSelector

```ts
export interface ExecutorSelectionInput {
  cliExecutor?: ExecutorType;
  mode: ExecutionMode;
  policy: PolicyConfig;
  agentProfile?: AgentProfileConfig;
  registry: ExecutorRegistry;
  projectRoot: string;
  worktreePath?: string;
}

export interface ExecutorSelectionResult {
  executor: ExecutorType;
  fallbackExecutors: ExecutorType[];
  reason: string;
}

export class ExecutorSelector {
  async select(input: ExecutorSelectionInput): Promise<ExecutorSelectionResult> {
    // 1. CLI 显式指定优先
    // 2. Agent Profile 推荐
    // 3. policy 默认
    // 4. mode 默认
    // 5. fallback
  }
}
```

---

# 4.9 State Machine 与 Executor 交互契约

状态机调用执行器的标准流程：

```text
select executor
↓
checkAvailability
↓
prepare
↓
execute
↓
verify
↓
publish event
↓
transition state
```

伪代码：

```ts
async function runStage(input: RunStageInput): Promise<StageResult> {
  const executor = await executorSelector.select(input);

  const availability = await executor.provider.checkAvailability({
    projectRoot: input.projectRoot,
    worktreePath: input.worktreePath,
    env: process.env
  });

  if (!availability.available) {
    throw new AiSpecError('EXECUTOR_NOT_AVAILABLE', availability.fixSuggestion);
  }

  const contextBundle = await contextBuilder.build({
    runId: input.runId,
    stage: input.stage,
    projectRoot: input.projectRoot,
    targets: input.targets,
    contextIndexPath: input.contextIndexPath,
    registryIndexPath: input.registryIndexPath,
    lockFilePath: input.lockFilePath,
    tokenBudget: input.policy.tokenBudget
  });

  await executor.provider.prepare({
    runId: input.runId,
    projectRoot: input.projectRoot,
    worktreePath: input.worktreePath,
    contextBundle,
    agentProfile: input.agentProfile,
    policy: input.policy
  });

  const result = await executor.provider.execute({
    runId: input.runId,
    taskId: input.taskId,
    stage: input.stage,
    projectRoot: input.projectRoot,
    worktreePath: input.worktreePath,
    requirement: input.requirement,
    contextBundle,
    agentProfile: input.agentProfile,
    timeoutMs: input.policy.executorTimeout.executeTimeoutMs,
    retry: {
      attempt: input.attempt,
      maxRetries: input.policy.retryPolicy.maxRetries
    }
  });

  if (!result.success) {
    return escapeHatch.handleExecutorFailure(result);
  }

  return {
    success: true,
    changedFiles: result.changedFiles,
    summary: result.summary
  };
}
```

---

# 4.10 Dirty Working Tree 策略接口

```ts
export interface IDirtyStrategyHandler {
  name: DirtyStrategy;
  handle(input: DirtyStrategyInput): Promise<DirtyStrategyResult>;
}

export interface DirtyStrategyInput {
  repoRoot: string;
  changedFiles: string[];
  runId: string;
  requirementSummary: string;
}

export interface DirtyStrategyResult {
  canContinue: boolean;
  strategy: DirtyStrategy;
  message: string;
  wipCommitHash?: string;
  patchPath?: string;
}
```

策略：

| 策略               | 行为                            |
| ---------------- | ----------------------------- |
| `block`          | 阻断执行，要求用户手动处理                 |
| `wip-commit`     | 创建临时 WIP commit 后继续           |
| `patch-snapshot` | 生成 patch 快照，不带入新分支            |
| `ignore`         | 忽略 dirty，从当前 HEAD 创建 worktree |

默认：

```text
block
```

---

# 4.11 Visual / Hub 上报隐私过滤接口

```ts
export interface IPrivacyFilter {
  filterRuntimeEvent(input: RuntimeEventPayload): RuntimeEventPayload;
  assertNoSensitiveData(input: unknown): void;
}

export interface RuntimeEventPayload {
  eventId: string;
  runId?: string;
  workspaceId?: string;
  projectId?: string;
  eventType: RuntimeEventType;
  stage?: string;
  executor?: ExecutorType;
  status?: string;
  success?: boolean;
  durationMs?: number;
  payload?: Record<string, unknown>;
  privacy: {
    sourceCodeIncluded: false;
    rawPromptIncluded: false;
    rawResponseIncluded: false;
    absolutePathIncluded: false;
    userNameIncluded: false;
  };
}
```

实现要求：

```text
1. 如果 payload 中出现疑似源码大文本，必须拒绝上报。
2. 如果出现绝对路径，必须脱敏为相对路径或 hash。
3. 如果出现 token / secret / password，必须拒绝上报。
4. 如果 privacy 标识不全为 false，必须拒绝。
```

---

# 4.12 Asset Tamper Check 接口

```ts
export interface IAssetTamperChecker {
  check(input: AssetTamperCheckInput): Promise<AssetTamperCheckResult>;
}

export interface AssetTamperCheckInput {
  lockFilePath: string;
  registryIndexPath: string;
  globalCacheRoot: string;
  overlaysDir: string;
}

export interface AssetTamperCheckResult {
  passed: boolean;
  issues: AssetTamperIssue[];
}

export interface AssetTamperIssue {
  level: 'warning' | 'error' | 'fatal';
  kind: 'asset' | 'manifest' | 'agent-profile' | 'overlay' | 'registry';
  slug?: string;
  expectedChecksum?: string;
  actualChecksum?: string;
  message: string;
  suggestion: string;
}
```

阻断条件：

```text
1. Platform asset checksum 不一致。
2. Manifest checksum 不一致。
3. Agent Profile checksum 不一致。
4. registry.index.json 引用不存在 cache。
5. Overlay 修改后未更新 lock。
```

---

# 4.13 API 契约实现边界

本章节完成后，AI 编程助手必须实现或遵循：

```text
1. Hub API 必须支持 Manifest 推荐、Manifest 导出、Asset 内容拉取、Agent Profile 导出。
2. Hub API 必须支持 Asset Factory 创建、生成、校验、导入草稿。
3. Hub API 必须支持安装记录和运行反馈上报。
4. Visual API 必须支持 project-state、run-event、history、incident 上报。
5. br-ai-spec 内部必须定义 TechScannerEngine、ContextBuilder、StateMachine、ExecutorProvider。
6. Codex / Cursor / Claude Code 必须分别实现 IExecutorProvider。
7. ExecutorSelector 必须支持 CLI 参数、policy、Agent Profile、mode 四级选择。
8. Dirty working tree 必须通过策略接口处理。
9. 所有上报必须通过 PrivacyFilter。
10. 所有资产执行前必须通过 AssetTamperChecker。
```

