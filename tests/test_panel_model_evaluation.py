from __future__ import annotations

import numpy as np
import pandas as pd

from src.panel.evaluation import (
    evaluate_panel_predictions,
    rank_ic_by_date,
    sparse_panel_backtest,
)
from src.panel.model import walk_forward_predict


def make_model_panel(days: int = 80, symbols: int = 5) -> pd.DataFrame:
    dates = pd.bdate_range("2021-01-04", periods=days)
    names = [f"S{number}" for number in range(symbols)]
    records: list[dict] = []
    for date_index, current_date in enumerate(dates):
        for symbol_index, symbol in enumerate(names):
            signal = symbol_index / max(symbols - 1, 1) + date_index * 0.001
            excess = 0.02 * signal - 0.005
            records.append(
                {
                    "date": current_date,
                    "symbol": symbol,
                    "signal": signal,
                    "noise": np.sin(date_index + symbol_index),
                    "target_excess_return_5d": (
                        excess if date_index < days - 5 else np.nan
                    ),
                    "target_return_5d": (
                        excess + 0.002 if date_index < days - 5 else np.nan
                    ),
                    "target_market_return_5d": (
                        0.002 if date_index < days - 5 else np.nan
                    ),
                    "market_regime": "bull" if date_index % 2 else "sideways",
                }
            )
    return pd.DataFrame(records).set_index(["date", "symbol"])


def test_expanding_walk_forward_produces_purged_oos_and_latest_rankings() -> None:
    panel = make_model_panel()
    result = walk_forward_predict(
        panel,
        target="target_excess_return_5d",
        feature_columns=["signal", "noise"],
        min_train_dates=30,
        validation_dates=5,
        test_dates=10,
        gap=5,
        xgboost_params={"num_boost_round": 12, "max_depth": 2, "nthread": 1},
    )

    assert not result.predictions.empty
    assert result.predictions.index.is_unique
    assert len(result.latest_ranking) == 5
    assert result.latest_ranking["predicted_rank"].tolist() == [1, 2, 3, 4, 5]
    assert (result.folds["gap"] == 5).all()
    assert (result.folds["train_end"] < result.folds["test_start"]).all()
    assert (result.folds["train_end"] < result.folds["validation_start"]).all()
    assert (result.folds["validation_end"] < result.folds["test_start"]).all()
    assert result.predictions.index.get_level_values("date").max() <= pd.bdate_range(
        "2021-01-04", periods=80
    )[-6]
    assert set(result.feature_importance) == {"signal", "noise"}
    assert result.predictions.groupby(level="date")["predicted_rank"].min().eq(1).all()
    assert (result.predictions["prediction_lower_bound"] <= result.predictions["prediction"]).all()


def test_ranking_mode_uses_each_date_as_query_group() -> None:
    result = walk_forward_predict(
        make_model_panel(days=55, symbols=4),
        target="target_excess_return_5d",
        feature_columns=["signal", "noise"],
        min_train_dates=25,
        validation_dates=5,
        test_dates=10,
        gap=5,
        model_kind="ranking",
        xgboost_params={"num_boost_round": 4, "max_depth": 2, "nthread": 1},
    )
    assert result.model_kind == "ranking"
    assert len(result.latest_ranking) == 4
    assert result.predictions["prediction"].notna().all()


def test_evaluation_reports_rank_ic_net_portfolio_and_regimes() -> None:
    dates = pd.bdate_range("2024-01-02", periods=20)
    records: list[dict] = []
    for date_index, current_date in enumerate(dates):
        for symbol_index, symbol in enumerate(["A", "B", "C", "D"]):
            score = float(symbol_index)
            records.append(
                {
                    "date": current_date,
                    "symbol": symbol,
                    "prediction": score,
                    "actual_excess_return": score * 0.01,
                    "actual_return": score * 0.01 + date_index * 0.0001,
                    "actual_market_return": 0.001,
                    "market_regime": "bull" if date_index < 10 else "bear",
                }
            )
    predictions = pd.DataFrame(records).set_index(["date", "symbol"])

    daily_ic = rank_ic_by_date(predictions)
    metrics, backtest = evaluate_panel_predictions(
        predictions,
        top_k=2,
        transaction_cost_bps=10,
        horizon=5,
        rebalance_every=5,
    )

    assert np.allclose(daily_ic.to_numpy(), 1.0)
    assert metrics["rank_ic"]["mean"] == 1.0
    assert metrics["rank_ic"]["positive_rate"] == 1.0
    assert metrics["top_k_portfolio"]["observations"] == 4
    assert metrics["top_k_portfolio"]["average_turnover"] >= 0
    assert metrics["top_k_portfolio"]["max_drawdown"] <= 0
    assert set(metrics["by_regime"]) == {"bull", "bear"}
    assert backtest.iloc[0]["net_return"] < backtest.iloc[0]["gross_return"]
    assert (backtest["net_return"] <= backtest["gross_return"]).all()
    assert np.isclose(backtest["round_trip_turnover"].sum(), 8.0)
    assert np.isclose(backtest["cost"].sum(), 4 * 10 / 10_000)
    assert metrics["sparse_portfolio"]["completed_round_trips"] == 8
    assert metrics["sparse_portfolio"]["no_trade_rate"] == 0.0
    assert metrics["sparse_portfolio"]["cash_is_default"] is True


def test_sparse_backtest_keeps_cash_when_predictions_do_not_clear_cost() -> None:
    dates = pd.bdate_range("2024-01-02", periods=12)
    rows = [
        {
            "date": date,
            "symbol": symbol,
            "prediction": 0.004,
            "actual_return": 0.02,
            "actual_market_return": 0.001,
        }
        for date in dates
        for symbol in ["A", "B", "C"]
    ]
    cohorts, trades = sparse_panel_backtest(
        pd.DataFrame(rows),
        max_positions=2,
        transaction_cost_bps=50,
        horizon=5,
        min_symbols_per_date=3,
    )

    assert trades.empty
    assert cohorts["positions"].eq(0).all()
    assert cohorts["cost"].eq(0).all()
    assert cohorts["net_return"].eq(0).all()


def test_sparse_backtest_trades_only_eligible_rows_and_uses_row_cost() -> None:
    dates = pd.bdate_range("2024-01-02", periods=6)
    rows = []
    for current_date in dates:
        rows.extend(
            [
                {
                    "date": current_date,
                    "symbol": "LIQUID",
                    "prediction": 0.02,
                    "actual_return": 0.03,
                    "actual_market_return": 0.0,
                    "is_tradable": True,
                    "estimated_round_trip_cost": 0.007,
                },
                {
                    "date": current_date,
                    "symbol": "ILLIQUID",
                    "prediction": 0.50,
                    "actual_return": 0.50,
                    "actual_market_return": 0.0,
                    "is_tradable": False,
                    "estimated_round_trip_cost": 0.20,
                },
            ]
        )
    cohorts, trades = sparse_panel_backtest(
        pd.DataFrame(rows),
        max_positions=1,
        min_symbols_per_date=2,
        horizon=5,
        prediction_is_net=True,
    )
    assert set(trades["symbol"]) == {"LIQUID"}
    assert np.isclose(trades.iloc[0]["cost"], 0.007)
    assert np.isclose(trades.iloc[0]["net_return"], 0.023)


def test_frozen_holdout_is_scored_after_purge_and_never_selects_margin() -> None:
    result = walk_forward_predict(
        make_model_panel(days=120, symbols=5),
        target="target_excess_return_5d",
        feature_columns=["signal", "noise"],
        min_train_dates=30,
        validation_dates=5,
        test_dates=10,
        gap=5,
        frozen_holdout_dates=10,
        minimum_validation_trades=1,
        max_positions=2,
        xgboost_params={"num_boost_round": 8, "max_depth": 2, "nthread": 1},
    )

    assert not result.frozen_predictions.empty
    assert result.predictions.index.get_level_values("date").max() < (
        result.frozen_predictions.index.get_level_values("date").min()
    )
    frozen_meta = result.training_metadata["frozen_holdout"]
    assert frozen_meta["enabled"] is True
    assert frozen_meta["purge_before_frozen"] == 5
    assert "prediction_lower_bound" in result.frozen_predictions


def test_evaluation_drops_dates_with_too_few_symbols() -> None:
    panel = make_model_panel(days=30, symbols=5).reset_index()
    sparse_date = panel["date"].min()
    panel = panel[~((panel["date"] == sparse_date) & panel["symbol"].isin(["S2", "S3", "S4"]))]
    panel = panel.rename(
        columns={
            "signal": "prediction",
            "target_excess_return_5d": "actual_excess_return",
            "target_return_5d": "actual_return",
            "target_market_return_5d": "actual_market_return",
        }
    ).set_index(["date", "symbol"])

    metrics, backtest = evaluate_panel_predictions(
        panel,
        top_k=2,
        transaction_cost_bps=10,
        horizon=5,
        rebalance_every=5,
        min_symbols_per_date=5,
    )

    assert sparse_date not in backtest.index
    assert metrics["top_k_portfolio"]["min_symbols_per_date"] == 5
