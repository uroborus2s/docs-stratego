# 认证数据存储设计

## 当前策略

认证数据交给 Casdoor 保存。当前正式部署使用 PostgreSQL，由 `deploy/docker-compose.yml` 内置 `postgres` 服务提供。

## 存储内容

- 本地用户名密码账号
- GitHub 登录映射出的用户记录
- 应用和 OIDC 配置

## 约束

- Postgres 数据目录通过 `deploy/pg_data/` 持久化
- 数据连接串由 `deploy/.env` 和 `DB_DSN` 注入，不在 `app.conf` 中硬编码
