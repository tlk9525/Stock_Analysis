from __future__ import annotations

import math

import numpy as np
import pandas as pd

from src.utils import safe_float


MODEL_FEATURES = [
    "return_1d",
    "return_5d",
    "return_20d",
    "rsi_14",
    "macd",
    "macd_hist",
    "volatility_20d",
    "volume_z_20",
    "volume_ratio_20",
    "range_pct",
    "close_vs_sma20",
    "close_vs_sma60",
    "bb_position_20",
    "atr_pct_14",
    "adx_14",
    "stoch_k_14",
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
    return true_range(frame).ewm(
        alpha=1 / window,
        adjust=False,
        min_periods=window,
    ).mean()


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
        100
        * (plus_di - minus_di).abs()
        / (plus_di + minus_di).replace(0, np.nan)
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
    k_value = (
        100
        * (frame["close"] - low_min)
        / (high_max - low_min).replace(0, np.nan)
    )
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
    out["return_5d"] = out["close"].pct_change(5)
    out["return_20d"] = out["close"].pct_change(20)
    out["sma_5"] = out["close"].rolling(5).mean()
    out["sma_20"] = out["close"].rolling(20).mean()
    out["sma_60"] = out["close"].rolling(60).mean()
    out["ema_12"] = out["close"].ewm(span=12, adjust=False).mean()
    out["ema_26"] = out["close"].ewm(span=26, adjust=False).mean()
    out["macd"] = out["ema_12"] - out["ema_26"]
    out["macd_signal"] = out["macd"].ewm(span=9, adjust=False).mean()
    out["macd_hist"] = out["macd"] - out["macd_signal"]
    out["rsi_14"] = rsi(out["close"], 14)
    out["bb_mid_20"] = out["sma_20"]
    out["bb_std_20"] = out["close"].rolling(20).std()
    out["bb_upper_20"] = out["bb_mid_20"] + 2 * out["bb_std_20"]
    out["bb_lower_20"] = out["bb_mid_20"] - 2 * out["bb_std_20"]
    out["bb_width_20"] = (
        (out["bb_upper_20"] - out["bb_lower_20"]) / out["bb_mid_20"]
    )
    out["bb_position_20"] = (
        (out["close"] - out["bb_lower_20"])
        / (out["bb_upper_20"] - out["bb_lower_20"]).replace(0, np.nan)
    )
    out["atr_14"] = average_true_range(out, 14)
    out["atr_pct_14"] = out["atr_14"] / out["close"]
    out["adx_14"], out["plus_di_14"], out["minus_di_14"] = adx_components(out, 14)
    out["stoch_k_14"], out["stoch_d_3"] = stochastic_oscillator(out, 14, 3)
    out["obv"] = on_balance_volume(out)
    out["obv_sma_20"] = out["obv"].rolling(20).mean()
    out["volatility_20d"] = out["return_1d"].rolling(20).std() * math.sqrt(252)
    out["volume_sma_20"] = out["volume"].rolling(20).mean()
    out["volume_z_20"] = (
        (out["volume"] - out["volume_sma_20"])
        / out["volume"].rolling(20).std()
    )
    out["volume_ratio_20"] = out["volume"] / out["volume_sma_20"]
    out["range_pct"] = (out["high"] - out["low"]) / out["close"]
    out["close_vs_sma20"] = out["close"] / out["sma_20"] - 1
    out["close_vs_sma60"] = out["close"] / out["sma_60"] - 1
    out["target_next_up"] = (out["close"].shift(-1) > out["close"]).astype(int)
    out["next_return"] = out["close"].pct_change().shift(-1)
    return out


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
        signals.append(_signal("Trend", "Tich cuc", "Gia nam tren SMA20 va SMA60.", 2))
    elif latest > levels["sma60"]:
        signals.append(_signal("Trend", "Trung tinh", "Gia tren SMA60 nhung chua vuot SMA20.", 0))
    else:
        signals.append(_signal("Trend", "Can than", "Gia nam duoi SMA60.", -2))

    if levels["macd"] > levels["macd_signal"] and levels["macd_hist"] > 0:
        signals.append(_signal("MACD", "Tich cuc", "MACD tren signal, histogram duong.", 2))
    elif levels["macd"] < levels["macd_signal"] and levels["macd_hist"] < 0:
        signals.append(_signal("MACD", "Can than", "MACD duoi signal, histogram am.", -2))
    else:
        signals.append(_signal("MACD", "Trung tinh", "MACD chua xac nhan ro.", 0))

    rsi_value = levels["rsi14"]
    if rsi_value >= 70:
        signals.append(_signal("RSI14", "Qua mua", f"RSI {rsi_value:.1f}.", -1))
    elif rsi_value <= 30:
        signals.append(_signal("RSI14", "Qua ban", f"RSI {rsi_value:.1f}.", 1))
    elif rsi_value >= 55:
        signals.append(_signal("RSI14", "Tich cuc", f"RSI {rsi_value:.1f}.", 1))
    elif rsi_value <= 45:
        signals.append(_signal("RSI14", "Yeu", f"RSI {rsi_value:.1f}.", -1))
    else:
        signals.append(_signal("RSI14", "Trung tinh", f"RSI {rsi_value:.1f}.", 0))

    bb_position = levels["bb_position20"]
    if bb_position >= 0.9:
        signals.append(_signal("Bollinger", "Gan bien tren", "Gia sat/vuot bien tren.", 0))
    elif bb_position <= 0.1:
        signals.append(_signal("Bollinger", "Gan bien duoi", "Gia sat/vuot bien duoi.", -1))
    else:
        signals.append(_signal("Bollinger", "On dinh", "Gia nam trong dai Bollinger.", 1))

    adx_value = levels["adx14"]
    if adx_value >= 25 and levels["plus_di14"] > levels["minus_di14"]:
        signals.append(_signal("ADX", "Xu huong tang", f"ADX {adx_value:.1f}, +DI vuot -DI.", 2))
    elif adx_value >= 25 and levels["plus_di14"] < levels["minus_di14"]:
        signals.append(_signal("ADX", "Xu huong giam", f"ADX {adx_value:.1f}, -DI vuot +DI.", -2))
    else:
        signals.append(_signal("ADX", "Di ngang", f"ADX {adx_value:.1f}.", 0))

    volume_ratio = levels["volume_ratio20"]
    if volume_ratio >= 1.5:
        signals.append(_signal("Thanh khoan", "Dot bien", f"{volume_ratio:.2f} lan trung binh.", 1))
    elif volume_ratio <= 0.7:
        signals.append(_signal("Thanh khoan", "Thap", f"{volume_ratio:.2f} lan trung binh.", -1))
    else:
        signals.append(_signal("Thanh khoan", "Binh thuong", f"{volume_ratio:.2f} lan trung binh.", 0))

    if levels["stoch_k14"] > levels["stoch_d3"] and levels["stoch_k14"] < 80:
        signals.append(_signal("Stochastic", "Hoi phuc", "%K nam tren %D.", 1))
    elif levels["stoch_k14"] < levels["stoch_d3"] and levels["stoch_k14"] > 20:
        signals.append(_signal("Stochastic", "Yeu lai", "%K nam duoi %D.", -1))
    else:
        signals.append(
            _signal(
                "Stochastic",
                "Cuc tri",
                f"%K {levels['stoch_k14']:.1f}, %D {levels['stoch_d3']:.1f}.",
                0,
            )
        )

    score = int(sum(item["score"] for item in signals))
    if score >= 5:
        bias = "Tich cuc"
    elif score >= 2:
        bias = "Hoi phuc / nghieng tang"
    elif score <= -5:
        bias = "Tieu cuc"
    elif score <= -2:
        bias = "Suy yeu / can than"
    else:
        bias = "Trung tinh"
    return {"score": score, "bias": bias, "signals": signals}

