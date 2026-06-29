# Project Requirements

This document preserves the durable product and engineering requirements for `market-backtest`.
It describes what the finished research system must support without pretending that later-phase
implementation details have already been settled.

The delivery order and current status live in [`PROJECT_PLAN.md`](../PROJECT_PLAN.md). Exact
interfaces, file formats, edge-case policies, and acceptance tests belong in the relevant
`docs/phases/PHASE_N_*.md` specification before that phase is implemented.

## 1. Scope and boundaries

The project must support local:

- Historical market-data collection.
- Data cleaning, normalization, validation, and resampling.
- Parquet storage and DuckDB queries.
- Indicator and strategy research.
- Backtesting and cross-exchange validation.
- Visual signal and trade review.
- Export of research-only strategy definitions.

The project must not contain:

- Live alerts or notification services.
- Server deployment or private automation tooling.
- Live exchange API-key management.
- Automated trading, order submission, or execution.

The system targets strategies using 15-minute and higher candles. It is not intended for
high-frequency, order-book, or tick-level execution research in its initial versions.

## 2. Target markets and timeframes

Initial instruments:

| Exchange | Market type | Venue symbol | Canonical symbol | Primary role |
| --- | --- | --- | --- | --- |
| Binance | USD-M futures | `BTCUSDT` | `BTC-USDT` | Long-history research/backtests |
| Binance | USD-M futures | `ETHUSDT` | `ETH-USDT` | Long-history research/backtests |
| OKX | USDT swap | `BTC-USDT-SWAP` | `BTC-USDT` | Intended-venue validation |
| OKX | USDT swap | `ETH-USDT-SWAP` | `ETH-USDT` | Intended-venue validation |

- Raw candle timeframe: `1m`.
- Initial strategy timeframes: `15m`, `30m`, `1h`, `4h`, and `1d`.
- Higher timeframes must be resampled locally from validated 1-minute candles.
- Initial implementation remains focused on BTC and ETH; adding symbols later must not require
  exchange-specific changes in shared processing or backtesting code.

## 3. Local storage and data safety

The default data root is `<repository>/data`. `MARKET_BACKTEST_DATA_DIR` may point to another
local directory or disk.

Storage roles:

| Layer | Preferred format | Purpose |
| --- | --- | --- |
| Raw Binance | Exchange ZIP/CSV archives | Immutable source material |
| Raw OKX | Lossless JSON-derived API records | Immutable source material and replay |
| Processed | Parquet | Typed, normalized, efficient datasets |
| Query | DuckDB | Local SQL views and research queries |

Raw and processed datasets, DuckDB/SQLite databases, `.env` files, and generated reports must
remain uncommitted. Empty repository folders may be retained with `.gitkeep` files.

Raw data must remain separate from normalized data. A downloader must not silently rewrite or
reinterpret already-preserved source records.

## 4. Historical data acquisition

All downloaders must:

- Accept an explicit inclusive `--start` value.
- Treat optional `--end` as exclusive and default it to the latest fully closed candle.
- Use UTC for user-facing and internal range boundaries.
- Be restartable and idempotent for the same instrument, timeframe, and range.
- Avoid duplicate complete files or records.
- Use bounded retries and readable error reporting.
- Write incomplete downloads atomically so they cannot be mistaken for complete data.
- Report unavailable or missing ranges.
- Never require private trading credentials for public historical data.

### 4.1 Binance USD-M futures

The first Binance downloader must:

- Download BTCUSDT and ETHUSDT 1-minute futures data.
- Use Binance Data Collection monthly public archives in Phase 1.
- Treat unpublished current-month data as unavailable in Phase 1 rather than falling back to daily
  archives or the REST API.
- Skip verified files that already exist and resume after interruption.
- Preserve archives beneath `data/raw/binance/futures_um/<symbol>/1m/`.
- Log missing archives and source-side gaps.
- Support checksum verification when the official archive source exposes checksums.

Phase 1 is successful when both initial symbols can be downloaded for a bounded range, rerunning
does not duplicate valid files, and an interrupted run resumes safely.

### 4.2 OKX USDT swaps

The first OKX downloader must:

- Download BTC-USDT-SWAP and ETH-USDT-SWAP 1-minute historical candles.
- Follow documented pagination and current public rate limits.
- Preserve API records losslessly beneath `data/raw/okx/swap/<instrument>/1m/`.
- Retain enough request/progress metadata to resume without silently creating gaps.
- Distinguish confirmed candles from the current incomplete candle.
- Detect missing ranges after pagination.

The Phase 2 specification must confirm current API retention limits, raw-file granularity,
pagination cursors, and rate-limit behavior against official OKX documentation.

Phase 2 is successful when both initial instruments can be downloaded for a bounded range,
pagination is complete, missing ranges are visible, and interrupted runs resume safely.

## 5. Normalized candle data

The shared candle schema must contain:

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

Schema behavior:

- `symbol` retains the venue-native instrument identifier.
- `canonical_symbol` pairs economically equivalent instruments across exchanges.
- `timestamp` is the timezone-aware UTC candle-open time.
- Numeric OHLCV fields use consistent types chosen in the Phase 3 specification.
- Fields not supplied by an exchange are nullable; they must not be fabricated as zero.
- Processed rows are sorted by timestamp.
- Duplicate handling is deterministic and reports conflicting source rows.
- Incomplete/unconfirmed candles are excluded from research-ready datasets.
- Processed output is partitioned so exchange, market type, symbol, timeframe, and bounded date
  ranges can be read efficiently. Exact partition keys are a Phase 3 decision.

Relevant Binance raw kline values include open/close time, OHLC, volume, quote volume, trade
count, and taker-buy volumes. Relevant OKX values include timestamp, OHLC, `vol`, `volCcy`,
`volCcyQuote`, and `confirm`. For OKX swaps, `vol` represents contracts, `volCcy` base volume,
and `volCcyQuote` quote volume. Binance contract/base-volume semantics must be verified before
the final field mapping is implemented.

Normalization is successful when Binance and OKX datasets share one typed dataframe contract,
timestamps are UTC, native/canonical symbols are correct, invalid rows are not silently accepted,
and deterministic Parquet output can be produced.

## 6. Data validation

Validation must detect and report:

- Duplicate timestamps and conflicting duplicate rows.
- Missing candles and timestamp gaps.
- Misaligned timestamps for the declared timeframe.
- Invalid or non-numeric OHLC values.
- Negative volumes or trade counts.
- Incomplete current candles.
- Unexpected row counts for a bounded range.

At minimum, every candle must satisfy:

```text
high >= open
high >= close
high >= low
low <= open
low <= close
volume values >= 0 when present
number_of_trades >= 0 when present
```

Validation must produce a readable result and identify missing ranges. Reports may be written
under `outputs/reports/`, but generated reports remain uncommitted. Tests must cover valid data,
gaps, duplicates, bad OHLC relationships, negative values, and incomplete candles.

Validation policy must distinguish warnings from errors before Phase 4 implementation; source
problems must not be hidden merely to make a dataset pass.

## 7. DuckDB query layer

The query layer must:

- Query normalized Parquet for both exchanges.
- Filter by exchange, native symbol, canonical symbol, timeframe, and half-open UTC date range.
- Return results ordered by timestamp.
- Expose small reusable Python helpers as well as SQL access.
- Keep the DuckDB database file as generated local state.
- Refresh or recreate views predictably when Parquet partitions change.

## 8. Resampling

Initial target timeframes are `15m`, `30m`, `1h`, `4h`, and `1d`.

Aggregation rules:

```text
open = first open
high = maximum high
low = minimum low
close = last close
volume_contracts = sum when available
volume_base = sum when available
volume_quote = sum when available
number_of_trades = sum when available
timestamp = UTC start of the output candle
is_confirmed = true only when the complete source bucket is confirmed
```

Resampled output must be validated and may be compared with exchange-provided higher-timeframe
candles. The Phase 6 specification must settle bucket alignment, daylight-saving independence,
nullable aggregation, and whether a source-minute gap rejects or flags the output bucket.

## 9. Indicators

Initial indicator support:

- SMA and EMA.
- RSI and ATR.
- Volume moving average and volume-spike ratio.
- Candle body size, upper/lower wick size, and range percentage.
- A small, explicitly defined trend-direction helper.

Possible later indicators:

- MACD and Bollinger Bands.
- VWAP and Donchian Channels.
- Market-structure swings.
- Funding-rate and open-interest filters.

Indicator functions must be exchange-agnostic, work on any supported strategy timeframe, use
Polars internally, document warm-up/null behavior, and have deterministic unit tests.

## 10. Backtesting engine V1

The first backtesting engine must support:

- Long and short trades.
- Explicit entry and exit rules.
- Stop loss and take profit.
- Position sizing.
- Fees and a configurable slippage assumption.
- Trade logs and an equity curve.
- Basic summary and long-versus-short metrics.

Initial metrics:

```text
total trades
win rate
net profit
average win
average loss
profit factor
maximum drawdown
return percentage
risk/reward summary
long versus short performance
```

Minimum trade-record fields:

```text
trade_id
exchange
symbol
canonical_symbol
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

The engine must export trade logs to CSV or Parquet and summaries to a readable structured
format such as JSON or Markdown. The Phase 8 specification must define signal timing, fill
timing, intrabar stop/target precedence, fee application, slippage direction, position-sizing
semantics, and look-ahead protections before implementation.

Backtest results must always be presented as historical simulations, not guarantees of live
performance.

## 11. Binance-to-OKX validation

Equivalent strategies must be runnable on paired canonical markets from both exchanges.
Comparison must make it possible to inspect:

- Signals, entries, exits, and trade outcomes.
- Price and wick differences.
- Stop-loss and take-profit differences.
- Volume-condition differences.
- Candle-close direction and timing differences.
- Cases where one venue triggers and the other does not.

The result should expose exchange-sensitive rules and help determine whether a Binance-researched
strategy remains plausible on OKX.

## 12. Local dashboard

Streamlit is the first dashboard technology. The initial dashboard should provide:

- Exchange, symbol, timeframe, and date-range selectors.
- Candlestick and volume charts.
- Indicator overlays.
- A backtest runner and summary metrics.
- Trade tables and entry/exit markers.
- Binance-versus-OKX comparison.
- Data-health results.

Planned pages:

1. Market Viewer.
2. Backtest Runner.
3. Signal Review.
4. Binance vs OKX Comparison.
5. Data Health Report.

Dashboard components must call reusable package APIs; data, strategy, or backtest logic must not
exist only inside Streamlit callbacks.

## 13. Strategy research workflow

The project should support this repeatable workflow:

1. Select a market and timeframe.
2. Explore and validate candles.
3. Define a strategy idea and risk rules.
4. Backtest on Binance.
5. Review trades visually.
6. Refine and rerun without hiding adverse results.
7. Validate the same rules on OKX.
8. Save reproducible strategy notes and results.

Strategy notes should record the strategy name, market, timeframe, entry/exit conditions, risk
rules, favorable/adverse market conditions, known weaknesses, Binance result, OKX validation
result, and manual-review observations.

## 14. External strategy-definition export

The project may export research definitions for use outside this repository.

- Supported candidate formats: JSON, YAML, or TOML.
- An export may contain strategy identity, venue/native and canonical symbols, timeframe,
  indicator conditions, risk parameters, and whether a closed candle is required.
- Exports must be deterministic, versioned, and validated against an explicit schema when this
  feature is implemented.
- Exporting a definition does not authorize sending an alert, deploying a service, handling live
  credentials, or executing a trade in this repository.

The concrete export schema and compatibility policy are deferred until a strategy model exists.

## 15. Future datasets and advanced features

After the candle pipeline is stable, futures-specific data may be added in this order:

1. Funding rates.
2. Mark-price candles.
3. Index-price candles.
4. Open interest.

Possible later research data includes taker pressure, futures/spot basis, cross-exchange price or
wick differences, aggregate trades, liquidation data, and order-book snapshots. Tick-level data
remains low priority because of its storage and processing cost.

Possible advanced backtesting features include multiple targets, partial closes, trailing and
break-even stops, risk-per-trade sizing, compounding, session/volatility/funding/open-interest
filters, walk-forward testing, out-of-sample testing, parameter exploration, and Monte Carlo
analysis. Robustness is more important than an optimized historical curve.

A custom Next.js/TypeScript frontend with TradingView Lightweight Charts and a FastAPI backend is
optional late-game work. It must not begin before the data pipeline and backtesting engine are
stable.

## 16. Testing requirements

Use pytest with small deterministic fixtures created at test runtime. Basic tests must not depend
on network access or large real datasets.

Coverage must be added as the relevant phase is implemented for:

- Raw Binance and OKX parsing.
- Schema and native/canonical symbol normalization.
- UTC timestamp and range-boundary behavior.
- Duplicate, gap, OHLC, volume, and confirmation validation.
- Resampling and nullable-volume aggregation.
- Indicator calculations and warm-up behavior.
- Backtest entries, exits, stop/target behavior, and look-ahead protection.
- Fee, slippage, PnL, equity, and metric calculations.
- Cross-exchange comparison behavior.
- Configuration and filesystem-path behavior.

Every phase specification must name its unit and integration scenarios and define objective
acceptance criteria.

## 17. Engineering conventions

[`AGENTS.md`](../AGENTS.md) is the canonical coding and repository-policy document. In summary:

- Use typed, small, reusable Python modules under `market_backtest/`.
- Keep command scripts thin and place them under `scripts/`.
- Keep notebooks experimental; important logic must live in the package.
- Keep exchange-specific behavior under `market_backtest/exchanges/`.
- Use Polars internally and pandas only at a justified interface boundary.
- Use Ruff and pytest.
- Avoid hardcoded absolute paths and generated datasets in Git.
- Do not add live trading, deployment, or alerting behavior.

Actual setup and verification commands belong in [`README.md`](../README.md) and
[`docs/ENVIRONMENT.md`](ENVIRONMENT.md). A future command must remain a planned phase interface
until its entrypoint exists and has been tested.
