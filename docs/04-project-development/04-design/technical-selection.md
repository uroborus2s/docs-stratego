# 技术选型与工程规则

## 选型

- 静态站点生成：MkDocs + Material
- 元数据格式：Markdown + YAML front matter
- 同步方式：Git submodule + sparse-checkout
- 认证服务：Casdoor
- 认证代理：oauth2-proxy
- 网关：宿主机 Nginx
- 会话存储：Docker 网络内现有 Redis
- 自动化脚本：Python + uv

## 关键工程规则

- 根仓不改写源仓内容
- 只有源仓根 `docs/index.md` 负责导航和页面权限
- 所有目录都必须有 `index.md`
- 所有页面都必须在根 `docs/index.md` 的 `mkdocs.nav` 中显式声明
- 任何未声明页面都直接让构建失败
- 单站点模式下默认不启用匿名全文搜索，以避免私有信息被索引
- 宿主机 Nginx 负责静态站点、私有页面拦截和 Casdoor 外部入口
- oauth2-proxy 通过 Redis 保存会话，不使用进程内临时会话
