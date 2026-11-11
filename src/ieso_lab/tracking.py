"""Minimal experiment tracker: one row per run in experiments/runs.csv.
Committed to Git, so your model history is versioned with your code."""
from __future__ import annotations

import json
import subprocess
from datetime import datetime

import pandas as pd

from .paths import EXPERIMENTS_FILE


def _git_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], text=True, stderr=subprocess.DEVNULL
        ).strip()
    except Exception:
        return "no-git"


def log_run(module: str, model: str, params: dict, metrics: dict, notes: str = "") -> None:
    row = {
        "time": datetime.now().isoformat(timespec="seconds"),
        "commit": _git_commit(),
        "module": module,
        "model": model,
        "params": json.dumps(params, default=str),
        **{k: round(float(v), 4) for k, v in metrics.items()},
        "notes": notes,
    }
    new = pd.DataFrame([row])
    if EXPERIMENTS_FILE.exists():
        old = pd.read_csv(EXPERIMENTS_FILE, dtype={"module": str})
        new = pd.concat([old, new], ignore_index=True)
    new.to_csv(EXPERIMENTS_FILE, index=False)
    print(f"logged: {model} {metrics}")


def show_runs(module: str | None = None) -> pd.DataFrame:
    if not EXPERIMENTS_FILE.exists():
        return pd.DataFrame()
    df = pd.read_csv(EXPERIMENTS_FILE, dtype={"module": str})
    return df if module is None else df[df["module"] == module]
