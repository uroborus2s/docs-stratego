# CLI 发布手册

这页回答的是：当你已经确认“这次 CLI 变更值得发布”后，具体应该怎么发。

## 1. 谁应该读这页

适合这两类角色：

- `docs-stratego` 根仓维护者
- 负责 CLI 对外分发的发布执行者

如果你还在判断“这次改动到底要不要发包”，先读 [CLI 分发与发布](distribution.md)。

## 2. 发版前先做判断

只有满足下面条件之一，才建议进入发版流程：

- 外部源仓需要新的 CLI 能力
- CLI 参数、默认值、模板或校验逻辑发生了外部可见变化
- 你需要修复已发布版本中的外部使用问题

如果只是这些改动，通常不发版：

- 纯项目文档
- `.factory/` 记忆层
- 只影响根仓内部流程的文档或脚本
- 不改变已发布包行为的仓库整理

## 3. 发布前检查清单

开始发版前，先确认：

- [ ] 已完成代码、文档和测试同步
- [ ] `uv run python -m unittest tests.test_source_sync tests.test_site_builder tests.test_deploy_stack tests.test_sync_source_pointers tests.test_source_admin tests.test_cli` 通过
- [ ] `uv run docs-stratego dev --help` 通过
- [ ] `uv run docs-stratego build --project-root . --output-dir .generated --source-mode local` 通过
- [ ] `uv run mkdocs build -f .generated/mkdocs.generated.yml -d /tmp/docs-stratego-site-check` 通过
- [ ] `pyproject.toml` 中的版本号准备好更新
- [ ] GitHub 已配置 `testpypi` 和 `pypi` environments
- [ ] TestPyPI / PyPI 已为 `.github/workflows/publish-cli.yml` 配置 Trusted Publisher

## 4. 版本更新

当前仓库没有额外的自动版本管理脚本，所以建议直接修改仓库根目录 `pyproject.toml` 中的：

```toml
[project]
version = "0.1.1"
```

建议规则：

- 修 Bug：升补丁号，例如 `0.1.1 -> 0.1.2`
- 新增兼容能力：升次版本，例如 `0.1.1 -> 0.2.0`
- 不兼容改动：升主版本，例如 `0.1.1 -> 1.0.0`

## 5. 本地发版前验证

在根仓执行：

```bash
uv sync
uv run python -m unittest tests.test_source_sync tests.test_site_builder tests.test_deploy_stack tests.test_sync_source_pointers tests.test_source_admin tests.test_cli
uv build --no-sources
```

可选本地烟雾验证：

```bash
uv run docs-stratego --help
uv run docs-stratego dev --help
uv run docs-stratego source validate --help
```

## 6. 触发正式发布

当前仓库的发布 workflow 是 `.github/workflows/publish-cli.yml`。

它遵守两个原则：

- 普通 `push` 不发布
- 只有 `cli-vX.Y.Z` tag 才自动走完整发布链路

### 6.1 标准发版方式：打 tag

版本更新并提交后，执行：

```bash
git tag cli-v0.1.1
git push origin cli-v0.1.1
```

这个 tag 必须和 `pyproject.toml` 的版本一致。  
例如：

- `version = "0.1.1"`
- tag 必须是 `cli-v0.1.1`

workflow 会先校验这一点，不一致会直接失败。

### 6.2 手动演练：workflow_dispatch

如果你只想演练，不想正式发到 PyPI，可在 GitHub Actions 页面手动运行 `Publish CLI`：

- `publish_target = testpypi`
  - 只发布到 TestPyPI
- `publish_target = both`
  - 先 TestPyPI，再正式 PyPI

建议：

- 平时先用 `testpypi`
- 只有确认没问题时，才用 tag 走正式链路

## 7. 发布链路里会发生什么

`publish-cli.yml` 的顺序是：

1. `build`
2. `publish-testpypi`
3. `smoke-test-testpypi`
4. `publish-pypi`

每一步的含义：

- `build`
  - 跑单元测试
  - 执行 `uv build --no-sources`
  - 上传 `dist/` 产物
- `publish-testpypi`
  - 用 Trusted Publishing 发到 TestPyPI
- `smoke-test-testpypi`
  - 用 `uvx --from 'docs-stratego==<version>'` 做最小验证
- `publish-pypi`
  - 只有前面都通过才发到正式 PyPI

## 8. 发布后怎么验证

### 8.1 TestPyPI 验证

```bash
uvx --index testpypi=https://test.pypi.org/simple/ \
  --from 'docs-stratego==0.1.1' \
  docs-stratego --help
```

### 8.2 正式 PyPI 验证

```bash
uvx --from 'docs-stratego==0.1.1' docs-stratego --help
uvx --from 'docs-stratego==0.1.1' docs-stratego source validate --help
```

### 8.3 外部源仓验证

任选一个接入仓，执行：

```bash
uvx --from 'docs-stratego==0.1.1' docs-stratego source validate --repo-path .
```

如果要验证通知模板：

```bash
uvx --from 'docs-stratego==0.1.1' docs-stratego source scaffold-notify --repo-path . --dry-run
```

## 9. 失败处理

### 9.1 TestPyPI 失败

如果失败在：

- `build`
- `publish-testpypi`
- `smoke-test-testpypi`

处理方式：

- 修复问题
- bump 新版本
- 重新打新 tag

不要复用旧版本号。

### 9.2 正式 PyPI 发布前失败

如果 TestPyPI 已通过，但正式发布前失败，优先：

- 修复 workflow 或包元数据问题
- 保持版本号不变时，只能通过手动 `workflow_dispatch` 补发同一套产物

如果你已经改了包内容，就必须 bump 新版本。

### 9.3 正式 PyPI 发布后发现缺陷

PyPI 版本不可覆盖，所以不要尝试“重传同版本”。

正确做法：

1. 修复问题
2. bump 新版本
3. 打新的 `cli-vX.Y.Z` tag
4. 通知接入方升级到新版本

## 10. 对外升级口径

发版后，文档和接入方推荐写法保持固定：

### 一次性执行

```bash
uvx --from 'docs-stratego==0.1.1' docs-stratego source validate --repo-path .
```

### 常驻安装

```bash
uv tool install 'docs-stratego==0.1.1'
docs-stratego source validate --repo-path .
```

## 11. 最短发布路径

如果你只想看最短步骤：

1. 修改 `pyproject.toml` 版本号
2. 跑测试和 `uv build --no-sources`
3. 提交代码
4. 打 `cli-vX.Y.Z` tag
5. 推送 tag
6. 等 `Publish CLI` 跑完
7. 用 `uvx --from 'docs-stratego==X.Y.Z'` 做烟雾验证
