# Next.js 前端工程标准

## 适用技术栈

- **语言**：TypeScript 为默认；`strict` 建议开启；`next-env.d.ts` 不手改，由工具生成维护。
- **框架与运行时**：Next.js 当前组织采用的稳定主版本（App Router 为推荐方向，Pages Router 存量维护需单独约定）；**React 服务端/客户端组件边界**须遵守 `use client`/`server` 分工。
- **构建工具**：`next` 内建（Webpack 或 Turbopack，依版本与配置）；部署目标（Node/Edge/静态）与**运行时**（serverless、容器等）在文档中明确。
- **常见 UI 与数据**：可配合 Tailwind、shadcn/ui、Radix、MUI 等；数据获取在 App Router 下以 `fetch`+缓存语义、`server actions` 或 BFF/Route Handlers 为准；与 TanStack Query 搭配时注意 SSR/水合与缓存一致性。

## 适用项目类型

- **多页与混合渲染站点**：需要 SEO、流式、ISR/SSG 的站点与类 CMS 项目。
- **BFF/全栈同仓**：`app/api` 或 Route Handlers 承载轻量 BFF 时，须与鉴权、限流、日志和下游服务契约写清。
- **Monorepo**：Next 应用可位于 `apps/web`，与共享 `packages/ui`、设计 Token、类型包协同；`transpilePackages` 与 TS project references 按 turborepo/ nx 等规范配置。

## 目录结构规范

- **App Router 推荐**：`app/` 下以路由段组织 `layout.tsx`、`page.tsx`、`loading.tsx`、`error.tsx`；`route.ts` 仅作 API/代理；`components` 可放 `app/.../components`（就近）与根 `components`（共享）分层的约定须在团队内统一。
- **资产与内容**：`public` 为静态；`app` 内可共置 `favicon` 等；内容优先 MDX/远程 CMS 的边界写清。
- **模块边界**：`features` 竖切、或按 `lib/xxx` 分域；禁止 `app` 路由间随意跨越引用导致循环与隐式边依赖；**服务端模块不得被客户端包意外打包**（避免在 client 中 import 仅该在 server 使用的模块，必要时拆包与 `import type`）。

## 组件规范

- **职责**：`Server Components` 做数据取与零交互展示；`Client Components` 承担交互、浏览器 API、useEffect 等。默认在 App Router 下**尽可能 server-first**。
- **命名**：与 React 习惯一致，PascalCase；hooks 在 client 组件或 client 子模块中定义；`server` 与 `client` 模块文件命名/目录约定团队统一（如 `*.client.tsx`）。
- **Props**：为公共组件提供明确类型；序列化可传递 props 时注意「服务器→客户端」边界，复杂对象/函数/不可序列化内容不得跨边界。
- **状态与副作用**：客户端状态在 client 内；`useEffect` 使用场景有节制；避免水合问题（`suppressHydrationWarning` 仅作最后手段并注释原因）。
- **复用边界**：`packages/ui` 中组件保持框架无关与样式 Token 化；**Next/路由/headers/cookies 相关逻辑**不塞进通用 UI 包，留在 app 内。

## 路由规范

- **组织**：以文件系统路由为单一事实；动态段 `[id]`、可选段、`route groups` `(group)` 用途与 URL 不混淆的约定要文档化。
- **权限路由**：在 `layout`/`page` 的服务端侧鉴权、中间件 `middleware`、或 BFF 层多选；对未授权**重定向/401** 行为在设计与 SEO 上可控（避免可索引 200 的空白页）。
- **懒加载**：`dynamic()` 对重型 client 组件、第三方图表等；RSC 本身已具备边界，不滥用 dynamic。
- **页面边界**：`layout` 不频繁随子路由重挂载的共享壳；`template` 若使用需知每次导航重挂载的语义。嵌套与并行 route（`@modal` 等）若用则注明交互与可访问性。

## 状态管理规范

- **局部状态**：优先组件内与 URL/搜索参数（可 shareable），避免在无需全局共享时引入 store。
- **全局状态**：Zustand/Jotai/Context 等仅用于 client 岛；不将服务器可恢复数据在全局中重复存一份，除非有明确客户端协作需求；与 React Query 缓存职责勿重叠到难以推理。
- **服务端状态与缓存**：依赖 Next 的 `fetch` 缓存、`revalidate`、Tag 机制；与 CDN/中间层 cache-control 的协作写清，避免**私有数据被公共缓存**。

## 接口请求规范

- **BFF/Route Handlers**：统一错误体、CORS、鉴权、幂等与 trace id；对外 secret 不暴露到浏览器，敏感调用仅服务端。
- **在 RSC/Server Action 中**：遵守 Next 的表单与**渐进增强**语义，错误与重验证路径清晰；避免将不可信输入直接透传到下游。

- **客户端请求**：`fetch` 到同源或 BFF 路径；`credentials` 与 token 刷新的策略在文档中定稿；`AbortController` 与**竞态**在列表/快速切换中处理。

- **类型与校验**：Zod/valibot 在边界层校验请求体/响应子集；类型从 schema 或 OpenAPI 生成，避免手抄漂移。

- **重试/Loading**：在 React Query/自定义 hook 中策略化；在 RSC/流式中配合 `loading.tsx` 与 `Suspense` 边界，避免全页白屏。

## 表单规范

- **Server Actions / forms**：`action` 中校验与**二次提交**防护；错误映射回字段；`useFormStatus` 等配合 pending UI。
- **全客户端表单**：`react-hook-form`+Zod 等，注意与 RSC 的数据注入方式，避免可序列化边界问题。

- **可访问性**：`label`、错误与 `aria-*` 完整；**焦点管理**在提交后/错误时合理。

- **多步/草稿**：`draft` 在服务端/客户端存储的隐私与一致性问题在 PRD 中定。

## 权限规范

- **中间件/布局鉴权**：中间件中 token 续期/redirect 与**边缘/Node 能力**要匹配；`layout` 中二次校验的重复度控制合理。

- **细粒度控制**：`server` 中基于 session/角色决定数据可见性，不在 HTML 中泄漏敏感字段到不应看的角色。

- **RSC/缓存**：有权限区分的**页面不可**被长缓存、共享缓存污染；`fetch` 缓存配置与**认证请求**一致。

- **多租户/组织**：`tenant` 在请求上下文与 BFF 中**贯穿**；`cookie` 路径与**子域**策略在文档中固定。

## 测试规范

- **单元/组件**：Jest 或 Vitest 与 RSC/客户端拆分测；`next/jest` 或自定义 alias；mock `next/navigation` 等。

- **E2E**：Playwright 为主；测关键路径与**鉴权/角色**矩阵；`preview` 部署或 Vercel preview 上跑。

- **契约测试**：BFF/Route Handlers 的输入输出与**下游** mock；若用 OpenAPI，有 breaking change 时 CI 报。

- **性能与指标**：Lighthouse/CI 预算、Core Web Vitals 的门槛；RSC/流式/图片优化（`next/image`）纳入验收。

## Rule 生成要求

- **生成约束**：显式 **Next 版本、App 或 Pages 路由模式、运行时（node/edge）、`metadata` 与 i18n 是否启用、图片与字体优化策略**。

- **禁止行为**：禁止在 Rule 中混淆「可在 Server Component 中使用的库」与只能 client 的库；禁止假设所有页面都可静态导出（`output: export`）除非项目真如此。

- **验收标准**：`next build` 在 CI 通过、无类型错误、主要路由在预览环境可手测/自动测通过；敏感路由无缓存外泄。

## Skill 生成要求

- **输入**：功能说明、Figma/文案、**接口契约/权限**、**缓存与 SEO** 要求、目标 Next 与 Node 版本。

- **步骤**：在 `app` 下定路由与布局 → 实现 RSC/ server action 或 BFF → client 岛 → 样式与 a11y → 单测/ E2E → 预发与缓存头/机器人策略检查。

- **输出**：PR、测试证据、**缓存/重验策略**、回滚点与 feature flag 说明。

- **异常处理**：`hydration` 问题、RSC/ client 错配、Turbopack/alias 与生产差异、**边缘中间件**限制等需记录到 ADR/故障单。

## Flow 生成要求

- **阶段**：技术方案（RSC/缓存/中间件/部署目标）→ 实现 → 预览 → 预发压力与权限回归 → 生产与监控/告警。

- **门禁**：`lint`/`typecheck`/`build`/`e2e` 必过；**CSP/安全头**、依赖漏洞门禁按组织要求；环境变量在部署平台**校验齐全**（若用 Zod 校验 `process.env` 更好）。

- **状态流转**：与**灰度/金丝雀**、数据库迁移节奏对齐；`rollback` 含 CDN 缓存清除策略（若用）。

- **异常出口**：维护页、**只读模式**、BFF 熔断、上游降级，流程与**值班**角色明确。

## Manifest 推荐

- **推荐资产组合**：`create-next-app` 带 TS+ESLint+Tailwind 或团队基线、统一 logger、Sentry/OTel 示例、`next-auth`/自建 session 的文档化样例、Playwright、CI 上的 `build`+ E2E。

- **安装策略**：锁 `next`/`react` 主版本线；**小版本/补丁**升级读 release notes 与**CVE**；大升级走试点应用或分支实验。

## 禁止行为

- 禁止在文档或生成物中写出完整可投产的业务**密钥**、真实用户数据、未脱敏的接口响应。

- 禁止虚构**部署平台专属**配置（Vercel/自托管）而不标注适用环境；禁止**跳过** `next build` 或**误导性**的「本地 only」合入说明。

- 禁止把只应在**服务端**执行的库或密钥打入 client chunk。

## 验收标准

- `next build` 无警告**或**有登记豁免；LCP/CLS 在目标环境达标；鉴权/缓存/SEO 有清单式验收；`middleware` 与**边缘/Node 行为**与文档一致；**敏感数据不进入公共缓存**。
