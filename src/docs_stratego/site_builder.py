from __future__ import annotations

import json
import os
import shutil
from dataclasses import dataclass
from html import escape
from pathlib import Path

import yaml


HOME_CSS = """:root {
  --docs-card-border: rgba(15, 23, 42, 0.12);
  --docs-card-bg: rgba(255, 255, 255, 0.82);
  --docs-muted: #5b6577;
  --md-grid-max-width: 100%;
  --docs-contract-border: rgba(15, 23, 42, 0.1);
}

.md-grid {
  width: 100%;
  max-width: none !important;
}

.md-main__inner {
  width: 100%;
  max-width: none !important;
  margin: 0 !important;
}

.md-content {
  flex: 1 1 auto;
  width: 100%;
  max-width: none !important;
}

.md-content__inner {
  width: 100%;
  max-width: none !important;
  margin: 0 !important;
  padding-left: 0.6rem;
  padding-right: 0.6rem;
}

@media screen and (min-width: 76.25em) {
  .md-content__inner {
    padding-left: 1rem;
    padding-right: 1rem;
  }
}

.md-sidebar--secondary:has(.md-nav:empty) {
  display: none;
}

.md-sidebar--secondary:has(.md-nav:empty) ~ .md-content {
  max-width: none !important;
}

.md-sidebar--primary .md-nav__item--nested > .md-nav__link {
  font-weight: 700;
  color: #344054;
}

.md-sidebar--primary .md-nav__list .md-nav__list {
  margin-left: 0.55rem;
  padding-left: 0.75rem;
  border-left: 1px solid rgba(15, 23, 42, 0.12);
}

.md-sidebar--primary .md-nav__list .md-nav__list .md-nav__link {
  font-size: 0.92rem;
}

.md-sidebar--primary .md-nav__item .md-nav__item .md-nav__link {
  opacity: 0.9;
}

.project-card-grid {
  display: grid;
  gap: 1rem;
  margin: 1rem 0 2rem;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
}

.project-card {
  display: block;
  padding: 1rem 1.1rem;
  border: 1px solid var(--docs-card-border);
  border-radius: 14px;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.94), var(--docs-card-bg));
  box-shadow: 0 10px 24px rgba(15, 23, 42, 0.06);
  color: inherit;
}

.project-card h3,
.project-card h4,
.project-card p,
.project-card ul {
  margin-top: 0;
}

.project-card h3 {
  margin-bottom: 0.35rem;
}

.project-card h4 {
  margin-bottom: 0.35rem;
  color: #23324d;
  font-size: 0.92rem;
}

.project-card p {
  color: var(--docs-muted);
}

.project-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.55rem;
  margin: 0.8rem 0 1rem;
}

.project-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  padding: 0.28rem 0.65rem;
  border-radius: 999px;
  background: rgba(67, 97, 238, 0.08);
  color: #2846a7;
  font-size: 0.82rem;
  font-weight: 600;
  text-decoration: none;
}

.project-section-list {
  margin: 0 0 0.9rem;
  padding-left: 1.1rem;
}

.project-section-list li + li {
  margin-top: 0.25rem;
}

.md-tabs__item {
  position: relative;
}

.md-tabs,
.md-tabs__list {
  overflow: visible !important;
}

.md-tabs__list {
  contain: none !important;
}

.docs-tab-toggle {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.9rem;
  font-weight: 600;
}

.docs-tab-toggle::after {
  content: "";
  width: 0.45rem;
  height: 0.45rem;
  border-right: 2px solid currentColor;
  border-bottom: 2px solid currentColor;
  transform: rotate(45deg) translateY(-0.08rem);
  opacity: 0.72;
}

.md-tabs__item--active > .docs-tab-toggle {
  font-weight: 700;
  color: #fff;
}

.docs-tab-dropdown {
  position: absolute;
  top: calc(100% + 0.4rem);
  left: 0;
  min-width: 15rem;
  padding: 0.45rem 0;
  border-radius: 0.8rem;
  background: rgba(20, 28, 56, 0.96);
  box-shadow: 0 18px 40px rgba(15, 23, 42, 0.24);
  opacity: 0;
  pointer-events: none;
  transform: translateY(-0.25rem);
  transition: opacity 0.18s ease, transform 0.18s ease;
  z-index: 20;
}

.docs-tab-dropdown.is-open {
  opacity: 1;
  pointer-events: auto;
  transform: translateY(0);
}

.docs-tab-dropdown__link {
  display: block;
  padding: 0.55rem 0.9rem;
  color: rgba(255, 255, 255, 0.92);
  font-size: 0.78rem;
  text-decoration: none;
  white-space: nowrap;
}

.docs-tab-dropdown__link:hover {
  background: rgba(255, 255, 255, 0.08);
}

.docs-tab-dropdown__group {
  padding: 0.45rem 0.9rem 0.25rem;
  color: rgba(255, 255, 255, 0.58);
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.docs-tab-dropdown__link--external {
  margin-top: 0.25rem;
  border-top: 1px solid rgba(255, 255, 255, 0.14);
}

.docs-tab-dropdown__link--external::before {
  content: "GH";
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 1.35rem;
  margin-right: 0.45rem;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.12);
  font-size: 0.64rem;
  font-weight: 700;
}

.docs-sidebar-section-only .md-nav__item--nested {
  margin-top: 0;
}

.docs-contract-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem;
  margin: 0.6rem 0 1rem;
}

.docs-contract-note {
  margin: 0 0 1rem;
  color: var(--docs-muted);
}

.docs-contract-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  padding: 0.28rem 0.7rem;
  border-radius: 999px;
  border: 1px solid var(--docs-contract-border);
  background: rgba(255, 255, 255, 0.85);
  color: #22324d;
  font-size: 0.82rem;
  font-weight: 600;
  text-decoration: none;
}

.docs-openapi-scalar {
  min-height: 72vh;
  border: 1px solid var(--docs-contract-border);
  border-radius: 18px;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.94);
}

.docs-openapi-scalar.is-loading,
.docs-openapi-scalar.is-error {
  display: grid;
  place-items: center;
  padding: 2rem;
  color: var(--docs-muted);
}

.docs-openapi-scalar__status {
  font-size: 0.95rem;
}

.docs-openapi-scalar__error {
  max-width: 42rem;
  text-align: center;
}

.docs-openapi-scalar__error a {
  font-weight: 700;
}
"""

ALLOWED_ACCESS = {"public", "private"}
CONTRACT_FILE_SUFFIXES = (
    (".openapi.yaml", "openapi"),
    (".openapi.yml", "openapi"),
    (".openapi.json", "openapi"),
    (".mcp-tools.yaml", "mcp_tools"),
    (".mcp-tools.yml", "mcp_tools"),
    (".mcp-tools.json", "mcp_tools"),
)
SCALAR_CDN_URL = "https://cdn.jsdelivr.net/npm/@scalar/api-reference"


@dataclass(frozen=True)
class SourceRepository:
    name: str
    title: str
    source_type: str
    repo_url: str | None = None
    git_url: str | None = None
    branch: str = "main"
    docs_path: str = "docs"
    local_path: str | None = None
    submodule_path: str | None = None

    def resolve_docs_root(self, project_root: Path | None = None) -> Path:
        if self.source_type == "local":
            if not self.local_path:
                raise ValueError(f"{self.name} missing local_path")
            base = project_root or Path.cwd()
            return (base / self.local_path).resolve()
        if self.source_type == "submodule_sparse":
            if not self.submodule_path:
                raise ValueError(f"{self.name} missing submodule_path")
            base = project_root or Path.cwd()
            return (base / self.submodule_path / self.docs_path).resolve()
        if self.source_type == "git_sparse":
            base = project_root or Path.cwd()
            return (base / "sources" / self.name / self.docs_path).resolve()
        raise ValueError(f"unsupported source_type: {self.source_type}")


@dataclass(frozen=True)
class NavNode:
    title: str
    path: str | None = None
    access: str | None = None
    children: tuple[NavNode, ...] = ()
    render_kind: str = "markdown"


@dataclass(frozen=True)
class RootIndexMetadata:
    title: str
    home_access: str
    nav: tuple[NavNode, ...]


@dataclass(frozen=True)
class PageLink:
    title: str
    path: str
    access: str
    source_path: str
    render_kind: str = "markdown"


@dataclass(frozen=True)
class RepoTabLink:
    title: str
    url: str
    kind: str = "section"


def normalize_access(value: str | None, context: Path) -> str | None:
    if value is None:
        return None
    if value not in ALLOWED_ACCESS:
        raise ValueError(f"{context} has invalid access value: {value}")
    return value


def detect_render_kind(raw_path: str, index_path: Path, title: str) -> str:
    lower_path = raw_path.lower()
    if lower_path.endswith(".md"):
        return "markdown"
    for suffix, render_kind in CONTRACT_FILE_SUFFIXES:
        if lower_path.endswith(suffix):
            return render_kind
    raise ValueError(f"{index_path} page item '{title}' points to an unsupported file: {raw_path}")


def rendered_page_path(relative_path: str, render_kind: str) -> str:
    if render_kind == "markdown":
        return relative_path
    path = Path(relative_path)
    if not path.suffix:
        raise ValueError(f"{relative_path} missing file suffix")
    return path.with_suffix(".md").as_posix()


def load_structured_document(file_path: Path) -> tuple[dict, str]:
    text = file_path.read_text(encoding="utf-8")
    if file_path.suffix.lower() == ".json":
        payload = json.loads(text)
    else:
        payload = yaml.safe_load(text) or {}
    if not isinstance(payload, dict):
        raise ValueError(f"{file_path} must contain a top-level object")
    return payload, text


def schema_ref_name(ref: str) -> str:
    return ref.rsplit("/", 1)[-1]


def summarize_schema(schema: object) -> str:
    if not isinstance(schema, dict) or not schema:
        return "-"
    if "$ref" in schema:
        return f"`{schema_ref_name(str(schema['$ref']))}`"
    if "enum" in schema and isinstance(schema["enum"], list):
        values = [str(item) for item in schema["enum"][:4]]
        suffix = "..." if len(schema["enum"]) > 4 else ""
        return f"`enum[{', '.join(values)}{suffix}]`"
    schema_type = schema.get("type")
    if schema_type == "object":
        properties = schema.get("properties", {})
        prop_names = list(properties.keys()) if isinstance(properties, dict) else []
        required = schema.get("required", [])
        prop_preview = ", ".join(prop_names[:5])
        required_preview = ", ".join(str(item) for item in required[:5]) if isinstance(required, list) else ""
        parts = ["object"]
        if prop_preview:
            parts.append(f"fields: {prop_preview}{'...' if len(prop_names) > 5 else ''}")
        if required_preview:
            parts.append(f"required: {required_preview}{'...' if len(required) > 5 else ''}")
        return "; ".join(parts)
    if schema_type == "array":
        return f"array<{summarize_schema(schema.get('items'))}>"
    if isinstance(schema_type, list):
        return " | ".join(str(item) for item in schema_type)
    if isinstance(schema_type, str):
        return schema_type
    if "oneOf" in schema and isinstance(schema["oneOf"], list):
        options = [summarize_schema(item) for item in schema["oneOf"][:3]]
        suffix = ", ..." if len(schema["oneOf"]) > 3 else ""
        return f"oneOf({', '.join(options)}{suffix})"
    if "anyOf" in schema and isinstance(schema["anyOf"], list):
        options = [summarize_schema(item) for item in schema["anyOf"][:3]]
        suffix = ", ..." if len(schema["anyOf"]) > 3 else ""
        return f"anyOf({', '.join(options)}{suffix})"
    return "-"


def markdown_cell(value: object) -> str:
    if value is None:
        return ""
    text = str(value).replace("\n", "<br>")
    return text.replace("|", "\\|")


def dump_code_block(data: object) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)


def html_fragment_id(value: str) -> str:
    sanitized = [
        char.lower() if char.isalnum() else "-" for char in value
    ]
    collapsed = "".join(sanitized).strip("-")
    while "--" in collapsed:
        collapsed = collapsed.replace("--", "-")
    return collapsed or "docs-contract"


def extract_h1(markdown_text: str, file_path: Path) -> str:
    for line in markdown_text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError(f"{file_path} missing H1 title")


def parse_front_matter(markdown_text: str, file_path: Path) -> tuple[dict, str]:
    if not markdown_text.startswith("---\n"):
        return {}, markdown_text
    marker = "\n---\n"
    end_index = markdown_text.find(marker, 4)
    if end_index == -1:
        raise ValueError(f"{file_path} has unterminated front matter")
    metadata = yaml.safe_load(markdown_text[4:end_index]) or {}
    body = markdown_text[end_index + len(marker) :]
    return metadata, body


def markdown_url(repo_name: str, relative_path: str) -> str:
    if relative_path == "index.md":
        return f"/{repo_name}/"
    no_suffix = relative_path.removesuffix(".md")
    if no_suffix.endswith("/index"):
        no_suffix = no_suffix[: -len("/index")]
    return f"/{repo_name}/{no_suffix}/"


def resource_url(repo_name: str, relative_path: str) -> str:
    return f"/{repo_name}/{relative_path}"


def append_entry(
    entries: list[dict],
    repo_name: str,
    relative_path: str,
    url: str,
    access: str,
    kind: str,
) -> None:
    entries.append(
        {
            "source": repo_name,
            "path": relative_path,
            "url": url,
            "access": access,
            "kind": kind,
        }
    )


def append_nav_lines(lines: list[str], items: list[dict], indent: int) -> None:
    for item in items:
        label, value = next(iter(item.items()))
        if isinstance(value, list):
            lines.append(" " * indent + f'- "{label}":')
            append_nav_lines(lines, value, indent + 2)
        else:
            lines.append(" " * indent + f'- "{label}": {value}')


def is_hidden_path(relative_path: Path) -> bool:
    return any(part.startswith(".") for part in relative_path.parts)


def is_resource_path(relative_path: Path) -> bool:
    return "assets" in relative_path.parts


def validate_markdown_title(file_path: Path) -> None:
    _, body = parse_front_matter(file_path.read_text(encoding="utf-8"), file_path)
    extract_h1(body, file_path)


def validate_openapi_document(document: dict, file_path: Path) -> None:
    openapi_version = document.get("openapi")
    if not isinstance(openapi_version, str) or not openapi_version.startswith("3."):
        raise ValueError(f"{file_path} must declare OpenAPI 3.x")
    info = document.get("info")
    if not isinstance(info, dict):
        raise ValueError(f"{file_path} missing info block")
    if not isinstance(info.get("title"), str) or not info["title"].strip():
        raise ValueError(f"{file_path} missing info.title")
    if not isinstance(info.get("version"), str) or not info["version"].strip():
        raise ValueError(f"{file_path} missing info.version")
    paths = document.get("paths")
    if paths is not None and not isinstance(paths, dict):
        raise ValueError(f"{file_path} paths must be an object")


def extract_mcp_tools_payload(document: dict) -> dict:
    if isinstance(document.get("tools"), list):
        return document
    result = document.get("result")
    if isinstance(result, dict) and isinstance(result.get("tools"), list):
        return result
    raise ValueError("missing MCP tools payload")


def validate_mcp_tools_document(document: dict, file_path: Path) -> dict:
    payload = extract_mcp_tools_payload(document)
    tools = payload.get("tools")
    if not isinstance(tools, list) or not tools:
        raise ValueError(f"{file_path} must declare a non-empty tools list")
    for index, item in enumerate(tools, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"{file_path} tool #{index} must be an object")
        if not isinstance(item.get("name"), str) or not item["name"].strip():
            raise ValueError(f"{file_path} tool #{index} missing name")
        if not isinstance(item.get("description"), str) or not item["description"].strip():
            raise ValueError(f"{file_path} tool '{item['name']}' missing description")
        input_schema = item.get("inputSchema")
        if not isinstance(input_schema, dict):
            raise ValueError(f"{file_path} tool '{item['name']}' missing inputSchema")
    return payload


def validate_contract_document(file_path: Path, render_kind: str) -> tuple[dict, str]:
    document, raw_text = load_structured_document(file_path)
    if render_kind == "openapi":
        validate_openapi_document(document, file_path)
        return document, raw_text
    if render_kind == "mcp_tools":
        return validate_mcp_tools_document(document, file_path), raw_text
    raise ValueError(f"{file_path} unsupported render kind: {render_kind}")


def render_markdown_table(headers: list[str], rows: list[list[object]]) -> list[str]:
    if not rows:
        return []
    lines = [
        "| " + " | ".join(markdown_cell(header) for header in headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(markdown_cell(cell) for cell in row) + " |")
    return lines


def relative_link(from_path: str, to_path: str) -> str:
    return os.path.relpath(to_path, Path(from_path).parent.as_posix())


def render_openapi_page(page: PageLink, file_path: Path) -> str:
    document, _raw_text = validate_contract_document(file_path, "openapi")
    info = document["info"]
    title = page.title
    summary = info.get("summary") or info.get("description") or ""
    container_id = html_fragment_id(page.path)
    raw_contract_link = relative_link(page.path, page.source_path)
    server_count = len(document.get("servers", [])) if isinstance(document.get("servers"), list) else 0
    tag_count = len(document.get("tags", [])) if isinstance(document.get("tags"), list) else 0
    path_count = len(document.get("paths", {})) if isinstance(document.get("paths"), dict) else 0

    lines = [
        f"# {title}",
        "",
        f"> 本页由 Scalar 渲染，源文件为 `{page.source_path}`",
        "",
    ]
    if summary:
        lines.extend([str(summary).strip(), ""])

    lines.extend(
        [
            '<div class="docs-contract-meta">',
            f'<span class="docs-contract-pill">OpenAPI {escape(str(document.get("openapi", "")))}</span>',
            f'<span class="docs-contract-pill">Spec {escape(str(info.get("version", "")))}</span>',
            f'<span class="docs-contract-pill">{path_count} paths</span>',
            f'<span class="docs-contract-pill">{tag_count} tags</span>',
            f'<span class="docs-contract-pill">{server_count} servers</span>',
            f'<a class="docs-contract-pill" href="{escape(raw_contract_link)}">下载原始契约</a>',
            "</div>",
            "",
            '<p class="docs-contract-note">交互式接口文档由 Scalar API Reference 提供；站点权限仍以根 <code>docs/index.md</code> 的 <code>access</code> 为准。</p>',
            "",
            f'<div id="{escape(container_id)}" class="docs-openapi-scalar is-loading" data-openapi-url="{escape(raw_contract_link)}" data-openapi-title="{escape(str(title))}" data-openapi-version="{escape(str(info.get("version", "")))}">',
            '  <div class="docs-openapi-scalar__status">正在加载 Scalar API Reference...</div>',
            "</div>",
            "",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def render_mcp_tools_page(page: PageLink, file_path: Path) -> str:
    payload, raw_text = validate_contract_document(file_path, "mcp_tools")
    tools = [item for item in payload.get("tools", []) if isinstance(item, dict)]

    lines = [
        f"# {page.title}",
        "",
        f"> 本页基于 MCP tools 快照渲染，源文件为 `{page.source_path}`",
        "",
        '<p class="docs-contract-note">MCP 目前没有像 Swagger UI 那样成熟的通用文档 UI；本页提供静态参考，交互调试建议使用 MCP Inspector。</p>',
        "",
        '<div class="docs-contract-meta">',
        f'<span class="docs-contract-pill">{len(tools)} tools</span>',
        f'<a class="docs-contract-pill" href="{escape(relative_link(page.path, page.source_path))}">下载原始快照</a>',
        '<a class="docs-contract-pill" href="https://modelcontextprotocol.io/docs/tools/inspector" target="_blank" rel="noreferrer">MCP Inspector</a>',
        "</div>",
        "",
        "## 工具总览",
        "",
    ]

    overview_rows = []
    for tool in tools:
        overview_rows.append(
            [
                tool.get("name", ""),
                tool.get("title", ""),
                summarize_schema(tool.get("inputSchema")),
                tool.get("description", ""),
            ]
        )
    lines.extend(render_markdown_table(["名称", "标题", "输入", "说明"], overview_rows))
    lines.append("")

    for tool in tools:
        name = tool.get("name", "")
        lines.extend([f"### `{name}`", ""])
        if tool.get("description"):
            lines.extend([str(tool["description"]).strip(), ""])
        detail_rows = [
            ["标题", tool.get("title", "")],
            ["输入 Schema", summarize_schema(tool.get("inputSchema"))],
            ["输出 Schema", summarize_schema(tool.get("outputSchema"))],
        ]
        lines.extend(render_markdown_table(["字段", "值"], detail_rows))
        lines.append("")

        annotations = tool.get("annotations")
        if isinstance(annotations, dict) and annotations:
            annotation_rows = [[key, value] for key, value in annotations.items()]
            lines.extend(["Annotations", ""])
            lines.extend(render_markdown_table(["字段", "值"], annotation_rows))
            lines.append("")

        input_schema = tool.get("inputSchema")
        if isinstance(input_schema, dict):
            lines.extend(["输入 Schema", "", "```json", dump_code_block(input_schema), "```", ""])

        output_schema = tool.get("outputSchema")
        if isinstance(output_schema, dict):
            lines.extend(["输出 Schema", "", "```json", dump_code_block(output_schema), "```", ""])

    code_lang = "json" if file_path.suffix.lower() == ".json" else "yaml"
    lines.extend(
        [
            "<details>",
            "<summary>原始 MCP tools 快照</summary>",
            "",
            f"```{code_lang}",
            raw_text.rstrip(),
            "```",
            "",
            "</details>",
            "",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def render_contract_page(page: PageLink, file_path: Path) -> str:
    if page.render_kind == "openapi":
        return render_openapi_page(page, file_path)
    if page.render_kind == "mcp_tools":
        return render_mcp_tools_page(page, file_path)
    raise ValueError(f"{file_path} unsupported render kind: {page.render_kind}")


def parse_nav_node(item: dict, index_path: Path) -> NavNode:
    if not isinstance(item, dict):
        raise ValueError(f"{index_path} contains a non-object nav item")

    title = item.get("title")
    if not isinstance(title, str) or not title.strip():
        raise ValueError(f"{index_path} nav item missing title")

    has_path = "path" in item
    has_children = "children" in item
    if has_path == has_children:
        raise ValueError(f"{index_path} nav item '{title}' must define either path or children")

    if has_path:
        raw_path = item["path"]
        if not isinstance(raw_path, str) or not raw_path.strip():
            raise ValueError(f"{index_path} nav item '{title}' missing path")
        relative_path = Path(raw_path)
        if relative_path.is_absolute() or ".." in relative_path.parts:
            raise ValueError(f"{index_path} nav item '{title}' contains forbidden path: {raw_path}")
        if is_hidden_path(relative_path) or is_resource_path(relative_path):
            raise ValueError(f"{index_path} page item '{title}' points to a forbidden location: {raw_path}")
        render_kind = detect_render_kind(raw_path, index_path, title)
        access = normalize_access(item.get("access"), index_path)
        if access is None:
            raise ValueError(f"{index_path} page item '{title}' missing access")
        return NavNode(
            title=title.strip(),
            path=relative_path.as_posix(),
            access=access,
            render_kind=render_kind,
        )

    if item.get("access") is not None:
        raise ValueError(f"{index_path} section item '{title}' cannot define access")

    children_raw = item.get("children")
    if not isinstance(children_raw, list) or not children_raw:
        raise ValueError(f"{index_path} section item '{title}' must define non-empty children")

    return NavNode(
        title=title.strip(),
        children=tuple(parse_nav_node(child, index_path) for child in children_raw),
    )


def parse_root_index(docs_root: Path) -> RootIndexMetadata:
    index_path = docs_root / "index.md"
    if not index_path.exists():
        raise ValueError(f"{docs_root} missing index.md")

    text = index_path.read_text(encoding="utf-8")
    metadata, body = parse_front_matter(text, index_path)
    mkdocs_meta = metadata.get("mkdocs", {})
    title = metadata.get("title") or extract_h1(body, index_path)
    nav_items = tuple(parse_nav_node(item, index_path) for item in mkdocs_meta.get("nav", []))
    home_access = normalize_access(mkdocs_meta.get("home_access"), index_path) or "public"
    return RootIndexMetadata(title=title, home_access=home_access, nav=nav_items)


def iter_docs_directories(docs_root: Path) -> list[Path]:
    directories = [docs_root]
    directories.extend(path for path in docs_root.rglob("*") if path.is_dir())
    return sorted(directories)


def validate_directory_indexes(docs_root: Path) -> None:
    for directory in iter_docs_directories(docs_root):
        relative_dir = directory.relative_to(docs_root)
        if relative_dir.parts and (is_hidden_path(relative_dir) or is_resource_path(relative_dir)):
            continue
        if not (directory / "index.md").exists():
            raise ValueError(f"{directory} missing index.md")


def collect_declared_pages(
    repo_name: str,
    nodes: tuple[NavNode, ...],
    declared_pages: list[PageLink],
    seen_sources: set[str],
    seen_outputs: set[str],
) -> list[dict]:
    nav_items: list[dict] = []
    for node in nodes:
        if node.path is not None:
            output_path = rendered_page_path(node.path, node.render_kind)
            if node.path in seen_sources:
                raise ValueError(f"duplicate page declaration: {node.path}")
            if output_path in seen_outputs:
                raise ValueError(f"duplicate rendered page declaration: {output_path}")
            seen_sources.add(node.path)
            seen_outputs.add(output_path)
            declared_pages.append(
                PageLink(
                    title=node.title,
                    path=output_path,
                    access=node.access or "public",
                    source_path=node.path,
                    render_kind=node.render_kind,
                )
            )
            nav_items.append({node.title: f"{repo_name}/{output_path}"})
            continue
        nav_items.append(
            {
                node.title: collect_declared_pages(
                    repo_name, node.children, declared_pages, seen_sources, seen_outputs
                )
            }
        )
    return nav_items


def flatten_page_links(nodes: tuple[NavNode, ...]) -> list[PageLink]:
    pages: list[PageLink] = []
    for node in nodes:
        if node.path is not None:
            pages.append(
                PageLink(
                    title=node.title,
                    path=rendered_page_path(node.path, node.render_kind),
                    access=node.access or "public",
                    source_path=node.path,
                    render_kind=node.render_kind,
                )
            )
            continue
        pages.extend(flatten_page_links(node.children))
    return pages


def resolve_node_target(node: NavNode) -> str:
    if node.path is not None:
        return rendered_page_path(node.path, node.render_kind)
    for child in node.children:
        target = resolve_node_target(child)
        if target:
            return target
    raise ValueError(f"section '{node.title}' has no reachable page target")


def build_repo_tab_links(repo: SourceRepository, nodes: tuple[NavNode, ...]) -> list[RepoTabLink]:
    links = [
        RepoTabLink(title="简介", url=markdown_url(repo.name, "index.md"), kind="section"),
        *[
            RepoTabLink(title=node.title, url=markdown_url(repo.name, resolve_node_target(node)), kind="section")
            for node in nodes
        ],
    ]
    if repo.repo_url:
        links.append(RepoTabLink(title="GitHub 仓库", url=repo.repo_url, kind="external"))
    return links


def validate_declared_pages(docs_root: Path, declared_pages: list[PageLink]) -> None:
    for page in declared_pages:
        file_path = docs_root / page.source_path
        if not file_path.exists():
            raise ValueError(f"{file_path} declared in root index but does not exist")
        if page.render_kind == "markdown":
            validate_markdown_title(file_path)
            continue
        validate_contract_document(file_path, page.render_kind)


def validate_markdown_coverage(docs_root: Path, declared_pages: list[PageLink]) -> None:
    declared_markdown = {page.source_path for page in declared_pages if page.render_kind == "markdown"}
    declared_markdown.add("index.md")
    undeclared: list[str] = []

    for file_path in sorted(path for path in docs_root.rglob("*") if path.is_file()):
        relative_path = file_path.relative_to(docs_root)
        if is_hidden_path(relative_path):
            continue
        if is_resource_path(relative_path):
            if file_path.suffix.lower() == ".md":
                raise ValueError(f"{file_path} invalid: assets directory cannot contain Markdown")
            continue
        if file_path.suffix.lower() != ".md":
            continue
        validate_markdown_title(file_path)
        if relative_path.as_posix() not in declared_markdown:
            undeclared.append(relative_path.as_posix())

    if undeclared:
        raise ValueError(f"Markdown files not declared in mkdocs.nav: {', '.join(undeclared)}")


def build_directory_access_map(home_access: str, declared_pages: list[PageLink]) -> dict[Path, str]:
    access_map = {Path(): home_access}
    for page in declared_pages:
        path = Path(page.source_path)
        if path.name == "index.md":
            access_map[path.parent] = page.access
    return access_map


def resolve_resource_access(access_map: dict[Path, str], relative_path: Path) -> str:
    current = relative_path.parent
    while True:
        if current in access_map:
            return access_map[current]
        if not current.parts:
            return access_map[Path()]
        current = current.parent


def collect_resource_entries(
    repo: SourceRepository,
    docs_root: Path,
    access_map: dict[Path, str],
    source_access_overrides: dict[str, str],
    entries: list[dict],
) -> None:
    for file_path in sorted(path for path in docs_root.rglob("*") if path.is_file()):
        relative_path = file_path.relative_to(docs_root)
        if is_hidden_path(relative_path):
            continue
        if file_path.suffix.lower() == ".md":
            continue
        access = source_access_overrides.get(relative_path.as_posix()) or resolve_resource_access(
            access_map, relative_path
        )
        append_entry(
            entries,
            repo.name,
            relative_path.as_posix(),
            resource_url(repo.name, relative_path.as_posix()),
            access,
            "resource",
        )


def build_repo_nav_and_entries(
    repo: SourceRepository, docs_root: Path
) -> tuple[list[dict], list[dict], RootIndexMetadata]:
    validate_directory_indexes(docs_root)
    root_metadata = parse_root_index(docs_root)

    declared_pages: list[PageLink] = []
    repo_nav = collect_declared_pages(repo.name, root_metadata.nav, declared_pages, set(), set())
    validate_declared_pages(docs_root, declared_pages)
    validate_markdown_coverage(docs_root, declared_pages)

    entries: list[dict] = []
    append_entry(entries, repo.name, "index.md", markdown_url(repo.name, "index.md"), root_metadata.home_access, "page")
    for page in sorted(declared_pages, key=lambda item: item.path):
        append_entry(
            entries,
            repo.name,
            page.path,
            markdown_url(repo.name, page.path),
            page.access,
            "page",
        )

    access_map = build_directory_access_map(root_metadata.home_access, declared_pages)
    source_access_overrides = {
        page.source_path: page.access for page in declared_pages if page.render_kind != "markdown"
    }
    collect_resource_entries(repo, docs_root, access_map, source_access_overrides, entries)

    return [{"概览": f"{repo.name}/index.md"}, *repo_nav], entries, root_metadata


def matches_keywords(page: PageLink, keywords: tuple[str, ...]) -> bool:
    haystack = f"{page.title} {page.path}".lower()
    return any(keyword in haystack for keyword in keywords)


def classify_project_sections(repo: SourceRepository, pages: list[PageLink]) -> list[tuple[str, list[PageLink]]]:
    intro_keywords = ("getting-started", "快速开始", "入门", "开始")
    user_keywords = (
        "user-guide",
        "admin-guide",
        "handover",
        "用户",
        "安装",
        "配置",
        "使用",
        "部署",
        "运维",
        "release",
    )
    developer_keywords = (
        "plugin",
        "backend",
        "application",
        "scaffold",
        "sdk",
        "api",
        "开发",
        "插件",
        "应用",
    )
    internal_prefixes = (
        "00-governance/",
        "01-discovery/",
        "02-requirements/",
        "03-solution/",
        "04-delivery/",
        "05-quality/",
        "06-release/",
        "07-operations/",
        "08-handover/",
        "09-evolution/",
        "traceability/",
        "01-framework-development/",
    )

    used: set[str] = set()

    def pick(predicate, limit: int, include_indexes: bool = True) -> list[PageLink]:
        picked: list[PageLink] = []
        for page in pages:
            if page.path in used:
                continue
            if not include_indexes and page.path.endswith("/index.md"):
                continue
            if predicate(page):
                picked.append(page)
                used.add(page.path)
                if len(picked) >= limit:
                    break
        return picked

    intro: list[PageLink] = [
        PageLink(title="项目首页", path="index.md", access="public", source_path="index.md")
    ]
    used.add("index.md")
    intro.extend(pick(lambda page: matches_keywords(page, intro_keywords), limit=2, include_indexes=False))

    user_guides = pick(lambda page: matches_keywords(page, user_keywords), limit=4)
    developer_guides = pick(lambda page: matches_keywords(page, developer_keywords), limit=4)
    internal_docs = pick(
        lambda page: page.access == "private" or any(page.path.startswith(prefix) for prefix in internal_prefixes),
        limit=5,
    )

    return [
        ("入门说明", intro),
        ("用户指南", user_guides),
        ("开发者指南", developer_guides),
        ("项目开发文档（内部）", internal_docs),
    ]


def build_project_card(repo: SourceRepository, pages: list[PageLink]) -> str:
    section_html: list[str] = []
    for heading, section_pages in classify_project_sections(repo, pages):
        if not section_pages:
            continue
        section_html.append(f"<h4>{escape(heading)}</h4>")
        section_html.append('<ul class="project-section-list">')
        for page in section_pages:
            section_html.append(
                f'<li><a href="{escape(markdown_url(repo.name, page.path))}">{escape(page.title)}</a></li>'
            )
        section_html.append("</ul>")

    meta_links = [
        f'<a class="project-pill" href="{escape(markdown_url(repo.name, "index.md"))}">文档首页</a>',
    ]
    if repo.repo_url:
        meta_links.append(f'<a class="project-pill" href="{escape(repo.repo_url)}">GitHub 仓库</a>')

    return "\n".join(
        [
            '<section class="project-card">',
            f"<h3>{escape(repo.title)}</h3>",
            f'<p>统一入口聚合展示，导航顺序与页面权限均以 <code>{escape(repo.name)}/docs/index.md</code> 为准。</p>',
            f'<div class="project-meta">{"".join(meta_links)}</div>',
            *section_html,
            "</section>",
        ]
    )


def write_root_index(site_docs_dir: Path, repositories: list[SourceRepository], repo_pages: dict[str, list[PageLink]]) -> None:
    cards = "\n".join(build_project_card(repo, repo_pages[repo.name]) for repo in repositories)
    lines = [
        "# 章略·墨衡阁",
        "",
        "这是统一文档入口站点。每个项目都保留源仓自维护的目录与权限，本站只负责聚合展示、主题装配和访问控制。",
        "",
        "## 项目入口",
        "",
        '<div class="project-card-grid">',
        cards,
        "</div>",
        "",
        "## 站点约定",
        "",
        "- 目录顺序以源仓根 `docs/index.md` 的 `mkdocs.nav` 为准",
        "- 页面权限以页面节点的 `access` 为准",
        "- 私有页面仍会出现在导航中，但访问时进入登录链路",
        "",
    ]
    (site_docs_dir / "index.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_home_css(site_docs_dir: Path) -> None:
    css_path = site_docs_dir / "assets" / "stylesheets" / "home.css"
    css_path.parent.mkdir(parents=True, exist_ok=True)
    css_path.write_text(HOME_CSS, encoding="utf-8")


def write_navigation_js(site_docs_dir: Path, repo_tab_links: dict[str, list[RepoTabLink]]) -> None:
    js_path = site_docs_dir / "assets" / "javascripts" / "navigation.js"
    js_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        repo_name: [{"title": link.title, "url": link.url, "kind": link.kind} for link in links]
        for repo_name, links in repo_tab_links.items()
    }
    js_path.write_text(
        f"""const PROJECT_TAB_MENUS = {json.dumps(payload, ensure_ascii=False)};

function closeProjectMenus(root = document) {{
  root.querySelectorAll(".docs-tab-dropdown.is-open").forEach((menu) => {{
    menu.classList.remove("is-open");
    const ownerId = menu.getAttribute("data-owner-id");
    if (ownerId) {{
      const owner = root.getElementById(ownerId);
      if (owner) {{
        owner.setAttribute("aria-expanded", "false");
      }}
    }}
  }});
}}

function openProjectMenu(anchor, dropdown) {{
  closeProjectMenus(document);
  dropdown.classList.add("is-open");
  anchor.setAttribute("aria-expanded", "true");
}}

function appendMenuGroup(container, label) {{
  const group = document.createElement("div");
  group.className = "docs-tab-dropdown__group";
  group.textContent = label;
  container.appendChild(group);
}}

function appendMenuLinks(container, items) {{
  let lastKind = "";
  items.forEach((item) => {{
    if (item.kind !== lastKind) {{
      appendMenuGroup(container, item.kind === "external" ? "仓库链接" : "文档分区");
      lastKind = item.kind;
    }}
    const link = document.createElement("a");
    link.className = "docs-tab-dropdown__link";
    if (item.kind === "external") {{
      link.classList.add("docs-tab-dropdown__link--external");
    }}
    link.href = item.url;
    link.textContent = item.title;
    link.setAttribute("role", "menuitem");
    if (item.url.startsWith("http")) {{
      link.target = "_blank";
      link.rel = "noreferrer";
    }}
    container.appendChild(link);
  }});
}}

function simplifyPrimarySidebar() {{
  const activeProjects = document.querySelectorAll(
    ".md-nav--primary > .md-nav__list > .md-nav__item--section.md-nav__item--active"
  );

  activeProjects.forEach((activeProject) => {{
    if (activeProject.dataset.docsSidebarSimplified === "true") {{
      return;
    }}
    activeProject.dataset.docsSidebarSimplified = "true";

    const levelOneList = activeProject.querySelector(":scope > nav.md-nav > ul.md-nav__list");
    if (!levelOneList) {{
      return;
    }}

    const sectionItems = Array.from(levelOneList.children).filter(
      (item) => item.classList.contains("md-nav__item--nested")
    );
    if (!sectionItems.length) {{
      return;
    }}

    const activeSection =
      sectionItems.find(
        (item) =>
          item.classList.contains("md-nav__item--active") ||
          item.querySelector(":scope .md-nav__link--active, :scope .md-nav__item--active")
      ) || sectionItems[0];

    const nestedList = activeSection.querySelector(":scope > nav.md-nav > ul.md-nav__list");
    if (!nestedList) {{
      return;
    }}

    const sectionTitle = activeSection.querySelector(":scope > label .md-ellipsis")?.textContent?.trim() || "";
    const nestedChildren = Array.from(nestedList.children);
    const sectionOverview = nestedChildren.find(
      (child) =>
        child.classList.contains("md-nav__item") && !child.classList.contains("md-nav__item--nested")
    );
    if (sectionOverview) {{
      const overviewLabels = sectionOverview.querySelectorAll(
        ":scope > .md-nav__link .md-ellipsis, :scope > a.md-nav__link .md-ellipsis"
      );
      if (overviewLabels.length && sectionTitle) {{
        overviewLabels.forEach((overviewLabel) => {{
          overviewLabel.textContent = sectionTitle;
        }});
      }}
    }}

    levelOneList.innerHTML = "";
    nestedChildren.forEach((child) => {{
      levelOneList.appendChild(child);
    }});
  }});
}}

document$.subscribe(() => {{
  closeProjectMenus();
  simplifyPrimarySidebar();
  const tabAnchors = document.querySelectorAll(".md-tabs__list > .md-tabs__item > .md-tabs__link");
  tabAnchors.forEach((anchor, index) => {{
    const title = anchor.textContent?.trim() || "";
    const items = PROJECT_TAB_MENUS[title];
    if (!items || !items.length) {{
      return;
    }}

    const parent = anchor.parentElement;
    if (!parent || parent.dataset.docsMenuBound === "true") {{
      return;
    }}
    parent.dataset.docsMenuBound = "true";
    const menuToggle = anchor.cloneNode(true);
    menuToggle.classList.add("docs-tab-toggle");
    menuToggle.removeAttribute("href");
    menuToggle.setAttribute("aria-haspopup", "true");
    menuToggle.setAttribute("aria-expanded", "false");
    menuToggle.setAttribute("role", "button");
    menuToggle.setAttribute("tabindex", "0");
    menuToggle.setAttribute("aria-label", `${{title}} 菜单`);
    menuToggle.id = anchor.id || `docs-tab-toggle-${{index}}`;
    parent.replaceChild(menuToggle, anchor);

    const dropdown = document.createElement("div");
    dropdown.className = "docs-tab-dropdown";
    dropdown.setAttribute("role", "menu");
    dropdown.setAttribute("data-owner-id", menuToggle.id);
    appendMenuLinks(dropdown, items);

    parent.appendChild(dropdown);
    menuToggle.addEventListener("click", (event) => {{
      event.preventDefault();
      const opened = dropdown.classList.contains("is-open");
      if (!opened) {{
        openProjectMenu(menuToggle, dropdown);
      }} else {{
        closeProjectMenus(document);
      }}
    }});

    menuToggle.addEventListener("keydown", (event) => {{
      if (!(event.key === "Enter" || event.key === " " || event.key === "ArrowDown")) {{
        if (event.key === "Escape") {{
          closeProjectMenus(document);
        }}
        return;
      }}
      event.preventDefault();
      openProjectMenu(menuToggle, dropdown);
      dropdown.querySelector(".docs-tab-dropdown__link")?.focus();
    }});
  }});

  if (window.__docsProjectMenuHandlersBound) {{
    return;
  }}
  window.__docsProjectMenuHandlersBound = true;

  document.addEventListener("click", (event) => {{
    if (!(event.target instanceof Element) || !event.target.closest(".md-tabs__item")) {{
      closeProjectMenus(document);
    }}
  }});

  document.addEventListener("keydown", (event) => {{
    if (event.key === "Escape") {{
      closeProjectMenus(document);
    }}
  }});
}});
""",
        encoding="utf-8",
    )


def write_contracts_js(site_docs_dir: Path) -> None:
    js_path = site_docs_dir / "assets" / "javascripts" / "contracts.js"
    js_path.parent.mkdir(parents=True, exist_ok=True)
    js_path.write_text(
        f"""const SCALAR_CDN_URL = "{SCALAR_CDN_URL}";

let scalarScriptPromise = null;
let scalarMountedReferences = [];

function loadScalarScript() {{
  if (window.Scalar && typeof window.Scalar.createApiReference === "function") {{
    return Promise.resolve(window.Scalar);
  }}
  if (scalarScriptPromise) {{
    return scalarScriptPromise;
  }}
  scalarScriptPromise = new Promise((resolve, reject) => {{
    const existing = document.querySelector('script[data-docs-scalar-cdn="true"]');
    if (existing) {{
      existing.addEventListener("load", () => resolve(window.Scalar), {{ once: true }});
      existing.addEventListener("error", () => reject(new Error("Scalar CDN load failed")), {{ once: true }});
      return;
    }}
    const script = document.createElement("script");
    script.src = SCALAR_CDN_URL;
    script.async = true;
    script.dataset.docsScalarCdn = "true";
    script.addEventListener("load", () => resolve(window.Scalar), {{ once: true }});
    script.addEventListener("error", () => reject(new Error("Scalar CDN load failed")), {{ once: true }});
    document.head.appendChild(script);
  }});
  return scalarScriptPromise;
}}

function resolveScalarTheme() {{
  const scheme = document.body?.getAttribute("data-md-color-scheme") || "";
  return scheme === "slate" ? "deepSpace" : "default";
}}

function clearMountedScalarReferences() {{
  scalarMountedReferences.forEach((instance) => {{
    if (instance && typeof instance.destroy === "function") {{
      try {{
        instance.destroy();
      }} catch (_error) {{
        // ignore Scalar cleanup errors
      }}
    }}
  }});
  scalarMountedReferences = [];
}}

function renderScalarError(container, specUrl) {{
  container.classList.remove("is-loading");
  container.classList.add("is-error");
  container.innerHTML = `
    <div class="docs-openapi-scalar__error">
      <p>Scalar API Reference 加载失败。</p>
      <p><a href="${{specUrl}}">打开原始契约</a></p>
    </div>
  `;
}}

async function mountScalarReferences(root = document) {{
  const containers = Array.from(root.querySelectorAll(".docs-openapi-scalar[data-openapi-url]"));
  if (!containers.length) {{
    clearMountedScalarReferences();
    return;
  }}
  clearMountedScalarReferences();
  let scalarApi = null;
  try {{
    scalarApi = await loadScalarScript();
  }} catch (_error) {{
    containers.forEach((container) => renderScalarError(container, container.dataset.openapiUrl || "#"));
    return;
  }}
  if (!scalarApi || typeof scalarApi.createApiReference !== "function") {{
    containers.forEach((container) => renderScalarError(container, container.dataset.openapiUrl || "#"));
    return;
  }}
  containers.forEach((container) => {{
    const specUrl = container.dataset.openapiUrl;
    if (!specUrl || !container.id) {{
      return;
    }}
    container.classList.remove("is-loading", "is-error");
    container.innerHTML = "";
    try {{
      const instance = scalarApi.createApiReference(`#${{container.id}}`, {{
        url: specUrl,
        theme: resolveScalarTheme(),
        layout: "modern",
        showSidebar: true,
        showDeveloperTools: "never",
        withDefaultFonts: false,
      }});
      scalarMountedReferences.push(instance);
    }} catch (_error) {{
      renderScalarError(container, specUrl);
    }}
  }});
}}

document$.subscribe(() => {{
  mountScalarReferences();
}});
""",
        encoding="utf-8",
    )


def write_access_control_js(site_docs_dir: Path, pages: list[dict]) -> None:
    js_path = site_docs_dir / "assets" / "javascripts" / "access-control.js"
    js_path.parent.mkdir(parents=True, exist_ok=True)
    private_urls = sorted({item["url"] for item in pages if item["access"] == "private"})
    js_path.write_text(
        f"""const PRIVATE_URLS = new Set({json.dumps(private_urls, ensure_ascii=False)});
const AUTH_POPUP_MESSAGE_TYPE = "docs-auth-popup-complete";
const AUTH_POPUP_CALLBACK_PATH = "/assets/auth/popup-complete.html";
const AUTH_STATUS_TTL_MS = 60 * 1000;

let authPopup = null;
let authPopupMonitor = null;
let authFlowId = 0;
let pendingTargetUrl = "";
let authStatus = "unknown";
let authStatusCheckedAt = 0;
let authStatusRequest = null;

function normalizeSitePath(rawUrl) {{
  try {{
    const url = new URL(rawUrl, window.location.origin);
    if (url.origin !== window.location.origin) {{
      return null;
    }}
    let path = url.pathname || "/";
    if (path.endsWith("/index.html")) {{
      path = path.slice(0, -10) || "/";
    }} else if (path.endsWith(".html")) {{
      path = `${{path.slice(0, -5)}}/`;
    }} else if (!path.endsWith("/") && !path.split("/").pop().includes(".")) {{
      path = `${{path}}/`;
    }}
    return path || "/";
  }} catch (_error) {{
    return null;
  }}
}}

function isPrivateUrl(rawUrl) {{
  const normalizedPath = normalizeSitePath(rawUrl);
  return normalizedPath ? PRIVATE_URLS.has(normalizedPath) : false;
}}

function resolveSameOriginUrl(rawUrl) {{
  try {{
    const url = new URL(rawUrl, window.location.origin);
    if (url.origin !== window.location.origin) {{
      return null;
    }}
    return url.toString();
  }} catch (_error) {{
    return null;
  }}
}}

async function checkAuthStatus() {{
  try {{
    const response = await fetch("/oauth2/auth", {{
      credentials: "same-origin",
      cache: "no-store",
    }});
    return response.status >= 200 && response.status < 300;
  }} catch (_error) {{
    return false;
  }}
}}

function persistAuthState(authenticated) {{
  authStatus = authenticated ? "authenticated" : "anonymous";
  authStatusCheckedAt = Date.now();
  try {{
    sessionStorage.setItem("docsAuthState", authStatus);
    sessionStorage.setItem("docsAuthStateCheckedAt", String(authStatusCheckedAt));
  }} catch (_error) {{
    // ignore sessionStorage access errors
  }}
}}

function hydrateAuthState() {{
  try {{
    const storedState = sessionStorage.getItem("docsAuthState");
    const storedCheckedAt = Number(sessionStorage.getItem("docsAuthStateCheckedAt") || "0");
    if (!storedState || !storedCheckedAt) {{
      return;
    }}
    if (Date.now() - storedCheckedAt > AUTH_STATUS_TTL_MS) {{
      return;
    }}
    authStatus = storedState;
    authStatusCheckedAt = storedCheckedAt;
  }} catch (_error) {{
    // ignore sessionStorage access errors
  }}
}}

function hasFreshAuthenticatedSession() {{
  return authStatus === "authenticated" && Date.now() - authStatusCheckedAt <= AUTH_STATUS_TTL_MS;
}}

async function refreshAuthState(force = false) {{
  if (!force && hasFreshAuthenticatedSession()) {{
    return true;
  }}
  if (!force && authStatus === "anonymous" && Date.now() - authStatusCheckedAt <= AUTH_STATUS_TTL_MS) {{
    return false;
  }}
  if (authStatusRequest) {{
    return authStatusRequest;
  }}
  authStatusRequest = (async () => {{
    const authenticated = await checkAuthStatus();
    persistAuthState(authenticated);
    return authenticated;
  }})().finally(() => {{
    authStatusRequest = null;
  }});
  return authStatusRequest;
}}

function stopAuthPopupMonitor() {{
  if (authPopupMonitor) {{
    window.clearInterval(authPopupMonitor);
    authPopupMonitor = null;
  }}
}}

function closeAuthPopup() {{
  stopAuthPopupMonitor();
  if (authPopup && !authPopup.closed) {{
    try {{
      authPopup.close();
    }} catch (_error) {{
      // ignore popup close errors
    }}
  }}
  authPopup = null;
}}

function dismissAuthPopupOnBackgroundInteraction() {{
  if (!authPopup || authPopup.closed) {{
    authPopup = null;
    return;
  }}
  closeAuthPopup();
}}

function buildAuthPopupFeatures() {{
  const width = 480;
  const height = 760;
  const left = Math.max(window.screenX + Math.round((window.outerWidth - width) / 2), 0);
  const top = Math.max(window.screenY + Math.round((window.outerHeight - height) / 2), 0);
  return `popup=yes,width=${{width}},height=${{height}},left=${{left}},top=${{top}},resizable=yes,scrollbars=yes`;
}}

function openAuthPopupShell() {{
  closeAuthPopup();
  const popup = window.open("about:blank", "docsAuthPopup", buildAuthPopupFeatures());
  if (!popup) {{
    return null;
  }}
  try {{
    popup.document.title = "打开登录中";
    popup.document.body.style.margin = "0";
    popup.document.body.style.display = "grid";
    popup.document.body.style.placeItems = "center";
    popup.document.body.style.minHeight = "100vh";
    popup.document.body.style.fontFamily = "system-ui, sans-serif";
    popup.document.body.style.color = "#344054";
    popup.document.body.textContent = "正在打开登录...";
  }} catch (_error) {{
    // ignore popup rendering errors
  }}
  return popup;
}}

function buildAuthPopupCallbackUrl(targetUrl, flowId) {{
  const callbackUrl = new URL(AUTH_POPUP_CALLBACK_PATH, window.location.origin);
  callbackUrl.searchParams.set("flow", String(flowId));
  callbackUrl.searchParams.set("target", targetUrl);
  return callbackUrl.toString();
}}

function startAuthPopupMonitor(flowId) {{
  stopAuthPopupMonitor();
  authPopupMonitor = window.setInterval(async () => {{
    if (flowId !== authFlowId) {{
      stopAuthPopupMonitor();
      return;
    }}
    if (!authPopup) {{
      stopAuthPopupMonitor();
      return;
    }}
    if (!authPopup.closed) {{
      return;
    }}
    stopAuthPopupMonitor();
    authPopup = null;
    if (!pendingTargetUrl) {{
      return;
    }}
    const targetUrl = pendingTargetUrl;
    pendingTargetUrl = "";
    const authenticated = await refreshAuthState(true);
    if (authenticated) {{
      window.location.assign(targetUrl);
    }}
  }}, 500);
}}

function handleAuthPopupMessage(event) {{
  if (event.origin !== window.location.origin) {{
    return;
  }}
  const data = event.data;
  if (!data || data.type !== AUTH_POPUP_MESSAGE_TYPE) {{
    return;
  }}
  if (String(data.flowId || "") !== String(authFlowId)) {{
    return;
  }}
  persistAuthState(true);
  const targetUrl = resolveSameOriginUrl(data.targetUrl) || pendingTargetUrl;
  pendingTargetUrl = "";
  closeAuthPopup();
  if (targetUrl) {{
    window.location.assign(targetUrl);
  }}
}}

async function beginPopupAuthFlow(targetUrl) {{
  const safeTargetUrl = resolveSameOriginUrl(targetUrl);
  if (!safeTargetUrl) {{
    return;
  }}
  pendingTargetUrl = safeTargetUrl;
  authFlowId += 1;
  const flowId = authFlowId;
  const popup = openAuthPopupShell();
  const authenticated = await refreshAuthState(true);
  if (authenticated) {{
    pendingTargetUrl = "";
    if (popup && !popup.closed) {{
      popup.close();
    }}
    window.location.assign(safeTargetUrl);
    return;
  }}

  const signInUrl = `/oauth2/sign_in?rd=${{encodeURIComponent(buildAuthPopupCallbackUrl(safeTargetUrl, flowId))}}`;
  if (!popup) {{
    window.location.assign(signInUrl);
    return;
  }}

  authPopup = popup;
  startAuthPopupMonitor(flowId);
  try {{
    popup.location.replace(signInUrl);
    popup.focus();
  }} catch (_error) {{
    closeAuthPopup();
    window.location.assign(signInUrl);
  }}
}}

function annotatePrivateLinks(root = document) {{
  root.querySelectorAll("a[href]").forEach((anchor) => {{
    if (anchor.dataset.docsPrivateAnnotated === "true") {{
      return;
    }}
    const href = anchor.getAttribute("href") || anchor.href;
    if (!isPrivateUrl(href)) {{
      return;
    }}
    anchor.dataset.docsPrivateAnnotated = "true";
  }});
}}

function shouldInterceptClick(event, anchor) {{
  if (event.defaultPrevented || event.button !== 0) {{
    return false;
  }}
  if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) {{
    return false;
  }}
  if (anchor.hasAttribute("download")) {{
    return false;
  }}
  const target = anchor.getAttribute("target");
  if (target && target !== "_self") {{
    return false;
  }}
  if (isPrivateUrl(anchor.href) && hasFreshAuthenticatedSession()) {{
    return false;
  }}
  return isPrivateUrl(anchor.href);
}}

async function handlePrivateLinkClick(event, anchor) {{
  event.preventDefault();
  const authenticated = await refreshAuthState();
  if (authenticated) {{
    window.location.assign(anchor.href);
    return;
  }}
  beginPopupAuthFlow(anchor.href);
}}

document$.subscribe(() => {{
  hydrateAuthState();
  annotatePrivateLinks();
  refreshAuthState();

  if (window.__docsAccessControlHandlersBound) {{
    return;
  }}
  window.__docsAccessControlHandlersBound = true;

  document.addEventListener("click", (event) => {{
    if (!(event.target instanceof Element)) {{
      return;
    }}
    const anchor = event.target.closest("a[href]");
    if (!(anchor instanceof HTMLAnchorElement)) {{
      return;
    }}
    if (!shouldInterceptClick(event, anchor)) {{
      return;
    }}
    handlePrivateLinkClick(event, anchor);
  }});
  document.addEventListener("pointerdown", dismissAuthPopupOnBackgroundInteraction, true);
  window.addEventListener("focus", dismissAuthPopupOnBackgroundInteraction);
  window.addEventListener("message", handleAuthPopupMessage);
}});
""",
        encoding="utf-8",
    )


def write_auth_popup_complete_html(site_docs_dir: Path) -> None:
    popup_path = site_docs_dir / "assets" / "auth" / "popup-complete.html"
    popup_path.parent.mkdir(parents=True, exist_ok=True)
    popup_path.write_text(
        """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>登录完成</title>
  <script>
    (() => {
      const AUTH_POPUP_MESSAGE_TYPE = "docs-auth-popup-complete";

      function resolveSameOriginTarget(rawTarget) {
        try {
          const url = new URL(rawTarget || "/", window.location.origin);
          if (url.origin !== window.location.origin) {
            return new URL("/", window.location.origin).toString();
          }
          return url.toString();
        } catch (_error) {
          return new URL("/", window.location.origin).toString();
        }
      }

      const params = new URLSearchParams(window.location.search);
      const payload = {
        type: AUTH_POPUP_MESSAGE_TYPE,
        flowId: params.get("flow") || "",
        targetUrl: resolveSameOriginTarget(params.get("target")),
      };

      try {
        if (window.opener && !window.opener.closed) {
          window.opener.postMessage(payload, window.location.origin);
          window.close();
          setTimeout(() => {
            window.location.replace(payload.targetUrl);
          }, 250);
          return;
        }
      } catch (_error) {
        // ignore opener access errors
      }

      window.location.replace(payload.targetUrl);
    })();
  </script>
</head>
<body>
  登录完成，正在返回文档...
</body>
</html>
""",
        encoding="utf-8",
    )


def write_permissions(output_dir: Path, pages: list[dict]) -> None:
    authz_dir = output_dir / "authz"
    authz_dir.mkdir(parents=True, exist_ok=True)
    payload = {"pages": sorted(pages, key=lambda item: (item["url"], item["kind"]))}
    (authz_dir / "permissions.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def write_nginx_private_locations(output_dir: Path, pages: list[dict]) -> None:
    nginx_dir = output_dir / "nginx"
    nginx_dir.mkdir(parents=True, exist_ok=True)
    private_urls = sorted({item["url"] for item in pages if item["access"] == "private"})
    lines: list[str] = [
        "# generated by docs-stratego",
        "# only private URLs belong here; do not add auth_request to site root or location /",
        "",
    ]
    for url in private_urls:
        lines.extend(
            [
                f"location = {url} {{",
                "  auth_request /oauth2/auth;",
                "  error_page 401 = /oauth2/sign_in;",
                "  auth_request_set $user $upstream_http_x_auth_request_user;",
                "  auth_request_set $email $upstream_http_x_auth_request_email;",
                "}",
                "",
            ]
        )
    (nginx_dir / "private_locations.conf").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_mkdocs_config(output_dir: Path, nav_items: list[dict]) -> None:
    lines = [
        "site_name: 章略·墨衡",
        "site_description: 单站文档与页面级权限入口",
        "docs_dir: site_docs",
        "use_directory_urls: true",
        "theme:",
        "  name: material",
        "  language: zh",
        "  icon:",
        "    repo: fontawesome/brands/github",
        "  palette:",
        '    - media: "(prefers-color-scheme: light)"',
        "      scheme: default",
        "      primary: indigo",
        "      accent: teal",
        "      toggle:",
        "        icon: material/weather-night",
        "        name: 切换到深色模式",
        '    - media: "(prefers-color-scheme: dark)"',
        "      scheme: slate",
        "      primary: black",
        "      accent: amber",
        "      toggle:",
        "        icon: material/weather-sunny",
        "        name: 切换到浅色模式",
        "  features:",
        "    - navigation.instant",
        "    - navigation.tabs",
        "    - navigation.top",
        "    - content.code.copy",
        "extra_css:",
        "  - assets/stylesheets/home.css",
        "extra_javascript:",
        "  - assets/javascripts/navigation.js",
        "  - assets/javascripts/contracts.js",
        "  - assets/javascripts/access-control.js",
        "plugins: []",
        "nav:",
        '  - "首页": index.md',
    ]
    append_nav_lines(lines, nav_items, 2)
    lines.extend(
        [
            "markdown_extensions:",
            "  - admonition",
            "  - attr_list",
            "  - tables",
            "  - pymdownx.superfences",
            "",
        ]
    )
    (output_dir / "mkdocs.generated.yml").write_text("\n".join(lines), encoding="utf-8")


def materialize_repo_docs(site_docs_dir: Path, repo: SourceRepository, docs_root: Path) -> Path:
    target_dir = site_docs_dir / repo.name
    if target_dir.is_symlink():
        target_dir.unlink()
    elif target_dir.exists():
        shutil.rmtree(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    for directory in sorted(path for path in docs_root.rglob("*") if path.is_dir()):
        relative_path = directory.relative_to(docs_root)
        if is_hidden_path(relative_path):
            continue
        (target_dir / relative_path).mkdir(parents=True, exist_ok=True)

    for file_path in sorted(path for path in docs_root.rglob("*") if path.is_file()):
        relative_path = file_path.relative_to(docs_root)
        if is_hidden_path(relative_path):
            continue
        destination = target_dir / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.symlink_to(file_path.resolve())

    return target_dir


def write_generated_contract_pages(repo_dir: Path, docs_root: Path, pages: list[PageLink]) -> None:
    for page in pages:
        if page.render_kind == "markdown":
            continue
        source_file = docs_root / page.source_path
        output_file = repo_dir / page.path
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(render_contract_page(page, source_file), encoding="utf-8")


def build_site(repositories: list[SourceRepository], output_dir: Path, project_root: Path | None = None) -> Path:
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    site_docs_dir = output_dir / "site_docs"
    site_docs_dir.mkdir(parents=True, exist_ok=True)
    write_home_css(site_docs_dir)

    entries: list[dict] = []
    top_level_nav: list[dict] = []
    repo_pages: dict[str, list[PageLink]] = {}
    repo_tab_links: dict[str, list[RepoTabLink]] = {}

    for repo in repositories:
        docs_root = repo.resolve_docs_root(project_root)
        if not docs_root.exists():
            raise ValueError(f"{repo.name} docs root does not exist: {docs_root}")
        repo_dir = materialize_repo_docs(site_docs_dir, repo, docs_root)
        repo_nav, repo_entries, root_metadata = build_repo_nav_and_entries(repo, docs_root)
        top_level_nav.append({repo.title: repo_nav})
        entries.extend(repo_entries)
        repo_pages[repo.name] = flatten_page_links(root_metadata.nav)
        write_generated_contract_pages(repo_dir, docs_root, repo_pages[repo.name])
        repo_tab_links[repo.title] = build_repo_tab_links(repo, root_metadata.nav)

    write_root_index(site_docs_dir, repositories, repo_pages)
    write_navigation_js(site_docs_dir, repo_tab_links)
    write_contracts_js(site_docs_dir)
    write_access_control_js(site_docs_dir, entries)
    write_auth_popup_complete_html(site_docs_dir)
    write_permissions(output_dir, entries)
    write_nginx_private_locations(output_dir, entries)
    write_mkdocs_config(output_dir, top_level_nav)
    return output_dir
