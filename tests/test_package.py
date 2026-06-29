from pathlib import Path

import market_backtest
from market_backtest.config import DATA_DIR_ENV_VAR, PROJECT_ROOT, get_data_dir


def test_package_imports() -> None:
    assert market_backtest.__doc__


def test_data_dir_defaults_to_repository_data_directory() -> None:
    assert get_data_dir(environ={}) == PROJECT_ROOT / "data"


def test_data_dir_accepts_an_absolute_override(tmp_path: Path) -> None:
    configured_path = tmp_path / "market-data"

    assert get_data_dir(environ={DATA_DIR_ENV_VAR: str(configured_path)}) == configured_path


def test_relative_data_dir_is_resolved_from_repository_root() -> None:
    assert get_data_dir(environ={DATA_DIR_ENV_VAR: "../market-data"}) == (
        PROJECT_ROOT.parent / "market-data"
    ).resolve()
