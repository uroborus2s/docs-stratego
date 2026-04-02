from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from docs_stratego.site_builder import SourceRepository, build_site
from docs_stratego.source_admin import (
    ValidationReport,
    add_source_repository,
    register_submodule,
    remove_notify_workflow,
    remove_source_repository,
    remove_submodule,
    scaffold_notify_workflow,
    validate_source_repository,
)
from docs_stratego.source_sync import load_source_repositories, sync_sources


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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="docs-stratego", description="Docs Stratego project CLI.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    sync_parser = subparsers.add_parser("sync", help="Sync source repositories.")
    sync_parser.add_argument("--config", default="config/source-repos.json")
    sync_parser.add_argument("--project-root", default=".")
    sync_parser.add_argument("--source-mode", choices=["local", "remote"], default=None)
    sync_parser.set_defaults(handler=handle_sync)

    build_parser_cmd = subparsers.add_parser("build", help="Build generated site inputs.")
    build_parser_cmd.add_argument("--config", default="config/source-repos.json")
    build_parser_cmd.add_argument("--project-root", default=".")
    build_parser_cmd.add_argument("--output-dir", default=".generated")
    build_parser_cmd.add_argument("--source-mode", choices=["local", "remote"], default=None)
    build_parser_cmd.set_defaults(handler=handle_build)

    source_parser = subparsers.add_parser("source", help="Manage source repository onboarding.")
    source_subparsers = source_parser.add_subparsers(dest="source_command", required=True)

    validate_parser = source_subparsers.add_parser("validate", help="Validate a source repository docs tree.")
    validate_parser.add_argument("--repo-path", default=".")
    validate_parser.add_argument("--docs-dir", default="docs")
    validate_parser.set_defaults(handler=handle_source_validate)

    scaffold_parser = source_subparsers.add_parser(
        "scaffold-notify",
        help="Create or remove the source-repo notify workflow.",
    )
    scaffold_parser.add_argument("--repo-path", default=".")
    scaffold_parser.add_argument("--root-repository", default="uroborus2s/docs-stratego")
    scaffold_parser.add_argument("--branch", action="append", dest="branches")
    scaffold_parser.add_argument("--remove", action="store_true")
    scaffold_parser.add_argument("--dry-run", action="store_true")
    scaffold_parser.set_defaults(handler=handle_source_scaffold_notify)

    add_parser = source_subparsers.add_parser("add", help="Register a new source repository.")
    add_parser.add_argument("--project-root", default=".")
    add_parser.add_argument("--config", default="config/source-repos.json")
    add_parser.add_argument("--name", required=True)
    add_parser.add_argument("--title", required=True)
    add_parser.add_argument("--repo-url", required=True)
    add_parser.add_argument("--git-url", required=True)
    add_parser.add_argument("--local-path", required=True)
    add_parser.add_argument("--branch", default="main")
    add_parser.add_argument("--docs-path", default="docs")
    add_parser.add_argument("--submodule-path")
    add_parser.add_argument("--register-submodule", action="store_true")
    add_parser.add_argument("--dry-run", action="store_true")
    add_parser.set_defaults(handler=handle_source_add)

    remove_parser = source_subparsers.add_parser("remove", help="Remove a source repository.")
    remove_parser.add_argument("--project-root", default=".")
    remove_parser.add_argument("--config", default="config/source-repos.json")
    remove_parser.add_argument("--name", required=True)
    remove_parser.add_argument("--remove-submodule", action="store_true")
    remove_parser.add_argument("--dry-run", action="store_true")
    remove_parser.add_argument("--yes", action="store_true")
    remove_parser.set_defaults(handler=handle_source_remove)

    return parser


def handle_sync(args: argparse.Namespace) -> None:
    sync_sources(
        Path(args.config),
        Path(args.project_root).resolve(),
        source_mode=args.source_mode,
    )


def handle_build(args: argparse.Namespace) -> None:
    project_root = Path(args.project_root).resolve()
    repositories = [
        to_builder_repo(repo) for repo in load_source_repositories(Path(args.config), source_mode=args.source_mode)
    ]
    build_site(repositories, project_root / args.output_dir, project_root)


def handle_source_validate(args: argparse.Namespace) -> None:
    report = validate_source_repository(Path(args.repo_path).resolve(), docs_dir=args.docs_dir)
    print_validation_report(report)


def print_validation_report(report: ValidationReport) -> None:
    print(
        f"{report.title}: home_access={report.home_access} "
        f"pages={report.page_count} contracts={report.contract_count} docs_root={report.docs_root}"
    )


def handle_source_scaffold_notify(args: argparse.Namespace) -> None:
    repo_root = Path(args.repo_path).resolve()
    if args.remove:
        path = remove_notify_workflow(repo_root, dry_run=args.dry_run)
        print(f"removed notify workflow: {path}")
        return

    branches = args.branches or ["main"]
    path = scaffold_notify_workflow(
        repo_root=repo_root,
        repository_full_name=args.root_repository,
        branches=branches,
        dry_run=args.dry_run,
    )
    print(f"scaffolded notify workflow: {path}")


def handle_source_add(args: argparse.Namespace) -> None:
    from docs_stratego.source_admin import SourceRegistration

    project_root = Path(args.project_root).resolve()
    config_path = project_root / args.config
    spec = SourceRegistration(
        name=args.name,
        title=args.title,
        repo_url=args.repo_url,
        git_url=args.git_url,
        local_path=args.local_path,
        branch=args.branch,
        docs_path=args.docs_path,
        submodule_path=args.submodule_path,
    )
    entry = add_source_repository(config_path, spec, dry_run=args.dry_run)
    if args.register_submodule:
        register_submodule(project_root, spec, dry_run=args.dry_run)
    print(f"registered source: {entry['name']}")


def handle_source_remove(args: argparse.Namespace) -> None:
    if not args.yes:
        raise SystemExit(2)

    project_root = Path(args.project_root).resolve()
    config_path = project_root / args.config
    removed = remove_source_repository(config_path, args.name, dry_run=args.dry_run)
    if args.remove_submodule:
        submodule_path = removed["modes"]["remote"].get("submodule_path")
        if submodule_path:
            remove_submodule(project_root, submodule_path, dry_run=args.dry_run)
    print(f"removed source: {removed['name']}")


def main(argv: Sequence[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    args.handler(args)


if __name__ == "__main__":
    main()
