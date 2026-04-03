# 测试报告

当前已覆盖：

- 稀疏同步脚本命令生成
- 站点构建器导航/权限/Nginx 规则生成
- Docker/Nginx 认证部署骨架
- `Sync Source Pointers` workflow 的事件名、并发策略、凭证接入和 CI 测试收口
- `source_pointer_sync.py` 的 remote 配置解析、变更路径识别、共享 PR 提交流程

## 本地回归结果

- 2026-04-01：执行 `uv run python -m unittest tests.test_source_sync tests.test_site_builder tests.test_deploy_stack tests.test_sync_source_pointers`
- 结果：23 个测试全部通过

待后续补充：

- 真实 GitHub 环境中的 `repository_dispatch -> Sync Source Pointers -> 共享 PR -> Squash and merge -> Deploy Docs` 端到端演练
- Casdoor 与 GitHub Provider 的联调
- 服务器实际 Nginx + oauth2-proxy + Casdoor 端到端验证
