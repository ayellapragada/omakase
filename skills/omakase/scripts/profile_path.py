#!/usr/bin/env python3
"""Print the one Omakase profile path shared by a repository's worktrees."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys


PROFILE_NAME = ".omakase.local.yml"


def primary_checkout(repo: Path) -> Path:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), "worktree", "list", "--porcelain"],
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as error:
        raise RuntimeError("git executable is unavailable") from error

    if result.returncode != 0:
        raise RuntimeError(
            f"{repo}: not inside a Git repository with accessible worktree metadata"
        )

    first_record = result.stdout.split("\n\n", 1)[0].splitlines()
    if "bare" in first_record:
        raise RuntimeError(f"{repo}: bare repository has no working tree")

    for line in first_record:
        if line.startswith("worktree "):
            return Path(line.removeprefix("worktree ")).resolve()

    raise RuntimeError(f"{repo}: Git returned no primary checkout")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Resolve .omakase.local.yml in a repository's primary checkout."
    )
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    args = parser.parse_args()

    try:
        print(primary_checkout(args.repo) / PROFILE_NAME)
    except RuntimeError as error:
        print(f"profile_path.py: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
