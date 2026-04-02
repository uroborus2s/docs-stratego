# API 摘要

- 外部业务 API：当前无
- 关键契约：源仓 `docs/` 目录标准、根 `docs/index.md` 全站清单格式、页面权限清单格式
- 关键命令：`uv run docs-stratego sync --project-root .`、`uv run docs-stratego source add --project-root . ...`
- 关键产物：`.generated/authz/permissions.json`、`.generated/nginx/private_locations.conf`
