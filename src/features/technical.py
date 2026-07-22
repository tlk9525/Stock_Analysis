from __future__ import annotations

import math

import numpy as np
import pandas as pd

from src.utils import safe_float


MODEL_FEATURES = [
    "return_1d",
    "return_2d",
    "return_3d",
    "return_5d",
    "return_10d",
    "return_20d",
    "rsi_14",
    "macd_pct",
    "macd_hist_pct",
    "volatility_20d",
    "return_skew_20d",
    "return_kurtosis_20d",
    "volume_z_20",
    "volume_ratio_20",
    "range_pct",
    "close_vs_sma20",
    "close_vs_sma60",
    "bb_position_20",
    "atr_pct_14",
    "adx_14",
    "stoch_k_14",
    "day_of_week",
    "month_of_year",
]


def rsi(close: pd.Series, window: int = 14) -> pd.Series:
    diff = close.diff()
    gain = diff.clip(lower=0)
    loss = -diff.clip(upper=0)
    avg_gain = gain.ewm(alpha=1 / window, adjust=False, min_periods=window).mean()
    avg_loss = loss.ewm(alpha=1 / window, adjust=False, min_periods=window).mean()
    relative_strength = avg_gain / avg_loss.replace(0, np.nan)
    return 100 - (100 / (1 + relative_strength))


def true_range(frame: pd.DataFrame) -> pd.Series:
    previous_close = frame["close"].shift(1)
    ranges = pd.concat(
        [
            frame["high"] - frame["low"],
            (frame["high"] - previous_close).abs(),
            (frame["low"] - previous_close).abs(),
        ],
        axis=1,
    )
    return ranges.max(axis=1)


def average_true_range(frame: pd.DataFrame, window: int = 14) -> pd.Series:
    return (
        true_range(frame)
        .ewm(
            alpha=1 / window,
            adjust=False,
            min_periods=window,
        )
        .mean()
    )


def adx_components(
    frame: pd.DataFrame,
    window: int = 14,
) -> tuple[pd.Series, pd.Series, pd.Series]:
    up_move = frame["high"].diff()
    down_move = -frame["low"].diff()
    plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0.0)
    minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0.0)
    atr = average_true_range(frame, window).replace(0, np.nan)

    plus_di = (
        100
        * pd.Series(plus_dm, index=frame.index)
        .ewm(alpha=1 / window, adjust=False, min_periods=window)
        .mean()
        / atr
    )
    minus_di = (
        100
        * pd.Series(minus_dm, index=frame.index)
        .ewm(alpha=1 / window, adjust=False, min_periods=window)
        .mean()
        / atr
    )
    directional_index = (
        100 * (plus_di - minus_di).abs() / (plus_di + minus_di).replace(0, np.nan)
    )
    adx = directional_index.ewm(
        alpha=1 / window,
        adjust=False,
        min_periods=window,
    ).mean()
    return adx, plus_di, minus_di


def stochastic_oscillator(
    frame: pd.DataFrame,
    k_window: int = 14,
    d_window: int = 3,
) -> tuple[pd.Series, pd.Series]:
    low_min = frame["low"].rolling(k_window).min()
    high_max = frame["high"].rolling(k_window).max()
    k_value = 100 * (frame["close"] - low_min) / (high_max - low_min).replace(0, np.nan)
    return k_value, k_value.rolling(d_window).mean()


def on_balance_volume(frame: pd.DataFrame) -> pd.Series:
    direction = np.sign(frame["close"].diff()).fillna(0)
    return (direction * frame["volume"]).cumsum()


def max_drawdown(returns: pd.Series) -> tuple[float, pd.Timestamp, pd.Timestamp]:
    equity = (1 + returns.fillna(0)).cumprod()
    peaks = equity.cummax()
    drawdown = equity / peaks - 1
    trough_date = drawdown.idxmin()
    peak_date = equity.loc[:trough_date].idxmax()
    return float(drawdown.min()), peak_date, trough_date


def add_features(frame: pd.DataFrame) -> pd.DataFrame:
    out = frame.copy()
    out["return_1d"] = out["close"].pct_change()
    out["return_2d"] = out["close"].pct_change(2)
    out["return_3d"] = out["close"].pct_change(3)
    out["return_5d"] = out["close"].pct_change(5)
    out["return_10d"] = out["close"].pct_change(10)
    out["return_20d"] = out["close"].pct_change(20)
    out["sma_5"] = out["close"].rolling(5).mean()
    out["sma_20"] = out["close"].rolling(20).mean()
    out["sma_60"] = out["close"].rolling(60).mean()
    out["ema_12"] = out["close"].ewm(span=12, adjust=False).mean()
    out["ema_26"] = out["close"].ewm(span=26, adjust=False).mean()
    out["macd"] = out["ema_12"] - out["ema_26"]
    out["macd_signal"] = out["macd"].ewm(span=9, adjust=False).mean()
    out["macd_hist"] = out["macd"] - out["macd_signal"]
    close_base = out["close"].replace(0, np.nan)
    out["macd_pct"] = out["macd"] / close_base
    out["macd_hist_pct"] = out["macd_hist"] / close_base
    out["rsi_14"] = rsi(out["close"], 14)
    out["bb_mid_20"] = out["sma_20"]
    out["bb_std_20"] = out["close"].rolling(20).std()
    out["bb_upper_20"] = out["bb_mid_20"] + 2 * out["bb_std_20"]
    out["bb_lower_20"] = out["bb_mid_20"] - 2 * out["bb_std_20"]
    out["bb_width_20"] = (out["bb_upper_20"] - out["bb_lower_20"]) / out["bb_mid_20"]
    out["bb_position_20"] = (out["close"] - out["bb_lower_20"]) / (
        out["bb_upper_20"] - out["bb_lower_20"]
    ).replace(0, np.nan)
    out["atr_14"] = average_true_range(out, 14)
    out["atr_pct_14"] = out["atr_14"] / out["close"]
    out["adx_14"], out["plus_di_14"], out["minus_di_14"] = adx_components(out, 14)
    out["stoch_k_14"], out["stoch_d_3"] = stochastic_oscillator(out, 14, 3)
    out["obv"] = on_balance_volume(out)
    out["obv_sma_20"] = out["obv"].rolling(20).mean()
    out["volatility_20d"] = out["return_1d"].rolling(20).std() * math.sqrt(252)
    out["return_skew_20d"] = out["return_1d"].rolling(20).skew()
    out["return_kurtosis_20d"] = out["return_1d"].rolling(20).kurt()
    out["volume_sma_20"] = out["volume"].rolling(20).mean()
    out["volume_z_20"] = (out["volume"] - out["volume_sma_20"]) / out["volume"].rolling(
        20
    ).std()
    out["volume_ratio_20"] = out["volume"] / out["volume_sma_20"]
    out["range_pct"] = (out["high"] - out["low"]) / out["close"]
    out["close_vs_sma20"] = out["close"] / out["sma_20"] - 1
    out["close_vs_sma60"] = out["close"] / out["sma_60"] - 1
    out["day_of_week"] = out.index.dayofweek.astype(float)
    out["month_of_year"] = out.index.month.astype(float)
    next_open = out["open"].shift(-1)
    next_close = out["close"].shift(-1)
    out["next_return"] = next_close.div(next_open).sub(1)
    quality = frame.attrs.get("data_quality_report", {}) or {}
    quarantined_times = pd.to_datetime(
        [
            item.get("time")
            for item in quality.get("quarantine", [])
            if item.get("time") is not None
            and "invalid_time" not in item.get("reasons", [])
            and "duplicate_time" not in item.get("reasons", [])
        ],
        errors="coerce",
    )
    quarantined_times = pd.DatetimeIndex(quarantined_times).dropna()
    invalid_forward_target = pd.Series(False, index=out.index)
    if len(quarantined_times):
        current_dates = out.index[:-1]
        next_dates = out.index[1:]
        for current_date, next_date in zip(current_dates, next_dates):
            if ((quarantined_times > current_date) & (quarantined_times <= next_date)).any():
                invalid_forward_target.loc[current_date] = True
        out.loc[invalid_forward_target, "next_return"] = np.nan
    out["target_next_up"] = (out["next_return"] > 0).astype(float)
    out.loc[out["next_return"].isna(), "target_next_up"] = np.nan
    out.attrs.update(frame.attrs)
    out.attrs["target_definition"] = (
        "signal sau close t; vào open t+1; thoát close t+1"
    )
    out.attrs["targets_invalidated_by_quarantine"] = int(
        invalid_forward_target.sum()
    )
    return out


def latest_model_features(
    frame: pd.DataFrame,
    feature_columns: list[str] | None = None,
) -> pd.DataFrame:
    """Trả về feature mới nhất thực sự và từ chối dữ liệu stale/leakage."""
    if frame.empty:
        raise ValueError("Không có dữ liệu để lấy feature mới nhất.")
    if not frame.index.is_monotonic_increasing or not frame.index.is_unique:
        raise ValueError(
            "Dữ liệu feature phải được sắp xếp tăng dần và không trùng ngày."
        )

    columns = MODEL_FEATURES if feature_columns is None else feature_columns
    missing_columns = [column for column in columns if column not in frame.columns]
    if missing_columns:
        raise ValueError(f"Thiếu feature: {', '.join(missing_columns)}")

    latest = frame.iloc[[-1]]
    known_future_columns = [
        column
        for column in ("target_next_up", "next_return")
        if column in latest.columns and latest[column].notna().any()
    ]
    if known_future_columns:
        raise ValueError(
            "Dòng mới nhất không được có dữ liệu tương lai: "
            + ", ".join(known_future_columns)
        )

    numeric_latest = latest[columns].apply(pd.to_numeric, errors="coerce")
    finite = np.isfinite(numeric_latest.to_numpy(dtype=float)).all(axis=0)
    invalid_features = [
        column for column, is_finite in zip(columns, finite) if not is_finite
    ]
    if invalid_features:
        raise ValueError(
            "Feature mới nhất bị thiếu/không hợp lệ: " + ", ".join(invalid_features)
        )
    return numeric_latest.copy()


def current_levels(frame: pd.DataFrame) -> dict:
    latest = frame.iloc[-1]
    recent20 = frame.tail(20)
    recent60 = frame.tail(60)
    returns = frame["return_1d"].dropna()
    drawdown, peak_date, trough_date = max_drawdown(returns)

    return {
        "latest_date": str(frame.index[-1].date()),
        "latest_close": safe_float(latest["close"]),
        "sma20": safe_float(latest["sma_20"]),
        "sma60": safe_float(latest["sma_60"]),
        "rsi14": safe_float(latest["rsi_14"]),
        "macd": safe_float(latest["macd"]),
        "macd_signal": safe_float(latest["macd_signal"]),
        "macd_hist": safe_float(latest["macd_hist"]),
        "bb_upper20": safe_float(latest["bb_upper_20"]),
        "bb_lower20": safe_float(latest["bb_lower_20"]),
        "bb_width20": safe_float(latest["bb_width_20"]),
        "bb_position20": safe_float(latest["bb_position_20"]),
        "atr14": safe_float(latest["atr_14"]),
        "atr_pct14": safe_float(latest["atr_pct_14"]),
        "adx14": safe_float(latest["adx_14"]),
        "plus_di14": safe_float(latest["plus_di_14"]),
        "minus_di14": safe_float(latest["minus_di_14"]),
        "stoch_k14": safe_float(latest["stoch_k_14"]),
        "stoch_d3": safe_float(latest["stoch_d_3"]),
        "volume_ratio20": safe_float(latest["volume_ratio_20"]),
        "obv": safe_float(latest["obv"]),
        "vol20": safe_float(latest["volatility_20d"]),
        "volume20": safe_float(latest["volume_sma_20"]),
        "support20": safe_float(recent20["low"].min()),
        "resistance20": safe_float(recent20["high"].max()),
        "support60": safe_float(recent60["low"].min()),
        "resistance60": safe_float(recent60["high"].max()),
        "max_drawdown": safe_float(drawdown),
        "drawdown_peak": str(peak_date.date()),
        "drawdown_trough": str(trough_date.date()),
        "var_95_daily": safe_float(returns.quantile(0.05)),
    }


def _signal(name: str, status: str, detail: str, score: int) -> dict:
    return {"name": name, "status": status, "detail": detail, "score": score}


def technical_assessment(levels: dict) -> dict:
    signals: list[dict] = []
    latest = levels["latest_close"]

    if latest > levels["sma20"] > levels["sma60"]:
        signals.append(
            _signal("Xu hướng", "Tích cực", "Giá nằm trên SMA20 và SMA60.", 2)
        )
    elif latest > levels["sma60"]:
        signals.append(
            _signal(
                "Xu hướng", "Trung tính", "Giá trên SMA60 nhưng chưa vượt SMA20.", 0
            )
        )
    else:
        signals.append(_signal("Xu hướng", "Cẩn thận", "Giá nằm dưới SMA60.", -2))

    if levels["macd"] > levels["macd_signal"] and levels["macd_hist"] > 0:
        signals.append(
            _signal("MACD", "Tích cực", "MACD trên signal, histogram dương.", 2)
        )
    elif levels["macd"] < levels["macd_signal"] and levels["macd_hist"] < 0:
        signals.append(
            _signal("MACD", "Cẩn thận", "MACD dưới signal, histogram âm.", -2)
        )
    else:
        signals.append(_signal("MACD", "Trung tính", "MACD chưa xác nhận rõ.", 0))

    rsi_value = levels["rsi14"]
    if rsi_value >= 70:
        signals.append(_signal("RSI14", "Quá mua", f"RSI {rsi_value:.1f}.", -1))
    elif rsi_value <= 30:
        signals.append(_signal("RSI14", "Quá bán", f"RSI {rsi_value:.1f}.", 1))
    elif rsi_value >= 55:
        signals.append(_signal("RSI14", "Tích cực", f"RSI {rsi_value:.1f}.", 1))
    elif rsi_value <= 45:
        signals.append(_signal("RSI14", "Yếu", f"RSI {rsi_value:.1f}.", -1))
    else:
        signals.append(_signal("RSI14", "Trung tính", f"RSI {rsi_value:.1f}.", 0))

    bb_position = levels["bb_position20"]
    if bb_position >= 0.9:
        signals.append(
            _signal("Bollinger", "Gần biên trên", "Giá sát/vượt biên trên.", 0)
        )
    elif bb_position <= 0.1:
        signals.append(
            _signal("Bollinger", "Gần biên dưới", "Giá sát/vượt biên dưới.", -1)
        )
    else:
        signals.append(
            _signal("Bollinger", "Ổn định", "Giá nằm trong dải Bollinger.", 1)
        )

    adx_value = levels["adx14"]
    if adx_value >= 25 and levels["plus_di14"] > levels["minus_di14"]:
        signals.append(
            _signal("ADX", "Xu hướng tăng", f"ADX {adx_value:.1f}, +DI vượt -DI.", 2)
        )
    elif adx_value >= 25 and levels["plus_di14"] < levels["minus_di14"]:
        signals.append(
            _signal("ADX", "Xu hướng giảm", f"ADX {adx_value:.1f}, -DI vượt +DI.", -2)
        )
    else:
        signals.append(_signal("ADX", "Đi ngang", f"ADX {adx_value:.1f}.", 0))

    volume_ratio = levels["volume_ratio20"]
    if volume_ratio >= 1.5:
        signals.append(
            _signal("Thanh khoản", "Đột biến", f"{volume_ratio:.2f} lần trung bình.", 1)
        )
    elif volume_ratio <= 0.7:
        signals.append(
            _signal("Thanh khoản", "Thấp", f"{volume_ratio:.2f} lần trung bình.", -1)
        )
    else:
        signals.append(
            _signal(
                "Thanh khoản", "Bình thường", f"{volume_ratio:.2f} lần trung bình.", 0
            )
        )

    if levels["stoch_k14"] > levels["stoch_d3"] and levels["stoch_k14"] < 80:
        signals.append(_signal("Stochastic", "Hồi phục", "%K nằm trên %D.", 1))
    elif levels["stoch_k14"] < levels["stoch_d3"] and levels["stoch_k14"] > 20:
        signals.append(_signal("Stochastic", "Yếu lại", "%K nằm dưới %D.", -1))
    else:
        signals.append(
            _signal(
                "Stochastic",
                "Cực trị",
                f"%K {levels['stoch_k14']:.1f}, %D {levels['stoch_d3']:.1f}.",
                0,
            )
        )

    score = int(sum(item["score"] for item in signals))
    if score >= 5:
        bias = "Tích cực"
    elif score >= 2:
        bias = "Hồi phục / nghiêng tăng"
    elif score <= -5:
        bias = "Tiêu cực"
    elif score <= -2:
        bias = "Suy yếu / cẩn thận"
    else:
        bias = "Trung tính"
    return {"score": score, "bias": bias, "signals": signals}
