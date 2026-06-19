from __future__ import annotations

import argparse
import time
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from src.config import PROJECT_ROOT, load_config, resolve_config
from src.data.fetch import fetch_fundamentals, fetch_history
from src.database.postgres import save_postgres
from src.features.technical import add_features, current_levels, technical_assessment
from src.forecast.monte_carlo import simulate_forecast
from src.models.xgboost import train_models
from src.reports.dashboard import (
    make_forecast_chart,
    make_history_chart,
    make_technical_chart,
    write_dashboard,
    write_report,
)
from src.risk.management import build_risk_plan
from src.utils import write_json


def run_once(config: dict) -> Path:
    timezone = ZoneInfo(config.get("timezone", "Asia/Ho_Chi_Minh"))
    run_stamp = datetime.now(timezone).strftime("%Y-%m-%d_%H-%M-%S")
    report_root = PROJECT_ROOT / config.get("report_root", "reports")
    run_directory = report_root / config["symbol"] / run_stamp
    run_directory.mkdir(parents=True, exist_ok=True)

    print(f"[{datetime.now(timezone):%Y-%m-%d %H:%M:%S}] Lay du lieu {config['symbol']}...")
    history = fetch_history(config)

    print("Tinh chi bao ky thuat...")
    data = add_features(history)

    print("Train XGBoost va logistic baseline...")
    metrics, scored_test, latest_probabilities, booster = train_models(data, config)

    print("Mo phong Monte Carlo...")
    forecast = simulate_forecast(data, config)
    levels = current_levels(data)
    technical = technical_assessment(levels)
    risk_plan = build_risk_plan(levels, forecast, config)

    print("Lay phan tich co ban...")
    fundamentals, fundamental_frames = fetch_fundamentals(config)

    data.reset_index().rename(columns={"time": "date"}).to_csv(
        run_directory / "history_features.csv",
        index=False,
    )
    scored_test.reset_index().rename(columns={"time": "date"}).to_csv(
        run_directory / "model_test_predictions.csv",
        index=False,
    )
    forecast.reset_index(names="date").to_csv(
        run_directory / f"forecast_{config['forecast_sessions']}_sessions.csv",
        index=False,
    )
    for name, frame in fundamental_frames.items():
        frame.to_csv(run_directory / f"{name}.csv", index=False)

    booster.save_model(str(run_directory / "xgboost_model.json"))
    write_json(run_directory / "model_metrics.json", metrics)
    write_json(run_directory / "latest_probabilities.json", latest_probabilities)
    write_json(run_directory / "latest_levels.json", levels)
    write_json(run_directory / "technical_assessment.json", technical)
    write_json(run_directory / "risk_plan.json", risk_plan)
    write_json(run_directory / "fundamental_summary.json", fundamentals)

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
        risk_plan,
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
        risk_plan,
        run_directory / "dashboard.html",
    )

    if config.get("save_to_postgres", True):
        print("Luu PostgreSQL...")
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
            risk_plan,
        )

    print(f"Xong. Bao cao nam o: {run_directory}")
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
        print(f"Lan chay tiep theo: {next_run:%Y-%m-%d %H:%M:%S}")
        time.sleep(wait_seconds)
        try:
            run_once(config)
        except Exception as exc:
            print(f"Loi khi chay: {exc}")
            time.sleep(60)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Vietnam stock analysis with XGBoost and Monte Carlo."
    )
    parser.add_argument("symbol", nargs="?", help="Ma co phieu, vi du HCM, FPT, VCB.")
    parser.add_argument("--symbol", dest="symbol_option", help="Ma co phieu, uu tien hon positional symbol.")
    parser.add_argument("--source", help="Nguon vnstock, mac dinh theo config.json.")
    parser.add_argument("--forecast-sessions", type=int, help="So phien muon du bao.")
    parser.add_argument("--run-time", help="Gio chay hang ngay, vi du 15:30.")
    parser.add_argument("--database-url", help="PostgreSQL URL.")
    parser.add_argument("--no-postgres", action="store_true", help="Khong luu PostgreSQL.")
    parser.add_argument("--once", action="store_true", help="Chay mot lan roi dung.")
    parser.add_argument("--loop", action="store_true", help="Chay lap moi ngay.")
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

