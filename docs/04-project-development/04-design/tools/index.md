# 工具契约（MCP）

本目录收纳按 MCP tools 数据模型维护的稳定工具入口快照。

当前仓库先放一份 `site-builder.mcp-tools.yaml`，用于验证两件事：

- 根 `docs/index.md` 可以直接声明 `*.mcp-tools.yaml|yml|json`
- 构建器会把 MCP tools 快照渲染成可浏览的静态参考页，并保留原始快照下载地址

这里的“工具”包括但不限于：

- CLI 命令入口
- 稳定脚本入口
- Agent / MCP tools
- 其他适合以 schema 描述输入输出的可调用能力

交互调试不在文档站完成；需要实际调试时，使用 MCP Inspector。
