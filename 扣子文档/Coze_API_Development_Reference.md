# 扣子（Coze）开发文档 API 参考手册

> 整理日期：2026-04-26
> 用途：开发依据 / API 字段速查

---

## 目录

1. [API 调用方式概述](#1-api-调用方式概述)
2. [智能体开发（Vibe Coding）](#2-智能体开发vibe-coding)
3. [部署智能体为 API 服务](#3-部署智能体为-api-服务)
4. [通过 API 调用智能体](#4-通过-api-调用智能体)
5. [智能体管理 API](#5-智能体管理-api)
   - 5.1 创建智能体
   - 5.2 更新智能体
   - 5.3 查看智能体配置
6. [知识库管理 API](#6-知识库管理-api)
   - 6.1 创建知识库
   - 6.2 查看知识库列表
   - 6.3 修改知识库信息
   - 6.4 创建知识库文件
   - 6.5 修改知识库文件
7. [常见问题 FAQ](#7-常见问题-faq)

---

## 1. API 调用方式概述

### 1.1 调用方式总览

| 协议 | 调用方式 | 扣子域名 | 说明 |
|------|---------|---------|------|
| HTTP | 公网访问 | `https://api.coze.cn` | 所有用户均可使用，适用于常规 API 请求 |
| HTTP | 公网固定 IP 访问 | `https://static-api.coze.cn` | **仅企业版**支持，可将固定 IP 加入防火墙白名单 |
| HTTP | 私网连接访问 | `http://com.volces.privatelink.cn-beijing.epsvc-mjadtc7ir3sw5smt1a2gtwun` | **仅企业版**支持，协议为 `http` 非 `https` |
| WebSocket | 公网访问 | `wss://ws.coze.cn` | 基于 WebSocket OpenAPI 实现音频通话 |
| MCP | 公网访问 | `https://mcp.coze.cn` | 所有用户可用，通过 MCP 方式调用扣子插件商店中的付费插件 |

> **海外访问建议**：扣子公网域名全球可访问，但海外访问速度可能受跨境网络影响。建议海外用户优先使用海外域名访问。

### 1.2 通用请求头

| Header | 取值 | 说明 |
|--------|------|------|
| `Authorization` | `Bearer $AccessToken` | 用于验证客户端身份的访问令牌 |
| `Content-Type` | `application/json` | 解释请求正文的方式 |

### 1.3 通用响应结构

| 字段 | 类型 | 示例 | 说明 |
|------|------|------|------|
| `code` | Long | `0` | 调用状态码，`0` 表示成功，其他值表示失败 |
| `msg` | String | `""` | 状态信息，失败时包含详细错误信息 |
| `detail` | Object | `{"logid":"1234567890****"}` | 请求的详细日志信息，用于问题排查 |
| `data` | Object | — | 返回的业务数据 |

---

## 2. 智能体开发（Vibe Coding）

### 2.1 核心概念

- **Agent 模式**：扣子 AI 是"执行助手"，自主拆解任务、编写代码、自动调试，实现端到端闭环
- **问答模式**：扣子 AI 是"资深顾问"，专注辅助思考，不会改动项目，提供解释、优化建议或示例代码

### 2.2 工作流三层架构

| 层级 | 说明 |
|------|------|
| 语义层 | 自然语言描述驱动 |
| 参数层 | 输入输出参数配置 |
| 代码层 | 自动生成的代码实现 |

### 2.3 工作流节点类型

- **开始节点**：设定启动工作流需要的输入信息
- **结束节点**：返回工作流运行后的结果
- **任务执行节点**：核心功能单元，覆盖图像生成、数据库读写、第三方工具调用等

### 2.4 集成能力（技能）

| 能力类型 | 说明 |
|---------|------|
| 大语言模型 | 默认已开通，扣子 AI 自动添加 |
| 数据库 | 结构化数据托管，自动集成并设置 |
| 对象存储 | 非结构化数据托管，自动集成 |
| 外部集成 | 飞书消息、飞书多维表格等，需配置 |

### 2.5 关键限制

| 限制项 | 说明 |
|--------|------|
| 项目数量 | 存在可创建项目数量配额限制 |
| 回滚版本数 | 存在可回滚版本数配额限制 |
| 部署次数 | 存在可部署次数配额限制 |
| 文件上传 | 单个文件不可超过 **16 MB** |
| HTTP 连接 | 无数据传输时最长保持 **300 秒** |
| API Token | 每个项目最多 **10 个**，永久有效 |

### 2.6 环境变量

- 开发环境资源路径：`/workspace/project/assets`
- 生产环境资源路径：`/opt/bytefaas/assets`
- **建议**：使用 `COZE_WORKSPACE_PATH` 环境变量管理存储路径，设置为 `/$COZE_WORKSPACE_PATH/assets`

---

## 3. 部署智能体为 API 服务

### 3.1 部署流程

1. 在扣子编程左侧导航栏选择 **项目管理**
2. 筛选带有 `New` 标签的智能体，单击目标项目
3. 在 AI 编程开发界面右上角，单击 **部署**
4. 填写部署配置，单击 **开始部署**
5. 部署成功后，系统自动启用 **API 渠道**（默认开启且无法关闭）

### 3.2 渠道说明

| 渠道 | 默认状态 | 可关闭 | 说明 |
|------|---------|--------|------|
| API 渠道 | 自动开启 | ❌ 无法关闭 | 确保智能体始终可通过编程方式调用 |
| Web SDK | 需手动开启 | ✅ 可随时关闭 | 提供网页嵌入式聊天窗口 |

### 3.3 分享方式

- **API 请求示例分享**：开发页面右上角单击分享 → 获取 API 请求示例，对方调用时需将 API Token 包含在请求头 `Authorization` 参数中
- **Web SDK 分享链接**：分享产物页签 → 设为公开可见 → 获取分享链接

### 3.4 部署版本与数据同步策略

| 场景 | 数据库同步策略 |
|------|---------------|
| **首次部署** | 支持同步开发环境的表数据至生产环境；不勾选则仅同步表结构（Schema） |
| **后续部署** | 仅同步开发环境的表结构（Schema）变更，不同步具体数据 |
| **回滚编辑版本** | 勾选"同时回滚数据库"：还原至对应版本状态，该版本之后的数据将丢失（含 Schema 和数据）；不勾选：不影响数据库 |
| **回滚部署版本** | 暂不支持回滚数据库，生产环境数据保持不变 |

### 3.5 部署限制

- 仅支持通过 API 调用**生产环境运行版本**的智能体或工作流，**不能调用历史部署版本**
- 重新部署后，原有的 **API Token 仍然有效**，不同部署版本的 API Token 通用
- 目前项目部署的服务器为**固定配置**，暂不支持扩容和修改服务器资源
- 目前 AI 编程项目**暂不支持下线操作**，部署成功后无法撤销部署；如需停止访问，需删除项目
- 通过 AI 编程开发的智能体**暂时只支持发布为 API**，不支持发布到以前的官方和公共渠道

---

## 4. 通过 API 调用智能体

### 4.1 获取 API 访问信息

1. 在智能体开发页面右侧新建页签 → 选择 **部署**
2. 在部署总览页面，单击某条部署记录右侧的 **更多** → **查看**
3. 在 **API 请求示例及接口说明** 页面查看：
   - API 访问地址
   - 请求 Header
   - 请求参数

### 4.2 创建 API Token

1. 在 **API 请求示例及接口说明** 页面，单击 **管理 API Token**
2. 单击 **创建 API Token**
3. **复制并妥善保存**（令牌仅展示一次）

> ⚠️ **安全提示**：不要在浏览器或其他客户端代码中暴露 API Token。

### 4.3 调用接口说明

| 项目 | 说明 |
|------|------|
| 请求地址格式 | `https://<your_domain>/stream_run` |
| 响应方式 | **流式响应（SSE）**，服务端以数据流形式逐条发送事件 |
| 认证方式 | 请求头 `Authorization: Bearer <YOUR_TOKEN>` |

### 4.4 请求示例

```bash
curl --location --request POST "https://<your_domain>/stream_run" \
   --header "Authorization: Bearer <YOUR_TOKEN>" \
   --header "Content-Type: application/json" \
   --data '{
     "project_id": 75872598284063****
   }'
```

> **注意**：AI 编程项目中**不兼容**低代码 API 文档中的上传文件等 API。

---

## 5. 智能体管理 API

### 5.1 创建智能体

#### 接口信息

| 项目 | 内容 |
|------|------|
| 请求方式 | `POST` |
| 请求地址 | `https://api.coze.cn/v1/bot/create` |

#### 请求参数（Body）

| 参数 | 类型 | 是否必选 | 说明 |
|------|------|---------|------|
| `space_id` | String | ✅ 必选 | 智能体所在空间 ID |
| `name` | String | — | 智能体名称 |
| `description` | String | — | 智能体描述 |
| `icon_file_id` | String | — | 头像文件 ID（需先上传文件获取） |
| `prompt` | String | — | 人设与回复逻辑（提示词） |
| `prologue` | String | — | 开场白 |
| `suggested_questions` | Array | — | 推荐问题列表 |
| `model_id` | String | — | 模型 ID |
| `plugin_id` | String | — | 插件 ID |
| `api_id` | String | — | API ID |

#### 请求示例

```bash
curl --location --request POST 'https://api.coze.cn/v1/bot/create' \
--header 'Authorization: Bearer $AccessToken' \
--header 'Content-Type: application/json' \
--data '{
  "space_id": "736142423532160****",
  "name": "中餐大厨",
  "description": "每天教你一道菜的做法，暑假之后你将成为中餐大厨～",
  "icon_file_id": "73694959811****",
  "prompt": "你是一位经验丰富的中餐大厨，能够熟练传授各类中餐的烹饪技巧，每日为大学生厨师小白教学一道经典中餐的制作方法。",
  "prologue": "欢迎你，学徒，今天想学一道什么样的菜？",
  "suggested_questions": [],
  "model_id": "1706077826",
  "plugin_id": "731198934927553****",
  "api_id": "735057536617362****"
}'
```

#### 响应参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `bot_id` | String | 创建成功的智能体唯一标识 |
| `logid` | String | 请求日志 ID |

---

### 5.2 更新智能体

#### 接口信息

| 项目 | 内容 |
|------|------|
| 请求方式 | `POST` |
| 请求地址 | `https://api.coze.cn/v1/bot/update` |

#### 请求参数（Body）

| 参数 | 类型 | 是否必选 | 说明 |
|------|------|---------|------|
| `bot_id` | String | ✅ 必选 | 要更新的智能体 ID |
| `name` | String | — | 智能体名称 |
| `description` | String | — | 智能体描述 |
| `icon_file_id` | String | — | 头像文件 ID |
| `prompt` | String | — | 人设与回复逻辑 |
| `prologue` | String | — | 开场白 |
| `suggested_questions` | Array | — | 推荐问题列表 |
| `model_id` | String | — | 模型 ID |
| `plugin_id` | String | — | 插件 ID |
| `api_id` | String | — | API ID |

> **限制**：不支持通过 API 绑定火山知识库，只能绑定扣子知识库。

#### 请求示例

```bash
curl --location --request POST 'https://api.coze.cn/v1/bot/update' \
--header 'Authorization: Bearer pat_OYDacMzM3WyOWV3Dtj2bHRMymzxP****' \
--header 'Content-Type: application/json' \
--data '{
  "bot_id": "73428668****",
  "description": "每天教你一道菜的做法，暑假之后你将成为中餐大厨～",
  "icon_file_id": "73694959811****",
  "prompt": "你是一位经验丰富的中餐大厨...",
  "plugin_id": "731198934927553****",
  "api_id": "735057536617362****",
  "prologue": "欢迎你，学徒，今天想学一道什么样的菜？",
  "suggested_questions": [],
  "model_id": "1706077826"
}'
```

---

### 5.3 查看智能体配置

#### 接口信息

| 项目 | 内容 |
|------|------|
| 请求方式 | `GET` |
| 请求地址 | `https://api.coze.cn/v1/bots/:bot_id` |
| 权限要求 | `getMetadata`（访问令牌需开通此权限） |

#### 路径参数

| 参数 | 类型 | 是否必选 | 示例 | 说明 |
|------|------|---------|------|------|
| `bot_id` | String | ✅ 必选 | `73428668****` | 智能体 ID，从开发页面 URL 中 `bot` 参数后获取 |

#### Query 参数

| 参数 | 类型 | 是否必选 | 示例 | 说明 |
|------|------|---------|------|------|
| `is_published` | Boolean | 可选 | `true` | 筛选发布状态，默认 `true`。<br>`true`：查看已发布版本；`false`：查看草稿版本 |

#### 响应参数（data 字段 - BotInfo 对象）

| 参数 | 类型 | 示例 | 说明 |
|------|------|------|------|
| `bot_id` | String | `73428668****` | 智能体唯一标识 |
| `name` | String | `新闻` | 智能体名称 |
| `description` | String | `每天给我推送 AI 相关的新闻。` | 描述信息 |
| `icon_url` | String | `https://example.com/icon.png` | 头像地址 |
| `create_time` | Long | `1715689059` | 创建时间（Unix 时间戳，秒） |
| `update_time` | Long | `1716388526` | 更新时间（Unix 时间戳，秒） |
| `version` | String | `171638852****` | 最新版本号 |
| `prompt_info` | Object | `{"prompt": "..."}` | 提示词配置 |
| `onboarding_info` | Object | `{ "prologue": "...", "suggested_questions": [...] }` | 开场白配置 |
| `bot_mode` | Integer | `0` | 智能体模式：`0` 单 Agent，`1` 多 Agent |
| `plugin_info_list` | Array | `[{"plugin_id":"...", "name":"...", ...}]` | 插件列表 |
| `model_info` | Object | `{"model_id":"1706077826", "model_name":"豆包·Function call模型", ...}` | 模型配置信息 |
| `folder_id` | String | `752316125533***` | 所属文件夹 ID |
| `knowledge` | Object | `{ "knowledge_infos": [{"id":"...", "name":"..."}] }` | 绑定的知识库 |
| `variables` | Array | — | 变量列表 |
| `media_config` | Object | `{"is_voice_call_closed":false}` | 语音通话配置 |
| `owner_user_id` | String | `368567****` | 创建者扣子用户 ID |
| `voice_info_list` | Array | `[{"voice_id":"...", "language_code":"zh"}]` | 音色配置 |
| `shortcut_commands` | Array | `[{"id":"...", "name":"...", "command":"/sc_demo", ...}]` | 快捷指令 |
| `workflow_info_list` | Array | `[{"id":"...", "name":"...", ...}]` | 工作流列表 |
| `background_image_info` | Object | — | 背景图片配置 |
| `default_user_input_type` | String | `text` | 默认用户输入方式：`text`/`voice`/`call` |

#### model_info 详细字段

| 字段 | 说明 |
|------|------|
| `model_id` | 模型 ID |
| `model_name` | 模型名称 |
| `top_k` | Top-K 采样 |
| `top_p` | Top-P 采样 |
| `temperature` | 温度参数 |
| `max_tokens` | 最大 Token 数 |
| `context_round` | 上下文轮数 |
| `response_format` | 响应格式 |
| `presence_penalty` | 存在惩罚 |
| `frequency_penalty` | 频率惩罚 |
| `parameters` | 扩展参数，如 `{"thinking_type":"enabled"}` |

---

## 6. 知识库管理 API

> **重要区分**：知识库分为**扣子知识库**和**火山知识库**。以下 API **仅适用于扣子知识库**。

### 6.1 创建知识库

#### 接口信息

| 项目 | 内容 |
|------|------|
| 请求方式 | `POST` |
| 请求地址 | `https://api.coze.cn/v1/datasets` |

#### 请求参数（Body）

| 参数 | 类型 | 是否必选 | 说明 |
|------|------|---------|------|
| `space_id` | String | ✅ 必选 | 空间 ID |
| `name` | String | — | 知识库名称 |
| `file_id` | String | — | 知识库图标文件 ID（需先上传文件） |
| `description` | String | — | 知识库描述 |
| `format_type` | String | — | 知识库格式类型 |

#### 请求示例

```bash
curl --location --request POST 'https://api.coze.cn/v1/datasets' \
--header 'Authorization: Bearer pat_xitq9LWlowpX3qGCih1lwpAdzvXN****' \
--header 'Content-Type: application/json' \
--data '{
  "space_id": "731121948439879****",
  "name": "人工智能知识库",
  "file_id": "744667846938145****",
  "description": "包含机器学习、深度学习等内容"
}'
```

#### 响应参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `dataset_id` | String | 创建成功的知识库 ID |
| `logid` | String | 请求日志 ID |

> **限制**：暂不支持通过 API 创建表格知识库。

---

### 6.2 查看知识库列表

#### 接口信息

| 项目 | 内容 |
|------|------|
| 请求方式 | `GET` |
| 请求地址 | `https://api.coze.cn/v1/datasets` |

#### Query 参数

| 参数 | 类型 | 是否必选 | 示例 | 说明 |
|------|------|---------|------|------|
| `space_id` | String | ✅ 必选 | `731121948439879****` | 空间 ID |
| `name` | String | 可选 | `知识库` | 按名称筛选 |
| `format_type` | String | 可选 | — | 按格式类型筛选 |
| `page_num` | Integer | 可选 | `1` | 页码 |
| `page_size` | Integer | 可选 | `5` | 每页数量 |

#### 请求示例

```bash
curl --location --request GET 'https://api.coze.cn/v1/datasets?space_id=731121948439879****&name=知识库&format_type=&page_num=1&page_size=5' \
--header 'Authorization: Bearer pat_O*****' \
--header 'Content-Type: application/json'
```

#### 响应参数（列表项字段）

| 参数 | 类型 | 示例 | 说明 |
|------|------|------|------|
| `dataset_id` | String | `744668935865830****` | 知识库 ID |
| `name` | String | `人工智能知识库` | 知识库名称 |
| `description` | String | `openapi` | 描述 |
| `icon_url` | String | `https://...` | 图标 URL |
| `icon_uri` | String | `FileBizType.BIZ_DATASET_ICON/...` | 图标 URI |
| `space_id` | String | `731121948439879****` | 空间 ID |
| `creator_id` | String | `217526895615****` | 创建者 ID |
| `create_time` | Long | `1733817948` | 创建时间（Unix 时间戳） |
| `update_time` | Long | `1733817948` | 更新时间（Unix 时间戳） |
| `processing_file_id_list` | Array | `[]` | 处理中的文件 ID 列表 |
| `processing_file_list` | Array | `[]` | 处理中的文件列表 |
| `avatar_url` | String | `https://...` | 创建者头像 URL |

> **限制**：暂不支持通过 API 查看低代码应用中的知识库；暂不支持查看火山知识库中的文件列表等详细信息。

---

### 6.3 修改知识库信息

#### 接口信息

| 项目 | 内容 |
|------|------|
| 请求方式 | `PUT` |
| 请求地址 | `https://api.coze.cn/v1/datasets/:dataset_id` |

#### 路径参数

| 参数 | 类型 | 是否必选 | 说明 |
|------|------|---------|------|
| `dataset_id` | String | ✅ 必选 | 要修改的知识库 ID |

#### 请求参数（Body）

| 参数 | 类型 | 是否必选 | 说明 |
|------|------|---------|------|
| `name` | String | — | 知识库名称 |
| `file_id` | String | — | 图标文件 ID |
| `description` | String | — | 知识库描述 |

> ⚠️ **注意**：此接口会**全量刷新** `name`、`file_id` 和 `description`，如果未设置这些参数，参数将恢复默认配置。

#### 请求示例

```bash
curl --location --request PUT 'https://api.coze.cn/v1/datasets/744668935865830****' \
--header 'Authorization: Bearer pat_qad2rHYNqKnCmRYZW4PhVRibaS***' \
--header 'Content-Type: application/json' \
--data '{
  "name": "AI 知识库",
  "file_id": "74466784693814****",
  "description": "这是一个关于人工智能的知识库，包含机器学习、深度学习等内容。"
}'
```

> **限制**：仅支持修改本人为所有者的知识库信息。

---

### 6.4 创建知识库文件

#### 接口信息

| 项目 | 内容 |
|------|------|
| 请求方式 | `POST` |
| 请求地址 | `https://api.coze.cn/open_api/knowledge/document/create` |

#### 上传方式

支持三种上传方式（每次请求只能选择一种）：
1. **上传本地文件**：通过 `file_base64` 上传
2. **上传在线网页**：通过网页 URL 上传
3. **通过 file_id 上传图片**：先上传文件获取 `file_id`

#### 请求参数（Body）

| 参数 | 类型 | 是否必选 | 说明 |
|------|------|---------|------|
| `dataset_id` | String | ✅ 必选 | 知识库 ID |
| `document_name` | String | — | 文件名称 |
| `file_base64` | String | 条件必选 | 本地文件的 Base64 编码（方式1） |
| `file_id` | String | 条件必选 | 已上传文件的 ID（方式3） |
| `url` | String | 条件必选 | 在线网页 URL（方式2） |
| `remove_extra_spaces` | Boolean | — | 是否移除多余空格，默认 `false` |
| `remove_urls_emails` | Boolean | — | 是否移除 URL 和邮箱，默认 `false` |
| `caption_type` | String | — | 图片标注类型：`system`（系统标注）或 `manual`（手动标注） |

#### 响应参数

| 参数 | 类型 | 示例 | 说明 |
|------|------|------|------|
| `document_id` | String | `738694205603010****` | 文件唯一标识 |
| `tos_uri` | String | `FileBizType.BIZ_BOT_DATASET/...` | 文件存储 URI |
| `create_time` | Long | `1719907964` | 创建时间 |
| `update_time` | Long | `1719907969` | 更新时间 |
| `remove_extra_spaces` | Boolean | `false` | 是否移除多余空格 |
| `remove_urls_emails` | Boolean | `false` | 是否移除 URL 和邮箱 |
| `logid` | String | — | 请求日志 ID |

#### 请求示例（本地文件）

```bash
curl --location --request POST 'https://api.coze.cn/open_api/knowledge/document/create' \
--header 'Authorization: Bearer pat_****' \
--header 'Content-Type: application/json' \
--data '{
  "dataset_id": "736356924530694****",
  "document_name": "文档名称",
  "file_base64": "5rWL6K+V5LiA5LiL5ZOm",
  "remove_extra_spaces": false,
  "remove_urls_emails": false
}'
```

> **限制**：
> - 每次最多可上传 **10 个文件**
> - 必须上传和知识库类型匹配的文件
> - 仅知识库的所有者可以上传文件
> - 上传图片选择手动标注时，还需调用**更新知识库图片描述 API** 手动设置标注

---

### 6.5 修改知识库文件

#### 接口信息

| 项目 | 内容 |
|------|------|
| 请求方式 | `POST` |
| 请求地址 | `https://api.coze.cn/open_api/knowledge/document/update` |

#### 请求头

| Header | 取值 | 说明 |
|--------|------|------|
| `Authorization` | `Bearer $AccessToken` | 访问令牌 |
| `Content-Type` | `application/json` | 内容类型 |
| `Agw-Js-Conv` | `str` | 必需头 |

#### 请求参数（Body）

| 参数 | 类型 | 是否必选 | 说明 |
|------|------|---------|------|
| `document_id` | String | ✅ 必选 | 要修改的文件 ID |
| `document_name` | String | — | 新的文件名称 |

#### 请求示例

```bash
curl --location --request POST 'https://api.coze.cn/open_api/knowledge/document/update' \
--header 'Authorization: Bearer pat_OYDacMzM3WyOWV3Dtj2bHRMymzxP****' \
--header 'Content-Type: application/json' \
--header 'Agw-Js-Conv: str' \
--data '{
  "document_id": "738694205603010****",
  "document_name": "cozeoverview"
}'
```

---

## 7. 常见问题 FAQ

### 7.1 权限与协作

| 问题 | 解答 |
|------|------|
| 谁可以编辑/部署项目？ | 仅项目所有者能编辑和部署。工作空间所有者或其他成员无法编辑非本人创建的项目。 |
| 项目能否跨工作空间复制？ | 默认支持。但如果项目中接入了外部集成（如飞书消息等），则无法跨空间复制。 |
| 外部集成被禁用后，已配置的是否还能用？ | 如果禁用前已完成配置，则该空间内不受影响，仍可正常使用。 |
| 为什么空间内项目都用同一个飞书机器人？ | 外部集成采用空间内一次性配置原则，所有项目共享使用。 |

### 7.2 模型相关

| 问题 | 解答 |
|------|------|
| 如何查看/切换智能体使用的模型？ | 在智能体开发页面的预览窗口单击模型名称进行切换。切换后需重新部署才能生效。 |
| 模型即将停运怎么办？ | 工作空间所有者或管理员可批量切换模型。停运 7 天内仍支持批量切换。仅作用于已部署的线上版本。 |
| 能否接入第三方模型？ | 支持。可通过自然语言描述需求并提供 API Key、接口地址等信息，让扣子 AI 自动接入。 |

### 7.3 数据库与存储

| 问题 | 解答 |
|------|------|
| 不同项目的数据库能否共享？ | **不能**，相互独立。需在开发时通过与扣子 AI 对话为项目接入数据库能力。 |
| 不同项目的对象存储能否共享？ | **不能**，相互独立。需在开发时通过与扣子 AI 对话接入对象存储能力。 |
| 不同项目的环境变量能否共享？ | **不能**，相互独立。 |
| 如何实现级联删除？ | 创建数据表时添加外键关系，配置 `Cascade`/`Restrict`/`Set NULL`/`Set default`/`No action` 规则。 |

### 7.4 文件与资源

| 问题 | 解答 |
|------|------|
| 部署后资源加载失败？ | 开发环境与生产环境存储路径不一致。建议使用 `COZE_WORKSPACE_PATH` 环境变量管理路径。 |
| 文件超过 16MB 怎么办？ | 让扣子 AI 实现分片上传，单个分片不大于 4MB。 |
| 如何下载 AI 生成的文件？ | 开发页面右上角 → 文件夹图标打开文件树 → 单击下载图标一键压缩下载。 |

### 7.5 连接与部署

| 问题 | 解答 |
|------|------|
| HTTP 连接超时？ | 无数据传输时最长保持 300 秒。生图、多轮对话等场景需至少每 300 秒发送一次心跳信号。 |
| 忘了 API Token 怎么办？ | 重新创建新的 API Token。 |
| 部署失败如何修复？ | 1) 单击"一键修复"按钮；2) 或复制错误日志到对话框让 AI 修复。 |
| 能否调用历史部署版本？ | **不能**，仅支持调用生产环境运行版本。 |
| 重新部署后 API Token 是否有效？ | **仍然有效**，不同部署版本的 API Token 通用。 |
| 能否下线已部署项目？ | **暂不支持**。如需停止访问，只能删除项目。 |

### 7.6 域名与备案

| 问题 | 解答 |
|------|------|
| 使用自定义域名是否需要备案？ | **需要**。扣子编程自动部署在火山引擎服务器上，需在火山引擎备案系统重新备案。 |
| 备案需要多久？ | 通常 1~20 个工作日。 |
| 没有火山引擎云服务器能否用自定义域名？ | **不可以**。必须在火山引擎账号下购买符合备案条件的云服务器。 |
| 免费 SSL 证书有效期多久？ | 3 个月。付费火山证书一般 1 年。 |
| 免费证书额度多少？ | 主账号及子账号一个自然年内共享 **20 个**免费证书额度。 |

### 7.7 外部集成

| 问题 | 解答 |
|------|------|
| 向飞书多维表格推送数据报错 `FieldNameNotFound`？ | 工作流输出字段名称与多维表格表头名称不匹配，或数据类型不匹配。需严格对应。 |
| 企业微信发送图片报错 `SignatureDoesNotMatch`？ | 企业微信会在图片 URL 后添加参数导致签名不一致。建议先调用企业微信图片上传接口上传至素材库获取官方资源 ID。 |
| 企业旗舰版为何无法使用外部集成？ | 默认处于关闭状态，需由组织管理员在集成管理页面为指定工作空间启用。 |

---

## 附录：智能体配置完整字段参考

### BotInfo 对象结构

```json
{
  "bot_id": "String",
  "name": "String",
  "description": "String",
  "icon_url": "String",
  "create_time": "Long (Unix timestamp)",
  "update_time": "Long (Unix timestamp)",
  "version": "String",
  "prompt_info": {
    "prompt": "String"
  },
  "onboarding_info": {
    "prologue": "String",
    "suggested_questions": ["String"]
  },
  "bot_mode": "Integer (0=单Agent, 1=多Agent)",
  "plugin_info_list": [
    {
      "plugin_id": "String",
      "name": "String",
      "icon_url": "String",
      "description": "String",
      "api_info_list": [
        {
          "api_id": "String",
          "name": "String",
          "description": "String"
        }
      ]
    }
  ],
  "model_info": {
    "model_id": "String",
    "model_name": "String",
    "top_k": "Integer",
    "top_p": "Float",
    "temperature": "Float",
    "max_tokens": "Integer",
    "context_round": "Integer",
    "response_format": "String",
    "presence_penalty": "Float",
    "frequency_penalty": "Float",
    "parameters": "Object"
  },
  "folder_id": "String",
  "knowledge": {
    "knowledge_infos": [
      {
        "id": "String",
        "name": "String"
      }
    ]
  },
  "variables": "Array",
  "media_config": {
    "is_voice_call_closed": "Boolean"
  },
  "owner_user_id": "String",
  "voice_info_list": [
    {
      "voice_id": "String",
      "language_code": "String"
    }
  ],
  "shortcut_commands": [
    {
      "id": "String",
      "name": "String",
      "command": "String",
      "description": "String",
      "query_template": "String",
      "icon_url": "String",
      "components": [
        {
          "name": "String",
          "description": "String",
          "type": "String",
          "tool_parameter": "String",
          "default_value": "String",
          "is_hide": "Boolean"
        }
      ],
      "tool": {
        "name": "String",
        "type": "String"
      }
    }
  ],
  "workflow_info_list": [
    {
      "id": "String",
      "name": "String",
      "description": "String",
      "icon_url": "String"
    }
  ],
  "background_image_info": "Object",
  "default_user_input_type": "String (text/voice/call)"
}
```

---

> **文档说明**：本文档基于扣子（Coze）官方开发文档整理，涵盖智能体开发、工作流开发、API 部署、智能体管理 API、知识库管理 API 及常见问题。所有 API 字段均从官方文档提取，可作为开发依据使用。
