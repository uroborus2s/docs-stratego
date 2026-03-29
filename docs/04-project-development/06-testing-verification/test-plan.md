# 测试计划

## 单元测试

- 子模块更新与 sparse-checkout 命令是否正确生成
- `index.md` 元数据解析是否正确
- 导航、权限清单和 Nginx 规则是否一致

## 集成测试

- 使用本仓 `docs/` 生成 `.generated` 目录
- 使用生成的 MkDocs 配置完成静态构建

## 运维验证

- Docker Compose 中 Casdoor、oauth2-proxy、Nginx 是否连通
- Nginx 是否会对私有页面发起 `auth_request`
