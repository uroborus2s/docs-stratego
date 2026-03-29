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
        start_script_text = (PROJECT_ROOT / "start.sh").read_text(encoding="utf-8")

        self.assertIn("validate:", workflow_text)
        self.assertIn("needs: validate", workflow_text)
        self.assertIn("actions/checkout@v4", workflow_text)
        self.assertIn("actions/setup-python@v5", workflow_text)
        self.assertIn("astral-sh/setup-uv@v7", workflow_text)
        self.assertIn("uv sync --frozen", workflow_text)
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
        self.assertIn("scripts/sync_sources.py", start_script_text)
        self.assertIn('SOURCE_MODE="${DOCS_SOURCE_MODE:-local}"', start_script_text)
        self.assertIn("--source-mode", start_script_text)


if __name__ == "__main__":
    unittest.main()
