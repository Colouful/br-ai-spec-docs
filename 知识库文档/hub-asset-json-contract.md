# Hub 资产草稿 JSON 契约

所有可进入 Hub 审核流程的资产草稿，必须使用严格 JSON 输出。

## 顶层结构

{
  "assetPackage": {
    "name": "",
    "slug": "",
    "version": "0.1.0",
    "status": "draft",
    "targetDomain": "",
    "languages": [],
    "frameworks": [],
    "projectKinds": [],
    "scope": "team",
    "qualityLevel": "enterprise",
    "assets": []
  },
  "qualityReport": {
    "score": 0,
    "passed": false,
    "criticalIssues": [],
    "warnings": [],
    "suggestions": []
  },
  "importAdvice": {
    "recommended": false,
    "reason": "",
    "nextStep": ""
  }
}

## assets 数组中的资产结构

{
  "kind": "rule | skill | flow | manifest | agent-profile",
  "name": "",
  "slug": "",
  "version": "0.1.0",
  "status": "draft",
  "riskLevel": "low | medium | high",
  "purpose": "",
  "whenToUse": [],
  "inputs": [],
  "outputs": [],
  "steps": [],
  "constraints": [],
  "forbiddenActions": [],
  "acceptanceCriteria": [],
  "fallbackStrategy": {
    "action": "block | retry | diagnose | human-review",
    "description": ""
  },
  "testCases": [],
  "telemetryTags": []
}

## 强制规则

1. status 必须是 draft。
2. version 默认 0.1.0。
3. slug 只能使用小写字母、数字和中横线。
4. JSON 不允许注释。
5. JSON 不允许尾逗号。
6. 不允许用 Markdown 正文替代 JSON。
7. 质量分低于 80 时，qualityReport.passed 必须是 false。
8. 质量分低于 80 时，importAdvice.recommended 必须是 false。
9. 资产不允许直接发布，只能建议进入审核流程。
10. 不允许要求用户提供内部源码、密钥、环境变量。