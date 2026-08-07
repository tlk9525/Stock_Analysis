# Báo cáo panel cổ phiếu Việt Nam

- Dữ liệu: 2008-03-11 -> 2026-08-07.
- Universe (5 mã): FPT, HPG, MWG, VCB, VNM.
- Benchmark: VNINDEX.
- Timing: feature sau close t; vào lệnh open t+1; thoát close t+h.
- Chi phí: 50.0 bps full round-trip cho từng cohort.
- Data quarantine: 41 dòng.
- Cảnh báo: universe cố định theo cấu hình hiện tại nên vẫn có survivorship bias; cần universe point-in-time trước khi dùng cho nghiên cứu production.
- Cần xác minh dữ liệu giá đã điều chỉnh corporate action nhất quán giữa các mã.

## Horizon 5 phiên - NO_EDGE

- OOS Rank IC mean: 0.045 (346 ngày); HAC t-stat 1.10 với lag 4.
- Top-3 net return: -46.08%; Sharpe -1.69; max drawdown -48.74%.
- Selection turnover trung bình: 24.05%; 70 cohort, mỗi cohort chịu full round-trip cost.
- Guard fail: rank_ic_hac_significance, positive_net_return, positive_sharpe.

| Rank | Mã | Dự báo excess return | Percentile |
|---:|---|---:|---:|
| 1 | VCB | 0.24% | 100.00% |
| 2 | FPT | 0.23% | 80.00% |
| 3 | HPG | 0.11% | 60.00% |
| 4 | MWG | 0.05% | 40.00% |
| 5 | VNM | -0.05% | 20.00% |

### Kết quả theo market regime

- bear: net return -3.37%; Sharpe -0.47; Rank IC 0.036.
- bull: net return -14.71%; Sharpe -1.36; Rank IC 0.076.
- sideways: net return -34.58%; Sharpe -2.51; Rank IC 0.014.

## Horizon 20 phiên - NO_EDGE

- OOS Rank IC mean: -0.018 (359 ngày); HAC t-stat -0.33 với lag 19.
- Top-3 net return: -13.30%; Sharpe -0.36; max drawdown -19.77%.
- Selection turnover trung bình: 34.21%; 19 cohort, mỗi cohort chịu full round-trip cost.
- Guard fail: positive_rank_ic, rank_ic_hac_significance, positive_net_return, positive_sharpe.

| Rank | Mã | Dự báo excess return | Percentile |
|---:|---|---:|---:|
| 1 | VCB | 0.94% | 100.00% |
| 2 | HPG | 0.79% | 80.00% |
| 3 | FPT | 0.77% | 60.00% |
| 4 | VNM | 0.71% | 40.00% |
| 5 | MWG | -0.06% | 20.00% |

### Kết quả theo market regime

- bear: net return -5.21%; Sharpe -0.45; Rank IC -0.129.
- bull: net return -3.25%; Sharpe -0.19; Rank IC 0.016.
- sideways: net return -5.46%; Sharpe -0.40; Rank IC -0.007.

Lưu ý: ranking chỉ được xem là bảng xếp hạng nghiên cứu khi guard đạt; không phải khuyến nghị mua/bán.
