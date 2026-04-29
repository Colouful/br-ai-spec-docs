# AI 研发控制平面 V0.1 协议交付包

包含内容：

- `docs/enterprise-ai-control-plane-v0.1-protocol.md`：主协议文档。
- `docs/repo-implementation-checklist.md`：三仓改造实施清单。
- `schemas/*.schema.json`：V0.1 JSON Schema 硬契约。
- `examples/*.json`：中台金融系统样板配置和 Task DAG 示例。

推荐使用顺序：

1. 先阅读主协议文档。
2. 再阅读三仓实施清单。
3. 将 `schemas/` 放入 `br-ai-spec` 的协议校验模块。
4. 使用 `examples/` 作为第一条中台金融系统样板链路的输入。
