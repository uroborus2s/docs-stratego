from __future__ import annotations

import json
import subprocess
from pathlib import Path

from models import SourceRepository
from source_config import load_source_repositories
from source_sync import sync_sources


def run_command(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True)


def load_remote_submodule_repositories(config_path: Path) -> list[SourceRepository]:
    repositories = load_source_repositories(config_path, source_mode="remote")
    return [repo for repo in repositories if repo.source_type == "submodule_sparse" and repo.submodule_path]


def detect_base_branch(project_root: Path) -> str:
    try:
        ref = run_command(
            ["git", "symbolic-ref", "--quiet", "--short", "refs/remotes/origin/HEAD"],
            cwd=project_root,
        ).stdout.strip()
    except subprocess.CalledProcessError:
        remote_branches = run_command(["git", "branch", "-r"], cwd=project_root).stdout
        if "origin/main" in remote_branches:
            return "main"
        if "origin/master" in remote_branches:
            return "master"
        return "main"

    if ref.startswith("origin/"):
        return ref.split("/", 1)[1]
    return "main"


def prepare_bot_branch(project_root: Path, branch: str, base_branch: str) -> None:
    run_command(["git", "fetch", "origin", base_branch], cwd=project_root)
    run_command(["git", "checkout", "-B", branch, f"origin/{base_branch}"], cwd=project_root)


def get_changed_submodule_paths(project_root: Path) -> list[str]:
    result = run_command(
        ["git", "status", "--porcelain", "--untracked-files=no", "--", "sources"],
        cwd=project_root,
    )
    paths: list[str] = []
    for line in result.stdout.splitlines():
        if len(line) < 4:
            continue
        path = line[3:].strip()
        if path.startswith("sources/"):
            paths.append(path)
    return paths


def build_pr_body(updated_repositories: list[str]) -> str:
    lines = [
        "Automated sync of source repository submodule pointers.",
        "",
        "Updated repositories:",
    ]
    lines.extend(f"- {name}" for name in updated_repositories)
    lines.extend(
        [
            "",
            "Review checklist:",
            "- Diff only changes `sources/*` gitlinks.",
            "- Checks pass.",
            "- Updates align with the configured source branches.",
        ]
    )
    return "\n".join(lines)


def create_or_update_shared_pr(
    project_root: Path,
    branch: str,
    base_branch: str,
    updated_repositories: list[str],
    title: str,
) -> None:
    result = run_command(
        [
            "gh",
            "pr",
            "list",
            "--base",
            base_branch,
            "--head",
            branch,
            "--state",
            "open",
            "--json",
            "number",
        ],
        cwd=project_root,
    )
    prs = json.loads(result.stdout)
    body = build_pr_body(updated_repositories)

    if prs:
        run_command(
            ["gh", "pr", "edit", str(prs[0]["number"]), "--title", title, "--body", body],
            cwd=project_root,
        )
        return

    run_command(
        ["gh", "pr", "create", "--title", title, "--body", body, "--base", base_branch, "--head", branch],
        cwd=project_root,
    )


def sync_source_pointers(
    project_root: Path,
    config_path: Path,
    branch: str = "bot/sync-source-pointers",
    title: str = "chore: sync source repository pointers",
) -> list[str]:
    repositories = load_remote_submodule_repositories(config_path)
    base_branch = detect_base_branch(project_root)
    prepare_bot_branch(project_root, branch, base_branch)

    sync_sources(config_path, project_root, source_mode="remote")

    changed_paths = get_changed_submodule_paths(project_root)
    if not changed_paths:
        return []

    path_to_name = {repo.submodule_path: repo.name for repo in repositories if repo.submodule_path}
    updated_repositories = [path_to_name[path] for path in changed_paths if path in path_to_name]

    run_command(["git", "add", "--", *changed_paths], cwd=project_root)
    run_command(["git", "commit", "-m", title], cwd=project_root)
    run_command(["git", "push", "origin", branch, "--force-with-lease"], cwd=project_root)
    create_or_update_shared_pr(project_root, branch, base_branch, updated_repositories, title)
    return updated_repositories
