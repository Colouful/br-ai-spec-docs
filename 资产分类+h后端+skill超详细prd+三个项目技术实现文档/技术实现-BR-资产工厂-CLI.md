# 技术实现文档：br-ai-spec Asset Factory CLI

## 1. 实现目标

`br-ai-spec` 新增 Asset Factory CLI，支持：

1. 本地生成 Role / Skill / Rule / Flow / Manifest。
2. 本地校验资产质量。
3. 自动修复低风险结构问题。
4. 打包生成资产包。
5. 导入 skill-q-platform Hub。
6. 识别 Java Spring Boot 项目。
7. 推荐适配 Manifest。
8. 与现有 hub install / sync / diff / upgrade / rollback 联动。

---

## 2. 目录结构

```text
br-ai-spec/
├── bin/
│   ├── commands/
│   │   └── asset-factory/
│   │       ├── index.js
│   │       ├── plan.js
│   │       ├── generate.js
│   │       ├── validate.js
│   │       ├── fix.js
│   │       ├── package.js
│   │       ├── import.js
│   │       └── recommend.js
│   └── asset-factory/
│       ├── planner.js
│       ├── generator.js
│       ├── renderer.js
│       ├── validator.js
│       ├── fixer.js
│       ├── scorer.js
│       ├── packager.js
│       ├── importer.js
│       ├── detector.js
│       ├── checksum.js
│       └── types.js
├── .agents/
│   └── skills/
│       └── asset-factory/
│           ├── SKILL.md
│           ├── README.md
│           ├── templates/
│           ├── examples/
│           ├── schemas/
│           └── quality/
└── generated-assets/
```

---

## 3. Asset Factory Skill 结构

```text
.agents/skills/asset-factory/
├── SKILL.md
├── README.md
├── templates/
│   ├── skill.template.md
│   ├── rule.template.md
│   ├── role.template.md
│   ├── flow.template.md
│   ├── scenario.template.md
│   └── manifest.template.json
├── examples/
│   ├── backend-java-springboot/
│   └── generic/
├── schemas/
│   ├── skill.schema.json
│   ├── rule.schema.json
│   ├── role.schema.json
│   ├── flow.schema.json
│   └── manifest.schema.json
└── quality/
    ├── checklist.md
    ├── scoring-rubric.md
    └── forbidden-patterns.md
```

---

## 4. CLI 命令

### 4.1 生成计划

```bash
npx @ex/ai-spec-auto asset-factory plan   --profile backend-java-springboot   --scenario new-rest-api   --types role,skill,rule,flow,manifest
```

### 4.2 执行生成

```bash
npx @ex/ai-spec-auto asset-factory generate   --profile backend-java-springboot   --scenario new-rest-api   --types role,skill,rule,flow,manifest   --level enterprise
```

### 4.3 校验

```bash
npx @ex/ai-spec-auto asset-factory validate   --source generated-assets/backend-java-springboot-new-rest-api
```

### 4.4 自动修复

```bash
npx @ex/ai-spec-auto asset-factory fix   --source generated-assets/backend-java-springboot-new-rest-api
```

### 4.5 打包

```bash
npx @ex/ai-spec-auto asset-factory package   --source generated-assets/backend-java-springboot-new-rest-api
```

### 4.6 导入 Hub

```bash
npx @ex/ai-spec-auto asset-factory import   --source generated-assets/backend-java-springboot-new-rest-api   --hub http://localhost:3000   --status draft
```

### 4.7 推荐 Manifest

```bash
npx @ex/ai-spec-auto hub recommend --hub http://localhost:3000
```

---

## 5. 配置文件

支持：

```json
{
  "profile": "backend-java-springboot",
  "scenario": "new-rest-api",
  "assetTypes": ["role", "skill", "rule", "flow", "manifest"],
  "qualityLevel": "enterprise",
  "includeExamples": true,
  "includeBadExamples": true,
  "includeChecklists": true,
  "includeTests": true,
  "outputLanguage": "zh-CN",
  "outputDir": "generated-assets/backend-java-springboot-new-rest-api"
}
```

执行：

```bash
npx @ex/ai-spec-auto asset-factory generate --config asset-factory.config.json
```

---

## 6. 模板要求

### 6.1 Skill

必须包含：

```text
Skill 基本信息
使用时机
输入要求
执行流程
输出格式
示例代码
质量要求
失败处理
验收标准
```

### 6.2 Rule

必须包含：

```text
规则基本信息
规则目的
必须遵守
禁止行为
推荐实践
正确示例
错误示例
检查清单
适用场景
不适用场景
```

### 6.3 Role

必须包含：

```text
角色定位
职责范围
不负责的事情
输入信息
输出结果
协作关系
质量标准
```

### 6.4 Flow

必须包含：

```text
流程目标
适用场景
流程阶段
阶段说明
失败处理
验收标准
```

### 6.5 Manifest

必须包含：

```json
{
  "schemaVersion": "1.0.0",
  "slug": "backend-java-springboot-api-standard",
  "name": "Java Spring Boot 接口开发标准方案包",
  "domain": "backend",
  "language": "Java",
  "frameworks": ["Spring Boot"],
  "scenario": "new-rest-api",
  "version": "1.0.0",
  "installMode": "standard",
  "roles": [],
  "skills": [],
  "rules": [],
  "flows": [],
  "policies": {
    "requirePreview": true,
    "allowOverwrite": false,
    "allowLocalPatch": true,
    "riskLevel": "L1"
  }
}
```

---

## 7. 生成输出结构

```text
generated-assets/backend-java-springboot-new-rest-api/
├── roles/
│   └── backend-implementer/ROLE.md
├── skills/
│   └── springboot-rest-api-implementation-skill/SKILL.md
├── rules/
│   └── springboot-controller-rule/RULE.md
├── flows/
│   └── springboot-new-rest-api-flow/FLOW.md
├── manifests/
│   └── backend-java-springboot-api-standard/manifest.json
└── reports/
    ├── quality-report.md
    ├── quality-report.json
    └── import-preview.md
```

---

## 8. 校验器设计

### 8.1 校验结果结构

```ts
type AssetValidationResult = {
  assetKind: string;
  assetSlug: string;
  filePath: string;
  passed: boolean;
  score: number;
  issues: Array<{
    level: 'error' | 'warning' | 'info';
    code: string;
    message: string;
    suggestion?: string;
  }>;
};
```

### 8.2 阻断规则

以下情况直接 blocked：

1. 缺少核心章节。
2. 没有输入输出。
3. 没有适用场景。
4. 示例代码明显与技术栈不匹配。
5. 含有密钥、Token、密码。
6. Manifest 引用不存在资产。
7. slug 重复。

### 8.3 评分

```text
结构完整性 20%
内容清晰度 20%
技术准确性 20%
示例质量 15%
可执行性 15%
风险控制 10%
```

---

## 9. 自动修复

允许修复：

```text
缺少章节
标题层级
字段顺序
slug 大小写
缺少检查清单
缺少占位示例
```

不允许修复：

```text
技术准确性错误
安全规则错误
数据库规范错误
权限相关内容
生产部署相关内容
```

修复后生成：

```text
reports/fix-report.md
reports/fix-report.json
```

---

## 10. 打包格式

```text
asset-package.zip
├── package.json
├── roles/
├── skills/
├── rules/
├── flows/
├── manifests/
└── reports/
```

package.json：

```json
{
  "schemaVersion": "1.0.0",
  "name": "backend-java-springboot-new-rest-api",
  "profile": "backend-java-springboot",
  "scenario": "new-rest-api",
  "createdAt": "2026-04-24T10:00:00.000Z",
  "assets": []
}
```

---

## 11. Hub 导入

导入规则：

1. 读取 source 或 zip。
2. 读取 quality-report.json。
3. 拒绝导入 blocked 资产。
4. 调用 Hub API。
5. 处理冲突。
6. 输出导入结果。

状态：

```text
imported
skipped
failed
conflicted
```

---

## 12. Java / Spring Boot 项目识别

检测文件：

```text
pom.xml
build.gradle
src/main/java
src/main/resources/application.yml
src/main/resources/application.properties
```

检测依赖：

```text
spring-boot-starter-web
spring-boot-starter-validation
spring-cloud-starter
spring-cloud-starter-openfeign
mybatis-spring-boot-starter
spring-boot-starter-data-jpa
```

输出：

```json
{
  "domain": "backend",
  "language": "Java",
  "frameworks": ["Spring Boot", "Spring MVC"],
  "buildTool": "Maven",
  "orm": ["MyBatis"],
  "architecture": ["service"],
  "confidence": 0.92
}
```

---

## 13. 推荐 Manifest

逻辑：

1. 检测当前项目技术栈。
2. 请求 Hub 推荐接口。
3. 输出推荐 Manifest。
4. 支持一键安装。

输出示例：

```text
检测到当前项目技术栈：

语言：Java
框架：Spring Boot
构建工具：Maven
数据访问：MyBatis

推荐方案包：

1. Java Spring Boot 标准研发方案包
   标识：backend-java-springboot-standard
   匹配度：92%
   推荐原因：检测到 Spring Boot Web、Maven、MyBatis 依赖
```

---

## 14. 与 hub install 联动

生成资产导入 Hub 并发布 Manifest 后：

```bash
npx @ex/ai-spec-auto hub install backend-java-springboot-api-standard --hub http://localhost:3000
```

安装后生成：

```text
.agents/registry/
.ai-spec/hub-lock.json
```

---

## 15. 安全要求

1. 不上传源码。
2. 不上传绝对路径。
3. 不上传用户名。
4. 扫描密钥、Token、密码。
5. 默认导入 draft。
6. 高风险资产阻断发布。
7. CLI 输出全部中文。

---

## 16. 测试用例

### 单元测试

1. planner 生成计划。
2. renderer 渲染模板。
3. validator 校验 Skill。
4. validator 校验 Rule。
5. validator 校验 Manifest。
6. fixer 修复缺失章节。
7. packager 生成 zip。
8. detector 识别 Spring Boot。

### 集成测试

1. plan → generate → validate → package。
2. generate → validate → import Hub。
3. recommend → install Manifest。
4. 低分资产阻断导入。
5. slug 冲突提示。

---

## 17. 验收标准

1. 可以生成 backend-java-springboot-new-rest-api 资产包。
2. 可以输出质量报告。
3. 可以校验每个资产分数。
4. 可以自动修复低风险结构问题。
5. 可以打包 zip。
6. 可以导入 Hub 草稿。
7. 可以识别 Java Spring Boot 项目。
8. 可以推荐 Spring Boot Manifest。
9. CLI 输出全部中文。
10. 错误提示明确可执行。
