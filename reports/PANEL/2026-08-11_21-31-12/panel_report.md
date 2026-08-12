# Báo cáo panel cổ phiếu Việt Nam

- Dữ liệu: 2008-03-10 -> 2026-08-11.
- Universe (12 mã): FPT, GAS, HCM, HPG, MBB, MWG, SSI, TCB, VCB, VHM, VIC, VNM.
- Benchmark: VNINDEX.
- Timing: feature sau close t; vào lệnh open t+1; thoát close t+h.
- Chi phí: 50.0 bps full round-trip cho từng cohort.
- Data quarantine: 1368 dòng.
- Cảnh báo: universe cố định theo cấu hình hiện tại nên vẫn có survivorship bias; cần universe point-in-time trước khi dùng cho nghiên cứu production.
- Cần xác minh dữ liệu giá đã điều chỉnh corporate action nhất quán giữa các mã.

## Horizon 5 phiên - NO_EDGE

- OOS Rank IC mean: -0.007 (316 ngày); HAC t-stat -0.21 với lag 4.
- Top-3 net return: 16.05%; Sharpe 0.50; max drawdown -34.31%.
- Selection turnover trung bình: 45.57%; 64 cohort, mỗi cohort chịu full round-trip cost.
- Guard fail: positive_rank_ic, rank_ic_hac_significance.

| Rank | Mã | Dự báo excess return | Percentile |
|---:|---|---:|---:|
| 1 | GAS | 0.44% | 100.00% |
| 2 | VCB | 0.40% | 91.67% |
| 3 | FPT | 0.39% | 83.33% |
| 4 | VHM | 0.25% | 75.00% |
| 5 | HCM | 0.21% | 66.67% |
| 6 | MBB | 0.21% | 58.33% |
| 7 | SSI | 0.15% | 50.00% |
| 8 | MWG | 0.15% | 41.67% |
| 9 | VNM | 0.14% | 33.33% |
| 10 | TCB | 0.11% | 25.00% |

### Kết quả theo market regime

- bear: net return 1.42%; Sharpe 0.34; Rank IC -0.112.
- bull: net return -13.16%; Sharpe -0.77; Rank IC 0.024.
- sideways: net return 31.77%; Sharpe 1.47; Rank IC 0.012.

## Horizon 20 phiên - NO_EDGE

- OOS Rank IC mean: 0.036 (334 ngày); HAC t-stat 0.79 với lag 19.
- Top-3 net return: 82.74%; Sharpe 1.42; max drawdown -16.42%.
- Selection turnover trung bình: 61.76%; 17 cohort, mỗi cohort chịu full round-trip cost.
- Guard fail: rank_ic_hac_significance.

| Rank | Mã | Dự báo excess return | Percentile |
|---:|---|---:|---:|
| 1 | GAS | 1.63% | 100.00% |
| 2 | MWG | 1.30% | 91.67% |
| 3 | SSI | 1.16% | 83.33% |
| 4 | FPT | 1.13% | 70.83% |
| 5 | VCB | 1.13% | 70.83% |
| 6 | TCB | 0.89% | 58.33% |
| 7 | VHM | 0.78% | 50.00% |
| 8 | VNM | 0.75% | 41.67% |
| 9 | HCM | 0.68% | 33.33% |
| 10 | MBB | 0.55% | 25.00% |

### Kết quả theo market regime

- bear: net return 31.08%; Sharpe 6.40; Rank IC 0.074.
- bull: net return 22.55%; Sharpe 0.91; Rank IC -0.010.
- sideways: net return 13.77%; Sharpe 1.12; Rank IC 0.071.

Lưu ý: ranking chỉ được xem là bảng xếp hạng nghiên cứu khi guard đạt; không phải khuyến nghị mua/bán.
