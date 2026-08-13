from __future__ import annotations

import argparse
import copy
from datetime import date, datetime
from pathlib import Path
from typing import Mapping
from zoneinfo import ZoneInfo

import pandas as pd

from src.config import PROJECT_ROOT, load_config
from src.database.postgres import save_panel_postgres
from src.metadata import build_run_metadata
from src.panel.data import load_price_panel
from src.panel.evaluation import evaluate_panel_predictions
from src.panel.features import PANEL_MODEL_FEATURES, add_panel_features
from src.panel.flows import FLOW_MODEL_FEATURES, add_foreign_flow_features, load_foreign_flow
from src.panel.news import NEWS_MODEL_FEATURES, add_panel_news_features, load_news_articles
from src.panel.model import walk_forward_predict
from src.panel.universe import (
    apply_point_in_time_eligibility,
    discover_current_universe,
    load_universe_registry,
    normalize_universe_registry,
    point_in_time_symbols,
)
from src.panel.report import (
    build_panel_publish_guard,
    make_panel_performance_chart,
    write_panel_dashboard,
    write_panel_report,
)
from src.utils import write_json


def _csv_strings(value: str) -> list[str]:
    values = [item.strip().upper() for item in value.split(",") if item.strip()]
    return list(dict.fromkeys(values))


def _csv_integers(value: str) -> list[int]:
    try:
        values = [int(item.strip()) for item in value.split(",") if item.strip()]
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Danh sách horizon phải là số nguyên.") from exc
    if not values or any(item <= 0 for item in values):
        raise argparse.ArgumentTypeError("Horizon phải là số nguyên dương.")
    return list(dict.fromkeys(values))


def resolve_panel_config(config: dict, args: argparse.Namespace) -> dict:
    resolved = copy.deepcopy(config)
    panel = resolved.setdefault("panel", {})
    overrides = {
        "symbols": args.symbols,
        "benchmark_symbol": args.benchmark,
        "horizons": args.horizons,
        "top_k": args.top_k,
        "max_positions": getattr(args, "max_positions", None),
        "min_train_dates": args.min_train_dates,
        "validation_dates": args.validation_dates,
        "test_dates": args.test_dates,
        "step_dates": args.step_dates,
        "max_folds": args.max_folds,
        "min_symbols_per_date": args.min_symbols_per_date,
        "model_kind": args.model_kind,
        "transaction_cost_bps": args.transaction_cost_bps,
    }
    for name, value in overrides.items():
        if value is not None:
            panel[name] = value
    if args.source:
        resolved["source"] = args.source.strip().upper()
    if args.start_date:
        resolved["start_date"] = args.start_date
    if args.end_date:
        resolved["end_date"] = args.end_date
    if args.database_url:
        resolved["database_url"] = args.database_url
    if args.no_postgres:
        resolved["save_to_postgres"] = False
    universe_mode = getattr(args, "universe", None)
    if universe_mode:
        panel["universe_mode"] = universe_mode
    universe_csv = getattr(args, "universe_csv", None)
    if universe_csv:
        panel["universe_csv"] = str(universe_csv)
    exchanges = getattr(args, "exchanges", None)
    if exchanges:
        panel["exchanges"] = exchanges
    max_symbols = getattr(args, "max_symbols", None)
    if max_symbols is not None:
        panel["max_symbols"] = int(max_symbols)
    flow_csv = getattr(args, "foreign_flow_csv", None)
    if flow_csv:
        panel.setdefault("foreign_flow", {})["csv"] = str(flow_csv)
        panel["foreign_flow"]["enabled"] = True
    news_model = panel.setdefault("news_model", {})
    news_path = getattr(args, "news_articles_csv", None)
    use_news = bool(getattr(args, "use_news", False))
    if news_path:
        news_model["articles_csv"] = str(news_path)
        news_model["enabled"] = True
    elif use_news:
        news_model["enabled"] = True

    required = [
        "symbols",
        "benchmark_symbol",
        "horizons",
        "top_k",
        "min_train_dates",
        "validation_dates",
        "test_dates",
        "step_dates",
        "max_folds",
        "min_symbols_per_date",
        "model_kind",
        "transaction_cost_bps",
    ]
    missing = [name for name in required if panel.get(name) in (None, "", [])]
    if missing:
        raise ValueError(f"Cấu hình panel thiếu: {', '.join(missing)}")
    panel["symbols"] = (
        _csv_strings(panel["symbols"])
        if isinstance(panel["symbols"], str)
        else list(
            dict.fromkeys(
                str(item).strip().upper()
                for item in panel["symbols"]
                if str(item).strip()
            )
        )
    )
    panel["benchmark_symbol"] = str(panel["benchmark_symbol"]).strip().upper()
    panel["max_positions"] = int(panel.get("max_positions", panel["top_k"]))
    panel["top_k"] = panel["max_positions"]
    panel["horizons"] = (
        _csv_integers(panel["horizons"])
        if isinstance(panel["horizons"], str)
        else list(dict.fromkeys(int(item) for item in panel["horizons"]))
    )
    if any(horizon <= 0 for horizon in panel["horizons"]):
        raise ValueError("Mọi horizon phải là số nguyên dương.")
    minimum_holding = int(panel.get("minimum_holding_sessions", 2))
    if minimum_holding < 2:
        raise ValueError("minimum_holding_sessions phải >= 2 để tôn trọng T+2.")
    if any(horizon < minimum_holding for horizon in panel["horizons"]):
        raise ValueError("Mọi horizon phải >= minimum_holding_sessions.")
    if len(panel["symbols"]) < int(panel["min_symbols_per_date"]):
        raise ValueError("Số mã trong universe nhỏ hơn min_symbols_per_date.")
    if int(panel["top_k"]) > int(panel["min_symbols_per_date"]):
        raise ValueError("max_positions không được lớn hơn min_symbols_per_date.")
    if int(panel["step_dates"]) < int(panel["test_dates"]):
        raise ValueError("step_dates phải lớn hơn hoặc bằng test_dates.")
    if float(panel["transaction_cost_bps"]) < 0:
        raise ValueError("transaction_cost_bps không được âm.")
    margins = [float(value) for value in panel.get("entry_margin_candidates", [0.0])]
    if not margins or any(value < 0 for value in margins):
        raise ValueError("entry_margin_candidates phải có số không âm.")
    panel["entry_margin_candidates"] = margins
    if int(panel.get("minimum_validation_trades", 1)) < 1:
        raise ValueError("minimum_validation_trades phải >= 1.")
    if int(panel.get("cooldown_cohorts", 0)) < 0:
        raise ValueError("cooldown_cohorts không được âm.")
    if int(panel.get("frozen_holdout_dates", 0)) < 0:
        raise ValueError("frozen_holdout_dates không được âm.")
    confidence = float(panel.get("lower_confidence_level", 0.80))
    if not 0.5 <= confidence < 1.0:
        raise ValueError("lower_confidence_level phải thuộc [0.5, 1.0).")
    return resolved


def _resolve_universe(config: dict, *, injected: bool = False) -> tuple[list[str], pd.DataFrame, dict]:
    panel = config["panel"]
    mode = str(panel.get("universe_mode", "configured")).lower()
    if injected or mode == "configured":
        registry = pd.DataFrame(
            {
                "symbol": panel["symbols"],
                "available_at": pd.Timestamp.now(tz="UTC"),
                "source": config.get("source", "VCI"),
                "status": "active",
            }
        )
        registry = normalize_universe_registry(registry)
        return panel["symbols"], registry, {
            "mode": "configured",
            "symbols": len(registry),
            "survivorship_complete": False,
            "point_in_time_complete": False,
        }
    path = panel.get("universe_csv")
    if path:
        registry_path = Path(path)
        if not registry_path.is_absolute():
            registry_path = PROJECT_ROOT / registry_path
        registry = load_universe_registry(registry_path)
        symbols = point_in_time_symbols(
            registry,
            config.get("end_date", str(date.today())),
            exchanges=panel.get("exchanges", ["HOSE", "HNX", "UPCOM"]),
        )
        metadata = {
            "mode": "point_in_time_csv",
            "source": str(registry_path),
            "symbols": len(symbols),
            "survivorship_complete": bool(panel.get("survivorship_complete", False)),
            "point_in_time_complete": True,
        }
    elif mode in {"all-vietnam", "all_vietnam", "current-market", "current_market"}:
        registry, metadata = discover_current_universe(
            source=config.get("source", "VCI"),
            exchanges=panel.get("exchanges", ["HOSE", "HNX", "UPCOM"]),
        )
        symbols = registry["symbol"].tolist()
    else:
        raise ValueError(f"universe_mode không hỗ trợ: {mode}")
    maximum = panel.get("max_symbols")
    if maximum:
        symbols = symbols[: int(maximum)]
        registry = registry[registry["symbol"].isin(symbols)].copy()
        metadata["truncated_to"] = int(maximum)
    if len(symbols) < int(panel["min_symbols_per_date"]):
        raise ValueError("Universe sau lọc nhỏ hơn min_symbols_per_date.")
    return symbols, registry, metadata


def run_panel_once(
    config: dict,
    *,
    frames: Mapping[str, pd.DataFrame] | None = None,
) -> Path:
    panel_options = config["panel"]
    timezone = ZoneInfo(config.get("timezone", "Asia/Ho_Chi_Minh"))
    stamp = datetime.now(timezone).strftime("%Y-%m-%d_%H-%M-%S")
    run_directory = (
        PROJECT_ROOT / config.get("report_root", "reports") / "PANEL" / stamp
    )
    run_directory.mkdir(parents=True, exist_ok=True)

    symbols, universe_registry, universe_metadata = _resolve_universe(
        config, injected=frames is not None
    )
    panel_options["symbols"] = symbols
    print(
        f"[{datetime.now(timezone):%Y-%m-%d %H:%M:%S}] "
        f"Lấy {len(panel_options['symbols'])} mã + {panel_options['benchmark_symbol']}..."
    )
    price_panel = load_price_panel(
        symbols,
        panel_options["benchmark_symbol"],
        start_date=config.get("start_date", "2015-01-01"),
        end_date=config.get("end_date", str(date.today())),
        source=config.get("source", "VCI"),
        frames=frames,
        universe_registry=universe_registry,
        cache_dir=panel_options.get("price_cache_dir"),
        continue_on_error=bool(panel_options.get("continue_on_fetch_error", False)),
    )
    if universe_metadata.get("point_in_time_complete", False):
        price_panel = apply_point_in_time_eligibility(
            price_panel,
            universe_registry,
            timezone_name=config.get("timezone", "Asia/Ho_Chi_Minh"),
        )
    panel_options["_universe_point_in_time_complete"] = bool(
        universe_metadata.get("point_in_time_complete", False)
    )
    data_quality = price_panel.attrs.get("data_quality_report", {})
    data_quality["universe"] = universe_metadata
    print("Tạo feature cổ phiếu + benchmark và target có thể giao dịch...")
    featured = add_panel_features(
        price_panel,
        horizons=panel_options["horizons"],
        price_multiplier=float(config.get("backtest", {}).get("price_multiplier", 1000)),
        base_round_trip_cost_bps=float(panel_options["transaction_cost_bps"]),
        min_history_sessions=int(panel_options.get("min_history_sessions", 252)),
        min_active_sessions_20d=int(panel_options.get("min_active_sessions_20d", 15)),
        min_median_traded_value_vnd=float(
            panel_options.get("min_median_traded_value_vnd", 5_000_000_000)
        ),
        liquidity_impact_bps=float(panel_options.get("liquidity_impact_bps", 20)),
    )
    news_model = panel_options.get("news_model", {}) or {}
    news_enabled = bool(news_model.get("enabled", False))
    feature_columns = list(PANEL_MODEL_FEATURES)
    if news_enabled:
        news_path = news_model.get("articles_csv")
        if not news_path:
            raise ValueError(
                "panel.news_model.enabled=true nhưng chưa có articles_csv. "
                "Truyền --news-articles-csv PATH."
            )
        news_path = Path(news_path)
        if not news_path.is_absolute():
            news_path = PROJECT_ROOT / news_path
        print(f"Nối feature tin point-in-time từ {news_path}...")
        news_articles = load_news_articles(news_path)
        featured = add_panel_news_features(
            featured,
            news_articles,
            lookback_days=int(news_model.get("lookback_days", 5)),
            timezone=config.get("timezone", "Asia/Ho_Chi_Minh"),
        )
        feature_columns.extend(NEWS_MODEL_FEATURES)
    foreign_flow = panel_options.get("foreign_flow", {}) or {}
    flow_enabled = bool(foreign_flow.get("enabled", False))
    if flow_enabled:
        raw_flow_path = str(foreign_flow.get("csv", "")).strip()
        if not raw_flow_path:
            raise ValueError("foreign_flow.enabled=true nhưng chưa có csv.")
        flow_path = Path(raw_flow_path)
        if not flow_path.is_absolute():
            flow_path = PROJECT_ROOT / flow_path
        featured = add_foreign_flow_features(
            featured,
            load_foreign_flow(flow_path),
            timezone=config.get("timezone", "Asia/Ho_Chi_Minh"),
        )
        feature_columns.extend(FLOW_MODEL_FEATURES)

    artifacts: dict[int, dict] = {}
    aggregate_latest: list[pd.DataFrame] = []
    aggregate_backtests: list[pd.DataFrame] = []
    for horizon in panel_options["horizons"]:
        print(f"Walk-forward XGBoost panel horizon {horizon} phiên...")
        result = walk_forward_predict(
            featured,
            target=f"target_net_excess_return_{horizon}d",
            feature_columns=feature_columns,
            min_train_dates=int(panel_options["min_train_dates"]),
            validation_dates=int(panel_options["validation_dates"]),
            test_dates=int(panel_options["test_dates"]),
            step_dates=int(panel_options["step_dates"]),
            max_folds=int(panel_options["max_folds"]),
            min_symbols_per_date=int(panel_options["min_symbols_per_date"]),
            gap=horizon,
            model_kind=panel_options.get("model_kind", "regression"),
            xgboost_params=config.get("xgboost", {}),
            transaction_cost_bps=float(panel_options["transaction_cost_bps"]),
            max_positions=int(panel_options.get("max_positions", panel_options["top_k"])),
            entry_margin_candidates=panel_options.get(
                "entry_margin_candidates", [0.0, 0.0025, 0.005, 0.01]
            ),
            minimum_validation_trades=int(
                panel_options.get("minimum_validation_trades", 3)
            ),
            cooldown_cohorts=int(panel_options.get("cooldown_cohorts", 0)),
            frozen_holdout_dates=int(panel_options.get("frozen_holdout_dates", 0)),
            lower_confidence_level=float(
                panel_options.get("lower_confidence_level", 0.80)
            ),
        )
        metrics, backtest = evaluate_panel_predictions(
            result.predictions,
            top_k=int(panel_options["top_k"]),
            transaction_cost_bps=float(panel_options["transaction_cost_bps"]),
            horizon=horizon,
            rebalance_every=horizon,
            min_symbols_per_date=int(panel_options["min_symbols_per_date"]),
            cooldown_cohorts=int(panel_options.get("cooldown_cohorts", 0)),
            minimum_holding_sessions=int(
                panel_options.get("minimum_holding_sessions", 2)
            ),
            cost_stress_multipliers=panel_options.get(
                "cost_stress_multipliers", [1.0, 1.5, 2.0]
            ),
            prediction_is_net=True,
        )
        development_metrics = metrics
        trades = backtest.attrs.get("trade_ledger", pd.DataFrame()).copy()
        frozen_backtest = pd.DataFrame()
        frozen_trades = pd.DataFrame()
        if not result.frozen_predictions.empty:
            frozen_metrics, frozen_backtest = evaluate_panel_predictions(
                result.frozen_predictions,
                top_k=int(panel_options["top_k"]),
                transaction_cost_bps=float(panel_options["transaction_cost_bps"]),
                horizon=horizon,
                rebalance_every=horizon,
                min_symbols_per_date=int(panel_options["min_symbols_per_date"]),
                cooldown_cohorts=int(panel_options.get("cooldown_cohorts", 0)),
                minimum_holding_sessions=int(
                    panel_options.get("minimum_holding_sessions", 2)
                ),
                cost_stress_multipliers=panel_options.get(
                    "cost_stress_multipliers", [1.0, 1.5, 2.0]
                ),
                prediction_is_net=True,
            )
            frozen_trades = frozen_backtest.attrs.get(
                "trade_ledger", pd.DataFrame()
            ).copy()
            metrics = {
                **development_metrics,
                "development": development_metrics,
                "frozen": frozen_metrics,
            }
        metrics["publish_guard"] = build_panel_publish_guard(metrics, config)
        metrics["walk_forward"] = result.training_metadata
        metrics["execution"] = {
            "signal": "after_close_t",
            "entry": "open_t_plus_1",
            "exit": f"close_t_plus_{horizon}",
            "target": f"target_net_excess_return_{horizon}d",
            "gross_target_for_audit": f"target_excess_return_{horizon}d",
            "transaction_cost_bps_full_round_trip_selected_positions": float(
                panel_options["transaction_cost_bps"]
            ),
            "state_machine": "CASH -> LONG -> CASH",
            "max_positions": int(panel_options.get("max_positions", panel_options["top_k"])),
            "cash_is_default": True,
            "minimum_holding_sessions": int(
                panel_options.get("minimum_holding_sessions", 2)
            ),
        }
        live = result.latest_ranking.copy()
        research_ok = metrics["publish_guard"]["status"] == "RESEARCH_OK"
        live["decision"] = "WAIT"
        if research_ok:
            live.loc[live["candidate_decision"] == "BUY_CANDIDATE", "decision"] = (
                "BUY_CANDIDATE"
            )
        live["publish_gate"] = metrics["publish_guard"]["status"]
        result.latest_ranking = live
        artifacts[horizon] = {
            "result": result,
            "metrics": metrics,
            "backtest": backtest,
            "trades": trades,
            "frozen_backtest": frozen_backtest,
            "frozen_trades": frozen_trades,
        }

        result.predictions.reset_index().to_csv(
            run_directory / f"predictions_{horizon}d.csv", index=False
        )
        if not result.frozen_predictions.empty:
            result.frozen_predictions.reset_index().to_csv(
                run_directory / f"frozen_predictions_{horizon}d.csv", index=False
            )
        latest = result.latest_ranking.reset_index()
        latest.insert(0, "horizon", horizon)
        latest.to_csv(run_directory / f"latest_ranking_{horizon}d.csv", index=False)
        aggregate_latest.append(latest)
        folds = result.folds.reset_index()
        folds.to_csv(run_directory / f"folds_{horizon}d.csv", index=False)
        backtest_output = backtest.reset_index()
        backtest_output.attrs = {}
        backtest_output.insert(0, "horizon", horizon)
        backtest_output.insert(1, "sample", "development")
        backtest_output.to_csv(
            run_directory / f"backtest_{horizon}d.csv", index=False
        )
        aggregate_backtests.append(backtest_output)
        if not trades.empty:
            trades.to_csv(run_directory / f"trades_{horizon}d.csv", index=False)
        if not frozen_backtest.empty:
            frozen_output = frozen_backtest.reset_index()
            frozen_output.attrs = {}
            frozen_output.insert(0, "horizon", horizon)
            frozen_output.insert(1, "sample", "frozen")
            frozen_output.to_csv(
                run_directory / f"frozen_backtest_{horizon}d.csv", index=False
            )
            aggregate_backtests.append(frozen_output)
        if not frozen_trades.empty:
            frozen_trades.to_csv(
                run_directory / f"frozen_trades_{horizon}d.csv", index=False
            )
        write_json(run_directory / f"metrics_{horizon}d.json", metrics)
        write_json(
            run_directory / f"feature_importance_{horizon}d.json",
            result.feature_importance,
        )
        result.final_model.save_model(
            str(run_directory / f"xgboost_panel_{horizon}d.json")
        )

    price_panel.reset_index().to_csv(run_directory / "price_panel.csv", index=False)
    featured.reset_index().to_csv(run_directory / "panel_features.csv", index=False)
    pd.concat(aggregate_latest, ignore_index=True).to_csv(
        run_directory / "latest_rankings.csv", index=False
    )
    pd.concat(aggregate_backtests, ignore_index=True).to_csv(
        run_directory / "panel_backtests.csv", index=False
    )
    write_json(
        run_directory / "panel_metrics.json",
        {f"{horizon}d": artifact["metrics"] for horizon, artifact in artifacts.items()},
    )
    write_json(run_directory / "data_quality_report.json", data_quality)
    universe_registry.to_csv(run_directory / "universe_registry.csv", index=False)
    write_json(run_directory / "universe_summary.json", universe_metadata)
    write_json(
        run_directory / "feature_availability.json",
        {
            "price_liquidity_market_breadth": "applied",
            "sector": "applied" if universe_registry["sector"].notna().any() else "market_fallback",
            "foreign_flow": "applied" if flow_enabled else "unavailable_not_imputed",
            "news": "applied" if news_enabled else "research_only_not_applied",
            "point_in_time_universe_complete": bool(
                universe_metadata.get("point_in_time_complete", False)
            ),
        },
    )
    write_json(
        run_directory / "news_model_summary.json",
        {
            "enabled": news_enabled,
            "feature_columns": NEWS_MODEL_FEATURES if news_enabled else [],
            "articles_csv": str(news_model.get("articles_csv")) if news_enabled else None,
            "lookback_days": int(news_model.get("lookback_days", 5)) if news_enabled else None,
            "point_in_time_rule": "available_at <= local market close of date t",
        },
    )
    write_json(run_directory / "resolved_config.json", config)
    metadata_config = {**config, "symbol": "PANEL"}
    metadata = build_run_metadata(metadata_config, price_panel, PROJECT_ROOT)
    metadata["symbols"] = panel_options["symbols"]
    metadata["benchmark_symbol"] = panel_options["benchmark_symbol"]
    metadata["execution_timing"] = (
        "tạo feature sau close t; vào open t+1; thoát close t+h"
    )
    write_json(run_directory / "run_metadata.json", metadata)

    make_panel_performance_chart(artifacts, run_directory / "panel_performance.png")
    write_panel_report(
        config,
        price_panel,
        artifacts,
        data_quality,
        run_directory / "panel_report.md",
    )
    write_panel_dashboard(
        config,
        price_panel,
        artifacts,
        run_directory / "panel_dashboard.html",
    )

    if config.get("save_to_postgres", True):
        print("Lưu panel vào PostgreSQL...")
        save_panel_postgres(config, run_directory, artifacts)
    print(f"Xong panel. Báo cáo nằm ở: {run_directory}")
    return run_directory


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Xếp hạng panel cổ phiếu Việt Nam bằng XGBoost walk-forward có purge."
    )
    parser.add_argument("--symbols", type=_csv_strings, help="Ví dụ FPT,VCB,HPG,VNM,MWG")
    parser.add_argument("--benchmark", help="Benchmark, mặc định VNINDEX.")
    parser.add_argument("--horizons", type=_csv_integers, help="Ví dụ 5,20")
    parser.add_argument("--top-k", type=int)
    parser.add_argument("--max-positions", type=int)
    parser.add_argument("--source")
    parser.add_argument("--start-date")
    parser.add_argument("--end-date")
    parser.add_argument("--min-train-dates", type=int)
    parser.add_argument("--validation-dates", type=int)
    parser.add_argument("--test-dates", type=int)
    parser.add_argument("--step-dates", type=int)
    parser.add_argument("--max-folds", type=int)
    parser.add_argument("--min-symbols-per-date", type=int)
    parser.add_argument("--model-kind", choices=["regression", "ranking"])
    parser.add_argument("--transaction-cost-bps", type=float)
    parser.add_argument(
        "--universe",
        choices=["configured", "all-vietnam", "current-market"],
        help="Universe cấu hình hoặc snapshot toàn HOSE/HNX/UPCOM.",
    )
    parser.add_argument("--universe-csv", help="Registry PIT có symbol/listed_at/delisted_at/available_at.")
    parser.add_argument("--exchanges", type=_csv_strings, help="HOSE,HNX,UPCOM")
    parser.add_argument("--max-symbols", type=int, help="Giới hạn smoke test; không dùng để chọn mã theo kết quả.")
    parser.add_argument("--foreign-flow-csv", help="CSV foreign flow point-in-time.")
    parser.add_argument("--news-articles-csv", help="CSV lịch sử tin đã có available_at.")
    parser.add_argument("--use-news", action="store_true", help="Bật news features; cần --news-articles-csv.")
    parser.add_argument("--database-url")
    parser.add_argument("--no-postgres", action="store_true")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    config = resolve_panel_config(load_config(), args)
    run_panel_once(config)


if __name__ == "__main__":
    main()
