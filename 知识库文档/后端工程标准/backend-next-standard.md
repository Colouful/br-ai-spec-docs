# Next.js 服务端与 BFF 工程标准

> 说明：本标准聚焦 **App Router** 下的 HTTP 层、**Server Actions**、中间件与「同仓 BFF」；与《Next.js 前端工程标准》互补——前端标准侧重 RSC/客户端与页面，本标准侧重仅服务端可执行的逻辑、数据边界与安全。

## 适用技术栈

- **语言**：TypeScript 为默认，建议 `strict`；`next-env.d.ts` 由工具维护，不手改。
- **框架与运行时**：Next.js 稳定主版本，App Router 为推荐；Route Handlers 通过 `app/**/route.ts` 暴露；Server Actions 作为受控的写路径（与表单/乐观 UI 的契约在 PRD 中定）。
- **运行环境**：为每个 Route Handler、Server Action 与 `middleware` 显式声明 `export const runtime = 'nodejs' | 'edge'`（以项目默认策略为准）。Edge 能力受限（部分 Node API、长连接、部分 ORM 不可用），不得混用未声明假设。
- **数据与集成**：经官方或团队封装的数据库客户端、HTTP 客户端、消息队列 SDK 等。密钥与连接串仅通过环境变量或密钥注入，不进入仓库与客户端 bundle。

## 适用项目类型

- **BFF / API 同仓**：与前端同部署，为浏览器提供聚合、裁剪、鉴权代转与错误翻译。若 BFF 不是唯一真源，须文档化下游 SOT 与缓存/一致性。
- **全栈应用的后端面**：RSC/页面取数在服务端；可写操作经 Server Actions 或 Route Handlers（分工须统一并文档化）。
- **仅 Headless API**：若 `app` 下几乎只有 `route.ts` 与少量 `page`，应评估是否用独立 Node 服务；若保留 Next，则本标准全部适用。
- **Monorepo**：`apps/bff` 或 `apps/web` 内嵌 BFF；共享 `packages/api-contract`、`packages/db` 等；`transpilePackages` 与 Server/Client 边界须保证服务端模块不被 client 包误引。

## 项目结构规范

- **HTTP 入口**：`app/api/.../route.ts` 或与 UI 同路径的 `app/.../route.ts`（代理/专用 API 的约定二选一并写清，避免同 URL 双实现）。
- **业务逻辑**：在 `lib/`、`server/`、`services/` 等无 `"use client"` 的模块中实现；Route Handler 与 Server Action 宜薄，做协议、状态码、校验与委托，不在入口写大段业务分支。
- **数据访问**：`lib/db`、Repository 或 ORM 封装与多租户/会话上下文绑定；禁止在 `route.ts` 中散布无约束的裸 SQL（除非有受控 query builder 与审计）。
- **契约**：OpenAPI 或 Zod schema 与对外 JSON 一一对应；内部 Entity 不直接串行化出给公网，除非有显式 mapper 与字段白名单。
- **中间件**：根目录 `middleware.ts`；`matcher` 精确，避免对静态与无关路径跑重逻辑；注意 Edge 下 API 限制。

## Route Handlers（`route.ts`）规范

- **职责**：按 Method（GET/POST/PUT/PATCH/DELETE）分函数导出；解析 `NextRequest`、校验输入、调用服务层、映射 HTTP 状态与 body；领域规则宜下沉服务层。
- **输入**：Query/Body/Header 用 Zod/valibot 等在边界解析；`Content-Type` 与文件上传有独立分支与大小限制。
- **响应**：统一成功/错误体（若项目约定）；`Cache-Control`、ETag、Vary 在可缓存读接口上显式设置；含用户或敏感数据的读接口禁止误配公共 CDN 长缓存。
- **状态码**：201 与 `Location` 表示创建；可预期业务失败在《API 设计》中唯一约定；5xx 仅用于非预期；不向客户端返回堆栈与内网地址。
- **CORS**：若 BFF 被跨源调用，白名单与 `credentials` 策略在配置中管理，不默认 `*` 与生产 cookie 同用，除非经安全评审。
- **流式与 SSE**：`ReadableStream` 等需超时、背压与客户端断开处理；在 serverless 上注意执行时长与连接限制。

## Server Actions 规范

- **边界**：`"use server"` 文件或顶置函数；仅从 Server Components 或表单的 `action` 以框架允许的方式调用；不将 Action 当作未鉴权的随意 RPC。
- **鉴权与 CSRF**：依赖 Next/Session 的会话与同源策略；若有跨站或非 form 调用需求，须单独设计 token/二次校验，禁止无防护的写操作。
- **输入校验**：与 Route Handlers 同等级 schema；不信任任意客户端序列化对象，不把不可信字符串直接拼进 SQL/命令。
- **重验证与副作用**：`revalidatePath`/`revalidateTag` 范围最小化；写后读与下游最终一致在文档中说明；失败时可逆或补偿策略可审计。
- **可测试性**：Action 内宜薄，核心逻辑放在纯函数或服务中做单测。

## 业务与数据层规范

- **服务层**：编排用例、事务、调用外部 HTTP/队列；配置超时、冪等键、重试上界、熔断/降级；日志带 `requestId`/`correlationId`。
- **Repository / 数据访问**：每个用例的数据范围（含租户、数据权限）在查询中体现，禁止「查全量再在内存里 filter」替代授权（大表、泄露风险）。
- **N+1**：ORM 的 `include`/dataloader 或显式 join；列表接口有分页、游标与最大 page size。
- **外部服务**：不硬编码 URL；不在日志中打印完整 token；对 4xx/5xx 区分可重试与不可重试。

## 中间件（`middleware`）规范

- **职责**：宜轻量——鉴权初筛、重定向、请求头注入、A/B 或地理粗路由；重业务放 Node Route 或下游。
- **与 Edge**：只用 Edge 支持的 API；JWT 验签注意算法与密钥来源；长耗时与大 body 不在中间件做。
- **匹配**：`matcher` 排除 `_next`、静态资源、健康检查路径，避免误伤与成本。
- **与 Route 的重复**：不要在每个 Handler 重复相同鉴权却行为不一；抽成 `assertSession()` 等单点。

## DTO、校验与类型

- **请求/响应 DTO** 与对外 JSON 一一对应；演进用版本或可选字段与文档，不静默改语义。
- **Zod/valibot** 在边界；共用的 schema 可与前端/契约包共享（`packages/contract`），避免手抄漂移。
- **TypeScript** 的 `any` 不进业务核心；JSON 入参先 parse，再 schema，再进领域。

## 异常处理与错误响应

- **统一错误体**（若项目有）：`code`/`message`/`requestId`；不返回堆栈、SQL、路径、内网 host。
- **可预期** 业务错误用 4xx 与稳定 `code`；**不可预期** 记 error 级日志与追踪，对外 500 泛化文案。
- **从下游映射** 错误：限流 429、认证 401/403；不把下游 500 原样当作可重试而无限重打。

## 日志与可观测

- **结构化** 日志；单请求贯穿 `requestId`；多服务用 `correlationId` 透传。
- **脱敏**：密码、refresh token、证件、全卡号等；PII 与留痕符合合规清单。
- **指标与追踪**：OpenTelemetry 或等价；关键路径延迟、错误率、依赖调用在可看板上可见；健康检查与深度探测分离。

## 安全规范

- **密钥**：仅环境/密钥服务；构建时不把生产密钥打进镜像层历史（多阶段构建与 `.dockerignore`）。
- **头**：`Content-Security-Policy` 等与产品形态一致；BFF 对下游的 mTLS/固定 IP 依环境文档化。
- **限流与防刷**：在网关或 BFF 对写与敏感读限流；登录/验证码有防爆破策略。
- **SSRF**：禁止由用户输入直接作为服务端 `fetch` URL；需白名单或内网代理模式。

## 缓存与数据一致性

- **Next `fetch` 缓存**：`cache`/`revalidate`/`tags` 与鉴权一致；用户级数据不共用可被误复用的 tag。
- **HTTP 缓存头**：`private`/`no-store` 用于含敏感或用户专属响应；BFF 聚合是否可缓存分资源讨论。
- **失效**：`revalidateTag` 与业务写的对应关系在设计中可追踪；最终一致有轮询/推送或可理解的延迟说明。

## 事务、冪等与并发

- **单库事务**：在一个服务方法内显式边界；不依赖未文档的隐式连接行为。
- **冪等**：`Idempotency-Key` 或业务唯一键；重复提交返回相同语义的成功或冲突响应。
- **分布式**：Saga/Outbox/消息等不在本标准穷举，但须有设计与可观测的补偿路径说明。

## 权限与多租户

- **认证**：Session、JWT、OAuth 等在一层统一；Route/Action 在进入业务前已解析 `user`/`tenant`（或明确匿名）。
- **授权**：RBAC/ABAC 的判定点在服务或领域层，不只在 UI 隐藏按钮；数据权限在查询中注入条件。
- **多租户**：`tenantId`（或等价）在全链路不来自可伪造的单一客户端字段而无校验；跨租户查询须经强审计与明确场景，禁止误串数据。

## 测试规范

- **单测**：服务层、校验 schema、纯函数；mock 外部 HTTP/DB 接口。
- **Route/Action 集成**：`node-mocks-http` 或官方推荐方式调用导出函数，或经部署环境的请求测试；覆盖 4xx/5xx 与鉴权分支。
- **契约**：Pact 或 OpenAPI diff；破坏兼容的变更在 CI 失败或需显式基线提升。
- **E2E**：对关键 BFF 路径与下游桩或沙箱；不在 CI 打生产下游。

## Rule 生成要求

- **生成约束**：须显式 App Router、runtime、错误体格式、Zod 边界、禁止 client 引用仅服务端密钥模块、`middleware` 匹配范围、环境变量清单与占位符命名规范。
- **禁止行为**：禁止虚构 `process.env.XXX` 的语义与下游 URL；禁止假定 Pages Router 的 `getServerSideProps` 为默认模式（除非项目声明存量）；禁止在 Rule 中要求关闭 TypeScript 严格以合并不合规代码。
- **验收标准**：`next build` 可通过；新增 Route/Action 不引入可被误打包到 client 的边界错误；与《API 设计》中的状态码与体一致。

## Skill 生成要求

- **输入**：功能、子域、鉴权与租户模型、NFR（延迟、一致、留痕）、现有 OpenAPI/错误码、下游契约或 mock 地址（非生产秘密）。
- **步骤**：定 URL 与 method → 定 schema 与错误码 → 写服务、数据与 Route 或 Action → 接日志/追踪 → 单测与集成测试 → 更新 OpenAPI/文档。
- **输出**：可审查的 diff、测试结果、环境变量说明、回滚与 `revalidate` 影响范围、无虚构端点与密钥的部署注记。
- **异常处理**：下游超时、部分成功、冪等冲突、`middleware` 与 Route 行为不一致、Edge/Node 运行时差异，须有检查清单与升级路径。

## Flow 生成要求

- **阶段**：接口与安全评审 → 实现 → 自测与契约测试 → Code Review → 预发与下游联调 → 生产发布与观测验证。
- **门禁**：`lint`、`typecheck`、`next build`、关键集成/契约测试、依赖与许可证扫描、敏感信息检测。
- **状态流转**：版本/变更单/缺陷与发布关联；灰度与功能开关的责任人明确。
- **异常出口**：回滚、只读、降级、熔断、人工对账、死信与重试。

## Manifest 推荐

- **推荐资产组合**：Zod/valibot、与前端共享的契约包、OpenAPI 生成/校验、统一错误体、`pino` 或 `next-axiom` 等结构化日志、OpenTelemetry、健康检查与 SLO 模板、`.env.example`（无真实秘密）、安全头与 CORS 基线。
- **安装策略**：锁定 Next 与 Node LTS 与生产一致；大版本升级须跑全量构建与 BFF 集成测试。

## 禁止行为

- 禁止在文档/Skill/AI 产物中输出大段可未经评审即视为可上线的业务实现，并以此作为最终判据。
- 禁止虚构不存在的 API、环境变量名、下游服务、租户模型、权限点；未确认须标注 TBD 与对接人。
- 禁止在服务端日志/错误体中回显可复用凭据与可识别全量 PII（除经批准的审计流）。
- 禁止将仅服务器可用的模块被同仓客户端包误引用，导致信息或凭据泄露。
- 禁止在无设计的情况下将 Server Action 当作对外公开 RPC 使用。

## 验收标准

- 本地与 CI 可复现 `next build`、测试与静态检查。
- 公开或约定 BFF 路径的行为与 OpenAPI/契约一致。
- 高危路径经鉴权与权限，审计有落点。
- 不存在客户可复用手段绕过服务端授权。
- 下游失败时行为可预期、可观测、可回滚或补偿。
- 与本文各章节一致，或差异在项目 ADR/清单中记录。
