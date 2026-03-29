# 认证与权限服务设计

## 设计目标

- 不手写完整认证系统
- 用开源服务承接账号、密码和 GitHub 登录
- 让 Nginx 可以按页面 URL 判断是否需要登录

## 方案

- Casdoor：作为统一身份服务
- oauth2-proxy：作为 OIDC Client 和 Nginx 前置认证适配器
- Nginx：读取构建时生成的私有路径清单，对命中路径执行 `auth_request`

## 认证流

1. 用户访问私有页面
2. Nginx 命中该页面的私有规则
3. Nginx 调用 `/oauth2/auth`
4. 未登录时重定向到 oauth2-proxy 登录入口
5. oauth2-proxy 跳转到 Casdoor
6. Casdoor 支持本地账号密码或 GitHub 登录
7. 登录成功后返回原页面
