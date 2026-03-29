# 实施计划

1. 定义源仓 `docs/` 标准和 `index.md` 标准
2. 替换旧同步逻辑，改为 Git submodule + sparse-checkout
3. 实现站点构建器，生成导航和权限清单
4. 接入 Casdoor、oauth2-proxy 和 Nginx Docker 部署骨架
5. 删除旧双站点、旧挂载、旧子模块逻辑
6. 用本仓文档作为首个标准源完成构建验证
