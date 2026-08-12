# Báo cáo panel cổ phiếu Việt Nam

- Dữ liệu: 2008-03-06 -> 2026-08-11.
- Universe (7 mã): ACB, BID, CTG, MBB, STB, TCB, VCB.
- Benchmark: VNINDEX.
- Timing: feature sau close t; vào lệnh open t+1; thoát close t+h.
- Chi phí: 50.0 bps full round-trip cho từng cohort.
- Data quarantine: 36 dòng.
- Cảnh báo: universe cố định theo cấu hình hiện tại nên vẫn có survivorship bias; cần universe point-in-time trước khi dùng cho nghiên cứu production.
- Cần xác minh dữ liệu giá đã điều chỉnh corporate action nhất quán giữa các mã.

## Horizon 5 phiên - NO_EDGE

- OOS Rank IC mean: 0.007 (303 ngày); HAC t-stat 0.17 với lag 4.
- Top-3 net return: -28.14%; Sharpe -0.81; max drawdown -38.82%.
- Selection turnover trung bình: 40.36%; 64 cohort, mỗi cohort chịu full round-trip cost.
- Guard fail: rank_ic_hac_significance, positive_net_return, positive_sharpe.

| Rank | Mã | Dự báo excess return | Percentile |
|---:|---|---:|---:|
| 1 | CTG | 0.14% | 100.00% |
| 2 | VCB | 0.10% | 85.71% |
| 3 | STB | 0.10% | 71.43% |
| 4 | ACB | 0.08% | 50.00% |
| 5 | MBB | 0.08% | 50.00% |
| 6 | BID | -0.03% | 28.57% |
| 7 | TCB | -0.06% | 14.29% |

### Kết quả theo market regime

- bear: net return -10.42%; Sharpe -2.39; Rank IC -0.104.
- bull: net return -20.17%; Sharpe -1.83; Rank IC 0.102.
- sideways: net return 0.49%; Sharpe 0.21; Rank IC -0.043.

## Horizon 20 phiên - NO_EDGE

- OOS Rank IC mean: 0.061 (316 ngày); HAC t-stat 1.02 với lag 19.
- Top-3 net return: 21.05%; Sharpe 0.67; max drawdown -13.88%.
- Selection turnover trung bình: 50.00%; 17 cohort, mỗi cohort chịu full round-trip cost.
- Guard fail: rank_ic_hac_significance.

| Rank | Mã | Dự báo excess return | Percentile |
|---:|---|---:|---:|
| 1 | VCB | -0.15% | 100.00% |
| 2 | STB | -0.18% | 85.71% |
| 3 | ACB | -0.20% | 71.43% |
| 4 | CTG | -0.20% | 57.14% |
| 5 | BID | -0.23% | 42.86% |
| 6 | TCB | -0.26% | 28.57% |
| 7 | MBB | -0.35% | 14.29% |

### Kết quả theo market regime

- bear: net return 13.68%; Sharpe 12.06; Rank IC 0.153.
- bull: net return 31.56%; Sharpe 1.72; Rank IC 0.049.
- sideways: net return -19.06%; Sharpe -1.71; Rank IC 0.026.

Lưu ý: ranking chỉ được xem là bảng xếp hạng nghiên cứu khi guard đạt; không phải khuyến nghị mua/bán.
