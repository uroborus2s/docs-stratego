# OpenAPI 契约

本目录收纳需要以 OpenAPI 形式维护并在文档站通过 Scalar 渲染的 HTTP 接口契约。

当前仓库先放一个最小示例，用于验证三件事：

- 源文档标准已经允许 `*.openapi.yaml|yml|json` 进入根导航
- 构建器会为每个契约文件自动生成 Scalar API Reference 包装页
- 页面权限会同时作用于渲染页和原始契约文件

正式项目接入时，应优先把真实的业务契约按“端 / 服务 / 版本”拆分到本目录或 `03-developer-guide/openapi/`。
