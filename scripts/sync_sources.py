from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from docs_stratego.source_sync import sync_sources


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync source repositories with sparse checkout.")
    parser.add_argument("--config", default="config/source-repos.json")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--source-mode", choices=["local", "remote"], default=None)
    args = parser.parse_args()

    sync_sources(Path(args.config), Path(args.project_root).resolve(), source_mode=args.source_mode)


if __name__ == "__main__":
    main()
