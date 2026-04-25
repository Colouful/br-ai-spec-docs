# Product Requirements Document

## 目标

本文档服务于 `skill-q-platform`、`br-ai-spec`、`br-ai-spec-visual` 三仓协同开发。核心目标是打通：资产创建 → Manifest 方案包编排 → CLI 安装同步 → Visual 运行态观测 → Hub 质量回流。

## 产品定位

`skill-q-platform` 从 Skill / Rule 分享站升级为 AI 工程资产 Hub；`br-ai-spec` 作为 CLI 执行底座；`br-ai-spec-visual` 作为运行态观测和治理看板。Manifest 是核心产品抓手，把零散资产组合成可安装、可审计、可回滚的团队级方案包。

## 用户角色

| 角色 | 诉求 | 权限 |
|---|---|---|
| 平台管理员 | 管理资产、审核发布、治理默认方案 | 全部 |
| 架构师 | 定义团队标准方案包 | 创建、审核、发布 |
| 资产贡献者 | 上传 Skill / Rule / Role | 创建、编辑、提交 |
| 普通开发者 | 在项目中安装方案包 | 查询、安装 |
| 项目负责人 | 看项目接入和风险 | 查看画像 |

## V1 范围

必须完成：Manifest 创建、资产编排、发布、Export API、CLI install/sync/diff、hub-lock.json、Visual 项目资产画像、安装记录回流。暂不做：智能推荐算法、商业化市场、复杂组织权限、在线执行 Agent。

## 核心验收标准

1. Hub 可以创建并发布 Manifest v1.0.0。
2. CLI 可以按 Manifest ID 安装。
3. 本地生成 `.agents/registry`、`.ai-spec`、`hub-lock.json`。
4. Visual 可以展示项目当前 Manifest 与资产版本。
5. Hub 可以看到安装记录和运行态回流。
6. 所有命令行提示使用中文。

