# Báo cáo panel cổ phiếu Việt Nam

- Dữ liệu: 2008-03-10 -> 2026-08-13.
- Universe (12 mã): FPT, GAS, HCM, HPG, MBB, MWG, SSI, TCB, VCB, VHM, VIC, VNM.
- Benchmark: VNINDEX.
- Timing: feature sau close t; vào lệnh open t+1; thoát close t+h.
- Chi phí: 50.0 bps cho mỗi vị thế mua-bán hoàn tất.
- Tối đa 3 vị thế; tiền mặt là mặc định nếu không mã nào vượt phí + margin.
- Data quarantine: 1368 dòng.
- Cảnh báo: universe cố định theo cấu hình hiện tại nên vẫn có survivorship bias; cần universe point-in-time trước khi dùng cho nghiên cứu production.
- Cần xác minh dữ liệu giá đã điều chỉnh corporate action nhất quán giữa các mã.

## Horizon 5 phiên - NO_EDGE

- OOS Rank IC mean: 0.002 (252 ngày); HAC t-stat 0.07 với lag 4.
- Sparse portfolio net return: 0.00%; Sharpe N/A; max drawdown 0.00%.
- 0 vòng hoàn tất; no-trade 100.00%; nắm giữ trung bình N/A phiên.
- Turnover năm: 0.00x; chi phí chỉ tính cho vị thế thật sự được mở.
- Guard fail: entry_rule_selected, rank_ic_hac_significance, positive_net_return, positive_sharpe, enough_completed_round_trips, positive_cost_stress_return, positive_cost_stress_sharpe, positive_development_net_return.

| Rank | Mã | Dự báo excess return | Percentile |
|---:|---|---:|---:|
| 1 | GAS | 0.48% | 100.00% |
| 2 | HCM | 0.34% | 91.67% |
| 3 | VCB | 0.24% | 83.33% |
| 4 | VHM | 0.23% | 75.00% |
| 5 | VNM | 0.22% | 66.67% |
| 6 | TCB | 0.15% | 58.33% |
| 7 | SSI | 0.08% | 50.00% |
| 8 | MWG | 0.08% | 41.67% |
| 9 | MBB | 0.07% | 33.33% |
| 10 | FPT | 0.02% | 25.00% |

### Kết quả theo market regime

- bear: net return 0.00%; Sharpe N/A; Rank IC 0.109.
- bull: net return 0.00%; Sharpe N/A; Rank IC 0.135.
- sideways: net return 0.00%; Sharpe N/A; Rank IC -0.009.

## Horizon 10 phiên - NO_EDGE

- OOS Rank IC mean: 0.005 (252 ngày); HAC t-stat 0.10 với lag 9.
- Sparse portfolio net return: 0.00%; Sharpe N/A; max drawdown 0.00%.
- 0 vòng hoàn tất; no-trade 100.00%; nắm giữ trung bình N/A phiên.
- Turnover năm: 0.00x; chi phí chỉ tính cho vị thế thật sự được mở.
- Guard fail: entry_rule_selected, rank_ic_hac_significance, positive_net_return, positive_sharpe, enough_completed_round_trips, positive_cost_stress_return, positive_cost_stress_sharpe, positive_development_net_return.

| Rank | Mã | Dự báo excess return | Percentile |
|---:|---|---:|---:|
| 1 | GAS | 1.61% | 100.00% |
| 2 | TCB | 1.11% | 91.67% |
| 3 | HCM | 0.93% | 83.33% |
| 4 | MWG | 0.63% | 75.00% |
| 5 | VCB | 0.56% | 66.67% |
| 6 | SSI | 0.56% | 58.33% |
| 7 | MBB | 0.52% | 50.00% |
| 8 | FPT | 0.28% | 41.67% |
| 9 | VNM | 0.20% | 33.33% |
| 10 | VHM | 0.14% | 25.00% |

### Kết quả theo market regime

- bear: net return 0.00%; Sharpe N/A; Rank IC 0.036.
- bull: net return 0.00%; Sharpe N/A; Rank IC 0.170.
- sideways: net return 0.00%; Sharpe N/A; Rank IC -0.023.

## Horizon 20 phiên - NO_EDGE

- OOS Rank IC mean: 0.048 (252 ngày); HAC t-stat 0.79 với lag 19.
- Sparse portfolio net return: 0.00%; Sharpe N/A; max drawdown 0.00%.
- 0 vòng hoàn tất; no-trade 100.00%; nắm giữ trung bình N/A phiên.
- Turnover năm: 0.00x; chi phí chỉ tính cho vị thế thật sự được mở.
- Guard fail: entry_rule_selected, rank_ic_hac_significance, positive_net_return, positive_sharpe, enough_completed_round_trips, positive_cost_stress_return, positive_cost_stress_sharpe, positive_development_net_return.

| Rank | Mã | Dự báo excess return | Percentile |
|---:|---|---:|---:|
| 1 | HCM | 2.18% | 100.00% |
| 2 | GAS | 1.65% | 91.67% |
| 3 | TCB | 1.27% | 83.33% |
| 4 | MWG | 1.01% | 75.00% |
| 5 | SSI | 0.87% | 66.67% |
| 6 | VCB | 0.79% | 58.33% |
| 7 | VNM | 0.75% | 50.00% |
| 8 | VHM | 0.67% | 41.67% |
| 9 | FPT | 0.54% | 33.33% |
| 10 | MBB | 0.52% | 25.00% |

### Kết quả theo market regime

- bear: net return 0.00%; Sharpe N/A; Rank IC -0.100.
- bull: net return 0.00%; Sharpe N/A; Rank IC 0.106.
- sideways: net return 0.00%; Sharpe N/A; Rank IC 0.092.

Lưu ý: ranking chỉ được xem là bảng xếp hạng nghiên cứu khi guard đạt; không phải khuyến nghị mua/bán.
