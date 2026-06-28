# Development Environment

## Preferred Setup

This project is developed on Windows using Ubuntu WSL 2.

The repo should live inside the WSL Linux filesystem for better performance:

```bash
~/projects/market-backtest
```

Avoid running the project from:

```bash
/mnt/c/Users/<WindowsUser>/...
```

This matters because the project will download and process large market datasets, including ZIP, CSV, Parquet, and DuckDB files.

---

## Repo Location

Recommended location:

```bash
~/projects/market-backtest
```

Check current location:

```bash
pwd
```

Expected result should look like:

```bash
/home/<wsl-user>/projects/market-backtest
```

---

## Ubuntu Packages

Install basic system tools:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git curl unzip python3 python3-pip python3-venv
```

---

## Python Virtual Environment

Create the virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Upgrade pip:

```bash
pip install -U pip
```

Install the project:

```bash
pip install -e .
```

---

## Common Commands

Run tests:

```bash
pytest
```

Run the Streamlit dashboard:

```bash
streamlit run app/dashboard.py
```

Run Binance downloader:

```bash
python scripts/download_binance.py
```

Run OKX downloader:

```bash
python scripts/download_okx.py
```

Convert raw data to Parquet:

```bash
python scripts/convert_to_parquet.py
```

Validate data:

```bash
python scripts/validate_data.py
```

---

## Opening in VS Code

From inside the repo:

```bash
code .
```

This should open VS Code through WSL.

---

## Data Storage

Downloaded market data should stay local and should not be committed to Git.

Local data folders:

```text
data/raw/
data/processed/
data/duckdb/
```

These folders are intentionally ignored by Git except for `.gitkeep` files.
