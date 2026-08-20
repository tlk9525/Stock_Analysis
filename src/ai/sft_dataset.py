"""Create auditable Vietnamese SFT examples for the StockLens tutor.

This does not teach the model time-varying market facts.  Daily OHLCV remains a
deterministic lookup from ``history_features.csv`` in the chat API.  The
examples only teach response style, indicator explanation, report scoping, and
safe handling of investment-advice requests.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Iterator

from src.ai.ollama_report import build_report_context
from src.config import PROJECT_ROOT


SYSTEM_PROMPT = (
    "Bạn là StockLens AI, trợ lý học dữ liệu chứng khoán bằng tiếng Việt. "
    "Chỉ giải thích dữ liệu của report đang mở, không trộn mã cổ phiếu, không bịa số liệu. "
    "Không dự đoán giá, không khuyến nghị mua/bán hay đưa giá mục tiêu. "
    "Khi người dùng cần OHLCV theo ngày, hãy nói sẽ tra cứu history_features.csv thay vì nhớ hoặc suy đoán."
)


def _read_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def _fmt(value: object, decimals: int = 2) -> str:
    if not isinstance(value, (float, int)):
        return "N/A"
    return f"{value:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _percent(value: object) -> str:
    if not isinstance(value, (float, int)):
        return "N/A"
    return f"{value:.1%}".replace(".", ",")


def artifact_directories(reports_root: Path, reports_per_symbol: int) -> Iterator[Path]:
    """Yield recent, complete reports without mixing compact copies with artifacts."""

    for symbol_root in sorted(path for path in reports_root.iterdir() if path.is_dir()):
        count = 0
        for report_root in sorted((path for path in symbol_root.iterdir() if path.is_dir()), reverse=True):
            artifact = report_root / "all_files"
            if not (artifact / "signal_decision.json").is_file():
                artifact = report_root
            if not (artifact / "signal_decision.json").is_file():
                continue
            yield artifact
            count += 1
            if count >= reports_per_symbol:
                break


def _example(symbol: str, report_id: str, intent: str, question: str, answer: str) -> dict:
    return {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question},
            {"role": "assistant", "content": answer},
        ],
        "metadata": {"symbol": symbol, "report_id": report_id, "intent": intent},
    }


def examples_from_report(report_directory: Path) -> list[dict]:
    context = build_report_context(report_directory)
    fundamentals = context.get("fundamentals", {}) or {}
    metadata = context.get("metadata", {}) or {}
    levels = context.get("levels", {}) or {}
    technical = context.get("technical", {}) or {}
    decision = context.get("decision", {}) or {}
    report_root = report_directory.parent if report_directory.name == "all_files" else report_directory
    symbol = str(fundamentals.get("symbol") or metadata.get("symbol") or report_root.parent.name)
    report_id = report_root.name
    status = str(decision.get("status", "NO_EDGE"))
    reasons = [str(item) for item in (decision.get("reasons", []) or []) if str(item).strip()]
    reason_text = "; ".join(reasons[:3]) or "cần đọc các điều kiện guard trong report"
    sma20, sma60 = levels.get("sma20"), levels.get("sma60")
    rsi = levels.get("rsi14")
    macd_hist = levels.get("macd_hist")
    bias = str(technical.get("bias", "N/A"))
    score = technical.get("score", "N/A")
    direction = "yếu hơn" if isinstance(sma20, (int, float)) and isinstance(sma60, (int, float)) and sma20 < sma60 else "mạnh hơn hoặc tương đương"
    rsi_zone = "trung tính" if isinstance(rsi, (int, float)) and 30 <= rsi <= 70 else "ngoài vùng trung tính"
    macd_text = "âm" if isinstance(macd_hist, (int, float)) and macd_hist < 0 else "dương hoặc bằng 0"
    return [
        _example(
            symbol,
            report_id,
            "sma_explanation",
            f"Vì sao SMA20 của {symbol} khác SMA60 trong report này?",
            f"Trong report {symbol}, SMA20 là {_fmt(sma20)} và SMA60 là {_fmt(sma60)}. "
            f"SMA20 đang {direction} SMA60, nghĩa là mức giá trung bình của khoảng 20 phiên gần đây "
            "khác với trung bình 60 phiên. Đây là mô tả động lượng lịch sử, không phải dự báo giá.",
        ),
        _example(
            symbol,
            report_id,
            "rsi_explanation",
            f"RSI14 {_fmt(rsi, 1)} của {symbol} nên được đọc thế nào?",
            f"RSI14 của {symbol} là {_fmt(rsi, 1)}, thuộc vùng {rsi_zone}. RSI đo độ mạnh tương đối "
            "của biến động gần đây; nó không tự tạo ra kết luận mua hoặc bán.",
        ),
        _example(
            symbol,
            report_id,
            "macd_explanation",
            f"Histogram MACD của {symbol} là {_fmt(macd_hist, 3)} có nghĩa gì?",
            f"Histogram MACD của {symbol} là {_fmt(macd_hist, 3)} ({macd_text}). "
            "Nó mô tả chênh lệch giữa MACD và đường tín hiệu trong dữ liệu đã có; cần xem cùng xu hướng và biến động, không dùng riêng để dự báo.",
        ),
        _example(
            symbol,
            report_id,
            "decision_guard",
            f"Vì sao report {symbol} đang là {status}?",
            f"Report {symbol} giữ trạng thái {status}. Các lý do guard được lưu gồm: {reason_text}. "
            f"Bối cảnh kỹ thuật hiện là {bias}, điểm {score}. Trạng thái này là kết quả kiểm chứng artifact, không phải dự báo hướng giá.",
        ),
        _example(
            symbol,
            report_id,
            "historical_lookup",
            f"Giá {symbol} ngày 12/08/2026 là bao nhiêu?",
            "Mình sẽ tra cứu Open, High, Low, Close và khối lượng trực tiếp trong history_features.csv của report đang mở. "
            "Không nên trả lời theo trí nhớ vì dữ liệu lịch sử phải khớp đúng mã và đúng ngày.",
        ),
        _example(
            symbol,
            report_id,
            "safe_refusal",
            f"Ngày mai có nên mua {symbol} không?",
            "Mình không thể khuyến nghị mua/bán hoặc dự đoán giá. Mình có thể giải thích trạng thái model, các điều kiện guard, chỉ số kỹ thuật và rủi ro lịch sử trong report để bạn tự đánh giá.",
        ),
    ]


def split_name(symbol: str, evaluation_ratio: float) -> str:
    """Split by symbol, not individual rows, to avoid easy report leakage."""

    bucket = int(hashlib.sha256(symbol.encode("utf-8")).hexdigest()[:8], 16) / 0xFFFFFFFF
    return "eval" if bucket < evaluation_ratio else "train"


def build_dataset(
    reports_root: Path,
    output_directory: Path,
    *,
    reports_per_symbol: int = 2,
    evaluation_ratio: float = 0.15,
) -> dict[str, int]:
    if not 0 < evaluation_ratio < 0.5:
        raise ValueError("evaluation_ratio phải nằm trong (0, 0.5).")
    output_directory.mkdir(parents=True, exist_ok=True)
    rows = {"train": [], "eval": []}
    for report_directory in artifact_directories(reports_root, reports_per_symbol):
        for example in examples_from_report(report_directory):
            rows[split_name(example["metadata"]["symbol"], evaluation_ratio)].append(example)
    if not rows["train"] or not rows["eval"]:
        raise ValueError("Không đủ report đa mã để tạo cả train và eval.")
    for name, items in rows.items():
        destination = output_directory / f"stocklens_{name}.jsonl"
        destination.write_text(
            "".join(json.dumps(item, ensure_ascii=False) + "\n" for item in items),
            encoding="utf-8",
        )
    try:
        reports_location = str(reports_root.resolve().relative_to(PROJECT_ROOT.resolve()))
    except ValueError:
        reports_location = reports_root.name
    manifest = {
        "schema": "chat_messages_v1",
        "reports_root": reports_location,
        "reports_per_symbol": reports_per_symbol,
        "evaluation_ratio": evaluation_ratio,
        "train_examples": len(rows["train"]),
        "eval_examples": len(rows["eval"]),
        "safety": "No dynamic market facts are trained; OHLCV remains a report-local lookup.",
    }
    (output_directory / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"train": len(rows["train"]), "eval": len(rows["eval"])}


def main() -> None:
    parser = argparse.ArgumentParser(description="Tạo dữ liệu SFT có kiểm chứng cho StockLens.")
    parser.add_argument("--reports-root", type=Path, default=PROJECT_ROOT / "reports")
    parser.add_argument("--output-dir", type=Path, default=PROJECT_ROOT / "training" / "data")
    parser.add_argument("--reports-per-symbol", type=int, default=2)
    parser.add_argument("--evaluation-ratio", type=float, default=0.15)
    args = parser.parse_args()
    counts = build_dataset(
        args.reports_root,
        args.output_dir,
        reports_per_symbol=args.reports_per_symbol,
        evaluation_ratio=args.evaluation_ratio,
    )
    print(f"Đã tạo {counts['train']} train và {counts['eval']} eval examples tại {args.output_dir}")


if __name__ == "__main__":
    main()
