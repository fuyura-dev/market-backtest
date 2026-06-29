# AGENTS.md

## Project Name

`market-backtest`

## Project Purpose

This repository is a local crypto market-data, research, and backtesting project.

The project focuses on:

* Downloading Binance futures historical data
* Downloading OKX swap/perpetual historical data
* Normalizing exchange data into one shared schema
* Storing processed data locally using Parquet and DuckDB
* Resampling 1-minute candles into higher timeframes
* Building a backtesting engine for 15m+ strategies
* Comparing Binance and OKX behavior
* Building a local dashboard for research and signal review

This repo does **not** include live alerting, deployment, or private automation tools.

---

## Important Project Scope

Do not add live alerting, deployment, private automation, or server-specific code to this repository.

Do not add live trade execution code to this repository.

Do not add exchange API key handling for live trading unless explicitly requested.

This repo is for:

```text
data collection
data cleaning
data validation
local research
backtesting
dashboard/interface
strategy validation
```

This repo is not for:

```text
live alerting
server deployment
private automation tools
automatic trading
live order execution
```

---

## Main Markets

Initial Binance symbols:

```text
BTCUSDT
ETHUSDT
```

Initial OKX instruments:

```text
BTC-USDT-SWAP
ETH-USDT-SWAP
```

Primary raw timeframe:

```text
1m
```

Main strategy timeframes:

```text
15m
30m
1h
4h
1d
```

---

## Architecture

The planned architecture is:

```text
Raw exchange data
↓
Normalized candle schema
↓
Parquet storage
↓
Data validation
↓
DuckDB query layer
↓
Resampling engine
↓
Indicators
↓
Backtesting engine
↓
Dashboard
```

Use Binance futures data for long-history backtesting.

Use OKX swap data for validation because OKX is the actual intended trading venue.

---

## Folder Structure

Expected structure:

```text
market-backtest/
├── app/
├── data/
│   ├── raw/
│   │   ├── binance/
│   │   └── okx/
│   ├── processed/
│   └── duckdb/
├── market_backtest/
│   ├── config/
│   ├── data/
│   ├── exchanges/
│   ├── indicators/
│   ├── backtest/
│   ├── strategies/
│   └── utils/
├── notebooks/
├── outputs/
├── scripts/
├── tests/
├── docs/
│   └── ENVIRONMENT.md
├── .env.example
├── .gitignore
├── README.md
├── PROJECT_PLAN.md
├── AGENTS.md
└── pyproject.toml
```

---

## Data Rules

Do not commit downloaded market data.

Do not commit:

```text
CSV files
ZIP files
Parquet files
DuckDB databases
SQLite databases
large generated outputs
.env files
```

The `data/` folder should exist, but actual market data should stay local.

Use `.gitkeep` files if empty folders need to be preserved.

---

## Preferred Storage

Raw data:

```text
ZIP
CSV
JSON only when required
```

Processed data:

```text
Parquet
```

Query layer:

```text
DuckDB
```

Avoid PostgreSQL for this repo unless explicitly requested later.

---

## Normalized Candle Schema

Use this shared schema when possible:

```text
exchange
market_type
symbol
canonical_symbol
timeframe
timestamp
open
high
low
close
volume_contracts
volume_base
volume_quote
number_of_trades
is_confirmed
source
created_at
```

All timestamps should be UTC.

`symbol` should retain the venue-native instrument ID. `canonical_symbol` should identify
equivalent markets across exchanges, for example `BTC-USDT`.

All processed candle data should be sorted by timestamp.

Duplicate candles should be removed.

---

## Coding Style

Use Python for the core project.

Prefer:

```text
clear function names
type hints
small reusable modules
simple scripts that call reusable package logic
tests for important logic
```

Avoid:

```text
large messy scripts
important logic only inside notebooks
hardcoded absolute paths
committing generated datasets
mixing live alerting or deployment code into this repo
```

---

## Python Package Rules

Reusable code should go inside:

```text
market_backtest/
```

Command scripts should go inside:

```text
scripts/
```

Experimental notebooks should go inside:

```text
notebooks/
```

Generated reports and charts should go inside:

```text
outputs/
```

---

## Commands

Create virtual environment:

```bash
python3 -m venv .venv
```

Activate on Ubuntu WSL:

```bash
source .venv/bin/activate
```

Install editable package:

```bash
python -m pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```

Run lint checks:

```bash
ruff check .
```

Add downloader, conversion, validation, and dashboard commands here only after their entrypoint
files exist.

---

## Environment Notes

For local setup, WSL usage, and development environment commands, read:

```text
docs/ENVIRONMENT.md
```

Assume the preferred development environment is Ubuntu WSL 2.

Prefer Linux/WSL commands in documentation and scripts. Add Windows PowerShell alternatives only when useful.

---

## Testing Expectations

Add or update tests when changing:

```text
data parsing
schema normalization
timestamp logic
resampling
indicator calculations
backtest engine behavior
fee calculations
PnL calculations
validation checks
```

Use `pytest`.

Tests should be small and deterministic.

Do not require large real market datasets for basic tests. Use small sample fixtures.

---

## Dashboard Plan

Phase 1 frontend:

```text
Streamlit
```

Late-game frontend:

```text
Next.js
TypeScript
TradingView Lightweight Charts
FastAPI backend
```

Do not build the Next.js frontend until the data pipeline and backtesting engine are stable.

---

## Backtesting Principles

The backtesting engine should support:

```text
long trades
short trades
entry rules
exit rules
stop loss
take profit
fees
slippage assumptions
trade logs
equity curve
summary metrics
```

Do not assume backtest results guarantee live performance.

Because live trading is intended for OKX, any strategy tested on Binance should later be validated using OKX data.

---

## Implementation Priorities

Current priority order:

```text
1. Repo setup
2. Binance futures downloader
3. OKX swap downloader
4. Data normalization and Parquet output
5. Data validation
6. DuckDB query layer
7. Resampling
8. Indicators
9. Backtesting engine
10. Streamlit dashboard
11. Binance vs OKX comparison
```

Do not jump ahead to live trading, private alert integration, deployment, or a complex frontend unless explicitly requested.

---

## Agent Instructions

When working in this repo:

1. Read `PROJECT_PLAN.md`, `docs/PROJECT_REQUIREMENTS.md`, and the active phase specification in
   `docs/phases/` first.
2. Keep changes aligned with the project phases.
3. Prefer simple, working implementations over over-engineered abstractions.
4. Keep live alerting, deployment, and private automation code out of this repo.
5. Do not commit or generate large data files unless explicitly requested.
6. Update docs when adding important behavior.
7. Add tests for core logic.
8. Keep scripts usable from the command line.
9. Make Windows-friendly commands when possible.
10. Ask before changing the overall architecture.
11. Follow repository collaboration preferences when the user provides them.

Guide mode:
When collaborating in this repository, default to guide mode unless the user explicitly asks for implementation.

Guide mode means:
- do not edit files
- do not write code on the user's behalf
- explain what to change step by step
- suggest file structure, function signatures, and tests
- review code the user writes
- only implement when the user explicitly asks

Personal reference notes such as files under `notes/` are for the repository owner and should
not be treated as project requirements or implementation guidance unless the user explicitly points to them.

---

## Current Stage

Current stage:

```text
Phase 0 complete; Phase 1 specification complete; implementation in progress
```

Next likely tasks:

```text
build the Binance futures downloader
```
