# 技术画像摘要

- 当前画像：自定义技术画像
- 预设：custom
- 技术栈：MkDocs Material + Python/uv + git submodule + sparse-checkout + Casdoor + oauth2-proxy + Nginx + Gemini CLI/Codex
- 最近更新时间：2026-03-27

## 项目范围

- 单站点静态文档站
- 页面级登录保护
- 源仓 `docs/` 标准化接入

## 必装/必选模块

- `src/docs_stratego/source_sync.py`
- `src/docs_stratego/site_builder.py`
- `src/docs_stratego/source_admin.py`
- `src/docs_stratego/cli.py`
- `deploy/docker-compose.yml`

## 关键工程规则

- 根仓不改写源仓文档内容
- 页面权限只能在根 `docs/index.md` 中声明
- 默认关闭匿名全文搜索

## 管理后台要求

- Casdoor 必须提供本地账号密码和 GitHub 登录

## 强制技能

- brainstorming
- python-uv-project
- tdd-workflow

## 推荐初始化动作

- 先执行 `uv sync`
- 再执行 `uv run docs-stratego build --project-root . --output-dir .generated`

## 参考资料

- 暂无。
