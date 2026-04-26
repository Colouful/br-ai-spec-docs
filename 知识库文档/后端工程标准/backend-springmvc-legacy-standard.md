# Spring MVC（传统 XML / 注解式）后端工程标准

> 面向存量 Servlet + Spring MVC 与 XML 或早期 JavaConfig 并存的**遗留**系统。新系统优先 Spring Boot 标准。

## 适用技术栈

- **语言**：Java 8+（以现场 JDK/容器基线为准；向上迁移时单独出迁移项）。
- **框架**：Spring Framework（MVC/Context/tx）、Servlet 容器（Tomcat/WebLogic 等视部署环境）。
- **配置**：`web.xml`+XML Bean、或 JavaConfig+`DispatcherServlet` 混用；部分模块无 Boot 可执行 jar。
- **构建**：多数为 Maven/Gradle 打 **WAR**；**运行环境**为外置或嵌入式 Servlet 容器，通过 JNDI/系统属性/属性文件配置。

## 适用项目类型

- **application**：WAR 部署的 Web 应用，可能含多模块 EAR/多 WAR 协作。
- **service**：**单体** 或按包划分的**逻辑服务**，物理部署仍为一应用。
- **microservice**：较少通过纯 MVC 新建；若拆分需明确协议、数据边界与**兼容期**双写策略。
- **monorepo**：多模块时保持 **API 与实现模块** 的依赖方向，禁止**反向**依赖 WAR 聚合模块到纯库。

## 项目结构规范

- **Controller 层**（`@Controller` / `@RestController`）：`*.controller` 或 `web` 包，仅做请求映射与**薄**适配，不写复杂业务。
- **Service 层**（`*.service`）：`@Service` 业务用例、事务在实现类**接口或类**上声明，与**旧** XML `<tx:advice>` 不冲突——以**单一路径**为权威（评审固定）。
- **Repository / DAO**：`hibernate` 模板、`JdbcTemplate`、iBatis/MyBatis 的 `Mapper`，统一放 `dao`/`repository` 包，与 Entity 的映射在 XML/注解中。
- **DTO/VO/Entity**：Struts/早期 FormBean 如仍存在，**新接口** 一律不用；Entity 为 Hibernate/POJO，**禁止** 与 JSP/前端模型混包。
- **config**：`spring-*.xml` 或 `WebMvcConfigurer` 实现类、拦截器、转换器、全局异常**集中**配置。

## Controller 规范

- 职责：URL 映射、参数解析（`@RequestParam`/`@PathVariable`）、视图名或**JSON 输出**、文件下载。
- 参数：为每个接口建独立**命令对象**或 DTO，避免在方法签名上堆积多参数；旧接口改造时**增量**加 DTO。
- 响应：REST 用统一 JSON 体；JSP/视图**逐步退出** 路径需在清单登记；**禁止** 在 Controller 中直接 `getWriter()` 打异常信息给浏览器。
- 状态码与错误体：能改为 `@ResponseStatus`/`@ExceptionHandler` 的**新代码** 建议统一；遗留错误页由 `web.xml`+error-page 管理时，API 新入口与页面入口**分路径** 避免行为混淆。
- 校验边界：优先 **Bean Validation 2.0+** 若容器支持；否则在 Service 层**显式** 校验，并在文档写清，避免**双头** 校验逻辑。

## Service 规范

- 业务编排：**接口+实现** 保持与 XML/注解引用一致，避免**同名** Service 在多处定义。
- 事务边界：XML 声明式与 `@Transactional` **只选一种** 为新增代码权威；`readOnly`、**传播/隔离** 在代码评审必查；**禁止** 在 private 方法上**误以为** 事务生效。
- 领域逻辑：在 Service 中保持**可测** 方法抽取；**禁止** 在 DAO 中写**跨表** 业务条件而不经 Service 命名自解释。

## DTO / VO / Entity 规范

- **Request/Command DTO**：与表单或 JSON 一一对应；不继承带延迟加载的** Hibernate 代理** 类型做输入。
- **Response/VO**：面向调用方，字段稳定；JSP 用的 Model 不当作 API 契约的**源** 版本。
- **Entity**：Hibernate/ORM 管理，**禁止** 在 Controller/Interceptor 中直接修改**游离** 实体**跨请求** 传递。

## Repository / Mapper 规范

- DAO/Mapper 仅数据访问，返回 Entity/Row DTO/基础类型；Hibernate **Session** 生命周期在 OpenSessionInView 关闭后**不** 依赖**懒加载** 于 Controller。
- 禁止在 JSP/Tag 中发起**隐式** N+1，除非已列入性能白名单与缓存策略。
- 禁止在 Controller 中拼 SQL 或**直接** 拿 `DataSource`（**审计类** 与排障**临时** 脚本需走单独流程）。

## 异常处理

- **ControllerAdvice/HandlerExceptionResolver**：统一 JSON 与页面错误，与 `web.xml` error 配置**不冲突**。
- 业务异常：可区分业务可预期失败与系统失败；**禁止** 在 Filter 中吞**所有** 异常不记录。
- 参数异常与绑定错误：在 REST 中返回 400+字段错误；JSP 返回**可访问** 的错误提示需符合安全**不** 泄露**堆栈**。
- 外部依赖：超时、熔断（若有 Resilience 或**容器** 层机制）在日志中**可** 关联**请求** ID。

## 参数校验

- 若 Bean Validation 可用，在 DTO/参数对象上**声明** 约束；否则 Service **入口** 校验并抛**明确定义** 异常。
- 范围与枚举、跨字段、跨表唯一性在 Service/DAO 协作处**有单点** 入口，**禁止** 在多处复制粘贴校验。

## 日志规范

- 使用**一致** 日志门面（如 SLF4J），`log4j1` **迁移** 计划单列；**禁止** `System.out` 在**生产** 路径上。
- 操作与审计：同 Spring Boot 标准，注意**老** 日志**格式** 与**解析** 管道；敏感信息脱敏。

## 权限规范

- Spring Security 或**容器/网关** 认证在 **Filter/Interceptor** 层；URL 与角色映射在**一处** 维护，**避免** 多处**重复** 列表。
- 方法级安全若**未** 启用，则**在 Service** 显式鉴权，并在清单登记**例外** 接口（公开、健康、静态资源）。

## 事务规范

- 与 Service 中 **REQUIRED** 为默认、只读、传播行为一致；**大事务** 分片；**与 EJB/外部** 两阶段 若存在，由**专家** 评审**边界**。

## 测试规范

- 单元测试：JUnit+Mock 隔离 DAO；**集成测试** 可用 `@ContextConfiguration`+嵌入式 DB/内存容器（若可行）。
- 回归：**关键** 路径有**可重复** 的自动化，与**手测** 清单**互补** 而非替代；**修 bug** 必**补** 测试**防回归**。

## Rule 生成要求

- **约束**：分层、事务单一路径、禁止懒加载在 API 上裸奔、**禁止** 在 Filter 中写业务**分支**。
- **禁止行为**：Controller 大事务、DAO 中业务规则、未文档化**全局** 异常**吞没**。
- **验收标准**：WAR 可**构建**、**冒烟** 用例**通过**、**已知** 技术债有**登记** 与**负责人**。

## Skill 生成要求

- **输入**：遗留**约束**、容器类型、**禁止** 大改**模块** 列表、接口**契约**。
- **步骤**：**最小** 范围改 → 补测试/清单 → 评审**事务** 与**异常** 路径 → **不** 虚构**部署** 参数。
- **输出**：变更说明、**不** 含**生产** 密钥、**不** 伪造**不** 存在**的** 中间件** 版本**。

## Flow 生成要求

- **阶段**：**评估** 影响 → 实现 → **回归** → **UAT/上线窗口**（**窗口** 外**禁止** **无** 回滚**方案** 发布）。
- **门禁**：**变更单**、**回滚** 脚本/制品、**监控** 看板**就绪**。
- **状态流转**：**缺陷** 与**变** 更**关联** **版本**、**不** 混在**一个** 分支**无** 目的** 合并**。

## Manifest 推荐

- **推荐资产组合**：`springmvc-legacy-coding-rules`、**依赖与 CVE** 基线、**JVM/容器** 基线、**排障** Runbook。
- **安装策略**：**不** 自动化**强推** 与**现场** **JVM/容器** **不** 兼容**的** 库** 版本**；**升级** 走**单独** 任务** 与** 验证** 列表**。

## 禁止行为

- **禁止** 在未经评审下**大改** **XML/Bean** 顺序**导致** **生产** 行为**变** 更**无法** 解释**。
- **禁止** 虚构**中间件/容器** 特性** 与** **内部** 路由** 规则**。
- **禁止** 索取**与** 任务**无关** 的** 生产** 凭据**。

## 验收标准

- 构建**可** 复现、**主流程** 可**验证**、**重大** 风险有**回滚** 与**值** 班**约定**、**不** 引入**新** 环**状** 依赖**。
