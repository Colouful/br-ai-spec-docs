# Agent 与 Skill 官方资料索引

## 用途

本文件用于帮助 AI 工程资产工厂识别标准 Agent、Skill、Tool、Workflow、Knowledge、Guardrail 等智能体工程资产的官方资料来源。

生成 Hub 平台中心资产时，应优先遵循 Hub 资产契约、团队智能体工程规范和平台实际约束，官方文档仅作为能力边界、术语定义和工程实践参考。

本文件重点服务于以下资产生成场景：

1. 标准 Skill 创建
2. 标准 Agent 创建
3. 多 Agent 协作设计
4. Agent 工具调用设计
5. Agent 工作流编排
6. Agent 知识库接入
7. Agent 安全边界、权限和审核机制设计
8. Agent / Skill 的 Manifest、Rule、Flow、Prompt、Guardrail 资产生成

## 官方资料索引

### Coze Skill

- 官方文档：https://docs.coze.cn/guides/skill_overview
- 适用场景：扣子 Skill 定义、Skill 结构、说明文件、元数据、代码脚本、智能体能力扩展。
- 使用说明：用于理解 Coze Skill 的官方概念和结构边界，不直接复制官方示例作为 Hub 资产正文。

### Coze 智能体开发

- 官方文档：https://www.coze.cn/open/docs/guides
- 适用场景：扣子智能体、低代码智能体、AI 应用构建、平台能力入口。
- 使用说明：用于确认扣子平台智能体开发入口和能力边界。

### Coze 工作流

- 官方文档：https://www.coze.cn/open/docs/guides/workflow
- 智能体工作流文档：https://www.coze.cn/open/docs/guides/agent_workflow
- 适用场景：低代码工作流、对话流、任务编排、节点串联、复杂业务流程自动化。
- 使用说明：用于生成 Flow 类资产时识别工作流节点、输入输出、执行路径和异常处理约束。

### Coze 插件

- 官方文档：https://www.coze.cn/open/docs/guides/plugin
- 智能体插件文档：https://www.coze.cn/open/docs/guides/agent_plugin
- 适用场景：插件、工具调用、外部 API 能力扩展、多模态能力扩展。
- 使用说明：用于生成 Tool / Plugin / Skill 调用规则时确认工具边界、输入输出和调用风险。

### Coze 知识库

- 官方文档：https://www.coze.cn/open/docs/guides/knowledge
- 智能体知识库文档：https://www.coze.cn/open/docs/guides/agent_knowledge
- 使用知识库文档：https://www.coze.cn/open/docs/guides/use_knowledge
- 适用场景：知识库接入、RAG、文档检索、外部知识增强、降低幻觉风险。
- 使用说明：用于生成 Knowledge / RAG 类资产时确认知识库接入方式、检索边界和引用要求。

### OpenAI Agents

- 官方文档：https://developers.openai.com/api/docs/guides/agents
- 适用场景：Agent 定义、模型配置、运行编排、工具调用、Handoff、Guardrail、人类审核、可观测性。
- 使用说明：用于参考标准 Agent 工程化设计，包括任务边界、工具调用、交接机制、安全防护和运行追踪。  
- **可访问性说明（校验）**：自动化 HTTP 拉取在部分环境会对 OpenAI 门户返回 403，不代表链接无效；**请以浏览器中人工打开为准**；与 Hub 能力冲突时仍以 Hub 契约为准。亦可与下方 OpenAI Agents SDK（Python）文档搭配使用，区分「平台总览」与「具体 SDK 行为」。

### OpenAI Agents SDK Python

- 官方文档：https://openai.github.io/openai-agents-python/
- Guardrails 文档：https://openai.github.io/openai-agents-python/guardrails/
- Handoffs 文档：https://openai.github.io/openai-agents-python/handoffs/
- 适用场景：多 Agent 编排、Agent 交接、Guardrail、安全校验、可追踪执行。
- 使用说明：用于生成企业级 Agent 资产时参考可靠性、安全性和可观测性约束。

### LangChain Agents

- Python 官方文档：https://docs.langchain.com/oss/python/langchain/agents
- JavaScript 官方文档：https://docs.langchain.com/oss/javascript/langchain/agents
- Tools 官方文档：https://docs.langchain.com/oss/python/langchain/tools
- Multi-agent 官方文档：https://docs.langchain.com/oss/python/langchain/multi-agent
- 适用场景：Agent、Tool、工具调用循环、多 Agent 模式、上下文工程。
- 使用说明：用于理解 Agent 与 Tool 的工程关系，不得直接套用到项目实现，除非项目技术栈明确使用 LangChain。

### LangGraph Workflows and Agents

- 官方文档：https://docs.langchain.com/oss/python/langgraph/workflows-agents
- 适用场景：工作流与 Agent 模式区分、固定流程、动态决策、复杂状态编排。
- 使用说明：用于判断某个需求更适合 Flow、Agent，还是 Agent + Workflow 混合模式。

### CrewAI Agents

- 官方文档：https://docs.crewai.com/en/concepts/agents
- Tools 文档：https://docs.crewai.com/en/concepts/tools
- Tasks 文档：https://docs.crewai.com/en/concepts/tasks
- Skills 文档：https://docs.crewai.com/en/skills
- 适用场景：角色型 Agent、任务分工、多 Agent 协作、工具能力、Coding Agent Skill。
- 使用说明：用于参考 Agent 角色、目标、工具、任务和协作关系的描述方式。

### AutoGen AgentChat

- 官方文档：https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/index.html
- Agents 文档：https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/agents.html
- Memory and RAG 文档：https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/memory.html
- 适用场景：多 Agent 对话、Agent 团队、消息传递、记忆、RAG。
- 使用说明：用于参考多 Agent 通信、团队协作和上下文记忆设计。

### Dify Agent

- 官方文档：https://docs.dify.ai/en/use-dify/build/agent
- Knowledge 文档：https://docs.dify.ai/en/use-dify/knowledge/readme
- 适用场景：可视化 Agent、工具调用、知识库、Agentic Workflow。
- 使用说明：用于参考低代码 Agent 平台中的 Agent、Workflow、Knowledge 组织方式。

## 使用原则

1. 本文件仅作为 Agent / Skill 官方资料索引，不替代 Hub 平台中心自身的资产契约。
2. 生成标准 Skill 时，必须明确：
   - Skill 名称
   - Skill 目标
   - 适用场景
   - 不适用场景
   - 输入参数
   - 输出结果
   - 依赖工具
   - 依赖知识库
   - 执行步骤
   - 风险边界
   - 验收标准
3. 生成标准 Agent 时，必须明确：
   - Agent 名称
   - Agent 角色定位
   - Agent 职责边界
   - 可调用 Skill
   - 可调用 Tool
   - 可访问 Knowledge
   - 工作流入口
   - 失败处理策略
   - 人工确认节点
   - 安全与权限边界
4. Agent 不应被设计成“万能助手”，必须有明确职责边界。
5. Skill 不应承载过多职责，应保持单一能力、可复用、可测试、可审计。
6. Tool / Plugin 调用必须声明输入、输出、失败情况、权限风险和调用限制。
7. Workflow 适合稳定、可预测、可编排的业务流程。
8. Agent 适合需要动态判断、工具选择、任务拆解和多轮推理的场景。
9. Knowledge / RAG 适合补充事实性知识，但不得替代权限校验、业务规则和人工审核。
10. 涉及权限、审批、资金、客户数据、生产发布、数据库变更、外部 API 写操作时，必须设置人工确认或门禁审批节点。
11. 不直接复制官方文档示例代码作为 Hub 资产内容。
12. 不虚构平台能力；无法确认的平台能力必须标记为“需要人工确认”。
13. 如果不同平台的 Agent / Skill 概念不一致，应以 Hub 平台中心的资产契约为准。
14. 输出的 Agent / Skill 资产必须可执行、可审核、可测试，而不是只描述抽象原则。
15. Agent / Skill 资产必须显式声明输入、输出、依赖、执行边界、失败处理、安全约束和验收标准。
16. 对外部系统有写操作、删除操作、审批操作、发布操作的 Agent，必须默认要求人工确认。
17. 对涉及用户隐私、企业数据、客户资料、财务、合同、订单、权限的场景，必须提高风险等级。
18. 不得让 Agent 绕过权限、审批、审计、日志、灰度和回滚机制。

## 标准 Skill 资产建议结构

生成标准 Skill 时，建议使用以下结构：

```yaml
skill:
  name: ""
  displayName: ""
  description: ""
  category: ""
  version: "0.1.0"

scope:
  goals: []
  nonGoals: []
  applicableScenarios: []
  excludedScenarios: []

inputs:
  parameters: []
  requiredContext: []
  optionalContext: []

outputs:
  resultFormat: ""
  artifacts: []
  sideEffects: []

dependencies:
  tools: []
  knowledgeBases: []
  workflows: []
  externalServices: []

execution:
  steps: []
  fallbackStrategy: ""
  humanApprovalRequired: false

guardrails:
  permissions: []
  dataSensitivity: ""
  riskLevel: ""
  prohibitedActions: []
  confirmationRequiredActions: []

quality:
  acceptanceCriteria: []
  testCases: []
  reviewChecklist: []
```

## 标准 Agent 资产建议结构

生成标准 Agent 时，建议使用以下结构：

```yaml
agent:
  name: ""
  displayName: ""
  role: ""
  description: ""
  version: "0.1.0"

responsibilities:
  primaryGoals: []
  secondaryGoals: []
  nonGoals: []

capabilities:
  skills: []
  tools: []
  workflows: []
  knowledgeBases: []

behavior:
  systemPrompt: ""
  taskPlanningStrategy: ""
  toolSelectionPolicy: ""
  responseStyle: ""
  clarificationPolicy: ""
  failureHandlingPolicy: ""

collaboration:
  upstreamAgents: []
  downstreamAgents: []
  handoffRules: []
  escalationRules: []

security:
  permissionBoundary: []
  approvalRequiredActions: []
  forbiddenActions: []
  dataHandlingRules: []

observability:
  logs: []
  traces: []
  metrics: []
  auditEvents: []

quality:
  acceptanceCriteria: []
  testCases: []
  reviewChecklist: []
```

## 标准 Agent / Skill 生成检查清单

生成 Agent 或 Skill 资产时，必须检查以下内容：

1. 是否有明确名称。
2. 是否有明确职责。
3. 是否有明确不做什么。
4. 是否有明确输入参数。
5. 是否有明确输出格式。
6. 是否有明确依赖工具。
7. 是否有明确依赖知识库。
8. 是否有明确执行步骤。
9. 是否有明确失败处理策略。
10. 是否有明确人工确认节点。
11. 是否有明确权限边界。
12. 是否有明确风险等级。
13. 是否有明确验收标准。
14. 是否有明确测试用例。
15. 是否有明确审计或日志要求。
16. 是否避免把 Agent 设计成万能助手。
17. 是否避免让 Skill 承担多个不相关职责。
18. 是否避免虚构平台不存在的能力。
19. 是否避免绕过审批、权限、审计和安全约束。
20. 是否能被后续 AI 工程执行器直接消费。

## 链接校验摘要

| 资料项 | 链接 | 校验结果 | 备注 |
|---|---|---|---|
| Coze Skill | https://docs.coze.cn/guides/skill_overview | 已确认：官方资料入口正确 | HTTP 200，扣子国内文档站 |
| Coze 智能体开发 | https://www.coze.cn/open/docs/guides | 已确认：官方资料入口正确 | HTTP 200，Coze 官方开放文档 |
| Coze 工作流 | https://www.coze.cn/open/docs/guides/workflow | 已确认：官方资料入口正确 | HTTP 200 |
| Coze Agent Workflow | https://www.coze.cn/open/docs/guides/agent_workflow | 已确认：官方资料入口正确 | HTTP 200 |
| Coze 插件 | https://www.coze.cn/open/docs/guides/plugin | 已确认：官方资料入口正确 | HTTP 200 |
| Coze Agent Plugin | https://www.coze.cn/open/docs/guides/agent_plugin | 已确认：官方资料入口正确 | HTTP 200 |
| Coze 知识库 | https://www.coze.cn/open/docs/guides/knowledge | 已确认：官方资料入口正确 | HTTP 200 |
| Coze Agent Knowledge | https://www.coze.cn/open/docs/guides/agent_knowledge | 已确认：官方资料入口正确 | HTTP 200 |
| Coze Use Knowledge | https://www.coze.cn/open/docs/guides/use_knowledge | 已确认：官方资料入口正确 | HTTP 200 |
| OpenAI Agents | https://developers.openai.com/api/docs/guides/agents | 需要人工确认：无法确认官方性或可访问性 | 本环境 `curl` 对 OpenAI 开发者门户返回 HTTP 403（可能为反爬/需浏览器会话）；**请在浏览器中人工验证**；域名归属 OpenAI 官方。 |
| OpenAI Agents SDK Python | https://openai.github.io/openai-agents-python/ | 已确认：官方资料入口正确 | HTTP 200，OpenAI 组织下 GitHub Pages 文档 |
| OpenAI Guardrails | https://openai.github.io/openai-agents-python/guardrails/ | 已确认：官方资料入口正确 | HTTP 200，同上子路径 |
| OpenAI Handoffs | https://openai.github.io/openai-agents-python/handoffs/ | 已确认：官方资料入口正确 | HTTP 200，同上子路径 |
| LangChain Python Agents | https://docs.langchain.com/oss/python/langchain/agents | 已确认：官方资料入口正确 | HTTP 200，LangChain 官方 docs 子域 |
| LangChain JavaScript Agents | https://docs.langchain.com/oss/javascript/langchain/agents | 已确认：官方资料入口正确 | HTTP 200 |
| LangChain Tools | https://docs.langchain.com/oss/python/langchain/tools | 已确认：官方资料入口正确 | HTTP 200 |
| LangChain Multi-agent | https://docs.langchain.com/oss/python/langchain/multi-agent | 已确认：官方资料入口正确 | HTTP 200 |
| LangGraph Workflows and Agents | https://docs.langchain.com/oss/python/langgraph/workflows-agents | 已确认：官方资料入口正确 | HTTP 200 |
| CrewAI Agents | https://docs.crewai.com/en/concepts/agents | 已确认：官方资料入口正确 | HTTP 200，CrewAI 官方文档站 |
| CrewAI Tools | https://docs.crewai.com/en/concepts/tools | 已确认：官方资料入口正确 | HTTP 200 |
| CrewAI Tasks | https://docs.crewai.com/en/concepts/tasks | 已确认：官方资料入口正确 | HTTP 200 |
| CrewAI Skills | https://docs.crewai.com/en/skills | 已确认：官方资料入口正确 | HTTP 200 |
| AutoGen AgentChat | https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/index.html | 已确认：官方资料入口正确 | HTTP 200，Microsoft org 的 GitHub Pages 文档 |
| AutoGen Agents | https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/agents.html | 已确认：官方资料入口正确 | HTTP 200 |
| AutoGen Memory and RAG | https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/memory.html | 已确认：官方资料入口正确 | HTTP 200 |
| Dify Agent | https://docs.dify.ai/en/use-dify/build/agent | 已确认：官方资料入口正确 | HTTP 200，Dify 官方英文文档站 |
| Dify Knowledge | https://docs.dify.ai/en/use-dify/knowledge/readme | 已确认：官方资料入口正确 | HTTP 200 |

## 风险提示

1. Agent / Skill 官方文档仅能作为参考，不能自动代表项目可以直接落地。
2. 不同平台对 Agent、Skill、Tool、Workflow 的定义可能不同。
3. 生成 Hub 资产时必须统一到 Hub 平台中心自己的资产模型。
4. 对外部工具调用、写操作、审批、权限、数据处理必须默认提高风险等级。
5. 对不确定的平台能力、版本差异、API 限制，必须输出“需要人工确认”。
6. 不允许通过 Agent 自动执行高风险操作，除非存在明确授权、审批、日志和回滚机制。

*OpenAI 等厂商文档的访问与版本更新频繁；上表不保证长期 URL 结构不变，关键页面变更请以厂商公告与站内导航为准。*
