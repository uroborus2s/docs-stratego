# 接入聚合站点

这页是“把一个已经合规的源仓正式接到根仓”的执行手册。  
它不解释为什么要这样设计，只告诉你该按什么顺序做、做到哪一步算成功。

## 1. 先确认你手里有没有这 6 个信息

在开始前，请准备：

| 你需要知道什么 | 示例 |
| --- | --- |
| 源仓本地路径 | `/path/to/source-repo` |
| 源仓展示标题 | `星图` |
| 源仓 GitHub 页面地址 | `https://github.com/example/atlas` |
| 源仓 Git 克隆地址 | `https://github.com/example/atlas.git` |
| 远程分支 | `main` |
| 本地 docs 路径 | `../atlas/docs` |

前提边界：

- 源仓已经满足 [源文档标准](source-docs-standard.md)
- 源仓侧命令默认假设你已经能拿到已发布的 CLI
- 如果 CLI 还没发布，请先看 [CLI 分发与发布](distribution.md)

## 2. 完整接入流程长什么样

![源仓接入流程示意截图](../../assets/user-guide/source-onboarding-flow.svg)

## 3. 第一步：先在源仓做结构校验

在源仓本地执行：

```bash
uvx --from 'docs-stratego==<version>' docs-stratego source validate --repo-path /path/to/source-repo
```

这一步会检查：

- 根 `docs/index.md` 是否存在且结构合法
- 导航里声明的页面是否真实存在
- 每个内容目录是否有 `index.md`
- OpenAPI / MCP tools 契约是否满足最低要求

成功标志：

- 命令正常退出
- 没有未声明页面、缺失 `index.md` 或契约格式错误

## 4. 第二步：在根仓登记源仓

进入 `docs-stratego` 根仓后执行：

```bash
uv run docs-stratego source add \
  --project-root /path/to/docs-stratego \
  --name atlas \
  --title 星图 \
  --repo-url https://github.com/example/atlas \
  --git-url https://github.com/example/atlas.git \
  --local-path ../atlas/docs \
  --branch main
```

这一步至少会更新：

- `config/source-repos.json`

### 4.1 什么时候要加 `--register-submodule`

如果你希望 remote 模式也能直接拉这个仓，就追加：

```bash
--register-submodule
```

### 4.2 什么时候先用 `--dry-run`

如果你不确定命令会写什么，先演练：

```bash
uv run docs-stratego source add ... --dry-run
```

适用场景：

- 第一次接入，不想直接落盘
- 要核对子模块路径或 title
- 要让 reviewer 先确认计划写入内容

成功标志：

- `config/source-repos.json` 里出现新的仓库定义
- 如启用 submodule，`.gitmodules` 与 Git 索引路径一致

## 5. 第三步：用 remote 模式做一次真实构建验证

登记完成后，在根仓执行：

```bash
uv run docs-stratego sync --project-root /path/to/docs-stratego --source-mode remote
uv run docs-stratego build --project-root /path/to/docs-stratego --source-mode remote
uv run mkdocs build -f /path/to/docs-stratego/.generated/mkdocs.generated.yml -d /path/to/docs-stratego/site
```

这一步必须做，因为很多问题只有 remote 模式才会暴露，例如：

- 根仓无法真实拉到该源仓
- submodule 路径和配置不一致
- 远程分支不存在
- 源仓在真实构建里还有未声明页面

成功标志：

- `sync` 通过
- `build` 通过
- `mkdocs build` 通过

## 6. 第四步：决定是否继续开自动联动

接入成功只代表“根仓已经认识这个源仓”。  
如果你希望源仓未来的 `docs/**` 变化能自动形成根仓共享 PR，还要继续做 [自动联动](automation.md)。

## 7. 常见误区

### 7.1 我在源仓校验通过了，为什么还要回根仓验证

因为源仓校验只确认“源仓自己合规”。  
真正的接入问题通常发生在根仓登记、remote 拉取、submodule 路径和统一构建阶段。

### 7.2 我只更新了 `config/source-repos.json`，是不是就算接入完成

不算。  
至少还要跑一次 remote 模式构建验证，确认真实输入能被站点生成器消费。

### 7.3 我是不是一接入就必须开自动联动

不是。  
你可以先只做静态接入，待远程构建稳定后再补自动联动。

## 8. 接入验收清单

- [ ] 源仓本地校验通过
- [ ] `config/source-repos.json` 已新增仓库定义
- [ ] 如使用 remote 模式，submodule 已成功注册
- [ ] `sync --source-mode remote` 通过
- [ ] `build --source-mode remote` 通过
- [ ] `mkdocs build` 通过

## 9. 接下来读什么

- 想补自动联动：读 [自动联动](automation.md)
- 想看完整命令参数：读 [CLI 命令](cli.md)
- 想准备外部源仓使用 CLI：读 [CLI 分发与发布](distribution.md)
