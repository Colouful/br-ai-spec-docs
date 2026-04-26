# Python FastAPI 后端工程标准

## 适用技术栈

- 语言：Python 3.11+（以团队 LTS/最低版本为准），`pyproject.toml` 或 `requirements` 在 CI 中可复现；类型提示推荐 `mypy` 或 `pyright` 与 Ruff/Black 等基线。
- 框架：FastAPI；`Pydantic` v2 用于配置与请求/响应模型；依赖注入用 `Depends` 组织分层；必要时 `APIRouter` 分模块。
- 构建与运行：Uvicorn、Gunicorn+Uvicorn worker 等；`uv`、Poetry 或 `pip-tools` 锁版本；**运行环境**为容器或进程管理器，环境变量分环境注入。
- 可观测性：结构日志、OpenTelemetry 或等价的 request id、与指标/追踪对接。

## 适用项目类型

- application：独立 `main` 或 `app` 工厂，对外暴露 HTTP/健康检查/指标。
- service：单体或按包划分子域，单进程多路由；大项目用 `routers` 包分域。
- microservice：多部署单元，通过 API 或消息解耦，不共享可写进程内状态。
- monorepo：多包时（如 `src/xxx`、shared lib）保持依赖方向，共享库不反向依赖应用包。

## 项目结构规范

- `routers` 或 `api`：路由、依赖声明、**不** 写长业务逻辑，仅编排与调 Service。
- `services` 或 `application`：用例、事务、外部 HTTP/消息/缓存 调用顺序；可再拆 `domain`（纯逻辑）。
- `repositories` 或 `adapters`：SQLAlchemy/SQLModel/tortoise 等，或原生命令封装，仅数据通道。
- `models` 或 `db`：表 ORM/映射；`schemas`（Pydantic）**仅** API 与配置契约，不混用为持久化对外的**唯一**真相（除非有明确 DTO 映射层）。
- `core`：配置、安全、DB 会话/引擎、限流、异常处理器集中定义。

## Controller 规范

- 路由函数保持短小：依赖注入、调用 Service、返回 Pydantic 模型或 `Response`。
- 入参用 `Path` / `Query` / `Body` 对应独立 `schema` 类，列表与分页/游标一致。
- 出参用响应 schema 或 `JSONResponse`；统一 `HTTPException` 与全局 `exception_handler` 的错误体，客户端不读堆栈。
- 状态码在路径装饰器与业务异常中**一致**可预测；`201`+`Location` 用于创建。业务可预期错误须文档约定（4xx/5xx+子码 或 200+业务 code，二选一并贯彻）。
- 简单校验在 Pydantic 的 `Field` 与 `model_validator`；资源级与跨表规则在 Service/领域。

## Service 规范

- 用例方法接收纯数据或 DTO，返回 DTO/领域结果；在 Service 中管理**数据库会话/事务**（`session` context、commit/rollback）。
- 不将 ORM 实体长期泄露到 API 层外；对外转换在 Service 或独立 mapper。
- 外部调用加超时、重试策略与熔断/降级在配置或**独立** 客户端类中，不在路由里写裸 `httpx` 大段。

## DTO / VO / Entity 规范

- 请求/响应、列表项、Webhook 体各自定义 Pydantic 模型，命名清晰（如 `*Create`、`*Read`、`*Public`）。
- ORM/表模型在 `db` 包，**禁止** 直接把 ORM 对象序列化为 API 默认（除非有 `from_attributes`+显式字段与评审）。
- 内部分页、Job 等可用内部 NamedTuple/dataclass，不进入 OpenAPI 文档时标记清楚。

## Repository / Mapper 规范

- 查询、聚合、行映射在 `repository` 中；`router` **禁止** 直接 `session.execute` 大段 SQL（**除非** 明确评审的报表模块）。
- **禁止** 在数据层写**业务**条件分支不反映在与 Service 同名的可测用例中；N+1 用 `selectinload`、子查询等显式策略。

## 异常处理

- 全局 `app.exception_handler` 覆盖可预期与不可预期异常；统一 `request_id` 与**不** 泄露内部实现细节给客户端。
- 业务用自定义异常类 + 映射为 HTTP+body；`HTTPException` 的 `detail` 不暴露**敏感** 内部错误。
- 外呼失败可包装为**可** 重试/不可 重试，日志带上游名与**脱敏** 的关联 id。

## 参数校验

- 必填、类型、范围、长度、模式、日期、枚举、嵌套、列表、联合类型在 Pydantic；跨字段在 `field_validator`/`model_validator` 或领域函数。
- 与数据库/唯一约束冲突在 Service/Repository 捕获，转为**文档化** 的 409/422 等，避免裸 `500`。

## 日志规范

- `structlog` 或标准 `logging` 的 JSON/键值格式；`request_id` 贯穿。密码、Token、全量 PII 不打明文。
- 审计操作单独**标识** 或**落地** 到可检索存储，留痕周期符合政策。

## 权限规范

- 认证/授权用依赖（如 `get_current_user`、`require_roles`、OAuth2/ OIDC 集成）；在路由或依赖**一处** 声明，不复制粘贴 if。
- 数据权在查库时**注入** 租户/组织；禁止在**多处** 手写不审计的特判 `WHERE`。
- 服务间 mTLS/服务 Token，轮换有 Runbook。

## 事务规范

- 在 Service 或 `get_db` 的上下文中**明确** 事务；读多可 `read` session，写**短** 事务。不在路由里随意 `commit` 散布。
- 冪等键/唯一键；分布式用 Saga/Outbox，不默认 XA。
- 重试仅对**瞬时** 可重试错误，写接口重试有冪等保障。

## 测试规范

- 单元：pytest，mock 掉 repository 与 httpx 客户端，覆盖**领域** 与**分支**。
- 集成：`TestClient`+内存或 Testcontainers 数据库；**迁移** 与生产一致**策略** 或**等价** 子集。
- 契约/快照：对 OpenAPI 或**关键** 响应对照；Pact 等可选。CI 中 `pytest`+lint+类型 必过**或** 显式**豁免** 列表。

## Rule 生成要求

- 约束：Pydantic 在边界、路由薄、**禁止** `import *` 污染、敏感配置**仅** 环境变量/密钥管、**禁止** `print` 在生产路径。
- 禁止行为：路由内长事务、多处不一致校验、在日志中**打印** 密钥与**完整** Token。
- 验收标准：CI 绿、OpenAPI 可生成且与**实现** 对齐、**依赖** 漏洞/许可证**不** 低于**门** 槛 或 有**例外** 单。

## Skill 生成要求

- 输入：功能范围、NFR、现有 Pydantic schema/错误码表、部署约束。
- 步骤：定义 `schemas` 与 `routers` 契约；实现 `services`+`repositories`；挂全局中间件/异常/认证；单测+集成+文档；不含虚构外部 URL。
- 输出：可 `uvicorn` 启动的模块结构、**不含** 密钥 的 `.env.example` 与 Runbook 片段、异常与**补偿** 说明。
- 异常：失败**回** 滚/消息重试/人工对账/死信 的**边界**。

## Flow 生成要求

- 阶段：OpenAPI/模型评审、实现、自测、Code Review、分环境发布、可观测**验收**、压测/故障**演练**。
- 门禁：Ruff/Black、pytest、mypy（若开启）、SAST/依赖 扫描、迁移**在** 流水线**有** 策略。
- 状态：版本、变更单、与缺陷/发布 关联；配置与 Schema **协同** 演进。
- 异常：回滚、**只** 读/降级、补偿任务、**人工** 对账 出口。

## Manifest 推荐

- 资产：FastAPI 与 Pydantic 基线**规则**、OpenAPI 导出/校验 脚本、Gunicorn+Uvicorn **Docker**、**OTel** 侧**车** 或 进程 内 导出。
- 安装：在 `pyproject` **锁** 住 FastAPI/Starlette/Pydantic 大 版本**范围** 与 最低 Python；不 在 文档 中 写 死 私有 PyPI 凭据。

## 禁止行为

- 禁止将大段可直接用于上线的业务实现作为唯一交付物且未经评审。禁止虚构不存在的内部服务 URL、认证方式与租户模型。禁止在文档中索取或固化生产密钥、证书私钥与数据库高权限凭据；使用占位符与密钥管理服务说明。

## 验收标准

- 可复现执行安装、测试与运行；配置项清单与密钥来源分离。API 行为可用自动化测试与 OpenAPI/文档相互验证。敏感信息不入业务库、不出现在未脱敏的明文日志中。
