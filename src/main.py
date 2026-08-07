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
    current_levels,
    technical_assessment,
)
from src.forecast.monte_carlo import simulate_forecast
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

    print("Huấn luyện XGBoost và logistic baseline...")
    metrics, scored_test, latest_probabilities, booster = train_models(data, config)

    print("Mô phỏng Monte Carlo...")
    forecast = simulate_forecast(data, config)
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
    forecast.reset_index(names="date").to_csv(
        run_directory / f"forecast_{config['forecast_sessions']}_sessions.csv",
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
    write_json(run_directory / "model_metrics.json", metrics)
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
