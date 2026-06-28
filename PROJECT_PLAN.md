# market-backtest

`market-backtest` is a local market-data, research, and backtesting project focused on crypto futures analysis.

The main purpose of this repo is to collect and organize historical market data from Binance and OKX, convert it into a clean local format, build backtesting tools, and eventually create a custom interface for reviewing candles, testing strategies, and comparing exchange behavior.

This repo is focused only on local market-data research, backtesting, validation, and dashboard development. Live alerting, deployment, and private automation tools are outside the scope of this repository.

---

## 1. Project Goals

The goal of `market-backtest` is to build a complete local research system for crypto futures trading.

The project should eventually support:

* Downloading Binance futures historical market data
* Downloading OKX swap/perpetual historical market data
* Cleaning and normalizing data from both exchanges
* Storing processed data efficiently on the local PC
* Resampling 1-minute candles into higher timeframes
* Comparing Binance and OKX candles
* Running backtests on Binance data
* Validating strategies on OKX data
* Reviewing signals visually
* Building a custom market/backtesting dashboard
* Exporting strategy rules or signal definitions for optional external use

The project is designed around **15-minute and higher timeframe strategies**, not high-frequency trading or tick-level execution.

---

## 2. What This Repo Includes

This repo includes:

```text
market-backtest/
├── historical data downloaders
├── local data processing scripts
├── Binance futures data tools
├── OKX swap data tools
├── data normalization logic
├── Parquet/DuckDB storage
├── backtesting engine
├── indicators
├── strategy experiments
├── local dashboard/interface
└── research notebooks
```

This repo does **not** include:

```text
Live alerting services
Server deployment
Private automation tools
Trade execution systems
Exchange API key management for live trading
Automated futures trading
```

---

## 3. Trading Context

The intended trading venue is **OKX futures/perpetuals**, specifically USDT-margined swap markets such as:

```text
BTC-USDT-SWAP
ETH-USDT-SWAP
```

However, Binance futures historical data will also be collected because Binance provides easier long-term historical data access.

The planned data setup is:

```text
Binance futures data:
- Main long-history research and backtesting dataset

OKX swap data:
- Main validation dataset
- Used to check whether Binance-tested strategies behave similarly on the exchange actually traded
```

This means the workflow is:

```text
Research on Binance
↓
Backtest on Binance
↓
Validate on OKX
↓
Manually review signals
↓
Later export useful strategy configs if needed
```

---

## 4. Target Markets

Initial supported symbols:

### Binance USD-M Futures

```text
BTCUSDT
ETHUSDT
```

### OKX USDT Swap / Perpetual

```text
BTC-USDT-SWAP
ETH-USDT-SWAP
```

Other symbols can be added later, but the first version should stay focused on BTC and ETH only.

---

## 5. Target Timeframes

The raw data should be collected at the smallest practical timeframe needed for flexible research.

Initial raw timeframe:

```text
1m
```

Primary strategy timeframes:

```text
15m
30m
1h
4h
1d
```

The project should download and store 1-minute candles first, then resample locally into higher timeframes.

This allows consistent backtesting and avoids relying on exchange-provided higher-timeframe candles when we can generate them ourselves.

---

## 6. Data Types

### 6.1 Required Candle Data

The first version should focus on OHLCV candle data.

Required normalized fields:

```text
exchange
market_type
symbol
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

Not every exchange will provide every field in the same way.

For example:

### Binance Futures

Binance futures kline data usually includes:

```text
open_time
open
high
low
close
volume
close_time
quote_asset_volume
number_of_trades
taker_buy_base_asset_volume
taker_buy_quote_asset_volume
```

### OKX Swap

OKX candle data includes fields similar to:

```text
timestamp
open
high
low
close
vol
volCcy
volCcyQuote
confirm
```

For OKX derivatives:

```text
vol = contract volume
volCcy = base currency volume
volCcyQuote = quote currency volume
```

The project should normalize these differences into one consistent internal schema.

---

## 7. Optional Future Data Types

After the candle system is stable, the project may add:

```text
funding rates
mark price candles
index price candles
open interest
taker buy/sell pressure
basis between futures and spot
Binance vs OKX price difference
Binance vs OKX wick difference
```

Lower priority data:

```text
raw trades
aggregate trades
order book snapshots
liquidation data
tick-level data
```

Raw tick data should not be added early because it will make the project heavier and more complicated.

---

## 8. Local Storage Strategy

The project should use local PC storage.

Recommended storage format:

```text
Raw downloaded data:
- ZIP
- CSV
- JSON, only if required by API response

Processed data:
- Parquet

Query layer:
- DuckDB
```

Why this setup:

```text
Parquet:
- efficient
- compressed
- good for large historical datasets
- easy to partition by exchange/symbol/timeframe

DuckDB:
- allows SQL queries over local files
- works well with Parquet
- easier than running PostgreSQL locally for research
```

PostgreSQL is not required for this repo unless a future version needs it.

---

## 9. Proposed Folder Structure

```text
market-backtest/
├── app/
│   └── dashboard.py
│
├── data/
│   ├── raw/
│   │   ├── binance/
│   │   │   └── futures_um/
│   │   │       ├── BTCUSDT/
│   │   │       └── ETHUSDT/
│   │   │
│   │   └── okx/
│   │       └── swap/
│   │           ├── BTC-USDT-SWAP/
│   │           └── ETH-USDT-SWAP/
│   │
│   ├── processed/
│   │   └── candles_1m/
│   │
│   └── duckdb/
│       └── market_data.duckdb
│
├── market_backtest/
│   ├── __init__.py
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py
│   │
│   ├── data/
│   │   ├── __init__.py
│   │   ├── schema.py
│   │   ├── loader.py
│   │   ├── writer.py
│   │   ├── resample.py
│   │   └── validation.py
│   │
│   ├── exchanges/
│   │   ├── __init__.py
│   │   ├── binance.py
│   │   └── okx.py
│   │
│   ├── indicators/
│   │   ├── __init__.py
│   │   ├── trend.py
│   │   ├── momentum.py
│   │   ├── volatility.py
│   │   └── volume.py
│   │
│   ├── backtest/
│   │   ├── __init__.py
│   │   ├── engine.py
│   │   ├── position.py
│   │   ├── trade.py
│   │   ├── metrics.py
│   │   └── reports.py
│   │
│   ├── strategies/
│   │   ├── __init__.py
│   │   └── examples/
│   │
│   └── utils/
│       ├── __init__.py
│       ├── time.py
│       ├── paths.py
│       └── logging.py
│
├── notebooks/
│   └── exploratory/
│
├── outputs/
│   ├── reports/
│   ├── charts/
│   └── backtests/
│
├── scripts/
│   ├── download_binance.py
│   ├── download_okx.py
│   ├── convert_to_parquet.py
│   ├── update_all.py
│   ├── resample_candles.py
│   └── validate_data.py
│
├── tests/
│   ├── test_resample.py
│   ├── test_schema.py
│   └── test_backtest_engine.py
│
├── docs/
│   └── ENVIRONMENT.md
│
├── .env.example
├── .gitignore
├── README.md
├── PROJECT_PLAN.md
├── AGENTS.md
└── pyproject.toml
```

---

## 10. Git Ignore Rules

The repo should not commit downloaded market data.

The `data/` folder structure can exist in the repo, but the actual contents should be ignored.

Recommended `.gitignore` rules:

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class

# Virtual environments
.venv/
venv/
env/

# Environment variables
.env
.env.*
!.env.example

# IDE
.vscode/
.idea/

# OS files
.DS_Store
Thumbs.db

# Jupyter
.ipynb_checkpoints/

# Caches
.pytest_cache/
.mypy_cache/
.ruff_cache/

# Build files
build/
dist/
*.egg-info/

# Logs
logs/
*.log

# Market data
data/raw/*
data/processed/*
data/duckdb/*

# Keep folder structure
!data/raw/.gitkeep
!data/raw/binance/.gitkeep
!data/raw/okx/.gitkeep
!data/processed/.gitkeep
!data/duckdb/.gitkeep

# Data file formats
*.csv
*.zip
*.parquet
*.duckdb
*.db
*.sqlite
*.sqlite3

# Generated outputs
outputs/reports/*
outputs/charts/*
outputs/backtests/*

!outputs/reports/.gitkeep
!outputs/charts/.gitkeep
!outputs/backtests/.gitkeep
```

---

## 11. Development Phases

## Phase 0 — Repo Setup

Goal: create the base project structure.

Tasks:

```text
Create repo: market-backtest
Create folder structure
Add .gitignore
Add README.md
Add PROJECT_PLAN.md
Add pyproject.toml
Add .env.example
Create Python virtual environment
Install base dependencies
```

Suggested base dependencies:

```text
pandas
polars
pyarrow
duckdb
requests
python-dotenv
pydantic
pytest
ruff
streamlit
plotly
```

Possible later dependencies:

```text
fastapi
uvicorn
httpx
numpy
ta-lib or pandas-ta
lightweight-charts wrapper, if useful
```

Development environment details are documented in [`docs/ENVIRONMENT.md`](docs/ENVIRONMENT.md).

---

## Phase 1 — Binance Futures Data Downloader

Goal: download Binance USD-M futures historical 1-minute candle data.

Initial symbols:

```text
BTCUSDT
ETHUSDT
```

Initial timeframe:

```text
1m
```

Tasks:

```text
Create Binance downloader script
Download monthly files where available
Download daily files for current/incomplete month if needed
Save raw files under data/raw/binance/futures_um/
Skip files that already exist
Log missing files
Add retry logic
Add checksum support later if needed
```

Expected output structure:

```text
data/raw/binance/futures_um/BTCUSDT/1m/
├── BTCUSDT-1m-2020-01.zip
├── BTCUSDT-1m-2020-02.zip
└── ...

data/raw/binance/futures_um/ETHUSDT/1m/
├── ETHUSDT-1m-2020-01.zip
├── ETHUSDT-1m-2020-02.zip
└── ...
```

Success criteria:

```text
Can download BTCUSDT 1m futures data
Can download ETHUSDT 1m futures data
Does not duplicate files
Can resume after interruption
```

---

## Phase 2 — OKX Swap Data Downloader

Goal: download OKX USDT swap historical candles.

Initial instruments:

```text
BTC-USDT-SWAP
ETH-USDT-SWAP
```

Initial timeframe:

```text
1m
```

Tasks:

```text
Create OKX API client
Create historical candle downloader
Support pagination
Respect API rate limits
Save raw responses or normalized CSV files
Track download progress
Resume from last downloaded timestamp
Handle incomplete candles
```

Expected output structure:

```text
data/raw/okx/swap/BTC-USDT-SWAP/1m/
├── 2023-07.csv
├── 2023-08.csv
└── ...

data/raw/okx/swap/ETH-USDT-SWAP/1m/
├── 2023-07.csv
├── 2023-08.csv
└── ...
```

Success criteria:

```text
Can download OKX BTC-USDT-SWAP 1m candles
Can download OKX ETH-USDT-SWAP 1m candles
Can resume interrupted downloads
Can handle OKX pagination cleanly
Can detect missing ranges
```

---

## Phase 3 — Data Normalization

Goal: convert Binance and OKX raw data into one shared schema.

Normalized candle schema:

```text
exchange
market_type
symbol
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

Example values:

```text
exchange: binance
market_type: futures_um
symbol: BTCUSDT
timeframe: 1m
source: binance_public_data
```

```text
exchange: okx
market_type: swap
symbol: BTC-USDT-SWAP
timeframe: 1m
source: okx_history_candles
```

Tasks:

```text
Write Binance raw parser
Write OKX raw parser
Normalize timestamps to UTC
Normalize numeric types
Normalize symbol names
Handle missing fields
Save output as Parquet
Partition by exchange, market type, symbol, and timeframe
```

Possible processed output structure:

```text
data/processed/candles_1m/
├── exchange=binance/
│   └── market_type=futures_um/
│       ├── symbol=BTCUSDT/
│       └── symbol=ETHUSDT/
│
└── exchange=okx/
    └── market_type=swap/
        ├── symbol=BTC-USDT-SWAP/
        └── symbol=ETH-USDT-SWAP/
```

Success criteria:

```text
Binance and OKX data can be loaded into the same DataFrame shape
All timestamps are UTC
All candles have valid OHLC values
Duplicate candles are removed
Data is saved as Parquet
```

---

## Phase 4 — Data Validation

Goal: verify that downloaded and processed data is reliable.

Validation checks:

```text
Check duplicate timestamps
Check missing candles
Check invalid OHLC values
Check open/high/low/close consistency
Check negative volume
Check timestamp gaps
Check incomplete current candles
Compare row counts against expected candle counts
```

OHLC rules:

```text
high >= open
high >= close
high >= low
low <= open
low <= close
volume >= 0
```

Tasks:

```text
Create validation module
Create validation report
Print missing ranges
Save validation results to outputs/reports/
Add tests for validation logic
```

Success criteria:

```text
Can detect missing candles
Can detect duplicate rows
Can detect bad OHLC values
Can produce a readable validation report
```

---

## Phase 5 — DuckDB Query Layer

Goal: allow fast local SQL queries over processed Parquet data.

Tasks:

```text
Create DuckDB database file
Create views over Parquet datasets
Create helper functions for loading candles
Support filters by exchange, symbol, timeframe, and date range
```

Example query:

```sql
SELECT *
FROM candles
WHERE exchange = 'binance'
  AND symbol = 'BTCUSDT'
  AND timeframe = '1m'
  AND timestamp >= '2024-01-01'
  AND timestamp < '2024-02-01'
ORDER BY timestamp;
```

Success criteria:

```text
Can query Binance candles with SQL
Can query OKX candles with SQL
Can filter by date range
Can load query result into Python
```

---

## Phase 6 — Resampling Engine

Goal: generate higher timeframe candles from 1-minute data.

Target timeframes:

```text
15m
30m
1h
4h
1d
```

Resampling rules:

```text
open = first open
high = max high
low = min low
close = last close
volume = sum volume
number_of_trades = sum number_of_trades
timestamp = start of candle
```

Tasks:

```text
Create resample function
Support multiple timeframes
Save resampled candles as Parquet
Validate resampled output
Compare generated candles with exchange-provided candles if available
```

Success criteria:

```text
Can generate 15m candles from 1m data
Can generate 1h candles from 1m data
Can generate 4h candles from 1m data
Can preserve volume correctly
```

---

## Phase 7 — Indicator System

Goal: add common indicators used for strategy research.

Initial indicators:

```text
Moving averages
EMA
SMA
RSI
ATR
Volume moving average
Volume spike ratio
Candle body size
Wick size
Range percentage
Trend direction
```

Possible later indicators:

```text
MACD
Bollinger Bands
VWAP
Donchian Channels
Market structure swings
Funding-based filters
Open interest filters
```

Tasks:

```text
Create indicator functions
Keep indicators exchange-agnostic
Add unit tests
Allow indicators to be applied to any timeframe
```

Success criteria:

```text
Can apply indicators to Binance candles
Can apply indicators to OKX candles
Can use indicators inside backtests
```

---

## Phase 8 — Backtesting Engine V1

Goal: build a simple but reliable backtesting system.

The first backtesting engine should support:

```text
Long trades
Short trades
Entry rules
Exit rules
Stop loss
Take profit
Position sizing
Fees
Slippage assumption
Trade logs
Equity curve
Basic performance metrics
```

Initial metrics:

```text
total trades
win rate
net profit
average win
average loss
profit factor
max drawdown
return percentage
risk/reward summary
long vs short performance
```

Trade record fields:

```text
trade_id
exchange
symbol
timeframe
side
entry_time
entry_price
exit_time
exit_price
stop_loss
take_profit
quantity
fee
pnl
pnl_percent
exit_reason
strategy_name
```

Tasks:

```text
Create backtest engine
Create trade model
Create position model
Create metrics module
Create simple example strategy
Export trade logs to CSV/Parquet
Export backtest summary to JSON/Markdown
```

Success criteria:

```text
Can run a backtest on Binance BTCUSDT 15m data
Can run a backtest on Binance ETHUSDT 15m data
Can output trade logs
Can output summary metrics
Can plot equity curve
```

---

## Phase 9 — Binance to OKX Strategy Validation

Goal: test whether Binance backtest results still make sense on OKX data.

This phase is important because the actual trading venue is OKX.

Tasks:

```text
Run same strategy on Binance and OKX
Compare signals
Compare entries
Compare exits
Compare wicks
Compare stop loss hits
Compare take profit hits
Compare volume conditions
```

Comparison checks:

```text
Did Binance trigger but OKX did not?
Did OKX trigger but Binance did not?
Did Binance hit stop but OKX did not?
Did OKX hit stop but Binance did not?
Was volume condition different?
Was candle close direction the same?
Were major wicks similar?
```

Success criteria:

```text
Can compare Binance and OKX results side by side
Can identify strategy rules that are too exchange-sensitive
Can decide whether a strategy is robust enough for OKX-based validation
```

---

## Phase 10 — Streamlit Dashboard V1

Goal: create a fast local interface for research.

The first frontend should use:

```text
Streamlit
```

The Streamlit dashboard should include:

```text
Exchange selector
Symbol selector
Timeframe selector
Date range selector
Candlestick chart
Volume chart
Indicator overlays
Backtest runner
Trade table
Backtest summary metrics
Binance vs OKX comparison view
```

Suggested dashboard pages:

```text
1. Market Viewer
2. Backtest Runner
3. Signal Review
4. Binance vs OKX Comparison
5. Data Health Report
```

Success criteria:

```text
Can open local dashboard
Can view BTC and ETH candles
Can switch between Binance and OKX
Can run a basic backtest
Can view trade entries and exits on chart
```

---

## Phase 11 — Strategy Research Workflow

Goal: create a repeatable workflow for strategy development.

Recommended workflow:

```text
1. Choose market
2. Choose timeframe
3. Explore candles
4. Create basic strategy idea
5. Backtest on Binance
6. Review trades visually
7. Modify strategy rules
8. Re-run backtest
9. Validate on OKX
10. Save strategy notes
11. Export useful strategy configs if needed
```

Strategy notes should include:

```text
strategy name
market
timeframe
entry condition
exit condition
risk rules
best market condition
worst market condition
known weaknesses
Binance result
OKX validation result
manual review notes
```

Possible strategy note location:

```text
notebooks/
outputs/reports/
strategies/
```

---

## Phase 12 — Advanced Data Additions

After the core system works, add futures-specific data.

Priority:

```text
funding rates
mark price candles
index price candles
open interest
```

Why these matter:

```text
funding rates:
- useful for perpetual futures sentiment and holding cost

mark price:
- important because futures liquidations and risk systems often depend on mark price

index price:
- useful for comparing traded price against reference price

open interest:
- useful for identifying leverage buildup or position crowding
```

These should be added only after the OHLCV pipeline is stable.

---

## Phase 13 — Advanced Backtesting Features

Possible improvements:

```text
multiple take-profit levels
trailing stop
break-even stop
partial closes
dynamic position sizing
risk-per-trade sizing
compound account growth
session filters
volatility filters
funding filters
open interest filters
walk-forward testing
out-of-sample testing
parameter optimization
Monte Carlo analysis
```

Important rule:

```text
Avoid over-optimizing strategies.
```

The goal is not to find a perfect historical curve. The goal is to find strategy behavior that is robust enough to survive exchange differences and future market conditions.

---

## Phase 14 — Late-Game Custom Frontend

The first dashboard should be Streamlit.

The late-game interface should use:

```text
Next.js
TypeScript
TradingView Lightweight Charts
FastAPI backend
DuckDB/Parquet data layer
```

Possible future structure:

```text
market-backtest/
├── frontend/
│   └── Next.js app
│
├── backend/
│   └── FastAPI app
│
├── market_backtest/
│   └── Python core logic
│
└── data/
```

Possible pages:

```text
/dashboard
/markets
/backtests
/strategies
/signals
/compare
/data-health
/settings
```

Late-game frontend features:

```text
interactive candlestick chart
volume panel
indicator overlays
trade markers
strategy result cards
Binance vs OKX comparison mode
signal replay mode
saved strategy presets
saved date ranges
manual notes per setup
export strategy config
```

The late-game interface should feel like a custom research terminal, not a generic trading app.

---

## 15. External Signal Export

This repository may eventually export strategy rules or signal definitions for use outside the project.

Possible export format:

```text
JSON
YAML
TOML
```

Example:

```json
{
  "strategy_name": "btc_15m_volume_trend_v1",
  "exchange": "okx",
  "symbol": "BTC-USDT-SWAP",
  "timeframe": "15m",
  "conditions": {
    "trend": "close_above_ema_200",
    "volume": "volume_quote_above_2x_average",
    "momentum": "rsi_above_50"
  },
  "signal": {
    "enabled": true,
    "require_candle_close": true
  }
}
```

This repo should only contain research, backtesting, validation, data processing, and dashboard code.

Live alerting, deployment, private automation, and trade execution are outside the scope of this repository.

---

## 16. Testing Plan

Tests should cover:

```text
data parsing
schema normalization
timestamp handling
resampling
indicator calculations
backtest engine logic
trade PnL calculations
fee calculations
validation checks
```

Example test files:

```text
tests/test_schema.py
tests/test_resample.py
tests/test_indicators.py
tests/test_backtest_engine.py
tests/test_metrics.py
```

---

## 17. Coding Style

Recommended style:

```text
Use type hints
Use clear function names
Keep exchange-specific logic inside exchanges/
Keep reusable logic inside market_backtest/
Keep scripts thin
Keep notebooks for experiments only
Do not put important business logic only inside notebooks
```

Formatting/linting tools:

```text
ruff
pytest
```

Optional later:

```text
mypy
pre-commit
```

---

## 18. Example Commands

Create virtual environment:

```bash
python3 -m venv .venv
```

Activate on Ubuntu WSL:

```bash
source .venv/bin/activate
```

Install project:

```bash
pip install -e .
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

Resample candles:

```bash
python scripts/resample_candles.py
```

Run validation:

```bash
python scripts/validate_data.py
```

Run dashboard:

```bash
streamlit run app/dashboard.py
```

Run tests:

```bash
pytest
```

---

## 19. Suggested Milestones

### Milestone 1 — Repo Ready

```text
Folder structure created
.gitignore added
pyproject.toml added
README/PROJECT_PLAN added
Virtual environment working
```

### Milestone 2 — Binance Data Working

```text
Can download Binance BTCUSDT 1m futures data
Can download Binance ETHUSDT 1m futures data
Can save raw files locally
Can resume downloads
```

### Milestone 3 — OKX Data Working

```text
Can download OKX BTC-USDT-SWAP 1m candles
Can download OKX ETH-USDT-SWAP 1m candles
Can handle pagination
Can resume downloads
```

### Milestone 4 — Processed Data Working

```text
Can parse Binance raw files
Can parse OKX raw files
Can normalize to shared schema
Can save Parquet
Can query with DuckDB
```

### Milestone 5 — Resampling Working

```text
Can generate 15m candles
Can generate 1h candles
Can generate 4h candles
Can validate resampled candles
```

### Milestone 6 — Backtesting V1

```text
Can run simple strategy
Can record trades
Can calculate metrics
Can export backtest result
```

### Milestone 7 — Dashboard V1

```text
Can view candles
Can view volume
Can run backtest from UI
Can see entries/exits
Can compare Binance vs OKX
```

### Milestone 8 — Strategy Validation

```text
Can test strategy on Binance
Can test same strategy on OKX
Can compare differences
Can identify exchange-sensitive strategies
```

### Milestone 9 — Advanced Futures Data

```text
Funding rates added
Mark price added
Index price added
Open interest added
```

### Milestone 10 — Late-Game Interface

```text
Next.js frontend created
FastAPI backend created
TradingView Lightweight Charts integrated
Streamlit replaced or kept as dev dashboard
```

---

## 20. Main Design Principles

```text
Keep data local.
Keep raw data separate from processed data.
Use Binance for long historical research.
Use OKX for validation because OKX is the actual trading venue.
Start with 1-minute candles.
Resample locally to 15m+.
Do not overcomplicate early.
Do not add live trading execution to this repo.
Keep live alerting and deployment code separate.
Build simple first, then improve.
```

---

## 21. Current Planned Architecture

```text
market-backtest
│
├── Binance historical futures data
│   └── long-history research and backtesting
│
├── OKX historical swap data
│   └── exchange-specific validation
│
├── Local processing
│   └── normalize, clean, validate, resample
│
├── Local storage
│   └── Parquet + DuckDB
│
├── Backtesting engine
│   └── test strategies on 15m+ candles
│
├── Dashboard
│   ├── Phase 1: Streamlit
│   └── Phase 2: Next.js + FastAPI
│
└── Exported strategy configs
    └── optional external use
```

---

## 22. Project Status

Current stage:

```text
Planning / initial repo setup
```

Next immediate tasks:

```text
1. Create repo folder structure
2. Add .gitignore
3. Add pyproject.toml
4. Add this project plan
5. Build Binance futures downloader
6. Build OKX swap downloader
```

---

## 23. Notes

This project is for research and backtesting only.

Backtest results do not guarantee live trading performance.

Exchange differences matter, especially for:

```text
wicks
volume
funding
mark price
open interest
liquidity
slippage
stop-loss behavior
```

Because actual trading will happen on OKX, any strategy found using Binance data should be validated on OKX before being trusted.
