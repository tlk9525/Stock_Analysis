from __future__ import annotations

import argparse
import time
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd

from src.config import PROJECT_ROOT, load_config, resolve_config
from src.data.fetch import fetch_fundamentals, fetch_history
from src.data.news import build_asof_news_features, fetch_company_news
from src.database.postgres import save_postgres
from src.features.technical import (
    add_features,
    add_market_features,
    add_swing_target,
    current_levels,
    technical_assessment,
)
from src.forecast.monte_carlo import simulate_forecast
from src.forecast.supervised import train_supervised_forecast
from src.metadata import build_run_metadata
from src.models.xgboost import train_models
from src.reports.dashboard import (
    make_forecast_chart,
    make_history_chart,
    make_technical_chart,
    write_dashboard,
    write_report,
)
from src.risk.management import build_risk_plan
from src.risk.decision import build_signal_decision, enforce_signal_decision
from src.strategy import train_swing_strategy
from src.utils import write_json


def run_once(config: dict) -> Path:
    timezone = ZoneInfo(config.get("timezone", "Asia/Ho_Chi_Minh"))
    run_stamp = datetime.now(timezone).strftime("%Y-%m-%d_%H-%M-%S")
    report_root = PROJECT_ROOT / config.get("report_root", "reports")
    run_directory = report_root / config["symbol"] / run_stamp
    run_directory.mkdir(parents=True, exist_ok=True)

    print(f"[{datetime.now(timezone):%Y-%m-%d %H:%M:%S}] Lấy dữ liệu {config['symbol']}...")
    history = fetch_history(config)
    data_quality = history.attrs.get("data_quality_report", {})

    print("Tính chỉ báo kỹ thuật...")
    data = add_features(history)
    market_options = config.get("market_features", {}) or {}
    if bool(market_options.get("enabled", False)):
        benchmark_symbol = str(
            market_options.get("benchmark_symbol", "VNINDEX")
        ).upper()
        print(f"Lấy benchmark {benchmark_symbol} và tính feature thị trường...")
        benchmark = fetch_history({**config, "symbol": benchmark_symbol})
        data = add_market_features(data, benchmark)

    forecast_model_options = config.get("forecast_model", {}) or {}
    forecast_model_enabled = bool(forecast_model_options.get("enabled", True))
    if forecast_model_enabled:
        if not bool(market_options.get("enabled", False)):
            raise ValueError(
                "forecast_model cần market_features.enabled=true để giữ cùng contract target."
            )
        for horizon in sorted(
            {int(value) for value in forecast_model_options.get("horizons", [5, 10, 20])}
        ):
            data = add_swing_target(data, horizon_sessions=horizon)

    swing_options = config.get("swing_strategy", {}) or {}
    swing_enabled = bool(swing_options.get("enabled", False))
    if swing_enabled:
        if not bool(market_options.get("enabled", False)):
            raise ValueError(
                "swing_strategy cần market_features.enabled=true để học excess return."
            )
        data = add_swing_target(
            data,
            horizon_sessions=int(swing_options.get("horizon_sessions", 5)),
        )

    print("Huấn luyện XGBoost và logistic baseline...")
    metrics, scored_test, latest_probabilities, booster = train_models(data, config)
    swing_metrics = None
    swing_oos = None
    swing_latest = None
    swing_booster = None
    if swing_enabled:
        print("Huấn luyện chiến lược swing excess-return và frozen holdout...")
        swing_metrics, swing_oos, swing_payload, swing_booster = train_swing_strategy(
            data, config
        )
        swing_latest = swing_payload["latest"]
        metrics["swing_strategy"] = swing_metrics
        latest_probabilities["swing_expected_excess_return_5d"] = swing_latest[
            "expected_excess_return_5d"
        ]
        latest_probabilities["swing_entry_margin"] = swing_latest[
            "selected_entry_margin"
        ]
        latest_probabilities["swing_expected_excess_return_5d_lower_bound"] = swing_latest[
            "expected_excess_return_5d_lower_bound"
        ]

    print("Mô phỏng Monte Carlo cho kịch bản rủi ro...")
    monte_carlo_forecast = simulate_forecast(data, config)
    forecast_model_metrics = {
        "available": False,
        "method": "monte_carlo_fallback",
    }
    forecast_models: dict[int, object] = {}
    forecast = monte_carlo_forecast
    if forecast_model_enabled:
        print("Huấn luyện direct quantile forecast 5/10/20D và conformal calibration...")
        try:
            forecast, forecast_model_metrics, forecast_models = train_supervised_forecast(
                data, config
            )
        except Exception as exc:
            forecast_model_metrics = {
                "available": False,
                "method": "monte_carlo_fallback",
                "error": str(exc),
            }
            print(f"Cảnh báo: supervised forecast thất bại, dùng Monte Carlo fallback: {exc}")
    metrics["forecast_model"] = forecast_model_metrics
    levels = current_levels(data)
    technical = technical_assessment(levels)
    risk_plan = build_risk_plan(levels, forecast, config)
    decision = build_signal_decision(
        metrics,
        latest_probabilities,
        technical,
        risk_plan,
        levels["latest_date"],
        config,
    )
    risk_plan = enforce_signal_decision(risk_plan, decision)

    print("Lấy phân tích cơ bản...")
    fundamentals, fundamental_frames = fetch_fundamentals(config)
    print("Lấy và phân tích tin tức (research only)...")
    news, news_articles = fetch_company_news(config)
    latest_cutoff = pd.Timestamp(levels["latest_date"])
    latest_cutoff = latest_cutoff.tz_localize(config.get("timezone", "Asia/Ho_Chi_Minh")) + pd.Timedelta(hours=15)
    news_features = build_asof_news_features(
        news_articles,
        [latest_cutoff],
        lookback_days=int((config.get("news", {}) or {}).get("lookback_days", 5)),
        timezone=config.get("timezone", "Asia/Ho_Chi_Minh"),
    )
    if not news_features.empty:
        news["latest_asof_features"] = news_features.iloc[-1].to_dict()

    data.reset_index().rename(columns={"time": "date"}).to_csv(
        run_directory / "history_features.csv",
        index=False,
    )
    scored_test.reset_index().rename(columns={"time": "date"}).to_csv(
        run_directory / "model_test_predictions.csv",
        index=False,
    )
    backtest_details = scored_test.attrs.get("backtest_details")
    if isinstance(backtest_details, pd.DataFrame) and not backtest_details.empty:
        backtest_details.reset_index().rename(columns={"time": "date"}).to_csv(
            run_directory / "backtest_oos.csv",
            index=False,
        )
    if swing_oos is not None and swing_metrics is not None:
        swing_oos.reset_index().rename(columns={"time": "date"}).to_csv(
            run_directory / "swing_development_oos.csv", index=False
        )
        swing_details = swing_oos.attrs.get("backtest_details")
        if isinstance(swing_details, pd.DataFrame) and not swing_details.empty:
            swing_details.reset_index().rename(columns={"time": "date"}).to_csv(
                run_directory / "swing_development_backtest.csv", index=False
            )
        swing_trades = swing_oos.attrs.get("backtest_trades")
        if isinstance(swing_trades, pd.DataFrame):
            swing_trades.to_csv(run_directory / "swing_development_trades.csv", index=False)
        frozen_scored = swing_payload["frozen_scored"]
        frozen_scored.reset_index().rename(columns={"time": "date"}).to_csv(
            run_directory / "swing_frozen_holdout.csv", index=False
        )
        frozen_details = frozen_scored.attrs.get("backtest_details")
        if isinstance(frozen_details, pd.DataFrame) and not frozen_details.empty:
            frozen_details.reset_index().rename(columns={"time": "date"}).to_csv(
                run_directory / "swing_frozen_backtest.csv", index=False
            )
        frozen_trades = frozen_scored.attrs.get("backtest_trades")
        if isinstance(frozen_trades, pd.DataFrame):
            frozen_trades.to_csv(run_directory / "swing_frozen_trades.csv", index=False)
    forecast.reset_index(names="date").to_csv(
        run_directory / f"forecast_{config['forecast_sessions']}_sessions.csv",
        index=False,
    )
    monte_carlo_forecast.reset_index(names="date").to_csv(
        run_directory / f"monte_carlo_forecast_{config['forecast_sessions']}_sessions.csv",
        index=False,
    )
    for name, frame in fundamental_frames.items():
        frame.to_csv(run_directory / f"{name}.csv", index=False)
    raw_directory = run_directory / "raw"
    raw_fundamental_directory = raw_directory / "financial_statements"
    raw_fundamental_directory.mkdir(parents=True, exist_ok=True)
    for name, frame in fundamental_frames.items():
        frame.to_csv(raw_fundamental_directory / f"{name}.csv", index=False)
    raw_news_directory = raw_directory / "news"
    raw_news_directory.mkdir(parents=True, exist_ok=True)
    news_articles.to_csv(raw_news_directory / "articles.csv", index=False)
    news_articles.to_csv(run_directory / "news_articles.csv", index=False)
    if not news_features.empty:
        news_features.reset_index().to_csv(run_directory / "news_features_latest.csv", index=False)

    booster.save_model(str(run_directory / "xgboost_model.json"))
    if swing_booster is not None:
        swing_booster.save_model(str(run_directory / "xgboost_swing_5d.json"))
    for horizon, forecast_model in forecast_models.items():
        forecast_model.save_model(
            str(run_directory / f"xgboost_quantile_forecast_{horizon}d.json")
        )
    write_json(run_directory / "model_metrics.json", metrics)
    if swing_metrics is not None:
        write_json(run_directory / "swing_model_metrics.json", swing_metrics)
    write_json(
        run_directory / "forecast_model_metrics.json", forecast_model_metrics
    )
    write_json(run_directory / "latest_probabilities.json", latest_probabilities)
    write_json(run_directory / "latest_levels.json", levels)
    write_json(run_directory / "technical_assessment.json", technical)
    write_json(run_directory / "risk_plan.json", risk_plan)
    write_json(run_directory / "signal_decision.json", decision)
    write_json(run_directory / "data_quality_report.json", data_quality)
    write_json(run_directory / "resolved_config.json", config)
    write_json(
        run_directory / "run_metadata.json",
        build_run_metadata(config, history, PROJECT_ROOT),
    )
    write_json(run_directory / "fundamental_summary.json", fundamentals)
    write_json(run_directory / "news_summary.json", news)

    make_history_chart(data, run_directory / "history_chart.png")
    make_forecast_chart(data, forecast, levels, run_directory / "forecast_chart.png")
    make_technical_chart(data, run_directory / "technical_chart.png")
    write_report(
        config,
        data,
        forecast,
        levels,
        metrics,
        latest_probabilities,
        technical,
        fundamentals,
        news,
        risk_plan,
        decision,
        run_directory / "analysis_report.md",
    )
    write_dashboard(
        config,
        data,
        forecast,
        levels,
        metrics,
        latest_probabilities,
        technical,
        fundamentals,
        news,
        risk_plan,
        decision,
        run_directory / "dashboard.html",
    )

    if config.get("save_to_postgres", True):
        print("Lưu PostgreSQL...")
        save_postgres(
            config,
            run_directory,
            data,
            scored_test,
            forecast,
            metrics,
            levels,
            latest_probabilities,
            technical,
            fundamentals,
            fundamental_frames,
            news_articles,
            risk_plan,
            decision,
        )

    print(f"Xong. Báo cáo nằm ở: {run_directory}")
    return run_directory


def seconds_until_next_run(config: dict) -> float:
    timezone = ZoneInfo(config.get("timezone", "Asia/Ho_Chi_Minh"))
    hour, minute = [int(part) for part in config["daily_run_time"].split(":")]
    now = datetime.now(timezone)
    target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if target <= now:
        target += timedelta(days=1)
    return (target - now).total_seconds()


def loop_daily(config: dict) -> None:
    while True:
        wait_seconds = seconds_until_next_run(config)
        timezone = ZoneInfo(config.get("timezone", "Asia/Ho_Chi_Minh"))
        next_run = datetime.now(timezone) + timedelta(seconds=wait_seconds)
        print(f"Lần chạy tiếp theo: {next_run:%Y-%m-%d %H:%M:%S}")
        time.sleep(wait_seconds)
        try:
            run_once(config)
        except Exception as exc:
            print(f"Lỗi khi chạy: {exc}")
            time.sleep(60)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Phân tích cổ phiếu Việt Nam bằng XGBoost và Monte Carlo."
    )
    parser.add_argument("symbol", nargs="?", help="Mã cổ phiếu, ví dụ HCM, FPT, VCB.")
    parser.add_argument("--symbol", dest="symbol_option", help="Mã cổ phiếu, ưu tiên hơn positional symbol.")
    parser.add_argument("--source", help="Nguồn vnstock, mặc định theo config.json.")
    parser.add_argument("--forecast-sessions", type=int, help="Số phiên muốn dự báo.")
    parser.add_argument("--run-time", help="Giờ chạy hằng ngày, ví dụ 15:30.")
    parser.add_argument("--database-url", help="PostgreSQL URL.")
    parser.add_argument("--no-postgres", action="store_true", help="Không lưu PostgreSQL.")
    parser.add_argument("--once", action="store_true", help="Chạy một lần rồi dừng.")
    parser.add_argument("--loop", action="store_true", help="Chạy lặp mỗi ngày.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    config = resolve_config(load_config(), args)
    if args.loop:
        loop_daily(config)
    else:
        run_once(config)


if __name__ == "__main__":
    main()
