from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo


APP_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = APP_DIR.parents[1]
LOCAL_PYDEPS = PROJECT_ROOT / "work" / "pydeps"

if LOCAL_PYDEPS.exists() and str(LOCAL_PYDEPS) not in sys.path:
    sys.path.append(str(LOCAL_PYDEPS))

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def load_config() -> dict:
    config_path = APP_DIR / "config.json"
    with config_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def normalize_symbol(symbol: str | None) -> str:
    """Chuan hoa ma co phieu nguoi dung nhap vao."""
    if symbol is None:
        return ""
    return symbol.strip().upper()


def resolve_config(config: dict, args: argparse.Namespace) -> dict:
    """
    Ghep config trong file voi tham so nguoi dung truyen vao.

    Thu tu uu tien:
    1. --symbol
    2. positional symbol, vi du: ./run_now.sh FPT
    3. config.json
    4. hoi truc tiep neu dang chay trong terminal
    """
    selected_symbol = normalize_symbol(args.symbol_option or args.symbol or config.get("symbol"))

    if not selected_symbol and sys.stdin.isatty():
        selected_symbol = normalize_symbol(input("Nhap ma co phieu, vi du HCM/FPT/VCB: "))

    if not selected_symbol:
        raise ValueError(
            "Chua co ma co phieu. Hay chay: ./run_now.sh HCM hoac python3 "
            "vn_stock_daily_analysis.py --once --symbol HCM"
        )

    config = config.copy()
    config["symbol"] = selected_symbol

    if args.source:
        config["source"] = args.source.strip().upper()
    if args.forecast_sessions:
        config["forecast_sessions"] = args.forecast_sessions
    if args.run_time:
        config["daily_run_time"] = args.run_time
    if args.database_url:
        config["database_url"] = args.database_url
    if args.no_postgres:
        config["save_to_postgres"] = False

    return config


def rsi(close: pd.Series, window: int = 14) -> pd.Series:
    """Tinh RSI de do suc manh tang/giam cua gia."""
    diff = close.diff()
    gain = diff.clip(lower=0)
    loss = -diff.clip(upper=0)
    avg_gain = gain.ewm(alpha=1 / window, adjust=False, min_periods=window).mean()
    avg_loss = loss.ewm(alpha=1 / window, adjust=False, min_periods=window).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


def max_drawdown(returns: pd.Series) -> tuple[float, pd.Timestamp, pd.Timestamp]:
    """Tinh muc sut giam lon nhat tu dinh gan nhat."""
    equity = (1 + returns.fillna(0)).cumprod()
    peaks = equity.cummax()
    drawdown = equity / peaks - 1
    trough_date = drawdown.idxmin()
    peak_date = equity.loc[:trough_date].idxmax()
    return float(drawdown.min()), peak_date, trough_date


def sigmoid(values: np.ndarray) -> np.ndarray:
    """Ham sigmoid chuyen diem so bat ky ve xac suat 0..1."""
    values = np.clip(values, -35, 35)
    return 1 / (1 + np.exp(-values))


def fit_simple_logistic(
    x_train: pd.DataFrame,
    y_train: pd.Series,
    iterations: int = 2500,
    learning_rate: float = 0.08,
    l2: float = 0.01,
) -> dict:
    """
    Logistic Regression nho gon bang NumPy.

    Ly do tu viet:
    - Giam phu thuoc nang nhu scikit-learn/scipy.
    - Du de hoc cach model bien chi bao thanh xac suat tang/giam.
    """
    x = x_train.to_numpy(dtype=float)
    y = y_train.to_numpy(dtype=float)

    mean = np.nanmean(x, axis=0)
    std = np.nanstd(x, axis=0)
    std[std == 0] = 1
    x_scaled = (x - mean) / std
    x_aug = np.column_stack([np.ones(len(x_scaled)), x_scaled])

    weights = np.zeros(x_aug.shape[1])
    count_pos = max(float(y.sum()), 1.0)
    count_neg = max(float(len(y) - y.sum()), 1.0)
    weight_pos = len(y) / (2 * count_pos)
    weight_neg = len(y) / (2 * count_neg)
    row_weights = np.where(y == 1, weight_pos, weight_neg)

    for _ in range(iterations):
        prob = sigmoid(x_aug @ weights)
        error = (prob - y) * row_weights
        gradient = (x_aug.T @ error) / len(y)
        gradient[1:] += l2 * weights[1:] / len(y)
        weights -= learning_rate * gradient

    return {"weights": weights, "mean": mean, "std": std}


def predict_simple_logistic(model: dict, x_data: pd.DataFrame) -> np.ndarray:
    x = x_data.to_numpy(dtype=float)
    x_scaled = (x - model["mean"]) / model["std"]
    x_aug = np.column_stack([np.ones(len(x_scaled)), x_scaled])
    return sigmoid(x_aug @ model["weights"])


def binary_metrics(y_true: pd.Series, y_pred: np.ndarray) -> dict:
    """Tinh accuracy, balanced accuracy va confusion matrix cho bai toan 0/1."""
    y = y_true.to_numpy(dtype=int)
    pred = y_pred.astype(int)

    tn = int(((y == 0) & (pred == 0)).sum())
    fp = int(((y == 0) & (pred == 1)).sum())
    fn = int(((y == 1) & (pred == 0)).sum())
    tp = int(((y == 1) & (pred == 1)).sum())

    accuracy = float((tp + tn) / max(len(y), 1))
    recall_0 = tn / max(tn + fp, 1)
    recall_1 = tp / max(tp + fn, 1)
    balanced_accuracy = float((recall_0 + recall_1) / 2)

    return {
        "accuracy": accuracy,
        "balanced_accuracy": balanced_accuracy,
        "confusion_matrix": [[tn, fp], [fn, tp]],
    }


def fetch_history(config: dict) -> pd.DataFrame:
    """Lay du lieu lich su tu vnstock."""
    from vnstock import Quote

    quote = Quote(symbol=config["symbol"], source=config["source"])
    raw = quote.history(
        start=config["start_date"],
        end=str(date.today()),
        interval="d",
    )

    df = raw.copy()
    df["time"] = pd.to_datetime(df["time"]).dt.tz_localize(None)
    df = df.sort_values("time").drop_duplicates("time").set_index("time")
    df = df.rename(columns={col: col.lower() for col in df.columns})

    for col in ["open", "high", "low", "close", "volume"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    cleaned = df.dropna(subset=["open", "high", "low", "close", "volume"])
    if cleaned.empty:
        raise ValueError(f"Khong lay duoc du lieu cho ma {config['symbol']}.")
    return cleaned


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """Tao cac chi bao de phan tich va dua vao model."""
    out = df.copy()
    out["return_1d"] = out["close"].pct_change()
    out["return_5d"] = out["close"].pct_change(5)
    out["return_20d"] = out["close"].pct_change(20)
    out["sma_5"] = out["close"].rolling(5).mean()
    out["sma_20"] = out["close"].rolling(20).mean()
    out["sma_60"] = out["close"].rolling(60).mean()
    out["ema_12"] = out["close"].ewm(span=12, adjust=False).mean()
    out["ema_26"] = out["close"].ewm(span=26, adjust=False).mean()
    out["macd"] = out["ema_12"] - out["ema_26"]
    out["rsi_14"] = rsi(out["close"], 14)
    out["volatility_20d"] = out["return_1d"].rolling(20).std() * math.sqrt(252)
    out["volume_sma_20"] = out["volume"].rolling(20).mean()
    out["volume_z_20"] = (
        (out["volume"] - out["volume_sma_20"]) / out["volume"].rolling(20).std()
    )
    out["range_pct"] = (out["high"] - out["low"]) / out["close"]
    out["close_vs_sma20"] = out["close"] / out["sma_20"] - 1
    out["close_vs_sma60"] = out["close"] / out["sma_60"] - 1

    # Muc tieu cho model: ngay ke tiep tang thi 1, khong tang thi 0.
    out["target_next_up"] = (out["close"].shift(-1) > out["close"]).astype(int)
    out["next_return"] = out["close"].pct_change().shift(-1)
    return out


def train_models(df: pd.DataFrame) -> tuple[dict, pd.DataFrame, dict]:
    """Train model xu huong va tinh xac suat tang cho phien ke tiep."""
    features = [
        "return_1d",
        "return_5d",
        "return_20d",
        "rsi_14",
        "macd",
        "volatility_20d",
        "volume_z_20",
        "range_pct",
        "close_vs_sma20",
        "close_vs_sma60",
    ]

    model_df = df.dropna(subset=features + ["target_next_up"]).copy()
    labeled = model_df.iloc[:-1]
    latest_features = model_df.tail(1)[features]

    split = int(len(labeled) * 0.8)
    train = labeled.iloc[:split]
    test = labeled.iloc[split:]

    X_train, y_train = train[features], train["target_next_up"]
    X_test, y_test = test[features], test["target_next_up"]

    metrics = {
        "split": {
            "train_start": str(train.index.min().date()),
            "train_end": str(train.index.max().date()),
            "test_start": str(test.index.min().date()),
            "test_end": str(test.index.max().date()),
            "train_rows": int(len(train)),
            "test_rows": int(len(test)),
        }
    }
    scored_test = test.copy()

    model = fit_simple_logistic(X_train, y_train)
    proba = predict_simple_logistic(model, X_test)
    pred = (proba >= 0.5).astype(int)
    metrics["logistic_regression"] = binary_metrics(y_test, pred)
    scored_test["logistic_prediction"] = pred
    scored_test["logistic_prob_up"] = proba

    # Fit lai tren tat ca du lieu da co nhan de uoc tinh phien ke tiep.
    final_model = fit_simple_logistic(labeled[features], labeled["target_next_up"])
    latest_probs = {
        "logistic_regression": float(predict_simple_logistic(final_model, latest_features)[0])
    }

    majority = int(y_train.mode().iloc[0])
    baseline_pred = np.full(len(y_test), majority)
    metrics["majority_baseline"] = {"class": majority, **binary_metrics(y_test, baseline_pred)}

    return metrics, scored_test, latest_probs


def simulate_forecast(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    """Mo phong vung gia tuong lai bang Monte Carlo."""
    sessions = int(config["forecast_sessions"])
    simulations = int(config["simulations"])
    lookback = int(config["lookback_sessions"])

    returns = df["return_1d"].dropna().tail(lookback)
    latest_close = df["close"].iloc[-1]

    rng = np.random.default_rng(42)
    drift = returns.mean() * 0.35
    vol = returns.std()

    simulated_returns = rng.normal(loc=drift, scale=vol, size=(simulations, sessions))
    simulated_prices = latest_close * np.cumprod(1 + simulated_returns, axis=1)
    percentiles = np.percentile(simulated_prices, [10, 25, 50, 75, 90], axis=0)

    future_dates = pd.bdate_range(df.index[-1] + pd.Timedelta(days=1), periods=sessions)
    forecast = pd.DataFrame(
        {
            "p10": percentiles[0],
            "p25": percentiles[1],
            "p50": percentiles[2],
            "p75": percentiles[3],
            "p90": percentiles[4],
        },
        index=future_dates,
    )
    forecast["prob_end_above_latest"] = float((simulated_prices[:, -1] > latest_close).mean())
    forecast["latest_close"] = latest_close
    return forecast


def current_levels(df: pd.DataFrame) -> dict:
    latest = df.iloc[-1]
    recent20 = df.tail(20)
    recent60 = df.tail(60)
    returns = df["return_1d"].dropna()
    mdd, peak_date, trough_date = max_drawdown(returns)

    return {
        "latest_date": str(df.index[-1].date()),
        "latest_close": float(latest["close"]),
        "sma20": float(latest["sma_20"]),
        "sma60": float(latest["sma_60"]),
        "rsi14": float(latest["rsi_14"]),
        "vol20": float(latest["volatility_20d"]),
        "volume20": float(latest["volume_sma_20"]),
        "support20": float(recent20["low"].min()),
        "resistance20": float(recent20["high"].max()),
        "support60": float(recent60["low"].min()),
        "resistance60": float(recent60["high"].max()),
        "max_drawdown": float(mdd),
        "drawdown_peak": str(peak_date.date()),
        "drawdown_trough": str(trough_date.date()),
        "var_95_daily": float(returns.quantile(0.05)),
    }


def make_history_chart(df: pd.DataFrame, out_path: Path) -> None:
    returns = df["return_1d"]
    equity = (1 + returns.fillna(0)).cumprod()
    drawdown = equity / equity.cummax() - 1

    fig, axes = plt.subplots(3, 1, figsize=(13, 9), sharex=True, height_ratios=[2.2, 1, 1])
    axes[0].plot(df.index, df["close"], label="Close", color="#1f77b4", linewidth=1.4)
    axes[0].plot(df.index, df["sma_20"], label="SMA20", color="#ff7f0e", linewidth=1.0)
    axes[0].plot(df.index, df["sma_60"], label="SMA60", color="#2ca02c", linewidth=1.0)
    axes[0].set_title("Gia lich su va duong trung binh")
    axes[0].set_ylabel("Nghin VND/cp")
    axes[0].legend(loc="upper left")
    axes[0].grid(alpha=0.25)

    axes[1].bar(df.index, df["volume"] / 1_000_000, color="#6c757d", width=1.0)
    axes[1].set_title("Khoi luong giao dich")
    axes[1].set_ylabel("Trieu cp")
    axes[1].grid(alpha=0.25)

    axes[2].fill_between(df.index, drawdown, 0, color="#d62728", alpha=0.35)
    axes[2].set_title("Drawdown")
    axes[2].set_ylabel("Drawdown")
    axes[2].grid(alpha=0.25)

    fig.tight_layout()
    fig.savefig(out_path, dpi=170)
    plt.close(fig)


def make_forecast_chart(df: pd.DataFrame, forecast: pd.DataFrame, levels: dict, out_path: Path) -> None:
    chart_df = df.tail(260)

    fig, ax = plt.subplots(figsize=(13, 7))
    ax.plot(chart_df.index, chart_df["close"], label="Close", color="#1f77b4", linewidth=1.5)
    ax.plot(chart_df.index, chart_df["sma_20"], label="SMA20", color="#ff7f0e", linewidth=1.1)
    ax.plot(chart_df.index, chart_df["sma_60"], label="SMA60", color="#2ca02c", linewidth=1.1)
    ax.plot(forecast.index, forecast["p50"], label="Forecast P50", color="#111111", linewidth=1.6)
    ax.fill_between(forecast.index, forecast["p25"], forecast["p75"], color="#6baed6", alpha=0.35, label="P25-P75")
    ax.fill_between(forecast.index, forecast["p10"], forecast["p90"], color="#c6dbef", alpha=0.45, label="P10-P90")

    ax.axhline(levels["support20"], color="#d62728", linestyle="--", linewidth=1, label="Support 20")
    ax.axhline(levels["resistance20"], color="#9467bd", linestyle="--", linewidth=1, label="Resistance 20")
    ax.axhline(levels["latest_close"], color="#555555", linestyle=":", linewidth=1, label="Latest close")

    ax.set_title("Du bao so bo cac phien toi")
    ax.set_ylabel("Nghin VND/cp")
    ax.grid(alpha=0.25)
    ax.legend(loc="upper left", ncol=2)
    fig.tight_layout()
    fig.savefig(out_path, dpi=170)
    plt.close(fig)


def scenario_text(levels: dict, forecast: pd.DataFrame, latest_probs: dict) -> list[str]:
    latest = levels["latest_close"]
    end = forecast.iloc[-1]
    prob_up_model = latest_probs.get("logistic_regression", float("nan"))
    prob_up_sim = float(end["prob_end_above_latest"])

    if latest > levels["sma20"] > levels["sma60"]:
        trend = "Xu huong ngan han dang thuan: gia nam tren SMA20 va SMA60."
    elif latest > levels["sma60"]:
        trend = "Xu huong trung han chua xau, nhung ngan han con yeu vi gia duoi SMA20."
    else:
        trend = "Xu huong dang yeu: gia nam duoi SMA60, can uu tien quan tri rui ro."

    return [
        trend,
        f"Mo hinh logistic uoc tinh xac suat phien ke tiep tang: {prob_up_model:.1%}.",
        f"Mo phong uoc tinh xac suat ket thuc tren gia hien tai: {prob_up_sim:.1%}.",
        f"Kich ban tham do: chi giai ngan nho neu gia giu tren {levels['support20']:.2f}-{levels['sma60']:.2f}.",
        f"Kich ban mua theo xac nhan: tang ty trong khi gia dong cua vuot SMA20 quanh {levels['sma20']:.2f} kem thanh khoan tot.",
        f"Kich ban phong thu: neu gia dong cua thung {min(levels['support20'], levels['sma60']):.2f}, can giam ty trong hoac dung lo theo ke hoach.",
        f"Kich ban ha rui ro: neu gia tiep can {levels['resistance20']:.2f} ma dong luc yeu, can can nhac chot/ha mot phan.",
    ]


def write_report(
    config: dict,
    df: pd.DataFrame,
    forecast: pd.DataFrame,
    levels: dict,
    metrics: dict,
    latest_probs: dict,
    out_path: Path,
) -> None:
    latest = levels["latest_close"]
    end = forecast.iloc[-1]
    lines = [
        f"# Bao cao ngay {datetime.now().date()} - {config['symbol']}",
        "",
        "## Du lieu",
        "",
        f"- Ma: {config['symbol']}; source: vnstock/{config['source']}.",
        f"- Vung du lieu: {df.index.min().date()} -> {df.index.max().date()}, {len(df):,} phien.",
        f"- Gia dong cua moi nhat: {latest:.2f} nghin VND/cp.",
        "",
        "## Tin hieu hien tai",
        "",
        f"- SMA20: {levels['sma20']:.2f}; SMA60: {levels['sma60']:.2f}; RSI14: {levels['rsi14']:.1f}.",
        f"- Volatility 20 phien, nam hoa: {levels['vol20']:.2%}.",
        f"- Ho tro 20 phien: {levels['support20']:.2f}; khang cu 20 phien: {levels['resistance20']:.2f}.",
        f"- VaR 95% ngay: {levels['var_95_daily']:.2%}.",
        f"- Max drawdown lich su: {levels['max_drawdown']:.2%}, tu {levels['drawdown_peak']} den {levels['drawdown_trough']}.",
        "",
        "## Mo hinh xu huong",
        "",
        f"- Test: {metrics['split']['test_start']} -> {metrics['split']['test_end']}.",
        f"- Baseline balanced accuracy: {metrics['majority_baseline']['balanced_accuracy']:.3f}.",
        f"- Logistic balanced accuracy: {metrics['logistic_regression']['balanced_accuracy']:.3f}.",
        f"- Logistic prob phien ke tiep tang: {latest_probs['logistic_regression']:.1%}.",
        "",
        f"## Du bao {config['forecast_sessions']} phien toi",
        "",
        f"- P50 cuoi ky: {end['p50']:.2f}, tuong duong {end['p50'] / latest - 1:.2%}.",
        f"- P10 cuoi ky: {end['p10']:.2f}, tuong duong {end['p10'] / latest - 1:.2%}.",
        f"- P90 cuoi ky: {end['p90']:.2f}, tuong duong {end['p90'] / latest - 1:.2%}.",
        f"- Xac suat mo phong ket thuc tren gia hien tai: {end['prob_end_above_latest']:.1%}.",
        "",
        "## Khung hanh dong tham khao",
        "",
    ]

    lines.extend(f"- {item}" for item in scenario_text(levels, forecast, latest_probs))
    lines.extend(
        [
            "",
            "Luu y: bao cao nay dung de hoc tap va lap kich ban. No khong phai khuyen nghi mua/ban.",
        ]
    )
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def clean_db_value(value):
    """Chuyen NaN/NaT cua Pandas ve None de PostgreSQL hieu la NULL."""
    if pd.isna(value):
        return None
    if isinstance(value, pd.Timestamp):
        return value.to_pydatetime()
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    return value


def dataframe_records(df: pd.DataFrame) -> list[tuple]:
    """Chuyen DataFrame thanh danh sach tuple sach de executemany."""
    return [tuple(clean_db_value(value) for value in row) for row in df.to_numpy()]


def quote_ident(name: str) -> str:
    """Quote ten cot/bang co dinh de tranh trung keyword."""
    return '"' + name.replace('"', '""') + '"'


def upsert_dataframe(conn, table: str, df: pd.DataFrame, conflict_cols: list[str]) -> None:
    """INSERT nhieu dong vao PostgreSQL, neu trung key thi UPDATE."""
    if df.empty:
        return

    columns = list(df.columns)
    col_sql = ", ".join(quote_ident(col) for col in columns)
    placeholders = ", ".join(["%s"] * len(columns))
    conflict_sql = ", ".join(quote_ident(col) for col in conflict_cols)
    update_cols = [col for col in columns if col not in conflict_cols]
    update_sql = ", ".join(
        f"{quote_ident(col)} = EXCLUDED.{quote_ident(col)}" for col in update_cols
    )

    query = (
        f"INSERT INTO {quote_ident(table)} ({col_sql}) VALUES ({placeholders}) "
        f"ON CONFLICT ({conflict_sql}) DO UPDATE SET {update_sql}"
    )

    with conn.cursor() as cur:
        cur.executemany(query, dataframe_records(df))


def load_postgres_schema() -> str:
    return (APP_DIR / "postgres_schema.sql").read_text(encoding="utf-8")


def ensure_postgres_schema(conn) -> None:
    with conn.cursor() as cur:
        cur.execute(load_postgres_schema())


def frame_with_date(df: pd.DataFrame, symbol: str, run_id: str, date_col: str) -> pd.DataFrame:
    """Reset index ngay va them run_id/symbol truoc khi luu PostgreSQL."""
    out = df.reset_index()
    first_col = out.columns[0]
    out = out.rename(columns={first_col: date_col})
    out[date_col] = pd.to_datetime(out[date_col]).dt.date
    out.insert(0, "run_id", run_id)
    out.insert(1, "symbol", symbol)
    return out


def save_postgres(
    config: dict,
    run_dir: Path,
    data: pd.DataFrame,
    scored_test: pd.DataFrame,
    forecast: pd.DataFrame,
    metrics: dict,
    levels: dict,
    latest_probs: dict,
) -> None:
    """
    Luu ket qua vao PostgreSQL 18 database stock_db.

    Mac dinh dung config database_url = postgresql:///stock_db.
    Co the override bang bien moi truong DATABASE_URL hoac --database-url.
    """
    try:
        import psycopg
    except ImportError as exc:
        raise RuntimeError(
            "Thieu psycopg. Hay chay: python3 -m pip install -r requirements.txt"
        ) from exc

    database_url = os.environ.get("DATABASE_URL") or config.get("database_url")
    if not database_url:
        raise ValueError("Chua co database_url. Vi du: postgresql:///stock_db")

    symbol = config["symbol"]
    run_id = run_dir.name
    tz = ZoneInfo(config.get("timezone", "Asia/Ho_Chi_Minh"))
    generated_at = datetime.now(tz)
    end_forecast = forecast.iloc[-1]

    daily_runs = pd.DataFrame(
        [
            {
                "run_id": run_id,
                "symbol": symbol,
                "source": config["source"],
                "generated_at": generated_at,
                "report_dir": str(run_dir),
                "latest_date": pd.to_datetime(levels["latest_date"]).date(),
                "latest_close": levels["latest_close"],
                "sma20": levels["sma20"],
                "sma60": levels["sma60"],
                "rsi14": levels["rsi14"],
                "vol20": levels["vol20"],
                "volume20": levels["volume20"],
                "support20": levels["support20"],
                "resistance20": levels["resistance20"],
                "support60": levels["support60"],
                "resistance60": levels["resistance60"],
                "max_drawdown": levels["max_drawdown"],
                "var_95_daily": levels["var_95_daily"],
                "logistic_prob_next_up": latest_probs["logistic_regression"],
                "forecast_sessions": int(config["forecast_sessions"]),
                "forecast_p10_end": float(end_forecast["p10"]),
                "forecast_p50_end": float(end_forecast["p50"]),
                "forecast_p90_end": float(end_forecast["p90"]),
                "forecast_prob_end_above_latest": float(end_forecast["prob_end_above_latest"]),
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

    history_features = frame_with_date(data, symbol, run_id, "trade_date")
    test_predictions = frame_with_date(scored_test, symbol, run_id, "trade_date")
    forecasts = frame_with_date(forecast, symbol, run_id, "forecast_date")

    with psycopg.connect(database_url) as conn:
        ensure_postgres_schema(conn)
        upsert_dataframe(conn, "daily_runs", daily_runs, ["run_id", "symbol"])
        upsert_dataframe(conn, "history_features", history_features, ["run_id", "symbol", "trade_date"])
        upsert_dataframe(conn, "model_test_predictions", test_predictions, ["run_id", "symbol", "trade_date"])
        upsert_dataframe(conn, "forecasts", forecasts, ["run_id", "symbol", "forecast_date"])
        upsert_dataframe(conn, "model_metrics", metric_rows, ["run_id", "symbol", "metric_name"])


def run_once(config: dict) -> Path:
    tz = ZoneInfo(config.get("timezone", "Asia/Ho_Chi_Minh"))
    run_stamp = datetime.now(tz).strftime("%Y-%m-%d_%H-%M-%S")
    report_root = APP_DIR / config.get("report_root", "reports")
    run_dir = report_root / config["symbol"] / run_stamp
    run_dir.mkdir(parents=True, exist_ok=True)

    print(f"[{datetime.now(tz):%Y-%m-%d %H:%M:%S}] Lay du lieu {config['symbol']}...")
    history = fetch_history(config)

    print("Tinh chi bao...")
    data = add_features(history)

    print("Train model xu huong...")
    metrics, scored_test, latest_probs = train_models(data)

    print("Mo phong du bao...")
    forecast = simulate_forecast(data, config)
    levels = current_levels(data)

    data.reset_index().rename(columns={"time": "date"}).to_csv(run_dir / "history_features.csv", index=False)
    scored_test.reset_index().rename(columns={"time": "date"}).to_csv(run_dir / "model_test_predictions.csv", index=False)
    forecast.reset_index(names="date").to_csv(run_dir / f"forecast_{config['forecast_sessions']}_sessions.csv", index=False)
    (run_dir / "model_metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    (run_dir / "latest_levels.json").write_text(json.dumps(levels, indent=2), encoding="utf-8")

    make_history_chart(data, run_dir / "history_chart.png")
    make_forecast_chart(data, forecast, levels, run_dir / "forecast_chart.png")
    write_report(config, data, forecast, levels, metrics, latest_probs, run_dir / "analysis_report.md")
    if config.get("save_to_postgres", True):
        print("Luu PostgreSQL...")
        save_postgres(config, run_dir, data, scored_test, forecast, metrics, levels, latest_probs)

    print(f"Xong. Bao cao nam o: {run_dir}")
    return run_dir


def seconds_until_next_run(config: dict) -> float:
    tz = ZoneInfo(config.get("timezone", "Asia/Ho_Chi_Minh"))
    hour, minute = [int(part) for part in config["daily_run_time"].split(":")]
    now = datetime.now(tz)
    target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if target <= now:
        target += timedelta(days=1)
    return (target - now).total_seconds()


def loop_daily(config: dict) -> None:
    while True:
        wait_seconds = seconds_until_next_run(config)
        next_run = datetime.now(ZoneInfo(config["timezone"])) + timedelta(seconds=wait_seconds)
        print(f"Lan chay tiep theo: {next_run:%Y-%m-%d %H:%M:%S}")
        time.sleep(wait_seconds)
        try:
            run_once(config)
        except Exception as exc:
            print(f"Loi khi chay: {exc}")
            time.sleep(60)


def main() -> None:
    parser = argparse.ArgumentParser(description="Daily Vietnam stock analysis and forecast.")
    parser.add_argument("symbol", nargs="?", help="Ma co phieu, vi du HCM, FPT, VCB.")
    parser.add_argument("--symbol", dest="symbol_option", help="Ma co phieu, uu tien hon positional symbol.")
    parser.add_argument("--source", help="Nguon du lieu vnstock, mac dinh theo config.json.")
    parser.add_argument("--forecast-sessions", type=int, help="So phien muon du bao.")
    parser.add_argument("--run-time", help="Gio chay hang ngay, vi du 15:30.")
    parser.add_argument("--database-url", help="PostgreSQL URL, vi du postgresql:///stock_db.")
    parser.add_argument("--no-postgres", action="store_true", help="Khong luu vao PostgreSQL.")
    parser.add_argument("--once", action="store_true", help="Chay mot lan roi dung.")
    parser.add_argument("--loop", action="store_true", help="Chay lap moi ngay theo config.")
    args = parser.parse_args()

    config = resolve_config(load_config(), args)

    if args.loop:
        loop_daily(config)
    else:
        run_once(config)


if __name__ == "__main__":
    main()
