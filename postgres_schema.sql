CREATE TABLE IF NOT EXISTS daily_runs (
    run_id TEXT NOT NULL,
    symbol TEXT NOT NULL,
    source TEXT NOT NULL,
    generated_at TIMESTAMPTZ NOT NULL,
    report_dir TEXT NOT NULL,
    latest_date DATE,
    latest_close DOUBLE PRECISION,
    sma20 DOUBLE PRECISION,
    sma60 DOUBLE PRECISION,
    rsi14 DOUBLE PRECISION,
    vol20 DOUBLE PRECISION,
    volume20 DOUBLE PRECISION,
    support20 DOUBLE PRECISION,
    resistance20 DOUBLE PRECISION,
    support60 DOUBLE PRECISION,
    resistance60 DOUBLE PRECISION,
    max_drawdown DOUBLE PRECISION,
    var_95_daily DOUBLE PRECISION,
    logistic_prob_next_up DOUBLE PRECISION,
    forecast_sessions INTEGER,
    forecast_p10_end DOUBLE PRECISION,
    forecast_p50_end DOUBLE PRECISION,
    forecast_p90_end DOUBLE PRECISION,
    forecast_prob_end_above_latest DOUBLE PRECISION,
    PRIMARY KEY (run_id, symbol)
);

CREATE TABLE IF NOT EXISTS history_features (
    run_id TEXT NOT NULL,
    symbol TEXT NOT NULL,
    trade_date DATE NOT NULL,
    open DOUBLE PRECISION,
    high DOUBLE PRECISION,
    low DOUBLE PRECISION,
    close DOUBLE PRECISION,
    volume DOUBLE PRECISION,
    return_1d DOUBLE PRECISION,
    return_5d DOUBLE PRECISION,
    return_20d DOUBLE PRECISION,
    sma_5 DOUBLE PRECISION,
    sma_20 DOUBLE PRECISION,
    sma_60 DOUBLE PRECISION,
    ema_12 DOUBLE PRECISION,
    ema_26 DOUBLE PRECISION,
    macd DOUBLE PRECISION,
    rsi_14 DOUBLE PRECISION,
    volatility_20d DOUBLE PRECISION,
    volume_sma_20 DOUBLE PRECISION,
    volume_z_20 DOUBLE PRECISION,
    range_pct DOUBLE PRECISION,
    close_vs_sma20 DOUBLE PRECISION,
    close_vs_sma60 DOUBLE PRECISION,
    target_next_up INTEGER,
    next_return DOUBLE PRECISION,
    PRIMARY KEY (run_id, symbol, trade_date)
);

CREATE TABLE IF NOT EXISTS model_test_predictions (
    run_id TEXT NOT NULL,
    symbol TEXT NOT NULL,
    trade_date DATE NOT NULL,
    open DOUBLE PRECISION,
    high DOUBLE PRECISION,
    low DOUBLE PRECISION,
    close DOUBLE PRECISION,
    volume DOUBLE PRECISION,
    return_1d DOUBLE PRECISION,
    return_5d DOUBLE PRECISION,
    return_20d DOUBLE PRECISION,
    sma_5 DOUBLE PRECISION,
    sma_20 DOUBLE PRECISION,
    sma_60 DOUBLE PRECISION,
    ema_12 DOUBLE PRECISION,
    ema_26 DOUBLE PRECISION,
    macd DOUBLE PRECISION,
    rsi_14 DOUBLE PRECISION,
    volatility_20d DOUBLE PRECISION,
    volume_sma_20 DOUBLE PRECISION,
    volume_z_20 DOUBLE PRECISION,
    range_pct DOUBLE PRECISION,
    close_vs_sma20 DOUBLE PRECISION,
    close_vs_sma60 DOUBLE PRECISION,
    target_next_up INTEGER,
    next_return DOUBLE PRECISION,
    logistic_prediction INTEGER,
    logistic_prob_up DOUBLE PRECISION,
    PRIMARY KEY (run_id, symbol, trade_date)
);

CREATE TABLE IF NOT EXISTS forecasts (
    run_id TEXT NOT NULL,
    symbol TEXT NOT NULL,
    forecast_date DATE NOT NULL,
    p10 DOUBLE PRECISION,
    p25 DOUBLE PRECISION,
    p50 DOUBLE PRECISION,
    p75 DOUBLE PRECISION,
    p90 DOUBLE PRECISION,
    prob_end_above_latest DOUBLE PRECISION,
    latest_close DOUBLE PRECISION,
    PRIMARY KEY (run_id, symbol, forecast_date)
);

CREATE TABLE IF NOT EXISTS model_metrics (
    run_id TEXT NOT NULL,
    symbol TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    metric_json TEXT NOT NULL,
    PRIMARY KEY (run_id, symbol, metric_name)
);

CREATE INDEX IF NOT EXISTS idx_daily_runs_symbol_generated
    ON daily_runs (symbol, generated_at DESC);

CREATE INDEX IF NOT EXISTS idx_history_features_symbol_date
    ON history_features (symbol, trade_date DESC);

CREATE INDEX IF NOT EXISTS idx_forecasts_symbol_date
    ON forecasts (symbol, forecast_date);
