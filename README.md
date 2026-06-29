# market-backtest

`market-backtest` is a local crypto futures market-data, research, and backtesting project.
It will collect Binance USD-M futures and OKX swap candles, normalize them into a shared
schema, store processed datasets in Parquet, query them with DuckDB, and support local
strategy research. It does not include live trading, alerting, or deployment code.

## Current status

Phase 1 Binance downloader specification is complete, and implementation is now in progress.

See [PROJECT_PLAN.md](PROJECT_PLAN.md) for the roadmap and
[docs/PROJECT_REQUIREMENTS.md](docs/PROJECT_REQUIREMENTS.md) for durable project requirements.
Completed and active implementation specifications live under [`docs/phases/`](docs/phases/),
starting with [Phase 0](docs/phases/PHASE_0_SETUP.md).

## Setup

The supported baseline is Python 3.10 or newer. Ubuntu WSL 2 is the preferred environment.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Dashboard dependencies are isolated from the core package and can be installed later with:

```bash
python -m pip install -e ".[dev,dashboard]"
```

## Available commands

```bash
pytest
ruff check .
```

## Local data directory

Data defaults to the repository's `data/` directory. To store large datasets elsewhere,
copy `.env.example` to `.env` and set an absolute or repository-relative path:

```dotenv
MARKET_BACKTEST_DATA_DIR=/home/your-user/market-data
```

Downloaded data, processed datasets, local databases, generated outputs, and `.env` files
must remain uncommitted.

## Core conventions

- Polars is the internal dataframe engine; pandas is limited to interface boundaries.
- `symbol` retains the venue-native instrument ID, while `canonical_symbol` identifies an
  equivalent market across exchanges (for example, `BTC-USDT`).
- Candle timestamps represent UTC candle-open times.
- Only confirmed, complete candles belong in research datasets.
- Raw OKX API records remain lossless in the raw layer; normalization happens later.

Detailed WSL setup notes are in [docs/ENVIRONMENT.md](docs/ENVIRONMENT.md).
