# Node.js NestJS 后端工程标准

## 适用技术栈

- 语言：TypeScript 5+，开启 `strict`；ESLint/Prettier 与团队基线一致。Node.js 使用 LTS 版本，写在 `.nvmrc` 或项目 README 中。
- 框架：NestJS；HTTP、GraphQL、gRPC、微服务传输等按需使用，以模块（Module）为依赖注入与边界单位。
- 构建：`nest build` 与 TypeScript 编译；pnpm、yarn 或 npm 的锁文件在 CI 中不可忽略。`package.json` 的 `engines` 与生产镜像中的 Node 版本一致。
- 运行环境：进程或容器；`NODE_ENV` 等通过 `@nestjs/config` 加载，并用 `class-validator`、Joi 或 Zod 等做配置校验，团队内统一选一种在边界使用。

## 适用项目类型

- application：可独立启动的 HTTP 或混合入口；若有后台任务或 CLI，建议拆为独立应用或同仓独立 `main`。
- service：单体或模块化单部署单元，以目录与模块划分子域。
- microservice：多个 Nest 应用或不同传输；不得依赖可写共享内存做业务正确性，以数据存储与消息为准。
- monorepo：通过 Nx、Turborepo 或 npm workspaces 管理；共享包被应用引用，应用间不互引实现包，只通过已发布的 API、消息或契约包集成。

## 项目结构规范

- Controller（或 GraphQL Resolver）：路由、Guard、Pipe、Interceptor 的落点，不写业务规则、不管理事务。
- Service / 用例类：用例编排、 ORM/事务、外部服务调用与顺序；可拆为 Query/Command 或领域服务，避免单类承担全部逻辑。
- Repository 与数据访问层：将 TypeORM、Prisma、MikroORM 或原生 SQL 封在模块内；Controller 不直接写查询或调用底层驱动。
- Entity/Schema 与 DTO 分离；请求、响应、列表项类型各自定义，便于演进而不在公网 API 中泄漏内部表结构。
- Module 按限界上下文划分，禁止 `imports` 成环。

## Controller 规范

- 职责：协议适配、参数与身份（通过 Guard/装饰器）绑定、HTTP 状态、与 `ExceptionFilter` 协作。
- 参数：`ValidationPipe` 与 DTO；根据项目选择 `whitelist`、`forbidNonWhitelisted` 等；文件、分页、游标、排序使用专用 DTO。
- 响应：若使用统一成功或错误体，全项目一致；分页/游标字段名固定。
- 状态码：201 与 `Location` 用于创建；4xx/5xx 的语义在文档中唯一约定。业务可预期失败采用「4xx+子码」或「200+业务 code」二选一，禁止无说明混用。
- 校验：字段与简单结构在 Pipe+DTO；跨表、跨聚合规则在 Service 或领域层。

## Service 规范

- 在 Service 中声明业务编排与单库事务边界；禁止在 Controller 中显式开闭事务或依赖未文档的连接行为。
- 领域规则可下放到纯函数、领域实体、领域服务，提高可测性。
- 对 HTTP、消息、缓存的调用应配置超时、冪等键、重试上界、熔断/降级，日志带 `request id` / `correlation id`。

## DTO / VO / Entity 规范

- Request/Response DTO 与 OpenAPI/路由一一对应；不直接把 ORM 实体作公网 JSON 外发，除非有显式 Mapping 与字段白名单。
- 内部可定义 VO/ReadModel，不纳入对外契约版本。
- DTO 的演进（新增/废弃字段）在文档与客户端约定上可追溯。

## Repository / Mapper 规范

- 数据访问封装在同一模块；Controller 不拼接 SQL/GraphQL 片段。
- Repository 不包含业务 if-else，仅做查询、映射、显式 `join`/关系策略，避免无约束的 N+1。

## 异常处理

- `ExceptionFilter` 将异常统一为 body、HTTP 码与 trace；不向客户端返回堆栈与内网信息。
- 可预期业务错误用自定义 `HttpException` 或项目约定的错误体；不可预期错误记 error 级日志与追踪。
- 外部服务失败应结构化记日志，不打 Token 全量。

## 参数校验

- 必填、类型、范围、长度、格式、嵌套、数组、枚举在 DTO+Pipe 中；跨字段在自定义校验器或 Service/领域层。
- 与数据库唯一性、状态机相关的校验在 Service/领域，返回码与《API 设计》一致（如 409/422）。

## 日志规范

- 使用结构化日志，贯穿 `request id`；脱敏密码、Token、身份证、卡号等。
- 审计与业务操作可区分 `level` 与输出目标，满足留存策略。

## 权限规范

- 认证在 Guard 与 Passport 等策略中集中配置；各 Controller 不重复手写解析用户。
- 授权用角色、资源、策略；数据权限在查询层注入租户/数据范围，禁止在多处散落硬编码 `WHERE` 特例。
- 服务间用服务账户、mTLS 或短生命周期 Token，轮换有清单。

## 事务规范

- 单库：在同一用例的 Service 方法中提交或回滚；不依赖未文档的隐式连接/会话。
- 冪等：用唯一键、冪等表、冪等键 header；分布式用 Saga、Outbox、最终一致，不默认两阶段跨异构资源。
- 可重试错误类型与重试上界、熔断在配置或代码中可审计。

## 测试规范

- 单元：Jest，mock 掉 Repository 与 HTTP；覆盖领域与分支。
- 集成：最小 Nest 应用切片 + 内存/容器化依赖。
- 契约与 E2E：Supertest 或 Pact 等覆盖公开路径；主路径在 CI 为必过。

## Rule 生成要求

- 约束：无环 `Module`、入口强制 DTO 校验、禁止无约束的 `any`、外呼带超时、敏感配置不进仓库。
- 禁止行为：在 Controller/Resolver 写大段业务、多处重复或不一致的校验、日志打印密钥。
- 验收标准：`lint`、`test`、`build` 在 CI 全绿，OpenAPI 与实现可对照。

## Skill 生成要求

- 输入：功能说明、子域/模块建议、NFR 与合规模块、现有基线（OpenAPI/错误码表）。
- 步骤：定模块与 DTO 契约；实现 Service+事务+数据层；接 Controller+Guard+Pipe；补单测和集成测试；更新文档。
- 输出：可安装可运行的项目骨架、接口清单、不含虚构 URL 与密钥的部署说明。
- 异常：说明失败时回滚/补偿/人工对账/消息重试的边界。

## Flow 生成要求

- 阶段：设计评审后实现、自测、Code Review、按环境发布与联调、观测与告警校验。
- 门禁：类型检查、lint、单测、关键 E2E、依赖漏洞扫描、许可证策略。
- 状态：任务/版本/缺陷与发布单、变更记录关联。
- 异常出口：回滚、hotfix、只读/降级、人工对账、死信与补偿任务。

## Manifest 推荐

- 资产组合：Nest 编码规范规则集、OpenAPI 生成/校验、适用于团队的 Node 基础镜像、OpenTelemetry 或等价的追踪指标日志方案。
- 安装策略：锁定 `@nestjs` 与核心 peer 依赖大版本；不在 Skill 中写死组织内部 registry 地址与凭证。

## 禁止行为

- 禁止以「可直接上线」为由输出大量未经评审的完整业务源码；不虚构不存在的端点、版本、认证与租户模型。
- 禁止在文档或技能中要求提供或固化生产密钥、证书私钥、生产数据库高权限账户；以占位符与密钥服务为准。

## 验收标准

- 本地与 CI 可复现安装与构建，测试与静态检查通过，环境变量可列出清单，公网行为与 OpenAPI/契约可验证，敏感信息不入库、不入普通日志。
