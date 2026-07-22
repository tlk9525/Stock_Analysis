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
    day_of_week DOUBLE PRECISION,
    month_of_year DOUBLE PRECISION,
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
    day_of_week DOUBLE PRECISION,
    month_of_year DOUBLE PRECISION,
    target_next_up INTEGER,
    next_return DOUBLE PRECISION,
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

CREATE INDEX IF NOT EXISTS idx_daily_runs_symbol_generated
    ON daily_runs (symbol, generated_at DESC);

CREATE INDEX IF NOT EXISTS idx_history_features_symbol_date
    ON history_features (symbol, trade_date DESC);

CREATE INDEX IF NOT EXISTS idx_forecasts_symbol_date
    ON forecasts (symbol, forecast_date);

CREATE INDEX IF NOT EXISTS idx_fundamental_metrics_symbol_period
    ON fundamental_metrics (symbol, period);

CREATE INDEX IF NOT EXISTS idx_panel_predictions_date_rank
    ON panel_predictions (horizon, trade_date DESC, predicted_rank);

CREATE INDEX IF NOT EXISTS idx_panel_latest_rankings_date_rank
    ON panel_latest_rankings (horizon, as_of_date DESC, predicted_rank);
