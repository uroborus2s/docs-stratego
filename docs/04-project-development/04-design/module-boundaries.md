# 模块边界

| 模块 | 输入 | 输出 | 职责 |
| --- | --- | --- | --- |
| `source-sync` | 源仓地址、分支、`docs_path` | `sources/<repo>/docs` | 稀疏同步文档目录 |
| `site-builder` | `docs/` 标准目录 | 导航、权限清单、Nginx 私有规则、MkDocs 配置 | 解释元数据并生成构建输入 |
| `mkdocs-builder` | `.generated/site_docs`, `.generated/mkdocs.generated.yml` | `site/` | 生成静态页面 |
| `casdoor` | 用户、GitHub Provider、SQLite | 登录服务 | 负责身份认证 |
| `oauth2-proxy` | Casdoor OIDC | `auth_request` 接口 | 负责登录态验证 |
| `nginx` | 静态站点、私有路径规则 | 最终网站 | 负责页面访问控制 |
