from __future__ import annotations

import importlib
import json
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))


def load_module():
    return importlib.import_module("source_admin")


class SourceAdminTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_module()

    def test_add_source_repository_appends_dual_mode_entry(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            config_path = tmp_path / "source-repos.json"
            config_path.write_text(
                json.dumps(
                    {
                        "version": 3,
                        "default_source_mode": "local",
                        "repositories": [
                            {
                                "name": "docs-stratego",
                                "title": "章略·墨衡",
                                "modes": {
                                    "local": {"source_type": "local", "local_path": "docs"},
                                    "remote": {"source_type": "local", "local_path": "docs"},
                                },
                            }
                        ],
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )

            spec = self.module.SourceRegistration(
                name="atlas",
                title="星图",
                repo_url="https://github.com/example/atlas",
                git_url="https://github.com/example/atlas.git",
                branch="main",
                local_path="../atlas/docs",
            )

            added = self.module.add_source_repository(config_path, spec)
            payload = json.loads(config_path.read_text(encoding="utf-8"))

        self.assertEqual("atlas", added["name"])
        self.assertEqual("../atlas/docs", added["modes"]["local"]["local_path"])
        self.assertEqual("sources/atlas", added["modes"]["remote"]["submodule_path"])
        self.assertEqual(
            ["docs-stratego", "atlas"],
            [item["name"] for item in payload["repositories"]],
        )

    def test_add_source_repository_rejects_duplicate_name(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            config_path = tmp_path / "source-repos.json"
            config_path.write_text(
                json.dumps(
                    {
                        "version": 3,
                        "repositories": [
                            {
                                "name": "atlas",
                                "title": "星图",
                                "modes": {
                                    "local": {"source_type": "local", "local_path": "../atlas/docs"},
                                    "remote": {
                                        "source_type": "submodule_sparse",
                                        "git_url": "https://github.com/example/atlas.git",
                                        "branch": "main",
                                        "submodule_path": "sources/atlas",
                                        "docs_path": "docs",
                                    },
                                },
                            }
                        ],
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )

            spec = self.module.SourceRegistration(
                name="atlas",
                title="星图",
                repo_url="https://github.com/example/atlas",
                git_url="https://github.com/example/atlas.git",
                branch="main",
                local_path="../atlas/docs",
            )

            with self.assertRaisesRegex(ValueError, "already exists"):
                self.module.add_source_repository(config_path, spec)

    def test_remove_source_repository_rejects_protected_name(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            config_path = tmp_path / "source-repos.json"
            config_path.write_text(
                json.dumps(
                    {
                        "version": 3,
                        "repositories": [
                            {
                                "name": "docs-stratego",
                                "title": "章略·墨衡",
                                "modes": {
                                    "local": {"source_type": "local", "local_path": "docs"},
                                    "remote": {"source_type": "local", "local_path": "docs"},
                                },
                            }
                        ],
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "cannot be removed"):
                self.module.remove_source_repository(config_path, "docs-stratego")

    def test_render_notify_workflow_contains_dispatch_contract(self) -> None:
        workflow = self.module.render_notify_workflow(
            repository_full_name="uroborus2s/docs-stratego",
            branches=["main", "release"],
        )

        self.assertIn("name: Notify Docs Stratego", workflow)
        self.assertIn("source-pointer-sync-requested", workflow)
        self.assertIn("https://api.github.com/repos/uroborus2s/docs-stratego/dispatches", workflow)
        self.assertIn("  - main", workflow)
        self.assertIn("  - release", workflow)

    def test_scaffold_notify_workflow_creates_and_removes_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir)

            created_path = self.module.scaffold_notify_workflow(
                repo_root=repo_root,
                repository_full_name="uroborus2s/docs-stratego",
                branches=["main"],
            )
            self.assertTrue(created_path.exists())
            self.assertIn("Notify Docs Stratego", created_path.read_text(encoding="utf-8"))

            removed_path = self.module.remove_notify_workflow(repo_root)
            self.assertEqual(created_path, removed_path)
            self.assertFalse(created_path.exists())

    def test_validate_source_repository_reports_declared_pages(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir)
            docs_root = repo_root / "docs"
            (docs_root / "01-getting-started").mkdir(parents=True)
            (docs_root / "index.md").write_text(
                "---\n"
                "title: 星图\n"
                "mkdocs:\n"
                "  home_access: public\n"
                "  nav:\n"
                "    - title: 快速开始\n"
                "      children:\n"
                "        - title: 概览\n"
                "          path: 01-getting-started/index.md\n"
                "          access: public\n"
                "---\n"
                "# 星图\n",
                encoding="utf-8",
            )
            (docs_root / "01-getting-started" / "index.md").write_text(
                "# 快速开始\n",
                encoding="utf-8",
            )

            report = self.module.validate_source_repository(repo_root)

        self.assertEqual("星图", report.title)
        self.assertEqual("public", report.home_access)
        self.assertEqual(1, report.page_count)
        self.assertEqual(0, report.contract_count)


if __name__ == "__main__":
    unittest.main()
