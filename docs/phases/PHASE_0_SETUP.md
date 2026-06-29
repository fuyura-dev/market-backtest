# Phase 0 — Repository Setup

Status: complete.

Related project requirements: scope and boundaries, local storage/data safety, testing, and
engineering conventions in [`docs/PROJECT_REQUIREMENTS.md`](../PROJECT_REQUIREMENTS.md).

## Goal

Provide a reproducible Python 3.10+ project skeleton before exchange or market-data logic is
added. Phase 0 contains no network downloaders, data conversions, or dashboard application.

## Deliverables

- Package metadata and a setuptools build in `pyproject.toml`.
- Core dependencies for Polars, Parquet, DuckDB, HTTP downloads, and `.env` loading.
- Separate `dev` and `dashboard` optional dependency groups.
- Ruff and pytest project configuration.
- A small configuration API for the local data root.
- Accurate README and WSL environment documentation.
- Ignore rules for local configuration, market data, databases, and generated outputs.
- Deterministic package/configuration smoke tests.

## Configuration contract

`market_backtest.config.get_data_dir()` returns the local data root without creating it.

1. `MARKET_BACKTEST_DATA_DIR` from the process environment has highest precedence.
2. When no process value exists, the repository `.env` file is read.
3. When neither provides a non-empty value, `<repository>/data` is returned.
4. Relative configured paths are resolved from the repository root.

No exchange API keys or live-trading configuration belong in this project.

## Dependency policy

- Polars is the internal dataframe engine.
- pandas, Streamlit, and Plotly remain in the `dashboard` extra.
- pytest and Ruff remain in the `dev` extra.
- Phase 0 does not introduce a lockfile; minimum compatible versions are declared in
  `pyproject.toml`.

## Acceptance criteria

```bash
python -m pip install -e ".[dev]"
pytest
ruff check .
```

Additionally:

- `market_backtest` imports successfully on Python 3.10+.
- Default, absolute, and relative data-root behavior is tested.
- `.env.*` files except `.env.example` are ignored.
- Market datasets and generated output files are ignored while `.gitkeep` files remain tracked.
- Documentation advertises only commands backed by files in the repository.

Verified on Ubuntu 22.04 with Python 3.10.12.
