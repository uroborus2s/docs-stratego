from __future__ import annotations

import importlib
import json
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))


def load_module():
    return importlib.import_module("docs_stratego.site_builder")


class SiteBuilderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_module()

    def test_builder_generates_nav_permissions_and_nginx_locations_from_root_index(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            docs_root = tmp_path / "docs"
            (docs_root / "02-requirements").mkdir(parents=True)
            (docs_root / "03-solution" / "reference-design" / "assets").mkdir(parents=True)
            (docs_root / "03-solution" / "assets").mkdir(parents=True)

            (docs_root / "index.md").write_text(
                "---\n"
                "title: 平台文档\n"
                "mkdocs:\n"
                "  home_access: public\n"
                "  nav:\n"
                "    - title: 需求\n"
                "      children:\n"
                "        - title: 概览\n"
                "          path: 02-requirements/index.md\n"
                "          access: public\n"
                "        - title: PRD\n"
                "          path: 02-requirements/prd.md\n"
                "          access: public\n"
                "    - title: 方案设计\n"
                "      children:\n"
                "        - title: 概览\n"
                "          path: 03-solution/index.md\n"
                "          access: private\n"
                "        - title: 系统架构\n"
                "          path: 03-solution/system-architecture.md\n"
                "          access: private\n"
                "        - title: 参考设计\n"
                "          children:\n"
                "            - title: 概览\n"
                "              path: 03-solution/reference-design/index.md\n"
                "              access: private\n"
                "            - title: 总体设计\n"
                "              path: 03-solution/reference-design/overview.md\n"
                "              access: private\n"
                "---\n"
                "# 平台文档\n",
                encoding="utf-8",
            )
            (docs_root / "02-requirements" / "index.md").write_text("# 需求概览\n", encoding="utf-8")
            (docs_root / "02-requirements" / "prd.md").write_text("# PRD\n", encoding="utf-8")
            (docs_root / "03-solution" / "index.md").write_text("# 方案设计概览\n", encoding="utf-8")
            (docs_root / "03-solution" / "system-architecture.md").write_text(
                "# 系统架构\n", encoding="utf-8"
            )
            (docs_root / "03-solution" / "reference-design" / "index.md").write_text(
                "# 参考设计概览\n", encoding="utf-8"
            )
            (docs_root / "03-solution" / "reference-design" / "overview.md").write_text(
                "# 总体设计\n", encoding="utf-8"
            )
            (docs_root / "03-solution" / "assets" / "diagram.png").write_bytes(b"fake-image")
            (docs_root / "03-solution" / "reference-design" / "assets" / "detail.png").write_bytes(
                b"fake-detail-image"
            )

            repo = self.module.SourceRepository(
                name="platform",
                title="平台文档",
                source_type="local",
                repo_url="https://github.com/example/platform",
                local_path=str(docs_root),
            )
            output_dir = tmp_path / "build"

            self.module.build_site([repo], output_dir)

            permissions = json.loads((output_dir / "authz" / "permissions.json").read_text(encoding="utf-8"))
            private_urls = {item["url"] for item in permissions["pages"] if item["access"] == "private"}
            public_urls = {item["url"] for item in permissions["pages"] if item["access"] == "public"}
            nginx_text = (output_dir / "nginx" / "private_locations.conf").read_text(encoding="utf-8")
            mkdocs_text = (output_dir / "mkdocs.generated.yml").read_text(encoding="utf-8")
            home_text = (output_dir / "site_docs" / "index.md").read_text(encoding="utf-8")
            home_css_text = (output_dir / "site_docs" / "assets" / "stylesheets" / "home.css").read_text(
                encoding="utf-8"
            )
            nav_js_text = (output_dir / "site_docs" / "assets" / "javascripts" / "navigation.js").read_text(
                encoding="utf-8"
            )
            access_js_text = (
                output_dir / "site_docs" / "assets" / "javascripts" / "access-control.js"
            ).read_text(encoding="utf-8")
            popup_complete_text = (
                output_dir / "site_docs" / "assets" / "auth" / "popup-complete.html"
            ).read_text(encoding="utf-8")
            private_kinds = {
                (item["url"], item["kind"]) for item in permissions["pages"] if item["access"] == "private"
            }

        self.assertIn("/platform/", public_urls)
        self.assertIn("/platform/03-solution/system-architecture/", private_urls)
        self.assertIn("/platform/03-solution/reference-design/overview/", private_urls)
        self.assertIn(("/platform/03-solution/assets/diagram.png", "resource"), private_kinds)
        self.assertIn(
            ("/platform/03-solution/reference-design/assets/detail.png", "resource"),
            private_kinds,
        )
        self.assertIn("/platform/02-requirements/prd/", public_urls)
        self.assertIn('location = /platform/03-solution/system-architecture/', nginx_text)
        self.assertIn('location = /platform/03-solution/reference-design/assets/detail.png', nginx_text)
        self.assertIn("auth_request /oauth2/auth;", nginx_text)
        self.assertIn("error_page 401 = /oauth2/sign_in;", nginx_text)
        self.assertNotIn("include /etc/nginx/includes/auth_request.conf;", nginx_text)
        self.assertIn('docs_dir: ', mkdocs_text)
        self.assertIn("plugins: []", mkdocs_text)
        self.assertIn("palette:", mkdocs_text)
        self.assertIn("fontawesome/brands/github", mkdocs_text)
        self.assertIn("navigation.instant", mkdocs_text)
        self.assertIn("extra_javascript:", mkdocs_text)
        self.assertIn("assets/javascripts/navigation.js", mkdocs_text)
        self.assertIn("assets/javascripts/access-control.js", mkdocs_text)
        self.assertNotIn("navigation.expand", mkdocs_text)
        self.assertIn('"平台文档":', mkdocs_text)
        self.assertIn('"参考设计":', mkdocs_text)
        self.assertIn('platform/03-solution/reference-design/overview.md', mkdocs_text)
        self.assertIn("GitHub 仓库", home_text)
        self.assertIn("项目开发文档（内部）", home_text)
        self.assertIn("入门说明", home_text)
        self.assertIn("PROJECT_TAB_MENUS", nav_js_text)
        self.assertIn('{"title": "简介", "url": "/platform/", "kind": "section"}', nav_js_text)
        self.assertIn("GitHub 仓库", nav_js_text)
        self.assertIn('docs-tab-dropdown', nav_js_text)
        self.assertIn('aria-expanded', nav_js_text)
        self.assertIn('仓库链接', nav_js_text)
        self.assertIn('simplifyPrimarySidebar', nav_js_text)
        self.assertIn('querySelectorAll(\n    ".md-nav--primary > .md-nav__list > .md-nav__item--section.md-nav__item--active"', nav_js_text)
        self.assertIn('overviewLabels.forEach((overviewLabel) => {', nav_js_text)
        self.assertIn('overviewLabel.textContent = sectionTitle', nav_js_text)
        self.assertNotIn('docs-drawer-projects', nav_js_text)
        self.assertIn('.md-tabs__list {\n  contain: none !important;', home_css_text)
        self.assertIn(".docs-tab-toggle {\n  display: inline-flex;", home_css_text)
        self.assertIn("font-size: 0.9rem;", home_css_text)
        self.assertIn("font-weight: 600;", home_css_text)
        self.assertNotIn('button.md-tabs__link', home_css_text)
        self.assertNotIn(".docs-private-link", home_css_text)
        self.assertNotIn("锁定", home_css_text)
        self.assertNotIn(".docs-auth-modal", home_css_text)
        self.assertIn("const menuToggle = anchor.cloneNode(true);", nav_js_text)
        self.assertIn('menuToggle.removeAttribute("href");', nav_js_text)
        self.assertIn('menuToggle.setAttribute("tabindex", "0");', nav_js_text)
        self.assertIn('parent.replaceChild(menuToggle, anchor);', nav_js_text)
        self.assertIn("const PRIVATE_URLS = new Set(", access_js_text)
        self.assertIn('const AUTH_POPUP_MESSAGE_TYPE = "docs-auth-popup-complete";', access_js_text)
        self.assertIn('const AUTH_POPUP_CALLBACK_PATH = "/assets/auth/popup-complete.html";', access_js_text)
        self.assertIn("const AUTH_STATUS_TTL_MS =", access_js_text)
        self.assertIn("/platform/03-solution/system-architecture/", access_js_text)
        self.assertIn("/platform/03-solution/reference-design/assets/detail.png", access_js_text)
        self.assertIn('fetch("/oauth2/auth"', access_js_text)
        self.assertIn('sessionStorage.getItem("docsAuthState")', access_js_text)
        self.assertIn('sessionStorage.setItem("docsAuthState"', access_js_text)
        self.assertIn("function hasFreshAuthenticatedSession()", access_js_text)
        self.assertIn("refreshAuthState()", access_js_text)
        self.assertIn("if (isPrivateUrl(anchor.href) && hasFreshAuthenticatedSession())", access_js_text)
        self.assertIn('window.open("about:blank", "docsAuthPopup"', access_js_text)
        self.assertIn("window.addEventListener(\"message\"", access_js_text)
        self.assertIn("window.opener.postMessage", popup_complete_text)
        self.assertIn("window.close()", popup_complete_text)
        self.assertIn("docs-auth-popup-complete", popup_complete_text)
        self.assertIn("/assets/auth/popup-complete.html", access_js_text)
        self.assertIn("authPopup.closed", access_js_text)
        self.assertIn("function dismissAuthPopupOnBackgroundInteraction()", access_js_text)
        self.assertIn('document.addEventListener("pointerdown", dismissAuthPopupOnBackgroundInteraction, true);', access_js_text)
        self.assertIn('window.addEventListener("focus", dismissAuthPopupOnBackgroundInteraction);', access_js_text)
        self.assertNotIn("iframe", access_js_text)
        self.assertNotIn("去登录", access_js_text)
        self.assertNotIn("window.open(signInUrl", access_js_text)
        self.assertNotIn("location = / {", nginx_text)

    def test_builder_allows_undeclared_markdown_pages_outside_nav(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            docs_root = tmp_path / "docs"
            (docs_root / "03-solution").mkdir(parents=True)
            (docs_root / "03-solution" / "drafts").mkdir(parents=True)
            (docs_root / "index.md").write_text(
                "---\n"
                "title: 平台文档\n"
                "mkdocs:\n"
                "  home_access: public\n"
                "  nav:\n"
                "    - title: 方案设计\n"
                "      children:\n"
                "        - title: 概览\n"
                "          path: 03-solution/index.md\n"
                "          access: private\n"
                "---\n"
                "# 平台文档\n",
                encoding="utf-8",
            )
            (docs_root / "03-solution" / "index.md").write_text("# 方案设计概览\n", encoding="utf-8")
            (docs_root / "03-solution" / "drafts" / "orphan.md").write_text("# Orphan\n", encoding="utf-8")

            repo = self.module.SourceRepository(
                name="platform",
                title="平台文档",
                source_type="local",
                local_path=str(docs_root),
            )

            self.module.build_site([repo], tmp_path / "build")

    def test_builder_rejects_declared_directory_without_index(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            docs_root = tmp_path / "docs"
            (docs_root / "03-solution" / "drafts").mkdir(parents=True)
            (docs_root / "index.md").write_text(
                "---\n"
                "title: 平台文档\n"
                "mkdocs:\n"
                "  home_access: public\n"
                "  nav:\n"
                "    - title: 方案设计\n"
                "      children:\n"
                "        - title: 草稿页\n"
                "          path: 03-solution/drafts/orphan.md\n"
                "          access: private\n"
                "---\n"
                "# 平台文档\n",
                encoding="utf-8",
            )
            (docs_root / "03-solution" / "orphan.md").write_text("# Unused\n", encoding="utf-8")
            (docs_root / "03-solution" / "drafts" / "orphan.md").write_text("# Orphan\n", encoding="utf-8")

            repo = self.module.SourceRepository(
                name="platform",
                title="平台文档",
                source_type="local",
                local_path=str(docs_root),
            )

            with self.assertRaisesRegex(ValueError, "missing index.md"):
                self.module.build_site([repo], tmp_path / "build")

    def test_builder_rejects_markdown_inside_assets_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            docs_root = tmp_path / "docs"
            (docs_root / "assets").mkdir(parents=True)
            (docs_root / "index.md").write_text(
                "---\n"
                "title: 平台文档\n"
                "mkdocs:\n"
                "  home_access: public\n"
                "  nav: []\n"
                "---\n"
                "# 平台文档\n",
                encoding="utf-8",
            )
            (docs_root / "assets" / "README.md").write_text("# bad asset doc\n", encoding="utf-8")

            repo = self.module.SourceRepository(
                name="platform",
                title="平台文档",
                source_type="local",
                local_path=str(docs_root),
            )

            with self.assertRaisesRegex(ValueError, "assets directory cannot contain Markdown"):
                self.module.build_site([repo], tmp_path / "build")

    def test_builder_renders_openapi_and_mcp_tools_contract_pages(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            docs_root = tmp_path / "docs"
            (docs_root / "03-developer-guide" / "openapi").mkdir(parents=True)
            (docs_root / "03-developer-guide" / "tools").mkdir(parents=True)

            (docs_root / "index.md").write_text(
                "---\n"
                "title: 平台文档\n"
                "mkdocs:\n"
                "  home_access: public\n"
                "  nav:\n"
                "    - title: 开发者指南\n"
                "      children:\n"
                "        - title: 概览\n"
                "          path: 03-developer-guide/index.md\n"
                "          access: public\n"
                "        - title: OpenAPI 契约\n"
                "          children:\n"
                "            - title: 概览\n"
                "              path: 03-developer-guide/openapi/index.md\n"
                "              access: public\n"
                "            - title: 平台开放接口\n"
                "              path: 03-developer-guide/openapi/platform.openapi.yaml\n"
                "              access: public\n"
                "        - title: 工具契约（MCP）\n"
                "          children:\n"
                "            - title: 概览\n"
                "              path: 03-developer-guide/tools/index.md\n"
                "              access: public\n"
                "            - title: 站点构建工具\n"
                "              path: 03-developer-guide/tools/site-builder.mcp-tools.yaml\n"
                "              access: private\n"
                "---\n"
                "# 平台文档\n",
                encoding="utf-8",
            )
            (docs_root / "03-developer-guide" / "index.md").write_text(
                "# 开发者指南\n", encoding="utf-8"
            )
            (docs_root / "03-developer-guide" / "openapi" / "index.md").write_text(
                "# OpenAPI 契约\n", encoding="utf-8"
            )
            (docs_root / "03-developer-guide" / "tools" / "index.md").write_text(
                "# 工具契约（MCP）\n", encoding="utf-8"
            )
            (docs_root / "03-developer-guide" / "openapi" / "platform.openapi.yaml").write_text(
                "openapi: 3.1.0\n"
                "info:\n"
                "  title: 平台开放接口\n"
                "  version: 1.0.0\n"
                "  summary: 对外健康检查与版本信息接口\n"
                "servers:\n"
                "  - url: https://docs.example.com\n"
                "tags:\n"
                "  - name: Health\n"
                "    description: 健康与状态接口\n"
                "paths:\n"
                "  /health:\n"
                "    get:\n"
                "      tags: [Health]\n"
                "      operationId: getHealth\n"
                "      summary: 获取健康状态\n"
                "      responses:\n"
                "        '200':\n"
                "          description: OK\n"
                "          content:\n"
                "            application/json:\n"
                "              schema:\n"
                "                $ref: '#/components/schemas/HealthResponse'\n"
                "components:\n"
                "  schemas:\n"
                "    HealthResponse:\n"
                "      type: object\n"
                "      description: 健康检查返回体\n"
                "      required: [status]\n"
                "      properties:\n"
                "        status:\n"
                "          type: string\n",
                encoding="utf-8",
            )
            (docs_root / "03-developer-guide" / "tools" / "site-builder.mcp-tools.yaml").write_text(
                "tools:\n"
                "  - name: build_site\n"
                "    title: 站点构建\n"
                "    description: 构建聚合文档站点\n"
                "    annotations:\n"
                "      readOnlyHint: false\n"
                "      destructiveHint: false\n"
                "      idempotentHint: true\n"
                "      openWorldHint: false\n"
                "    inputSchema:\n"
                "      type: object\n"
                "      required: [config]\n"
                "      properties:\n"
                "        config:\n"
                "          type: string\n"
                "        output_dir:\n"
                "          type: string\n"
                "    outputSchema:\n"
                "      type: object\n"
                "      properties:\n"
                "        outputDir:\n"
                "          type: string\n",
                encoding="utf-8",
            )

            repo = self.module.SourceRepository(
                name="platform",
                title="平台文档",
                source_type="local",
                repo_url="https://github.com/example/platform",
                local_path=str(docs_root),
            )
            output_dir = tmp_path / "build"

            self.module.build_site([repo], output_dir)

            permissions = json.loads((output_dir / "authz" / "permissions.json").read_text(encoding="utf-8"))
            mkdocs_text = (output_dir / "mkdocs.generated.yml").read_text(encoding="utf-8")
            openapi_text = (
                output_dir / "site_docs" / "platform" / "03-developer-guide" / "openapi" / "platform.openapi.md"
            ).read_text(encoding="utf-8")
            tools_text = (
                output_dir
                / "site_docs"
                / "platform"
                / "03-developer-guide"
                / "tools"
                / "site-builder.mcp-tools.md"
            ).read_text(encoding="utf-8")
            contracts_js_text = (
                output_dir / "site_docs" / "assets" / "javascripts" / "contracts.js"
            ).read_text(encoding="utf-8")

            public_pages = {item["url"] for item in permissions["pages"] if item["kind"] == "page" and item["access"] == "public"}
            private_pages = {item["url"] for item in permissions["pages"] if item["kind"] == "page" and item["access"] == "private"}
            private_resources = {
                item["url"] for item in permissions["pages"] if item["kind"] == "resource" and item["access"] == "private"
            }

        self.assertIn("/platform/03-developer-guide/openapi/platform.openapi/", public_pages)
        self.assertIn("/platform/03-developer-guide/tools/site-builder.mcp-tools/", private_pages)
        self.assertIn("/platform/03-developer-guide/tools/site-builder.mcp-tools.yaml", private_resources)
        self.assertIn('platform/03-developer-guide/openapi/platform.openapi.md', mkdocs_text)
        self.assertIn('platform/03-developer-guide/tools/site-builder.mcp-tools.md', mkdocs_text)
        self.assertIn("assets/javascripts/contracts.js", mkdocs_text)
        self.assertIn("# 平台开放接口", openapi_text)
        self.assertIn("Scalar API Reference", openapi_text)
        self.assertIn('class="docs-openapi-scalar', openapi_text)
        self.assertIn('data-openapi-url="platform.openapi.yaml"', openapi_text)
        self.assertIn('href="platform.openapi.yaml">下载原始契约<', openapi_text)
        self.assertIn("loadScalarScript", contracts_js_text)
        self.assertIn("createApiReference", contracts_js_text)
        self.assertIn("# 站点构建工具", tools_text)
        self.assertIn("## 工具总览", tools_text)
        self.assertIn("build_site", tools_text)
        self.assertIn("MCP Inspector", tools_text)
        self.assertIn('href="site-builder.mcp-tools.yaml">下载原始快照<', tools_text)


if __name__ == "__main__":
    unittest.main()
