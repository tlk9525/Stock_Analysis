from __future__ import annotations

import csv
import subprocess
import sys
from datetime import datetime
from pathlib import Path


SYMBOLS = [
    "ACB",
    "BID",
    "CTG",
    "FPT",
    "GMD",
    "HCM",
    "HPG",
    "KDH",
    "MBB",
    "MSN",
    "MWG",
    "NVL",
    "PLX",
    "PNJ",
    "POW",
    "SAB",
    "SSI",
    "STB",
    "TCB",
    "VCB",
    "VHM",
    "VIC",
    "VNM",
]


def _report_dir(output: str) -> str:
    marker = "Báo cáo nằm ở: "
    paths = [line.split(marker, 1)[1].strip() for line in output.splitlines() if marker in line]
    return paths[-1] if paths else ""


def main() -> int:
    news_csv = Path("data/news_articles.csv")
    if not news_csv.exists():
        raise SystemExit("Thiếu data/news_articles.csv. Hãy chạy export-news-history hoặc collect-news trước.")
    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_path = Path("reports") / f"symbol_news_train_batch_{stamp}.csv"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["symbol", "status", "report_dir", "error"])
        writer.writeheader()
        for symbol in SYMBOLS:
            print(f"=== train-symbol-news {symbol} ===", flush=True)
            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "src.finai_cli",
                    "train-symbol-news",
                    symbol,
                    "--news-articles-csv",
                    str(news_csv),
                    "--lookback-days",
                    "5",
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            output = "\n".join(part for part in [completed.stdout, completed.stderr] if part)
            print("\n".join(output.splitlines()[-5:]), flush=True)
            if completed.returncode == 0:
                writer.writerow(
                    {
                        "symbol": symbol,
                        "status": "ok",
                        "report_dir": _report_dir(output),
                        "error": "",
                    }
                )
            else:
                writer.writerow(
                    {
                        "symbol": symbol,
                        "status": "fail",
                        "report_dir": "",
                        "error": " ".join(output.splitlines()[-20:])[:800],
                    }
                )
            file.flush()
    print(log_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
