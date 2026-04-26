# 公开工程规范参考索引

## 用途

本文件收录公开工程规范和风格指南，仅作为参考。生成企业资产时应优先遵循 Hub 资产契约、团队规范和项目实际情况。

本文件主要服务于以下场景：

1. 代码风格规则生成
2. 提交规范生成
3. 版本规范生成
4. 云原生应用设计原则参考
5. 安全风险识别
6. CI / Review / Release 质量门禁规则生成

## 规范索引

### Google Style Guides

- 链接：https://google.github.io/styleguide/
- 适用场景：多语言代码风格参考。
- 使用说明：用于参考多语言代码风格，不得替代项目已有格式化和静态检查规则。

### Airbnb JavaScript Style Guide

- 链接：https://github.com/airbnb/javascript
- 适用场景：JavaScript 风格参考。
- 使用说明：用于参考 JavaScript 代码风格，不得强制覆盖项目已有 ESLint / Prettier 配置。

### TypeScript ESLint

- 链接：https://typescript-eslint.io/
- 适用场景：TypeScript 静态检查规则。
- 使用说明：用于参考 TypeScript 静态检查、Lint 规则和类型安全实践。

### Conventional Commits

- 链接：https://www.conventionalcommits.org/en/v1.0.0/
- 适用场景：提交信息规范、版本管理。
- 使用说明：用于参考提交信息格式和自动化版本管理实践。

### Semantic Versioning

- 链接：https://semver.org/
- 适用场景：版本号规范。
- 使用说明：用于参考版本号 MAJOR.MINOR.PATCH 规则和兼容性说明。

### Twelve-Factor App

- 链接：https://12factor.net/
- 适用场景：云原生应用设计原则。
- 使用说明：用于参考云原生应用配置、依赖、构建、发布、进程和日志等设计原则。

### OWASP

- 链接：https://owasp.org/
- 适用场景：Web 安全、API 安全、认证授权风险。
- 使用说明：用于参考 Web 安全、API 安全、认证、授权、输入校验和常见风险识别。

## 使用原则

1. 公开规范只能作为参考，不能替代项目内规则。
2. 生成资产时要转化为可执行、可审核、可测试的规则。
3. 不确定适配性时，标记为“建议人工确认”。
4. 安全、权限、数据、发布相关内容默认提高风险等级。
5. 风格规范不得凌驾于项目现有 ESLint、Prettier、Checkstyle、Formatter 或 CI 规则。
6. 涉及提交规范和版本规范时，应结合项目现有发布流程，不得强行套用。
7. 涉及安全规范时，应输出风险点、验证方式和最低防护要求。
8. 生成工程规范资产时，应优先输出规则、理由、适用范围、例外情况、验证方式。
9. 不应把公开规范原文复制为团队规范。
10. 若项目已存在团队规范，应以团队规范为准，公开规范仅作为补充参考。

## 链接校验摘要

| 资料项 | 链接 | 校验结果 | 备注 |
|---|---|---|---|
| Google Style Guides | https://google.github.io/styleguide/ | 已确认：官方资料入口正确 | HTTP 200，Google GitHub Pages 上托管的公开规范集 |
| Airbnb JavaScript Style Guide | https://github.com/airbnb/javascript | 需要人工确认：无法确认官方性或可访问性 | 自动化环境对 github.com 返回异常（HTTP 000）；该仓库为 Airbnb 组织官方维护的公开项目，但请在可访问 GitHub 的网络中复核 |
| TypeScript ESLint | https://typescript-eslint.io/ | 已确认：官方资料入口正确 | HTTP 200，ts-eslint 项目官方站 |
| Conventional Commits | https://www.conventionalcommits.org/en/v1.0.0/ | 已确认：官方资料入口正确 | HTTP 200，规范 1.0.0 正式页 |
| Semantic Versioning | https://semver.org/ | 已确认：官方资料入口正确 | HTTP 200，SemVer 规范官网 |
| Twelve-Factor App | https://12factor.net/ | 已确认：官方资料入口正确 | HTTP 200，12factor 官方站点 |
| OWASP | https://owasp.org/ | 已确认：官方资料入口正确 | HTTP 200，OWASP 组织官网 |

*Airbnb 与 Google 属于社区/组织级公开参考，其「官方性」以发布主体为准，不替代你司内部规约。*
