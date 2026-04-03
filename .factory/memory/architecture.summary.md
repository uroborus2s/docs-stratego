# 架构摘要

- 核心链路：源仓 -> `git submodule update --init` -> 子仓内 `fetch + checkout` -> `sparse-checkout set /docs/ /docs/**` -> `sources/<repo>/docs` -> `docs-stratego build` -> `.generated/` -> `mkdocs build` -> `site/`
- 鉴权策略：Nginx 根据生成的私有路径规则调用 oauth2-proxy，oauth2-proxy 再对接 Casdoor
- 特殊规则：导航和权限都由根 `docs/index.md` 的全站清单决定，默认关闭匿名全文搜索
