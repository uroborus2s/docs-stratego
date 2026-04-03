from __future__ import annotations

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

    def resolve_docs_root(self, project_root: Path | None = None) -> Path:
        base = project_root or Path.cwd()
        if self.source_type == "local":
            if not self.local_path:
                raise ValueError(f"{self.name} missing local_path")
            return (base / self.local_path).resolve()
        if self.source_type == "submodule_sparse":
            if not self.submodule_path:
                raise ValueError(f"{self.name} missing submodule_path")
            return (base / self.submodule_path / self.docs_path).resolve()
        if self.source_type == "git_sparse":
            return (base / "sources" / self.name / self.docs_path).resolve()
        raise ValueError(f"unsupported source_type: {self.source_type}")


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
