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
    return importlib.import_module("docs_stratego.source_sync")


class SourceSyncTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_module()

    def test_load_source_repositories_supports_dual_mode_configuration(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            config_path = tmp_path / "source-repos.json"
            config_path.write_text(
                "{\n"
                '  "version": 3,\n'
                '  "default_source_mode": "local",\n'
                '  "repositories": [\n'
                "    {\n"
                '      "name": "crawler4j",\n'
                '      "title": "蛛行演略",\n'
                '      "repo_url": "https://github.com/example/crawler4j",\n'
                '      "modes": {\n'
                '        "local": {\n'
                '          "source_type": "local",\n'
                '          "local_path": "sources/crawler4j/docs"\n'
                "        },\n"
                '        "remote": {\n'
                '          "source_type": "submodule_sparse",\n'
                '          "git_url": "https://github.com/example/crawler4j.git",\n'
                '          "branch": "main",\n'
                '          "submodule_path": "sources/crawler4j",\n'
                '          "docs_path": "docs"\n'
                "        }\n"
                "      }\n"
                "    }\n"
                "  ]\n"
                "}\n",
                encoding="utf-8",
            )

            local_repos = self.module.load_source_repositories(config_path, source_mode="local")
            remote_repos = self.module.load_source_repositories(config_path, source_mode="remote")
            default_repos = self.module.load_source_repositories(config_path)

        self.assertEqual("local", local_repos[0].source_type)
        self.assertEqual("sources/crawler4j/docs", local_repos[0].local_path)
        self.assertEqual("submodule_sparse", remote_repos[0].source_type)
        self.assertEqual("https://github.com/example/crawler4j.git", remote_repos[0].git_url)
        self.assertEqual("main", remote_repos[0].branch)
        self.assertEqual("sources/crawler4j", remote_repos[0].submodule_path)
        self.assertEqual("local", default_repos[0].source_type)

    def test_load_source_repositories_rejects_missing_mode_definition(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            config_path = tmp_path / "source-repos.json"
            config_path.write_text(
                "{\n"
                '  "version": 3,\n'
                '  "repositories": [\n'
                "    {\n"
                '      "name": "crawler4j",\n'
                '      "title": "蛛行演略",\n'
                '      "modes": {\n'
                '        "local": {\n'
                '          "source_type": "local",\n'
                '          "local_path": "../crawler4j/docs"\n'
                "        }\n"
                "      }\n"
                "    }\n"
                "  ]\n"
                "}\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "missing source mode: remote"):
                self.module.load_source_repositories(config_path, source_mode="remote")

    def test_load_source_repositories_rejects_legacy_flat_repo_configuration(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            config_path = tmp_path / "source-repos.json"
            config_path.write_text(
                "{\n"
                '  "version": 3,\n'
                '  "repositories": [\n'
                "    {\n"
                '      "name": "crawler4j",\n'
                '      "title": "蛛行演略",\n'
                '      "source_type": "local",\n'
                '      "local_path": "../crawler4j/docs"\n'
                "    }\n"
                "  ]\n"
                "}\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "missing modes configuration"):
                self.module.load_source_repositories(config_path, source_mode="local")

    def test_sync_submodule_sparse_repo_updates_remote_and_sparse_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            repo = self.module.SourceRepository(
                name="crawler4j",
                title="蛛行演略",
                source_type="submodule_sparse",
                git_url="https://example.com/crawler4j.git",
                branch="main",
                docs_path="docs",
                submodule_path="sources/crawler4j",
            )

            with mock.patch.object(self.module.subprocess, "run") as mocked_run:
                self.module.sync_submodule_sparse_repository(repo, tmp_path)

        repo_root = (tmp_path / "sources" / "crawler4j").resolve()
        mocked_run.assert_has_calls(
            [
                mock.call(
                    ["git", "submodule", "sync", "--", "sources/crawler4j"],
                    cwd=tmp_path,
                    check=True,
                ),
                mock.call(
                    ["git", "submodule", "update", "--init", "--depth", "1", "--", "sources/crawler4j"],
                    cwd=tmp_path,
                    check=True,
                ),
                mock.call(
                    ["git", "-C", str(repo_root), "fetch", "origin", "main", "--depth", "1"],
                    check=True,
                ),
                mock.call(
                    ["git", "-C", str(repo_root), "checkout", "-B", "main", "FETCH_HEAD"],
                    check=True,
                ),
                mock.call(
                    ["git", "-C", str(repo_root), "sparse-checkout", "init", "--no-cone"],
                    check=True,
                ),
                mock.call(
                    ["git", "-C", str(repo_root), "sparse-checkout", "set", "--no-cone", "/docs/", "/docs/**"],
                    check=True,
                ),
            ]
        )

    def test_sync_existing_submodule_sparse_repo_updates_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            repo_root = (tmp_path / "sources" / "crawler4j").resolve()
            repo_root.mkdir(parents=True)
            (repo_root / ".git").write_text("gitdir: ../../.git/modules/sources/crawler4j\n", encoding="utf-8")

            repo = self.module.SourceRepository(
                name="crawler4j",
                title="蛛行演略",
                source_type="submodule_sparse",
                git_url="https://example.com/crawler4j.git",
                branch="main",
                docs_path="docs",
                submodule_path="sources/crawler4j",
            )

            with mock.patch.object(self.module.subprocess, "run") as mocked_run:
                self.module.sync_submodule_sparse_repository(repo, tmp_path)

        mocked_run.assert_has_calls(
            [
                mock.call(["git", "submodule", "sync", "--", "sources/crawler4j"], cwd=tmp_path, check=True),
                mock.call(
                    ["git", "submodule", "update", "--init", "--depth", "1", "--", "sources/crawler4j"],
                    cwd=tmp_path,
                    check=True,
                ),
                mock.call(["git", "-C", str(repo_root), "fetch", "origin", "main", "--depth", "1"], check=True),
                mock.call(["git", "-C", str(repo_root), "checkout", "-B", "main", "FETCH_HEAD"], check=True),
                mock.call(["git", "-C", str(repo_root), "sparse-checkout", "init", "--no-cone"], check=True),
                mock.call(
                    ["git", "-C", str(repo_root), "sparse-checkout", "set", "--no-cone", "/docs/", "/docs/**"],
                    check=True,
                ),
            ]
        )

    def test_sync_non_git_directory_recreates_submodule_checkout(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            repo_root = (tmp_path / "sources" / "crawler4j").resolve()
            repo_root.mkdir(parents=True)
            (repo_root / "docs").mkdir()

            repo = self.module.SourceRepository(
                name="crawler4j",
                title="蛛行演略",
                source_type="submodule_sparse",
                git_url="https://example.com/crawler4j.git",
                branch="main",
                docs_path="docs",
                submodule_path="sources/crawler4j",
            )

            with mock.patch.object(self.module.subprocess, "run") as mocked_run:
                self.module.sync_submodule_sparse_repository(repo, tmp_path)

        self.assertFalse((repo_root / "docs").exists())
        mocked_run.assert_has_calls(
            [
                mock.call(
                    ["git", "submodule", "sync", "--", "sources/crawler4j"],
                    cwd=tmp_path,
                    check=True,
                ),
                mock.call(
                    ["git", "submodule", "update", "--init", "--depth", "1", "--", "sources/crawler4j"],
                    cwd=tmp_path,
                    check=True,
                ),
                mock.call(
                    ["git", "-C", str(repo_root), "fetch", "origin", "main", "--depth", "1"],
                    check=True,
                ),
                mock.call(
                    ["git", "-C", str(repo_root), "checkout", "-B", "main", "FETCH_HEAD"],
                    check=True,
                ),
                mock.call(
                    ["git", "-C", str(repo_root), "sparse-checkout", "init", "--no-cone"],
                    check=True,
                ),
                mock.call(
                    ["git", "-C", str(repo_root), "sparse-checkout", "set", "--no-cone", "/docs/", "/docs/**"],
                    check=True,
                ),
            ]
        )

    def test_sync_submodule_sparse_repo_rejects_unregistered_gitlink(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            repo = self.module.SourceRepository(
                name="ride-loop",
                title="千乘坊",
                source_type="submodule_sparse",
                git_url="https://example.com/ride-loop.git",
                branch="main",
                docs_path="docs",
                submodule_path="sources/ride-loop",
            )

            def fake_run(args, **kwargs):
                if args[:3] == ["git", "ls-files", "--stage"]:
                    return mock.Mock(stdout="")
                raise AssertionError(f"unexpected subprocess call: {args}")

            with mock.patch.object(self.module.subprocess, "run", side_effect=fake_run):
                with self.assertRaisesRegex(
                    ValueError,
                    "ride-loop submodule_path sources/ride-loop is not registered as a git submodule",
                ):
                    self.module.sync_submodule_sparse_repository(repo, tmp_path)


if __name__ == "__main__":
    unittest.main()
