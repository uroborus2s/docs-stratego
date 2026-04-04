from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class DeployStackTests(unittest.TestCase):
    def test_compose_contains_auth_services_and_external_network(self) -> None:
        compose_text = (PROJECT_ROOT / "deploy" / "docker-compose.yml").read_text(encoding="utf-8")

        self.assertIn("casdoor:", compose_text)
        self.assertIn("oauth2-proxy:", compose_text)
        self.assertNotIn("\n  nginx:\n", compose_text)
        self.assertIn("127.0.0.1:4180:4180", compose_text)
        self.assertIn("external: true", compose_text)
        self.assertIn("DOCS_REDIS_DOCKER_NETWORK", compose_text)
        self.assertIn("docs_internal", compose_text)

    def test_host_nginx_templates_are_not_versioned(self) -> None:
        self.assertFalse((PROJECT_ROOT / "deploy" / "nginx").exists())
        self.assertFalse((PROJECT_ROOT / "scripts" / "render_host_nginx_conf.sh").exists())

    def test_runtime_auth_configs_exist(self) -> None:
        self.assertTrue((PROJECT_ROOT / "deploy" / "casdoor" / "app.conf").exists())
        self.assertTrue((PROJECT_ROOT / "deploy" / "oauth2-proxy" / "oauth2-proxy.cfg").exists())
        self.assertFalse((PROJECT_ROOT / "deploy" / "nginx").exists())

    def test_remote_submodule_sources_are_registered_in_git(self) -> None:
        config = json.loads((PROJECT_ROOT / "config" / "source-repos.json").read_text(encoding="utf-8"))
        gitmodules_text = (PROJECT_ROOT / ".gitmodules").read_text(encoding="utf-8")

        for repo in config["repositories"]:
            remote = repo["modes"]["remote"]
            if remote["source_type"] != "submodule_sparse":
                continue
            submodule_path = remote["submodule_path"]
            self.assertIn(f"path = {submodule_path}", gitmodules_text)

            result = subprocess.run(
                ["git", "ls-files", "--stage", "--", submodule_path],
                cwd=PROJECT_ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertRegex(result.stdout, rf"^160000 [0-9a-f]{{40}} 0\t{submodule_path}\n?$")

    def test_deploy_scripts_and_workflow_cover_host_nginx_sync(self) -> None:
        workflow_text = (PROJECT_ROOT / ".github" / "workflows" / "deploy-docs.yml").read_text(encoding="utf-8")
        deploy_script_text = (PROJECT_ROOT / "scripts" / "deploy_remote.sh").read_text(encoding="utf-8")
        cli_text = (PROJECT_ROOT / "src" / "cli.py").read_text(encoding="utf-8")
        pyproject_text = (PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8")

        self.assertIn("validate:", workflow_text)
        self.assertIn("needs: validate", workflow_text)
        self.assertIn("actions/checkout@v4", workflow_text)
        self.assertIn("actions/setup-python@v5", workflow_text)
        self.assertIn("astral-sh/setup-uv@v7", workflow_text)
        self.assertIn("uv sync --frozen --extra site", workflow_text)
        self.assertIn('-d "$GITHUB_WORKSPACE/site"', workflow_text)
        self.assertIn("if-no-files-found: error", workflow_text)
        self.assertIn("--source-mode remote", workflow_text)
        self.assertIn("/var/www/docs-stratego", workflow_text)
        self.assertIn("/etc/nginx/snippets/docs-stratego/private_locations.conf", workflow_text)
        self.assertIn("DOCS_PRIVATE_LOCATIONS_PATH", workflow_text)
        self.assertIn("RELOAD_HOST_NGINX", workflow_text)
        self.assertIn("sudo nginx -t", workflow_text)
        self.assertIn("sudo systemctl reload nginx", workflow_text)
        self.assertNotIn('${EUID}', workflow_text)
        self.assertNotIn("render_host_nginx_conf.sh", workflow_text)
        self.assertNotIn("render_host_nginx_conf.sh", deploy_script_text)
        self.assertIn('DOCS_SOURCE_MODE="${DOCS_SOURCE_MODE:-remote}"', deploy_script_text)
        self.assertIn('--source-mode "$DOCS_SOURCE_MODE"', deploy_script_text)
        self.assertIn("systemctl reload nginx", deploy_script_text)
        self.assertFalse((PROJECT_ROOT / "start.sh").exists())
        self.assertIn('subparsers.add_parser("dev"', cli_text)
        self.assertIn('dev_parser.add_argument("--source-mode"', cli_text)
        self.assertIn('dev_parser.add_argument("--build-only"', cli_text)
        self.assertIn('run_mkdocs_command(["serve"', cli_text)
        self.assertNotIn("repository_dispatch", workflow_text)
        self.assertIn('docs-stratego = "cli:main"', pyproject_text)
        self.assertIn("[project.optional-dependencies]", pyproject_text)
        self.assertIn('site = [', pyproject_text)
        self.assertIn('"mkdocs>=1.6,<2.0"', pyproject_text)
        self.assertIn('"mkdocs-material>=9.6,<10.0"', pyproject_text)
        self.assertIn('name = "testpypi"', pyproject_text)
        self.assertIn('publish-url = "https://test.pypi.org/legacy/"', pyproject_text)
        self.assertFalse((PROJECT_ROOT / "scripts" / "sync_sources.py").exists())
        self.assertFalse((PROJECT_ROOT / "scripts" / "build_site.py").exists())
        self.assertFalse((PROJECT_ROOT / "scripts" / "sync_source_pointers.py").exists())

    def test_cli_publish_workflow_is_tag_gated_and_uses_trusted_publish(self) -> None:
        workflow_text = (PROJECT_ROOT / ".github" / "workflows" / "publish-cli.yml").read_text(encoding="utf-8")

        self.assertIn('name: Publish CLI', workflow_text)
        self.assertIn('cli-v*.*.*', workflow_text)
        self.assertIn('workflow_dispatch:', workflow_text)
        self.assertIn('uv build --no-sources', workflow_text)
        self.assertIn('uv publish --index testpypi --no-attestations', workflow_text)
        self.assertIn('uv publish --no-attestations', workflow_text)
        self.assertIn('id-token: write', workflow_text)
        self.assertIn('environment:\n      name: testpypi', workflow_text)
        self.assertIn('environment:\n      name: pypi', workflow_text)
        self.assertIn('uvx --refresh', workflow_text)
        self.assertIn('docs-stratego source validate --help', workflow_text)

    def test_source_pointer_sync_workflows_and_docs_are_consistent(self) -> None:
        sync_workflow_text = (PROJECT_ROOT / ".github" / "workflows" / "sync-source-pointers.yml").read_text(
            encoding="utf-8"
        )
        validate_workflow_text = (
            PROJECT_ROOT / ".github" / "workflows" / "validate-source-pointer-pr.yml"
        ).read_text(encoding="utf-8")
        spec_text = (
            PROJECT_ROOT / "docs" / "04-project-development" / "04-design" / "subrepo-sync-specification.md"
        ).read_text(encoding="utf-8")
        usage_text = (PROJECT_ROOT / "docs" / "02-user-guide" / "usage.md").read_text(encoding="utf-8")
        contributor_index_text = (
            PROJECT_ROOT / "docs" / "02-user-guide" / "contributor-guide" / "index.md"
        ).read_text(encoding="utf-8")
        user_guide_index_text = (PROJECT_ROOT / "docs" / "02-user-guide" / "index.md").read_text(encoding="utf-8")
        reader_text = (PROJECT_ROOT / "docs" / "02-user-guide" / "reader-guide.md").read_text(encoding="utf-8")
        local_development_text = (
            PROJECT_ROOT / "docs" / "02-user-guide" / "local-development.md"
        ).read_text(encoding="utf-8")
        onboarding_text = (
            PROJECT_ROOT / "docs" / "02-user-guide" / "contributor-guide" / "onboarding.md"
        ).read_text(encoding="utf-8")
        automation_text = (
            PROJECT_ROOT / "docs" / "02-user-guide" / "contributor-guide" / "automation.md"
        ).read_text(encoding="utf-8")
        contributor_standard_text = (
            PROJECT_ROOT / "docs" / "02-user-guide" / "contributor-guide" / "source-docs-standard.md"
        ).read_text(encoding="utf-8")
        contributor_cli_text = (
            PROJECT_ROOT / "docs" / "02-user-guide" / "contributor-guide" / "cli.md"
        ).read_text(encoding="utf-8")
        distribution_text = (
            PROJECT_ROOT / "docs" / "02-user-guide" / "contributor-guide" / "distribution.md"
        ).read_text(encoding="utf-8")
        publish_setup_text = (
            PROJECT_ROOT / "docs" / "02-user-guide" / "contributor-guide" / "publish-setup.md"
        ).read_text(encoding="utf-8")
        release_text = (
            PROJECT_ROOT / "docs" / "02-user-guide" / "contributor-guide" / "release.md"
        ).read_text(encoding="utf-8")
        admin_text = (PROJECT_ROOT / "docs" / "02-user-guide" / "admin-guide.md").read_text(encoding="utf-8")
        config_text = (PROJECT_ROOT / "docs" / "02-user-guide" / "configuration.md").read_text(encoding="utf-8")
        installation_text = (PROJECT_ROOT / "docs" / "02-user-guide" / "installation.md").read_text(encoding="utf-8")
        root_index_text = (PROJECT_ROOT / "docs" / "index.md").read_text(encoding="utf-8")
        workflow_report_text = (
            PROJECT_ROOT
            / "docs"
            / "04-project-development"
            / "08-operations-maintenance"
            / "github-actions-workflow-report.md"
        ).read_text(encoding="utf-8")
        review_report_text = (
            PROJECT_ROOT
            / "docs"
            / "04-project-development"
            / "08-operations-maintenance"
            / "user-guide-readability-review.md"
        ).read_text(encoding="utf-8")

        self.assertIn("source-pointer-sync-requested", sync_workflow_text)
        self.assertNotIn("source-docs-updated", sync_workflow_text)
        self.assertIn("cancel-in-progress: true", sync_workflow_text)
        self.assertIn("DOCS_STRATEGO_SYNC_PAT", sync_workflow_text)
        self.assertIn("persist-credentials: false", sync_workflow_text)
        self.assertIn("DOCS_STRATEGO_SYNC_PAT", sync_workflow_text)
        self.assertIn("Validate Source Pointer PR", validate_workflow_text)
        self.assertIn("github.head_ref == 'bot/sync-source-pointers'", validate_workflow_text)
        self.assertIn("tests.test_source_admin", validate_workflow_text)
        self.assertIn("tests.test_cli", validate_workflow_text)
        self.assertIn("uv sync --frozen --extra site", validate_workflow_text)
        self.assertIn("docs-stratego sync --config config/source-repos.json --project-root . --source-mode remote", validate_workflow_text)
        self.assertIn("tests.test_sync_source_pointers", validate_workflow_text)
        self.assertIn("tests.test_source_admin", (PROJECT_ROOT / ".github" / "workflows" / "deploy-docs.yml").read_text(encoding="utf-8"))
        self.assertIn("tests.test_cli", (PROJECT_ROOT / ".github" / "workflows" / "deploy-docs.yml").read_text(encoding="utf-8"))
        self.assertIn("source-pointer-sync-requested", spec_text)
        self.assertIn("自动联动", usage_text)
        self.assertIn("CLI 命令", usage_text)
        self.assertIn("CLI 分发与发布", usage_text)
        self.assertIn("发布前外部配置", usage_text)
        self.assertIn("CLI 发布手册", usage_text)
        self.assertIn("uv run docs-stratego dev", usage_text)
        self.assertIn("按任务找入口", user_guide_index_text)
        self.assertIn("平台管理", user_guide_index_text)
        self.assertIn("接入知识地图", contributor_index_text)
        self.assertIn("发布前外部配置", contributor_index_text)
        self.assertIn("site-reader-login-popup.svg", reader_text)
        self.assertIn("### 4.1 `source_mode=local`", local_development_text)
        self.assertIn("local-dev-watch-mode.svg", local_development_text)
        self.assertIn("uv sync --extra site", local_development_text)
        self.assertIn("source_mode=remote", local_development_text)
        self.assertIn("source-onboarding-flow.svg", onboarding_text)
        self.assertIn("source validate", onboarding_text)
        self.assertIn("--project-root /path/to/docs-stratego", onboarding_text)
        self.assertIn("source-notify-workflow.svg", automation_text)
        self.assertIn("唯一导航与权限事实源", contributor_standard_text)
        self.assertIn("uv sync --extra site", (PROJECT_ROOT / "README.md").read_text(encoding="utf-8"))
        self.assertIn("uv run docs-stratego dev", (PROJECT_ROOT / "README.md").read_text(encoding="utf-8"))
        self.assertIn("uv run docs-stratego dev", contributor_cli_text)
        self.assertIn("自动重建", contributor_cli_text)
        self.assertIn("先按任务找命令", contributor_cli_text)
        self.assertIn("docs-stratego[site]", contributor_cli_text)
        self.assertIn("uv run docs-stratego source add", contributor_cli_text)
        self.assertIn("uv run docs-stratego source remove", contributor_cli_text)
        self.assertIn("uvx --from 'docs-stratego==<version>'", contributor_cli_text)
        self.assertIn("Trusted Publisher", publish_setup_text)
        self.assertIn("publish-cli.yml", publish_setup_text)
        self.assertIn("Trusted Publishing", distribution_text)
        self.assertIn("docs-stratego[site]", distribution_text)
        self.assertIn("TestPyPI", distribution_text)
        self.assertIn("uv tool install", distribution_text)
        self.assertIn("cli-vX.Y.Z", distribution_text)
        self.assertIn("普通 `push` 不触发发布", distribution_text)
        self.assertIn("uv sync --extra site", release_text)
        self.assertIn("git tag cli-v0.1.2", release_text)
        self.assertIn("Publish CLI", release_text)
        self.assertIn("uv run docs-stratego dev --help", release_text)
        self.assertIn("PyPI 版本不可覆盖", release_text)
        self.assertIn("source sync-pointers", admin_text)
        self.assertIn("DOCS_STRATEGO_DISPATCH_TOKEN", admin_text)
        self.assertIn("DOCS_STRATEGO_SYNC_PAT", admin_text)
        self.assertIn("DOCS_STRATEGO_DISPATCH_TOKEN", config_text)
        self.assertIn("source scaffold-notify", config_text)
        self.assertIn("server-deployment-layout.svg", installation_text)
        self.assertIn("阅读与访问", root_index_text)
        self.assertIn("平台管理", root_index_text)
        self.assertIn("Deploy Docs", workflow_report_text)
        self.assertIn("Sync Source Pointers", workflow_report_text)
        self.assertIn("Validate Source Pointer PR", workflow_report_text)
        self.assertIn("Publish CLI", workflow_report_text)
        self.assertIn("uv sync --frozen --extra site", workflow_report_text)
        self.assertIn("当前未发现阻断性的知识盲点", review_report_text)

        for asset_name in [
            "site-reader-login-popup.svg",
            "local-dev-watch-mode.svg",
            "source-onboarding-flow.svg",
            "source-notify-workflow.svg",
            "operator-sync-pr-review.svg",
            "server-deployment-layout.svg",
        ]:
            self.assertTrue((PROJECT_ROOT / "docs" / "assets" / "user-guide" / asset_name).exists())


if __name__ == "__main__":
    unittest.main()
