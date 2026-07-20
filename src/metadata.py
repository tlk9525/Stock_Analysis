from __future__ import annotations

import hashlib
import subprocess
from datetime import datetime, timezone
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

import pandas as pd


TRACKED_PACKAGES = ["vnstock", "pandas", "numpy", "matplotlib", "psycopg", "xgboost"]


def _package_versions() -> dict[str, str | None]:
    result: dict[str, str | None] = {}
    for package in TRACKED_PACKAGES:
        try:
            result[package] = version(package)
        except PackageNotFoundError:
            result[package] = None
    return result


def _git_state(project_root: Path) -> dict:
    def run(*args: str) -> str | None:
        try:
            completed = subprocess.run(
                ["git", *args],
                cwd=project_root,
                check=True,
                capture_output=True,
                text=True,
                timeout=5,
            )
            return completed.stdout.strip()
        except (OSError, subprocess.SubprocessError):
            return None

    status = run("status", "--porcelain")
    return {
        "commit": run("rev-parse", "HEAD"),
        "branch": run("branch", "--show-current"),
        "dirty": bool(status) if status is not None else None,
    }


def _data_fingerprint(frame: pd.DataFrame) -> str:
    columns = [
        column
        for column in ["open", "high", "low", "close", "volume"]
        if column in frame.columns
    ]
    hashed = pd.util.hash_pandas_object(frame[columns], index=True).to_numpy()
    return hashlib.sha256(hashed.tobytes()).hexdigest()


def build_run_metadata(config: dict, frame: pd.DataFrame, project_root: Path) -> dict:
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "symbol": config.get("symbol"),
        "source": config.get("source"),
        "data_start": str(frame.index.min()),
        "data_end": str(frame.index.max()),
        "data_rows": int(len(frame)),
        "data_fingerprint_sha256": _data_fingerprint(frame),
        "git": _git_state(project_root),
        "packages": _package_versions(),
        "execution_timing": "feature dùng dữ liệu đến close[t]; sớm nhất thực thi ở phiên t+1",
    }
