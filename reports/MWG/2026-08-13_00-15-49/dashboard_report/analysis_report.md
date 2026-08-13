# Báo cáo ngày 2026-08-13 - MWG

## Tổng quan

- Dữ liệu: 2014-07-14 -> 2026-08-12, 3,017 phiên.
- Giá đóng cửa: 74.00 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận (điểm -2).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 47.4%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Khuyến nghị sau phí: WAIT - Chờ điểm mua tốt hơn.
- Lý do khuyến nghị: Ngưỡng sau phí đang tốt hơn là 0.62, nhưng xác suất hiện tại chỉ 47.4%.

## Phân tích kỹ thuật

- SMA20 70.93; SMA60 74.89; RSI14 54.7.
- MACD -0.510; đường tín hiệu -1.255; biểu đồ cột 0.745.
- ATR14 2.37; ATR% 3.2%; ADX14 26.0.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Trung tính - RSI 54.7.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng giảm - ADX 26.0, -DI vượt +DI.
- Thanh khoản: Thấp - 0.57 lần trung bình.
- Stochastic: Cực trị - %K 98.4, %D 92.7.

## Phân tích cơ bản

- Doanh nghiệp: Thế giới di động.
- Ngành: Retail.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 10.98.
- P/B: 3.02.
- ROE: 29.2%.
- ROA: 11.2%.
- Market cap: 108,026.0 tỷ.
- Revenue Growth: 29.6%.
- Profit Growth: 100.4%.
- P/E 10.98: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 3.02: nên đọc cùng ROE và đặc thù ngành.
- ROE 29.2%: hiệu quả vốn chủ sở hữu tốt.
- ROA 11.2%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 1.44: thanh khoản ngắn hạn khá.
- Revenue Growth 29.6% YoY.
- Profit Growth 100.4% YoY.
- CFO/LNST 5.06: chất lượng chuyển đổi lợi nhuận sang tiền mặt khá tốt.
- Dòng tiền tự do quý gần nhất dương; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là nợ vay ròng; không dùng một mình để kết luận rủi ro.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.10 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-10T09:51:48+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2024-01-23 -> 2026-08-11.
- XGBoost: độ chính xác cân bằng 0.511; AUC 0.506; log-loss 0.694.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.529; AUC 0.525.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 87.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -6.6%; Sharpe -0.21; mức sụt giảm tối đa -14.2%.

### Khuyến nghị đầu tư sau phí

| Mục | Kết quả | Diễn giải |
|---|---:|---|
| Khuyến nghị sau phí | WAIT | Chờ điểm mua tốt hơn |
| Lý do chính |  | Ngưỡng sau phí đang tốt hơn là 0.62, nhưng xác suất hiện tại chỉ 47.4%. |
| Xác suất hiện tại | 47.4% | So với ngưỡng sau phí được chọn từ OOS. |
| Ngưỡng sau phí chọn | 0.62 | Ngưỡng 0.62; net +14.4%; 9 vòng. |
| Baseline cấu hình | 84 vòng | Net sau phí -6.6%. |
| Reward/Risk | 2.15 | Chỉ dùng nếu decision cuối cùng cho phép mở vị thế. |

### Breakdown trước phí / sau phí

| Kịch bản | Kết quả | Diễn giải |
|---|---:|---|
| Kịch bản trước chi phí | +39.8% | Gross PnL 39,831,560 VND; chưa trừ commission/slippage/tax. |
| Chi phí giao dịch | -40.4% | 84 vòng; entry 20.0 bps + exit 30.0 bps = 50.0 bps/vòng; tổng phí 38,498,506 VND. |
| Kịch bản sau chi phí | -6.6% | Net PnL -6,561,506 VND; gross - cost gap khoảng +46.4%. |
| Ngưỡng phí hòa vốn | 49.3 bps/vòng | Phí hiện tại 50.0 bps/vòng; cao hơn ngưỡng này thì gross dương vẫn có thể thành net âm. |
| Kết luận hành động | CHƯA CÓ LỢI THẾ (NO_EDGE) | Không mở vị thế mới; nếu đang giữ thì ưu tiên giảm/bán theo kỷ luật vì sau phí vẫn âm. |
| Cách cải thiện cần test | Giảm turnover | Hiện có 84 phiên active/84 vòng; nên test threshold 0.58/0.60/0.62 hoặc giữ nhiều phiên hơn. |

### Bảng chính: turnover, gross, phí và net

| Kịch bản | Cách chọn | Vòng | Gross trước phí | Phí | Net sau phí | Sharpe | Ghi chú |
|---|---|---:|---:|---:|---:|---:|---|
| Gốc | Ngưỡng gốc ≥ 0.55 | 84 | +39.8% | 40.4% | -6.6% | -0.21 | Baseline 61 vòng nếu model phát tín hiệu nhiều. |
| Ngưỡng 0.58 | Chỉ vào lệnh khi xác suất ≥ 0.58 | 36 | +19.7% | 17.3% | +0.7% | 0.08 | Tăng ngưỡng để giảm vòng lệnh. |
| Ngưỡng 0.60 | Chỉ vào lệnh khi xác suất ≥ 0.60 | 20 | +23.1% | 9.7% | +11.8% | 0.83 | Tăng ngưỡng để giảm vòng lệnh. |
| Ngưỡng 0.62 | Chỉ vào lệnh khi xác suất ≥ 0.62 | 9 | +19.5% | 4.4% | +14.4% | 1.15 | Tăng ngưỡng để giảm vòng lệnh. |
| Giới hạn 10 vòng | Tối đa 10 vòng, ưu tiên xác suất cao hơn | 10 | +17.9% | 4.9% | +12.4% | 0.97 | Ngưỡng xác suất trong nhóm: 61.8%. |
| Giới hạn 5 vòng | Tối đa 5 vòng, ưu tiên xác suất cao hơn | 5 | +9.3% | 2.5% | +6.7% | 0.74 | Ngưỡng xác suất trong nhóm: 63.9%. |
| Giới hạn 1 vòng | Tối đa 1 vòng, ưu tiên xác suất cao hơn | 1 | +5.4% | 0.5% | +4.9% | 0.63 | Ngưỡng xác suất trong nhóm: 73.2%. |
Ghi chú: đọc bảng từ trái sang phải để thấy phí giảm khi turnover giảm; các dòng 10/5/1 giới hạn số vòng bằng xác suất model cao hơn, không phải chọn lệnh thắng sau khi biết kết quả và không tự biến NO_EDGE thành BUY.
- Mức độ quan trọng của đặc trưng: beta_60d=8.40; day_of_week=7.80; excess_return_5d=7.60; month_of_year=7.38; return_2d=7.37; stoch_k_14=7.25.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 70.45; mục tiêu 1 82.80; mục tiêu 2 82.80.
- Tỷ lệ lợi nhuận/rủi ro 2.15; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 73.52 (-0.64%).
- P10/P90 cuối kỳ 65.38 / 82.80.
- Lịch giao dịch: VN stock calendar: loại Thứ Bảy/Chủ Nhật và các ngày nghỉ 2026 đã công bố; ngày làm bù Thứ Bảy không được tính là phiên giao dịch chứng khoán.
- Ngày nghỉ đã loại khỏi forecast: 2026-01-01, 2026-01-02, 2026-02-16, 2026-02-17, 2026-02-18, 2026-02-19, 2026-02-20, 2026-04-27, 2026-04-30, 2026-05-01, 2026-08-31, 2026-09-01, 2026-09-02.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.506 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.511 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5056010383386581, AUC logistic=0.5245007987220447.
- Điều kiện phát hành tín hiệu: Probability 47.4% < 55.0%.
- Điều kiện phát hành tín hiệu: Technical score -2 < 2.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.06561506000000039, Sharpe=-0.21066571922901275.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 47.4%.
- Mô hình Logistic đối chứng: 42.4%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 47.1%.
- Mức dừng lỗ tham chiếu 70.45, mục tiêu 1 82.80, tỷ lệ lợi nhuận/rủi ro 2.15.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
