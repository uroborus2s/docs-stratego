from __future__ import annotations

import importlib
import io
import sys
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

    def test_dev_command_runs_sync_build_and_mkdocs_serve(self) -> None:
        with (
            mock.patch.object(self.module, "sync_sources") as sync_sources,
            mock.patch.object(self.module, "build_generated_inputs", return_value=Path("/tmp/mkdocs.generated.yml")) as build_inputs,
            mock.patch.object(self.module, "run_mkdocs_command") as run_mkdocs,
            redirect_stdout(io.StringIO()) as stdout,
        ):
            self.module.main(["dev", "--project-root", ".", "--host", "127.0.0.1", "--port", "9000"])

        sync_sources.assert_called_once()
        build_inputs.assert_called_once()
        run_mkdocs.assert_called_once_with(
            ["serve", "-f", "/tmp/mkdocs.generated.yml", "-a", "127.0.0.1:9000"]
        )
        self.assertIn("Preview: http://127.0.0.1:9000/", stdout.getvalue())

    def test_dev_command_build_only_runs_mkdocs_build(self) -> None:
        with (
            mock.patch.object(self.module, "sync_sources"),
            mock.patch.object(self.module, "build_generated_inputs", return_value=Path("/tmp/mkdocs.generated.yml")),
            mock.patch.object(self.module, "run_mkdocs_command") as run_mkdocs,
        ):
            self.module.main(["dev", "--project-root", ".", "--build-only", "--site-dir", "site-out"])

        run_mkdocs.assert_called_once_with(
            ["build", "-f", "/tmp/mkdocs.generated.yml", "-d", str((Path(".").resolve() / "site-out").resolve())]
        )


if __name__ == "__main__":
    unittest.main()
