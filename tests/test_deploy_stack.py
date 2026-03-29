from __future__ import annotations

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

    def test_nginx_template_is_manual_host_config_template(self) -> None:
        docs_text = (PROJECT_ROOT / "deploy" / "nginx" / "docs.conf.template").read_text(encoding="utf-8")
        docs_bootstrap_text = (PROJECT_ROOT / "deploy" / "nginx" / "docs.bootstrap.conf.template").read_text(
            encoding="utf-8"
        )
        auth_text = (PROJECT_ROOT / "deploy" / "nginx" / "auth.conf.template").read_text(encoding="utf-8")
        auth_bootstrap_text = (PROJECT_ROOT / "deploy" / "nginx" / "auth.bootstrap.conf.template").read_text(
            encoding="utf-8"
        )

        self.assertIn("include __PRIVATE_LOCATIONS_PATH__;", docs_text)
        self.assertIn("listen 443 ssl http2;", docs_text)
        self.assertIn("__DOCS_SSL_CERT_PATH__", docs_text)
        self.assertIn("__DOCS_SSL_KEY_PATH__", docs_text)
        self.assertIn("location /oauth2/", docs_text)
        self.assertIn("server_name __DOCS_SERVER_NAME__;", docs_text)
        self.assertIn("proxy_pass __OAUTH2_PROXY_UPSTREAM__;", docs_text)
        self.assertIn("listen 80;", docs_bootstrap_text)
        self.assertNotIn("listen 443 ssl http2;", docs_bootstrap_text)
        self.assertIn("location /oauth2/", docs_bootstrap_text)

        self.assertIn("listen 443 ssl http2;", auth_text)
        self.assertIn("__AUTH_SSL_CERT_PATH__", auth_text)
        self.assertIn("__AUTH_SSL_KEY_PATH__", auth_text)
        self.assertIn("server_name __AUTH_SERVER_NAME__;", auth_text)
        self.assertIn("proxy_pass __CASDOOR_UPSTREAM__;", auth_text)
        self.assertIn("listen 80;", auth_bootstrap_text)
        self.assertNotIn("listen 443 ssl http2;", auth_bootstrap_text)
        self.assertIn("proxy_pass __CASDOOR_UPSTREAM__;", auth_bootstrap_text)

    def test_runtime_auth_configs_exist(self) -> None:
        self.assertTrue((PROJECT_ROOT / "deploy" / "casdoor" / "app.conf").exists())
        self.assertTrue((PROJECT_ROOT / "deploy" / "oauth2-proxy" / "oauth2-proxy.cfg").exists())
        self.assertFalse((PROJECT_ROOT / "deploy" / "nginx" / "includes" / "auth_request.conf").exists())

    def test_deploy_scripts_and_workflow_cover_host_nginx_render_and_sync(self) -> None:
        workflow_text = (PROJECT_ROOT / ".github" / "workflows" / "deploy-docs.yml").read_text(encoding="utf-8")
        deploy_script_text = (PROJECT_ROOT / "scripts" / "deploy_remote.sh").read_text(encoding="utf-8")
        render_script_text = (PROJECT_ROOT / "scripts" / "render_host_nginx_conf.sh").read_text(encoding="utf-8")
        start_script_text = (PROJECT_ROOT / "start.sh").read_text(encoding="utf-8")

        self.assertIn("validate:", workflow_text)
        self.assertIn("needs: validate", workflow_text)
        self.assertIn("actions/checkout@v4", workflow_text)
        self.assertIn("actions/setup-python@v5", workflow_text)
        self.assertIn("astral-sh/setup-uv@v7", workflow_text)
        self.assertIn("uv sync --frozen", workflow_text)
        self.assertIn("--source-mode remote", workflow_text)
        self.assertIn("/var/www/docs-stratego", workflow_text)
        self.assertIn("/etc/nginx/snippets/docs-stratego/private_locations.conf", workflow_text)
        self.assertIn("DOCS_PRIVATE_LOCATIONS_PATH", workflow_text)
        self.assertIn("RELOAD_HOST_NGINX", workflow_text)
        self.assertNotIn("render_host_nginx_conf.sh", deploy_script_text)
        self.assertIn('DOCS_SOURCE_MODE="${DOCS_SOURCE_MODE:-remote}"', deploy_script_text)
        self.assertIn('--source-mode "$DOCS_SOURCE_MODE"', deploy_script_text)
        self.assertIn("systemctl reload nginx", deploy_script_text)
        self.assertIn("scripts/sync_sources.py", start_script_text)
        self.assertIn('SOURCE_MODE="${DOCS_SOURCE_MODE:-local}"', start_script_text)
        self.assertIn("--source-mode", start_script_text)
        self.assertIn("__PRIVATE_LOCATIONS_PATH__", render_script_text)
        self.assertIn("__DOCS_SERVER_NAME__", render_script_text)
        self.assertIn("__DOCS_SSL_CERT_PATH__", render_script_text)


if __name__ == "__main__":
    unittest.main()
