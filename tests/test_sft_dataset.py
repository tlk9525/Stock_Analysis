from __future__ import annotations

import json

from src.ai.sft_dataset import build_dataset, examples_from_report


def _write_report(artifact, symbol: str) -> None:
    artifact.mkdir(parents=True)
    (artifact / "signal_decision.json").write_text(
        json.dumps({"status": "NO_EDGE", "reasons": ["Frozen holdout chưa đủ trade"]}),
        encoding="utf-8",
    )
    (artifact / "fundamental_summary.json").write_text(json.dumps({"symbol": symbol}), encoding="utf-8")
    (artifact / "latest_levels.json").write_text(
        json.dumps({"sma20": 20.0, "sma60": 21.0, "rsi14": 42.0, "macd_hist": -0.2}),
        encoding="utf-8",
    )
    (artifact / "technical_assessment.json").write_text(
        json.dumps({"bias": "Tiêu cực", "score": -2}), encoding="utf-8"
    )


def test_examples_are_report_scoped_and_keep_dynamic_prices_out_of_training(tmp_path) -> None:
    artifact = tmp_path / "reports" / "VIC" / "run-1" / "all_files"
    _write_report(artifact, "VIC")

    examples = examples_from_report(artifact)

    assert len(examples) == 6
    assert {row["metadata"]["symbol"] for row in examples} == {"VIC"}
    lookup = next(row for row in examples if row["metadata"]["intent"] == "historical_lookup")
    assert "history_features.csv" in lookup["messages"][-1]["content"]
    assert "215,50" not in lookup["messages"][-1]["content"]


def test_dataset_builder_creates_train_eval_and_manifest(tmp_path) -> None:
    reports = tmp_path / "reports"
    for index in range(30):
        _write_report(reports / f"SYM{index:02}" / "run-1" / "all_files", f"SYM{index:02}")
    output = tmp_path / "output"

    counts = build_dataset(reports, output, reports_per_symbol=1)

    assert counts["train"] > 0
    assert counts["eval"] > 0
    assert (output / "stocklens_train.jsonl").is_file()
    assert json.loads((output / "manifest.json").read_text(encoding="utf-8"))["schema"] == "chat_messages_v1"
