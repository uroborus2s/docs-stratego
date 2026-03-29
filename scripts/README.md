# Scripts

- `sync_sources.py`：通过 Git submodule + sparse-checkout 同步外部源仓的 `docs/`
- `build_site.py`：生成单站点所需的导航、权限清单、Nginx 规则和 MkDocs 配置
- `deploy_remote.sh`：面向完整仓库工作区的全量重建与 Docker 部署入口，主要用于维护机或临时运维工作区的应急回退
- 运行前需要准备 `deploy/casdoor/app.conf` 和 `deploy/oauth2-proxy/oauth2-proxy.cfg`
