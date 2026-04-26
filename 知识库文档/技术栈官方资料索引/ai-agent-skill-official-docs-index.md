---
id: ai-agent-skill-official-docs-index
title: AI Agent 与 Skill 框架官方资料索引
version: "1.0"
updated: "2026-04-26"
category: ai-agent
tags: [langgraph, crewai, autogen, semantic-kernel, pydantic-ai, vercel-ai-sdk, openai-agents, google-adk, mcp, dify, llama-index, official-docs]
---

# AI Agent 与 Skill 框架官方资料索引

## 用途
本文件用于帮助 AI 工程资产工厂识别 AI Agent、Skill、多智能体编排框架的官方资料来源。生成资产时，应**优先遵循 Hub 资产契约和团队 AI 工程标准**，官方文档仅用于确认框架能力边界与 API 行为事实。

## 技术栈索引

### 一、Agent 编排框架（Orchestration Frameworks）

| 技术名称 | 官方文档 | 文档类型 | 适用场景 | 检索关键词 | 风险等级 | 备注 |
|----------|----------|----------|----------|------------|----------|------|
| LangGraph | [langchain-ai.github.io/langgraph](https://langchain-ai.github.io/langgraph/) / [Python](https://langchain-ai.github.io/langgraph/) / [JS/TS](https://langchain-ai.github.io/langgraphjs/) | 综合文档 | 有状态 Agent 工作流、图编排、检查点、人机协同、时间旅行调试 | langgraph, state graph, checkpoint, interrupt, stream, subgraph, supervisor, langsmith | 中 | 与 LangChain 生态深度绑定，支持 Python/JS/TS，已稳定 1.0 GA |
| CrewAI | [docs.crewai.com](https://docs.crewai.com/) | 综合文档 | 角色扮演多智能体编排、自主 Agent 协作、任务流 | crewai, agent, crew, task, process, flow, tool, memory, knowledge | 低 | 独立框架（不依赖 LangChain），支持 Flow 与 Crew 两种编排模式 |
| AutoGen (Microsoft) | [microsoft.github.io/autogen/stable](https://microsoft.github.io/autogen/stable/) / [0.2 旧版](https://microsoft.github.io/autogen/0.2/) | 框架文档 | 多智能体对话、事件驱动架构、分布式 Agent 系统、.NET/Python 跨语言 | autogen, multi-agent, conversation, event-driven, group chat, xlang, distributed | 中 | 0.4 为最新事件驱动架构，0.2 为旧版对话模式；已进入维护模式，微软推荐迁移至 Microsoft Agent Framework |
| Semantic Kernel (Microsoft) | [learn.microsoft.com/semantic-kernel](https://learn.microsoft.com/en-us/semantic-kernel/) / [GitHub Docs](https://github.com/MicrosoftDocs/semantic-kernel-docs) | SDK 文档 | 插件化 AI 应用、Planner、Agent Framework、Process Framework、C#/Python/Java | semantic kernel, plugin, planner, kernel, skill, agent framework, process | 低 | 微软官方 SDK，支持 C#/Python/Java；含 Agent Framework 与 Process Framework 两个高级框架 |
| Pydantic AI | [ai.pydantic.dev](https://ai.pydantic.dev/) | 框架文档 | 类型安全 Agent 开发、依赖注入、结构化输出、Logfire 可观测 | pydantic ai, agent, run, tool, dependency, structured output, logfire, llms.txt | 低 | Pydantic 团队出品，强调类型安全与生产级可靠性；提供 llms.txt 供 AI 助手索引 |
| Vercel AI SDK | [ai-sdk.dev](https://ai-sdk.dev/) / [sdk.vercel.ai/docs](https://sdk.vercel.ai/docs) | SDK 文档 | TypeScript 全栈 AI 应用、流式响应、工具调用、多模型统一 API、Agent 抽象 | vercel ai sdk, stream, tool, generateText, useChat, agent, mcp, provider | 低 | 前端/后端统一 SDK，支持 React/Next.js/Svelte；v6 引入原生 Agent 抽象与 MCP 支持 |
| OpenAI Agents SDK | [openai.github.io/openai-agents-python](https://openai.github.io/openai-agents-python/) / [platform.openai.com/docs/guides/agents-sdk](https://platform.openai.com/docs/guides/agents-sdk) | SDK 文档 | 轻量多智能体工作流、Handoff、Guardrails、Tracing、MCP 集成 | openai agents, handoff, guardrail, tool, trace, runner, session, sandbox | 中 | OpenAI 官方出品，Python/TypeScript 双版本；支持 100+ LLM 提供商（通过 LiteLLM） |
| Google ADK (Agent Development Kit) | [google.github.io/adk-docs](https://google.github.io/adk-docs/) / [Python](https://github.com/google/adk-python) / [Java](https://github.com/google/adk-java) / [TS](https://github.com/google/adk-js) | 综合文档 | Google Cloud 原生 Agent 开发、多智能体系统、A2A 协议、Agent Engine 部署 | google adk, agent development kit, gemini, tool, multi-agent, a2a, agent engine | 低 | Google 官方开源，模型无关（支持 Gemini/OpenAI 等），支持 Python/Java/TypeScript/Go/Web |

### 二、数据与上下文框架（Data & Context Frameworks）

| 技术名称 | 官方文档 | 文档类型 | 适用场景 | 检索关键词 | 风险等级 | 备注 |
|----------|----------|----------|----------|------------|----------|------|
| LlamaIndex | [docs.llamaindex.ai](https://docs.llamaindex.ai/en/stable/) | 数据框架文档 | RAG 系统、数据连接器、索引、查询引擎、Agent 数据层 | llamaindex, rag, index, retriever, query engine, data connector, agent, vector store | 低 | LLM 应用数据框架，支持 Python/TypeScript；提供多种索引策略与数据连接器 |
| Model Context Protocol (MCP) | [modelcontextprotocol.io](https://modelcontextprotocol.io/) / [specification](https://modelcontextprotocol.io/specification/2025-11-25) | 协议规范 | AI 应用与外部数据源/工具的标准化连接协议、Client-Server 架构 | mcp, model context protocol, resource, tool, prompt, server, client, stdio, sse | 低 | Anthropic 发起的开放协议，已成为事实标准；OpenAI/Google 等主流厂商均已支持 |

### 三、低代码 / 可视化 Agent 平台（Low-Code Platforms）

| 技术名称 | 官方文档 | 文档类型 | 适用场景 | 检索关键词 | 风险等级 | 备注 |
|----------|----------|----------|----------|------------|----------|------|
| Dify | [docs.dify.ai](https://docs.dify.ai/) | 平台文档 | 可视化 AI 应用构建、工作流编排、知识库、模型管理、API 发布 | dify, workflow, knowledge, chatbot, agent, model provider, prompt, api | 低 | 开源 LLM 应用开发平台，支持自托管与云服务；适合快速原型与生产部署 |

## AI 生成约束（强制执行）

1. **Agent 框架选型必须匹配团队技术栈与部署环境**。如团队使用 Google Cloud 优先推荐 ADK；使用 Azure 优先推荐 Semantic Kernel/AutoGen；前端全栈优先推荐 Vercel AI SDK。
2. **不虚构框架能力或版本特性**。涉及多智能体、持久化、分布式等高级特性时，必须核对官方文档确认支持状态，不确定时标记「需要人工确认」。
3. **禁止直接复制官方示例代码作为项目交付代码**。示例仅用于理解 API 行为，必须根据项目上下文重写。
4. **涉及 LLM 调用成本、Token 消耗、速率限制时，必须显式标注**。多智能体框架（如 AutoGen）单次任务可能产生 20+ LLM 调用。
5. **MCP 集成必须明确 Server 与 Client 角色**。禁止混淆 MCP Server（提供工具/资源）与 MCP Client（消费工具/资源）的架构边界。
6. **当官方文档与 Hub 资产规范冲突时，以 Hub 资产规范为准**。官方文档仅用于确认技术事实（如 API 签名、生命周期顺序、支持版本）。

## 变更日志

- `2026-04-26` v1.0: 初始版本，收录 11 个主流 Agent/Skill 框架