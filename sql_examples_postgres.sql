-- Chay trong PostgreSQL 18 / stock_db:
-- psql -d stock_db -f sql_examples_postgres.sql

-- 1. Cac lan chay moi nhat
SELECT
    symbol,
    run_id,
    latest_date,
    latest_close,
    rsi14,
    logistic_prob_next_up,
    forecast_p50_end
FROM daily_runs
ORDER BY generated_at DESC
LIMIT 10;

-- 2. So sanh lan chay moi nhat cua moi ma
WITH latest AS (
    SELECT symbol, max(generated_at) AS generated_at
    FROM daily_runs
    GROUP BY symbol
)
SELECT
    d.symbol,
    d.latest_close,
    d.sma20,
    d.sma60,
    d.rsi14,
    d.logistic_prob_next_up,
    d.forecast_prob_end_above_latest
FROM daily_runs d
JOIN latest l
  ON d.symbol = l.symbol
 AND d.generated_at = l.generated_at
ORDER BY d.logistic_prob_next_up DESC;

-- 3. Hai muoi phien gan nhat cua HCM trong run moi nhat
WITH latest_run AS (
    SELECT run_id
    FROM daily_runs
    WHERE symbol = 'HCM'
    ORDER BY generated_at DESC
    LIMIT 1
)
SELECT
    trade_date,
    close,
    volume,
    return_1d,
    sma_20,
    sma_60,
    rsi_14
FROM history_features
WHERE symbol = 'HCM'
  AND run_id = (SELECT run_id FROM latest_run)
ORDER BY trade_date DESC
LIMIT 20;

-- 4. Bang forecast cua HCM trong run moi nhat
WITH latest_run AS (
    SELECT run_id
    FROM daily_runs
    WHERE symbol = 'HCM'
    ORDER BY generated_at DESC
    LIMIT 1
)
SELECT
    forecast_date,
    p10,
    p50,
    p90
FROM forecasts
WHERE symbol = 'HCM'
  AND run_id = (SELECT run_id FROM latest_run)
ORDER BY forecast_date;
