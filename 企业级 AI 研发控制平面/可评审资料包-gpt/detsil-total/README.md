# Enterprise AI Control Plane V0.1 评审资料包

版本：V0.1 Review Pack  
用途：给产品、前端、后端、测试、架构、研发效能同事进行第一轮方案评审。

## 一、资料包目标

本资料包用于评审一套面向企业全栈项目的 AI 研发控制平面方案。它不是单纯的提示词库，也不是某个 IDE 的配置集合，而是围绕 Cursor、Claude Code、Codex 等 AI IDE 建立统一的规范资产、项目上下文、OpenSpec、Task DAG、多执行 Agent、Git worktree 隔离、Hook 门禁、Test Gate、Evidence 证据落盘和运行态观测体系。

核心目标：

1. 让 AI 开发从“会写代码”升级为“按企业流程交付需求”。
2. 让 AI 在真实中台金融系统中可控、可验证、可审计。
3. 让 Rule、Skill、Agent Profile、Hook、Test Gate、Context Policy 成为企业可治理资产。
4. 支持 5-10 小时级复杂开发任务：大任务拆小任务、小任务拆需求、需求拆可执行清单。
5. 通过 Git worktree 做多执行 Agent 隔离开发，避免并行修改污染主工作区。
6. 最大限度降低对业务项目的侵入性。

## 二、推荐阅读顺序

| 顺序 | 文档 | 角色 | 评审重点 |
|---:|---|---|---|
| 1 | `01-prd/v0.1-prd.md` | 产品、负责人 | 是否值得做，V0.1 范围是否合理 |
| 2 | `02-architecture/v0.1-architecture.md` | 架构、前后端负责人 | 总体架构、三仓职责、执行链路 |
| 3 | `03-repo-implementation/three-repo-implementation-plan.md` | 项目负责人 | 三个仓库各改什么、怎么对接 |
| 4 | `04-code-design/v0.1-code-implementation-design.md` | 开发同事、AI 编码工具 | 代码模块、命令、数据结构、实现细节 |
| 5 | `06-sample-financial-middle-platform-flow/financial-mid-platform-sample-flow.md` | 业务、研发、测试 | 是否贴近真实中台金融系统需求 |
| 6 | `05-review-checklist/enterprise-review-checklist.md` | 全体评审人 | 按问题清单反馈 |
| 7 | `07-roadmap/v0.1-to-v1.0-roadmap.md` | 负责人 | 后续规划与投入判断 |

## 三、本次评审最关键的 10 个问题

1. 是否认可“企业级 AI 研发控制平面”的定位？
2. V0.1 是否应该以中台金融系统为第一条真实样板链路？
3. OpenSpec 是否接受放在项目根目录 `openspec/`，作为需求规格事实源？
4. L2 标准需求是否也强制生成完整 OpenSpec？
5. `.ai-spec/` 与 `.ai-spec-local/` 的目录侵入性是否可接受？
6. Git worktree 是否作为多执行 Agent 并行开发的强制隔离机制？
7. “一个可执行 Task 一个 worktree”的粒度是否合理？
8. 证据落盘是否默认放在 `.ai-spec-local/runs/{runId}/`，并支持归档？
9. 三仓职责是否清晰：br-ai-spec 本地控制器、skill-q-platform 资产治理、br-ai-spec-visual 运行观测？
10. V0.1 的范围是否需要缩小？

## 四、评审反馈建议格式

```text
评审人：
角色：前端 / 后端 / 测试 / 架构 / 产品 / 研发效能 / 其他
关注文档：

1. 我认可的部分：
2. 我认为不符合实际需求的部分：
3. 我认为风险最大的部分：
4. 我建议 V0.1 必须保留的能力：
5. 我建议 V0.1 暂缓的能力：
6. 其他补充：
```
