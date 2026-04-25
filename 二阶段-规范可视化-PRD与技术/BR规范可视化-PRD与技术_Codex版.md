<!--
Codex 使用说明：
1. 先阅读全文，不要直接全量改代码。
2. 先输出“实现计划 + 文件影响清单 + 风险点 + 第一阶段 PR 范围”。
3. 第一阶段只做开发者当前专家工作台、动态专家流、门禁审批、规范资产入口。
-->

# br-ai-spec-visual: PRD + 开发实现技术文档

主题：当前专家工作台、动态专家流、门禁审批、OpenSpec 治理驾驶舱

版本：v2.0｜日期：2026-04-24

适用项目：Colouful/br-ai-spec-visual 与 Colouful/br-ai-spec（ai-spec-auto）

交付目标：让 Codex 能按本文档直接完成产品改造、数据模型补齐、页面开发、API 接入、验收测试。

# 文档结论摘要

| 决策项 | 结论 |
| --- | --- |
| 默认首页 | /w/[slug] 默认进入“开发者当前专家工作台”，不再默认进入 overview。 |
| 第一视觉 | 当前专家为一级视觉；阶段、任务、flow、run 状态作为二级小字描述。 |
| 流程来源 | 流程必须从 .agents/registry/flows.json 读取；专家必须从 .agents/registry/roles.json 读取；Visual 不写死流程和专家。 |
| 交互方式 | 点击专家节点、阶段节点、资产摘要时打开右侧抽屉，减少页面跳转。 |
| 门禁审批 | 专家工作台 P0 能力；waiting-approval 时按钮区优先展示“批准通过 / 驳回修改 / 查看待审资产”。 |
| 资产重点 | 规范资产是核心资产；需同时识别 openspec/ 与 .ai-spec/history/<run-id>/。 |
| 管理员页 | /admin 做多项目 OpenSpec 治理总览；/w/[slug]/admin 做单项目治理详情。 |

# 一、背景与项目理解

br-ai-spec（ai-spec-auto）是一套面向前端项目的 AI 规范驱动开发底座。它把项目规则、专家资产、IDE 命令入口、OpenSpec 交付产物和 .ai-spec 运行状态放进同一个项目，使 AI 开发能按统一约束执行、留痕、归档和复用。

br-ai-spec-visual 是 ai-spec-auto 的可视化与控制面，聚合已接入规范的本地/团队项目运行态、变更、拓扑与采集数据，并通过 Collector 扫描 .ai-spec/、.agents/registry/、.omx/logs/、openspec/ 等目录上报。

本轮改造的核心问题不是“UI 不够好看”，而是信息架构主次错位：现有能力偏向 Runs / Changes / Specs / Topology 等资源模块并列展示，而真实开发者心智是“当前哪个专家正在推进、是否被门禁卡住、下一步我要做什么、规范资产在哪里”。

# 二、目标用户与场景

| 用户 | 核心问题 | 主入口 | 页面目标 |
| --- | --- | --- | --- |
| 开发者 | 当前 run 进行到哪个专家？我需要点击什么？是否需要审批？ | /w/[slug] | 当前专家工作台 |
| 管理员 / 领导 | OpenSpec 是否用起来？变更与归档是否闭环？哪些项目卡住？ | /admin | 多项目 OpenSpec 治理总览 |
| 项目负责人 | 单项目规范资产是否健康？未归档风险在哪里？ | /w/[slug]/admin | 单项目治理详情 |

# 三、产品范围

## P0 必须完成

- /w/[slug] 默认进入开发者当前专家工作台。
- CurrentExpertHero：突出当前专家，显示中文名、英文 code、当前阶段、任务摘要、run 状态、门禁状态。
- DynamicExpertFlow：从 FlowInstance.nodes 渲染动态专家流，不写死五阶段，不写死专家。
- GateApprovalPanel：门禁审批作为专家工作台 P0 功能，支持批准、驳回、要求补充、查看待审资产。
- StageDrawer：点击专家/节点后右侧抽屉展示概览、规范资产、时间线、队列/日志、门禁审批。
- SpecAssetPanel：识别 openspec/ 正式资产与 .ai-spec/history/<run-id>/ 轻量历史资产。
- /admin：多项目 OpenSpec 治理总览，第一屏突出活跃 Change、待评审、待归档、已归档、归档成功率、资产增长。
## P1 应完成

- /w/[slug]/admin 单项目 OpenSpec 治理详情。
- OpenSpec 变更闭环漏斗：proposal -> design -> tasks -> apply -> verify -> archive。
- 多项目卡片：当前专家、活跃 Change、待归档、已归档、规范资产数、轻量历史任务数、健康状态。
- 资产健康度：过期规范、未归档变更、高频复用规范、最近更新规范、缺少 owner 的规范。
## P2 后续增强

- 拓扑图从资源关系升级为专家流、资产流、变更流组合视图。
- 支持组织级趋势图、项目排行、未归档风险排行。
- 支持远程触发、审批放行、状态查询、结果回传围绕 .ai-spec 和 OpenSpec 产物统一展开。
# 四、信息架构与路由设计

```
/workspaces              工作区选择
/w/[slug]                开发者当前专家工作台，默认首页
/w/[slug]/assets         单项目规范资产中心，含 openspec + .ai-spec/history
/w/[slug]/changes        单项目 OpenSpec Change 列表
/w/[slug]/runs           单项目运行历史
/w/[slug]/admin          单项目 OpenSpec 治理详情
/admin                   多项目 OpenSpec 治理总览
/w/[slug]/topology       高级拓扑入口
/w/[slug]/settings       工作区设置
```

底部导航建议：工作台、资产、变更、运行、更多。管理员概览、拓扑、Collector、成员、设置放入“更多”；桌面端可在顶部提供“开发者工作台 / 管理员概览”切换。

# 五、开发者当前专家工作台 PRD

## 页面目标

开发者进入工作区后，不应先选择 Runs / Specs / Topology，而应立即看到当前 run 的当前专家、当前状态、门禁审批、规范资产和下一步动作。

## 5.1 CurrentExpertHero 当前专家大卡

| 字段 | 展示要求 | 优先级 |
| --- | --- | --- |
| expertNameZh | 中文名大字，例如：前端实现专家 | P0 |
| expertCode / expertNameEn | 英文 code 小字，例如：frontend-implementer | P0 |
| flowName | 流程名，例如：PRD 到交付 | P0 |
| stage/status | 运行中、等待审批、阻塞、已完成等 | P0 |
| taskSummary | 当前任务一句话摘要 | P0 |
| gateStatus | none / waiting-approval / approved / rejected / blocked | P0 |
| nextRole | 下一专家中文名 + code | P1 |
| assetSummary | 输入资产、输出资产、待审资产数量 | P0 |

### 按钮区状态机

| 当前状态 | 主按钮 | 次按钮 | 禁止项 |
| --- | --- | --- | --- |
| waiting-approval | 批准通过、驳回修改 | 查看待审资产、要求补充 | 不要只显示“继续执行” |
| blocked | 查看阻塞原因 | 人工介入、查看日志 | 禁止自动进入下一专家 |
| active/running | 继续执行 | 查看规范资产、人工介入 | 若存在前置门禁未通过，禁止执行 |
| done | 查看产物 | 进入下一专家、查看归档 | 不要误导继续当前专家 |
| failed | 查看失败原因 | 重试、人工介入 | 禁止显示成功态资产 |

## 5.2 DynamicExpertFlow 动态专家流

动态专家流必须从 flow 运行实例渲染，而运行实例由 .agents/registry/flows.json 模板、.agents/registry/roles.json 角色注册表、run 状态共同派生。Visual 只展示真实编排，不定义流程规则。

```
type FlowInstance = {
id: string
workspaceId: string
runId: string
flowCode: string
flowName: string
currentRoleCode: string
status: "running" | "waiting-approval" | "blocked" | "success" | "failed"
nodes: FlowNodeInstance[]
}
type FlowNodeInstance = {
id: string
roleCode: string
roleNameZh: string
roleNameEn?: string
required: boolean
optional: boolean
status: "pending" | "active" | "done" | "skipped" | "blocked" | "failed" | "waiting-approval"
openspecActions?: string[]
requiredInputs?: string[]
requiredOutputs?: string[]
inputAssets?: SpecAssetRef[]
outputAssets?: SpecAssetRef[]
gate?: GateApproval
taskSummary?: string
}
```

### 展示规则

- 中文名称为主，英文 code 为辅。节点显示“前端实现专家 / frontend-implementer”。
- required 节点为实线；optional 节点为虚线或浅色；skipped 节点弱化。
- active 或 waiting-approval 节点必须高亮；waiting-approval 节点显示门禁图标。
- 点击节点打开 StageDrawer，不跳转页面。
- 如果 flow 后续新增专家节点，Visual 不改代码也能展示。
## 5.3 StageDrawer 右侧抽屉

右侧抽屉用于展开专家或阶段详情，减少页面跳转。桌面端右侧抽屉宽度建议 420-560px；移动端转为底部抽屉或全屏抽屉。

| Tab | 内容 | 默认条件 |
| --- | --- | --- |
| 概览 | 专家职责、当前任务、输入输出、下一步、风险 | 点击专家节点默认 |
| 规范资产 | 输入资产、输出资产、待审资产、OpenSpec/历史资产 | 点击阶段或资产摘要默认 |
| 门禁审批 | 门禁类型、原因、所需资产、审批记录、批准/驳回/要求补充 | gateStatus=waiting-approval 时默认 |
| 时间线 | run 事件、专家切换、审批记录、归档记录 | 按需 |
| 队列/日志 | 实时队列、执行日志、错误详情、重试记录 | 阻塞或失败时默认 |

# 六、门禁审批功能 PRD 与技术实现

门禁审批不能作为独立角落能力，它是专家工作台 P0 功能。ai-spec-auto 的 /spec-status 用于查看当前阶段、门禁和下一步；默认 /spec-start 使用 auto + none 自动推进，显式切换 main-flow-blocking 时恢复人工审核门禁。因此 Visual 必须把门禁状态放在当前专家大卡和 StageDrawer 的主路径里。

## 6.1 门禁状态模型

```
type GateApproval = {
id: string
workspaceId: string
runId: string
nodeId: string
roleCode: string
gateType: "before-implementation" | "before-archive" | "stage" | "artifact" | "manual"
status: "none" | "waiting-approval" | "approved" | "rejected" | "blocked"
mode: "auto-none" | "main-flow-blocking" | "manual"
reason?: string
requiredAssets?: SpecAssetRef[]
reviewer?: string
comment?: string
createdAt: string
updatedAt: string
approvedAt?: string
rejectedAt?: string
}
```

## 6.2 门禁审批交互

- 当 gate.status = waiting-approval 时，CurrentExpertHero 顶部状态显示“等待门禁审批”。
- 按钮区优先展示：批准通过、驳回修改、查看待审资产；“继续执行”降级或隐藏。
- 批准通过时必须要求确认弹窗，显示将要放行到哪个专家或阶段。
- 驳回修改时必须填写驳回原因，并可选择要求补充的资产。
- 审批动作写入 timeline，并通过 WebSocket 推送到当前工作区订阅者。
- 如果后端暂时没有真实审批 API，先实现 server action/API mock + Prisma 模型，保证 UI 与状态机稳定。
## 6.3 API 设计

```
GET  /api/workspaces/:workspaceId/runs/:runId/gate
POST /api/workspaces/:workspaceId/runs/:runId/gate/:gateId/approve
POST /api/workspaces/:workspaceId/runs/:runId/gate/:gateId/reject
POST /api/workspaces/:workspaceId/runs/:runId/gate/:gateId/request-changes
```

### 请求示例

```
POST /api/workspaces/ws_123/runs/run_456/gate/gate_789/approve
{
"comment": "proposal/design/tasks/checklist 已确认，允许进入归档。",
"approvedBy": "current-user"
}
```

### 响应示例

```
{
"gate": {
"id": "gate_789",
"status": "approved",
"approvedAt": "2026-04-24T10:00:00.000Z"
},
"next": {
"roleCode": "archive-change",
"roleNameZh": "归档专家"
}
}
```

# 七、规范资产模型与识别策略

规范资产是本系统的核心交付物。对于大需求和完整 OpenSpec 流，资产主要来自 openspec/；对于低风险小修、bugfix、轻量运行记录，资产来自 .ai-spec/history/<run-id>/。

```
type SpecAsset = {
id: string
workspaceId: string
runId?: string
changeId?: string
sourceKind: "openspec" | "ai-spec-history"
sourcePath: string
assetType: "proposal" | "spec" | "design" | "tasks" | "checklist" |
"iterations" | "bugfix" | "implementation-notes" | "archive" | "other"
status: "draft" | "active" | "reviewing" | "archived" | "history" | "missing"
title?: string
roleCode?: string
stageCode?: string
updatedAt?: string
}
```

| 来源 | 典型文件 | 用途 | 管理页统计 |
| --- | --- | --- | --- |
| openspec/ | proposal.md、design.md、tasks.md、specs/、archive | 正式 OpenSpec change 与长期规范沉淀 | OpenSpec 正式资产、活跃 Change、已归档 Change |
| .ai-spec/history/<run-id>/ | bugfix.md、implementation-notes.md、checklist.md、iterations.md | 小需求、bug 修复、轻量历史留痕 | 轻量历史任务、快速修复闭环 |

# 八、管理员 OpenSpec 治理驾驶舱 PRD

/admin 是多项目总览，不是单项目页面。领导重点关注 OpenSpec 使用情况、变更、归档、规范资产沉淀，因此第一屏必须围绕 OpenSpec 和归档闭环，而不是拓扑、实时队列或运行日志。

## 8.1 /admin 多项目总览

| 模块 | 指标 | 说明 |
| --- | --- | --- |
| OpenSpec 使用总览 | 活跃项目、活跃 Change、待评审 Change、待归档 Change、已归档 Change、归档成功率、本周新增规范资产、轻量历史任务 | 第一屏 P0 |
| 变更闭环漏斗 | proposal、design、tasks、apply、verify、archive 各阶段数量、阻塞数、平均耗时 | 回答 OpenSpec 是否跑起来 |
| 多项目卡片 | 项目名、当前专家、活跃 Change、待归档、已归档、规范资产数、轻量历史任务数、健康状态、最近更新时间 | 点击进入 /w/[slug]/admin |
| 风险排行 | 未归档最多、待评审最长、失败回环最多、规范资产缺失最多 | P1 |

## 8.2 /w/[slug]/admin 单项目治理详情

- 单项目 OpenSpec 使用情况：活跃 Change、待评审、待归档、已归档、归档成功率。
- 单项目规范资产健康度：规范数、过期规范、未归档变更、最近更新、高频复用。
- 单项目门禁与阻塞：当前等待审批、长期未处理门禁、驳回次数。
- 单项目轻量历史任务：bugfix 数、implementation-notes 数、checklist 完成率。
- 单项目最近运行：run、当前专家、状态、耗时、产物、门禁。
# 九、技术实现方案

## 9.1 数据读取与派生

1. Collector 扫描并上报 .agents/registry/flows.json、.agents/registry/roles.json、openspec/、.ai-spec/history/。
1. 服务端保存 FlowTemplate、RoleRegistry、Run、FlowInstance、SpecAsset、GateApproval、TimelineEvent。
1. 前端 /w/[slug] 请求当前 active run，服务端把 flow 模板 + role 注册表 + run 状态合成为 FlowInstance。
1. DynamicExpertFlow 只消费 FlowInstance，不直接解析 registry 文件。
1. CurrentExpertHero 通过 currentRoleCode 找到 active node，并显示专家中文名、英文 code、门禁状态、任务摘要。
## 9.2 Prisma 模型建议

```
model FlowTemplate {
id          String   @id @default(cuid())
code        String   @unique
name        String
status      String
rawJson     Json
updatedAt   DateTime @updatedAt
}
model RoleRegistry {
id          String   @id @default(cuid())
code        String   @unique
nameZh      String
status      String
rawJson     Json
updatedAt   DateTime @updatedAt
}
model FlowInstance {
id              String   @id @default(cuid())
workspaceId     String
runId           String
flowCode        String
currentRoleCode String?
status          String
nodesJson       Json
createdAt       DateTime @default(now())
updatedAt       DateTime @updatedAt
}
model SpecAsset {
id          String   @id @default(cuid())
workspaceId String
runId       String?
changeId    String?
sourceKind  String
sourcePath  String
assetType   String
status      String
title       String?
roleCode    String?
updatedAt   DateTime @updatedAt
}
model GateApproval {
id          String   @id @default(cuid())
workspaceId String
runId       String
nodeId      String?
roleCode    String?
gateType    String
status      String
mode        String
reason      String?  @db.Text
requiredAssetsJson Json?
reviewer    String?
comment     String?  @db.Text
approvedAt  DateTime?
rejectedAt  DateTime?
createdAt   DateTime @default(now())
updatedAt   DateTime @updatedAt
}
model TimelineEvent {
id          String   @id @default(cuid())
workspaceId String
runId       String?
type        String
title       String
payload     Json?
createdAt   DateTime @default(now())
}
```

## 9.3 前端组件拆分

| 组件 | 职责 | 输入 | 输出/事件 |
| --- | --- | --- | --- |
| CurrentExpertHero | 当前专家主卡、门禁状态、主按钮 | FlowInstance、currentNode、assets、gate | onApprove、onReject、onOpenDrawer、onContinue |
| DynamicExpertFlow | 动态专家流渲染 | FlowInstance.nodes | onNodeClick |
| StageDrawer | 专家/阶段详情抽屉 | selectedNode、assets、gate、timeline | onTabChange、onApprove、onReject |
| GateApprovalPanel | 门禁详情与审批操作 | GateApproval、requiredAssets | approve/reject/requestChanges |
| SpecAssetPanel | 规范资产列表与分组 | SpecAsset[] | onAssetClick |
| AdminGovernanceDashboard | /admin 多项目治理 | GlobalGovernanceSummary | onProjectClick |
| ProjectGovernanceDashboard | /w/[slug]/admin 单项目治理 | ProjectGovernanceSummary | onRunClick/onChangeClick |

## 9.4 API 路由建议

```
GET  /api/workspaces/:workspaceId/dashboard/current
GET  /api/workspaces/:workspaceId/flow/current
GET  /api/workspaces/:workspaceId/assets
GET  /api/workspaces/:workspaceId/runs/:runId/timeline
GET  /api/admin/governance/summary
GET  /api/admin/governance/workspaces
GET  /api/workspaces/:workspaceId/governance
POST /api/workspaces/:workspaceId/runs/:runId/gate/:gateId/approve
POST /api/workspaces/:workspaceId/runs/:runId/gate/:gateId/reject
POST /api/workspaces/:workspaceId/runs/:runId/gate/:gateId/request-changes
```

## 9.5 WebSocket 实时事件

```
type RealtimeEvent =
| { type: "flow.node.updated"; workspaceId: string; runId: string; nodeId: string }
| { type: "gate.waiting"; workspaceId: string; runId: string; gateId: string }
| { type: "gate.approved"; workspaceId: string; runId: string; gateId: string }
| { type: "gate.rejected"; workspaceId: string; runId: string; gateId: string }
| { type: "asset.updated"; workspaceId: string; assetId: string }
| { type: "run.completed"; workspaceId: string; runId: string }
```

# 十、页面验收标准

## 开发者工作台验收

- 进入 /w/[slug] 后第一屏看到 CurrentExpertHero，而不是统计概览。
- 当前专家中文名大字展示，英文 code 小字展示。
- 流程节点来自 flow 数据，不写死；新增 optional role 后无需改 UI 即可显示。
- 当 gate.status=waiting-approval 时，按钮区展示批准/驳回/查看待审资产；不得只显示继续执行。
- 点击任意专家节点打开右侧抽屉，不发生整页跳转。
- 规范资产能同时展示 openspec/ 与 .ai-spec/history/<run-id>/ 来源。
- 审批动作后状态、时间线、按钮区、动态流节点状态同步更新。
## 管理员页验收

- /admin 第一屏展示 OpenSpec 使用总览，而不是普通运行日志。
- 多项目卡片显示当前专家、活跃 Change、待归档、已归档、规范资产、轻量历史、健康状态。
- 点击项目卡片进入 /w/[slug]/admin。
- 单项目页可查看变更、归档、规范资产健康度、门禁与阻塞。
## 技术验收

- npm run typecheck 通过。
- npm run lint 通过。
- npm run test 通过或新增测试可单独运行通过。
- 新增 API 有 Zod 入参校验与错误处理。
- 审批接口必须写 TimelineEvent。
- 不破坏现有 Runs / Changes / Specs / Topology 页面。
# 十一、Codex 执行提示词

把下面提示词直接交给 Codex 执行。

```
你现在负责重构 br-ai-spec-visual。目标是把工作区默认首页改成“开发者当前专家工作台”，并新增门禁审批能力与管理员 OpenSpec 治理驾驶舱。
必须遵守：
1. /w/[slug] 默认进入 CurrentExpertWorkspace，不再默认 overview。
2. 第一视觉是当前专家：中文名大字、英文 code 小字。阶段、任务、flow、run 状态作为小字描述。
3. 流程和专家不能写死，必须读取 .agents/registry/flows.json 与 .agents/registry/roles.json 上报后的数据。
4. flows.json 是流程模板，roles.json 是专家注册表；Visual 只负责展示和派生 FlowInstance，不负责定义流程规则。
5. DynamicExpertFlow 从 FlowInstance.nodes 渲染，支持 required / optional、pending / active / waiting-approval / blocked / done / skipped / failed。
6. 点击专家节点或阶段节点打开右侧 StageDrawer，不跳转页面。
7. StageDrawer tabs: overview / spec-assets / gate-approval / timeline / queue-log.
8. 门禁审批是 P0 功能。若 gate.status=waiting-approval，CurrentExpertHero 按钮区必须优先显示：批准通过、驳回修改、查看待审资产。
9. 审批 API 至少包含 approve、reject、request-changes，审批动作必须写入 TimelineEvent，并推送 WebSocket 事件。
10. 规范资产来源必须支持 openspec/ 与 .ai-spec/history/<run-id>/ 两类。
11. 新增 /admin 多项目 OpenSpec 治理总览，第一屏展示活跃项目、活跃 Change、待评审 Change、待归档 Change、已归档 Change、归档成功率、本周新增规范资产、轻量历史任务。
12. 新增 /w/[slug]/admin 单项目 OpenSpec 治理详情。
13. 保留现有 Runs / Changes / Specs / Topology 页面，不要破坏原路由。
14. 使用 TypeScript、Zod、Prisma、React、Tailwind，风格与现有项目保持一致。
15. 完成后运行 typecheck、lint、test，并说明改动文件与验证结果。
请按顺序完成：
A. 梳理现有路由与组件。
B. 补数据模型和 mock/seed。
C. 实现 /w/[slug] 当前专家工作台。
D. 实现 GateApprovalPanel 与审批 API。
E. 实现 SpecAssetPanel 的双来源资产识别。
F. 实现 /admin 多项目治理总览。
G. 实现 /w/[slug]/admin 单项目治理详情。
H. 补测试与验收。
```

# 十二、实施任务拆分

| 阶段 | 任务 | 产出 |
| --- | --- | --- |
| Step 1 | 检查现有 app/(protected)/w/[slug] 路由、dashboard/runs/specs/topology 组件结构 | 改造影响清单 |
| Step 2 | 新增 FlowInstance、SpecAsset、GateApproval、TimelineEvent 数据模型或 mock 数据层 | 类型定义 + Prisma migration/seed |
| Step 3 | 实现 CurrentExpertHero、DynamicExpertFlow、StageDrawer、GateApprovalPanel、SpecAssetPanel | 组件与单元测试 |
| Step 4 | 把 /w/[slug] 默认渲染为 CurrentExpertWorkspace | 开发者首页改造 |
| Step 5 | 实现门禁审批 API 与 UI 状态联动 | approve/reject/request-changes 可用 |
| Step 6 | 实现 /admin 多项目治理总览 | GlobalGovernanceDashboard |
| Step 7 | 实现 /w/[slug]/admin 单项目治理详情 | ProjectGovernanceDashboard |
| Step 8 | 跑 typecheck/lint/test，修复回归 | 验收报告 |

# 十三、风险与约束

- 不要把流程写死成“规范、计划、运行、评审、归档”；这些只能作为展示分组，不能作为数据源。
- 不要把管理员概览和开发者工作台混在同一首页，否则继续造成层级混乱。
- 不要把工作区运行时间线、实时队列、拓扑放到一级主视觉；它们是抽屉 tab 或更多入口。
- 门禁审批不是仅在详情页展示，必须在 CurrentExpertHero 主按钮区体现。
- OpenSpec 使用情况是管理员页 P0，规范内容健康度是 P1，两者都要有，但前者更靠前。
# 十四、参考资料

- br-ai-spec README: https://raw.githubusercontent.com/Colouful/br-ai-spec/main/README.md
- br-ai-spec-visual README: https://raw.githubusercontent.com/Colouful/br-ai-spec-visual/main/README.md
- flows.json: https://raw.githubusercontent.com/Colouful/br-ai-spec/main/.agents/registry/flows.json
- roles.json: https://raw.githubusercontent.com/Colouful/br-ai-spec/main/.agents/registry/roles.json