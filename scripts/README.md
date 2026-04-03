# Scripts

- 日常同步、构建、接入、移除和 source pointer 同步统一使用 `uv run docs-stratego ...`
- `deploy_remote.sh`：面向完整仓库工作区的全量重建与 Docker 部署入口，主要用于维护机或临时运维工作区的应急回退
- 运行前需要准备 `deploy/casdoor/app.conf` 和 `deploy/oauth2-proxy/oauth2-proxy.cfg`
