# Hub Registry Field Contract

> 文档状态：V1 可执行版  
> 所属项目：`skill-q-platform` 为主，`br-ai-spec` 和 `br-ai-spec-visual` 消费  
> 核心目标：定义 Hub 资产字段契约，避免 Skill、Rule、Role、Manifest 在三个仓库中出现结构漂移。

---

## 1. 设计原则

Hub Registry 是三个仓库之间的资产契约层。所有项目必须遵循以下原则：

1. `skill-q-platform` 是 Registry 主数据源。
2. `br-ai-spec` 只消费 Registry，不私自扩展核心字段。
3. `br-ai-spec-visual` 只展示 Registry 与运行态组合后的结果，不重新定义资产结构。
4. 所有资产必须有 `id`、`kind`、`slug`、`version`、`status`、`checksum`。
5. 所有对外输出必须携带 `contractVersion`，便于后续兼容升级。

---

## 2. Registry 总结构

```ts
interface HubRegistryExport {
  contractVersion: '1.0.0';
  exportedAt: string;
  hub: {
    id: string;
    name: string;
    baseUrl: string;
  };
  assets: HubAsset[];
  manifests: HubManifest[];
}
```

---

## 3. Asset 通用字段

```ts
type AssetKind =
  | 'skill'
  | 'rule'
  | 'role'
  | 'flow'
  | 'scenario'
  | 'template'
  | 'adapter'
  | 'checklist'
  | 'quality_gate';

type AssetStatus =
  | 'draft'
  | 'submitted'
  | 'approved'
  | 'published'
  | 'deprecated'
  | 'archived';

interface HubAsset {
  id: string;
  kind: AssetKind;
  slug: string;
  name: string;
  displayName: string;
  description: string;
  version: string;
  status: AssetStatus;
  category: string;
  tags: string[];
  author: HubUserRef;
  ownerTeam?: HubTeamRef;
  targetStacks: string[];
  targetIDEs: string[];
  targetStages: DeliveryStage[];
  riskLevel: RiskLevel;
  audit: AssetAuditSnapshot;
  files: RegistryFileRef[];
  dependencies: AssetDependency[];
  checksum: string;
  createdAt: string;
  updatedAt: string;
  publishedAt?: string;
  deprecatedAt?: string;
}
```

---

## 4. Skill 字段

Skill 对应 `SKILL.md` 技能包，主要被 `br-ai-spec` 安装到 `.agents/skills/`。

```ts
interface SkillAsset extends HubAsset {
  kind: 'skill';
  skill: {
    entryFile: 'SKILL.md';
    capabilityType: 'analysis' | 'implementation' | 'review' | 'testing' | 'operation' | 'documentation';
    invocation: {
      command?: string;
      naturalLanguageTriggers: string[];
    };
    requiredInputs: SkillInputSpec[];
    expectedOutputs: SkillOutputSpec[];
    sideEffects: SideEffectSpec[];
    permissions: PermissionSpec[];
  };
}
```

### 必填校验

| 字段 | 规则 |
|---|---|
| `skill.entryFile` | 必须存在且文件名固定为 `SKILL.md` |
| `skill.capabilityType` | 必须属于枚举范围 |
| `skill.expectedOutputs` | 至少一个输出声明 |
| `sideEffects` | 如果会修改文件，必须声明 |
| `permissions` | 如果需要外部网络、Shell、文件写入，必须声明 |

---

## 5. Rule 字段

Rule 对应规则包，主要被 `br-ai-spec` 安装到 `.agents/rules/`。

```ts
interface RuleAsset extends HubAsset {
  kind: 'rule';
  rule: {
    entryFile: 'RULE.md';
    ruleType: 'coding' | 'architecture' | 'api' | 'ui' | 'testing' | 'security' | 'process';
    enforceMode: 'advisory' | 'warning' | 'blocking';
    priority: 'P0' | 'P1' | 'P2';
    appliesTo: string[];
    examples: RuleExample[];
    forbiddenPatterns?: string[];
    recommendedPatterns?: string[];
  };
}
```

### 执行语义

| `enforceMode` | 说明 |
|---|---|
| `advisory` | 仅提示，不阻塞 |
| `warning` | 产生告警，允许继续 |
| `blocking` | 违反后阻断流程或要求人工确认 |

---

## 6. Role 字段

Role 用于描述 AI 专家角色，例如 `frontend-implementer`、`code-guardian`、`requirement-analyst`。

```ts
interface RoleAsset extends HubAsset {
  kind: 'role';
  role: {
    roleName: string;
    responsibility: string[];
    allowedSkills: string[];
    requiredRules: string[];
    inputContract: string[];
    outputContract: string[];
    handoffTargets: string[];
  };
}
```

### Role 设计要求

1. 一个 Role 必须有明确职责边界。
2. Role 不直接绑定具体项目路径。
3. Role 可以依赖多个 Skill 和 Rule。
4. Role 输出必须可被下一个 Role 消费。

---

## 7. Flow 字段

Flow 用于描述流程链路，例如 `prd-to-delivery`、`bugfix-to-verification`。

```ts
interface FlowAsset extends HubAsset {
  kind: 'flow';
  flow: {
    stages: FlowStage[];
    defaultEntryRole: string;
    gates: QualityGateRef[];
    fallbackPolicy: 'stop' | 'ask-human' | 'auto-fix' | 'rollback';
  };
}

interface FlowStage {
  id: string;
  name: string;
  role: string;
  requiredInputs: string[];
  expectedOutputs: string[];
  next: string[];
}
```

---

## 8. Scenario 字段

Scenario 是面向业务场景的预设，例如“新需求开发”“低风险小修”“组件库优化”。

```ts
interface ScenarioAsset extends HubAsset {
  kind: 'scenario';
  scenario: {
    sceneType: 'new-feature' | 'bugfix' | 'refactor' | 'component-library' | 'tracking-system' | 'documentation';
    recommendedFlow: string;
    recommendedRoles: string[];
    recommendedRules: string[];
    triggerExamples: string[];
  };
}
```

---

## 9. Manifest 字段

Manifest 是方案包，不是单个资产。

```ts
interface HubManifest {
  id: string;
  slug: string;
  name: string;
  displayName: string;
  description: string;
  version: string;
  status: 'draft' | 'submitted' | 'approved' | 'published' | 'deprecated' | 'archived';
  targetStacks: string[];
  targetIDEs: string[];
  targetProjectTypes: string[];
  installMode: 'light' | 'standard' | 'strict' | 'audit-only';
  assets: ManifestAssetRef[];
  installPolicies: InstallPolicy[];
  compatibility: CompatibilitySpec;
  audit: ManifestAuditSnapshot;
  checksum: string;
  createdAt: string;
  updatedAt: string;
  publishedAt?: string;
}

interface ManifestAssetRef {
  assetId: string;
  kind: AssetKind;
  slug: string;
  version: string;
  required: boolean;
  installPath: string;
  checksum: string;
}
```

---

## 10. Version 字段

所有 Asset 和 Manifest 均采用 SemVer。

```text
MAJOR.MINOR.PATCH
```

| 版本变化 | 含义 | CLI 默认策略 |
|---|---|---|
| PATCH | 文案修复、示例补充、不改变执行语义 | 可自动升级 |
| MINOR | 新增能力、兼容字段、增加资产 | 需要确认 |
| MAJOR | 字段破坏、流程变化、删除资产 | 必须人工确认 |

---

## 11. Audit 字段

```ts
type RiskLevel = 'L0' | 'L1' | 'L2' | 'L3' | 'L4';

interface AssetAuditSnapshot {
  status: 'not_scanned' | 'passed' | 'warning' | 'blocked';
  riskLevel: RiskLevel;
  scannedAt?: string;
  scannerVersion?: string;
  findings: AuditFinding[];
  approvedBy?: string;
  approvedAt?: string;
}

interface AuditFinding {
  code: string;
  level: 'info' | 'warning' | 'error' | 'critical';
  message: string;
  file?: string;
  line?: number;
  suggestion?: string;
}
```

---

## 12. Install 字段

安装记录用于 Hub 和 Visual 统计。

```ts
interface HubInstallRecord {
  id: string;
  projectId: string;
  projectName: string;
  repositoryUrl?: string;
  manifestId: string;
  manifestVersion: string;
  installMode: string;
  cliVersion: string;
  installedAssets: ManifestAssetRef[];
  lockfileChecksum: string;
  status: 'success' | 'failed' | 'partial' | 'rolled_back';
  errorMessage?: string;
  installedAt: string;
}
```

---

## 13. 数据库表建议

### 13.1 `hub_asset`

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | varchar(64) | 主键 |
| `kind` | varchar(32) | asset 类型 |
| `slug` | varchar(128) | 唯一标识 |
| `name` | varchar(255) | 内部名称 |
| `display_name` | varchar(255) | 展示名称 |
| `description` | text | 描述 |
| `status` | varchar(32) | 状态 |
| `risk_level` | varchar(8) | 风险等级 |
| `created_at` | datetime | 创建时间 |
| `updated_at` | datetime | 更新时间 |

唯一索引：

```sql
UNIQUE KEY uk_asset_kind_slug (kind, slug)
```

### 13.2 `hub_asset_version`

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | varchar(64) | 主键 |
| `asset_id` | varchar(64) | 资产 ID |
| `version` | varchar(32) | 版本 |
| `content_json` | json | 结构化内容 |
| `file_manifest_json` | json | 文件清单 |
| `checksum` | varchar(128) | 校验和 |
| `published_at` | datetime | 发布时间 |

唯一索引：

```sql
UNIQUE KEY uk_asset_version (asset_id, version)
```

---

## 14. API 输出约束

所有对 CLI / Visual 输出的 API 统一返回：

```json
{
  "code": 0,
  "message": "成功",
  "data": {},
  "requestId": "req_xxx",
  "contractVersion": "1.0.0"
}
```

失败返回：

```json
{
  "code": 40001,
  "message": "Manifest 不存在或未发布",
  "data": null,
  "requestId": "req_xxx",
  "contractVersion": "1.0.0"
}
```

---

## 15. 验收标准

1. `skill-q-platform` 可以导出完整 Registry JSON。
2. `br-ai-spec` 可以解析 Registry 并安装 Manifest。
3. `br-ai-spec-visual` 可以读取 `hub-lock.json` 并展示资产列表。
4. 同一个 Asset 在三个仓库中的字段含义一致。
5. 任何缺失 `checksum`、`version`、`status` 的资产不得发布。
