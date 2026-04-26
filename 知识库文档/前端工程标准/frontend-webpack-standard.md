# Webpack 前端工程标准

## 适用技术栈

- **语言**：TypeScript 为首选；Babel/TS 在 `tsconfig` 与 Babel 配置中一致；`paths` 与 `webpack.resolve.alias` 需对齐，避免**重复解析**。

- **框架**：可为 React、Vue 2/3 或**无框架**（多页/传统增强）；**本文档不绑定单一 UI 库**，在项目中明确 React/Vue/原生之一的基线及版本下界。

- **构建工具**：Webpack 5+；`mode`、`devServer`、`splitChunks`、`Module Federation` 若使用须单独成文与代码评审门槛。

- **常见能力**：`babel-loader`/`ts-loader`/`swc`/`esbuild-loader` 选一为主并固定；`css`/`less`/`sass`/`postcss`；`mini-css-extract-plugin` 用于生产；`html-webpack-plugin` 或框架 CLI 的封装；**长缓存**的 `contenthash` 与 `runtimeChunk` 策略在团队内统一。

## 适用项目类型

- **遗留 SPA/MPA 工程**：`webpack` 深度定制、**迁移窗口长**的仓库。

- **多入口/微前端**：通过 `entry`+ `splitChunks` 或 Module Federation；基座与远程之间的**共享依赖版本契约**、**兼容窗口**、**回退策略**为强制设计项。

- **库/Design Token 包**：`output.library`+`externals`；`peerDependencies` 对宿主框架声明清晰。

## 目录结构规范

- **推荐组织**：`src` 为源码根，按**框架**习惯分子目录（如 `src/pages`、`src/components`）或**领域**子目录；`public` 为不经过 `import` 链的静态根。

- **构建配置**：`webpack.config` 可 `merge` 分 `common/dev/prod`；环境变量用 `webpack.DefinePlugin`/`env-cmd`/`dotenv` 的约定在 README 中固定，**不提交**生产密钥样例到仓库。

- **模块边界**：`alias` 仅作路径简化，不代替模块分层；`Module Federation` 的 `remotes`/`exposes` 的**可演进性**（不暴露内部未稳定模块）在评审中必须检查。

## 组件规范（在 Webpack 与所选框架下）

- **职责**：在 React/Vue 的既有规范上，额外保证**不依赖** HMR/开发服务的副作用逻辑（HMR 仅作 DX）；生产构建不依赖 `window` 在模块顶层的**非标准假设**（除非有 polyfill/分区加载）。

- **动态导入**：`import()` 的 chunk 名与**预取/预加载**由业务决定；`webpackPrefetch` 注释在关键路径**审慎**使用并评审。

- **复用与 Federation**：`exposed` 组件必须**自洽**、样式作用域不污染基座，主题通过**契约化** props/CSS 变量传递。

- **资源**：小图可 `import` 进 bundle，大图/字体走 `asset/resource` 或 CDN；`publicPath` 与**部署子路径**一致。

## 路由规范

- **SPA 路由**：由 `history` 模式/ hash 与服务器 `fallback` 到 `index.html` 的约定共同保证；Nginx/网关配置与**前端 `basename`** 成对出现。

- **多页**：每个 HTML 的 entry 与 chunk 关系清晰，避免**全量脚本**到每个 MPA 页上。

- **微前端子应用**：**路由前缀**不冲突、壳与子应用**生命周期**（`single-spa` 等）的加载/卸载/样式隔离有清单。

- **懒加载**：`import()` 的 chunk 在构建报告里可追；**弱网**首屏的骨架/占位与**错误** chunk 的 fallback 策略有说明。

## 状态管理规范

- **在 Webpack 下无额外约束**，以所选框架的 store/Context 等为准；注意**多 bundle** 与 Federation 的**单例/版本**问题（如多个 React 副本的禁忌）。

- **数据缓存**：在客户端库（SWR/Query 等）与**后端缓存头**、反向代理的协作与 SPA 的**stale-while-revalidate** 需一致。

- **与构建的关系**：`DefinePlugin` 的 flag 不用于驱动**敏感权限**，仅可驱动功能开关的**非敏感**分支，权限仍以**服务端/会话**为准。

## 接口请求规范

- **同源与代理**：`devServer.proxy` 仅开发；生产通过网关反代，**CORS 与鉴权**在部署文档中可复现；**路径前缀**在环境变量中统一，不在每个组件里拼接。

- **分块与 `publicPath`**：API 返回的**绝对资源 URL** 在跨环境（内外网/灰度）下的规则写清；避免硬编码**固定域名**。

- **错误与重试**：axios/fetch 的拦截与**可取消**请求在路由切换/组件卸载中避免泄漏与竞态；**长轮询/SSE** 的关闭钩子在微前端**卸载**时必执行。

- **类型与契约**：在仓库内维护 OpenAPI 或手写类型，与 **mock** 服务版本对齐。

## 表单规范

- 与具体框架/库一致（见各栈专项标准）；在 Webpack 中注意**大表单库**的摇树与**按需**引入，避免**全量打爆**主包。

- **i18n** 资源懒加载时与 `splitChunks` 策略协调，**语言切换**不重复全量下所有 chunk。

- **可访问性**：`label`、错误提示与焦点管理不依赖构建时注入的**旁路**脚本。

## 权限规范

- 菜单/按钮/数据权限逻辑与**Federation/MPA/SPA** 形态无关，均在**统一会话/统一网关**上结论一致；**子应用**不各自发明一套 `token` 存储，除非经安全评审。

- **CSP/安全头**在**网关/服务器**上配置，与**内联脚本**的取舍和 `webpack` 的**nonce/hash** 策略若采用则文档化（若项目禁止内联，则全走外链 chunk）。

- **多 bundle** 下不重复下发**可枚举的**权限点清单到客户端（若已最小化，仍注意不要过度暴露于 HTML）。

## 测试规范

- **单元/组件**：Jest+Testing Library 或同等级；`moduleNameMapper` 对齐 `alias` 与**静态资源 mock**；在 CI 与**本地**同一套配置。

- **E2E**：Cypress/Playwright；对**多入口/微前端**提供**可重复**的启动/桩服务脚本（`concurrently` 等）。

- **构建回归**：`webpack-bundle-analyzer` 的**基线**与**阈值**（主包/初载）在 PR 中大变更要贴对比。

- **验收标准**：`webpack` 构建在 CI 可缓存（`cache` 类型与**锁文件**），时间可接受；无未解释的 `performance` 回退。

## Rule 生成要求

- **生成约束**：**Webpack 主版本、目标浏览器、browserslist、`splitChunks` 与 `sideEffects` 的约定、是否用 Federation、**`publicPath` 的部署位点**、环境变量**前缀**与注入方式。

- **禁止行为**：禁止假设 `CRA` 若项目已不采用；禁止把**微前端**壳与子应用的**依赖版本**在 Rule 里写死为虚构数字；禁止忽略 **`npm ls`** 的 duplicate 问题（尤其 React）。

- **验收标准**：`npm run build` 产物可部署、source map 与**上传策略**、**SRI** 若用则一致。

## Skill 生成要求

- **输入**：现网 `webpack` 分档文件、Federation 拓扑（若有）、部署路径、Nginx 样例、**浏览器支持**、性能预算。

- **步骤**：在约定目录实现功能 → 验证 **dev** 与 **prod** 表现一致（路径、**懒加载**、**publicPath**）→ 走 bundle 分析 → 与网关/基座**联调**（若微前端）→ 文档更新。

- **输出**：PR 附**体积对比**、**Lighthouse** 或**自定义指标**、回滚点。

- **异常处理**：`publicPath` 错导致白屏、**远程 404**、Federation 版本漂移、HMR 正常但**生产**不工作等，要求**可诊断**的日志与检查清单。

## Flow 生成要求

- **阶段**：构建配置评审（含安全与缓存）→ 实现 → 性能与体积门禁 → 联调/预发 → 发布与**CDN 刷尾**（若需要）。

- **门禁**：`build` 在 CI 成功、**e2e** 在准生产、**CSP/安全**扫描、依赖漏洞的阻断策略。

- **状态流转**：与**灰度**、**Federation 远程**独立发布时序的兼容矩阵。

- **异常出口**：**远程不可用**的降级、**子应用**独立部署失败时的壳行为。

## Manifest 推荐

- **推荐资产组合**：`webpack-merge`、`mini-css-extract-plugin`、`terser`/`swc`、**`thread-loader`（慎用场景）**、`copy-webpack-plugin`（限定用途）、`fork-ts-checker`（若 Babel+TS 分离））、`playwright`、基础 **nginx** 与 **fallback** 样例、**Sentry 上传** 与 source map 策略。

- **安装策略**：锁 `webpack` 与**关键 loader 插件**主版本；**大版本**升级在试点分支跑**全量 E2E 与多入口场景**。

## 禁止行为

- 禁止在标准文档中粘贴可上线的**内网/密钥/真实**接口路径；可写占位符与**环境变量**名。

- 禁止在不明 `sideEffects` 的情况下**全局 false** 导致**样式丢失**等故障。

- 禁止微前端/多 bundle 在**不声明** `shared`/`singleton` 时上线造成**双 React**。

- 禁止跳过**生产**构建与**多环境**的 `publicPath` 自测。

## 验收标准

- `dev` 与 `prod` 的**首屏/路由懒加载/资源 404** 可验证；Federation/MPA/SPA 场景与文档一致；`bundle` 在预算内；**CSP/跨域/鉴权** 与**运维侧**的清单可对照通过。
