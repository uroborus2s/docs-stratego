from __future__ import annotations

import importlib
import io
import sys
import tempfile
import time
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))


def load_module():
    return importlib.import_module("cli")


class CliTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_module()
        cls.dev_server = importlib.import_module("dev_server")

    def test_sync_command_delegates_to_source_sync(self) -> None:
        with mock.patch.object(self.module, "sync_sources") as sync_sources:
            self.module.main(["sync", "--config", "config/source-repos.json", "--project-root", "."])

        sync_sources.assert_called_once()

    def test_source_validate_prints_summary(self) -> None:
        report = self.module.ValidationReport(
            repo_root=Path("/tmp/atlas"),
            docs_root=Path("/tmp/atlas/docs"),
            title="星图",
            home_access="public",
            page_count=3,
            contract_count=1,
        )

        with (
            mock.patch.object(self.module, "validate_source_repository", return_value=report),
            redirect_stdout(io.StringIO()) as stdout,
        ):
            self.module.main(["source", "validate", "--repo-path", "/tmp/atlas"])

        output = stdout.getvalue()
        self.assertIn("星图", output)
        self.assertIn("pages=3", output)
        self.assertIn("contracts=1", output)

    def test_source_remove_requires_yes_flag(self) -> None:
        with self.assertRaisesRegex(SystemExit, "2"):
            self.module.main(["source", "remove", "--name", "atlas"])

    def test_source_sync_pointers_delegates_to_pointer_sync_module(self) -> None:
        with mock.patch.object(self.module, "sync_source_pointers", return_value=["shanforge"]) as sync_pointers:
            self.module.main(["source", "sync-pointers", "--project-root", "."])

        sync_pointers.assert_called_once()

    def test_dev_command_local_mode_runs_watch_server(self) -> None:
        with (
            mock.patch.object(self.module, "ensure_site_dependencies_installed"),
            mock.patch.object(self.module, "sync_sources") as sync_sources,
            mock.patch.object(self.module, "build_generated_inputs", return_value=Path("/tmp/mkdocs.generated.yml")) as build_inputs,
            mock.patch.object(self.module, "resolve_dev_watch_paths", return_value=[Path("/tmp/docs"), Path("/tmp/config.json")]) as resolve_watch_paths,
            mock.patch.object(self.module, "serve_mkdocs_with_watch") as serve_with_watch,
            redirect_stdout(io.StringIO()) as stdout,
        ):
            self.module.main(["dev", "--project-root", ".", "--host", "127.0.0.1", "--port", "9000"])

        sync_sources.assert_called_once()
        build_inputs.assert_called_once()
        resolve_watch_paths.assert_called_once()
        serve_with_watch.assert_called_once()
        self.assertIn("watch mode: enabled", stdout.getvalue())

    def test_dev_command_remote_mode_runs_mkdocs_serve_without_watch(self) -> None:
        with (
            mock.patch.object(self.module, "ensure_site_dependencies_installed"),
            mock.patch.object(self.module, "sync_sources") as sync_sources,
            mock.patch.object(self.module, "build_generated_inputs", return_value=Path("/tmp/mkdocs.generated.yml")) as build_inputs,
            mock.patch.object(self.module, "run_mkdocs_command") as run_mkdocs,
            mock.patch.object(self.module, "serve_mkdocs_with_watch") as serve_with_watch,
            redirect_stdout(io.StringIO()) as stdout,
        ):
            self.module.main(
                ["dev", "--project-root", ".", "--source-mode", "remote", "--host", "127.0.0.1", "--port", "9000"]
            )

        sync_sources.assert_called_once()
        build_inputs.assert_called_once()
        run_mkdocs.assert_called_once_with(
            ["serve", "-f", "/tmp/mkdocs.generated.yml", "-a", "127.0.0.1:9000"]
        )
        serve_with_watch.assert_not_called()
        self.assertIn("watch mode: disabled", stdout.getvalue())

    def test_dev_command_build_only_runs_mkdocs_build(self) -> None:
        with (
            mock.patch.object(self.module, "ensure_site_dependencies_installed"),
            mock.patch.object(self.module, "sync_sources"),
            mock.patch.object(self.module, "build_generated_inputs", return_value=Path("/tmp/mkdocs.generated.yml")),
            mock.patch.object(self.module, "run_mkdocs_command") as run_mkdocs,
        ):
            self.module.main(["dev", "--project-root", ".", "--build-only", "--site-dir", "site-out"])

        run_mkdocs.assert_called_once_with(
            ["build", "-f", "/tmp/mkdocs.generated.yml", "-d", str((Path(".").resolve() / "site-out").resolve())]
        )

    def test_dev_command_fails_fast_without_site_extra(self) -> None:
        with mock.patch.object(
            self.module,
            "ensure_site_dependencies_installed",
            side_effect=SystemExit("The dev/build-only commands require the site extra."),
        ):
            with self.assertRaisesRegex(SystemExit, "site extra"):
                self.module.main(["dev", "--project-root", "."])

    def test_resolve_dev_watch_paths_includes_local_docs_and_config(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            project_root = Path(tmp_dir)
            (project_root / "docs").mkdir()
            external_docs = project_root / "external-docs"
            external_docs.mkdir()
            config_path = project_root / "config.json"
            config_path.write_text(
                (
                    '{\n'
                    '  "version": 3,\n'
                    '  "default_source_mode": "local",\n'
                    '  "repositories": [\n'
                    '    {\n'
                    '      "name": "docs-stratego",\n'
                    '      "title": "章略·墨衡",\n'
                    '      "modes": {\n'
                    '        "local": {"source_type": "local", "local_path": "docs"},\n'
                    '        "remote": {"source_type": "local", "local_path": "docs"}\n'
                    '      }\n'
                    '    },\n'
                    '    {\n'
                    '      "name": "atlas",\n'
                    '      "title": "星图",\n'
                    '      "modes": {\n'
                    '        "local": {"source_type": "local", "local_path": "external-docs"},\n'
                    '        "remote": {"source_type": "submodule_sparse", "git_url": "https://example.com/atlas.git", "submodule_path": "sources/atlas", "docs_path": "docs"}\n'
                    '      }\n'
                    '    }\n'
                    '  ]\n'
                    '}\n'
                ),
                encoding="utf-8",
            )

            watch_paths = self.dev_server.resolve_dev_watch_paths(project_root, config_path)

        self.assertEqual(
            {str(path) for path in watch_paths},
            {str(config_path.resolve()), str((project_root / "docs").resolve()), str(external_docs.resolve())},
        )

    def test_watch_loop_rebuilds_when_watched_file_changes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            docs_root = Path(tmp_dir) / "docs"
            docs_root.mkdir()
            page = docs_root / "index.md"
            page.write_text("# v1\n", encoding="utf-8")
            rebuild = mock.Mock(return_value=None)

            watch_loop = self.dev_server.WatchLoop([docs_root], rebuild_callback=rebuild)

            self.assertFalse(watch_loop.poll_once())
            time.sleep(0.01)
            page.write_text("# v2\n", encoding="utf-8")

            self.assertTrue(watch_loop.poll_once())
            rebuild.assert_called_once()
            self.assertFalse(watch_loop.poll_once())

    def test_watch_loop_refreshes_paths_after_config_change(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            config_path = Path(tmp_dir) / "config.json"
            config_path.write_text('{"version": 3}\n', encoding="utf-8")
            new_docs_root = Path(tmp_dir) / "new-docs"
            new_docs_root.mkdir()
            rebuild = mock.Mock(return_value=[config_path, new_docs_root])

            watch_loop = self.dev_server.WatchLoop([config_path], rebuild_callback=rebuild)

            self.assertFalse(watch_loop.poll_once())
            time.sleep(0.01)
            config_path.write_text('{"version": 4}\n', encoding="utf-8")

            self.assertTrue(watch_loop.poll_once())
            self.assertIn(new_docs_root.resolve(), watch_loop.watch_paths)


if __name__ == "__main__":
    unittest.main()
