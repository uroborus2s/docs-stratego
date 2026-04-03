from __future__ import annotations

import os
import subprocess
import sys
import threading
from pathlib import Path
from typing import Callable, Sequence

from source_config import load_source_repositories

IGNORED_DIRECTORY_NAMES = {
    ".generated",
    ".git",
    ".hg",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".svn",
    ".venv",
    "__pycache__",
    "site",
}


def resolve_dev_watch_paths(project_root: Path, config_path: Path) -> list[Path]:
    watch_paths = [config_path.resolve()]
    for repo in load_source_repositories(config_path, source_mode="local"):
        watch_paths.append(repo.resolve_docs_root(project_root))

    deduped_paths: list[Path] = []
    seen: set[str] = set()
    for path in sorted(watch_paths, key=lambda item: str(item.resolve())):
        resolved = path.resolve()
        if str(resolved) in seen:
            continue
        seen.add(str(resolved))
        deduped_paths.append(resolved)
    return deduped_paths


def take_watch_snapshot(watch_paths: Sequence[Path]) -> dict[str, tuple[int, int] | None]:
    snapshot: dict[str, tuple[int, int] | None] = {}
    for path in watch_paths:
        snapshot.update(_take_path_snapshot(path))
    return snapshot


def _take_path_snapshot(path: Path) -> dict[str, tuple[int, int] | None]:
    resolved = path.resolve()
    if not resolved.exists():
        return {str(resolved): None}

    root_stat = resolved.stat()
    snapshot: dict[str, tuple[int, int] | None] = {
        str(resolved): (root_stat.st_mtime_ns, root_stat.st_size)
    }
    if resolved.is_file():
        return snapshot

    for current_root, dir_names, file_names in os.walk(resolved):
        dir_names[:] = sorted(
            name
            for name in dir_names
            if name not in IGNORED_DIRECTORY_NAMES and not name.startswith(".")
        )
        file_names.sort()
        for file_name in file_names:
            file_path = Path(current_root) / file_name
            try:
                stat = file_path.stat()
            except FileNotFoundError:
                continue
            snapshot[str(file_path.resolve())] = (stat.st_mtime_ns, stat.st_size)
    return snapshot


class WatchLoop:
    def __init__(
        self,
        watch_paths: Sequence[Path],
        rebuild_callback: Callable[[], Sequence[Path] | None],
    ) -> None:
        self.watch_paths = [path.resolve() for path in watch_paths]
        self.rebuild_callback = rebuild_callback
        self._snapshot: dict[str, tuple[int, int] | None] | None = None

    def poll_once(self) -> bool:
        current_snapshot = take_watch_snapshot(self.watch_paths)
        if self._snapshot is None:
            self._snapshot = current_snapshot
            return False
        if current_snapshot == self._snapshot:
            return False

        self._snapshot = current_snapshot
        refreshed_paths = self.rebuild_callback()
        if refreshed_paths is not None:
            self.watch_paths = [path.resolve() for path in refreshed_paths]
        self._snapshot = take_watch_snapshot(self.watch_paths)
        return True

    def run(
        self,
        stop_event: threading.Event,
        poll_interval_seconds: float = 1.0,
        output: Callable[[str], None] = print,
        error_output: Callable[[str], None] | None = None,
    ) -> None:
        while not stop_event.wait(poll_interval_seconds):
            try:
                if self.poll_once():
                    output("Detected source doc changes. Rebuilt generated docs.")
            except Exception as exc:  # pragma: no cover - defensive runtime logging
                if error_output is not None:
                    error_output(f"Watch rebuild failed: {exc}")


def start_mkdocs_serve_process(args: list[str]) -> subprocess.Popen[bytes]:
    return subprocess.Popen([sys.executable, "-m", "mkdocs", *args])


def serve_mkdocs_with_watch(
    generated_config: Path,
    host: str,
    port: int,
    watch_paths: Sequence[Path],
    rebuild_callback: Callable[[], Sequence[Path] | None],
    poll_interval_seconds: float = 1.0,
) -> None:
    stop_event = threading.Event()
    watch_loop = WatchLoop(watch_paths, rebuild_callback=rebuild_callback)
    watcher = threading.Thread(
        target=watch_loop.run,
        kwargs={
            "stop_event": stop_event,
            "poll_interval_seconds": poll_interval_seconds,
            "output": print,
            "error_output": lambda message: print(message, file=sys.stderr),
        },
        daemon=True,
    )
    watcher.start()

    process = start_mkdocs_serve_process(
        ["serve", "-f", str(generated_config), "-a", f"{host}:{port}"]
    )
    return_code = 0
    try:
        return_code = process.wait()
    except KeyboardInterrupt:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:  # pragma: no cover - defensive cleanup
            process.kill()
            process.wait(timeout=5)
    finally:
        stop_event.set()
        watcher.join(timeout=max(1.0, poll_interval_seconds + 0.5))

    if return_code != 0:
        raise SystemExit(return_code)
