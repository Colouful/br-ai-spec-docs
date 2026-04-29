# 术语表

| 术语 | 说明 |
|---|---|
| AI Engineering Control Plane | AI 研发控制平面，统一规范、上下文、Agent、测试、证据、观测的系统 |
| br-ai-spec | 本地控制器，负责在业务项目中执行 AI 研发流程 |
| skill-q-platform | 资产治理中心，管理 Manifest、Rule、Skill、Agent Profile 等资产 |
| br-ai-spec-visual | 运行观测中心，展示 Run、Task、Agent、测试、证据 |
| OpenSpec | 需求规格事实源，包含 proposal、design、tasks、spec delta、archive |
| Manifest | 规范包索引，声明当前项目使用哪些资产 |
| Rule | 工程规则，如代码风格、架构边界、禁止事项 |
| Skill | 任务能力，如生成 API 契约、测试计划、前端页面实现 |
| Agent Profile | Agent 角色定义，包括职责、输入、输出、边界 |
| Hook Spec | 门禁规则，如 Scope Guard、Dangerous File Guard |
| Test Gate | 测试门禁，如 lint、unit test、api test |
| Context Pack | 当前任务上下文包，默认由 run.bundle.json 承载 |
| Progressive Disclosure | 渐进式披露，按需加载资产和上下文，不一次性塞入全部内容 |
| Task DAG | 有向无环任务图，包含 dependsOn、writeSet、lockKeys 等信息 |
| writeSet | 当前任务允许写入的文件范围 |
| readSet | 当前任务需要读取的文件范围 |
| lockKeys | 逻辑锁，如 api:/product-config、db:product_config |
| Executor Pool | 执行 Agent 池，可并行执行无冲突 Task |
| Git worktree | Git 多工作区机制，用于隔离多个并行 Task |
| Change Branch | 当前需求的主开发分支 |
| Task Branch | 某个 Task 的临时执行分支 |
| Patch Bundle | Task 执行完成后产出的补丁包 |
| Merge Agent | 负责合并 Patch Bundle 的 Agent |
| Repair Agent | 测试失败后进行有限修复的 Agent |
| Evidence | 执行证据，如测试结果、验收清单、diff 摘要、最终报告 |
| evidence-index.json | 证据索引文件，记录所有证据的类型、路径、关联任务、生成时间 |
| run.bundle.json | 当前 Run 的核心状态文件 |
| run.log.jsonl | 运行事件日志，支持回放和恢复 |
| L1 | 轻量修复任务 |
| L2 | 标准需求，强制完整 OpenSpec 与验收证据 |
| L3 | 高风险需求，强制人工确认和完整审查 |
