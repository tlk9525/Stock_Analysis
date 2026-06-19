from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

from src.config import PROJECT_ROOT


SCHEMA_PATH = PROJECT_ROOT / "postgres_schema.sql"


def _clean_value(value):
    if pd.isna(value):
        return None
    if isinstance(value, pd.Timestamp):
        return value.to_pydatetime()
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    return value


def _records(frame: pd.DataFrame) -> list[tuple]:
    return [tuple(_clean_value(value) for value in row) for row in frame.to_numpy()]


def _quote_identifier(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


def _upsert_dataframe(
    connection,
    table: str,
    frame: pd.DataFrame,
    conflict_columns: list[str],
) -> None:
    if frame.empty:
        return
    columns = list(frame.columns)
    column_sql = ", ".join(_quote_identifier(column) for column in columns)
    placeholders = ", ".join(["%s"] * len(columns))
    conflict_sql = ", ".join(_quote_identifier(column) for column in conflict_columns)
    update_columns = [column for column in columns if column not in conflict_columns]
    update_sql = ", ".join(
        f"{_quote_identifier(column)} = EXCLUDED.{_quote_identifier(column)}"
        for column in update_columns
    )
    query = (
        f"INSERT INTO {_quote_identifier(table)} ({column_sql}) VALUES ({placeholders}) "
        f"ON CONFLICT ({conflict_sql}) DO UPDATE SET {update_sql}"
    )
    with connection.cursor() as cursor:
        cursor.executemany(query, _records(frame))


def _ensure_schema(connection) -> None:
    with connection.cursor() as cursor:
        cursor.execute(SCHEMA_PATH.read_text(encoding="utf-8"))


def _frame_with_date(
    frame: pd.DataFrame,
    symbol: str,
    run_id: str,
    date_column: str,
) -> pd.DataFrame:
    out = frame.reset_index()
    out = out.rename(columns={out.columns[0]: date_column})
    out[date_column] = pd.to_datetime(out[date_column]).dt.date
    out.insert(0, "run_id", run_id)
    out.insert(1, "symbol", symbol)
    return out


def save_postgres(
    config: dict,
    run_directory: Path,
    data: pd.DataFrame,
    scored_test: pd.DataFrame,
    forecast: pd.DataFrame,
    metrics: dict,
    levels: dict,
    latest_probabilities: dict,
    technical: dict,
    fundamentals: dict,
    risk_plan: dict,
) -> None:
    try:
        import psycopg
    except ImportError as exc:
        raise RuntimeError("Thieu psycopg. Hay chay ./setup_env.sh") from exc

    database_url = os.environ.get("DATABASE_URL") or config.get("database_url")
    if not database_url:
        raise ValueError("Chua co database_url. Vi du: postgresql:///stock_db")

    symbol = config["symbol"]
    run_id = run_directory.name
    timezone = ZoneInfo(config.get("timezone", "Asia/Ho_Chi_Minh"))
    forecast_end = forecast.iloc[-1]
    daily_runs = pd.DataFrame(
        [
            {
                "run_id": run_id,
                "symbol": symbol,
                "source": config["source"],
                "generated_at": datetime.now(timezone),
                "report_dir": str(run_directory),
                "latest_date": pd.to_datetime(levels["latest_date"]).date(),
                "latest_close": levels["latest_close"],
                "sma20": levels["sma20"],
                "sma60": levels["sma60"],
                "rsi14": levels["rsi14"],
                "macd": levels["macd"],
                "macd_signal": levels["macd_signal"],
                "macd_hist": levels["macd_hist"],
                "bb_upper20": levels["bb_upper20"],
                "bb_lower20": levels["bb_lower20"],
                "bb_position20": levels["bb_position20"],
                "atr14": levels["atr14"],
                "atr_pct14": levels["atr_pct14"],
                "adx14": levels["adx14"],
                "stoch_k14": levels["stoch_k14"],
                "volume_ratio20": levels["volume_ratio20"],
                "vol20": levels["vol20"],
                "volume20": levels["volume20"],
                "support20": levels["support20"],
                "resistance20": levels["resistance20"],
                "support60": levels["support60"],
                "resistance60": levels["resistance60"],
                "max_drawdown": levels["max_drawdown"],
                "var_95_daily": levels["var_95_daily"],
                "technical_bias": technical["bias"],
                "technical_score": technical["score"],
                "xgboost_prob_next_up": latest_probabilities["xgboost"],
                "logistic_prob_next_up": latest_probabilities["logistic_regression"],
                "forecast_sessions": int(config["forecast_sessions"]),
                "forecast_p10_end": float(forecast_end["p10"]),
                "forecast_p50_end": float(forecast_end["p50"]),
                "forecast_p90_end": float(forecast_end["p90"]),
                "forecast_prob_end_above_latest": float(forecast_end["prob_end_above_latest"]),
                "risk_stop_loss": risk_plan["stop_loss"],
                "risk_target_1": risk_plan["target_1"],
                "risk_target_2": risk_plan["target_2"],
                "risk_reward_ratio": risk_plan["reward_risk"],
                "risk_position_shares": risk_plan["position_shares"],
                "risk_position_value_vnd": risk_plan["position_value_vnd"],
            }
        ]
    )
    metric_rows = pd.DataFrame(
        [
            {
                "run_id": run_id,
                "symbol": symbol,
                "metric_name": name,
                "metric_json": json.dumps(value, ensure_ascii=False),
            }
            for name, value in metrics.items()
        ]
    )
    fundamental_rows = pd.DataFrame(
        [
            {
                "run_id": run_id,
                "symbol": symbol,
                "source": fundamentals.get("source"),
                "period": item.get("period"),
                "metric_name": item["metric_name"],
                "metric_label": item["metric_label"],
                "metric_value": item["metric_value"],
                "metric_unit": item["metric_unit"],
            }
            for item in fundamentals.get("metrics", [])
        ]
    )
    history_features = _frame_with_date(data, symbol, run_id, "trade_date")
    test_predictions = _frame_with_date(scored_test, symbol, run_id, "trade_date")
    forecasts = _frame_with_date(forecast, symbol, run_id, "forecast_date")

    with psycopg.connect(database_url) as connection:
        _ensure_schema(connection)
        _upsert_dataframe(connection, "daily_runs", daily_runs, ["run_id", "symbol"])
        _upsert_dataframe(connection, "history_features", history_features, ["run_id", "symbol", "trade_date"])
        _upsert_dataframe(connection, "model_test_predictions", test_predictions, ["run_id", "symbol", "trade_date"])
        _upsert_dataframe(connection, "forecasts", forecasts, ["run_id", "symbol", "forecast_date"])
        _upsert_dataframe(connection, "model_metrics", metric_rows, ["run_id", "symbol", "metric_name"])
        _upsert_dataframe(connection, "fundamental_metrics", fundamental_rows, ["run_id", "symbol", "metric_name"])

