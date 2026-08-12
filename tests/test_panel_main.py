from __future__ import annotations

import json

import numpy as np
import pandas as pd

import src.panel_main as panel_main


def _history(
    dates: pd.DatetimeIndex,
    *,
    start: float,
    phase: float,
) -> pd.DataFrame:
    position = np.arange(len(dates), dtype=float)
    close = start * np.exp(0.0005 * position + 0.015 * np.sin(position / 8 + phase))
    open_price = close * (1 + 0.002 * np.cos(position / 5 + phase))
    return pd.DataFrame(
        {
            "open": open_price,
            "high": np.maximum(open_price, close) * 1.01,
            "low": np.minimum(open_price, close) * 0.99,
            "close": close,
            "volume": 2_000_000 + position * 1000,
        },
        index=dates,
    )


def test_panel_runner_creates_end_to_end_artifacts(tmp_path, monkeypatch) -> None:
    dates = pd.bdate_range("2023-01-02", periods=150)
    frames = {
        "AAA": _history(dates, start=10, phase=0.0),
        "BBB": _history(dates, start=20, phase=0.7),
        "CCC": _history(dates, start=30, phase=1.4),
        "VNINDEX": _history(dates, start=1000, phase=0.3),
    }
    news_csv = tmp_path / "news_history.csv"
    news_csv.write_text(
        "\n".join(
            [
                "symbol,available_at,sentiment_score,sentiment_label,event_type,source_name,title,source_url",
                "AAA,2023-02-01T07:00:00Z,1.0,positive,earnings,Test,AAA beats plan,https://example.test/aaa",
                "BBB,2023-02-01T09:00:00Z,-1.0,negative,legal,Test,BBB investigation,https://example.test/bbb",
                "CCC,2023-02-02T07:00:00Z,0.5,positive,corporate_action,Test,CCC dividend,https://example.test/ccc",
            ]
        ),
        encoding="utf-8",
    )
    config = {
        "source": "VCI",
        "start_date": "2023-01-01",
        "end_date": "2024-01-01",
        "timezone": "Asia/Ho_Chi_Minh",
        "report_root": "reports",
        "save_to_postgres": False,
        "xgboost": {
            "num_boost_round": 8,
            "early_stopping_rounds": 3,
            "max_depth": 2,
            "n_jobs": 1,
        },
        "panel": {
            "symbols": ["AAA", "BBB", "CCC"],
            "benchmark_symbol": "VNINDEX",
            "horizons": [5],
            "top_k": 2,
            "min_train_dates": 30,
            "validation_dates": 5,
            "test_dates": 10,
            "step_dates": 10,
            "max_folds": 2,
            "min_symbols_per_date": 3,
            "model_kind": "regression",
            "transaction_cost_bps": 50,
            "news_model": {
                "enabled": True,
                "articles_csv": str(news_csv),
                "lookback_days": 5,
            },
        },
    }
    monkeypatch.setattr(panel_main, "PROJECT_ROOT", tmp_path)

    run_directory = panel_main.run_panel_once(config, frames=frames)

    expected = {
        "panel_report.md",
        "panel_dashboard.html",
        "panel_performance.png",
        "price_panel.csv",
        "panel_features.csv",
        "predictions_5d.csv",
        "latest_ranking_5d.csv",
        "backtest_5d.csv",
        "metrics_5d.json",
        "xgboost_panel_5d.json",
        "data_quality_report.json",
        "news_model_summary.json",
        "run_metadata.json",
    }
    assert expected.issubset({path.name for path in run_directory.iterdir()})
    panel_features = pd.read_csv(run_directory / "panel_features.csv")
    assert "news_count_lookback" in panel_features.columns
    assert panel_features["news_count_lookback"].max() > 0
    news_summary = json.loads((run_directory / "news_model_summary.json").read_text())
    assert news_summary["enabled"] is True
    assert "news_sentiment_mean_lookback" in news_summary["feature_columns"]
    metrics = json.loads((run_directory / "metrics_5d.json").read_text())
    assert metrics["execution"]["entry"] == "open_t_plus_1"
    assert metrics["walk_forward"]["fold_count"] == 2
    assert metrics["top_k_portfolio"]["cost_convention"] == "full_round_trip_each_cohort"
    assert metrics["publish_guard"]["status"] in {"RESEARCH_OK", "NO_EDGE"}
    report = (run_directory / "panel_report.md").read_text(encoding="utf-8")
    assert "Báo cáo panel cổ phiếu Việt Nam" in report
