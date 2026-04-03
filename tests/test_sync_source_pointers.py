from __future__ import annotations

import importlib
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))


def load_module():
    return importlib.import_module("source_pointer_sync")


class SyncSourcePointersTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_module()

    def test_load_remote_submodule_repositories_uses_remote_mode(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            config_path = tmp_path / "source-repos.json"
            config_path.write_text(
                "{\n"
                '  "version": 3,\n'
                '  "repositories": [\n'
                "    {\n"
                '      "name": "docs-stratego",\n'
                '      "title": "章略·墨衡",\n'
                '      "modes": {\n'
                '        "local": {"source_type": "local", "local_path": "docs"},\n'
                '        "remote": {"source_type": "local", "local_path": "docs"}\n'
                "      }\n"
                "    },\n"
                "    {\n"
                '      "name": "shanforge",\n'
                '      "title": "山海工枢",\n'
                '      "modes": {\n'
                '        "local": {"source_type": "local", "local_path": "../shanforge/docs"},\n'
                '        "remote": {\n'
                '          "source_type": "submodule_sparse",\n'
                '          "git_url": "https://github.com/example/shanforge.git",\n'
                '          "branch": "main",\n'
                '          "submodule_path": "sources/shanforge",\n'
                '          "docs_path": "docs"\n'
                "        }\n"
                "      }\n"
                "    }\n"
                "  ]\n"
                "}\n",
                encoding="utf-8",
            )

            repos = self.module.load_remote_submodule_repositories(config_path)

        self.assertEqual(["shanforge"], [repo.name for repo in repos])
        self.assertEqual("submodule_sparse", repos[0].source_type)
        self.assertEqual("sources/shanforge", repos[0].submodule_path)

    def test_detect_base_branch_prefers_origin_head(self) -> None:
        completed = mock.Mock(stdout="origin/main\n")
        with mock.patch.object(self.module, "run_command", return_value=completed) as mocked_run:
            branch = self.module.detect_base_branch(PROJECT_ROOT)

        self.assertEqual("main", branch)
        mocked_run.assert_called_once_with(
            ["git", "symbolic-ref", "--quiet", "--short", "refs/remotes/origin/HEAD"],
            cwd=PROJECT_ROOT,
        )

    def test_changed_submodule_paths_reads_only_sources(self) -> None:
        completed = mock.Mock(stdout=" M sources/shanforge\n M sources/crawler4j\n")
        with mock.patch.object(self.module, "run_command", return_value=completed):
            changed_paths = self.module.get_changed_submodule_paths(PROJECT_ROOT)

        self.assertEqual(["sources/shanforge", "sources/crawler4j"], changed_paths)

    def test_sync_source_pointers_stages_only_changed_submodules_and_updates_pr(self) -> None:
        project_root = PROJECT_ROOT
        config_path = project_root / "config" / "source-repos.json"
        repos = [
            self.module.SourceRepository(
                name="shanforge",
                title="山海工枢",
                source_type="submodule_sparse",
                submodule_path="sources/shanforge",
                branch="main",
            ),
            self.module.SourceRepository(
                name="ctrip_crawler",
                title="携游数据管家",
                source_type="submodule_sparse",
                submodule_path="sources/ctrip_crawler",
                branch="main",
            ),
        ]

        with (
            mock.patch.object(self.module, "load_remote_submodule_repositories", return_value=repos),
            mock.patch.object(self.module, "detect_base_branch", return_value="main"),
            mock.patch.object(self.module, "prepare_bot_branch") as prepare_bot_branch,
            mock.patch.object(self.module, "sync_sources") as sync_sources,
            mock.patch.object(
                self.module,
                "get_changed_submodule_paths",
                return_value=["sources/shanforge", "sources/ctrip_crawler"],
            ),
            mock.patch.object(self.module, "run_command") as run_command,
            mock.patch.object(self.module, "create_or_update_shared_pr") as create_or_update_shared_pr,
        ):
            updated = self.module.sync_source_pointers(project_root, config_path)

        self.assertEqual(["shanforge", "ctrip_crawler"], updated)
        prepare_bot_branch.assert_called_once_with(
            project_root, "bot/sync-source-pointers", "main"
        )
        sync_sources.assert_called_once_with(config_path, project_root, source_mode="remote")
        run_command.assert_has_calls(
            [
                mock.call(
                    ["git", "add", "--", "sources/shanforge", "sources/ctrip_crawler"],
                    cwd=project_root,
                ),
                mock.call(
                    ["git", "commit", "-m", "chore: sync source repository pointers"],
                    cwd=project_root,
                ),
                mock.call(
                    ["git", "push", "origin", "bot/sync-source-pointers", "--force-with-lease"],
                    cwd=project_root,
                ),
            ]
        )
        create_or_update_shared_pr.assert_called_once_with(
            project_root,
            "bot/sync-source-pointers",
            "main",
            ["shanforge", "ctrip_crawler"],
            "chore: sync source repository pointers",
        )

    def test_sync_source_pointers_returns_early_when_no_changes(self) -> None:
        project_root = PROJECT_ROOT
        config_path = project_root / "config" / "source-repos.json"
        repos = [
            self.module.SourceRepository(
                name="shanforge",
                title="山海工枢",
                source_type="submodule_sparse",
                submodule_path="sources/shanforge",
                branch="main",
            )
        ]

        with (
            mock.patch.object(self.module, "load_remote_submodule_repositories", return_value=repos),
            mock.patch.object(self.module, "detect_base_branch", return_value="main"),
            mock.patch.object(self.module, "prepare_bot_branch"),
            mock.patch.object(self.module, "sync_sources"),
            mock.patch.object(self.module, "get_changed_submodule_paths", return_value=[]),
            mock.patch.object(self.module, "run_command") as run_command,
            mock.patch.object(self.module, "create_or_update_shared_pr") as create_or_update_shared_pr,
        ):
            updated = self.module.sync_source_pointers(project_root, config_path)

        self.assertEqual([], updated)
        run_command.assert_not_called()
        create_or_update_shared_pr.assert_not_called()


if __name__ == "__main__":
    unittest.main()
