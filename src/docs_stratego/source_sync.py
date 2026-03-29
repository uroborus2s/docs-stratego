from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


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


def resolve_source_mode(payload: dict, source_mode: str | None = None) -> str:
    resolved_mode = source_mode or payload.get("default_source_mode", "local")
    if resolved_mode not in {"local", "remote"}:
        raise ValueError(f"unsupported source mode: {resolved_mode}")
    return resolved_mode


def normalize_repository_config(item: dict, source_mode: str) -> dict:
    if "modes" not in item:
        raise ValueError(f'{item["name"]} missing modes configuration')

    mode_payload = item["modes"].get(source_mode)
    if not mode_payload:
        raise ValueError(f'{item["name"]} missing source mode: {source_mode}')

    normalized = {key: value for key, value in item.items() if key != "modes"}
    normalized.update(mode_payload)
    return normalized


def load_source_repositories(config_path: Path, source_mode: str | None = None) -> list[SourceRepository]:
    payload = json.loads(config_path.read_text(encoding="utf-8"))
    resolved_mode = resolve_source_mode(payload, source_mode)
    repositories: list[SourceRepository] = []
    for item in payload.get("repositories", []):
        normalized_item = normalize_repository_config(item, resolved_mode)
        repositories.append(
            SourceRepository(
                name=normalized_item["name"],
                title=normalized_item["title"],
                source_type=normalized_item["source_type"],
                repo_url=normalized_item.get("repo_url"),
                git_url=normalized_item.get("git_url"),
                branch=normalized_item.get("branch", "main"),
                docs_path=normalized_item.get("docs_path", "docs"),
                local_path=normalized_item.get("local_path"),
                submodule_path=normalized_item.get("submodule_path"),
            )
        )
    return repositories


def top_level_sparse_patterns(docs_path: str) -> list[str]:
    normalized = docs_path.strip("/")
    return [f"/{normalized}/", f"/{normalized}/**"]


def ensure_registered_submodule(repo: SourceRepository, project_root: Path) -> None:
    if not repo.submodule_path:
        raise ValueError(f"{repo.name} missing submodule_path")

    result = subprocess.run(
        ["git", "ls-files", "--stage", "--", repo.submodule_path],
        cwd=project_root,
        check=True,
        capture_output=True,
        text=True,
    )
    if not result.stdout.startswith("160000 "):
        raise ValueError(
            f"{repo.name} submodule_path {repo.submodule_path} is not registered as a git submodule in the repository index"
        )


def sync_submodule_sparse_repository(repo: SourceRepository, project_root: Path) -> None:
    if not repo.submodule_path:
        raise ValueError(f"{repo.name} missing submodule_path")

    ensure_registered_submodule(repo, project_root)
    repo_root = (project_root / repo.submodule_path).resolve()
    if repo_root.exists() and not (repo_root / ".git").exists():
        shutil.rmtree(repo_root)

    subprocess.run(
        ["git", "submodule", "sync", "--", repo.submodule_path],
        cwd=project_root,
        check=True,
    )
    subprocess.run(
        ["git", "submodule", "update", "--init", "--depth", "1", "--", repo.submodule_path],
        cwd=project_root,
        check=True,
    )
    subprocess.run(
        ["git", "-C", str(repo_root), "fetch", "origin", repo.branch, "--depth", "1"],
        check=True,
    )
    subprocess.run(
        ["git", "-C", str(repo_root), "checkout", "-B", repo.branch, "FETCH_HEAD"],
        check=True,
    )
    subprocess.run(
        ["git", "-C", str(repo_root), "sparse-checkout", "init", "--no-cone"],
        check=True,
    )
    subprocess.run(
        ["git", "-C", str(repo_root), "sparse-checkout", "set", "--no-cone", *top_level_sparse_patterns(repo.docs_path)],
        check=True,
    )


def sync_git_sparse_repository(repo: SourceRepository, sources_dir: Path) -> None:
    repo_root = sources_dir / repo.name
    if not repo.git_url:
        raise ValueError(f"{repo.name} missing git_url")

    if repo_root.exists() and not (repo_root / ".git").exists():
        shutil.rmtree(repo_root)

    if not repo_root.exists():
        subprocess.run(
            [
                "git",
                "clone",
                "--filter=blob:none",
                "--no-checkout",
                "--depth",
                "1",
                "--branch",
                repo.branch,
                repo.git_url,
                str(repo_root),
            ],
            check=True,
        )
        subprocess.run(
            ["git", "-C", str(repo_root), "sparse-checkout", "init", "--no-cone"],
            check=True,
        )
        subprocess.run(
            ["git", "-C", str(repo_root), "sparse-checkout", "set", "--no-cone", *top_level_sparse_patterns(repo.docs_path)],
            check=True,
        )
        subprocess.run(["git", "-C", str(repo_root), "checkout", "-B", repo.branch, "FETCH_HEAD"], check=True)
        return

    subprocess.run(
        ["git", "-C", str(repo_root), "fetch", "origin", repo.branch, "--depth", "1"],
        check=True,
    )
    subprocess.run(
        ["git", "-C", str(repo_root), "sparse-checkout", "set", "--no-cone", *top_level_sparse_patterns(repo.docs_path)],
        check=True,
    )
    subprocess.run(["git", "-C", str(repo_root), "checkout", "-B", repo.branch, "FETCH_HEAD"], check=True)


def sync_sources(config_path: Path, project_root: Path, source_mode: str | None = None) -> list[SourceRepository]:
    repositories = load_source_repositories(config_path, source_mode=source_mode)
    sources_dir = project_root / "sources"
    sources_dir.mkdir(parents=True, exist_ok=True)

    for repo in repositories:
        if repo.source_type == "submodule_sparse":
            sync_submodule_sparse_repository(repo, project_root)
        elif repo.source_type == "git_sparse":
            sync_git_sparse_repository(repo, sources_dir)

    return repositories
