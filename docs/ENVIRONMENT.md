# Development Environment

## Preferred setup

Use Ubuntu WSL 2 and keep the repository in the Linux filesystem for better performance with
large ZIP, Parquet, and DuckDB files:

```bash
~/projects/market-backtest
```

Avoid placing the working tree under `/mnt/c/Users/...`.

## Ubuntu prerequisites

The project supports Python 3.10 or newer. Ubuntu 22.04's default Python 3.10 is sufficient.

```bash
sudo apt update
sudo apt install -y git curl unzip python3 python3-pip python3-venv
```

## Create the development environment

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Install the optional UI libraries only when dashboard work begins:

```bash
python -m pip install -e ".[dev,dashboard]"
```

## Current verification commands

```bash
pytest
ruff check .
```

Downloader, conversion, validation, and Streamlit commands will be documented when those
entrypoints exist.

## Data storage

By default, local data is stored under:

```text
data/raw/
data/processed/
data/duckdb/
```

To use another local disk or directory, create a local `.env` file:

```bash
cp .env.example .env
```

Then set an absolute path, or a path relative to the repository root:

```dotenv
MARKET_BACKTEST_DATA_DIR=/home/your-user/market-data
```

The setting can also be exported for a single shell session; process environment values take
precedence over `.env`:

```bash
export MARKET_BACKTEST_DATA_DIR=/home/your-user/market-data
```

Downloaded datasets, local databases, `.env` files, and generated reports are intentionally
ignored by Git.

## Open in VS Code

From the repository root in WSL:

```bash
code .
```
