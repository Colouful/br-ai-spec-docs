# multi-repo-execution-docs

## 文档包用途

本任务包用于在 `br-ai-spec` 已经执行过 P0-P5 的前提下，进行多仓库补充落地。它不是从 0 重做 P0-P5，而是先审计当前 `br-ai-spec` 执行结果，再把 P4 Visual 运行态观测落到 `br-ai-spec-visual`，把 P5 Asset Hub 与组织复用落到 `skill-q-platform`，最后完成四仓联调。

## 当前前提

1. `br-ai-spec` 已基于原 `project-execution-docs.zip` 执行过 P0-P5。
2. `br-ai-spec-visual` 和 `skill-q-platform` 尚未完成对应 P4 / P5 主体改造。
3. 后续不能继续把 Visual 和 Hub 能力塞进 `br-ai-spec`。
4. 本包所有验收结果默认是模板状态，必须由实际执行后填写。

## 推荐执行顺序

1. `00-多仓库现状审计与边界收口/`
2. `01-br-ai-spec-执行收口与连接器补充/`
3. `02-br-ai-spec-visual-P4执行包/`
4. `03-skill-q-platform-P5执行包/`
5. `04-四仓联调与文档同步/`

## 四仓职责

| 仓库 | 职责 |
| --- | --- |
| br-ai-spec | 本地 CLI、Harness Runtime、IDE Adapter、Hook、Repair、Evidence、Visual Connector、Hub Connector |
| br-ai-spec-visual | Run Timeline、运行态观测、指标看板、风险审计看板、Visual Governance |
| skill-q-platform | Rule / Skill / Agent Profile / Workflow / Hook / Command 资产中心、审核、发布、版本、回滚、组织复用 |
| br-ai-spec-docs | 标准说明、实施手册、验收记录、汇报材料和架构文档 |

## 如何交给 AI 编程模型使用

每次只选择一个小阶段目录，将该目录下 4 类文档交给 AI 执行：技术实现文档、测试文档、验收结果文档、进度同步文档。


## 禁止事项

1. 不允许把 Visual UI、Asset Hub 后台、企业管理页面继续塞进 `br-ai-spec`。
2. 不允许在 `br-ai-spec-visual` 中实现 CLI、Harness 执行器或资产安装逻辑。
3. 不允许在 `skill-q-platform` 中存储业务源码、原始 Prompt、密钥、敏感日志。
4. 不允许跳过测试、删除测试、降低测试标准或伪造测试结果。
5. 不允许静默忽略失败，所有失败必须记录到验收结果文档和进度同步文档。
6. 不允许破坏现有接口兼容性；如必须变更，必须提供兼容层和迁移说明。
7. 不允许引入未说明的大型依赖。
8. 不允许把运行态数据写入业务项目仓库。
9. 不允许跨仓库随意修改；每个小阶段只能修改当前文档允许的仓库与文件。
10. 不允许提交密钥、原始 Prompt、敏感日志、完整源码快照。
