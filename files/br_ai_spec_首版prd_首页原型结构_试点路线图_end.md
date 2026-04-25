# 《BR AI Spec 首版 PRD + 首页原型结构 + 试点路线图》

## 1. 文档基本信息

- 项目名称：BR AI Spec
- 子产品：BR AI Spec Base / BR AI Spec Visual
- 文档版本：V1.0
- 产品阶段：内部试点版 / Demo-first，Team-ready
- 目标团队：前端开发团队、平台管理员
- 核心场景：规范驱动 AI 开发、OpenSpec 交付、组件替换类需求试点

---

## 2. 产品定义

### 2.1 一句话定义

BR AI Spec 是一套把 AI 研发从“个人对话式助手”升级为“规范驱动、可归档、可观测、可治理交付系统”的底座与控制面。

### 2.2 产品分层

#### BR AI Spec Base

面向业务项目的规范与运行时底座，负责：

- 项目规则注入
- 技能与流程注入
- IDE 命令接入
- OpenSpec 流程落地
- `.ai-spec` 运行态沉淀
- 轻量修正 / 完整交付链分流

#### BR AI Spec Visual

面向团队的可视化与控制面，负责：

- Workspace 管理
- 项目接入与状态汇总
- Runs / Changes / Specs / Topology 可视化
- Collector 数据上报
- 运行态实时更新
- 安装遥测与试点效果统计
- 后续可扩展的控制与治理能力

### 2.3 首版定位

首版不是做“功能大全”，而是优先证明：

1. 开发者可以低成本接入
2. 可以真实跑通一个规范驱动需求并归档
3. Visual 能让团队看见交付过程与结果
4. 规范可以显著提升 AI 代码被接受的概率

---

## 3. 背景与问题

### 3.1 当前团队痛点

当前团队在引入 AI 编码后，核心问题并不是 AI 不会写代码，而是：

1. 需求未收敛时 AI 已开始改代码，返工成本高
2. 规则、目录、接口、路由、样式、测试等约定分散，AI 输出不稳定
3. 过程只存在于聊天记录中，缺少可追溯、可归档资产
4. 开发者不知道什么时候该走完整链，什么时候该走轻量链
5. 接入后是否有价值、值不值得继续使用，缺少清晰证据

### 3.2 当前试点业务场景

- 公司业务中台项目
- 典型需求：新组件替换、页面局部重构、规范驱动交付
- 当前现状：即使使用 AI IDE，不使用统一规范时，一个页面平均仍需 0.5 ～ 1 天
- 目标：将单页面平均交付时长缩小到 0.2 ～ 0.5 天

### 3.3 首版要解决的问题

首版重点不是覆盖全部管理能力，而是回答四个问题：

1. 开发者如何快速上手
2. 一次真实需求如何走完整闭环
3. Visual 首页如何直接体现价值
4. 如何用数据证明“规范驱动 AI 开发”是有价值的

---

## 4. 产品目标

### 4.1 业务目标

1. 在前端团队内完成首批试点接入
2. 用组件替换类真实需求跑通规范驱动交付闭环
3. 建立可观测数据面板，形成内部推广依据
4. 为后续 Team 模式打下结构化基础

### 4.2 用户目标

#### 对开发者

- 上手简单
- 命令清晰
- 知道先做什么、后做什么
- 真能减少交付时间
- 留下可归档资产

#### 对平台管理员

- 知道谁在用
- 哪些项目已接入
- 哪些需求在跑
- 哪些需求归档完成
- 哪些环节常卡住

### 4.3 首版成功标准

满足以下任意四项即可视为首版成功：

- 有真实开发者完成接入并持续使用
- 有真实需求完成从发起到归档闭环
- 首页可清晰看到运行态、阻塞点、闭环结果
- 组件替换类需求平均时长下降明显
- 开发者反馈“比直接裸用 AI IDE 更清晰、更稳”

---

## 5. 目标用户与角色

### 5.1 核心用户

#### 开发者

核心诉求：

- 快速接入
- 快速开始一个需求
- 明确当前阶段与下一步
- 保证产出更容易被接受

#### 平台管理员

核心诉求：

- 了解接入情况
- 观测多个项目运行状态
- 看到归档、阻塞、效率等数据
- 为后续治理提供抓手

### 5.2 非首版核心用户

- 研发管理者
- TL / 架构师
- 跨团队治理负责人

首版兼顾但不作为首页唯一设计中心。

---

## 6. 产品原则

1. **Demo-first**：先保证个人开发者能快速看到结果
2. **Team-ready**：数据模型、字段、权限、埋点为团队扩展预留能力
3. **规范优先**：不是放大 AI 单轮生成，而是提升交付接受度与归档质量
4. **过程可追踪**：每次开发都要能看见过程和产物
5. **结果可证明**：必须有数据证明这套体系值不值得推广
6. **信息分层**：能力可以全，首页必须收敛

---

## 7. 首版范围

## 7.1 In Scope

### Base 侧

- 项目初始化
- 规范注入
- 技能与流程注入
- OpenSpec 目录与产物接入
- `.ai-spec` 运行态接入
- 完整需求流与轻量修正流支持
- 常用命令与最小开始路径

### Visual 侧

- Workspace 管理（最小可用）
- 项目接入引导
- Collector 上报
- 首页驾驶舱
- Runs / Changes 基础列表
- 归档状态统计
- 安装 / 使用 / 归档等首版指标面板
- 新手 onboarding 报告
- Demo Workspace

### 试点能力

- 组件替换场景模板
- 试点项目接入与复盘模板
- 首版指标追踪

## 7.2 Out of Scope

首版不重点做：

- 复杂审批流
- 强控制台指令编排
- 跨团队细粒度权限策略
- 企业级审计中心
- 多环境复杂部署控制台
- 全自动 AI 接受率判定

---

## 8. 核心能力设计

## 8.1 开发者首条成功路径

目标：让开发者在最短时间内完成“接入 → 发起需求 → 跑完 → 归档 → 在首页看到结果”。

### 路径设计

1. 进入“开发者快速开始”入口
2. 选择 Demo 模式 / 已有项目接入
3. 完成 Base 初始化
4. 执行最小命令开始真实需求
5. 用 Collector 把状态同步到 Visual
6. 在首页看到：
   - 运行态
   - 当前阻塞点
   - 已归档数量
   - 下一步推荐

### 要求

- 页面必须显式告诉用户下一步做什么
- 不允许用户阅读大量文档后仍不知道如何开始
- 必须给出最短命令链路

---

## 8.2 变更分流决策器

这是首版差异化亮点之一。

### 能力目标

让开发者不需要先读懂所有流程，就能知道这次改动应该走哪条链。

### 输入

- 是否是全新需求
- 是否新增路由 / 接口 / store / 模块
- 是否只是样式 / 文案 / 轻微局部调整
- 当前是否存在 active run
- 是否已有 open change
- 是否已经归档

### 输出

- 推荐流转路径
- 推荐命令
- 为什么推荐该路径

### 首版支持的推荐结果

- `prd-to-delivery`
- `bugfix-to-verification`
- `quick-fix`
- `patch`
- `scope-delta`
- `archive-fix`
- `followup-patch`
- `full-change`

### 交互形式

- 首页快捷入口
- Runs 页右上角入口
- 新建需求弹层入口

---

## 8.3 首页 onboarding 报告

### 设计目标

解决开发者三个最大困惑：

1. 文档从哪看
2. 命令怎么用
3. 接入后到底有没有价值

### 首页第一卡片展示内容

- 当前接入状态：未接入 / 已接入 / 已联通 Visual / 已跑通需求 / 已归档
- 已检测资产：规则 / 技能 / OpenSpec / `.ai-spec` / registry / logs
- 下一步推荐动作
- 新手建议入口
- Demo Workspace 入口

---

## 8.4 组件替换试点模板

### 适用场景

- 新组件替换老组件
- 页面局部重构
- 样式 / 交互标准化迁移
- 具备一定复用性的中台需求

### 模板结构

- 需求背景
- 替换范围
- 影响页面
- 涉及模块
- 风险级别
- 是否需要 OpenSpec 完整链
- 归档要求
- 回归建议

### 模板价值

- 降低开发者试点理解成本
- 形成组织可复制模板
- 为后续推广准备标准案例

---

## 9. 首页原型结构

## 9.1 首页定位

首页不是系统结构索引页，而是：

**规范驱动 AI 开发的交付驾驶舱首页**

定位上采用：

- 观测清晰度参考 Grafana
- 行动引导参考 cockpit

---

## 9.2 首页信息架构

### 顶部区域

#### A. 顶部导航

- Logo / 产品名
- 当前 Workspace 切换
- 搜索
- 快速新建 / 快捷操作
- 用户信息

#### B. 首页标题区

- 标题：交付驾驶舱
- 副标题：查看当前规范驱动 AI 开发的运行态、阻塞点与结果
- 操作：
  - 新建需求
  - 变更分流决策
  - 打开 Demo Workspace

---

### 第一屏核心模块

#### 模块 1：Onboarding 报告（首屏最高优先级）

展示：

- 当前项目 / Workspace 接入状态
- 已检测资产清单
- 下一步建议
- 快速开始入口
- 常见问题入口

#### 模块 2：运行态健康度

展示：

- 今日运行中的 Run 数
- 异常 / 中断 Run 数
- 最近一次上报时间
- 活跃项目数
- 健康趋势

#### 模块 3：阻塞变化流

展示：

- 当前卡住的需求数
- 卡在哪个阶段
- 阻塞原因 Top N
- 可点击进入详情

#### 模块 4：交付闭环进度

展示：

- 今日发起需求数
- 今日归档数
- 本周闭环率
- 组件替换试点完成数

#### 模块 5：效率收益卡

展示：

- 单页面平均交付耗时
- 组件替换类需求平均耗时
- 相比传统 AI IDE 的节省区间
- 规范驱动后收益概览

#### 模块 6：规范资产命中情况

展示：

- 规则是否命中
- OpenSpec 是否存在
- `.ai-spec` 是否完整
- 日志 / registry 是否同步
- 资产完整度评分

---

### 第二屏扩展模块

#### 模块 7：最近 Runs

- Run 名称
- 项目
- 当前阶段
- 当前角色
- 更新时间
- 状态标签

#### 模块 8：最近 Changes / Specs

- 变更名称
- 所属项目
- 是否归档
- 最后更新时间

#### 模块 9：安装与接入趋势

- 安装人数
- 接入项目数
- Collector 联通数量
- 最近 7 天接入趋势

#### 模块 10：试点项目专区

- 组件替换项目列表
- 当前状态
- 归档完成率
- 试点反馈入口

---

## 9.3 首页原型草图（文本版）

```text
┌──────────────────────────────────────────────────────────────┐
│ Logo   Workspace切换   搜索   新建需求   分流决策   用户信息 │
├──────────────────────────────────────────────────────────────┤
│ 交付驾驶舱                                                     │
│ 查看当前规范驱动 AI 开发的运行态、阻塞点与结果                │
│ [开始一个需求] [打开Demo Workspace] [查看接入引导]             │
├──────────────────────────────────────────────────────────────┤
│ Onboarding 报告                                                │
│ 已接入 Base / 已联通 Visual / 已检测 OpenSpec / 下一步建议     │
├──────────────────────────────────────────────────────────────┤
│ 运行态健康度        │ 阻塞变化流          │ 交付闭环进度        │
│ 运行中 / 异常 / 趋势│ 卡点 / 原因 / Top N │ 发起 / 归档 / 闭环率│
├──────────────────────────────────────────────────────────────┤
│ 效率收益卡          │ 规范资产命中情况                           │
│ 时长下降 / 收益区间 │ rules / skills / .ai-spec / openspec       │
├──────────────────────────────────────────────────────────────┤
│ 最近 Runs                                                    │
├──────────────────────────────────────────────────────────────┤
│ 最近 Changes / Specs     │ 安装与接入趋势   │ 试点项目专区       │
└──────────────────────────────────────────────────────────────┘
```

---

## 10. 页面清单

### 10.1 首页 / Dashboard

首版重点页面

### 10.2 Runs

展示：

- 运行列表
- 当前阶段
- 当前角色
- 最近更新时间
- 异常状态
- 快速进入详情

### 10.3 Changes

展示：

- Change 列表
- 所属项目
- 是否归档
- 当前状态
- 最后更新时间

### 10.4 Specs / Topology

展示规范资产、仓库关系与角色拓扑 首版可保持中等优先级

### 10.5 Workspace 管理

面向平台管理员

- Workspace 基础信息
- 接入项目
- 连接令牌
- 成员与权限

### 10.6 Demo Workspace

- 内置示例数据
- 首页关键模块都可演示
- 用于新用户理解平台

---

## 11. 指标体系设计

## 11.1 一级指标：接入层

- 安装人数
- 接入项目数
- 活跃 Workspace 数
- Collector 联通成功率
- 首次接入完成率

## 11.2 一级指标：运行层

- 发起需求数
- 运行中需求数
- 归档数
- 闭环率
- 平均阻塞数
- 阻塞原因 Top N

## 11.3 一级指标：结果层

- 单页面平均交付耗时
- 组件替换类需求平均耗时
- AI 产出进入可接受状态的比例
- 可归档资产生成率
- 规范资产复用次数

## 11.4 首版优先采集字段

- user\_id / workspace\_id / project\_id
- install\_time / first\_run\_time / first\_archive\_time
- run\_id / change\_id / status / phase / role
- block\_reason / archive\_result
- route\_decision / selected\_flow
- page\_count / component\_scope / business\_type
- estimated\_duration / actual\_duration

---

## 12. 试点路线图

## 12.1 试点目标

在前端团队中，围绕组件替换类需求，证明：

- 规范驱动 AI 开发可以真实降低交付成本
- 可以把开发过程沉淀为可追溯、可归档资产
- Visual 可以为开发者与平台管理员提供清晰价值

---

## 12.2 试点阶段划分

### 阶段一：接入验证（第 1 阶段）

目标：先跑通技术链路

交付项：

- Base 初始化成功
- Visual 启动成功
- Collector 联通成功
- 首页能看到接入结果

验收标准：

- 至少 1 个项目完成接入
- 至少 1 个 Workspace 可正常上报
- 首页 onboarding 报告正确显示

### 阶段二：真实需求闭环（第 2 阶段）

目标：跑通一个真实组件替换需求

交付项：

- 发起需求
- 执行交付链
- 生成规范资产
- 完成归档
- 首页出现完整闭环数据

验收标准：

- 至少 1 个真实需求完成归档
- Runs / Changes / 首页统计同步正常

### 阶段三：试点扩展（第 3 阶段）

目标：扩大到多位开发者 / 多个页面

交付项：

- 多开发者接入
- 组件替换模板稳定复用
- 指标面板可用于复盘

验收标准：

- 有持续使用者
- 有重复使用场景
- 有试点反馈沉淀

### 阶段四：Team 化准备（第 4 阶段）

目标：保持 Demo-first 体验的同时，完善 Team-ready 能力

交付项：

- Workspace 管理增强
- 权限模型补全
- 接入趋势与归档趋势数据完善
- 控制与治理能力的接口预留

---

## 12.3 试点里程碑建议

### M1：能接入

- 完成 Demo 路径
- 完成 onboarding 报告
- 完成 Demo Workspace

### M2：能闭环

- 跑通首个组件替换需求
- 首页可看见完整闭环
- 有基础数据统计

### M3：能复盘

- 有接入数据
- 有归档数据
- 有阻塞点分析
- 有试点总结

### M4：能推广

- 有场景模板
- 有文档体系
- 有平台演示能力
- 有内部推广话术

---

## 13. 文档重构建议

首版文档建议重构为以下 5 条入口：

### 1）开发者：10 分钟跑通 Demo

适合第一次接触用户

### 2）开发者：组件替换真实场景教程

直接围绕试点场景

### 3）平台管理员：30 分钟接起 Team 环境

面向接入与管理者

### 4）命令与流程速查

把高频命令与流程集中到一页

### 5）FAQ

重点回答：

- 为什么不直接只用 OpenSpec
- 为什么要规范驱动
- 什么场景走完整链，什么场景走轻量链
- 接入后价值怎么证明

---

## 14. 产品优先级

## P0

- 首页驾驶舱
- Onboarding 报告
- 开发者快速开始路径
- 变更分流决策器
- Demo Workspace
- 组件替换试点模板

## P1

- Runs / Changes 详情完善
- 试点指标面板
- 安装与归档趋势
- 规范资产完整度评分

## P2

- 更强控制能力
- 更强治理能力
- 更强权限与审计
- 跨团队视图

---

## 15. 风险与应对

### 风险 1：理解成本高

应对：

- 首页 onboarding
- Demo Workspace
- 文档入口重构
- 分流决策器替代纯文档理解

### 风险 2：接入麻烦

应对：

- 压缩最小路径
- 提供开发者一键式 Demo 教程
- 首页显式展示接入进度

### 风险 3：首页价值弱

应对：

- 首页围绕“运行态 / 阻塞 / 闭环 / 收益”设计
- 不按系统结构堆模块

### 风险 4：AI 接受率收益难证明

应对：

- 先定义字段与指标
- 用组件替换场景沉淀首批样板数据

---

## 16. 最终结论

BR AI Spec 首版不应追求“平台能力铺满”，而应优先证明：

1. 规范驱动 AI 开发确实能提升代码接受度
2. 开发过程可以被沉淀为可追溯、可归档资产
3. Visual 能把接入、运行、阻塞、闭环与收益清晰展示出来
4. 前端团队愿意持续使用这套系统

首版的核心成功，不是页面多，而是：

**开发者真的愿意装、真的能跑通、真的能归档、团队真的能看见价值。**

---

## 17. 首页高保真信息架构稿

## 17.1 设计目标

首页需要同时满足两类核心角色：

- 开发者：我现在该做什么、我做的需求走到哪了、有没有价值
- 平台管理员：谁在用、哪些项目在跑、哪里卡住了、整体效果如何

因此首页设计遵循以下原则：

1. 第一屏先回答“是否接入成功、现在是否在产生价值”
2. 第二层再展开“当前运行态与阻塞态”
3. 第三层再展示“趋势、试点与扩展模块”
4. 信息按“动作优先”而不是“系统结构优先”组织

---

## 17.2 首页整体布局（桌面端）

### 顶部导航区（固定）

从左到右：

- Logo + 产品名称
- Workspace 切换器
- 全局搜索
- 快捷操作区
  - 新建需求
  - 分流决策
  - 接入项目
- 通知入口
- 用户信息 / 设置

### 页面标题区

- 主标题：交付驾驶舱
- 副标题：查看规范驱动 AI 开发的接入状态、运行态、阻塞点与交付结果
- 辅助说明：默认展示当前 Workspace 的整体情况
- 页面级操作：
  - 打开 Demo Workspace
  - 查看快速开始
  - 查看命令速查

### 第一屏核心区

采用 **2 + 3 模块混排**：

- 左侧大卡：Onboarding 报告
- 右侧上方两张摘要卡：运行态健康度 / 交付闭环进度
- 右侧下方一张摘要卡：效率收益卡

### 第二屏观测区

采用 **2 列布局**：

- 左侧：阻塞变化流
- 右侧：规范资产命中情况

### 第三屏业务区

采用 **1 + 2 布局**：

- 最近 Runs（通栏）
- 最近 Changes / Specs
- 安装与接入趋势

### 第四屏试点区

采用 **1 + 1 布局**：

- 试点项目专区
- 试点复盘与建议动作区

---

## 17.3 页面模块层级

### L1：必须优先展示

1. Onboarding 报告
2. 运行态健康度
3. 交付闭环进度
4. 效率收益卡

### L2：体现平台价值

5. 阻塞变化流
6. 规范资产命中情况
7. 最近 Runs

### L3：体现可推广能力

8. 最近 Changes / Specs
9. 安装与接入趋势
10. 试点项目专区

---

## 17.4 首页模块详细结构

### 模块 A：Onboarding 报告

#### 模块目标

解决首次接入用户“不知道从哪里开始、不知道接入是否成功、不知道下一步做什么”的问题。

#### 展示内容

- 当前状态阶段：
  - 未接入
  - 已安装 Base
  - 已联通 Visual
  - 已启动首个需求
  - 已完成首个归档
- 资产检测结果：
  - rules
  - skills
  - OpenSpec
  - `.ai-spec`
  - registry
  - logs
- 下一步建议动作
- 快速入口：
  - 开始一个需求
  - 进入 Demo Workspace
  - 查看 10 分钟快速开始
  - 查看命令速查

#### 交互要求

- 支持根据当前接入状态动态变化
- 支持点击后跳转到对应引导或页面
- 若检测缺失资产，需给出明确提示与修复入口

---

### 模块 B：运行态健康度

#### 模块目标

快速让用户知道当前系统是不是在“正常跑”。

#### 展示内容

- 运行中的需求数
- 异常 / 中断需求数
- 活跃项目数
- 最近一次上报时间
- 7 日运行趋势

#### 支持视图

- 卡片摘要
- 迷你趋势图
- 点击进入 Runs 页面

---

### 模块 C：交付闭环进度

#### 模块目标

体现规范驱动开发是否真正产生“从发起到归档”的结果。

#### 展示内容

- 今日发起需求数
- 今日归档数
- 本周闭环率
- 首次归档完成数
- 组件替换试点已完成数

#### 支持视图

- 摘要数字
- 环比箭头
- 小型环图 / 进度条

---

### 模块 D：效率收益卡

#### 模块目标

体现这套系统值不值得继续使用。

#### 展示内容

- 单页面平均交付时长
- 组件替换场景平均时长
- 较基线节省时长区间
- 已沉淀归档资产数
- 已复用模板次数（有则展示）

#### 说明

首版可先采用“估算 + 实际记录结合”的方式，不要求全部自动化。

---

### 模块 E：阻塞变化流

#### 模块目标

让用户看到当前需求为什么没有继续往前推进。

#### 展示内容

- 当前阻塞需求总数
- 阻塞阶段分布：
  - before-implementation
  - before-guardian
  - before-archive
- 阻塞原因 Top N
- 最近 24 小时新增阻塞数
- 可点击进入阻塞详情

#### 推荐交互

- 阶段切换 Tab
- 原因分布条形图
- 阻塞列表快捷入口

---

### 模块 F：规范资产命中情况

#### 模块目标

让用户知道项目是否真的完成规范接入，而不是只装了一个壳。

#### 展示内容

- 规则资产完整度
- OpenSpec 检测结果
- `.ai-spec` 完整度
- logs / registry 同步状态
- 资产完整度评分

#### 推荐交互

- 采用清单式展示
- 支持查看缺失原因
- 支持一键查看修复指引

---

### 模块 G：最近 Runs

#### 展示字段

- 需求名称
- 所属项目
- 当前阶段
- 当前角色
- 更新时间
- 状态标签
- 是否阻塞

#### 支持操作

- 查看详情
- 继续推进
- 查看规范资产

---

### 模块 H：最近 Changes / Specs

#### 展示字段

- Change / Spec 名称
- 所属项目
- 当前状态
- 是否归档
- 最后更新时间

#### 支持操作

- 查看详情
- 打开归档内容
- 查看关联 Run

---

### 模块 I：安装与接入趋势

#### 展示内容

- 安装人数
- 接入项目数
- Workspace 数
- Collector 联通数
- 最近 7 / 30 天趋势

#### 价值说明

主要面向平台管理员和试点复盘使用。

---

### 模块 J：试点项目专区

#### 展示内容

- 当前试点项目列表
- 各项目当前状态
- 已归档需求数
- 当前阻塞数
- 负责人
- 最近反馈

#### 价值说明

方便内部汇报与样板复制。

---

## 17.5 页面状态设计

### 空状态

适用于：

- 尚未接入
- 尚未产生 Run
- 尚未有归档
- 尚未开启试点

设计要求：

- 不能只显示“暂无数据”
- 必须同时给出原因说明 + 下一步动作

### 加载状态

- 首页骨架屏
- 核心卡片优先加载
- 趋势图与列表可后置加载

### 异常状态

- Collector 断连
- Workspace 无权限
- 数据源未就绪
- 接入检测失败

设计要求：

- 必须显示错误原因
- 必须给出修复建议或跳转路径

---

## 17.6 首页响应式建议

### 大屏桌面端

- 采用完整 12 栅格布局
- 保持第一屏关键模块全部可见

### 普通笔记本

- 第一屏优先展示 Onboarding + 三张核心摘要卡
- 列表模块放到第二屏

### 平板端

- 缩减趋势图细节
- 优先保留卡片摘要

### 首版建议

首版以桌面 Web 为主，不优先投入移动端单独优化。

---

## 18. 模块文案

## 18.1 页面级文案

### 首页主标题

交付驾驶舱

### 首页副标题

查看规范驱动 AI 开发的接入状态、运行态、阻塞点与交付结果。

### 页面说明

从这里快速判断当前是否接入成功、需求是否在正常推进，以及这套体系是否正在产生价值。

---

## 18.2 顶部按钮文案

### 新建需求

按钮文案：开始一个需求 说明文案：发起一次新的规范驱动开发流程。

### 分流决策

按钮文案：判断本次改动走哪条链 说明文案：根据改动范围与当前状态，推荐最合适的流转路径。

### 接入项目

按钮文案：接入当前项目 说明文案：将项目接入 BR AI Spec Base 与 Visual。

### Demo Workspace

按钮文案：打开 Demo Workspace 说明文案：查看示例数据与标准页面结构。

### 快速开始

按钮文案：查看 10 分钟快速开始 说明文案：适合第一次接入的开发者。

---

## 18.3 模块标题与副标题文案

### Onboarding 报告

标题：接入与上手报告 副标题：确认当前接入状态，并按建议完成下一步。

### 运行态健康度

标题：运行态健康度 副标题：查看当前需求是否在正常推进。

### 交付闭环进度

标题：交付闭环进度 副标题：统计需求从发起到归档的完成情况。

### 效率收益卡

标题：效率收益 副标题：衡量这套体系是否真正节省了交付成本。

### 阻塞变化流

标题：阻塞变化流 副标题：查看需求卡在哪个阶段，以及为什么卡住。

### 规范资产命中情况

标题：规范资产命中情况 副标题：确认项目是否完整接入了规则、运行态与交付资产。

### 最近 Runs

标题：最近运行中的需求 副标题：快速查看最近活跃需求与当前状态。

### 最近 Changes / Specs

标题：最近变更与规格 副标题：查看最近生成、更新或归档的交付资产。

### 安装与接入趋势

标题：安装与接入趋势 副标题：查看接入规模与使用趋势。

### 试点项目专区

标题：试点项目专区 副标题：集中查看当前样板项目的推进情况。

---

## 18.4 空状态文案

### 首页未接入

标题：当前还没有接入项目 说明：先完成项目接入，才可以查看运行态、归档结果与效率数据。 按钮：立即接入项目

### 尚未启动需求

标题：当前还没有运行中的需求 说明：你可以直接开始一个真实需求，跑通从发起到归档的完整闭环。 按钮：开始一个需求

### 尚未归档

标题：还没有归档记录 说明：当首个需求完成归档后，这里会显示闭环进度与归档结果。 按钮：查看如何完成归档

### 尚无趋势数据

标题：趋势数据正在积累中 说明：当接入、运行与归档数据达到一定数量后，这里会显示趋势变化。 按钮：查看接入建议

### Demo Workspace 空态

标题：示例工作区尚未初始化 说明：初始化后可快速查看标准页面结构与示例数据。 按钮：初始化 Demo Workspace

---

## 18.5 异常状态文案

### Collector 断连

标题：Collector 暂未联通 说明：当前无法同步最新运行态与规范资产，请先检查服务地址、连接令牌与本地环境。 按钮：查看排查指引

### 资产检测失败

标题：规范资产检测失败 说明：系统未能完整检测到规则、OpenSpec 或运行态目录，请按指引修复后重试。 按钮：查看修复建议

### 权限不足

标题：当前无访问权限 说明：你暂时无法查看该 Workspace 的详细数据，请联系管理员开通权限。 按钮：返回工作区列表

### 数据源未就绪

标题：数据源尚未准备完成 说明：请先完成数据库初始化、Collector 接入或 Demo 数据加载。 按钮：查看初始化步骤

---

## 18.6 提示性文案

### Onboarding 完成提示

你已完成基础接入，下一步建议直接跑通一个真实需求并完成归档。

### 首个需求完成提示

恭喜，首个需求已进入闭环流程。继续推进归档后，即可看到完整结果数据。

### 首次归档完成提示

恭喜，首个规范驱动需求已完成归档。现在可以开始观察效率收益与复用价值。

### 分流决策提示

系统会根据改动范围、当前状态与风险等级，推荐本次变更应走的链路。

---

## 19. 关键埋点字段表

## 19.1 设计原则

1. 首版以“证明价值”为目标，不追求字段无限细化
2. 字段命名应兼容后续 Team 模式
3. 事件需覆盖：接入、运行、阻塞、归档、复用、收益
4. 页面埋点与业务埋点分层设计

---

## 19.2 埋点分层

### A. 用户与环境维度

用于标识是谁、在哪个工作区、对哪个项目进行操作。

### B. 接入与安装维度

用于统计安装、接入、初始化、联通情况。

### C. 运行态维度

用于统计需求发起、运行中、阻塞、完成、归档等状态。

### D. 规范资产维度

用于统计规则、OpenSpec、`.ai-spec`、registry、logs 等命中情况。

### E. 效果评估维度

用于统计交付耗时、闭环率、复用率、收益情况。

---

## 19.3 公共字段

| 字段名             | 类型       | 必填 | 说明                            |
| --------------- | -------- | -- | ----------------------------- |
| event\_name     | string   | 是  | 事件名称                          |
| event\_time     | datetime | 是  | 事件发生时间                        |
| user\_id        | string   | 否  | 用户唯一标识                        |
| user\_role      | string   | 否  | 用户角色，如 developer / admin      |
| workspace\_id   | string   | 否  | 工作区 ID                        |
| workspace\_name | string   | 否  | 工作区名称                         |
| project\_id     | string   | 否  | 项目 ID                         |
| project\_name   | string   | 否  | 项目名称                          |
| source\_page    | string   | 否  | 来源页面                          |
| source\_module  | string   | 否  | 来源模块                          |
| client\_type    | string   | 否  | 客户端类型，如 web / cli / collector |
| env             | string   | 否  | 环境标识，如 dev / test / prod      |
| platform        | string   | 否  | 操作系统                          |
| app\_version    | string   | 否  | 当前前端版本                        |
| cli\_version    | string   | 否  | CLI 版本                        |

---

## 19.4 接入与安装类事件字段

### 事件：install\_started

| 字段名               | 类型     | 必填 | 说明            |
| ----------------- | ------ | -- | ------------- |
| installation\_id  | string | 是  | 本次安装唯一 ID     |
| install\_mode     | string | 是  | demo / team   |
| target\_ide       | string | 否  | 目标 IDE        |
| selected\_profile | string | 否  | 安装选择的 profile |

### 事件：install\_completed

| 字段名              | 类型     | 必填 | 说明             |
| ---------------- | ------ | -- | -------------- |
| installation\_id | string | 是  | 本次安装唯一 ID      |
| install\_result  | string | 是  | success / fail |
| duration\_ms     | number | 否  | 安装耗时           |
| error\_code      | string | 否  | 失败错误码          |
| error\_message   | string | 否  | 失败原因           |

### 事件：collector\_connected

| 字段名                | 类型       | 必填 | 说明                 |
| ------------------ | -------- | -- | ------------------ |
| connection\_mode   | string   | 是  | token / simplified |
| server\_url        | string   | 否  | 服务地址               |
| connection\_result | string   | 是  | success / fail     |
| last\_sync\_time   | datetime | 否  | 最近同步时间             |

---

## 19.5 运行态类事件字段

### 事件：demand\_started

| 字段名          | 类型     | 必填 | 说明                                                 |
| ------------ | ------ | -- | -------------------------------------------------- |
| run\_id      | string | 是  | 运行实例 ID                                            |
| change\_id   | string | 否  | 关联变更 ID                                            |
| flow\_type   | string | 是  | prd-to-delivery / bugfix-to-verification / patch 等 |
| demand\_type | string | 否  | component-replace / bugfix / refactor              |
| risk\_level  | string | 否  | low / medium / high                                |

### 事件：run\_status\_changed

| 字段名              | 类型     | 必填 | 说明      |
| ---------------- | ------ | -- | ------- |
| run\_id          | string | 是  | 运行实例 ID |
| previous\_status | string | 否  | 上一个状态   |
| current\_status  | string | 是  | 当前状态    |
| current\_phase   | string | 否  | 当前阶段    |
| current\_role    | string | 否  | 当前角色    |

### 事件：run\_blocked

| 字段名             | 类型     | 必填 | 说明      |
| --------------- | ------ | -- | ------- |
| run\_id         | string | 是  | 运行实例 ID |
| blocked\_phase  | string | 是  | 阻塞阶段    |
| blocked\_reason | string | 是  | 阻塞原因    |
| blocked\_owner  | string | 否  | 当前需处理角色 |

### 事件：run\_resumed

| 字段名                 | 类型     | 必填 | 说明      |
| ------------------- | ------ | -- | ------- |
| run\_id             | string | 是  | 运行实例 ID |
| resume\_from\_phase | string | 否  | 从哪个阶段恢复 |
| resume\_reason      | string | 否  | 恢复原因    |

### 事件：archive\_completed

| 字段名               | 类型     | 必填 | 说明             |
| ----------------- | ------ | -- | -------------- |
| run\_id           | string | 是  | 运行实例 ID        |
| archive\_result   | string | 是  | success / fail |
| archive\_time\_ms | number | 否  | 从开始到归档耗时       |
| asset\_count      | number | 否  | 本次沉淀资产数量       |

---

## 19.6 分流决策类事件字段

### 事件：flow\_decision\_started

| 字段名               | 类型      | 必填 | 说明               |
| ----------------- | ------- | -- | ---------------- |
| decision\_id      | string  | 是  | 决策实例 ID          |
| input\_scope      | string  | 否  | 输入的改动范围描述        |
| has\_active\_run  | boolean | 否  | 是否存在 active run  |
| has\_open\_change | boolean | 否  | 是否存在 open change |
| is\_archived      | boolean | 否  | 是否已归档            |

### 事件：flow\_decision\_completed

| 字段名                 | 类型     | 必填 | 说明       |
| ------------------- | ------ | -- | -------- |
| decision\_id        | string | 是  | 决策实例 ID  |
| recommended\_flow   | string | 是  | 推荐链路     |
| selected\_flow      | string | 否  | 用户最终选择链路 |
| auto\_match\_reason | string | 否  | 推荐理由     |

---

## 19.7 规范资产类事件字段

### 事件：asset\_detected

| 字段名                 | 类型     | 必填 | 说明                                                    |
| ------------------- | ------ | -- | ----------------------------------------------------- |
| asset\_type         | string | 是  | rules / skills / openspec / ai-spec / registry / logs |
| asset\_status       | string | 是  | detected / missing / invalid                          |
| asset\_path         | string | 否  | 资产路径                                                  |
| completeness\_score | number | 否  | 完整度评分                                                 |

### 事件：asset\_reused

| 字段名          | 类型     | 必填 | 说明       |
| ------------ | ------ | -- | -------- |
| asset\_type  | string | 是  | 被复用资产类型  |
| reuse\_count | number | 否  | 当前累计复用次数 |
| reuse\_scene | string | 否  | 复用场景     |

---

## 19.8 首页交互类事件字段

### 事件：dashboard\_viewed

| 字段名                 | 类型      | 必填 | 说明          |
| ------------------- | ------- | -- | ----------- |
| dashboard\_version  | string  | 否  | 首页版本        |
| has\_demo\_data     | boolean | 否  | 是否为 Demo 数据 |
| first\_visit\_today | boolean | 否  | 今日是否首次访问    |

### 事件：onboarding\_action\_clicked

| 字段名               | 类型     | 必填 | 说明               |
| ----------------- | ------ | -- | ---------------- |
| action\_name      | string | 是  | 点击动作名称           |
| onboarding\_stage | string | 否  | 当前 onboarding 阶段 |
| target\_path      | string | 否  | 跳转目标路径           |

### 事件：module\_card\_clicked

| 字段名             | 类型     | 必填 | 说明      |
| --------------- | ------ | -- | ------- |
| module\_name    | string | 是  | 模块名称    |
| click\_target   | string | 否  | 点击对象    |
| position\_index | number | 否  | 在页面中的位置 |

---

## 19.9 效率评估类字段

### 事件：efficiency\_snapshot\_generated

| 字段名                       | 类型     | 必填 | 说明                          |
| ------------------------- | ------ | -- | --------------------------- |
| baseline\_duration\_hours | number | 否  | 基线工时                        |
| current\_duration\_hours  | number | 否  | 当前工时                        |
| saved\_duration\_hours    | number | 否  | 节省工时                        |
| scene\_type               | string | 否  | 场景类型                        |
| estimation\_type          | string | 否  | manual / calculated / mixed |

---

## 19.10 首版建议优先落地的事件

首版建议优先实现以下事件：

1. dashboard\_viewed
2. install\_started
3. install\_completed
4. collector\_connected
5. demand\_started
6. run\_status\_changed
7. run\_blocked
8. archive\_completed
9. flow\_decision\_completed
10. asset\_detected
11. onboarding\_action\_clicked
12. efficiency\_snapshot\_generated

这些事件已足够支撑首版验证：

- 有没有人用
- 有没有接入成功
- 有没有真实需求在跑
- 有没有完成归档
- 卡在哪
- 值不值得继续推广

---

## 19.11 字段命名建议

1. 所有事件统一采用小写下划线命名
2. 所有状态值统一采用枚举值，不允许中英文混写
3. 所有 ID 字段统一保留 string 类型，便于跨系统兼容
4. 所有时间字段统一保留原始时间戳与格式化时间两种能力
5. 首版字段先稳定，不要频繁改名

---

## 20. 下一步输出建议

基于本稿，下一步建议继续产出：

1. 《首页线框图 / 中保真原型说明》
2. 《首页各模块交互状态清单》
3. 《埋点事件字典与枚举值规范》
4. 《组件替换试点模板文档》
5. 《开发者 10 分钟快速开始文档》

这样就可以从产品方案继续推进到交互设计、前端实现与试点执行。

---

## 21. 首页线框图说明

## 21.1 页面目标

首页线框图的目标不是表达视觉风格，而是明确：
- 首屏应该先呈现什么
- 哪些信息必须固定在第一视区
- 哪些模块适合向下滚动查看
- 模块间的主次关系与交互跳转关系

首版首页以桌面 Web 为主，建议设计宽度基于 1440 栅格系统进行输出，同时兼容 1280 宽度下的主流笔记本场景。

---

## 21.2 首页线框图结构说明（桌面端）

### 区域 A：固定顶栏

#### 目标
承载全局导航、Workspace 切换与高频动作。

#### 布局
- 左侧：Logo + 产品名称
- 中部：Workspace 切换器 + 搜索框
- 右侧：快捷操作按钮组 + 通知 + 用户信息

#### 推荐按钮
- 开始一个需求
- 判断本次改动走哪条链
- 接入当前项目

#### 说明
顶栏固定，页面滚动时始终可见。

---

### 区域 B：页面标题与说明区

#### 目标
帮助用户快速理解首页定位与当前浏览范围。

#### 展示内容
- 主标题：交付驾驶舱
- 副标题：查看规范驱动 AI 开发的接入状态、运行态、阻塞点与交付结果
- 说明文本：默认展示当前 Workspace 的汇总信息
- 右侧操作：
  - 打开 Demo Workspace
  - 查看 10 分钟快速开始
  - 查看命令速查

---

### 区域 C：首屏核心区

#### 布局方式
采用左大右三的组合布局：
- 左侧 7 栅格：Onboarding 报告
- 右侧 5 栅格：
  - 第一行：运行态健康度
  - 第二行：交付闭环进度
  - 第三行：效率收益卡

#### 设计原因
- Onboarding 报告承担“引导 + 接入判断 + 下一步动作”，优先级最高
- 右侧三张卡解决“现在是否在跑、是否有结果、是否产生价值”三个核心判断

---

### 区域 D：观测分析区

#### 布局方式
左右两列等宽：
- 左侧：阻塞变化流
- 右侧：规范资产命中情况

#### 设计原因
- 阻塞是“流程推进问题”
- 资产命中是“接入质量问题”
- 两者组合后能判断“为什么没有跑出结果”

---

### 区域 E：业务运行区

#### 布局方式
- 第一行：最近 Runs（通栏）
- 第二行左侧：最近 Changes / Specs
- 第二行右侧：安装与接入趋势

#### 设计原因
- Runs 是最贴近当前开发动作的数据，优先级高于 Changes / Specs
- 安装与接入趋势偏管理视角，放在次级位置更合理

---

### 区域 F：试点与扩展区

#### 布局方式
左右两列：
- 左侧：试点项目专区
- 右侧：试点复盘与建议动作区

#### 设计原因
- 支撑内部推广与试点汇报
- 不打断首页首要信息，但为平台扩展留出空间

---

## 21.3 首页线框图（文本版增强）

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ Logo / 产品名    Workspace切换    全局搜索    开始一个需求    分流决策    用户 │
├──────────────────────────────────────────────────────────────────────────────┤
│ 交付驾驶舱                                                               │
│ 查看规范驱动 AI 开发的接入状态、运行态、阻塞点与交付结果。                │
│ [打开Demo Workspace] [查看10分钟快速开始] [查看命令速查]                  │
├──────────────────────────────────────────────────────────────────────────────┤
│                         │ 运行态健康度                                      │
│  接入与上手报告         ├───────────────────────────────────────────────────┤
│  - 当前接入阶段         │ 交付闭环进度                                      │
│  - 已检测资产           ├───────────────────────────────────────────────────┤
│  - 下一步建议           │ 效率收益                                          │
│  - 快速开始入口         │                                                   │
├──────────────────────────────────────────────────────────────────────────────┤
│ 阻塞变化流                              │ 规范资产命中情况                  │
│ - 阻塞阶段分布                          │ - rules / skills                  │
│ - 阻塞原因 Top N                        │ - openspec / .ai-spec             │
│ - 最近24小时新增                        │ - registry / logs                 │
├──────────────────────────────────────────────────────────────────────────────┤
│ 最近 Runs                                                             查看全部│
│ 需求名称 | 项目 | 当前阶段 | 当前角色 | 更新时间 | 状态标签                 │
├──────────────────────────────────────────────────────────────────────────────┤
│ 最近 Changes / Specs                   │ 安装与接入趋势                    │
│ - 最近更新与归档                        │ - 安装人数 / 项目数 / 趋势图       │
├──────────────────────────────────────────────────────────────────────────────┤
│ 试点项目专区                            │ 试点复盘与建议动作                │
│ - 项目状态 / 负责人 / 阻塞 / 归档       │ - 当前问题 / 下一步建议 / 复盘入口 │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 21.4 模块尺寸建议（桌面端）

| 模块 | 建议宽度 | 建议高度 | 备注 |
|------|----------|----------|------|
| 顶栏 | 100% | 64px | 固定吸顶 |
| 页面标题区 | 100% | 88px ~ 120px | 根据说明文字可伸缩 |
| Onboarding 报告 | 7/12 | 320px ~ 380px | 首屏最大卡 |
| 运行态健康度 | 5/12 | 100px ~ 120px | 摘要卡 |
| 交付闭环进度 | 5/12 | 100px ~ 120px | 摘要卡 |
| 效率收益卡 | 5/12 | 100px ~ 120px | 摘要卡 |
| 阻塞变化流 | 6/12 | 320px ~ 360px | 图表 + 列表 |
| 规范资产命中情况 | 6/12 | 320px ~ 360px | 清单 + 评分 |
| 最近 Runs | 12/12 | 320px ~ 420px | 表格主区域 |
| 最近 Changes / Specs | 6/12 | 240px ~ 300px | 列表卡 |
| 安装与接入趋势 | 6/12 | 240px ~ 300px | 图表卡 |
| 试点项目专区 | 6/12 | 260px ~ 320px | 列表卡 |
| 试点复盘与建议动作 | 6/12 | 260px ~ 320px | 总结卡 |

---

## 21.5 模块交互流说明

### 流 1：首次接入用户
1. 进入首页
2. 先看 Onboarding 报告
3. 点击“接入当前项目”或“查看 10 分钟快速开始”
4. 接入后返回首页
5. Onboarding 状态更新为“已安装 Base / 已联通 Visual”
6. 点击“开始一个需求”

### 流 2：已接入开发者
1. 进入首页
2. 查看运行态健康度与交付闭环进度
3. 查看最近 Runs
4. 进入某个 Run 详情继续推进

### 流 3：平台管理员
1. 进入首页
2. 查看安装与接入趋势
3. 查看阻塞变化流
4. 查看试点项目专区
5. 进入 Workspace / 项目详情进行排查

---

## 21.6 线框图输出要求（给设计 / 前端）

### 设计侧输出要求
- 输出桌面端首页线框图
- 补充 3 类状态：空态、加载态、异常态
- 标注各模块信息层级与跳转关系
- 提供中保真版本时补充主按钮状态与表格字段

### 前端侧输出要求
- 首页模块支持独立渲染与异步加载
- 首屏关键卡片优先请求与渲染
- 趋势图与次级列表支持懒加载或延迟加载
- 模块级错误边界独立显示

---

## 22. 前端页面拆解表

## 22.1 页面拆解原则

1. 首页必须支持模块级独立开发与独立联调
2. 页面状态要和模块状态拆开管理，避免一个接口失败拖垮整页
3. 数据请求按“首屏优先、趋势次之、列表再次之”的顺序组织
4. 每个模块必须绑定对应埋点事件和 API 来源

---

## 22.2 首页页面拆解总表

| 页面 / 模块 | 模块类型 | 优先级 | 是否首屏 | 负责人建议 | 备注 |
|------|------|------|------|------|------|
| DashboardPage | 页面容器 | P0 | 是 | 前端主负责人 | 承载布局、状态管理、模块装配 |
| TopNav | 导航模块 | P0 | 是 | 前端 | 吸顶、全局入口 |
| DashboardHeader | 标题模块 | P0 | 是 | 前端 | 页面标题与快捷入口 |
| OnboardingCard | 卡片模块 | P0 | 是 | 前端 | 首屏最高优先级 |
| RuntimeHealthCard | 卡片模块 | P0 | 是 | 前端 | 摘要 + 趋势 |
| DeliveryProgressCard | 卡片模块 | P0 | 是 | 前端 | 摘要 + 闭环率 |
| EfficiencyValueCard | 卡片模块 | P0 | 是 | 前端 | 收益展示 |
| BlockFlowPanel | 面板模块 | P0 | 否 | 前端 | 阻塞图表 + 列表 |
| AssetCoveragePanel | 面板模块 | P0 | 否 | 前端 | 资产命中情况 |
| RecentRunsTable | 表格模块 | P1 | 否 | 前端 | 最近 Runs |
| RecentChangesPanel | 列表模块 | P1 | 否 | 前端 | 最近 Changes / Specs |
| InstallationTrendPanel | 图表模块 | P1 | 否 | 前端 | 接入趋势 |
| PilotProjectsPanel | 列表模块 | P1 | 否 | 前端 | 试点项目 |
| PilotReviewPanel | 摘要模块 | P1 | 否 | 前端 | 试点复盘与建议 |

---

## 22.3 模块拆解明细

### 1）DashboardPage
#### 职责
- 页面布局编排
- 模块请求时序控制
- Workspace 维度切换
- 页面级空态 / 加载态 / 异常态兜底

#### 状态建议
- `workspaceReady`
- `pageLoading`
- `pageError`
- `hasAnyData`

#### 依赖
- 当前登录态
- 当前 Workspace
- 首页聚合接口

---

### 2）OnboardingCard
#### 职责
- 展示当前接入阶段
- 展示资产检测状态
- 展示下一步建议动作
- 提供快捷入口

#### 子组件建议
- `OnboardingStageTag`
- `AssetChecklist`
- `NextActionList`
- `QuickActionButtons`

#### 前端状态
- `stage`
- `assetChecklist`
- `nextActions`
- `hasDetectedError`

---

### 3）RuntimeHealthCard
#### 职责
- 展示运行摘要指标
- 展示迷你趋势图
- 提供跳转 Runs 页入口

#### 前端状态
- `runningCount`
- `abnormalCount`
- `activeProjectCount`
- `lastSyncTime`
- `trendData`

---

### 4）DeliveryProgressCard
#### 职责
- 展示交付闭环相关指标
- 支持周维度、今日维度切换

#### 前端状态
- `startedToday`
- `archivedToday`
- `weeklyCloseRate`
- `firstArchiveCount`
- `pilotDoneCount`

---

### 5）EfficiencyValueCard
#### 职责
- 展示时间收益与归档资产收益
- 支持基线说明与数据来源提示

#### 前端状态
- `avgPageDuration`
- `avgPilotDuration`
- `savedDurationRange`
- `archivedAssetCount`
- `reusedTemplateCount`

---

### 6）BlockFlowPanel
#### 职责
- 展示阻塞阶段分布
- 展示阻塞原因 Top N
- 展示阻塞需求列表入口

#### 子组件建议
- `BlockedStageTabs`
- `BlockedReasonChart`
- `BlockedSummaryList`

#### 前端状态
- `blockedTotal`
- `blockedStageStats`
- `blockedReasonTop`
- `blockedLast24h`

---

### 7）AssetCoveragePanel
#### 职责
- 展示规范资产检测清单
- 展示完整度评分
- 提供缺失资产修复入口

#### 前端状态
- `rulesStatus`
- `skillsStatus`
- `openSpecStatus`
- `aiSpecStatus`
- `registryStatus`
- `logsStatus`
- `coverageScore`

---

### 8）RecentRunsTable
#### 职责
- 展示最近运行中的需求
- 支持进入 Run 详情
- 支持快速筛选阻塞 / 归档前状态

#### 列字段建议
- 需求名称
- 项目
- 当前阶段
- 当前角色
- 更新时间
- 状态
- 操作

#### 前端状态
- `list`
- `pagination`
- `filters`
- `sorter`

---

### 9）RecentChangesPanel
#### 职责
- 展示最近 Change / Spec 动态
- 支持跳转详情

#### 前端状态
- `items`
- `activeTab`

---

### 10）InstallationTrendPanel
#### 职责
- 展示安装人数、接入项目数、趋势图
- 支持 7 天 / 30 天切换

#### 前端状态
- `installUsers`
- `projectCount`
- `workspaceCount`
- `collectorConnectedCount`
- `trendRange`
- `trendData`

---

### 11）PilotProjectsPanel
#### 职责
- 展示试点项目列表
- 展示当前状态、负责人、阻塞数、归档数

#### 前端状态
- `pilotProjects`
- `selectedProject`

---

### 12）PilotReviewPanel
#### 职责
- 展示试点复盘摘要
- 展示当前建议动作
- 支持跳转到试点文档或复盘页

#### 前端状态
- `reviewSummary`
- `nextRecommendations`

---

## 22.4 首页请求时序建议

### 第一批请求（首屏必需）
- 首页聚合摘要接口
- Onboarding 报告接口
- 当前 Workspace 基础信息接口

### 第二批请求（首屏后补充）
- 阻塞变化流接口
- 规范资产命中接口
- 最近 Runs 接口

### 第三批请求（次屏与扩展）
- 最近 Changes / Specs 接口
- 安装与接入趋势接口
- 试点项目接口
- 试点复盘接口

---

## 22.5 页面状态管理建议

### 页面级状态
- 当前 Workspace 是否有效
- 页面整体是否初始化完成
- 是否进入 Demo 模式

### 模块级状态
- 独立 loading
- 独立 empty
- 独立 error
- 独立 retry

### 首版技术建议
- 页面容器负责布局与共享上下文
- 模块组件负责各自请求与状态管理
- 趋势图和列表组件尽量无副作用、可复用

---

## 23. API / 埋点映射表

## 23.1 设计目标

该映射表用于明确三件事：
1. 每个首页模块依赖哪些 API
2. 每个模块应触发哪些埋点事件
3. 接口、页面、埋点之间如何形成闭环

---

## 23.2 首页模块 API / 埋点总表

| 模块 | API 建议 | 请求时机 | 核心埋点 | 说明 |
|------|------|------|------|------|
| DashboardPage | `/api/dashboard/summary` | 页面进入 | `dashboard_viewed` | 首页聚合摘要 |
| OnboardingCard | `/api/dashboard/onboarding` | 页面进入 | `onboarding_action_clicked` | 接入与下一步建议 |
| RuntimeHealthCard | `/api/dashboard/runtime-health` | 页面进入 | `module_card_clicked` | 运行摘要 |
| DeliveryProgressCard | `/api/dashboard/delivery-progress` | 页面进入 | `module_card_clicked` | 闭环进度 |
| EfficiencyValueCard | `/api/dashboard/efficiency` | 页面进入 | `efficiency_snapshot_generated` | 收益快照 |
| BlockFlowPanel | `/api/dashboard/block-flow` | 首屏后 | `module_card_clicked` | 阻塞分布 |
| AssetCoveragePanel | `/api/dashboard/asset-coverage` | 首屏后 | `asset_detected` | 资产命中 |
| RecentRunsTable | `/api/runs/recent` | 首屏后 | `module_card_clicked` | 最近 Runs |
| RecentChangesPanel | `/api/changes/recent` | 次屏 | `module_card_clicked` | 最近 Changes / Specs |
| InstallationTrendPanel | `/api/dashboard/installation-trend` | 次屏 | `module_card_clicked` | 接入趋势 |
| PilotProjectsPanel | `/api/dashboard/pilot-projects` | 次屏 | `module_card_clicked` | 试点项目 |
| PilotReviewPanel | `/api/dashboard/pilot-review` | 次屏 | `module_card_clicked` | 复盘建议 |

---

## 23.3 API 设计建议

### 1）首页聚合摘要接口
**接口建议**：`GET /api/dashboard/summary`

#### 返回字段建议
- workspace_id
- workspace_name
- onboarding_stage
- running_count
- abnormal_count
- active_project_count
- started_today
- archived_today
- weekly_close_rate
- avg_page_duration
- saved_duration_range
- has_demo_data

#### 使用模块
- DashboardPage
- 页面标题区部分摘要

---

### 2）Onboarding 报告接口
**接口建议**：`GET /api/dashboard/onboarding`

#### 返回字段建议
- stage
- asset_checklist
- next_actions
- quick_links
- missing_assets
- detect_error_message

#### 使用模块
- OnboardingCard

#### 对应埋点
- `onboarding_action_clicked`

---

### 3）运行态健康度接口
**接口建议**：`GET /api/dashboard/runtime-health`

#### 返回字段建议
- running_count
- abnormal_count
- active_project_count
- last_sync_time
- trend_data

#### 使用模块
- RuntimeHealthCard

#### 对应埋点
- `module_card_clicked`
- 进入详情后可触发 `module_card_clicked` + `click_target=runs_detail`

---

### 4）交付闭环进度接口
**接口建议**：`GET /api/dashboard/delivery-progress`

#### 返回字段建议
- started_today
- archived_today
- weekly_close_rate
- first_archive_count
- pilot_done_count
- compare_last_week

#### 使用模块
- DeliveryProgressCard

---

### 5）效率收益接口
**接口建议**：`GET /api/dashboard/efficiency`

#### 返回字段建议
- avg_page_duration
- avg_pilot_duration
- saved_duration_range
- archived_asset_count
- reused_template_count
- estimation_type

#### 使用模块
- EfficiencyValueCard

#### 对应埋点
- `efficiency_snapshot_generated`

---

### 6）阻塞变化流接口
**接口建议**：`GET /api/dashboard/block-flow`

#### 返回字段建议
- blocked_total
- blocked_stage_stats
- blocked_reason_top
- blocked_last_24h
- blocked_items_preview

#### 使用模块
- BlockFlowPanel

#### 对应埋点
- `module_card_clicked`

---

### 7）规范资产命中接口
**接口建议**：`GET /api/dashboard/asset-coverage`

#### 返回字段建议
- rules_status
- skills_status
- openspec_status
- ai_spec_status
- registry_status
- logs_status
- coverage_score
- missing_items

#### 使用模块
- AssetCoveragePanel

#### 对应埋点
- `asset_detected`

---

### 8）最近 Runs 接口
**接口建议**：`GET /api/runs/recent`

#### 返回字段建议
- list[].run_id
- list[].name
- list[].project_name
- list[].current_phase
- list[].current_role
- list[].updated_at
- list[].status
- list[].blocked

#### 使用模块
- RecentRunsTable

#### 对应埋点
- `module_card_clicked`

---

### 9）最近 Changes / Specs 接口
**接口建议**：`GET /api/changes/recent`

#### 返回字段建议
- list[].id
- list[].type
- list[].name
- list[].project_name
- list[].status
- list[].archived
- list[].updated_at

#### 使用模块
- RecentChangesPanel

---

### 10）安装与接入趋势接口
**接口建议**：`GET /api/dashboard/installation-trend`

#### 返回字段建议
- install_users
- project_count
- workspace_count
- collector_connected_count
- range
- trend_data

#### 使用模块
- InstallationTrendPanel

---

### 11）试点项目接口
**接口建议**：`GET /api/dashboard/pilot-projects`

#### 返回字段建议
- list[].project_id
- list[].project_name
- list[].owner
- list[].status
- list[].blocked_count
- list[].archived_count
- list[].last_feedback

#### 使用模块
- PilotProjectsPanel

---

### 12）试点复盘接口
**接口建议**：`GET /api/dashboard/pilot-review`

#### 返回字段建议
- summary
- current_issues
- next_recommendations
- report_link

#### 使用模块
- PilotReviewPanel

---

## 23.4 关键交互与埋点映射

| 页面动作 | 触发埋点 | 关键字段 | 说明 |
|------|------|------|------|
| 进入首页 | `dashboard_viewed` | workspace_id, has_demo_data | 首次访问首页 |
| 点击开始一个需求 | `onboarding_action_clicked` | action_name, onboarding_stage | 从首页进入需求流 |
| 点击分流决策 | `onboarding_action_clicked` | action_name=flow_decision | 进入变更分流器 |
| 点击接入项目 | `onboarding_action_clicked` | action_name=project_connect | 进入接入流程 |
| 点击运行态健康度卡片 | `module_card_clicked` | module_name=runtime_health | 进入 Runs 详情 |
| 点击阻塞变化流某阶段 | `module_card_clicked` | module_name=block_flow, click_target=phase_tab | 查看某阶段阻塞 |
| 点击最近 Runs 某行 | `module_card_clicked` | module_name=recent_runs, click_target=run_item | 进入 Run 详情 |
| 点击规范资产修复入口 | `module_card_clicked` | module_name=asset_coverage, click_target=repair_link | 查看修复指引 |

---

## 23.5 首页模块与后端能力映射建议

| 模块 | 后端能力来源建议 | 备注 |
|------|------|------|
| OnboardingCard | Workspace + Collector + 资产扫描聚合 | 需要聚合多个数据源 |
| RuntimeHealthCard | Runs / RunEvents 聚合 | 可结合最近心跳或最近更新时间 |
| DeliveryProgressCard | Runs + Changes + Archive 结果聚合 | 需要时间维度统计 |
| EfficiencyValueCard | 业务侧评估表 + 归档数据 | 首版可先半人工 |
| BlockFlowPanel | RunEvents / BlockState 聚合 | 需要原因枚举 |
| AssetCoveragePanel | Collector 扫描结果聚合 | 直接对应文件资产 |
| RecentRunsTable | Runs 列表查询 | 标准列表能力 |
| RecentChangesPanel | Changes / Specs 列表查询 | 标准列表能力 |
| InstallationTrendPanel | Installation / InstallationEvent 聚合 | 已有遥测方向 |
| PilotProjectsPanel | 试点项目白名单 + 状态表 | 可单独维护 |
| PilotReviewPanel | 试点复盘记录表 | 可先手工录入 |

---

## 23.6 首版接口实施优先级

### P0 接口
- `/api/dashboard/summary`
- `/api/dashboard/onboarding`
- `/api/dashboard/runtime-health`
- `/api/dashboard/delivery-progress`
- `/api/dashboard/efficiency`
- `/api/dashboard/block-flow`
- `/api/dashboard/asset-coverage`
- `/api/runs/recent`

### P1 接口
- `/api/changes/recent`
- `/api/dashboard/installation-trend`
- `/api/dashboard/pilot-projects`
- `/api/dashboard/pilot-review`

### 说明
P0 接口足以支撑首页首版上线；P1 接口用于完善平台推广与试点复盘能力。

---

## 24. 下一步建议

基于本稿，下一步建议继续产出：

1. 《首页各模块交互状态清单》
2. 《埋点事件字典与枚举值规范》
3. 《首页 API 数据结构定义（请求 / 响应示例）》
4. 《前端组件树与目录结构建议》
5. 《首页研发任务拆解表》

这样就可以继续从“页面方案”推进到“接口设计、前端开发与联调执行”。

---

## 25. 首页研发任务拆解表

## 25.1 拆解原则

1. 任务拆解按“页面骨架 → 核心卡片 → 数据列表 → 趋势图表 → 联调验收”的顺序推进
2. 首屏 P0 模块优先落地，保证最短可演示路径
3. 所有任务必须明确输入、输出、依赖与验收标准
4. 前端、后端、产品、测试的协作边界尽量清晰
5. 首版优先保证“能接入、能看见、能判断、能继续推进”

---

## 25.2 首页研发里程碑

### M1：页面骨架可运行
目标：页面路由、基础布局、顶栏、标题区可用

### M2：首屏核心卡片可联调
目标：Onboarding、运行态、闭环进度、效率收益可显示真实数据

### M3：观测与列表模块可联调
目标：阻塞变化流、资产命中、最近 Runs 可用

### M4：扩展模块与试点视图可演示
目标：Changes / Specs、安装趋势、试点项目、试点复盘可展示

### M5：埋点与异常状态补齐
目标：首页埋点、模块异常态、空态、重试逻辑全部补齐

---

## 25.3 研发任务拆解总表

| 任务编号 | 任务名称 | 优先级 | 负责人建议 | 前置依赖 | 交付物 | 验收标准 |
|------|------|------|------|------|------|------|
| FE-DASH-001 | 首页路由与页面容器搭建 | P0 | 前端 | 无 | DashboardPage 页面骨架 | 页面可访问，布局正确 |
| FE-DASH-002 | 顶栏与 Workspace 切换器 | P0 | 前端 | FE-DASH-001 | TopNav 模块 | 支持展示当前 Workspace |
| FE-DASH-003 | 页面标题区与快捷入口 | P0 | 前端 | FE-DASH-001 | DashboardHeader 模块 | 标题、副标题、按钮正常显示 |
| FE-DASH-004 | Onboarding 报告卡片开发 | P0 | 前端 | FE-DASH-001 | OnboardingCard | 支持不同状态展示 |
| FE-DASH-005 | 运行态健康度卡片开发 | P0 | 前端 | FE-DASH-001 | RuntimeHealthCard | 数据可正常显示 |
| FE-DASH-006 | 交付闭环进度卡片开发 | P0 | 前端 | FE-DASH-001 | DeliveryProgressCard | 数据可正常显示 |
| FE-DASH-007 | 效率收益卡开发 | P0 | 前端 | FE-DASH-001 | EfficiencyValueCard | 数据可正常显示 |
| FE-DASH-008 | 阻塞变化流面板开发 | P0 | 前端 | FE-DASH-001 | BlockFlowPanel | 图表与列表可渲染 |
| FE-DASH-009 | 规范资产命中面板开发 | P0 | 前端 | FE-DASH-001 | AssetCoveragePanel | 资产状态可展示 |
| FE-DASH-010 | 最近 Runs 表格开发 | P1 | 前端 | FE-DASH-001 | RecentRunsTable | 列表、操作、空态正常 |
| FE-DASH-011 | 最近 Changes / Specs 面板 | P1 | 前端 | FE-DASH-001 | RecentChangesPanel | 支持切换与展示 |
| FE-DASH-012 | 安装与接入趋势面板 | P1 | 前端 | FE-DASH-001 | InstallationTrendPanel | 趋势图可展示 |
| FE-DASH-013 | 试点项目专区面板 | P1 | 前端 | FE-DASH-001 | PilotProjectsPanel | 试点项目数据可展示 |
| FE-DASH-014 | 试点复盘与建议面板 | P1 | 前端 | FE-DASH-001 | PilotReviewPanel | 复盘摘要可展示 |
| FE-DASH-015 | 首页聚合数据请求接入 | P0 | 前端 | 后端首页摘要接口 | 页面数据接入层 | 页面首屏数据联通 |
| FE-DASH-016 | 首页模块级 loading / empty / error 处理 | P0 | 前端 | 各模块完成 | 状态组件与重试逻辑 | 各模块状态可独立展示 |
| FE-DASH-017 | 首页埋点接入 | P0 | 前端 | 埋点字典确认 | 页面与模块埋点 | 关键行为有埋点 |
| FE-DASH-018 | Demo Workspace 适配 | P1 | 前端 | 页面主体完成 | Demo 模式兼容 | 支持示例数据展示 |
| FE-DASH-019 | 首页视觉优化与样式统一 | P1 | 前端 | 模块基本完成 | 样式实现 | 与设计一致 |
| BE-DASH-001 | 首页摘要聚合接口开发 | P0 | 后端 | 数据表准备 | `/api/dashboard/summary` | 返回字段完整 |
| BE-DASH-002 | Onboarding 接口开发 | P0 | 后端 | Collector / Workspace 能力 | `/api/dashboard/onboarding` | 返回阶段与建议动作 |
| BE-DASH-003 | 运行态健康度接口开发 | P0 | 后端 | Runs 数据可查 | `/api/dashboard/runtime-health` | 返回摘要与趋势 |
| BE-DASH-004 | 交付闭环进度接口开发 | P0 | 后端 | Runs / Archive 数据 | `/api/dashboard/delivery-progress` | 返回闭环数据 |
| BE-DASH-005 | 效率收益接口开发 | P0 | 后端 | 评估口径确认 | `/api/dashboard/efficiency` | 返回收益字段 |
| BE-DASH-006 | 阻塞变化流接口开发 | P0 | 后端 | Block 数据可聚合 | `/api/dashboard/block-flow` | 返回阻塞分布 |
| BE-DASH-007 | 规范资产命中接口开发 | P0 | 后端 | Collector 数据可查 | `/api/dashboard/asset-coverage` | 返回资产状态 |
| BE-DASH-008 | 最近 Runs 接口开发 | P0 | 后端 | Runs 列表查询 | `/api/runs/recent` | 支持列表返回 |
| BE-DASH-009 | 最近 Changes / Specs 接口开发 | P1 | 后端 | Changes / Specs 数据 | `/api/changes/recent` | 支持列表返回 |
| BE-DASH-010 | 安装与接入趋势接口开发 | P1 | 后端 | Installation 数据 | `/api/dashboard/installation-trend` | 返回趋势数据 |
| BE-DASH-011 | 试点项目接口开发 | P1 | 后端 | 试点项目维护表 | `/api/dashboard/pilot-projects` | 返回试点列表 |
| BE-DASH-012 | 试点复盘接口开发 | P1 | 后端 | 复盘表 / 静态配置 | `/api/dashboard/pilot-review` | 返回复盘摘要 |
| QA-DASH-001 | 首页主流程测试用例设计 | P0 | 测试 | PRD / 页面方案 | 测试用例 | 覆盖首屏主流程 |
| QA-DASH-002 | 模块状态测试用例设计 | P0 | 测试 | 模块状态明确 | 测试用例 | 覆盖 loading/empty/error |
| QA-DASH-003 | 埋点验证测试 | P1 | 测试 | 埋点接入完成 | 埋点验证报告 | 关键事件准确上报 |

---

## 25.4 前端任务详细说明

### FE-DASH-001：首页路由与页面容器搭建
#### 目标
完成首页基础路由、整体布局容器、模块挂载位置。

#### 输入
- 首页信息架构稿
- 线框图说明

#### 输出
- `DashboardPage`
- 页面基础布局
- 模块占位结构

#### 验收标准
- 首页路由可访问
- 顶栏、标题区、模块区域布局正确
- 支持后续独立挂载各模块

---

### FE-DASH-004：Onboarding 报告卡片开发
#### 目标
优先完成首屏最核心卡片。

#### 输出
- 接入阶段展示
- 资产清单展示
- 下一步动作按钮
- 空态 / 异常态 / loading 态

#### 验收标准
- 支持至少 5 种阶段状态
- 支持点击跳转动作
- 缺失资产时有明显提示

---

### FE-DASH-008：阻塞变化流面板开发
#### 目标
体现平台观测价值。

#### 输出
- 阻塞阶段统计区
- 阻塞原因排行区
- 阻塞预览列表

#### 验收标准
- 支持图表或可视统计卡
- 支持点击进入筛选后的详情页

---

### FE-DASH-016：首页模块级状态处理
#### 目标
避免一个模块失败拖垮整页。

#### 输出
- 通用 `LoadingState`
- 通用 `EmptyState`
- 通用 `ErrorState`
- 模块级 retry 能力

#### 验收标准
- 任意模块报错时不影响其他模块渲染
- 支持单模块重试

---

## 25.5 后端任务详细说明

### BE-DASH-001：首页摘要聚合接口开发
#### 目标
一次返回首页首屏最关键聚合数据。

#### 输入
- Workspace 基础信息
- Runs 聚合数据
- 交付闭环统计
- 效率快照摘要

#### 输出
- `/api/dashboard/summary`

#### 验收标准
- 响应时间可控
- 字段完整
- 可用于首屏快速渲染

---

### BE-DASH-002：Onboarding 接口开发
#### 目标
聚合接入状态、资产扫描、下一步建议。

#### 验收标准
- 能正确识别接入阶段
- 支持返回缺失资产与建议动作

---

### BE-DASH-006：阻塞变化流接口开发
#### 目标
聚合阻塞阶段分布和原因分布。

#### 验收标准
- 支持按 Workspace 维度统计
- 支持返回 Top N 原因
- 支持最近 24 小时统计

---

## 25.6 联调顺序建议

### 第一轮联调
- `/api/dashboard/summary`
- `/api/dashboard/onboarding`
- `/api/dashboard/runtime-health`
- `/api/dashboard/delivery-progress`

### 第二轮联调
- `/api/dashboard/efficiency`
- `/api/dashboard/block-flow`
- `/api/dashboard/asset-coverage`
- `/api/runs/recent`

### 第三轮联调
- `/api/changes/recent`
- `/api/dashboard/installation-trend`
- `/api/dashboard/pilot-projects`
- `/api/dashboard/pilot-review`

---

## 25.7 验收清单

### 页面维度
- 首页首屏信息完整
- 首屏模块可独立工作
- 所有按钮可点击并有明确去向
- 空态 / 异常态 / loading 态齐全

### 数据维度
- 首页主摘要数据真实可用
- 模块数据与后台统计口径一致
- Demo 模式和真实模式都可运行

### 埋点维度
- 页面进入埋点正常
- 首页关键按钮埋点正常
- 模块点击埋点正常

---

## 26. 前端组件树与目录结构建议

## 26.1 设计原则

1. 页面容器、业务模块、通用状态组件分层明确
2. Dashboard 首页相关组件单独归类，避免与其他页面混杂
3. 图表、表格、卡片、状态组件可复用
4. 数据请求与 UI 组件解耦，便于后续演进

---

## 26.2 组件树建议

```text
DashboardPage
├── TopNav
│   ├── LogoBrand
│   ├── WorkspaceSwitcher
│   ├── GlobalSearch
│   ├── QuickActionGroup
│   └── UserMenu
├── DashboardHeader
│   ├── PageTitle
│   ├── PageDescription
│   └── HeaderActions
├── DashboardContent
│   ├── FirstScreenSection
│   │   ├── OnboardingCard
│   │   │   ├── OnboardingStageTag
│   │   │   ├── AssetChecklist
│   │   │   ├── NextActionList
│   │   │   └── QuickActionButtons
│   │   ├── RuntimeHealthCard
│   │   │   ├── SummaryMetrics
│   │   │   └── MiniTrendChart
│   │   ├── DeliveryProgressCard
│   │   │   ├── ProgressSummary
│   │   │   └── CloseRateChart
│   │   └── EfficiencyValueCard
│   │       ├── EfficiencyMetrics
│   │       └── BaselineHint
│   ├── InsightSection
│   │   ├── BlockFlowPanel
│   │   │   ├── StageTabs
│   │   │   ├── BlockReasonChart
│   │   │   └── BlockPreviewList
│   │   └── AssetCoveragePanel
│   │       ├── AssetStatusList
│   │       ├── CoverageScore
│   │       └── RepairEntry
│   ├── ActivitySection
│   │   ├── RecentRunsTable
│   │   ├── RecentChangesPanel
│   │   └── InstallationTrendPanel
│   └── PilotSection
│       ├── PilotProjectsPanel
│       └── PilotReviewPanel
└── DashboardStateLayer
    ├── PageLoadingState
    ├── PageEmptyState
    └── PageErrorState
```

---

## 26.3 目录结构建议

### 推荐目录（按页面域拆分）

```text
src/
├── app/
│   └── dashboard/
│       └── page.tsx
├── features/
│   └── dashboard/
│       ├── components/
│       │   ├── TopNav/
│       │   ├── DashboardHeader/
│       │   ├── OnboardingCard/
│       │   ├── RuntimeHealthCard/
│       │   ├── DeliveryProgressCard/
│       │   ├── EfficiencyValueCard/
│       │   ├── BlockFlowPanel/
│       │   ├── AssetCoveragePanel/
│       │   ├── RecentRunsTable/
│       │   ├── RecentChangesPanel/
│       │   ├── InstallationTrendPanel/
│       │   ├── PilotProjectsPanel/
│       │   ├── PilotReviewPanel/
│       │   └── states/
│       ├── hooks/
│       │   ├── useDashboardSummary.ts
│       │   ├── useOnboarding.ts
│       │   ├── useRuntimeHealth.ts
│       │   ├── useDeliveryProgress.ts
│       │   ├── useEfficiency.ts
│       │   ├── useBlockFlow.ts
│       │   ├── useAssetCoverage.ts
│       │   ├── useRecentRuns.ts
│       │   ├── useRecentChanges.ts
│       │   ├── useInstallationTrend.ts
│       │   ├── usePilotProjects.ts
│       │   └── usePilotReview.ts
│       ├── services/
│       │   ├── dashboard.service.ts
│       │   ├── runs.service.ts
│       │   └── changes.service.ts
│       ├── types/
│       │   ├── dashboard.ts
│       │   ├── runs.ts
│       │   └── changes.ts
│       ├── constants/
│       │   ├── dashboard.ts
│       │   └── enums.ts
│       └── utils/
│           ├── formatters.ts
│           ├── mappers.ts
│           └── chart.ts
├── components/
│   ├── common/
│   │   ├── LoadingState/
│   │   ├── EmptyState/
│   │   ├── ErrorState/
│   │   └── MetricCard/
│   └── charts/
│       ├── MiniTrendChart/
│       ├── BlockReasonChart/
│       └── ProgressChart/
└── lib/
    ├── request/
    ├── analytics/
    └── auth/
```

---

## 26.4 目录设计说明

### features/dashboard/components
用于存放首页专属业务组件，避免和全局组件混用。

### features/dashboard/hooks
每个模块一个 hook，负责请求、数据转换、状态输出。

### features/dashboard/services
集中封装接口请求，不把请求散落到组件内部。

### components/common
放通用状态组件、通用指标卡、通用空态组件。

### components/charts
图表组件独立抽离，便于在其他页面复用。

---

## 26.5 前端类型定义建议

### dashboard.ts 建议至少包含
- `DashboardSummaryResponse`
- `OnboardingResponse`
- `RuntimeHealthResponse`
- `DeliveryProgressResponse`
- `EfficiencyResponse`
- `BlockFlowResponse`
- `AssetCoverageResponse`
- `InstallationTrendResponse`
- `PilotProjectsResponse`
- `PilotReviewResponse`

### runs.ts 建议至少包含
- `RecentRunItem`
- `RecentRunsResponse`
- `RunStatus`
- `RunPhase`

### changes.ts 建议至少包含
- `RecentChangeItem`
- `RecentChangesResponse`
- `ChangeType`
- `ChangeStatus`

---

## 26.6 前端实现建议

1. 首屏四个核心卡片可优先走聚合接口 + 局部拆分接口兼容模式
2. 各模块请求 hook 统一返回：
   - `data`
   - `loading`
   - `error`
   - `reload`
3. 图表组件只接收整理后的数据，不直接感知接口结构
4. 埋点调用放在 action 层或 hooks 层，不散落在视图 JSX 中
5. Demo 数据与真实接口数据建议走统一 mapper 层适配

---

## 27. 首页 API 请求响应示例

## 27.1 说明

以下示例用于帮助前后端统一字段结构与接口理解。
首版建议全部使用 JSON 返回，状态码与错误格式统一。

---

## 27.2 通用响应格式建议

### 成功响应
```json
{
  "code": 0,
  "message": "成功",
  "data": {}
}
```

### 失败响应
```json
{
  "code": 1001,
  "message": "当前工作区不存在或无访问权限",
  "data": null,
  "requestId": "req_xxx"
}
```

---

## 27.3 首页摘要接口示例

### 请求
```http
GET /api/dashboard/summary?workspaceId=ws_demo_001
```

### 响应
```json
{
  "code": 0,
  "message": "成功",
  "data": {
    "workspaceId": "ws_demo_001",
    "workspaceName": "业务中台试点工作区",
    "hasDemoData": false,
    "onboardingStage": "connected_visual",
    "runningCount": 6,
    "abnormalCount": 1,
    "activeProjectCount": 3,
    "startedToday": 4,
    "archivedToday": 2,
    "weeklyCloseRate": 0.67,
    "avgPageDuration": 0.42,
    "savedDurationRange": "0.2-0.5天"
  }
}
```

---

## 27.4 Onboarding 接口示例

### 请求
```http
GET /api/dashboard/onboarding?workspaceId=ws_demo_001
```

### 响应
```json
{
  "code": 0,
  "message": "成功",
  "data": {
    "stage": "connected_visual",
    "assetChecklist": [
      { "assetType": "rules", "status": "detected" },
      { "assetType": "skills", "status": "detected" },
      { "assetType": "openspec", "status": "detected" },
      { "assetType": "ai_spec", "status": "detected" },
      { "assetType": "registry", "status": "missing" },
      { "assetType": "logs", "status": "detected" }
    ],
    "missingAssets": ["registry"],
    "nextActions": [
      {
        "actionKey": "start_demand",
        "title": "开始一个需求",
        "description": "发起一个真实需求并跑通从开始到归档的闭环",
        "targetPath": "/runs/new"
      },
      {
        "actionKey": "view_quickstart",
        "title": "查看10分钟快速开始",
        "description": "适合第一次接入的开发者快速了解路径",
        "targetPath": "/docs/quickstart"
      }
    ],
    "quickLinks": [
      { "title": "命令速查", "targetPath": "/docs/commands" },
      { "title": "Demo Workspace", "targetPath": "/demo" }
    ],
    "detectErrorMessage": ""
  }
}
```

---

## 27.5 运行态健康度接口示例

### 请求
```http
GET /api/dashboard/runtime-health?workspaceId=ws_demo_001&range=7d
```

### 响应
```json
{
  "code": 0,
  "message": "成功",
  "data": {
    "runningCount": 6,
    "abnormalCount": 1,
    "activeProjectCount": 3,
    "lastSyncTime": "2026-04-23 16:20:30",
    "trendData": [
      { "date": "2026-04-17", "runningCount": 3, "abnormalCount": 0 },
      { "date": "2026-04-18", "runningCount": 5, "abnormalCount": 1 },
      { "date": "2026-04-19", "runningCount": 4, "abnormalCount": 0 },
      { "date": "2026-04-20", "runningCount": 6, "abnormalCount": 1 },
      { "date": "2026-04-21", "runningCount": 7, "abnormalCount": 1 },
      { "date": "2026-04-22", "runningCount": 5, "abnormalCount": 0 },
      { "date": "2026-04-23", "runningCount": 6, "abnormalCount": 1 }
    ]
  }
}
```

---

## 27.6 交付闭环进度接口示例

### 请求
```http
GET /api/dashboard/delivery-progress?workspaceId=ws_demo_001
```

### 响应
```json
{
  "code": 0,
  "message": "成功",
  "data": {
    "startedToday": 4,
    "archivedToday": 2,
    "weeklyCloseRate": 0.67,
    "firstArchiveCount": 1,
    "pilotDoneCount": 3,
    "compareLastWeek": 0.12
  }
}
```

---

## 27.7 效率收益接口示例

### 请求
```http
GET /api/dashboard/efficiency?workspaceId=ws_demo_001
```

### 响应
```json
{
  "code": 0,
  "message": "成功",
  "data": {
    "avgPageDuration": 0.42,
    "avgPilotDuration": 0.38,
    "savedDurationRange": "0.2-0.5天",
    "archivedAssetCount": 11,
    "reusedTemplateCount": 2,
    "estimationType": "mixed"
  }
}
```

---

## 27.8 阻塞变化流接口示例

### 请求
```http
GET /api/dashboard/block-flow?workspaceId=ws_demo_001
```

### 响应
```json
{
  "code": 0,
  "message": "成功",
  "data": {
    "blockedTotal": 3,
    "blockedStageStats": [
      { "stage": "before_implementation", "count": 1 },
      { "stage": "before_guardian", "count": 1 },
      { "stage": "before_archive", "count": 1 }
    ],
    "blockedReasonTop": [
      { "reason": "需求范围未收敛", "count": 1 },
      { "reason": "规范资产不完整", "count": 1 },
      { "reason": "缺少回归验证结果", "count": 1 }
    ],
    "blockedLast24h": 1,
    "blockedItemsPreview": [
      {
        "runId": "run_1001",
        "name": "用户中心组件替换",
        "stage": "before_archive",
        "reason": "缺少回归验证结果"
      }
    ]
  }
}
```

---

## 27.9 规范资产命中接口示例

### 请求
```http
GET /api/dashboard/asset-coverage?workspaceId=ws_demo_001
```

### 响应
```json
{
  "code": 0,
  "message": "成功",
  "data": {
    "rulesStatus": "detected",
    "skillsStatus": "detected",
    "openspecStatus": "detected",
    "aiSpecStatus": "detected",
    "registryStatus": "missing",
    "logsStatus": "detected",
    "coverageScore": 84,
    "missingItems": [
      {
        "assetType": "registry",
        "repairHint": "请检查 .agents/registry 目录是否存在并完成同步"
      }
    ]
  }
}
```

---

## 27.10 最近 Runs 接口示例

### 请求
```http
GET /api/runs/recent?workspaceId=ws_demo_001&page=1&pageSize=10
```

### 响应
```json
{
  "code": 0,
  "message": "成功",
  "data": {
    "list": [
      {
        "runId": "run_1001",
        "name": "用户中心组件替换",
        "projectName": "业务中台项目A",
        "currentPhase": "implementation",
        "currentRole": "developer",
        "updatedAt": "2026-04-23 16:18:20",
        "status": "running",
        "blocked": false
      },
      {
        "runId": "run_1002",
        "name": "筛选面板规范重构",
        "projectName": "业务中台项目B",
        "currentPhase": "archive",
        "currentRole": "guardian",
        "updatedAt": "2026-04-23 15:42:11",
        "status": "blocked",
        "blocked": true
      }
    ],
    "pagination": {
      "page": 1,
      "pageSize": 10,
      "total": 26
    }
  }
}
```

---

## 27.11 最近 Changes / Specs 接口示例

### 请求
```http
GET /api/changes/recent?workspaceId=ws_demo_001&type=all
```

### 响应
```json
{
  "code": 0,
  "message": "成功",
  "data": {
    "list": [
      {
        "id": "chg_2001",
        "type": "change",
        "name": "用户中心组件替换变更单",
        "projectName": "业务中台项目A",
        "status": "active",
        "archived": false,
        "updatedAt": "2026-04-23 16:00:00"
      },
      {
        "id": "spec_3001",
        "type": "spec",
        "name": "筛选面板规范文档",
        "projectName": "业务中台项目B",
        "status": "archived",
        "archived": true,
        "updatedAt": "2026-04-23 14:21:55"
      }
    ]
  }
}
```

---

## 27.12 安装与接入趋势接口示例

### 请求
```http
GET /api/dashboard/installation-trend?workspaceId=ws_demo_001&range=7d
```

### 响应
```json
{
  "code": 0,
  "message": "成功",
  "data": {
    "installUsers": 8,
    "projectCount": 5,
    "workspaceCount": 1,
    "collectorConnectedCount": 4,
    "range": "7d",
    "trendData": [
      { "date": "2026-04-17", "installUsers": 1, "projectCount": 1 },
      { "date": "2026-04-18", "installUsers": 2, "projectCount": 2 },
      { "date": "2026-04-19", "installUsers": 4, "projectCount": 2 },
      { "date": "2026-04-20", "installUsers": 5, "projectCount": 3 },
      { "date": "2026-04-21", "installUsers": 6, "projectCount": 4 },
      { "date": "2026-04-22", "installUsers": 7, "projectCount": 4 },
      { "date": "2026-04-23", "installUsers": 8, "projectCount": 5 }
    ]
  }
}
```

---

## 27.13 试点项目接口示例

### 请求
```http
GET /api/dashboard/pilot-projects?workspaceId=ws_demo_001
```

### 响应
```json
{
  "code": 0,
  "message": "成功",
  "data": {
    "list": [
      {
        "projectId": "proj_001",
        "projectName": "业务中台项目A",
        "owner": "张三",
        "status": "running",
        "blockedCount": 1,
        "archivedCount": 3,
        "lastFeedback": "组件替换效率明显提升"
      },
      {
        "projectId": "proj_002",
        "projectName": "业务中台项目B",
        "owner": "李四",
        "status": "connected",
        "blockedCount": 0,
        "archivedCount": 1,
        "lastFeedback": "接入过程较顺畅"
      }
    ]
  }
}
```

---

## 27.14 试点复盘接口示例

### 请求
```http
GET /api/dashboard/pilot-review?workspaceId=ws_demo_001
```

### 响应
```json
{
  "code": 0,
  "message": "成功",
  "data": {
    "summary": "当前试点已覆盖 2 个中台项目，已完成 4 个组件替换闭环，整体反馈正向。",
    "currentIssues": [
      "首次接入仍需进一步压缩路径",
      "部分规范资产缺失时提示不够直接"
    ],
    "nextRecommendations": [
      "补齐 Demo Workspace 初始化能力",
      "增加分流决策器显式入口",
      "完善资产修复指引"
    ],
    "reportLink": "/pilot/review/2026-q2"
  }
}
```

---

## 27.15 错误码建议

| 错误码 | 含义 | 建议处理 |
|------|------|------|
| 1001 | Workspace 不存在或无权限 | 页面显示权限异常态 |
| 1002 | 当前 Workspace 尚未接入 | 页面显示接入引导空态 |
| 1003 | Collector 数据未准备完成 | 模块显示等待同步提示 |
| 1004 | 统计数据暂不可用 | 模块显示空态并支持重试 |
| 1005 | 请求参数错误 | 页面记录日志并提示刷新 |

---

## 28. 下一步建议

基于本稿，下一步建议继续产出：

1. 《首页各模块交互状态清单》
2. 《埋点事件字典与枚举值规范》
3. 《首页研发排期表（按周 / 按人）》
4. 《首页联调与测试用例清单》
5. 《首页 UI 视觉稿说明》

这样就可以从当前方案继续推进到真正的开发排期、接口联调和测试执行。

