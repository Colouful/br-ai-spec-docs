# 中台金融系统样板需求完整链路

样板需求：新增产品配置管理模块  
技术栈：Vue + Vite + Vuex、Spring Boot、MySQL、Redis、MQ  
任务等级：L2 标准需求  
执行模式：完整 OpenSpec + Task DAG + 多执行 Agent + Git worktree + Test Gate + Evidence

---

## 1. 原始需求

在中台金融系统中新增“产品配置管理”模块，运营人员可维护金融产品配置，包括产品名称、产品编码、产品类型、状态、授信额度范围、利率范围、启用/禁用状态等。配置变更后需要通知相关业务模块刷新缓存。

---

## 2. 需求边界

### 2.1 本期包含

1. 产品配置列表。
2. 新增产品配置。
3. 编辑产品配置。
4. 启用 / 禁用产品配置。
5. 后端 CRUD 接口。
6. MySQL 表结构。
7. Redis 缓存刷新策略。
8. MQ 配置变更通知。
9. 前后端基础测试。
10. 验收证据落盘。

### 2.2 本期不包含

1. 金融产品定价模型。
2. 风控规则引擎。
3. 审批流。
4. 多租户隔离。
5. 生产数据迁移。
6. 线上发布自动化。

---

## 3. OpenSpec 结构

```text
openspec/changes/add-product-config-management/
├── proposal.md
├── design.md
├── tasks.md
└── specs/
    └── product-config/spec.md
```

### 3.1 proposal.md 示例

```md
# 新增产品配置管理模块

## Why

当前金融中台的产品配置依赖人工维护或硬编码，缺少统一后台管理能力，导致配置变更效率低、风险高、不可追溯。

## What Changes

- 新增产品配置管理页面。
- 新增产品配置 CRUD 接口。
- 新增 product_config 表。
- 新增产品配置缓存刷新逻辑。
- 新增产品配置变更 MQ 通知。

## Impact

- 前端新增菜单与页面。
- 后端新增 Controller / Service / Mapper。
- 数据库新增表。
- Redis 新增缓存 key。
- MQ 新增产品配置变更消息。
```

### 3.2 design.md 示例

```md
# 技术设计

## 前端设计

- 页面路径：/product/config
- Vuex 模块：productConfig
- 组件：ProductConfigList.vue、ProductConfigForm.vue

## 后端设计

- Controller：ProductConfigController
- Service：ProductConfigService
- Mapper：ProductConfigMapper
- DTO：ProductConfigCreateRequest、ProductConfigUpdateRequest

## 数据库设计

表名：product_config

## 缓存设计

Redis Key：product_config:{productCode}

## MQ 设计

Topic：product-config-change
```

### 3.3 tasks.md 示例

```md
# 任务清单

- [ ] 定义数据库表结构
- [ ] 定义 API 契约
- [ ] 实现后端接口
- [ ] 实现前端页面
- [ ] 实现缓存刷新
- [ ] 实现 MQ 通知
- [ ] 编写测试用例
- [ ] 生成验收证据
```

---

## 4. API 契约

### 4.1 创建产品配置

```http
POST /api/admin/product-config
Content-Type: application/json
```

请求：

```json
{
  "productCode": "CASH_LOAN_BASIC",
  "productName": "基础现金贷产品",
  "productType": "CASH_LOAN",
  "minCreditAmount": 1000,
  "maxCreditAmount": 50000,
  "minRate": 0.01,
  "maxRate": 0.36,
  "status": "draft"
}
```

响应：

```json
{
  "code": 0,
  "message": "成功",
  "data": {
    "id": 1001
  }
}
```

### 4.2 查询产品配置列表

```http
GET /api/admin/product-config?pageNo=1&pageSize=20&status=active
```

---

## 5. MySQL 表设计

```sql
CREATE TABLE product_config (
  id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
  product_code VARCHAR(64) NOT NULL COMMENT '产品编码',
  product_name VARCHAR(128) NOT NULL COMMENT '产品名称',
  product_type VARCHAR(64) NOT NULL COMMENT '产品类型',
  min_credit_amount DECIMAL(18,2) NOT NULL COMMENT '最小授信额度',
  max_credit_amount DECIMAL(18,2) NOT NULL COMMENT '最大授信额度',
  min_rate DECIMAL(8,4) NOT NULL COMMENT '最小利率',
  max_rate DECIMAL(8,4) NOT NULL COMMENT '最大利率',
  status VARCHAR(32) NOT NULL DEFAULT 'draft' COMMENT '状态',
  deleted TINYINT NOT NULL DEFAULT 0 COMMENT '是否删除',
  created_by VARCHAR(64) DEFAULT NULL COMMENT '创建人',
  updated_by VARCHAR(64) DEFAULT NULL COMMENT '更新人',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  UNIQUE KEY uk_product_code (product_code),
  KEY idx_status (status),
  KEY idx_product_type (product_type)
) COMMENT='产品配置表';
```

---

## 6. Task DAG 示例

```json
{
  "tasks": [
    {
      "taskId": "task_openspec_product_config",
      "title": "生成产品配置 OpenSpec",
      "dependsOn": [],
      "writeSet": ["openspec/changes/add-product-config-management/**"],
      "lockKeys": ["openspec:product-config"],
      "executorType": "docs",
      "parallelizable": false
    },
    {
      "taskId": "task_db_product_config",
      "title": "新增 product_config 表设计",
      "dependsOn": ["task_openspec_product_config"],
      "writeSet": ["backend/src/main/resources/db/migration/**"],
      "lockKeys": ["db:product_config"],
      "executorType": "database",
      "parallelizable": false
    },
    {
      "taskId": "task_contract_product_config_api",
      "title": "定义产品配置 API 契约",
      "dependsOn": ["task_openspec_product_config", "task_db_product_config"],
      "writeSet": ["openspec/changes/add-product-config-management/specs/product-config/**"],
      "lockKeys": ["api:/product-config"],
      "executorType": "architect",
      "parallelizable": false
    },
    {
      "taskId": "task_backend_product_config_api",
      "title": "实现产品配置后端接口",
      "dependsOn": ["task_contract_product_config_api"],
      "writeSet": ["backend/src/main/java/**/ProductConfig*.java"],
      "lockKeys": ["module:backend-product-config"],
      "executorType": "backend",
      "parallelizable": true
    },
    {
      "taskId": "task_frontend_product_config_page",
      "title": "实现产品配置前端页面",
      "dependsOn": ["task_contract_product_config_api"],
      "writeSet": ["frontend/src/views/product-config/**", "frontend/src/store/modules/productConfig*.js"],
      "lockKeys": ["route:/product-config", "vuex:productConfig"],
      "executorType": "frontend",
      "parallelizable": true
    },
    {
      "taskId": "task_qa_product_config",
      "title": "编写产品配置测试用例",
      "dependsOn": ["task_contract_product_config_api"],
      "writeSet": ["backend/src/test/**/ProductConfig*.java", "frontend/src/**/*.spec.*"],
      "lockKeys": ["test:product-config"],
      "executorType": "qa",
      "parallelizable": true
    }
  ]
}
```

---

## 7. Git worktree 执行计划

### 7.1 Change Branch

```bash
git checkout -b ai/change/add-product-config-management-20260428
```

### 7.2 Task Worktree

```bash
git worktree add ~/.br-spec/worktrees/mid-platform/run_001/task-db ai/task/product-config-db
git worktree add ~/.br-spec/worktrees/mid-platform/run_001/task-backend ai/task/product-config-backend
git worktree add ~/.br-spec/worktrees/mid-platform/run_001/task-frontend ai/task/product-config-frontend
git worktree add ~/.br-spec/worktrees/mid-platform/run_001/task-qa ai/task/product-config-qa
```

### 7.3 并行执行策略

第一阶段串行：

1. OpenSpec。
2. DB Schema。
3. API Contract。

第二阶段并行：

1. Backend API。
2. Frontend Page。
3. QA Test。
4. Docs Evidence。

第三阶段串行：

1. Merge。
2. Verify。
3. Repair。
4. Report。

---

## 8. Agent 分工

| Agent | 输入 | 输出 |
|---|---|---|
| Product Agent | 原始需求 | 需求边界、验收点 |
| Architect Agent | 需求和技术栈 | 技术设计、Task DAG |
| Database Agent | 业务字段 | 表结构、索引、迁移建议 |
| Backend Expert Agent | API 契约 | 后端实现建议 |
| Frontend Expert Agent | 页面需求 | 前端实现建议 |
| QA Agent | 验收标准 | 测试计划、测试用例 |
| Executor Agent | Task 包 | Patch Bundle |
| Merge Agent | Patch Bundle | Merge Report |
| Repair Agent | 测试失败结果 | 修复 Patch |
| Docs Agent | 证据 | Final Report |

---

## 9. 验收清单

```md
# 产品配置管理模块验收清单

## 功能验收
- [ ] 产品配置列表可分页查询
- [ ] 产品配置可新增
- [ ] 产品配置可编辑
- [ ] 产品配置可启用
- [ ] 产品配置可禁用
- [ ] 产品编码唯一校验生效
- [ ] 已删除数据不展示

## 前端验收
- [ ] 页面路由正常
- [ ] 表格分页正常
- [ ] 表单校验正常
- [ ] 状态展示正确
- [ ] 接口错误提示为中文
- [ ] 无明显样式错乱

## 后端验收
- [ ] Controller 参数校验完整
- [ ] Service 事务边界清晰
- [ ] product_code 唯一约束生效
- [ ] Redis 缓存刷新逻辑正确
- [ ] MQ 消息发送具备失败日志

## 测试验收
- [ ] 后端单元测试通过
- [ ] 接口测试通过
- [ ] 前端单测通过
- [ ] 关键流程回归通过

## 证据验收
- [ ] OpenSpec 已生成
- [ ] Task DAG 已落盘
- [ ] worktree-index 已生成
- [ ] evidence-index 已生成
- [ ] final-report 已生成
```

---

## 10. Evidence 目录示例

```text
.ai-spec-local/runs/run_001/
├── run.bundle.json
├── task-dag.json
├── worktree-index.json
├── evidence-index.json
├── merge-report.md
├── final-report.md
└── artifacts/
    ├── test-plan.md
    ├── test-cases.md
    ├── acceptance-checklist.md
    ├── backend-unit-test-result.md
    ├── frontend-unit-test-result.md
    ├── api-test-result.md
    ├── diff-summary.md
    └── self-repair-log.md
```

---

## 11. 最终交付报告摘要示例

```md
# 最终交付报告：新增产品配置管理模块

## 结论

本次 L2 标准需求已完成开发、合并、测试与验收。所有强制证据已落盘。

## 修改范围

- 新增 product_config 表。
- 新增后端 ProductConfigController / Service / Mapper。
- 新增前端产品配置列表与表单页面。
- 新增 Redis 缓存刷新逻辑。
- 新增 MQ 变更通知逻辑。

## 测试结果

- 后端单测：通过。
- 前端单测：通过。
- API 测试：通过。
- 验收清单：全部通过。

## 风险

- MQ 失败重试策略本期仅记录日志，后续可增强为补偿机制。
```
