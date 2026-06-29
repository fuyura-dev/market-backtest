# Phase 1 — Binance Downloader

Status: specification complete; implementation in progress.

## Goal

Develop a resumable script that downloads raw monthly USD-M futures 1-minute candle archives for
`BTCUSDT` and `ETHUSDT` from Binance Data Collection, stores them locally without modification,
and supports safe reruns.

## Scope

Include:

- supported symbols: `BTCUSDT`, `ETHUSDT`
- supported timeframe: `1m`
- raw monthly archive downloads only
- raw-only output
- checksum or other published integrity checks when Binance exposes them
- no normalization, parsing, Parquet, or DuckDB

## Out of scope

- Binance REST API fallback
- daily archive downloads
- extracting or filtering rows from downloaded archive files
- downloading unpublished current-month data

## CLI contract

- `--symbol` is required and accepts one supported symbol per run.
- `--start` is required and inclusive.
- `--end` is optional and exclusive.
- `--data-dir` is optional.
- `--overwrite` is optional.
- Fail fast on invalid symbols, invalid timestamps, or `--end <= --start`.

## Time rules

- User-facing range boundaries are interpreted in UTC.
- `--start` is inclusive.
- `--end` is exclusive.
- If `--end` is omitted, the requested range extends to the latest closed 1-minute candle.
- Phase 1 does not trim candle rows inside an archive file. It downloads every published monthly
  archive whose covered month overlaps the requested range.
- Because Phase 1 is monthly-archive-only, unpublished current-month data is unavailable. If the
  requested range extends into a month whose monthly archive is not yet published, the downloader
  should download all earlier published months in range and clearly report the unavailable portion.

## Raw storage layout

- Store files beneath `data/raw/binance/futures_um/<symbol>/1m/YYYY/MM/`.
- Preserve Binance monthly archive filenames as published.
- Preserve companion checksum files when available.

## Data source strategy

- Use Binance Data Collection monthly archives only.
- Do not call the Binance REST API in Phase 1.
- Download only published monthly archives that overlap the requested range.

## Idempotency and overwrite behavior

- Reruns must not silently duplicate files.
- By default, skip existing verified files.
- `--overwrite` forces re-download of matching target files.
- Partial or failed downloads must be written atomically so they cannot be mistaken for complete
  files.

## Logging and errors

- Log the symbol, requested date range, archive months examined, files written, and files skipped.
- Report unavailable months that are outside the published monthly archive set.
- Emit clear errors for invalid symbols, bad dates, HTTP failures, checksum failures, and missing
  expected archive files.

## Tests

- argument and date validation
- requested-range-to-month selection
- output path construction
- skip-by-default versus `--overwrite` behavior
- handling of unpublished requested months
- atomic write behavior around failed downloads

## Acceptance criteria

- The script downloads raw Binance monthly `1m` USD-M futures archives for `BTCUSDT` and
  `ETHUSDT`.
- Files are stored under `data/raw/binance/futures_um/<symbol>/1m/YYYY/MM/`.
- Existing verified files are skipped by default, and `--overwrite` forces replacement.
- Reruns do not duplicate valid files.
- Requested ranges that reach unpublished months are reported clearly without corrupting earlier
  successful downloads.
