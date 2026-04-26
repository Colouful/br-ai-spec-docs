# 后端技术栈官方资料索引

## 用途

本文件用于帮助 AI 工程资产工厂识别后端技术栈官方资料来源。生成资产时，应优先遵循 Hub 资产契约、企业级后端工程标准和项目约束。

本文件主要服务于以下场景：

1. 后端 Rule 资产生成
2. 后端 Skill 资产生成
3. 后端 API 设计约束生成
4. 后端服务治理规则生成
5. 后端测试与验收标准生成
6. 后端安全、权限、事务、日志、监控相关资产生成

## 技术栈索引

### Java

- 官方文档：https://docs.oracle.com/en/java/
- 适用场景：Java 语言基础、标准库、JDK 行为。
- 使用说明：用于确认 Java 语言、JDK 标准库和运行时行为。

### Spring Boot

- 官方文档：https://spring.io/projects/spring-boot
- 参考文档：https://docs.spring.io/spring-boot/
- 适用场景：Java Web 应用、REST API、配置、自动装配、测试。
- 使用说明：用于确认 Spring Boot 应用配置、自动装配、Web 开发和测试实践。

### Spring Framework

- 官方文档：https://spring.io/projects/spring-framework
- 参考文档：https://docs.spring.io/spring-framework/reference/
- 适用场景：IoC、AOP、MVC、事务、验证。
- 使用说明：用于确认 Spring 核心容器、Web MVC、事务、验证和企业级应用基础能力。

### Spring Cloud

- 官方文档：https://spring.io/projects/spring-cloud
- 适用场景：微服务、服务治理、配置中心、网关、熔断、调用链路。
- 使用说明：用于确认 Spring Cloud 微服务生态能力和服务治理相关边界。

### NestJS

- 官方文档：https://docs.nestjs.com/
- 适用场景：Node.js 后端、模块、Controller、Provider、依赖注入、测试。
- 使用说明：用于确认 NestJS 模块化、依赖注入、控制器、服务和测试实践。

### Express

- 官方文档：https://expressjs.com/
- 适用场景：Node.js Web 服务、路由、中间件。
- 使用说明：用于确认 Express 路由、中间件和基础 Web 服务能力。

### FastAPI

- 官方文档：https://fastapi.tiangolo.com/
- 适用场景：Python API 服务、Pydantic、OpenAPI、异步接口。
- 使用说明：用于确认 FastAPI 路由、依赖注入、请求校验、OpenAPI 和异步接口能力。

### Django

- 官方文档：https://docs.djangoproject.com/
- 适用场景：Python Web 应用、ORM、Admin、认证、表单。
- 使用说明：用于确认 Django Web 应用、ORM、认证、Admin 和表单能力。

### Flask

- 官方文档：https://flask.palletsprojects.com/
- 适用场景：轻量 Python Web 服务。
- 使用说明：用于确认 Flask 路由、请求处理、扩展机制和轻量 Web 服务能力。

### Go

- 官方文档：https://go.dev/doc/
- 适用场景：Go 语言、并发、标准库、服务开发。
- 使用说明：用于确认 Go 语言、标准库、并发模型和服务开发基础能力。

### Gin

- 官方文档：https://gin-gonic.com/en/docs/（`https://gin-gonic.com/docs/` 会返回 404，请以带语言前缀的文档根路径为准）
- 适用场景：Go Web API、路由、中间件、参数绑定。
- 使用说明：用于确认 Gin 路由、中间件、参数绑定和 Web API 开发能力。

### Rust

- 官方文档：https://www.rust-lang.org/learn
- 适用场景：Rust 语言、类型安全、系统级服务。
- 使用说明：用于确认 Rust 语言学习入口、类型安全和系统级开发基础能力。

### Axum

- 官方文档：https://docs.rs/axum/
- 适用场景：Rust Web 服务、Router、Extractor、Tower 生态。
- 使用说明：用于确认 Axum 路由、Extractor、Handler 和 Tower 生态集成方式。

## 使用原则

1. 官方文档用于确认技术事实。
2. 资产正文必须转化为企业级工程约束。
3. 不输出源码级业务实现。
4. 不虚构框架能力。
5. 不确定时标记为“需要人工确认”。
6. 涉及认证、权限、事务、数据一致性、异步任务、接口兼容性时，必须提高风险等级。
7. 生成后端资产时，应补充接口契约、错误处理、日志、监控、测试和回滚要求。
8. 不得默认项目使用某个后端框架，除非项目上下文已经明确。
9. 不得生成真实数据库连接串、密钥、Token 或生产配置。
10. 涉及写操作、删除操作、批量操作、权限变更、资金和订单相关逻辑时，必须设置验收标准和回滚方案。

## 链接校验摘要

| 资料项 | 链接 | 校验结果 | 备注 |
|---|---|---|---|
| Java | https://docs.oracle.com/en/java/ | 已确认：官方资料入口正确 | HTTP 200，Oracle 官方文档域 |
| Spring Boot | https://spring.io/projects/spring-boot | 已确认：官方资料入口正确，但存在自动跳转 | 最终 URL 带尾部斜杠，仍为 spring.io 官方项目页 |
| Spring Boot Reference | https://docs.spring.io/spring-boot/ | 已确认：官方资料入口正确 | HTTP 200，Spring 官方参考文档站 |
| Spring Framework | https://spring.io/projects/spring-framework | 已确认：官方资料入口正确，但存在自动跳转 | 项目页，官方 spring.io 域 |
| Spring Framework Reference | https://docs.spring.io/spring-framework/reference/ | 已确认：官方资料入口正确 | HTTP 200，Spring 官方参考文档站 |
| Spring Cloud | https://spring.io/projects/spring-cloud | 已确认：官方资料入口正确，但存在自动跳转 | 官方项目页 |
| NestJS | https://docs.nestjs.com/ | 已确认：官方资料入口正确 | HTTP 200，Nest 官方文档 |
| Express | https://expressjs.com/ | 已确认：官方资料入口正确 | HTTP 200 |
| FastAPI | https://fastapi.tiangolo.com/ | 已确认：官方资料入口正确 | HTTP 200，作者/项目维护的官方文档站 |
| Django | https://docs.djangoproject.com/ | 已确认：官方资料入口正确，但存在自动跳转 | 会跳转至带版本号的文档根（如 en/6.x/），属官方默认行为 |
| Flask | https://flask.palletsprojects.com/ | 已确认：官方资料入口正确，但存在自动跳转 | 跳转至 stable 等官方路径 |
| Go | https://go.dev/doc/ | 已确认：官方资料入口正确 | HTTP 200，go.dev 官方 |
| Gin | https://gin-gonic.com/en/docs/ | 已确认：官方资料入口正确 | 建议优先使用本路径；`/docs/` 无语言前缀为 404 |
| Rust | https://www.rust-lang.org/learn | 已确认：官方资料入口正确，但存在自动跳转 | 校验时跳转至 rust-lang.org/learn/ |
| Axum | https://docs.rs/axum/ | 已确认：官方资料入口正确，但存在自动跳转 | docs.rs 官方 crate 文档，跳转至 latest 版本页 |

*校验环境：本仓库代理网络下以 `curl -L` 拉取；若你方网络策略封禁部分域名，以本地浏览器结果为准。*
