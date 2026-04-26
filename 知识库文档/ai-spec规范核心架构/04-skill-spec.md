# Skill 规范文档

> 文档用途：作为扣子知识库 `hub-asset-schema` 与 `asset-examples` 的 Skill 事实源，用于生成、审核、导入 Hub Skill 资产。

---

## 1. Skill 定位

Skill 是 AI 工程资产体系中的技能资产，用于指导 AI 完成一个具体工程任务。

Rule 解决“约束什么”，Skill 解决“怎么执行”。

Skill 应该提供：

1. 任务目标。
2. 输入要求。
3. 执行步骤。
4. 输出格式。
5. 质量门禁。
6. 异常处理。
7. 验收标准。
8. 测试用例。
9. 可观测标签。

---

## 2. Skill 与 Rule 区别

| 维度 | Rule | Skill |
|---|---|---|
| 关注点 | 约束行为 | 指导执行 |
| 形式 | 禁止 / 必须 / 应该 | 步骤 / 输入 / 输出 |
| 典型场景 | 编码规范、禁止行为 | 生成组件、生成接口、修复问题 |
| 加载阶段 | implementation / review | implementation / diagnosing / recovering |
| 是否可独立执行 | 通常否 | 通常是 |

---

## 3. Skill 命名规范

### 3.1 slug

示例：

```text
frontend-react-page-generation-skill
frontend-vue-form-generation-skill
backend-java-spring-api-generation-skill
backend-python-fastapi-router-generation-skill
backend-rust-axum-handler-generation-skill
fullstack-contract-generation-skill
```

规则：

1. 小写英文。
2. 数字。
3. 中横线。
4. 不使用中文。
5. 不使用下划线。

---

## 4. Skill Schema

```json
{
  "schemaVersion": "1.0.0",
  "kind": "skill",
  "slug": "backend-java-spring-api-generation-skill",
  "name": "Spring Boot API 生成技能",
  "description": "指导 AI 根据接口需求生成符合企业规范的 Spring Boot API 草稿。",
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
  "loadStages": ["implementation", "diagnosing"],
  "content": {
    "purpose": "根据 API 需求生成 Controller、Service、DTO 和测试建议。",
    "whenToUse": ["新增后端接口", "修改接口逻辑", "生成 API 契约"],
    "inputs": ["接口需求", "请求参数", "响应结构", "错误码规范", "项目分层规范"],
    "outputs": ["接口实现草稿", "DTO 约束", "测试建议", "风险说明"],
    "steps": [
      "确认接口路径、方法、请求参数和响应结构。",
      "确认项目分层和命名规范。",
      "生成 Controller 层草稿。",
      "生成 Service 层草稿。",
      "生成 DTO / Request / Response 结构说明。",
      "补充异常处理和日志策略。",
      "输出测试建议和验收标准。"
    ],
    "constraints": ["不得绕过统一异常处理", "不得直接生成数据库迁移", "不得修改无关文件"],
    "forbiddenActions": ["禁止上传源码", "禁止自动 push", "禁止自动部署"],
    "acceptanceCriteria": ["接口契约清晰", "分层职责明确", "异常处理一致", "测试建议完整"],
    "fallbackStrategy": {
      "triggerCondition": "接口契约缺失或分层规范不明确",
      "action": "human-review",
      "diagnosticPrompt": "请补充接口契约、分层规范和错误码规范。"
    },
    "testCases": [
      {
        "scenario": "新增用户详情接口",
        "mockInput": "生成 GET /users/{id} 接口",
        "expectedBehavior": "输出 Controller、Service、DTO、异常处理和测试建议。"
      }
    ],
    "telemetryTags": ["spring-controller", "api-contract"]
  },
  "dependencies": [
    {
      "kind": "rule",
      "slug": "backend-java-spring-controller-rule",
      "version": "1.0.0"
    }
  ],
  "quality": {
    "score": 92,
    "checks": [],
    "warnings": []
  }
}
```

---

## 5. content 字段要求

### 5.1 purpose

必须说明该技能解决什么工程任务。

### 5.2 whenToUse

必须说明触发时机。

### 5.3 inputs

必须列清楚执行前需要哪些信息。

### 5.4 outputs

必须说明输出结果。

### 5.5 steps

必须是可执行步骤，不要写空泛描述。

### 5.6 constraints

必须说明执行边界。

### 5.7 forbiddenActions

必须说明禁止行为。

### 5.8 acceptanceCriteria

必须可检查。

### 5.9 fallbackStrategy

必须描述失败兜底。

### 5.10 testCases

至少一个。

### 5.11 telemetryTags

1 到 3 个。

---

## 6. Skill 分类

### 6.1 前端 Skill

典型：

1. 页面生成 Skill。
2. 组件生成 Skill。
3. 表单生成 Skill。
4. 表格生成 Skill。
5. API Hook 生成 Skill。
6. 路由接入 Skill。
7. 单元测试生成 Skill。
8. UI 组件库适配 Skill。

### 6.2 后端 Skill

典型：

1. API 生成 Skill。
2. Controller / Router / Handler 生成 Skill。
3. Service / UseCase 生成 Skill。
4. DTO / Schema 生成 Skill。
5. 异常处理接入 Skill。
6. 日志接入 Skill。
7. 单元测试生成 Skill。
8. 接口契约生成 Skill。

### 6.3 全栈 Skill

典型：

1. API Contract 生成 Skill。
2. 共享业务模型生成 Skill。
3. 前后端联调 Skill。
4. 字段映射 Skill。
5. 错误码契约 Skill。

### 6.4 诊断 Skill

典型：

1. 构建失败诊断。
2. 类型错误诊断。
3. 测试失败诊断。
4. 资产缺失诊断。
5. 上下文超预算诊断。

---

## 7. 后端 Skill 专项要求

### 7.1 Java / Spring

必须关注：

1. Controller。
2. Service。
3. DTO / VO / BO。
4. Repository / Mapper。
5. 统一响应。
6. 统一异常。
7. 参数校验。
8. 事务边界。
9. 日志。
10. 测试。

### 7.2 Node.js / NestJS

必须关注：

1. Controller。
2. Provider / Service。
3. DTO。
4. Guard。
5. Interceptor。
6. Pipe。
7. Exception Filter。
8. OpenAPI。
9. 单元测试。

### 7.3 Python / FastAPI / Django / Flask

必须关注：

1. Router / View。
2. Service / UseCase。
3. Pydantic Schema / Serializer。
4. ORM Model。
5. Repository。
6. 异常处理。
7. OpenAPI。
8. 类型注解。
9. pytest。

### 7.4 Go

必须关注：

1. Handler。
2. Service / UseCase。
3. Struct DTO。
4. JSON Tag。
5. Validator Tag。
6. Repository。
7. context 传递。
8. error wrapping。
9. go test。

### 7.5 Rust

必须关注：

1. Handler / Route。
2. Service / UseCase。
3. Request / Response DTO。
4. serde。
5. validator。
6. Result / Error。
7. State / AppContext。
8. tracing。
9. SeaORM / Diesel / SQLx。
10. cargo test。

---

## 8. 示例：React 页面生成 Skill

```json
{
  "schemaVersion": "1.0.0",
  "kind": "skill",
  "slug": "frontend-react-page-generation-skill",
  "name": "React 页面生成技能",
  "description": "指导 AI 根据需求生成 React 页面草稿。",
  "version": "1.0.0",
  "status": "draft",
  "scope": "platform",
  "riskLevel": "medium",
  "applicableTechStacks": [
    {
      "domain": "frontend",
      "language": ["TypeScript"],
      "frameworks": ["React"],
      "projectKinds": ["application", "monorepo"]
    }
  ],
  "loadStages": ["implementation"],
  "content": {
    "purpose": "根据页面需求生成可维护的 React 页面结构。",
    "whenToUse": ["新增页面", "重构页面", "补充页面交互"],
    "inputs": ["页面需求", "路由信息", "组件库信息", "接口契约"],
    "outputs": ["页面组件草稿", "组件拆分建议", "测试建议"],
    "steps": [
      "确认页面路由和核心交互。",
      "确认使用的 UI 组件库。",
      "拆分页面、表单、表格、弹窗等组件。",
      "补充状态管理和接口调用策略。",
      "输出验收标准和测试建议。"
    ],
    "constraints": ["不得硬编码接口地址", "不得引入未确认依赖"],
    "forbiddenActions": ["禁止上传源码", "禁止自动部署"],
    "acceptanceCriteria": ["组件结构清晰", "状态职责明确", "交互路径可验证"],
    "fallbackStrategy": {
      "triggerCondition": "缺少组件库或接口契约信息",
      "action": "human-review",
      "diagnosticPrompt": "请补充组件库信息和接口契约。"
    },
    "testCases": [
      {
        "scenario": "生成用户列表页",
        "mockInput": "新增用户列表，包含筛选、表格、分页",
        "expectedBehavior": "输出页面拆分、组件职责、接口契约和测试建议。"
      }
    ],
    "telemetryTags": ["react-component", "api-contract"]
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

## 9. 示例：Rust Axum Handler 生成 Skill

```json
{
  "schemaVersion": "1.0.0",
  "kind": "skill",
  "slug": "backend-rust-axum-handler-generation-skill",
  "name": "Rust Axum Handler 生成技能",
  "description": "指导 AI 根据接口需求生成 Axum Handler、DTO、错误处理和测试建议。",
  "version": "1.0.0",
  "status": "draft",
  "scope": "platform",
  "riskLevel": "high",
  "applicableTechStacks": [
    {
      "domain": "backend",
      "language": ["Rust"],
      "frameworks": ["Axum"],
      "projectKinds": ["application", "monorepo"]
    }
  ],
  "loadStages": ["implementation", "diagnosing"],
  "content": {
    "purpose": "生成符合 Rust Axum 规范的接口 Handler 草稿。",
    "whenToUse": ["新增 Axum 接口", "生成 Request / Response DTO", "补充错误处理"],
    "inputs": ["接口需求", "请求结构", "响应结构", "错误类型", "状态管理方式"],
    "outputs": ["Handler 草稿", "DTO 约束", "错误处理策略", "测试建议"],
    "steps": [
      "确认路由、请求参数和响应结构。",
      "确认 AppState 和依赖注入方式。",
      "设计 Request / Response DTO。",
      "设计 Result / Error 返回策略。",
      "补充 tracing 和测试建议。"
    ],
    "constraints": ["不得忽略错误处理", "不得生成不安全代码", "不得要求上传源码"],
    "forbiddenActions": ["禁止生成 unsafe 代码", "禁止自动修改 Cargo.toml", "禁止自动部署"],
    "acceptanceCriteria": ["错误处理明确", "DTO 可序列化", "状态管理清晰", "测试建议完整"],
    "fallbackStrategy": {
      "triggerCondition": "缺少状态管理或错误类型定义",
      "action": "human-review",
      "diagnosticPrompt": "请补充 AppState、错误类型和序列化要求。"
    },
    "testCases": [
      {
        "scenario": "新增订单创建接口",
        "mockInput": "生成 POST /orders Axum Handler",
        "expectedBehavior": "输出 Handler、DTO、错误处理、tracing 和测试建议。"
      }
    ],
    "telemetryTags": ["rust-axum", "api-contract"]
  },
  "dependencies": [],
  "quality": {
    "score": 88,
    "checks": [],
    "warnings": ["Rust 类型和生命周期复杂，建议人工 Review。"]
  }
}
```

---

## 10. 校验清单

Skill 进入 Hub 审核前必须满足：

- [ ] kind = skill。
- [ ] slug 合法。
- [ ] version 合法。
- [ ] status = draft。
- [ ] riskLevel 存在。
- [ ] applicableTechStacks 非空。
- [ ] purpose 非空。
- [ ] whenToUse 非空。
- [ ] inputs 非空。
- [ ] outputs 非空。
- [ ] steps 非空。
- [ ] constraints 非空。
- [ ] forbiddenActions 非空。
- [ ] acceptanceCriteria 非空。
- [ ] fallbackStrategy 合法。
- [ ] testCases 至少一个。
- [ ] telemetryTags 1 到 3 个。
- [ ] 不包含源码级业务代码。
- [ ] 不要求上传源码。
- [ ] 质量分 >= 80。

---

## 11. 知识库使用建议

建议将本文放入扣子知识库：

```text
知识库名称：hub-asset-schema
文档名称：Skill 规范文档
用途：供 AI Asset Factory Agent 生成 Skill 资产、检查 Skill 质量、输出 Hub 导入 JSON。
```
