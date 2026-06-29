"""Filesystem configuration for local market data."""

from __future__ import annotations

import os
from collections.abc import Mapping
from pathlib import Path

from dotenv import dotenv_values

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR_ENV_VAR = "MARKET_BACKTEST_DATA_DIR"


def get_data_dir(environ: Mapping[str, str] | None = None) -> Path:
    """Return the configured data directory without creating it.

    Process environment values take precedence over the repository's ``.env`` file.
    Supplying ``environ`` makes configuration deterministic for callers and tests and
    intentionally bypasses ``.env`` loading.
    """
    if environ is None:
        dotenv_config = dotenv_values(PROJECT_ROOT / ".env")
        configured_path = os.environ.get(DATA_DIR_ENV_VAR) or dotenv_config.get(DATA_DIR_ENV_VAR)
    else:
        configured_path = environ.get(DATA_DIR_ENV_VAR)

    if not configured_path:
        return PROJECT_ROOT / "data"

    data_dir = Path(configured_path).expanduser()
    if not data_dir.is_absolute():
        data_dir = PROJECT_ROOT / data_dir

    return data_dir.resolve()
