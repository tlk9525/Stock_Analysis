# Báo cáo panel cổ phiếu Việt Nam

- Dữ liệu: 2008-03-07 -> 2026-08-05.
- Universe (12 mã): FPT, GAS, HCM, HPG, MBB, MWG, SSI, TCB, VCB, VHM, VIC, VNM.
- Benchmark: VNINDEX.
- Timing: feature sau close t; vào lệnh open t+1; thoát close t+h.
- Chi phí: 50.0 bps full round-trip cho từng cohort.
- Data quarantine: 1368 dòng.
- Cảnh báo: universe cố định theo cấu hình hiện tại nên vẫn có survivorship bias; cần universe point-in-time trước khi dùng cho nghiên cứu production.
- Cần xác minh dữ liệu giá đã điều chỉnh corporate action nhất quán giữa các mã.

## Horizon 5 phiên - NO_EDGE

- OOS Rank IC mean: 0.010 (376 ngày); HAC t-stat 0.36 với lag 4.
- Top-3 net return: 29.68%; Sharpe 0.68; max drawdown -28.99%.
- Selection turnover trung bình: 43.64%; 76 cohort, mỗi cohort chịu full round-trip cost.
- Guard fail: rank_ic_hac_significance.

| Rank | Mã | Dự báo excess return | Percentile |
|---:|---|---:|---:|
| 1 | VHM | 0.73% | 100.00% |
| 2 | MBB | 0.38% | 91.67% |
| 3 | VCB | 0.31% | 83.33% |
| 4 | SSI | 0.25% | 75.00% |
| 5 | FPT | 0.17% | 66.67% |
| 6 | VIC | 0.13% | 58.33% |
| 7 | HPG | 0.10% | 50.00% |
| 8 | HCM | 0.09% | 41.67% |
| 9 | MWG | 0.05% | 33.33% |
| 10 | TCB | 0.03% | 25.00% |

### Kết quả theo market regime

- bear: net return 11.36%; Sharpe 1.26; Rank IC -0.091.
- bull: net return 53.27%; Sharpe 1.87; Rank IC 0.066.
- sideways: net return -24.02%; Sharpe -1.69; Rank IC 0.000.

## Horizon 20 phiên - NO_EDGE

- OOS Rank IC mean: 0.044 (331 ngày); HAC t-stat 1.01 với lag 19.
- Top-3 net return: 120.27%; Sharpe 1.66; max drawdown -12.78%.
- Selection turnover trung bình: 57.84%; 17 cohort, mỗi cohort chịu full round-trip cost.
- Guard fail: rank_ic_hac_significance.

| Rank | Mã | Dự báo excess return | Percentile |
|---:|---|---:|---:|
| 1 | VHM | 1.58% | 100.00% |
| 2 | SSI | 1.40% | 91.67% |
| 3 | FPT | 1.37% | 83.33% |
| 4 | VCB | 1.31% | 75.00% |
| 5 | HPG | 1.22% | 66.67% |
| 6 | VIC | 0.78% | 58.33% |
| 7 | VNM | 0.71% | 50.00% |
| 8 | MBB | 0.69% | 41.67% |
| 9 | GAS | 0.67% | 33.33% |
| 10 | TCB | 0.46% | 25.00% |

### Kết quả theo market regime

- bear: net return 42.27%; Sharpe 3.90; Rank IC 0.007.
- bull: net return 27.34%; Sharpe 1.27; Rank IC 0.012.
- sideways: net return 21.58%; Sharpe 1.17; Rank IC 0.105.

Lưu ý: ranking chỉ được xem là bảng xếp hạng nghiên cứu khi guard đạt; không phải khuyến nghị mua/bán.
