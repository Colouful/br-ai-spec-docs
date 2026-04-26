# React + Vite 前端工程标准

## 适用技术栈

- **语言**：TypeScript 优先；必要时允许在迁移期使用 JSDoc 标注的 JavaScript。
- **框架与运行时**：React 18+，函数式组件 + Hooks 为主；避免在业务代码中新增 Class 组件。
- **构建工具**：Vite（`vite` + `vite.config.ts`）；包管理器推荐 pnpm 或 npm；锁文件须纳入版本控制。
- **常见 UI 与生态**：可配合 Ant Design、MUI、Radix、Tailwind CSS、React Router 等；新依赖须评估包体积、可访问性与维护态。

## 适用项目类型

- **单页应用（SPA）**：Vite 默认形态，配合客户端路由与按需代码分割。
- **库/工具包（library）**：`vite` library 模式或 tsup/rollup 打包，对外导出类型与 ESM 优先。
- **Monorepo**：推荐在根目录统一 TS、ESLint/Prettier、构建脚本；子包按领域划分，应用包与可复用包边界清晰。

## 目录结构规范

- **推荐顶层**：`src/app`（应用壳、Provider）、`src/routes` 或 `src/pages`（与路由一一对应）、`src/components`（通用 UI）、`src/features` 或 `src/modules`（按业务域竖切）、`src/entities`/`api`（接口与类型）、`src/shared`（纯工具、常量、hooks 基座）。
- **模块边界**：业务域之间禁止深层互相引用；跨域依赖通过 `shared` 或明确定义的公共契约（类型、轻量 hook）。
- **组件分层**：`ui`（无业务含义）→ `widgets`（组合块）→ `pages`（页面与数据编排）；业务逻辑优先下沉到 hook 与用例级函数，页面只做编排。

## 组件规范

- **职责**：单组件单一职责；容器组件负责取数与分派，展示组件纯 props 驱动（测试友好）。
- **命名**：组件文件使用 PascalCase 或与目录 `index.tsx` 约定一致；自定义 Hook 以 `use` 前缀；事件处理函数 `handleXxx`。
- **Props**：为对外组件编写显式类型/接口；避免透传过深的 `...rest`；布尔 props 使用正向语义（如 `isOpen`）。
- **状态与副作用**：本地 UI 状态用 `useState`/`useReducer`；副作用集中在 `useEffect`/`useLayoutEffect` 并写明依赖与清理函数；避免在 render 中副作用。
- **复用边界**：可复用度高的放入 `components` 或设计系统；业务强耦合的留在 `features/xxx` 下，不强行上提。

## 路由规范

- **组织**：以 URL 为契约；路由表集中定义或按 feature 分文件合并；保持路径与 `pages` 结构可对照。
- **权限路由**：路由元信息记录所需角色/权限点；在路由守卫或布局层做重定向/403，不在每个页面重复散落判断。
- **懒加载**：页面级使用 `React.lazy` + `Suspense` 与 Vite 分块；为关键路径预加载可配置；错误边界覆盖懒加载失败。
- **页面边界**：一个 URL 对应一个主页面入口；子路由由布局组件承载；避免在一个组件内通过巨大条件分支模拟多页。

## 状态管理规范

- **本地状态**：组件内、表单、局部 UI 开关优先本地状态，避免过早全局化。
- **全局状态**：Context + reducer、Zustand、Jotai 等；按域拆分 store，避免单一巨型 store；持久化只针对必要键并版本化。
- **服务端状态**：使用 TanStack Query、SWR 等管理缓存、去重、失效与重试；不在全局 store 中重复镜像服务器可恢复的数据，除非有明确离线或协作需求。

## 接口请求规范

- **API client**：单例或工厂封装 `fetch`/axios，统一 `baseURL`、认证头、请求 ID、超时；禁止在业务组件中裸写完整 URL。
- **错误处理**：HTTP 与业务码分层；统一错误对象映射为用户可读文案 + 可观测字段（code、requestId）；401/403 在拦截器或全局处理。
- **Loading/重试**：与 TanStack Query 的 `isPending`、重试策略对齐；对幂等读请求可指数退避；对写操作默认不重试或仅一次并需显式配置。
- **类型定义**：为请求/响应建类型，并在边界（API 层或 zod 解析）校验；不将 `any` 贯穿业务层。

## 表单规范

- **校验**：用 React Hook Form、Formik 或同等方案，Schema 用 Zod/Yup 等声明式；同步规则与异步（远程唯一性）分离。
- **提交**：`isSubmitting` 禁用重复提交；乐观更新需有回滚路径；多步表单的步骤机状态明确。
- **错误展示**：字段级错误与表单级（全局）错误分区展示；可访问性上关联 `aria-describedby` 与 `role=alert`（按库能力）。
- **反馈**：成功/失败使用 Toast 或行内信息；对敏感操作需二次确认。

## 权限规范

- **菜单权限**：菜单数据由授权结果与路由元信息派生，禁止前端硬编码「假菜单」与后端不一致。
- **按钮/操作权限**：以权限码/策略函数封装，组件内集中判断，避免魔法字符串。
- **路由权限**：在路由级拦截未授权访问；与登录态、租户（如有）一起评估。
- **数据权限**：列表/详情展示依赖后端按权限过滤后的数据；前端脱敏为补充，不替代鉴权。

## 测试规范

- **单元测试**：对纯函数、reducer、权限与格式化逻辑使用 Vitest；表驱动、边界用例必覆盖。
- **组件测试**：Testing Library，断言用户可见行为与可访问性；避免测实现细节（如内部 state 名称）。
- **E2E**：Playwright 覆盖核心登录、主路径、关键权限差异；在 CI 上稳定运行，敏感环境用测试账号。
- **验收标准**：关键域覆盖率阈值由项目约定；缺陷修复必须带回归用例；视觉回归对关键页可选（Percy/截图基线）。

## Rule 生成要求

- **生成约束**：必须显式 Vite 入口、`index.html` 根、环境变量 `import.meta.env` 前缀与构建模式；明确 ESLint 规则组（`react-hooks`、`@typescript-eslint` 等）与 import 顺序。
- **禁止行为**：禁止在 Rule 中假定 Create React App 或 Webpack 专属 API；禁止混淆 Next.js 的 SSR 约定与纯 SPA Vite 项目。
- **验收标准**：新人可按 Rule 在干净仓库完成 `pnpm install && pnpm dev` 与 `pnpm build` 无告警目标。

## Skill 生成要求

- **输入**：目标（如「新增一个带鉴权的列表页」）、技术栈为 React + Vite、现网目录与约束、设计稿或接口契约链接（如有）。
- **步骤**：拉分支 → 在约定目录建路由与页面 → 建 API 类型与 hook → 实现 UI 与测试 → 走 lint/类型检查 → 提交小步提交或 PR 说明。
- **输出**：代码变更、自测结果、对 ENV 与 feature flag 的说明、回滚点。
- **异常处理**：依赖安装失败、类型与 API 冲突、E2E 飘红时记录日志与最小复现，不跳过类型检查合并。

## Flow 生成要求

- **阶段**：开发 → 自测与静态检查 → Code Review → 合入主分支/发布分支 → 部署前验证（staging）。
- **门禁**：lint/类型/单测/关键 E2E 在 CI 必须通过；安全依赖扫描有高危时阻断或升级。
- **状态流转**：`draft` → `in_review` → `ready` → `released`；与版本号/变更日志挂钩。
- **异常出口**：热修分支、回滚、feature 开关关闭路径必须文档化。

## Manifest 推荐

- **推荐资产组合**：Vite 模板、ESLint+Prettier、TypeScript 严格模式、路径别名、TanStack Query、React Router、Testing Library+Vitest、Playwright 基础配置。
- **安装策略**：`create vite` 起步；在文档中锁版本范围；大版本升级前跑完整回归与性能对比。

## 禁止行为

- 禁止在文档或生成物中输出完整业务源码级实现（可给结构与伪代码边界）。
- 禁止虚构不存在的 API、字段或权限点；缺失须标注 TODO 与待确认人。
- 禁止跳过与项目约定一致的测试与检查；禁止将密钥写入前端代码或公共仓库。

## 验收标准

- 可本地、可 CI 复现的 `dev/build/test/lint` 全绿；路由与懒加载在构建产物中可验证分块；关键路径有自动化覆盖；与本文档各章节逐条可对照，无未解释的例外。
