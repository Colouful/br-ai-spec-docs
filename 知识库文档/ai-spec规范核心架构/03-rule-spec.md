# Rule 规范文档

> 文档用途：作为扣子知识库 `hub-asset-schema` 和 `asset-examples` 的 Rule 事实源，用于生成、审核和导入 Hub Rule 资产。

---

## 1. Rule 定位

Rule 是 AI 工程资产体系中的规则资产，用于约束 AI 编程终端在特定技术栈、框架、项目类型和执行阶段中的行为。

Rule 的目标不是解释概念，而是形成明确的工程约束，让 Codex / Cursor / Claude Code 在执行需求时知道：

1. 必须做什么。
2. 不能做什么。
3. 应该遵循哪些项目规范。
4. 出现异常时如何处理。
5. 如何判断输出是否合格。

---

## 2. Rule 与其他资产关系

```text
Manifest
  ├── Rule：约束行为
  ├── Skill：指导任务执行
  ├── Role：定义执行身份
  ├── Flow：定义流程阶段
  └── Agent Profile：定义执行器权限和上下文
```

Rule 通常由 Manifest 引用，并在 ContextBuilder 的 implementation / verification / review 阶段被加载。

---

## 3. Rule 适用场景

适合用 Rule 表达：

1. 编码规范。
2. 目录结构规范。
3. 命名规范。
4. 组件开发约束。
5. API 设计约束。
6. DTO / VO / BO 约束。
7. 异常处理约束。
8. 日志规范。
9. 测试规范。
10. 安全约束。
11. 禁止行为。
12. Review 门禁。

不适合用 Rule 表达：

1. 完整任务流程。
2. 多步骤复杂执行。
3. 角色人设。
4. Manifest 安装清单。
5. 执行器权限策略。

这些应分别使用 Skill、Flow、Role、Manifest、Agent Profile。

---

## 4. 命名规范

### 4.1 slug

规则：

1. 小写英文。
2. 数字。
3. 中横线。
4. 不使用中文。
5. 不使用下划线。

示例：

```text
frontend-react-component-rule
frontend-vue-composition-api-rule
backend-java-spring-controller-rule
backend-python-fastapi-router-rule
backend-rust-axum-handler-rule
fullstack-api-contract-rule
```

### 4.2 name

使用中文，清晰表达规则用途。

示例：

```text
React 组件开发规则
Spring Boot Controller 开发规则
FastAPI Router 开发规则
Rust Axum Handler 开发规则
```

---

## 5. Rule Schema

```json
{
  "schemaVersion": "1.0.0",
  "kind": "rule",
  "slug": "frontend-react-component-rule",
  "name": "React 组件开发规则",
  "description": "约束 React 组件开发过程中的结构、命名、状态管理、样式和测试要求。",
  "version": "1.0.0",
  "status": "draft",
  "scope": "platform",
  "riskLevel": "medium",
  "applicableTechStacks": [
    {
      "domain": "frontend",
      "language": ["TypeScript", "JavaScript"],
      "frameworks": ["React"],
      "projectKinds": ["application", "monorepo"]
    }
  ],
  "loadStages": ["implementation", "review"],
  "content": {
    "purpose": "规范 React 组件开发，提升可维护性、可测试性和一致性。",
    "whenToUse": ["新增 React 组件", "重构 React 页面", "修复组件交互问题"],
    "inputs": ["需求描述", "目标目录", "组件命名", "项目组件库信息"],
    "outputs": ["符合项目规范的组件代码", "必要测试", "变更说明"],
    "rules": [
      "组件必须使用明确的 Props 类型。",
      "组件内部状态必须最小化。",
      "禁止在组件中硬编码接口地址。"
    ],
    "constraints": ["不得修改无关文件", "不得引入未确认依赖"],
    "forbiddenActions": ["禁止上传源码", "禁止自动执行部署", "禁止修改 package.json"],
    "acceptanceCriteria": ["组件可构建", "类型检查通过", "核心交互有测试或说明"],
    "fallbackStrategy": {
      "triggerCondition": "组件生成后类型检查失败或无法确认组件库规范",
      "action": "human-review",
      "diagnosticPrompt": "请检查组件库使用方式、Props 类型和样式方案。"
    },
    "testCases": [
      {
        "scenario": "新增列表组件",
        "mockInput": "为用户列表页新增筛选表单和表格组件",
        "expectedBehavior": "生成具备 Props 类型、组件拆分清晰、无硬编码接口地址的组件草稿。"
      }
    ],
    "telemetryTags": ["react-component", "unit-test"]
  },
  "dependencies": [],
  "quality": {
    "score": 90,
    "checks": [],
    "warnings": []
  }
}
```

---

## 6. 字段说明

| 字段 | 类型 | 必填 | 说明 |
|---|---|---:|---|
| schemaVersion | string | 是 | Schema 版本 |
| kind | string | 是 | 固定为 rule |
| slug | string | 是 | 唯一标识 |
| name | string | 是 | 中文名称 |
| version | string | 是 | 版本 |
| status | string | 是 | draft / published / deprecated / archived |
| scope | string | 是 | platform / team / project |
| riskLevel | string | 是 | low / medium / high / critical |
| applicableTechStacks | array | 是 | 适用技术栈 |
| loadStages | array | 是 | 加载阶段 |
| content | object | 是 | 规则正文 |
| quality | object | 是 | 质量报告 |

---

## 7. content 字段规范

### 7.1 purpose

说明规则目的。必须清晰、可执行。

### 7.2 whenToUse

说明什么时候加载该规则。

### 7.3 inputs

说明 AI 执行该规则需要哪些输入。

### 7.4 outputs

说明期望产出。

### 7.5 rules

核心规则列表。必须明确、可执行。

### 7.6 constraints

约束条件。

### 7.7 forbiddenActions

禁止行为，必须明确。

常见禁止行为：

1. 禁止上传源码。
2. 禁止修改无关文件。
3. 禁止安装依赖。
4. 禁止自动发布。
5. 禁止自动 push。
6. 禁止自动 merge。
7. 禁止绕过测试。

### 7.8 acceptanceCriteria

验收标准必须可检查。

### 7.9 fallbackStrategy

规则失败时的状态机逃逸策略。

支持：

```text
block
retry
diagnose
human-review
```

### 7.10 testCases

用于 Hub 审核和后续沙盒验证。

### 7.11 telemetryTags

用于 Visual 归因分析。

---

## 8. 风险等级

| riskLevel | 说明 | 默认 fallback |
|---|---|---|
| low | 文档或轻量规则 | retry |
| medium | 常规代码生成规则 | diagnose |
| high | 影响架构、接口、数据库 | human-review |
| critical | 发布、权限、安全、数据迁移 | block |

---

## 9. Rule 类型分类

### 9.1 前端 Rule

典型类型：

1. 组件规则。
2. Hooks 规则。
3. 路由规则。
4. 状态管理规则。
5. API 调用规则。
6. 样式规则。
7. 组件库规则。
8. 测试规则。

### 9.2 后端 Rule

典型类型：

1. Controller / Router / Handler 规则。
2. Service / UseCase 规则。
3. DTO / Request / Response 规则。
4. Repository / DAO 规则。
5. 异常处理规则。
6. 日志规则。
7. 参数校验规则。
8. 接口契约规则。
9. 单元测试规则。
10. 权限与安全规则。

### 9.3 全栈 Rule

典型类型：

1. API 契约规则。
2. 共享业务模型规则。
3. 错误码规则。
4. 字段命名规则。
5. 联调规则。
6. 兼容性规则。

---

## 10. 示例：Spring Boot Controller Rule

```json
{
  "schemaVersion": "1.0.0",
  "kind": "rule",
  "slug": "backend-java-spring-controller-rule",
  "name": "Spring Boot Controller 开发规则",
  "description": "约束 Spring Boot Controller 层的接口命名、参数校验、响应结构和异常处理方式。",
  "version": "1.0.0",
  "status": "draft",
  "scope": "platform",
  "riskLevel": "medium",
  "applicableTechStacks": [
    {
      "domain": "backend",
      "language": ["Java"],
      "frameworks": ["Spring Boot"],
      "projectKinds": ["application", "monorepo"]
    }
  ],
  "loadStages": ["implementation", "review"],
  "content": {
    "purpose": "统一 Controller 层接口风格，降低接口联调成本。",
    "whenToUse": ["新增接口", "修改接口", "生成 Controller"],
    "inputs": ["接口需求", "请求参数", "响应结构", "错误码规范"],
    "outputs": ["Controller 草稿", "参数校验说明", "接口契约说明"],
    "rules": [
      "Controller 只负责请求接入和响应返回，不承载复杂业务逻辑。",
      "所有入参必须有校验策略。",
      "响应结构必须遵循统一 API 返回格式。",
      "异常必须交给统一异常处理机制。"
    ],
    "constraints": ["不得绕过 Service 层", "不得直接拼接 SQL"],
    "forbiddenActions": ["禁止在 Controller 中写复杂业务逻辑", "禁止返回不统一的数据结构"],
    "acceptanceCriteria": ["接口路径清晰", "入参校验完整", "响应格式统一", "异常处理一致"],
    "fallbackStrategy": {
      "triggerCondition": "缺少统一响应格式或错误码规范",
      "action": "human-review",
      "diagnosticPrompt": "请补充统一响应格式、错误码规范和接口契约。"
    },
    "testCases": [
      {
        "scenario": "新增用户查询接口",
        "mockInput": "新增 GET /users 查询用户列表接口",
        "expectedBehavior": "输出符合 Controller 分层、参数校验、统一响应和异常处理规则的接口草稿。"
      }
    ],
    "telemetryTags": ["spring-controller", "api-contract"]
  },
  "dependencies": [],
  "quality": {
    "score": 92,
    "checks": ["结构完整", "约束明确", "可测试"],
    "warnings": []
  }
}
```

---

## 11. 示例：FastAPI Router Rule

```json
{
  "schemaVersion": "1.0.0",
  "kind": "rule",
  "slug": "backend-python-fastapi-router-rule",
  "name": "FastAPI Router 开发规则",
  "description": "约束 FastAPI Router、Pydantic Schema、依赖注入和异常处理。",
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
  "loadStages": ["implementation", "review"],
  "content": {
    "purpose": "规范 FastAPI 接口开发，保证 Schema、异常、文档和测试一致。",
    "whenToUse": ["新增 FastAPI 接口", "修改 Router", "生成 Pydantic Schema"],
    "inputs": ["接口需求", "请求模型", "响应模型", "错误处理策略"],
    "outputs": ["Router 草稿", "Schema 约束", "测试建议"],
    "rules": [
      "请求和响应必须通过 Pydantic Schema 表达。",
      "Router 不应包含复杂业务逻辑。",
      "错误响应必须可被 OpenAPI 描述。"
    ],
    "constraints": ["不得跳过类型注解", "不得返回不稳定结构"],
    "forbiddenActions": ["禁止要求上传源码", "禁止生成包含密钥的示例"],
    "acceptanceCriteria": ["Schema 完整", "OpenAPI 友好", "异常处理清晰"],
    "fallbackStrategy": {
      "triggerCondition": "缺少请求响应 Schema 或异常结构",
      "action": "human-review",
      "diagnosticPrompt": "请补充 Pydantic Schema、错误码和响应格式。"
    },
    "testCases": [
      {
        "scenario": "新增订单创建接口",
        "mockInput": "生成 POST /orders 接口契约",
        "expectedBehavior": "输出 Router、请求 Schema、响应 Schema 和异常处理约束。"
      }
    ],
    "telemetryTags": ["python-fastapi", "api-contract"]
  },
  "dependencies": [],
  "quality": {
    "score": 90,
    "checks": [],
    "warnings": []
  }
}
```

---

## 12. 校验清单

Rule 进入 Hub 审核前必须满足：

- [ ] kind = rule。
- [ ] slug 合法。
- [ ] version 合法。
- [ ] status = draft。
- [ ] riskLevel 存在。
- [ ] applicableTechStacks 非空。
- [ ] purpose 非空。
- [ ] whenToUse 非空。
- [ ] inputs 非空。
- [ ] outputs 非空。
- [ ] rules 非空。
- [ ] forbiddenActions 非空。
- [ ] acceptanceCriteria 非空。
- [ ] fallbackStrategy 合法。
- [ ] testCases 至少一个。
- [ ] telemetryTags 1 到 3 个。
- [ ] 不包含源码级业务代码。
- [ ] 不要求上传源码。
- [ ] 质量分 >= 80。

---

## 13. 知识库使用建议

建议将本文放入扣子知识库：

```text
知识库名称：hub-asset-schema
文档名称：Rule 规范文档
用途：供 AI Asset Factory Agent 生成 Rule 资产、检查 Rule 质量、输出 Hub 导入 JSON。
```
