# crawler4j 接入包

## 目标

本文件用于评审“蛛行演略（crawler4j）”作为外部源仓接入 `docs-stratego` 的准备情况。当前仓库已经进入正式 `config/source-repos.json`，因此 remote 构建会真实拉取并校验它；是否能稳定通过 CI/CD，取决于源仓文档是否满足发布规则。

## 源仓事实

- 本机路径：`crawler4j` 源仓本地工作副本（实际绝对路径按维护环境配置）
- 远程仓库：`https://github.com/uroborus2s/crawler4j.git`
- 目标分支：`feature/task-plugin-system`
- 文档根目录：`docs/`
- 根导航清单：`crawler4j/docs/index.md`

## 已确认的源文档条件

- 本地工作副本中的 `crawler4j/docs/index.md` 已采用“根清单模式”
- 本地工作副本中的目录结构符合根仓标准
- `assets/` 目录只放资源文件，没有 Markdown 页面

## 当前阻塞项

远程接入分支 `feature/task-plugin-system` 经过真实 `submodule_sparse -> build_site` 验证后，仍包含一批未在根 `docs/index.md` 中声明的历史 Markdown 页面，因此根仓按规则必须拒绝构建。

当前典型阻塞目录包括：

- `08-handover/`
- `archive/`
- `model-development/`

这意味着：

- 只要 `crawler4j` 保留在正式 `config/source-repos.json` 中，GitHub Actions 的 remote 构建就会真实拉取并校验它
- 在源仓把这些页面纳入 `mkdocs.nav` 或迁出正式文档树之前，CI/CD 会继续按规则失败
- 因为当前策略只保留一个 `source-repos.json`，所以是否把它留在正式配置中，本身就是一次“是否纳入生产校验”的决定

## 计划接入方式

```json
{
  "version": 3,
  "default_source_mode": "local",
  "repositories": [
    {
      "name": "docs-stratego",
      "title": "章略·墨衡",
      "repo_url": "https://github.com/uroborus2s/docs-stratego",
      "modes": {
        "local": {
          "source_type": "local",
          "local_path": "docs"
        },
        "remote": {
          "source_type": "local",
          "local_path": "docs"
        }
      }
    },
    {
      "name": "crawler4j",
      "title": "蛛行演略",
      "repo_url": "https://github.com/uroborus2s/crawler4j",
      "modes": {
        "local": {
          "source_type": "local",
          "local_path": "../../PythonProject/crawler4j/docs"
        },
        "remote": {
          "source_type": "submodule_sparse",
          "git_url": "https://github.com/uroborus2s/crawler4j.git",
          "branch": "feature/task-plugin-system",
          "submodule_path": "sources/crawler4j",
          "docs_path": "docs"
        }
      }
    }
  ]
}
```

## 解除阻塞后的预期结果

- 站点首页会出现 `蛛行演略`
- 左侧目录树直接来自 `crawler4j/docs/index.md`
- `public` 页面匿名可读
- `private` 页面点击后进入登录链路
- `crawler4j/docs` 中的资源文件按所属目录 `index.md` 页面权限继承

## 评审清单

- 是否确认 `crawler4j` 继续使用 `feature/task-plugin-system` 作为接入分支
- 是否确认先在源仓清理未声明页面，再进入正式接入
- 是否确认服务器先按手工 SOP 部署，再进入 CI/CD 自动化
- 是否确认在源仓解除阻塞后，再把 `crawler4j` 作为正式生产源仓保留在唯一的 `config/source-repos.json` 中
