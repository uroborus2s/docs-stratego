from __future__ import annotations

import json
from pathlib import Path

from models import SourceRegistration, SourceRepository


def resolve_config_path(project_root: Path, config_path: str | Path) -> Path:
    candidate = Path(config_path)
    if candidate.is_absolute():
        return candidate
    return (project_root / candidate).resolve()


def load_source_config(config_path: Path) -> dict:
    return json.loads(config_path.read_text(encoding="utf-8"))


def write_source_config(config_path: Path, payload: dict, dry_run: bool = False) -> None:
    if dry_run:
        return
    config_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


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
    payload = load_source_config(config_path)
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
