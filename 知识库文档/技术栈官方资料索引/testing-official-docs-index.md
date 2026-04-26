# 测试与质量工具资料索引

## 用途

本文件用于帮助 AI 工程资产工厂识别测试与质量工具的参考来源。生成资产时应转化为验收标准、测试用例和质量门禁。

本文件主要服务于以下场景：

1. testCases 生成
2. acceptanceCriteria 生成
3. QA Checklist 生成
4. 单元测试、集成测试、端到端测试建议生成
5. CI 质量门禁规则生成
6. 回归测试和发布验收标准生成

## 测试工具索引

### Vitest

- 官方文档：https://vitest.dev/
- 适用场景：前端/TypeScript 单元测试。
- 使用说明：用于确认 Vitest 测试运行、断言、Mock、覆盖率和前端单测实践。

### Jest

- 官方文档：https://jestjs.io/docs/getting-started
- 适用场景：JavaScript/TypeScript 单元测试。
- 使用说明：用于确认 Jest 测试运行、断言、Mock、快照和覆盖率能力。

### Testing Library

- 官方文档：https://testing-library.com/docs/
- 适用场景：React/Vue 组件测试、用户行为测试。
- 使用说明：用于确认基于用户行为的组件测试方法和可访问性相关测试实践。

### Playwright

- 官方文档：https://playwright.dev/docs/intro
- 适用场景：端到端测试、浏览器自动化测试。
- 使用说明：用于确认 E2E 测试、浏览器自动化、断言、录制和多浏览器测试能力。

### JUnit 5

- 官方文档：https://junit.org/junit5/docs/current/user-guide/
- 适用场景：Java 单元测试。
- 使用说明：用于确认 Java 单元测试、测试生命周期、断言、参数化测试和扩展能力。

### Mockito

- 官方文档：https://site.mockito.org/
- 适用场景：Java Mock 测试。
- 使用说明：用于确认 Java Mock、Stub、Verify 和依赖隔离测试能力。

### Pytest

- 官方文档：https://docs.pytest.org/
- 适用场景：Python 测试。
- 使用说明：用于确认 Python 测试、Fixture、参数化测试、插件和测试组织方式。

### Go testing

- 官方文档：https://pkg.go.dev/testing
- 适用场景：Go 标准测试框架。
- 使用说明：用于确认 Go 标准库 testing 包、单元测试、基准测试和示例测试能力。

## 使用原则

1. 测试工具资料用于生成 testCases 和 acceptanceCriteria。
2. 不强制项目必须使用某个测试工具。
3. 未识别测试框架时，输出通用测试建议。
4. 验收标准必须可验证，不能只写“保证质量”。
5. 测试建议必须覆盖正常路径、异常路径、边界条件和回归风险。
6. 对涉及权限、资金、订单、数据删除、发布上线的需求，必须提高测试覆盖等级。
7. 如果无法确认项目测试框架，必须标记“需要人工确认”。
8. 测试建议应尽量区分单元测试、集成测试、端到端测试和手工验收。
9. 涉及 UI 的需求，应关注用户行为、状态变化、错误提示和可访问性。
10. 涉及 API 的需求，应关注请求参数、响应结构、错误码、权限和幂等性。
11. 涉及异步任务、消息队列、缓存和定时任务时，应补充重试、超时、失败补偿和数据一致性测试。

## 链接校验摘要

| 资料项 | 链接 | 校验结果 | 备注 |
|---|---|---|---|
| Vitest | https://vitest.dev/ | 已确认：官方资料入口正确 | HTTP 200，Vitest 官方站点 |
| Jest | https://jestjs.io/docs/getting-started | 已确认：官方资料入口正确 | HTTP 200，Jest 官方文档 |
| Testing Library | https://testing-library.com/docs/ | 已确认：官方资料入口正确 | HTTP 200，TL 官方组织站点 |
| Playwright | https://playwright.dev/docs/intro | 已确认：官方资料入口正确 | HTTP 200，Playwright 官方文档 |
| JUnit 5 | https://junit.org/junit5/docs/current/user-guide/ | 已确认：官方资料入口正确，但存在自动跳转 | 校验中经跳转到达 docs.junit.org 上当前发行文档（以官方当前版本为准） |
| Mockito | https://site.mockito.org/ | 已确认：官方资料入口正确 | HTTP 200，项目官方站点 |
| Pytest | https://docs.pytest.org/ | 已确认：官方资料入口正确，但存在自动跳转 | 常跳转至 `/en/stable/` 等，属官方站点 |
| Go testing | https://pkg.go.dev/testing | 已确认：官方资料入口正确 | HTTP 200，go.dev 官方包文档（google.cn 可解析情况下） |

*JUnit 用户指南的「当前版」会随大版本演进而变化；以团队锁定的 JUnit 版本与官方站点导航为准。*
