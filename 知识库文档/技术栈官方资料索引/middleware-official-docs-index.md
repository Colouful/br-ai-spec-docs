# 中间件官方资料索引

## 用途

本文件用于帮助 AI 工程资产工厂识别常见中间件的官方资料来源。生成资产时仅用于技术事实参考，不替代项目实际部署规范。

本文件主要服务于以下场景：

1. 数据库相关 Rule / Skill 资产生成
2. 缓存、消息队列、搜索、网关相关资产生成
3. 容器化和部署相关资产生成
4. 中间件接入规范生成
5. 运维风险、权限风险、数据一致性风险识别
6. 测试、回滚和可观测性要求生成

## 中间件索引

### MySQL

- 官方文档：https://dev.mysql.com/doc/
- 适用场景：关系型数据库、事务、索引、SQL 规范。
- 使用说明：用于确认 MySQL SQL、事务、索引、存储引擎和数据库行为。

### PostgreSQL

- 官方文档：https://www.postgresql.org/docs/
- 适用场景：关系型数据库、事务、索引、JSON、扩展能力。
- 使用说明：用于确认 PostgreSQL SQL、事务、索引、JSON、扩展和数据库行为。

### Redis

- 官方文档：https://redis.io/docs/
- 适用场景：缓存、分布式锁、限流、会话、队列。
- 使用说明：用于确认 Redis 数据结构、缓存模式、过期策略、持久化和高可用相关能力。

### MongoDB

- 官方文档：https://www.mongodb.com/docs/
- 适用场景：文档数据库、聚合查询、索引。
- 使用说明：用于确认 MongoDB 文档模型、查询、聚合、索引和数据建模方式。

### Elasticsearch

- 官方文档：https://www.elastic.co/guide/
- 适用场景：搜索、日志检索、全文索引。
- 使用说明：用于确认 Elasticsearch 索引、查询 DSL、全文检索、聚合和集群能力。

### Kafka

- 官方文档：https://kafka.apache.org/documentation/
- 适用场景：消息队列、事件流、异步解耦。
- 使用说明：用于确认 Kafka Topic、Producer、Consumer、Consumer Group、Offset 和事件流处理能力。

### RabbitMQ

- 官方文档：https://www.rabbitmq.com/docs
- 适用场景：消息队列、交换机、路由、消费确认。
- 使用说明：用于确认 RabbitMQ Exchange、Queue、Routing、Ack、重试和死信队列相关能力。

### Nginx

- 官方文档：https://nginx.org/en/docs/
- 适用场景：反向代理、静态资源、负载均衡、网关。
- 使用说明：用于确认 Nginx 反向代理、负载均衡、静态资源、TLS 和网关配置能力。

### Docker

- 官方文档：https://docs.docker.com/
- 适用场景：容器化、镜像、Compose、部署环境。
- 使用说明：用于确认 Docker 镜像、容器、Dockerfile、Compose 和容器化实践。

### Kubernetes

- 官方文档：https://kubernetes.io/docs/
- 适用场景：容器编排、Deployment、Service、Ingress、ConfigMap、Secret。
- 使用说明：用于确认 Kubernetes 工作负载、服务暴露、配置、密钥、扩缩容和容器编排能力。

## 使用原则

1. 只作为中间件事实参考。
2. 生成资产时必须询问或标记项目实际版本。
3. 不生成生产配置密钥。
4. 不要求用户提供真实连接串、账号、密码。
5. 涉及数据库、权限、发布、运维变更时，默认标记为较高风险。
6. 涉及缓存、消息队列、搜索、容器、网关时，必须关注容量、稳定性、幂等性、回滚和可观测性。
7. 不得假设项目已启用某个中间件，除非项目上下文明确说明。
8. 涉及数据库 Schema、索引、数据迁移、消息重放、缓存失效、网关路由变更时，必须输出风险说明和回滚方案。
9. 涉及 Kubernetes Secret、数据库密码、API Key、Token 时，只能描述占位符和安全原则，不得写入真实值。
10. 对生产环境变更，必须建议经过审批、灰度、监控和回滚验证。

## 链接校验摘要

| 资料项 | 链接 | 校验结果 | 备注 |
|---|---|---|---|
| MySQL | https://dev.mysql.com/doc/ | 已确认：官方资料入口正确 | HTTP 200，MySQL/Oracle 官方文档域 |
| PostgreSQL | https://www.postgresql.org/docs/ | 已确认：官方资料入口正确 | HTTP 200，社区官方文档站 |
| Redis | https://redis.io/docs/ | 已确认：官方资料入口正确，但存在自动跳转 | 跳转至 `/docs/latest/`，属官方内容组织方式 |
| MongoDB | https://www.mongodb.com/docs/ | 已确认：官方资料入口正确 | HTTP 200，厂商官方文档 |
| Elasticsearch | https://www.elastic.co/guide/ | 已确认：官方资料入口正确，但存在自动跳转 | 跳转至 index.html，仍属 Elastic 官方引导页 |
| Kafka | https://kafka.apache.org/documentation/ | 已确认：官方资料入口正确 | HTTP 200，Apache 项目官方文档 |
| RabbitMQ | https://www.rabbitmq.com/docs | 已确认：官方资料入口正确 | HTTP 200，Erlang Solutions / 项目官方文档站 |
| Nginx | https://nginx.org/en/docs/ | 已确认：官方资料入口正确 | HTTP 200，nginx.org 官方 |
| Docker | https://docs.docker.com/ | 已确认：官方资料入口正确 | HTTP 200，Docker 官方文档 |
| Kubernetes | https://kubernetes.io/docs/ | 已确认：官方资料入口正确，但存在自动跳转 | 跳转至 docs 首页，官方 kubernetes.io 域 |

*生产环境以集群实际版本与厂商发行说明为准；上表不替代变更评审。*
