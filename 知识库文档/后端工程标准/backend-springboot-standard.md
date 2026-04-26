# Spring Boot 后端工程标准

## 适用技术栈

- **语言**：Java 17+（LTS 优先，与团队 JDK 基线一致）。
- **框架**：Spring Boot 3.x，Spring Web / Spring Data / Validation 等按模块选用。
- **构建**：Gradle（Kotlin DSL 或 Groovy DSL）或 Maven 3.9+，与 CI 基线锁版本。
- **运行环境**：JVM 容器化或物理/虚拟机，配置通过 `application.yml` 与环境变量分层；可观测性对接 Micrometer/Actuator。

## 适用项目类型

- **application**：可独立部署的 HTTP/gRPC/批处理入口应用。
- **service**：对上游暴露业务能力、内部可再拆模块的单体或模块化单体。
- **microservice**：独立生命周期、独立数据存储边界的可部署单元（仍建议用模块化约束代码边界）。
- **monorepo**：多模块或多包仓库时，以 Maven/Gradle 模块与包结构反映领域边界，禁止循环依赖。

## 项目结构规范

- **Controller 层**（`controller` 或 `web` 包）：仅做 HTTP/协议适配、入参出参、状态码与全局异常落点，不写业务规则。
- **Service 层**（`service` 或 `application`）：用例编排、领域服务调用、事务开启点；可拆 `*Service` 与 `*Facade` 以隔离外部系统。
- **Repository 层**（`repository` / `jpa` / `mapper` 包）：JPA 接口、MyBatis Mapper 接口与 XML/注解 SQL，仅数据访问。
- **DTO/VO/Entity 包边界**：请求 DTO、响应 VO/DTO 与 JPA/持久化实体分目录，禁止在 API 层直接使用 Entity 作为出参（除非有明确全量与序列化控制）。
- **domain / model**（可选但推荐）：无框架依赖的实体与领域规则、领域事件、值对象。
- **config / common**：Bean 配置、安全、多数据源、重试、缓存等横切，避免业务类膨胀。

## Controller 规范

- 职责：路由、参数绑定、鉴权元数据、返回统一 `Response` 包装（若项目约定）、HTTP 状态码与 Location 等协议语义。
- 参数：Path/Query/Body 使用独立 DTO；文件上传、分页、排序在 DTO 内声明。
- 响应：成功体与错误体结构一致；分页统一字段（如 `items`/`total`/`page`）；禁止返回堆栈或内部异常详情给客户端。
- 状态码：4xx 客户端/校验错误，5xx 服务端/依赖失败；与业务「业务失败可预期」的区分在文档中明确（是 4xx+业务码 还是 200+业务 code）。
- 校验边界：简单字段校验在 DTO 上使用 Bean Validation；跨字段/跨聚合校验放到 Service 或领域层。

## Service 规范

- 业务编排：用例一个入口方法，步骤清晰，避免「上帝 Service」；复杂逻辑下推到 domain 或独立组件。
- 事务边界：在 Service 的公共方法上声明 `@Transactional`，只读用 `readOnly = true`；控制传播行为与回滚条件（`rollbackFor`）。
- 领域逻辑：优先放在 domain 或领域服务；Service 做编排与与基础设施的桥梁。
- 禁止在循环中开事务或大事务；对批量操作显式分片与失败策略。

## DTO / VO / Entity 规范

- **Request DTO**：与接口契约一一对应，可含验证注解，不承担持久化语义。
- **Response DTO/VO**：面向客户端视图，可聚合多实体字段，注意敏感字段与版本演进。
- **Entity**：JPA/ORM 实体仅映射表结构，不放 API 层返回；**禁止** 把 Entity 直接作 REST 出参，除非有 MapStruct/Assembler 与 OpenAPI 约束。
- 命名：`*Request`、`*Response`、`*Query` 等可读约定；**禁止** 同一类混用多职责。

## Repository / Mapper 规范

- 数据访问只出现在 Repository/Mapper 层，返回 Entity 或明确投影 DTO/Interface projection。
- 复杂查询可封装在 `@Query` 或 MyBatis 片段中；动态 SQL 集中、可测。
- **禁止** 在数据访问层写业务规则；**禁止** 在 Controller/Service 拼接 SQL 字符串（除非有统一 Query Builder 且可审计）。

## 异常处理

- **统一异常处理**：`@ControllerAdvice` 将异常映射为统一错误体与 HTTP 码；记录 traceId/请求标识。
- **业务异常**：可预见的规则违反用受检业务异常或错误码，避免当作 500。
- **参数异常**：Bean Validation 与 `MethodArgumentNotValidException` 统一为 400 与字段级错误信息。
- **外部依赖异常**：包装为可观测的结构化错误，可重试的用 Resilience4j/Retry 配置；日志含依赖名与可关联 ID，不含密钥。

## 参数校验

- 必填与格式：Bean Validation（`@NotNull`/`@Size`/`@Email` 等）在 DTO 上声明；分组用于创建/更新场景。
- 范围与枚举：数值范围、日期范围、集合大小；枚举用 `Enum`+自定义校验或 `Pattern` 约束字符串。
- 跨字段/跨表：在 Service 或 domain 中校验，可返回 422 与业务子码；避免在 Controller 写多步骤校验。

## 日志规范

- 操作日志：关键业务动作用结构化日志，含业务主键、操作人、结果。
- 错误日志：`error` 级别，含堆栈、traceId、关联 ID；敏感字段打码或脱敏（密码、Token、身份证等）。
- 审计日志：合规与权限相关操作落审计中间件或专用 appender，保留期限符合策略。
- **禁止** 在日志中输出完整 SQL 带明文密码或完整报文带 Token。

## 权限规范

- 认证：OAuth2/OIDC、JWT 或内部网关鉴权，与 **Spring Security 6** 基线配置一致；会话与 Token 续期规则文档化。
- 授权：方法级 `@PreAuthorize` 或 **RBAC** 角色/资源模型；**禁止** 在 Controller 手写分散 if-else 不纳入策略。
- 数据权限：在 Repository 层或 AOP/Specification 中注入租户/组织条件，**禁止** 在 SQL 中拼接不可审计的特判。
- 接口权限：与 OpenAPI/内部路由表对账，新接口默认需鉴权（显式放行的白名单列表管控）。

## 事务规范

- 边界：在 Service 层公共方法，默认**读多写一**的跨表一致同一事务；跨服务一致用**最终一致**与补偿/事务消息。
- 幂等：写接口使用幂等键、唯一约束、状态机**防止重复写**；对外回调验签+幂等表。
- 重试：仅对**可重试的瞬时失败**在基础设施层重试，业务冲突不重试为成功；记录重试次数与熔断。
- 回滚：默认回滚**运行时异常**与业务失败策略；有意的「不吞异常但业务不失败」须代码评审并文档说明。

## 测试规范

- 单元测试：Service/domain 用 JUnit 5 + Mockito；覆盖分支与业务规则。
- 集成测试：`@SpringBootTest`+Testcontainers/嵌入式 DB/分层切片；验证 Repository 与事务。
- 接口测试：`MockMvc` 或 `WebTestClient`，覆盖主路径、校验失败、鉴权失败。
- 验收标准：与 OpenAPI/契约测试对齐；**关键用例在 CI 必须通过**。

## Rule 生成要求

- **约束**：包分层、Controller 不含业务、Entity 不直接出参、事务在 Service 声明、安全默认开启。
- **禁止行为**：循环依赖、跨层直接访问 Mapper 绕过 Service（除非架构评审通过）、在 Controller 开启事务、日志泄露密钥。
- **验收标准**：`./mvnw test` 或 `gradle test` 通过；静态分析（如 SpotBugs/Checkstyle）不阻断时需在清单中列例外。

## Skill 生成要求

- **输入**：业务需求摘要、技术栈=Spring Boot、非功能约束（QPS/合规）。
- **步骤**：划分模块 → 定义 DTO/实体 → 实现 Service 与事务 → 暴露 API → 补充测试与文档。
- **输出**：可编译工程、OpenAPI/接口说明、**不含** 虚构第三方 URL。
- **异常处理**：在 Skill 中写清失败时回滚/告警/人工处理路径。

## Flow 生成要求

- **阶段**：需求/设计 → 实现 → 自测 → Code Review → 联调 → 上线检查。
- **门禁**：静态检查、测试、安全扫描、依赖 License 与漏洞检查。
- **状态流转**：任务从 Backlog 到 Done，缺陷从 Open 到 Verified。
- **异常出口**：阻塞项升级、回滚、hotfix 分支与合并策略。

## Manifest 推荐

- **推荐资产组合**：`springboot-base-rules`、`spring-data-jpa-或-mybatis-rules`、**OpenAPI 契约**、`dockerfile-jvm`、**观测性 sidecar/Agent**。
- **安装策略**：以 Boot 主版本为锚；依赖通过 BOM/Gradle 平台**统一**；**禁止** 在 Skill 中硬编码密钥与生产 URL。

## 禁止行为

- **禁止** 输出可运行的完整业务域源码长块作为「模板」**复制即上线** 而不经评审；允许高层伪代码与接口名。
- **禁止** 虚构不存在的**内部/外部** API 路径、认证方式、密钥与租户 ID。
- **禁止** 在文档/Skill 中要求提供或存储**生产密钥、证书私钥、数据库 root 密码**；使用占位符与密钥管理服务。

## 验收标准

- 仓库可构建、测试在 CI 执行且通过、接口与实现一致、敏感配置仅来自环境变量或密钥服务。
- 有 Runbook 或至少 README 中说明本地启动、**profile** 与**最小**依赖（DB/消息）。
