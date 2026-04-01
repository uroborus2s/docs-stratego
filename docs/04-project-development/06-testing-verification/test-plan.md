# 测试计划

## 单元测试

- 子模块更新与 sparse-checkout 命令是否正确生成
- `index.md` 元数据解析是否正确
- 导航、权限清单和 Nginx 规则是否一致
- 共享 bot PR 同步时，只有 `sources/*` gitlink 变化才会产生提交
- 多次 `repository_dispatch` 触发时，并发收口逻辑是否只保留最新同步结果

## 集成测试

- 使用本仓 `docs/` 生成 `.generated` 目录
- 使用生成的 MkDocs 配置完成静态构建
- 根仓 `sync-source-pointers` workflow 能否在 `source-pointer-sync-requested` 事件后形成或复用共享 bot PR
- `validate-source-pointer-pr` workflow 能否完成 `sync_sources.py --source-mode remote`、`build_site.py` 和 `mkdocs build`
- 子仓 `.github/workflows/notify-docs-stratego.yml` 是否只在目标分支的 `docs/**` 变更时触发

## 运维验证

- Docker Compose 中 Casdoor、oauth2-proxy、Nginx 是否连通
- Nginx 是否会对私有页面发起 `auth_request`
- 共享 bot PR 合并后，`Deploy Docs` 是否仍是唯一正式发布入口
- 根仓与子仓使用的 Token / Secret 是否符合最小权限边界
