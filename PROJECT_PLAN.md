# market-backtest roadmap

## Purpose and boundaries

`market-backtest` is a local crypto futures market-data, research, and backtesting project.
It collects public historical data, normalizes and validates candles, stores processed data in
Parquet, queries it with DuckDB, resamples it for 15-minute-and-higher strategies, and supports
local strategy review.

The repository does not include live alerting, deployment, private automation, API-key handling
for live trading, or order execution.

## Markets and research workflow

Initial venue instruments:

| Exchange | Market type | Venue-native symbols | Role |
| --- | --- | --- | --- |
| Binance | USD-M futures | `BTCUSDT`, `ETHUSDT` | Long-history research and backtesting |
| OKX | USDT swap | `BTC-USDT-SWAP`, `ETH-USDT-SWAP` | Validation on the intended venue |

Raw candles use the `1m` timeframe. Strategy datasets are resampled locally to `15m`, `30m`,
`1h`, `4h`, and `1d`.

The intended workflow is:

```text
Binance research and backtesting
→ OKX validation
→ visual/manual review
→ optional export of research-only strategy definitions
```

## Stable architecture decisions

```text
Raw exchange data
→ normalized candle schema
→ Parquet storage
→ data validation
→ DuckDB query layer
→ resampling
→ indicators
→ backtesting
→ Streamlit research dashboard
```

- Keep downloaded and generated data local and uncommitted.
- Preserve immutable raw Binance archives and lossless OKX API records.
- Use Polars for internal dataframe operations; use pandas only at interface boundaries.
- Use Parquet for processed datasets and DuckDB for local query access.
- Treat candle timestamps as timezone-aware UTC candle-open times.
- Exclude incomplete/unconfirmed candles from research datasets.
- Preserve the venue ID in `symbol`; use `canonical_symbol` for cross-exchange pairing, such as
  `BTC-USDT`.
- Downloader ranges require an explicit inclusive `--start`; optional `--end` is exclusive and
  defaults to the latest fully closed candle.
- Default the data root to `<repository>/data`; allow `MARKET_BACKTEST_DATA_DIR` to override it.
- Build the first dashboard with Streamlit. Next.js/FastAPI remains a late-game option after the
  pipeline and backtest engine are stable.

## Normalized candle contract

The shared schema will contain:

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

Processed rows are sorted by timestamp. Exact and conflicting duplicate policies, nullable
exchange-field mappings, concrete dtypes, and Parquet partition keys will be locked in the Phase
3 specification before implementation.

## Planning document map

- This roadmap owns project direction, phase order, milestones, and current status.
- [`docs/PROJECT_REQUIREMENTS.md`](docs/PROJECT_REQUIREMENTS.md) owns durable functional,
  data-quality, testing, dashboard, backtesting, and export requirements.
- `docs/phases/PHASE_N_*.md` owns decision-complete implementation and acceptance details for one
  phase.
- [`AGENTS.md`](AGENTS.md) owns coding conventions and repository boundaries.
- [`README.md`](README.md) and [`docs/ENVIRONMENT.md`](docs/ENVIRONMENT.md) advertise only commands
  that currently exist.

Phase specifications must link to the requirements they implement. If a phase intentionally
changes a durable requirement, the requirements document and roadmap must be updated in the same
change so scope cannot drift silently.

## Delivery roadmap

Each phase receives a decision-complete document under `docs/phases/` before its code is written.
Only the active phase specification is expected to contain implementation-level detail. Phase
specifications refine the relevant requirements; they do not silently replace them.

### Phase 0 — Repository setup

Establish packaging, dependency groups, local configuration, accurate documentation, ignore
rules, and test/lint tooling. See [docs/phases/PHASE_0_SETUP.md](docs/phases/PHASE_0_SETUP.md).

### Phase 1 — Binance futures acquisition

Download resumable BTCUSDT and ETHUSDT 1-minute USD-M futures archives for an explicit date
range. The phase specification must settle archive discovery, current-period gap filling,
checksums, retry behavior, atomic writes, and progress metadata against current official Binance
documentation.

### Phase 2 — OKX swap acquisition

Download resumable BTC-USDT-SWAP and ETH-USDT-SWAP 1-minute candles while respecting current
pagination and rate limits. Preserve lossless API records in the raw layer. The phase
specification must settle API availability limits, request metadata, file granularity, retry
behavior, and restart checkpoints against current official OKX documentation.

### Phase 3 — Normalization and Parquet

Parse both raw formats into the shared schema, map native instruments to canonical markets,
normalize UTC timestamps and numeric types, and write deterministic Parquet datasets. Lock
exchange-specific volume mappings, nullable fields, uniqueness rules, and partitioning first.

### Phase 4 — Data validation

Detect missing candles, duplicate or conflicting rows, invalid OHLC relationships, negative
volumes, timestamp misalignment, and incomplete candles. Produce small readable reports without
silently hiding source-data problems.

### Phase 5 — DuckDB query layer

Create local views over processed Parquet and typed helpers for exchange, symbol, timeframe, and
half-open date-range queries. The DuckDB database remains generated local state.

### Phase 6 — Resampling

Build `15m`, `30m`, `1h`, `4h`, and `1d` candles from validated 1-minute inputs. Specify UTC
bucket alignment and missing-source-minute behavior before implementation; partial current
buckets must not enter research datasets.

### Phase 7 — Indicators

Add small exchange-agnostic Polars functions for the initial trend, momentum, volatility, candle,
and volume indicators, with deterministic unit tests.

### Phase 8 — Backtesting engine V1

Support long/short trades, entries and exits, stops, targets, position sizing, fees, slippage,
trade logs, equity curves, and summary metrics. Before coding, specify signal timing, fill timing,
intrabar stop/target precedence, fee application, sizing, and look-ahead protections.

### Phase 9 — Binance-to-OKX validation

Run identical strategy rules on paired canonical markets and compare signals, entries, exits,
wicks, volume conditions, and stop/target outcomes.

### Phase 10 — Streamlit dashboard V1

Provide local market, backtest, signal-review, cross-exchange comparison, and data-health views.
Dashboard code consumes package APIs rather than owning research logic.

### Phase 11 — Strategy research workflow

Make strategy definitions, notes, reproducible inputs, Binance results, OKX validation results,
and manual observations easy to save and review locally. Once the strategy model is stable,
support versioned research-definition exports without adding alerting or execution behavior.

### Phase 12 — Futures-specific datasets

After the candle pipeline is stable, consider funding rates, mark/index price candles, and open
interest. Raw trades, order books, liquidation feeds, and tick data remain lower priority.

### Phase 13 — Advanced backtesting

Consider multi-target exits, trailing/break-even stops, partial closes, risk-based sizing,
walk-forward and out-of-sample testing, and Monte Carlo analysis. Avoid optimizing solely for a
historical equity curve.

### Phase 14 — Optional custom interface

Only after the core system is stable, consider a Next.js/TypeScript frontend with TradingView
Lightweight Charts and a FastAPI backend. Streamlit may remain the development dashboard.

## Outcome milestones

Milestones describe observable capability rather than merely counting completed files.

| Milestone | Completion outcome | Status |
| --- | --- | --- |
| 1. Repository ready | Editable install, configuration, docs, pytest, Ruff, and ignore rules work | Complete |
| 2. Binance acquisition | BTCUSDT and ETHUSDT 1m ranges download idempotently and resume safely | Planned |
| 3. OKX acquisition | Both OKX swap ranges paginate completely, preserve raw records, and resume | Planned |
| 4. Processed data | Both venues normalize to one schema and write deterministic Parquet | Planned |
| 5. Validated query layer | Data-quality reports pass and DuckDB serves bounded ordered queries | Planned |
| 6. Higher timeframes | Validated 15m, 30m, 1h, 4h, and 1d datasets are reproducible | Planned |
| 7. Backtesting V1 | Strategies produce tested trades, PnL, metrics, and equity curves | Planned |
| 8. OKX strategy validation | Equivalent Binance/OKX runs expose exchange-sensitive differences | Planned |
| 9. Dashboard V1 | Local market, backtest, signal, comparison, and health views work | Planned |
| 10. Advanced research | Futures-specific data or advanced simulation is added only after core stability | Deferred |

Detailed acceptance criteria live in [`docs/PROJECT_REQUIREMENTS.md`](docs/PROJECT_REQUIREMENTS.md)
and the corresponding phase specification.

## Testing and data safety

Use small deterministic pytest fixtures created at test runtime. Core tests must not download
large real datasets. Add or update tests for parsing, schema normalization, timestamps,
validation, resampling, indicators, fills, fees, PnL, and metrics as their phases arrive.

Do not commit raw or processed datasets, local databases, `.env` files, logs, or generated reports.

## Current status

Current status: **Phase 0 complete; Phase 1 specification complete; implementation in progress**.

Packaging, configuration, documentation, ignore behavior, editable installation, tests, and lint
checks have passed on Python 3.10. The Phase 1 downloader specification is decision-complete and
the project is now in the Phase 1 implementation stage.
