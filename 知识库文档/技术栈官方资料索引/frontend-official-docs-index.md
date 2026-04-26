# 前端技术栈官方资料索引

## 用途

本文件用于帮助 AI 工程资产工厂识别前端技术栈的官方资料来源。生成资产时，应优先遵循 Hub 资产契约和团队工程标准，官方文档仅作为技术事实参考。

本文件主要服务于以下场景：

1. 前端 Rule 资产生成
2. 前端 Skill 资产生成
3. 前端 Flow / Manifest 资产生成
4. 前端代码审查规则生成
5. 前端项目工程化约束生成
6. 前端测试与验收标准生成

## 技术栈索引

### React

- 官方文档：https://react.dev/
- 适用场景：React 组件、Hooks、状态组合、组件设计、前端应用开发。
- 使用说明：用于确认 React 官方推荐的组件、状态、Hooks、渲染和应用组织方式。

### Vue

- 官方文档：https://vuejs.org/
- 适用场景：Vue 3、组合式 API、组件设计、前端应用开发。
- 使用说明：用于确认 Vue 3 官方推荐的组合式 API、组件通信、响应式系统和应用组织方式。

### Next.js

- 官方文档：https://nextjs.org/docs
- 适用场景：React 全栈框架、路由、服务端渲染、App Router、数据加载。
- 使用说明：用于确认 Next.js 路由、渲染模式、服务端组件、数据加载和部署相关能力。

### Vite

- 官方文档：https://vite.dev/
- 适用场景：前端构建、开发服务器、插件机制、React/Vue 工程化。
- 使用说明：用于确认 Vite 构建、开发服务器、插件机制和前端工程配置方式。

### Webpack

- 官方文档：https://webpack.js.org/
- 适用场景：传统前端构建、Loader、Plugin、构建优化。
- 使用说明：用于确认 Webpack Loader、Plugin、模块打包和构建优化相关能力。

### TypeScript

- 官方文档：https://www.typescriptlang.org/docs/
- 适用场景：类型系统、前端/后端 TypeScript 工程规范。
- 使用说明：用于确认 TypeScript 类型系统、配置、类型收窄、泛型和工程化实践。

### Arco Design

- 官方文档：https://arco.design/
- 适用场景：企业级 React/Vue UI 组件库。
- 使用说明：用于确认 Arco Design 组件能力、设计规范和企业级 UI 组件使用边界。

### Ant Design

- 官方文档：https://ant.design/
- 适用场景：企业级 React UI 组件库。
- 使用说明：用于确认 Ant Design 组件能力、表单、表格、布局和企业后台 UI 实践。

### Element Plus

- 官方文档：https://element-plus.org/
- 适用场景：Vue 3 企业级 UI 组件库。
- 使用说明：用于确认 Element Plus 组件能力、表单、表格、弹窗和 Vue 企业级 UI 实践。

## 使用原则

1. 不直接复制官方文档内容作为资产正文。
2. 不把官方文档中的示例代码当作项目代码输出。
3. 只提炼与 Rule、Skill、Flow、Manifest 相关的工程约束。
4. 当官方文档与 Hub 资产规范冲突时，以 Hub 资产规范为准。
5. 如果项目存在既有前端规范、组件库封装或 UI 约束，应优先遵循项目内规范。
6. 不强制项目使用某个前端框架，除非项目上下文已经明确。
7. 生成前端资产时，应关注组件边界、状态管理、类型安全、交互体验、可访问性、测试和构建质量。
8. 涉及用户输入、权限展示、敏感数据展示、前端路由守卫时，必须提高风险等级。

## 链接校验摘要

| 资料项 | 链接 | 校验结果 | 备注 |
|---|---|---|---|
| React | https://react.dev/ | 已确认：官方资料入口正确 | HTTP 200，无跳转至非预期域名 |
| Vue | https://vuejs.org/ | 已确认：官方资料入口正确 | HTTP 200 |
| Next.js | https://nextjs.org/docs | 已确认：官方资料入口正确 | HTTP 200 |
| Vite | https://vite.dev/ | 已确认：官方资料入口正确 | HTTP 200 |
| Webpack | https://webpack.js.org/ | 已确认：官方资料入口正确 | HTTP 200 |
| TypeScript | https://www.typescriptlang.org/docs/ | 已确认：官方资料入口正确 | HTTP 200 |
| Arco Design | https://arco.design/ | 已确认：官方资料入口正确 | HTTP 200，字节系官方站点 |
| Ant Design | https://ant.design/ | 已确认：官方资料入口正确 | HTTP 200，蚂蚁系官方站点 |
| Element Plus | https://element-plus.org/ | 已确认：官方资料入口正确 | HTTP 200，项目官方站点 |

*校验说明：于自动化环境通过 `curl` 访问并记录最终 HTTP 状态与有效 URL；不同网络环境可能存在差异，若与上表不一致请本地复核。*
