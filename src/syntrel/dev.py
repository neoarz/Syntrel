from __future__ import annotations

import subprocess
import sys


def _run(*args: str) -> None:
    completed = subprocess.run(
        [sys.executable, "-m", *args],
        check=False,
        capture_output=True,
        text=True,
    )

    print(" ".join(args))

    for stream in (completed.stdout, completed.stderr):
        for line in stream.splitlines():
            print(f"  {line}")

    if completed.returncode != 0:
        raise SystemExit(completed.returncode)


def lint() -> None:
    _run("ruff", "check", ".")
    _run("ty", "check")


def format() -> None:
    _run("ruff", "check", "--fix", ".")
    _run("ruff", "format", ".")


def check() -> None:
    lint()
