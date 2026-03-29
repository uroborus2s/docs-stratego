from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from docs_stratego.site_builder import SourceRepository, build_site
from docs_stratego.source_sync import load_source_repositories


def to_builder_repo(repo) -> SourceRepository:
    return SourceRepository(
        name=repo.name,
        title=repo.title,
        source_type=repo.source_type,
        repo_url=repo.repo_url,
        git_url=repo.git_url,
        branch=repo.branch,
        docs_path=repo.docs_path,
        local_path=repo.local_path,
        submodule_path=repo.submodule_path,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Build single-site docs workspace and auth manifests.")
    parser.add_argument("--config", default="config/source-repos.json")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--output-dir", default=".generated")
    parser.add_argument("--source-mode", choices=["local", "remote"], default=None)
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    repositories = [
        to_builder_repo(repo) for repo in load_source_repositories(Path(args.config), source_mode=args.source_mode)
    ]
    build_site(repositories, project_root / args.output_dir, project_root)


if __name__ == "__main__":
    main()
