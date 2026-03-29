# Gemini 项目说明

你正在一个共享的软件工厂工作区中工作。
当前版本只落地 `Codex / Gemini CLI` 直接使用方式。

项目根目录：`/Users/uroborus/AiProject/docs-stratego`
项目名称：`章略·墨衡`

优先阅读（运行时）：

- `/Users/uroborus/.agent/skills/software-factory-cli/references/ai-runtime-protocol.md`
- `/Users/uroborus/.agent/skills/software-factory-cli/references/ai-role-charter.md`
- `docs/00-governance/project-charter.md`
- `docs/01-discovery/input.md`
- `.factory/project.json`

共享 skill 引用：

- `brainstorming`: /Users/uroborus/.agent/skills/brainstorming/SKILL.md
- `document-templates`: /Users/uroborus/.agent/skills/document-templates/SKILL.md
- `requirements-engineering`: /Users/uroborus/.agent/skills/requirements-engineering/SKILL.md
- `doc-coauthoring`: /Users/uroborus/.agent/skills/doc-coauthoring/SKILL.md
- `api-design`: /Users/uroborus/.agent/skills/api-design/SKILL.md
- `backend-patterns`: /Users/uroborus/.agent/skills/backend-patterns/SKILL.md
- `python-uv-project`: /Users/uroborus/.agent/skills/python-uv-project/SKILL.md
- `frontend-patterns`: /Users/uroborus/.agent/skills/frontend-patterns/SKILL.md
- `ui-ux-pro-max`: /Users/uroborus/.agent/skills/ui-ux-pro-max/SKILL.md
- `tdd-workflow`: /Users/uroborus/.agent/skills/tdd-workflow/SKILL.md
- `webapp-testing`: /Users/uroborus/.agent/skills/webapp-testing/SKILL.md

Gemini CLI 推荐职责：

- 头脑风暴和方案探索
- PRD 与需求分析
- 架构设计与 API 设计
- 变更影响分析
- 发布说明与验收复查

规则：

- 默认先按 AI 运行时协议工作，不要默认全文加载长篇工作流说明。
- 把 Markdown 文档当成事实来源
- 当前 V1 以本地 CLI 协作为主，不以 API 平台作为执行入口
- 需求和设计未获批准前，不要进入代码实现
- 进入实现前先读取 `docs/03-solution/technical-selection.md`，确认当前技术栈、模块清单和后台要求
- UX/UI 文档允许包含图片、HTML 原型、流程图和外部原型链接等设计交付物，必要时用 `factory-design-assets` 录入并引用
- 编写需求文档时尽量详细，完成后执行 `factory-requirements-verify` 反复比对 PRD 与需求分析，避免遗漏需求
- 代码类工作项在关单前需要完成 PR 创建、评审和合并
- 如果项目接入了远程仓库，优先用 `factory-pr-remote-open / sync / merge` 把远端状态同步回本地文档
- 任何已接受内容变更后，都要同步更新 `/.factory/memory/` 摘要
