# Vue + Vite 前端工程标准

## 适用技术栈

- **语言**：TypeScript 为默认；SFC 使用 `lang="ts"`；组合式 API（Composition API）为首选。
- **框架与运行时**：Vue 3+；`script setup` 为推荐单文件组件（SFC）写法；对选项式 API 以维护存量为主，新功能优先组合式。
- **构建工具**：Vite + `vite.config.ts`；`vue-tsc` 与类型检查在 CI 中必跑；包管理器与锁文件规范同组织策略。
- **常见 UI 与生态**：Element Plus、Naive UI、Vuetify、Quasar 等；Pinia 为官方推荐状态方案；vue-router 4+；可与 UnoCSS/Tailwind 搭配。

## 适用项目类型

- **SPA 应用**：常规后台与门户类项目；以路由为界的页面与布局结构。
- **可复用库/组件包**：Vite 库模式或 Vite-Plugin-DTS 生成类型；注意 `peerDependencies` 中声明 `vue`。
- **Monorepo**：`packages` 中拆分应用、共享 `ui`、领域模块；Vite 配置继承与 `alias` 统一在根或共享配置中维护。

## 目录结构规范

- **推荐顶层**：`src/app` 或 `src/main.ts` 入口、全局插件注册；`src/router` 与 `src/views`/`src/pages` 对应；`src/components`（通用与基础块）；`src/stores`（Pinia 按域拆分）；`src/api` 或 `src/composables` + `api` 子目录；`src/assets` 与 `public` 边界清晰（后者为不经打包处理的静态根）。
- **模块边界**：按 `features/xxx` 或领域文件夹竖切，内部自洽；跨域通过 `shared` 或只导出声明良好的 composable/类型。
- **组件分层**：`base`（无业务）→`business`（业务块）→`views`（页面，负责组装）；复杂逻辑进 composable 与 `useXxx` 函数，SFC 保持以模板为主的可读性。

## 组件规范

- **职责**：父级负责数据获取与子组件编排；子组件以 props/emit 通信；避免在通用组件里写死业务文案与接口路径。
- **命名**：多单词组件名（Vue 推荐）；`PascalCase` 文件名与注册名一致；composable 以 `use` 开头；事件名在 `script setup` 中显式 `defineEmits` 类型化。
- **Props**：`defineProps`+类型或运行时校验（按团队约定二选一，类型优先）；可选 props 提供默认值与文档化注释（`<!---` 与 `///` 均可）。
- **状态与副作用**：`ref`/`reactive` 边界清晰，避免对深层对象无节制解构导致响应性丢失；`watch`/`watchEffect` 指明依赖、清理与刷新策略；`onMounted` 等只承担必要的 DOM/订阅逻辑。
- **复用边界**：可跨项目者放独立包或 `packages/ui`；与后端契约强绑定的留在业务 feature。

## 路由规范

- **组织**：`vue-router` 路由表模块化拆分；`meta` 中声明 `title`、布局、所需权限、是否缓存 `keepAlive` 等；命名路由稳定可测。
- **权限路由**：动态路由在拿到权限列表后 `addRoute`，退出登录时 `reset`；静态路由仅保留 login、404 等；导航守卫中集中处理鉴权与重定向，避免在页面中复制粘贴。
- **懒加载**：使用 `() => import('.../views/Xxx.vue')`；按页面分包；大依赖配合 `defineAsyncComponent` 时提供 loading 与 error 组件（可选）。
- **页面边界**：每页有唯一入口组件；子路由在布局组件中 `router-view` 呈现；深链接与 `params/query` 类型在路由类型声明或生成器中体现（如有）。

## 状态管理规范

- **本地状态**：SFC 内、表单、局部弹层优先用本地 `ref`/`reactive`。
- **全局状态**：Pinia store 按域拆分，避免 `store` 全塞一个文件；`getter` 派生、异步 `action` 集中；持久化用插件时键名与版本要约定。
- **服务端状态**：可选 TanStack Query 的 Vue 版或自封装基于 `useAsync`/自定义 composable 的查询缓存；不重复在 Pinia 里镜像只读服务数据，除非有离线/协作需求。

## 接口请求规范

- **API 模块**：`axios` 或 `fetch` 单例，拦截器里挂 token、公共错误、trace id；`baseURL` 来自 `import.meta.env`。
- **错误处理**：HTTP 与业务体分离；`Axios` 的 `isAxiosError` 等分类；在拦截器与页面层有分工（全局 toast vs 可局部覆盖）。
- **Loading/重试**：在 composable 中封装 `isLoading`/`isFetching` 与可取消的 `AbortController`；对 GET 幂等可配置重试，写操作为显式、保守策略。
- **类型定义**：API 的 request/response 有 TS 类型；在边界用 zod 等校验未知负载（可选项）。

## 表单规范

- **校验**：VeeValidate 或自封装 + Zod 规则，与 SFC/组合式自然结合；跨字段在 schema 中声明；异步验证 debounce 防刷。
- **提交**：`submit` 中防止重复；错误映射到表单项的 `name` 路径；`aria-*` 与可访问性尽量满足组件库或原生支持。
- **错误展示**：字段下提示 + 全表单摘要区；大表单分步在步骤间持久草稿（若需求允许）。
- **反馈**：与全局 `ElMessage`/Toast 等策略统一，避免多来源冲突。

## 权限规范

- **菜单/路由**：与后端角色、权限点同步；`meta` 中声明与指令 `v-permission` 或 `hasPermission` 同源于权限状态。
- **按钮权限**：以指令、组件封装或 `computed` 策略，禁止复制权限字符串到十余处硬编码（应集中为常量/枚举/后端下发码表）。
- **数据权限**：表格列与按钮显隐可随数据行权限变化，以后端结果为准，前端不伪造「看见全部数据」的假象。

## 测试规范

- **单元测试**：Vitest + `vue` test utils；对 composable 与纯逻辑优先；`mount` 组件时 mock 网络与 store。
- **组件测试**：断言可见文本、emit、路由/ pinia 注入的交互；`stub` 子组件控制范围。
- **E2E**：Cypress/Playwright 对登录、主流程、权限差异；稳定选择器（`data-testid` 优先）。
- **验收标准**：关键域覆盖阈值由项目定义；`vue-tsc` 与 `vitest` 在 CI 必跑；回归缺陷补测试用例。

## Rule 生成要求

- **生成约束**：明确 Vue 3 + Vite 环境变量、SFC 规范、`@` 类路径别名、禁止混用已废弃的 Vue 2 全局 API（若迁移项目另附迁移 Rule）。
- **禁止行为**：禁止在 Rule 中假定 Nuxt/SSR 专属生命周期（与纯 SPA 区分）；禁止与 React 的 JSX 模式混淆。
- **验收标准**：生成代码能通过 `pnpm vue-tsc --noEmit` 与 `pnpm test` 基线，开发服务器热更新可预期工作。

## Skill 生成要求

- **输入**：功能描述、现网 `router`/`stores` 草图、接口或 mock、设计约束。
- **步骤**：定路由与页面骨架 → 写 API+类型 → 实现 `view`+composable+组件 → 补测试与 a11y 自审 → 提交 PR，说明 env 与开关。
- **输出**：可审查的差分、测试与截图/录屏（若 UI 敏感）、对权限与多语言的说明。
- **异常处理**：类型错误、HMR 异常、路由循环重定向、Pinia 未按序初始化等问题需记录与最小复现。

## Flow 生成要求

- **阶段**：设计对齐 → 开发 → 本地/CI 质量门禁 → 评审合入 → 预发验证 → 发布与监控。
- **门禁**：`lint`、`typecheck`、`test`、主路径 E2E、依赖审计（高危阻断或豁免流程）。
- **状态流转**：功能开关与发版单绑定；`rollback` 预案与回滚后数据一致性说明（若有写库）。
- **异常出口**：线上故障的开关关闭、只读模式、老版本重定向，需在 Flow 中可指名对应负责人。

## Manifest 推荐

- **推荐资产组合**：`create-vite` vue-ts 模板、ESLint+Prettier+Stylelint（若用 Less/CSS）、`unplugin-auto-import`/`unplugin-vue-components`（按团队需要）、`Pinia`、统一 axios 层、Plauwright/Cypress 样例、Commitlint/Changeset 可选。
- **安装策略**：在 README/内部文档中固定主要依赖主版本与升级周期间隔；Vite 插件升级时优先读 breaking notes。

## 禁止行为

- 禁止在规范文档或 AI 产物中直接粘贴可上线的完整业务实现代码；可做接口与结构说明。
- 禁止虚构环境变量名、端点、权限点；未确认须标注与对接人。
- 禁止为「省事」关闭严格类型或整文件 `eslint-disable` 无解释通过。

## 验收标准

- 本地与 CI 命令一致、可复现；路由懒加载在构建分析中可看到 chunk；`vue-tsc` 与测试无红；与本文各节一致或差异在清单中明确记载。
