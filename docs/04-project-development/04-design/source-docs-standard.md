# 源文档标准

本文是外部源仓必须遵守的正式标准。当前模式下，聚合站点只读取源仓根 `docs/index.md` 的导航清单来生成左侧目录树和页面权限。

## 1. 目录标准

源仓至少提供一个文档根目录，默认是 `docs/`。

推荐结构：

```text
docs/
  index.md
  00-governance/
    index.md
    project-charter.md
  02-requirements/
    index.md
    prd.md
    reference-srs/
      index.md
      01-document-control.md
  03-solution/
    index.md
    system-architecture.md
    reference-design/
      index.md
      overview.md
    assets/
      architecture.png
```

规则：

- 每个真实内容目录都必须保留自己的 `index.md`
- 每个 Markdown 页面都必须有一级标题 `# 标题`
- 根 `docs/index.md` 是唯一的导航清单文件
- 子目录 `index.md` 只是普通页面，不再承担导航声明职责
- 需要随页面一起保护的图片、附件和下载文件，放在页面目录或该目录的 `assets/` 下
- `assets/` 只能放资源文件，不能放 Markdown 页面

## 2. 根 `docs/index.md` 标准

根 `docs/index.md` 使用 YAML front matter，在一个文件里声明整个项目的目录树、页面路径和页面权限。

### 2.1 数据结构

- `title`: 项目标题
- `mkdocs.home_access`: 根首页权限，取值为 `public` 或 `private`
- `mkdocs.nav`: 全站目录树
- 目录节点只允许：
  - `title`
  - `children`
- 页面节点只允许：
  - `title`
  - `path`
  - `access`
- 页面权限只写在页面节点，目录节点不写权限

### 2.2 完整模板

```md
---
title: 蛛行演略
mkdocs:
  home_access: public
  nav:
    - title: 项目治理
      children:
        - title: 概览
          path: 00-governance/index.md
          access: public
        - title: 项目章程
          path: 00-governance/project-charter.md
          access: public

    - title: 调研与决策
      children:
        - title: 概览
          path: 01-discovery/index.md
          access: public
        - title: 输入背景
          path: 01-discovery/input.md
          access: public
        - title: 头脑风暴记录
          path: 01-discovery/brainstorm-record.md
          access: public
        - title: 当前真实状态分析
          path: 01-discovery/current-state-analysis.md
          access: public

    - title: 需求
      children:
        - title: 概览
          path: 02-requirements/index.md
          access: public
        - title: PRD
          path: 02-requirements/prd.md
          access: public
        - title: 需求分析
          path: 02-requirements/requirements-analysis.md
          access: public
        - title: Reference SRS
          children:
            - title: 概览
              path: 02-requirements/reference-srs/index.md
              access: public
            - title: 文档控制
              path: 02-requirements/reference-srs/01-document-control.md
              access: public

    - title: 方案设计
      children:
        - title: 概览
          path: 03-solution/index.md
          access: private
        - title: 技术选型与工程规则
          path: 03-solution/technical-selection.md
          access: private
        - title: 系统架构
          path: 03-solution/system-architecture.md
          access: private
        - title: 参考设计
          children:
            - title: 概览
              path: 03-solution/reference-design/index.md
              access: private
            - title: 总体设计
              path: 03-solution/reference-design/overview.md
              access: private
---
# 蛛行演略

这里写项目首页简介、范围边界和维护说明。
```

## 3. 页面路径与目录树规则

- 目录树只来自根 `docs/index.md` 的 `mkdocs.nav`
- 站点只认这一套结构，正文中的列表、目录说明、推荐顺序都不会参与构建
- `children` 可以继续嵌套，表示目录和二级目录
- 真正的页面必须落到 `path`
- `path` 必须指向一个 Markdown 文件
- `path` 统一写相对根 `docs/` 的路径，例如 `03-solution/system-architecture.md`
- 不允许在 `path` 中使用 `../`
- 不允许把 `assets/` 下的文件写成页面路径

## 4. 权限规则

- 只有页面节点有权限
- `access` 取值只允许 `public` 或 `private`
- 根首页权限由 `mkdocs.home_access` 决定
- 目录节点本身不设置权限，它们只是左侧结构节点
- 如果某个目录下的资源文件需要受保护，系统会继承该目录 `index.md` 页面本身的权限
- 私有页面会保留在同一套左侧目录中，但点击后走登录链路

## 5. 子目录 `index.md` 的职责

子目录 `index.md` 仍然必须存在，但职责已经变成：

- 作为该目录的正文首页
- 提供目录介绍、边界说明和上下文
- 作为资源文件权限继承的锚点页面

它不再负责：

- 声明 `mkdocs.nav`
- 决定左侧目录树
- 决定其他页面的权限
- 重复抄写本目录下的完整页面清单

推荐模板：

```md
# 方案设计概览

本目录收纳技术方案、模块边界、接口契约和工程规则。

本文只负责说明本目录做什么、适合谁看、有哪些约束。
```

## 6. 根 `docs/index.md` 正文要求

根 `docs/index.md` 只允许承担首页正文职责，不允许再手写第二套目录结构。

允许写：

- 项目简介
- 文档范围边界
- 面向读者说明
- 维护规则

不允许写：

- 目录树镜像
- 章节顺序清单
- 和 `mkdocs.nav` 重复的链接列表
- 人工维护的“推荐阅读顺序”目录

## 7. 构建器实际读取什么

要构建出项目的目录树和页面路径，构建器只需要：

1. 根 `docs/index.md` 的 front matter
2. 文件系统，校验 `path` 对应的 Markdown 是否存在
3. 所有页面文件自身的一级标题，用于内容质量校验

换句话说：

- 左侧目录树来自根 `docs/index.md`
- 页面 URL 来自根 `docs/index.md` 的 `path`
- 页面权限来自根 `docs/index.md` 的 `access`
- 子目录 `index.md` 只参与站点内容，不参与导航生成
