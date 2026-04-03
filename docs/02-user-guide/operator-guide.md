# 维护者指南 (Operator Guide)

本文档面向聚合站点的日常维护人员，介绍本地开发预览、子仓同步审核以及生产发布验证的标准操作流程。

## 1. 核心任务概览
维护者的主要职责是确保子仓文档能及时、准确地聚合到主站，并验证发布后的页面权限是否正确。

---

## 2. 本地预览与构建 (Preview)

在提交任何改动前，必须在本地验证构建结果。

### 2.1 模式选择
- **本地开发模式 (Local Mode)**：直接读取本机已有的子仓目录。速度最快，用于频繁修改。
  ```bash
  uv run docs-stratego dev --project-root . --source-mode local
  ```
- **生产预演模式 (Remote Mode)**：模拟 CI 环境，真实从远程拉取子仓。用于发布前的最后确认。
  ```bash
  uv run docs-stratego dev --project-root . --source-mode remote
  ```

### 2.2 验证指标
- 访问 `http://127.0.0.1:8001/`。
- 确认顶部及左侧导航层级符合预期。
- 确认 OpenAPI/MCP 等契约文件渲染正常。

---

## 3. 子仓同步管理 (Sync Management)

本项目采用“子仓变更驱动”机制。

### 3.1 自动同步流程
1. **子仓触发**：子仓 push 后发送 dispatch 信号。
2. **根仓 PR**：根仓会自动创建一个名为 `chore: sync source repository pointers` 的 PR。
3. **审核要点**：
   - 检查 `uv.lock` 或子仓指针的变化是否符合预期。
   - 在 PR 页面查看自动生成的预览链接（如果已配置）。
4. **合并**：确认无误后执行 `Squash and merge`。

---

## 4. 发布验证 (Post-Deployment)

当代码合并到 `main` 分支并触发 Actions 发布后，必须进行以下“闭环验证”：

| 验证项 | 操作 | 预期结果 |
| :--- | :--- | :--- |
| **匿名可读性** | 无登录状态访问首页 | 正常显示且无登录弹窗 |
| **私有页锁定** | 点击标记为 `access: private` 的页面 | 触发登录小窗 |
| **登录闭环** | 完成 GitHub/Casdoor 登录 | 小窗关闭，页面内容正常显示 |
| **Nginx 状态** | 检查私有路径是否生效 | 直接输入私有 URL 应返回 401 并触发认证 |

---

## 5. 故障处理矩阵 (Troubleshooting)

| 现象 | 可能原因 | 建议动作 |
| :--- | :--- | :--- |
| **同步 PR 包含过多无关改动** | 多个子仓并发同步 | 检查 Git 指针，必要时手动 Rebase |
| **私有页面变为匿名可见** | 子仓 `index.md` 缺少权限标记 | 检查源仓配置并重新触发同步 |
| **Actions 成功但站点未更新** | 宿主机 Nginx 缓存或 reload 失败 | 检查部署日志中的 `systemctl reload nginx` 部分 |
| **登录小窗报 500 错误** | Casdoor 或 Redis 服务异常 | 检查 `docker compose ps` 确认认证组件状态 |
