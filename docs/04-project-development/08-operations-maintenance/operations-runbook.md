# 运维手册

## 日常操作

- 重新同步源仓 `docs/`：`uv run docs-stratego sync --config config/source-repos.json --project-root .`
- 重新生成导航与权限清单：`uv run docs-stratego build --config config/source-repos.json --project-root . --output-dir .generated`
- 手动补跑共享 bot PR：`uv run docs-stratego source sync-pointers --config config/source-repos.json --project-root .`
- 重建静态站点：`uv run mkdocs build -f .generated/mkdocs.generated.yml -d site`
- 重启部署栈：`docker compose -f deploy/docker-compose.yml up -d`

## 排障点

- 首页或公开页一打开就跳登录：优先检查宿主机 `Nginx` 是否把 `auth_request` 写到了 `server` 根层或 `location /`；公开页只能通过 `include /etc/nginx/snippets/docs-stratego/private_locations.conf` 命中私有 URL 时再触发登录
- 页面未出现在导航：检查根 `docs/index.md` 是否声明了该页面路径
- 页面应该私有却未被拦截：检查 `permissions.json` 和 `private_locations.conf`
- 私有链接没有弹出站内登录框：检查最新站点静态资源是否已发布，并确认浏览器没有拦截站点打开的小窗口
- 私有页面图片或附件仍可匿名访问：检查资源是否放在页面目录或 `assets/` 下，以及是否进入权限清单
- 登录后无法返回原页：检查 oauth2-proxy 的 `redirect_url` 和 Nginx `X-Auth-Request-Redirect`
- GitHub 登录失败：检查 Casdoor 中 GitHub Provider 的回调地址、Client ID 和 Client Secret
