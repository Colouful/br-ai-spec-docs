# Hub API Contract

## 通用响应

```json
{ "success": true, "code": "OK", "message": "操作成功", "data": {}, "requestId": "req_xxx" }
```

## 核心接口

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | /api/hub/assets | 查询资产 |
| POST | /api/hub/assets | 创建资产 |
| POST | /api/hub/assets/:id/submit | 提交审核 |
| POST | /api/hub/assets/:id/approve | 审核通过 |
| GET | /api/hub/manifests | 查询 Manifest |
| POST | /api/hub/manifests | 创建 Manifest |
| POST | /api/hub/manifests/:id/publish | 发布 Manifest |
| GET | /api/hub/manifests/:id/export | CLI 导出 Manifest |
| POST | /api/hub/install/preview | 安装预览 |
| POST | /api/hub/install/report | 安装结果上报 |
| POST | /api/hub/runtime/report | 运行态回流 |

## Export API 响应

Export API 必须返回 manifest、version、checksum、installPolicy、assets、contentUrl、installPath、required，不允许暴露数据库内部字段。CLI 只消费 Export API。

## 错误码

`UNAUTHORIZED`、`FORBIDDEN`、`ASSET_NOT_FOUND`、`MANIFEST_NOT_FOUND`、`VERSION_CONFLICT`、`INVALID_MANIFEST`、`ASSET_DEPRECATED`、`INSTALL_REPORT_FAILED`、`RUNTIME_REPORT_FAILED`。

