from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from pathlib import Path

from docs_stratego.site_builder import (
    flatten_page_links,
    parse_root_index,
    validate_declared_pages,
    validate_directory_indexes,
    validate_markdown_coverage,
)


NOTIFY_WORKFLOW_RELATIVE_PATH = Path(".github/workflows/notify-docs-stratego.yml")
PROTECTED_SOURCE_NAMES = {"docs-stratego"}


@dataclass(frozen=True)
class SourceRegistration:
    name: str
    title: str
    repo_url: str
    git_url: str
    local_path: str
    branch: str = "main"
    docs_path: str = "docs"
    submodule_path: str | None = None

    def resolved_submodule_path(self) -> str:
        return self.submodule_path or f"sources/{self.name}"


@dataclass(frozen=True)
class ValidationReport:
    repo_root: Path
    docs_root: Path
    title: str
    home_access: str
    page_count: int
    contract_count: int


def load_source_config(config_path: Path) -> dict:
    return json.loads(config_path.read_text(encoding="utf-8"))


def write_source_config(config_path: Path, payload: dict, dry_run: bool = False) -> None:
    if dry_run:
        return
    config_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def build_source_entry(spec: SourceRegistration) -> dict:
    return {
        "name": spec.name,
        "title": spec.title,
        "repo_url": spec.repo_url,
        "modes": {
            "local": {
                "source_type": "local",
                "local_path": spec.local_path,
            },
            "remote": {
                "source_type": "submodule_sparse",
                "git_url": spec.git_url,
                "branch": spec.branch,
                "submodule_path": spec.resolved_submodule_path(),
                "docs_path": spec.docs_path,
            },
        },
    }


def add_source_repository(
    config_path: Path,
    spec: SourceRegistration,
    dry_run: bool = False,
) -> dict:
    payload = load_source_config(config_path)
    repositories = payload.setdefault("repositories", [])
    if any(item.get("name") == spec.name for item in repositories):
        raise ValueError(f"{spec.name} already exists in {config_path}")

    entry = build_source_entry(spec)
    repositories.append(entry)
    write_source_config(config_path, payload, dry_run=dry_run)
    return entry


def remove_source_repository(
    config_path: Path,
    name: str,
    dry_run: bool = False,
) -> dict:
    if name in PROTECTED_SOURCE_NAMES:
        raise ValueError(f"{name} cannot be removed")

    payload = load_source_config(config_path)
    repositories = payload.get("repositories", [])
    remaining = [item for item in repositories if item.get("name") != name]
    if len(remaining) == len(repositories):
        raise ValueError(f"{name} not found in {config_path}")

    removed = next(item for item in repositories if item.get("name") == name)
    payload["repositories"] = remaining
    write_source_config(config_path, payload, dry_run=dry_run)
    return removed


def run_git_command(cmd: list[str], cwd: Path) -> None:
    subprocess.run(cmd, cwd=cwd, check=True)


def register_submodule(project_root: Path, spec: SourceRegistration, dry_run: bool = False) -> list[list[str]]:
    command = [
        "git",
        "submodule",
        "add",
        "-b",
        spec.branch,
        "--name",
        spec.name,
        spec.git_url,
        spec.resolved_submodule_path(),
    ]
    if not dry_run:
        run_git_command(command, cwd=project_root)
    return [command]


def remove_submodule(project_root: Path, submodule_path: str, dry_run: bool = False) -> list[list[str]]:
    commands = [
        ["git", "submodule", "deinit", "-f", "--", submodule_path],
        ["git", "rm", "-f", "--", submodule_path],
    ]
    if not dry_run:
        for command in commands:
            run_git_command(command, cwd=project_root)
    return commands


def render_notify_workflow(
    repository_full_name: str,
    branches: list[str],
    event_type: str = "source-pointer-sync-requested",
) -> str:
    branch_lines = "\n".join(f"      - {branch}" for branch in branches)
    return (
        "name: Notify Docs Stratego\n\n"
        "on:\n"
        "  push:\n"
        "    branches:\n"
        f"{branch_lines}\n"
        "    paths:\n"
        "      - 'docs/**'\n"
        "  workflow_dispatch:\n\n"
        "jobs:\n"
        "  notify:\n"
        "    runs-on: ubuntu-latest\n"
        "    steps:\n"
        "      - name: Send Repository Dispatch to docs-stratego\n"
        "        run: |\n"
        "          curl -L \\\n"
        "            -X POST \\\n"
        '            -H "Accept: application/vnd.github+json" \\\n'
        '            -H "Authorization: Bearer ${{ secrets.DOCS_STRATEGO_DISPATCH_TOKEN }}" \\\n'
        '            -H "X-GitHub-Api-Version: 2022-11-28" \\\n'
        f"            https://api.github.com/repos/{repository_full_name}/dispatches \\\n"
        f"            -d '{{\"event_type\":\"{event_type}\",\"client_payload\":{{\"repository\":\"${{{{ github.repository }}}}\",\"branch\":\"${{{{ github.ref_name }}}}\",\"sha\":\"${{{{ github.sha }}}}\"}}}}'\n"
    )


def scaffold_notify_workflow(
    repo_root: Path,
    repository_full_name: str,
    branches: list[str],
    dry_run: bool = False,
) -> Path:
    workflow_path = repo_root / NOTIFY_WORKFLOW_RELATIVE_PATH
    workflow_text = render_notify_workflow(repository_full_name, branches)
    if not dry_run:
        workflow_path.parent.mkdir(parents=True, exist_ok=True)
        workflow_path.write_text(workflow_text, encoding="utf-8")
    return workflow_path


def remove_notify_workflow(repo_root: Path, dry_run: bool = False) -> Path:
    workflow_path = repo_root / NOTIFY_WORKFLOW_RELATIVE_PATH
    if workflow_path.exists() and not dry_run:
        workflow_path.unlink()
    return workflow_path


def validate_source_repository(
    repo_root: Path,
    docs_dir: str = "docs",
) -> ValidationReport:
    docs_root = (repo_root / docs_dir).resolve()
    if not docs_root.exists():
        raise ValueError(f"{docs_root} does not exist")

    root_metadata = parse_root_index(docs_root)
    declared_pages = flatten_page_links(root_metadata.nav)
    validate_directory_indexes(docs_root, declared_pages)
    validate_declared_pages(docs_root, declared_pages)
    validate_markdown_coverage(docs_root, declared_pages)

    contract_count = sum(1 for page in declared_pages if page.render_kind != "markdown")
    return ValidationReport(
        repo_root=repo_root.resolve(),
        docs_root=docs_root,
        title=root_metadata.title,
        home_access=root_metadata.home_access,
        page_count=len(declared_pages),
        contract_count=contract_count,
    )
