# 前后端技术栈全景图

我按**前端生态**、**后端生态**、**中间件与基础设施**、**代码规范**四个维度为你系统梳理。

---

## 一、前端技术生态

### 1. UI 框架 / 库
| 技术 | 定位 | 官方文档 |
|------|------|----------|
| **React** | 声明式 UI 库 | [react.dev](https://react.dev) |
| **Vue** | 渐进式框架 | [vuejs.org](https://vuejs.org) |
| **Angular** | 企业级全功能框架 | [angular.dev](https://angular.dev) |
| **Svelte** | 编译型框架（无虚拟 DOM） | [svelte.dev](https://svelte.dev) |
| **SolidJS** | 响应式细粒度更新 | [solidjs.com](https://www.solidjs.com) |
| **Preact** | React 轻量替代 | [preactjs.com](https://preactjs.com) |

### 2. 全栈 / 元框架（Meta Framework）
| 技术 | 基于 | 特点 |
|------|------|------|
| **Next.js** | React | SSR/SSG/ISR、App Router、Edge Runtime |
| **Nuxt** | Vue | 约定优于配置、自动导入 |
| **Remix** | React | 渐进增强、Web 标准优先 |
| **SvelteKit** | Svelte | 全栈、适配器模式 |
| **Astro** | 框架无关 | 岛屿架构、内容站点首选 |
| **Qwik** | 独立 | 可恢复性（Resumability）、零 JS 启动 |

### 3. 构建工具
| 技术 | 定位 |
|------|------|
| **Vite** | 下一代前端构建工具（ESM + Rollup） |
| **Webpack** | 老牌打包器，生态最丰富 |
| **Rollup** | 库打包首选 |
| **esbuild** | Go 编写，极速编译 |
| **Turbopack** | Webpack 继任者（Rust 编写） |
| **Rspack** | 字节出品，Webpack 兼容的高性能替代 |
| **Parcel** | 零配置打包器 |
| **SWC** | Rust 编写的 JS/TS 编译器 |

### 4. 状态管理与数据获取
| 技术 | 场景 |
|------|------|
| **Redux / Redux Toolkit** | 全局状态 |
| **Zustand** | 轻量状态 |
| **Pinia** | Vue 官方推荐 |
| **MobX** | 响应式编程 |
| **Jotai / Recoil** | React 原子化状态 |
| **TanStack Query (React Query)** | 服务端状态管理 |
| **SWR** | Vercel 出品的数据获取 |

### 5. UI 组件库 & CSS 方案
| 技术 | 生态 |
|------|------|
| **Ant Design** | React 企业级 |
| **Element Plus** | Vue 3 企业级 |
| **Material-UI (MUI)** | React Material Design |
| **Chakra UI** | React 易定制 |
| **shadcn/ui** | 无依赖、可复制组件 |
| **Tailwind CSS** | 原子化 CSS |
| **UnoCSS** | 即时原子化 CSS |
| **Styled Components / Emotion** | CSS-in-JS |

### 6. 测试工具
| 技术 | 用途 |
|------|------|
| **Jest** | 单元测试 |
| **Vitest** | Vite 原生测试 |
| **Cypress** | E2E 测试 |
| **Playwright** | 微软出品 E2E |
| **Testing Library** | 组件测试 |

---

## 二、后端技术生态

### 1. Java
| 技术 | 定位 |
|------|------|
| **Spring Boot** | 事实标准微服务框架 |
| **Spring Cloud** | 微服务全家桶 |
| **Spring Cloud Alibaba** | 阿里微服务方案 |
| **Quarkus** | 云原生、低内存、GraalVM 原生镜像 |
| **Micronaut** | AOT 编译、低启动时间 |
| **Vert.x** | 事件驱动、响应式 |
| **Jakarta EE** | 企业级标准 |

### 2. Node.js
| 技术 | 定位 |
|------|------|
| **NestJS** | 企业级、Angular 风格、TypeScript 优先 |
| **Express** | 最轻量、最流行 |
| **Fastify** | 高性能、低开销 |
| **Koa** | Express 原班人马，async/await 友好 |
| **Egg.js** | 阿里出品，企业级 |
| **Hapi** | 配置驱动 |
| **AdonisJS** | Laravel 风格的 Node 框架 |

### 3. Python
| 技术 | 定位 |
|------|------|
| **FastAPI** | 高性能、异步、自动生成 OpenAPI 文档 |
| **Django** | 全功能、ORM 内置、管理后台 |
| **Flask** | 微框架、灵活 |
| **Tornado** | 异步、长连接 |
| **Celery** | 分布式任务队列 |

### 4. Go
| 技术 | 定位 |
|------|------|
| **Gin** | 高性能、最流行 |
| **Echo** | 极简、高性能 |
| **Fiber** | Express 风格、基于 fasthttp |
| **Beego** | 全功能、类 Django |
| **Iris** | 全功能、性能极致 |
| **Go-zero** | 微服务框架（go-zero 出品） |
| **GORM** | ORM 库 |

### 5. Rust
| 技术 | 定位 |
|------|------|
| **Actix-web** | 高性能、Actor 模型 |
| **Axum** | Tokio 生态、类型安全路由 |
| **Rocket** | 易用、声明式 |
| **Warp** | 组合式过滤器 |
| **Tauri** | 桌面应用（替代 Electron） |

### 6. 其他语言
| 语言 | 代表框架 |
|------|----------|
| **PHP** | Laravel, Symfony, Yii, ThinkPHP |
| **Ruby** | Ruby on Rails, Sinatra |
| **C# (.NET)** | ASP.NET Core, Minimal API |
| **Kotlin** | Ktor, Spring Boot |

---

## 三、中间件与基础设施

### 1. 消息队列
| 技术 | 特点 |
|------|------|
| **Apache Kafka** | 高吞吐、持久化、流处理 |
| **RabbitMQ** | 成熟、多协议、灵活路由 |
| **RocketMQ** | 阿里出品、金融级可靠 |
| **Apache Pulsar** | 云原生、分层存储 |
| **NATS** | 轻量、高性能 |

### 2. 缓存
| 技术 | 用途 |
|------|------|
| **Redis** | 内存 KV、数据结构丰富 |
| **Memcached** | 纯 KV、简单高速 |
| **Caffeine** | Java 本地缓存 |
| **Dragonfly** | Redis 兼容、多线程 |

### 3. 数据库与 ORM
| 类型 | 技术 |
|------|------|
| 关系型 | MySQL, PostgreSQL, MariaDB, SQL Server, Oracle |
| NoSQL | MongoDB, Cassandra, Couchbase |
| 时序 | InfluxDB, TimescaleDB, TDengine |
| 图数据库 | Neo4j, NebulaGraph |
| 搜索引擎 | Elasticsearch, OpenSearch, Solr |
| 国产 | TiDB, OceanBase, PolarDB, GaussDB |

### 4. API 网关
| 技术 | 特点 |
|------|------|
| **Nginx / OpenResty** | 高性能反向代理 |
| **Kong** | 基于 OpenResty、插件丰富 |
| **Spring Cloud Gateway** | Spring 生态原生 |
| **Envoy** | 云原生、Service Mesh 数据面 |
| **Traefik** | 云原生、自动服务发现 |

### 5. 服务治理
| 技术 | 用途 |
|------|------|
| **Nacos** | 服务发现 + 配置中心 |
| **Consul** | 服务发现、健康检查 |
| **Eureka** | Netflix 服务注册 |
| **ZooKeeper** | 分布式协调 |
| **etcd** | Kubernetes 默认 KV 存储 |

### 6. 可观测性
| 技术 | 用途 |
|------|------|
| **Prometheus** | 时序指标采集 |
| **Grafana** | 可视化仪表盘 |
| **SkyWalking** | APM、分布式追踪 |
| **Zipkin / Jaeger** | 分布式链路追踪 |
| **ELK (Elasticsearch + Logstash + Kibana)** | 日志分析 |
| **Loki** | 轻量日志聚合 |

### 7. 容器与编排
| 技术 | 用途 |
|------|------|
| **Docker** | 容器化 |
| **Kubernetes (K8s)** | 容器编排标准 |
| **Helm** | K8s 包管理 |
| **Istio** | Service Mesh |
| **Harbor** | 镜像仓库 |

### 8. CI/CD & DevOps
| 技术 | 用途 |
|------|------|
| **Jenkins** | 老牌 CI/CD |
| **GitLab CI** | 与 GitLab 集成 |
| **GitHub Actions** | 与 GitHub 集成 |
| **ArgoCD** | GitOps 持续交付 |
| **Tekton** | K8s 原生 CI/CD |

---

## 四、代码规范与风格指南

| 规范名称 | 语言 | 链接 |
|----------|------|------|
| **Google Java Style Guide** | Java | [google.github.io/styleguide/javaguide.html](https://google.github.io/styleguide/javaguide.html) |
| **Google TypeScript Style Guide** | TypeScript | [google.github.io/styleguide/tsguide.html](https://google.github.io/styleguide/tsguide.html) |
| **Google Python Style Guide** | Python | [google.github.io/styleguide/pyguide.html](https://google.github.io/styleguide/pyguide.html) |
| **Airbnb JavaScript Style Guide** | JavaScript | [github.com/airbnb/javascript](https://github.com/airbnb/javascript) |
| **Alibaba Java 开发规约** | Java | [github.com/alibaba/p3c](https://github.com/alibaba/p3c) |
| **Oracle Code Conventions** | Java | 经典规范 |
| **PEP 8** | Python | [peps.python.org/pep-0008](https://peps.python.org/pep-0008/) |
| **Standard Go Project Layout** | Go | [github.com/golang-standards/project-layout](https://github.com/golang-standards/project-layout) |
| **Rust API Guidelines** | Rust | [rust-lang.github.io/api-guidelines](https://rust-lang.github.io/api-guidelines/) |

---

