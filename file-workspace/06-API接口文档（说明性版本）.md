# API 接口文档（说明性版本）

## 1. 文档说明
本接口文档用于说明首版首页和核心展示页需要具备哪些 API 能力，不作为最终研发级接口协议文档，但可作为接口设计基线。

## 2. 接口分组

### 2.1 Dashboard 组
- `GET /api/dashboard/summary`
- `GET /api/dashboard/onboarding`
- `GET /api/dashboard/runtime-health`
- `GET /api/dashboard/delivery-progress`
- `GET /api/dashboard/efficiency`
- `GET /api/dashboard/block-flow`
- `GET /api/dashboard/asset-coverage`
- `GET /api/dashboard/installation-trend`
- `GET /api/dashboard/pilot-projects`
- `GET /api/dashboard/pilot-review`

### 2.2 Runs / Changes 组
- `GET /api/runs/recent`
- `GET /api/changes/recent`

## 3. 接口通用规范

### 3.1 请求方式
- 查询接口统一使用 GET
- 参数统一通过 query 或 path 传递

### 3.2 通用成功响应
```json
{
  "code": 0,
  "message": "成功",
  "data": {}
}
```

### 3.3 通用错误响应
```json
{
  "code": 1001,
  "message": "错误信息",
  "data": null,
  "requestId": "req_xxx"
}
```

## 4. 核心接口说明

### 4.1 首页摘要
- 路径：`GET /api/dashboard/summary`
- 说明：提供首页首屏通用摘要
- 核心字段：Workspace、Onboarding 阶段、运行数、归档数、收益摘要

### 4.2 Onboarding 报告
- 路径：`GET /api/dashboard/onboarding`
- 说明：提供接入状态、资产检测、下一步建议
- 核心字段：stage、assetChecklist、nextActions、missingAssets

### 4.3 运行态健康度
- 路径：`GET /api/dashboard/runtime-health`
- 说明：提供运行中需求数、异常数、趋势图数据

### 4.4 交付闭环进度
- 路径：`GET /api/dashboard/delivery-progress`
- 说明：提供发起数、归档数、闭环率等

### 4.5 效率收益
- 路径：`GET /api/dashboard/efficiency`
- 说明：提供平均耗时、节省区间、归档资产数

### 4.6 阻塞变化流
- 路径：`GET /api/dashboard/block-flow`
- 说明：提供阻塞阶段分布和原因排行

### 4.7 规范资产命中情况
- 路径：`GET /api/dashboard/asset-coverage`
- 说明：提供 assets 状态和覆盖评分

### 4.8 最近 Runs
- 路径：`GET /api/runs/recent`
- 说明：提供首页最近需求列表

### 4.9 最近 Changes / Specs
- 路径：`GET /api/changes/recent`
- 说明：提供最近变更与规格记录

### 4.10 安装与接入趋势
- 路径：`GET /api/dashboard/installation-trend`
- 说明：提供安装人数、接入项目数与趋势图

### 4.11 试点项目专区
- 路径：`GET /api/dashboard/pilot-projects`
- 说明：提供试点项目列表与状态摘要

### 4.12 试点复盘
- 路径：`GET /api/dashboard/pilot-review`
- 说明：提供试点摘要、当前问题与下一步建议

## 5. 错误码说明

| 错误码 | 含义 |
|---|---|
| 1001 | Workspace 不存在或无权限 |
| 1002 | Workspace 尚未接入 |
| 1003 | Collector 数据未准备完成 |
| 1004 | 统计数据暂不可用 |
| 1005 | 请求参数错误 |

## 6. 首页关键接口字段建议

### 6.1 `/api/dashboard/summary`
建议字段：
- workspaceId
- workspaceName
- hasDemoData
- onboardingStage
- runningCount
- abnormalCount
- activeProjectCount
- startedToday
- archivedToday
- weeklyCloseRate
- avgPageDuration
- savedDurationRange

### 6.2 `/api/dashboard/onboarding`
建议字段：
- stage
- assetChecklist
- missingAssets
- nextActions
- quickLinks
- detectErrorMessage

### 6.3 `/api/dashboard/runtime-health`
建议字段：
- runningCount
- abnormalCount
- activeProjectCount
- lastSyncTime
- trendData

### 6.4 `/api/dashboard/delivery-progress`
建议字段：
- startedToday
- archivedToday
- weeklyCloseRate
- firstArchiveCount
- pilotDoneCount
- compareLastWeek

### 6.5 `/api/dashboard/efficiency`
建议字段：
- avgPageDuration
- avgPilotDuration
- savedDurationRange
- archivedAssetCount
- reusedTemplateCount
- estimationType