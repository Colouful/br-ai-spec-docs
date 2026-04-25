# CLI Command Design

## 命令总览

```bash
npx @ex/ai-spec-auto hub login
npx @ex/ai-spec-auto hub search react
npx @ex/ai-spec-auto hub install enterprise-react-standard
npx @ex/ai-spec-auto hub sync
npx @ex/ai-spec-auto hub diff
npx @ex/ai-spec-auto hub upgrade
npx @ex/ai-spec-auto hub rollback
```

## install 流程

读取项目环境 → 拉取 Manifest Export → 校验兼容性 → 生成安装计划 → 展示中文安装预览 → 创建备份 → 下载资产 → 写入本地文件 → 生成 `hub-lock.json` → 上报安装结果。

## dry-run

`--dry-run` 只输出安装计划，不写入文件，不生成锁文件，不上报安装成功。

## 幂等规则

重复安装时，checksum 一致则跳过；checksum 不一致则提示冲突；缺失文件则补齐；多余文件不删除，只提示。

## 错误处理

Hub 连接失败、Token 失效、Manifest 不存在、版本冲突、required 资产下载失败时必须输出中文错误。required 失败需要回滚；optional 失败允许跳过但必须警告。

