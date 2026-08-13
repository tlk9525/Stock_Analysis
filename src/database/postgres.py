from __future__ import annotations

import json
import os
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
from pandas.api.types import (
    is_bool_dtype,
    is_datetime64_any_dtype,
    is_float_dtype,
    is_integer_dtype,
)

from src.config import PROJECT_ROOT
from src.utils import clean_json_value, safe_float


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


def _infer_postgres_type(series: pd.Series) -> str:
    if isinstance(series.dtype, pd.DatetimeTZDtype):
        return "TIMESTAMPTZ"
    if is_datetime64_any_dtype(series):
        return "TIMESTAMP"
    if is_bool_dtype(series):
        return "BOOLEAN"
    if is_integer_dtype(series):
        return "BIGINT"
    if is_float_dtype(series):
        return "DOUBLE PRECISION"

    sample = next(
        (
            value
            for value in series
            if value is not None and not pd.isna(value)
        ),
        None,
    )
    if sample is None:
        return "TEXT"
    if hasattr(sample, "tzinfo") and sample.tzinfo is not None:
        return "TIMESTAMPTZ"
    if hasattr(sample, "hour") and hasattr(sample, "minute"):
        return "TIMESTAMP"
    if hasattr(sample, "year") and hasattr(sample, "month") and hasattr(sample, "day"):
        return "DATE"
    if isinstance(sample, (bool, np.bool_)):
        return "BOOLEAN"
    if isinstance(sample, (int, np.integer)):
        return "BIGINT"
    if isinstance(sample, (float, np.floating)):
        return "DOUBLE PRECISION"
    return "TEXT"


def _missing_column_statements(
    table: str,
    frame: pd.DataFrame,
    existing_columns: set[str],
) -> list[str]:
    statements: list[str] = []
    for column in frame.columns:
        if column in existing_columns:
            continue
        sql_type = _infer_postgres_type(frame[column])
        statements.append(
            f"ALTER TABLE {_quote_identifier(table)} "
            f"ADD COLUMN IF NOT EXISTS {_quote_identifier(column)} {sql_type}"
        )
    return statements


def _ensure_dataframe_columns(connection, table: str, frame: pd.DataFrame) -> None:
    if frame.empty:
        return
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = current_schema()
              AND table_name = %s
            """,
            (table,),
        )
        existing_columns = {row[0] for row in cursor.fetchall()}
        for statement in _missing_column_statements(table, frame, existing_columns):
            cursor.execute(statement)


def _upsert_dataframe(
    connection,
    table: str,
    frame: pd.DataFrame,
    conflict_columns: list[str],
) -> None:
    if frame.empty:
        return
    _ensure_dataframe_columns(connection, table, frame)
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
    if "target_next_up" in out.columns:
        out["target_next_up"] = pd.to_numeric(
            out["target_next_up"], errors="coerce"
        ).astype("Int64")
    return out


def _financial_statement_lines(
    frames: dict[str, pd.DataFrame],
    symbol: str,
    source: str,
    fetched_at: datetime,
) -> pd.DataFrame:
    """Persist every supplied statement line with provenance, not only ratios."""

    rows: list[dict] = []
    period_pattern = re.compile(r"^\d{4}-Q[1-4]$")
    for statement_type in ("income_statement", "balance_sheet", "cash_flow"):
        frame = frames.get(statement_type)
        if frame is None or frame.empty:
            continue
        period_columns = [
            str(column) for column in frame.columns if period_pattern.fullmatch(str(column))
        ]
        for position, (_, row) in enumerate(frame.iterrows()):
            for period in period_columns:
                value = safe_float(row.get(period))
                if value is None:
                    continue
                rows.append(
                    {
                        "symbol": symbol,
                        "source": source,
                        "statement_type": statement_type,
                        "period": period,
                        "line_position": position,
                        "line_item_id": str(row.get("item_id") or ""),
                        "line_item": str(row.get("item") or ""),
                        "line_item_en": str(row.get("item_en") or ""),
                        "metric_value": value,
                        "fetched_at": fetched_at,
                        # Do not manufacture an historical announcement time.
                        "available_at": None,
                        "availability_basis": "unverified_publication_time",
                    }
                )
    return pd.DataFrame(rows)


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
    fundamental_frames: dict[str, pd.DataFrame],
    news_articles: pd.DataFrame,
    risk_plan: dict,
    decision: dict | None = None,
) -> None:
    try:
        import psycopg
    except ImportError as exc:
        raise RuntimeError("Thiếu psycopg. Hãy chạy ./setup_env.sh") from exc

    database_url = os.environ.get("DATABASE_URL") or config.get("database_url")
    if not database_url:
        raise ValueError("Chưa có database_url. Ví dụ: postgresql:///stock_db")

    symbol = config["symbol"]
    run_id = run_directory.name
    timezone = ZoneInfo(config.get("timezone", "Asia/Ho_Chi_Minh"))
    forecast_end = forecast.iloc[-1]
    decision = decision or {}
    validation = metrics.get("validation") or metrics.get("walk_forward", {})
    backtest = metrics.get("backtest", {})
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
                "signal_status": decision.get("status"),
                "signal_reasons": json.dumps(
                    decision.get("reasons", []),
                    ensure_ascii=False,
                ),
                "validation_scheme": validation.get(
                    "scheme", validation.get("layout", "expanding_walk_forward")
                ),
                "validation_folds": validation.get(
                    "fold_count", len(validation.get("folds", []))
                ),
                "backtest_total_return": safe_float(
                    backtest.get("net_total_return", backtest.get("total_return"))
                ),
                "backtest_sharpe": safe_float(
                    backtest.get("sharpe_ratio", backtest.get("sharpe"))
                ),
                "backtest_max_drawdown": safe_float(backtest.get("max_drawdown")),
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
    statement_lines = _financial_statement_lines(
        fundamental_frames,
        symbol=symbol,
        source=str(fundamentals.get("source") or config.get("source", "")),
        fetched_at=datetime.now(timezone),
    )
    news_rows = news_articles.copy()
    if not news_rows.empty:
        news_rows = news_rows[
            [
                "article_key",
                "symbol",
                "provider",
                "source_name",
                "source_url",
                "title",
                "content_excerpt",
                "published_at",
                "available_at",
                "fetched_at",
                "availability_basis",
                "event_type",
                "sentiment_score",
                "sentiment_label",
                "analysis_method",
            ]
        ]
    entity_rows = pd.DataFrame()
    if not news_articles.empty:
        entity_rows = news_articles[
            ["article_key", "symbol", "entity_match_method", "entity_confidence"]
        ].copy()
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
        _upsert_dataframe(
            connection,
            "financial_statement_lines",
            statement_lines,
            ["symbol", "source", "statement_type", "period", "line_position", "fetched_at"],
        )
        _upsert_dataframe(connection, "news_articles", news_rows, ["article_key", "symbol"])
        _upsert_dataframe(connection, "news_entities", entity_rows, ["article_key", "symbol"])


def save_panel_postgres(
    config: dict,
    run_directory: Path,
    artifacts: dict[int, dict],
) -> None:
    """Lưu kết quả panel OOS, ranking mới nhất và metrics vào PostgreSQL."""

    try:
        import psycopg
    except ImportError as exc:
        raise RuntimeError("Thiếu psycopg. Hãy chạy ./setup_env.sh") from exc

    database_url = os.environ.get("DATABASE_URL") or config.get("database_url")
    if not database_url:
        raise ValueError("Chưa có database_url. Ví dụ: postgresql:///stock_db")

    panel_options = config["panel"]
    run_id = run_directory.name
    timezone = ZoneInfo(config.get("timezone", "Asia/Ho_Chi_Minh"))
    latest_dates = [
        result["result"].latest_ranking.index.get_level_values("date").max()
        for result in artifacts.values()
    ]
    panel_run = pd.DataFrame(
        [
            {
                "run_id": run_id,
                "generated_at": datetime.now(timezone),
                "source": config.get("source"),
                "benchmark_symbol": panel_options["benchmark_symbol"],
                "symbols_json": json.dumps(panel_options["symbols"]),
                "horizons_json": json.dumps(panel_options["horizons"]),
                "model_kind": panel_options.get("model_kind", "regression"),
                "transaction_cost_bps": float(
                    panel_options["transaction_cost_bps"]
                ),
                "latest_date": pd.Timestamp(max(latest_dates)).date(),
                "report_dir": str(run_directory),
            }
        ]
    )

    prediction_parts: list[pd.DataFrame] = []
    ranking_parts: list[pd.DataFrame] = []
    metric_rows: list[dict] = []
    for horizon, artifact in sorted(artifacts.items()):
        result = artifact["result"]
        predictions = result.predictions.reset_index().rename(
            columns={"date": "trade_date"}
        )
        predictions["sample"] = "development"
        if not result.frozen_predictions.empty:
            frozen_predictions = result.frozen_predictions.reset_index().rename(
                columns={"date": "trade_date"}
            )
            frozen_predictions["sample"] = "frozen"
            frozen_predictions["fold"] = None
            predictions = pd.concat(
                [predictions, frozen_predictions], ignore_index=True
            )
        predictions.insert(0, "run_id", run_id)
        predictions.insert(1, "horizon", int(horizon))
        prediction_columns = [
            "run_id",
            "horizon",
            "trade_date",
            "symbol",
            "sample",
            "fold",
            "prediction",
            "prediction_score",
            "predicted_rank",
            "predicted_percentile",
            "predicted_excess_return",
            "prediction_haircut",
            "prediction_lower_bound",
            "entry_margin",
            "entry_rule_selected",
            "entry_threshold",
            "expected_net_edge",
            "actual_excess_return",
            "actual_return",
            "actual_market_return",
            "entry_date",
            "exit_date",
            "entry_price",
            "exit_price",
            "market_regime",
        ]
        for column in prediction_columns:
            if column not in predictions:
                predictions[column] = None
        predictions["trade_date"] = pd.to_datetime(
            predictions["trade_date"]
        ).dt.date
        for date_column in ("entry_date", "exit_date"):
            predictions[date_column] = pd.to_datetime(
                predictions[date_column], errors="coerce"
            ).dt.date
        prediction_parts.append(predictions[prediction_columns])

        ranking = result.latest_ranking.reset_index().rename(
            columns={"date": "as_of_date"}
        )
        ranking.insert(0, "run_id", run_id)
        ranking.insert(1, "horizon", int(horizon))
        ranking_columns = [
            "run_id",
            "horizon",
            "as_of_date",
            "symbol",
            "prediction",
            "prediction_score",
            "predicted_rank",
            "predicted_percentile",
            "predicted_excess_return",
            "prediction_haircut",
            "prediction_lower_bound",
            "entry_margin",
            "entry_rule_selected",
            "entry_threshold",
            "expected_net_edge",
            "candidate_decision",
            "decision",
            "publish_gate",
        ]
        for column in ranking_columns:
            if column not in ranking:
                ranking[column] = None
        ranking["as_of_date"] = pd.to_datetime(ranking["as_of_date"]).dt.date
        ranking_parts.append(ranking[ranking_columns])

        payload = {
            "metrics": artifact["metrics"],
            "folds": result.folds.reset_index().to_dict("records"),
            "feature_importance": result.feature_importance,
        }
        metric_rows.append(
            {
                "run_id": run_id,
                "horizon": int(horizon),
                "metric_json": json.dumps(
                    clean_json_value(payload), ensure_ascii=False
                ),
            }
        )

    panel_predictions = pd.concat(prediction_parts, ignore_index=True)
    panel_rankings = pd.concat(ranking_parts, ignore_index=True)
    panel_metrics = pd.DataFrame(metric_rows)

    with psycopg.connect(database_url) as connection:
        _ensure_schema(connection)
        _upsert_dataframe(connection, "panel_runs", panel_run, ["run_id"])
        _upsert_dataframe(
            connection,
            "panel_predictions",
            panel_predictions,
            ["run_id", "horizon", "trade_date", "symbol"],
        )
        _upsert_dataframe(
            connection,
            "panel_latest_rankings",
            panel_rankings,
            ["run_id", "horizon", "as_of_date", "symbol"],
        )
        _upsert_dataframe(
            connection,
            "panel_metrics",
            panel_metrics,
            ["run_id", "horizon"],
        )
