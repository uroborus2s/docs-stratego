# 移除流程

下线一个源仓前，先判断你要做的是哪一种动作：

- 暂停自动联动：保留根仓登记，只停掉源仓通知 workflow
- 完整移除：同时移除源仓通知和根仓登记

## 1. 只暂停自动联动

在源仓执行：

```bash
uvx --from 'docs-stratego==<version>' docs-stratego source scaffold-notify \
  --repo-path /path/to/source-repo \
  --remove
```

适用场景：

- 源仓暂时冻结
- 文档还需要保留在聚合站点
- 你想先人工控制更新节奏

如果 CLI 还没有对外发布，请先看 [CLI 分发与发布](distribution.md)，不要默认在源仓里执行 `uv run docs-stratego ...`。

## 2. 完整移除一个源仓

建议按下面顺序做：

1. 在源仓删除通知 workflow。
2. 在根仓移除仓库定义。
3. 如果该源仓使用 remote submodule，再移除 submodule。
4. 重新跑一次根仓远程构建验证。

根仓命令：

```bash
uv run docs-stratego source remove \
  --project-root /path/to/docs-stratego \
  --name atlas \
  --yes
```

如果要连 submodule 一起移除，再追加：

```bash
--remove-submodule
```

如果你只想看即将删除什么，不真正落盘，追加：

```bash
--dry-run
```

## 3. 完整移除后的验证

在根仓执行：

```bash
uv run docs-stratego sync --project-root /path/to/docs-stratego --source-mode remote
uv run docs-stratego build --project-root /path/to/docs-stratego --source-mode remote
uv run mkdocs build -f /path/to/docs-stratego/.generated/mkdocs.generated.yml -d /path/to/docs-stratego/site
```

确认目标：

- `config/source-repos.json` 已不再包含该仓库
- `.gitmodules` 与 `sources/<name>` 状态一致
- 站点构建不再引用该源仓页面

## 4. 下线验收清单

- [ ] 源仓通知 workflow 已删除或停用
- [ ] 根仓仓库定义已移除
- [ ] 如适用，submodule 已移除
- [ ] 远程模式构建通过
- [ ] 维护者已知晓聚合站点内容会减少该项目入口
