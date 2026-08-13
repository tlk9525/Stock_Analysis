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
    macd DOUBLE PRECISION,
    macd_signal DOUBLE PRECISION,
    macd_hist DOUBLE PRECISION,
    bb_upper20 DOUBLE PRECISION,
    bb_lower20 DOUBLE PRECISION,
    bb_position20 DOUBLE PRECISION,
    atr14 DOUBLE PRECISION,
    atr_pct14 DOUBLE PRECISION,
    adx14 DOUBLE PRECISION,
    stoch_k14 DOUBLE PRECISION,
    volume_ratio20 DOUBLE PRECISION,
    vol20 DOUBLE PRECISION,
    volume20 DOUBLE PRECISION,
    support20 DOUBLE PRECISION,
    resistance20 DOUBLE PRECISION,
    support60 DOUBLE PRECISION,
    resistance60 DOUBLE PRECISION,
    max_drawdown DOUBLE PRECISION,
    var_95_daily DOUBLE PRECISION,
    technical_bias TEXT,
    technical_score INTEGER,
    xgboost_prob_next_up DOUBLE PRECISION,
    logistic_prob_next_up DOUBLE PRECISION,
    forecast_sessions INTEGER,
    forecast_p10_end DOUBLE PRECISION,
    forecast_p50_end DOUBLE PRECISION,
    forecast_p90_end DOUBLE PRECISION,
    forecast_prob_end_above_latest DOUBLE PRECISION,
    risk_stop_loss DOUBLE PRECISION,
    risk_target_1 DOUBLE PRECISION,
    risk_target_2 DOUBLE PRECISION,
    risk_reward_ratio DOUBLE PRECISION,
    risk_position_shares INTEGER,
    risk_position_value_vnd DOUBLE PRECISION,
    signal_status TEXT,
    signal_reasons TEXT,
    validation_scheme TEXT,
    validation_folds INTEGER,
    backtest_total_return DOUBLE PRECISION,
    backtest_sharpe DOUBLE PRECISION,
    backtest_max_drawdown DOUBLE PRECISION,
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
    return_2d DOUBLE PRECISION,
    return_3d DOUBLE PRECISION,
    return_5d DOUBLE PRECISION,
    return_10d DOUBLE PRECISION,
    return_20d DOUBLE PRECISION,
    sma_5 DOUBLE PRECISION,
    sma_20 DOUBLE PRECISION,
    sma_60 DOUBLE PRECISION,
    ema_12 DOUBLE PRECISION,
    ema_26 DOUBLE PRECISION,
    macd DOUBLE PRECISION,
    macd_signal DOUBLE PRECISION,
    macd_hist DOUBLE PRECISION,
    macd_pct DOUBLE PRECISION,
    macd_hist_pct DOUBLE PRECISION,
    rsi_14 DOUBLE PRECISION,
    bb_mid_20 DOUBLE PRECISION,
    bb_std_20 DOUBLE PRECISION,
    bb_upper_20 DOUBLE PRECISION,
    bb_lower_20 DOUBLE PRECISION,
    bb_width_20 DOUBLE PRECISION,
    bb_position_20 DOUBLE PRECISION,
    atr_14 DOUBLE PRECISION,
    atr_pct_14 DOUBLE PRECISION,
    adx_14 DOUBLE PRECISION,
    plus_di_14 DOUBLE PRECISION,
    minus_di_14 DOUBLE PRECISION,
    stoch_k_14 DOUBLE PRECISION,
    stoch_d_3 DOUBLE PRECISION,
    obv DOUBLE PRECISION,
    obv_sma_20 DOUBLE PRECISION,
    volatility_20d DOUBLE PRECISION,
    return_skew_20d DOUBLE PRECISION,
    return_kurtosis_20d DOUBLE PRECISION,
    volume_sma_20 DOUBLE PRECISION,
    volume_z_20 DOUBLE PRECISION,
    volume_ratio_20 DOUBLE PRECISION,
    range_pct DOUBLE PRECISION,
    close_vs_sma20 DOUBLE PRECISION,
    close_vs_sma60 DOUBLE PRECISION,
    market_open DOUBLE PRECISION,
    market_close DOUBLE PRECISION,
    day_of_week DOUBLE PRECISION,
    month_of_year DOUBLE PRECISION,
    target_next_up INTEGER,
    next_return DOUBLE PRECISION,
    target_entry_open_5d DOUBLE PRECISION,
    target_exit_close_5d DOUBLE PRECISION,
    target_return_5d DOUBLE PRECISION,
    target_market_return_5d DOUBLE PRECISION,
    target_excess_return_5d DOUBLE PRECISION,
    swing_execution_open DOUBLE PRECISION,
    swing_execution_close DOUBLE PRECISION,
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
    return_2d DOUBLE PRECISION,
    return_3d DOUBLE PRECISION,
    return_5d DOUBLE PRECISION,
    return_10d DOUBLE PRECISION,
    return_20d DOUBLE PRECISION,
    sma_5 DOUBLE PRECISION,
    sma_20 DOUBLE PRECISION,
    sma_60 DOUBLE PRECISION,
    ema_12 DOUBLE PRECISION,
    ema_26 DOUBLE PRECISION,
    macd DOUBLE PRECISION,
    macd_signal DOUBLE PRECISION,
    macd_hist DOUBLE PRECISION,
    macd_pct DOUBLE PRECISION,
    macd_hist_pct DOUBLE PRECISION,
    rsi_14 DOUBLE PRECISION,
    bb_mid_20 DOUBLE PRECISION,
    bb_std_20 DOUBLE PRECISION,
    bb_upper_20 DOUBLE PRECISION,
    bb_lower_20 DOUBLE PRECISION,
    bb_width_20 DOUBLE PRECISION,
    bb_position_20 DOUBLE PRECISION,
    atr_14 DOUBLE PRECISION,
    atr_pct_14 DOUBLE PRECISION,
    adx_14 DOUBLE PRECISION,
    plus_di_14 DOUBLE PRECISION,
    minus_di_14 DOUBLE PRECISION,
    stoch_k_14 DOUBLE PRECISION,
    stoch_d_3 DOUBLE PRECISION,
    obv DOUBLE PRECISION,
    obv_sma_20 DOUBLE PRECISION,
    volatility_20d DOUBLE PRECISION,
    return_skew_20d DOUBLE PRECISION,
    return_kurtosis_20d DOUBLE PRECISION,
    volume_sma_20 DOUBLE PRECISION,
    volume_z_20 DOUBLE PRECISION,
    volume_ratio_20 DOUBLE PRECISION,
    range_pct DOUBLE PRECISION,
    close_vs_sma20 DOUBLE PRECISION,
    close_vs_sma60 DOUBLE PRECISION,
    market_open DOUBLE PRECISION,
    market_close DOUBLE PRECISION,
    day_of_week DOUBLE PRECISION,
    month_of_year DOUBLE PRECISION,
    target_next_up INTEGER,
    next_return DOUBLE PRECISION,
    target_entry_open_5d DOUBLE PRECISION,
    target_exit_close_5d DOUBLE PRECISION,
    target_return_5d DOUBLE PRECISION,
    target_market_return_5d DOUBLE PRECISION,
    target_excess_return_5d DOUBLE PRECISION,
    swing_execution_open DOUBLE PRECISION,
    swing_execution_close DOUBLE PRECISION,
    xgboost_prediction INTEGER,
    xgboost_prob_up DOUBLE PRECISION,
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

CREATE TABLE IF NOT EXISTS fundamental_metrics (
    run_id TEXT NOT NULL,
    symbol TEXT NOT NULL,
    source TEXT,
    period TEXT,
    metric_name TEXT NOT NULL,
    metric_label TEXT,
    metric_value DOUBLE PRECISION,
    metric_unit TEXT,
    PRIMARY KEY (run_id, symbol, metric_name)
);

-- Raw financial lines are stored separately from summary ratios. ``available_at``
-- stays NULL until an official disclosure timestamp is available, so these rows
-- cannot silently enter a historical point-in-time model.
CREATE TABLE IF NOT EXISTS financial_statement_lines (
    symbol TEXT NOT NULL,
    source TEXT NOT NULL,
    statement_type TEXT NOT NULL,
    period TEXT NOT NULL,
    line_position INTEGER NOT NULL,
    line_item_id TEXT,
    line_item TEXT,
    line_item_en TEXT,
    metric_value DOUBLE PRECISION,
    fetched_at TIMESTAMPTZ NOT NULL,
    available_at TIMESTAMPTZ,
    availability_basis TEXT NOT NULL,
    PRIMARY KEY (symbol, source, statement_type, period, line_position, fetched_at)
);

CREATE TABLE IF NOT EXISTS news_articles (
    article_key TEXT NOT NULL,
    symbol TEXT NOT NULL,
    provider TEXT NOT NULL,
    source_name TEXT,
    source_url TEXT,
    title TEXT,
    content_excerpt TEXT,
    published_at TIMESTAMPTZ,
    available_at TIMESTAMPTZ,
    fetched_at TIMESTAMPTZ NOT NULL,
    availability_basis TEXT NOT NULL,
    event_type TEXT,
    sentiment_score DOUBLE PRECISION,
    sentiment_label TEXT,
    analysis_method TEXT NOT NULL,
    PRIMARY KEY (article_key, symbol)
);

CREATE TABLE IF NOT EXISTS news_entities (
    article_key TEXT NOT NULL,
    symbol TEXT NOT NULL,
    entity_match_method TEXT NOT NULL,
    entity_confidence DOUBLE PRECISION,
    PRIMARY KEY (article_key, symbol)
);

-- Personal portfolio is a transaction ledger. Position values are derived at
-- read time, so stale market values cannot be persisted as account balances.
CREATE TABLE IF NOT EXISTS portfolios (
    portfolio_id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    base_currency TEXT NOT NULL DEFAULT 'VND',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS portfolio_transactions (
    transaction_id BIGSERIAL PRIMARY KEY,
    portfolio_id BIGINT NOT NULL REFERENCES portfolios(portfolio_id) ON DELETE CASCADE,
    symbol TEXT NOT NULL,
    market TEXT NOT NULL DEFAULT 'VN',
    side TEXT NOT NULL CHECK (side IN ('BUY', 'SELL')),
    quantity NUMERIC(20, 6) NOT NULL CHECK (quantity > 0),
    price NUMERIC(20, 6) NOT NULL CHECK (price > 0),
    fee NUMERIC(20, 6) NOT NULL DEFAULT 0 CHECK (fee >= 0),
    currency TEXT NOT NULL DEFAULT 'VND',
    executed_at TIMESTAMPTZ NOT NULL,
    realized_pnl NUMERIC(20, 6),
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS panel_runs (
    run_id TEXT PRIMARY KEY,
    generated_at TIMESTAMPTZ NOT NULL,
    source TEXT,
    benchmark_symbol TEXT NOT NULL,
    symbols_json TEXT NOT NULL,
    horizons_json TEXT NOT NULL,
    model_kind TEXT NOT NULL,
    transaction_cost_bps DOUBLE PRECISION NOT NULL,
    latest_date DATE,
    report_dir TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS panel_predictions (
    run_id TEXT NOT NULL,
    horizon INTEGER NOT NULL,
    trade_date DATE NOT NULL,
    symbol TEXT NOT NULL,
    fold INTEGER,
    prediction DOUBLE PRECISION,
    prediction_score DOUBLE PRECISION,
    predicted_rank DOUBLE PRECISION,
    predicted_percentile DOUBLE PRECISION,
    predicted_excess_return DOUBLE PRECISION,
    actual_excess_return DOUBLE PRECISION,
    actual_return DOUBLE PRECISION,
    actual_market_return DOUBLE PRECISION,
    market_regime TEXT,
    PRIMARY KEY (run_id, horizon, trade_date, symbol)
);

CREATE TABLE IF NOT EXISTS panel_latest_rankings (
    run_id TEXT NOT NULL,
    horizon INTEGER NOT NULL,
    as_of_date DATE NOT NULL,
    symbol TEXT NOT NULL,
    prediction DOUBLE PRECISION,
    prediction_score DOUBLE PRECISION,
    predicted_rank DOUBLE PRECISION,
    predicted_percentile DOUBLE PRECISION,
    predicted_excess_return DOUBLE PRECISION,
    PRIMARY KEY (run_id, horizon, as_of_date, symbol)
);

CREATE TABLE IF NOT EXISTS panel_metrics (
    run_id TEXT NOT NULL,
    horizon INTEGER NOT NULL,
    metric_json TEXT NOT NULL,
    PRIMARY KEY (run_id, horizon)
);

ALTER TABLE daily_runs ADD COLUMN IF NOT EXISTS macd DOUBLE PRECISION;
ALTER TABLE daily_runs ADD COLUMN IF NOT EXISTS macd_signal DOUBLE PRECISION;
ALTER TABLE daily_runs ADD COLUMN IF NOT EXISTS macd_hist DOUBLE PRECISION;
ALTER TABLE daily_runs ADD COLUMN IF NOT EXISTS bb_upper20 DOUBLE PRECISION;
ALTER TABLE daily_runs ADD COLUMN IF NOT EXISTS bb_lower20 DOUBLE PRECISION;
ALTER TABLE daily_runs ADD COLUMN IF NOT EXISTS bb_position20 DOUBLE PRECISION;
ALTER TABLE daily_runs ADD COLUMN IF NOT EXISTS atr14 DOUBLE PRECISION;
ALTER TABLE daily_runs ADD COLUMN IF NOT EXISTS atr_pct14 DOUBLE PRECISION;
ALTER TABLE daily_runs ADD COLUMN IF NOT EXISTS adx14 DOUBLE PRECISION;
ALTER TABLE daily_runs ADD COLUMN IF NOT EXISTS stoch_k14 DOUBLE PRECISION;
ALTER TABLE daily_runs ADD COLUMN IF NOT EXISTS volume_ratio20 DOUBLE PRECISION;
ALTER TABLE daily_runs ADD COLUMN IF NOT EXISTS technical_bias TEXT;
ALTER TABLE daily_runs ADD COLUMN IF NOT EXISTS technical_score INTEGER;
ALTER TABLE daily_runs ADD COLUMN IF NOT EXISTS xgboost_prob_next_up DOUBLE PRECISION;
ALTER TABLE daily_runs ADD COLUMN IF NOT EXISTS risk_stop_loss DOUBLE PRECISION;
ALTER TABLE daily_runs ADD COLUMN IF NOT EXISTS risk_target_1 DOUBLE PRECISION;
ALTER TABLE daily_runs ADD COLUMN IF NOT EXISTS risk_target_2 DOUBLE PRECISION;
ALTER TABLE daily_runs ADD COLUMN IF NOT EXISTS risk_reward_ratio DOUBLE PRECISION;
ALTER TABLE daily_runs ADD COLUMN IF NOT EXISTS risk_position_shares INTEGER;
ALTER TABLE daily_runs ADD COLUMN IF NOT EXISTS risk_position_value_vnd DOUBLE PRECISION;
ALTER TABLE daily_runs ADD COLUMN IF NOT EXISTS signal_status TEXT;
ALTER TABLE daily_runs ADD COLUMN IF NOT EXISTS signal_reasons TEXT;
ALTER TABLE daily_runs ADD COLUMN IF NOT EXISTS validation_scheme TEXT;
ALTER TABLE daily_runs ADD COLUMN IF NOT EXISTS validation_folds INTEGER;
ALTER TABLE daily_runs ADD COLUMN IF NOT EXISTS backtest_total_return DOUBLE PRECISION;
ALTER TABLE daily_runs ADD COLUMN IF NOT EXISTS backtest_sharpe DOUBLE PRECISION;
ALTER TABLE daily_runs ADD COLUMN IF NOT EXISTS backtest_max_drawdown DOUBLE PRECISION;

ALTER TABLE history_features ADD COLUMN IF NOT EXISTS macd_signal DOUBLE PRECISION;
ALTER TABLE history_features ADD COLUMN IF NOT EXISTS macd_hist DOUBLE PRECISION;
ALTER TABLE history_features ADD COLUMN IF NOT EXISTS return_2d DOUBLE PRECISION;
ALTER TABLE history_features ADD COLUMN IF NOT EXISTS return_3d DOUBLE PRECISION;
ALTER TABLE history_features ADD COLUMN IF NOT EXISTS return_10d DOUBLE PRECISION;
ALTER TABLE history_features ADD COLUMN IF NOT EXISTS macd_pct DOUBLE PRECISION;
ALTER TABLE history_features ADD COLUMN IF NOT EXISTS macd_hist_pct DOUBLE PRECISION;
ALTER TABLE history_features ADD COLUMN IF NOT EXISTS bb_mid_20 DOUBLE PRECISION;
ALTER TABLE history_features ADD COLUMN IF NOT EXISTS bb_std_20 DOUBLE PRECISION;
ALTER TABLE history_features ADD COLUMN IF NOT EXISTS bb_upper_20 DOUBLE PRECISION;
ALTER TABLE history_features ADD COLUMN IF NOT EXISTS bb_lower_20 DOUBLE PRECISION;
ALTER TABLE history_features ADD COLUMN IF NOT EXISTS bb_width_20 DOUBLE PRECISION;
ALTER TABLE history_features ADD COLUMN IF NOT EXISTS bb_position_20 DOUBLE PRECISION;
ALTER TABLE history_features ADD COLUMN IF NOT EXISTS atr_14 DOUBLE PRECISION;
ALTER TABLE history_features ADD COLUMN IF NOT EXISTS atr_pct_14 DOUBLE PRECISION;
ALTER TABLE history_features ADD COLUMN IF NOT EXISTS adx_14 DOUBLE PRECISION;
ALTER TABLE history_features ADD COLUMN IF NOT EXISTS plus_di_14 DOUBLE PRECISION;
ALTER TABLE history_features ADD COLUMN IF NOT EXISTS minus_di_14 DOUBLE PRECISION;
ALTER TABLE history_features ADD COLUMN IF NOT EXISTS stoch_k_14 DOUBLE PRECISION;
ALTER TABLE history_features ADD COLUMN IF NOT EXISTS stoch_d_3 DOUBLE PRECISION;
ALTER TABLE history_features ADD COLUMN IF NOT EXISTS obv DOUBLE PRECISION;
ALTER TABLE history_features ADD COLUMN IF NOT EXISTS obv_sma_20 DOUBLE PRECISION;
ALTER TABLE history_features ADD COLUMN IF NOT EXISTS return_skew_20d DOUBLE PRECISION;
ALTER TABLE history_features ADD COLUMN IF NOT EXISTS return_kurtosis_20d DOUBLE PRECISION;
ALTER TABLE history_features ADD COLUMN IF NOT EXISTS volume_ratio_20 DOUBLE PRECISION;
ALTER TABLE history_features ADD COLUMN IF NOT EXISTS day_of_week DOUBLE PRECISION;
ALTER TABLE history_features ADD COLUMN IF NOT EXISTS month_of_year DOUBLE PRECISION;
ALTER TABLE history_features ADD COLUMN IF NOT EXISTS market_open DOUBLE PRECISION;
ALTER TABLE history_features ADD COLUMN IF NOT EXISTS market_close DOUBLE PRECISION;
ALTER TABLE history_features ADD COLUMN IF NOT EXISTS target_entry_open_5d DOUBLE PRECISION;
ALTER TABLE history_features ADD COLUMN IF NOT EXISTS target_exit_close_5d DOUBLE PRECISION;
ALTER TABLE history_features ADD COLUMN IF NOT EXISTS target_return_5d DOUBLE PRECISION;
ALTER TABLE history_features ADD COLUMN IF NOT EXISTS target_market_return_5d DOUBLE PRECISION;
ALTER TABLE history_features ADD COLUMN IF NOT EXISTS target_excess_return_5d DOUBLE PRECISION;
ALTER TABLE history_features ADD COLUMN IF NOT EXISTS swing_execution_open DOUBLE PRECISION;
ALTER TABLE history_features ADD COLUMN IF NOT EXISTS swing_execution_close DOUBLE PRECISION;

ALTER TABLE model_test_predictions ADD COLUMN IF NOT EXISTS macd_signal DOUBLE PRECISION;
ALTER TABLE model_test_predictions ADD COLUMN IF NOT EXISTS macd_hist DOUBLE PRECISION;
ALTER TABLE model_test_predictions ADD COLUMN IF NOT EXISTS return_2d DOUBLE PRECISION;
ALTER TABLE model_test_predictions ADD COLUMN IF NOT EXISTS return_3d DOUBLE PRECISION;
ALTER TABLE model_test_predictions ADD COLUMN IF NOT EXISTS return_10d DOUBLE PRECISION;
ALTER TABLE model_test_predictions ADD COLUMN IF NOT EXISTS macd_pct DOUBLE PRECISION;
ALTER TABLE model_test_predictions ADD COLUMN IF NOT EXISTS macd_hist_pct DOUBLE PRECISION;
ALTER TABLE model_test_predictions ADD COLUMN IF NOT EXISTS bb_mid_20 DOUBLE PRECISION;
ALTER TABLE model_test_predictions ADD COLUMN IF NOT EXISTS bb_std_20 DOUBLE PRECISION;
ALTER TABLE model_test_predictions ADD COLUMN IF NOT EXISTS bb_upper_20 DOUBLE PRECISION;
ALTER TABLE model_test_predictions ADD COLUMN IF NOT EXISTS bb_lower_20 DOUBLE PRECISION;
ALTER TABLE model_test_predictions ADD COLUMN IF NOT EXISTS bb_width_20 DOUBLE PRECISION;
ALTER TABLE model_test_predictions ADD COLUMN IF NOT EXISTS bb_position_20 DOUBLE PRECISION;
ALTER TABLE model_test_predictions ADD COLUMN IF NOT EXISTS atr_14 DOUBLE PRECISION;
ALTER TABLE model_test_predictions ADD COLUMN IF NOT EXISTS atr_pct_14 DOUBLE PRECISION;
ALTER TABLE model_test_predictions ADD COLUMN IF NOT EXISTS adx_14 DOUBLE PRECISION;
ALTER TABLE model_test_predictions ADD COLUMN IF NOT EXISTS plus_di_14 DOUBLE PRECISION;
ALTER TABLE model_test_predictions ADD COLUMN IF NOT EXISTS minus_di_14 DOUBLE PRECISION;
ALTER TABLE model_test_predictions ADD COLUMN IF NOT EXISTS stoch_k_14 DOUBLE PRECISION;
ALTER TABLE model_test_predictions ADD COLUMN IF NOT EXISTS stoch_d_3 DOUBLE PRECISION;
ALTER TABLE model_test_predictions ADD COLUMN IF NOT EXISTS obv DOUBLE PRECISION;
ALTER TABLE model_test_predictions ADD COLUMN IF NOT EXISTS obv_sma_20 DOUBLE PRECISION;
ALTER TABLE model_test_predictions ADD COLUMN IF NOT EXISTS return_skew_20d DOUBLE PRECISION;
ALTER TABLE model_test_predictions ADD COLUMN IF NOT EXISTS return_kurtosis_20d DOUBLE PRECISION;
ALTER TABLE model_test_predictions ADD COLUMN IF NOT EXISTS volume_ratio_20 DOUBLE PRECISION;
ALTER TABLE model_test_predictions ADD COLUMN IF NOT EXISTS day_of_week DOUBLE PRECISION;
ALTER TABLE model_test_predictions ADD COLUMN IF NOT EXISTS month_of_year DOUBLE PRECISION;
ALTER TABLE model_test_predictions ADD COLUMN IF NOT EXISTS xgboost_prediction INTEGER;
ALTER TABLE model_test_predictions ADD COLUMN IF NOT EXISTS xgboost_prob_up DOUBLE PRECISION;
ALTER TABLE model_test_predictions ADD COLUMN IF NOT EXISTS market_open DOUBLE PRECISION;
ALTER TABLE model_test_predictions ADD COLUMN IF NOT EXISTS market_close DOUBLE PRECISION;
ALTER TABLE model_test_predictions ADD COLUMN IF NOT EXISTS target_entry_open_5d DOUBLE PRECISION;
ALTER TABLE model_test_predictions ADD COLUMN IF NOT EXISTS target_exit_close_5d DOUBLE PRECISION;
ALTER TABLE model_test_predictions ADD COLUMN IF NOT EXISTS target_return_5d DOUBLE PRECISION;
ALTER TABLE model_test_predictions ADD COLUMN IF NOT EXISTS target_market_return_5d DOUBLE PRECISION;
ALTER TABLE model_test_predictions ADD COLUMN IF NOT EXISTS target_excess_return_5d DOUBLE PRECISION;
ALTER TABLE model_test_predictions ADD COLUMN IF NOT EXISTS swing_execution_open DOUBLE PRECISION;
ALTER TABLE model_test_predictions ADD COLUMN IF NOT EXISTS swing_execution_close DOUBLE PRECISION;

CREATE INDEX IF NOT EXISTS idx_daily_runs_symbol_generated
    ON daily_runs (symbol, generated_at DESC);

CREATE INDEX IF NOT EXISTS idx_history_features_symbol_date
    ON history_features (symbol, trade_date DESC);

CREATE INDEX IF NOT EXISTS idx_forecasts_symbol_date
    ON forecasts (symbol, forecast_date);

CREATE INDEX IF NOT EXISTS idx_fundamental_metrics_symbol_period
    ON fundamental_metrics (symbol, period);

CREATE INDEX IF NOT EXISTS idx_financial_statement_lines_available
    ON financial_statement_lines (symbol, available_at DESC);

CREATE INDEX IF NOT EXISTS idx_news_articles_available
    ON news_articles (symbol, available_at DESC);

CREATE INDEX IF NOT EXISTS idx_portfolio_transactions_portfolio_time
    ON portfolio_transactions (portfolio_id, executed_at, transaction_id);

CREATE INDEX IF NOT EXISTS idx_panel_predictions_date_rank
    ON panel_predictions (horizon, trade_date DESC, predicted_rank);

CREATE INDEX IF NOT EXISTS idx_panel_latest_rankings_date_rank
    ON panel_latest_rankings (horizon, as_of_date DESC, predicted_rank);
