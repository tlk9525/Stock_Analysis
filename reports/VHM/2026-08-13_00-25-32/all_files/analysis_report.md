# Báo cáo ngày 2026-08-13 - VHM

## Tổng quan

- Dữ liệu: 2011-11-10 -> 2026-08-12, 2,162 phiên.
- Giá đóng cửa: 73.80 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng (điểm 4).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 51.7%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Model health: WEAK - Có ngưỡng sau phí dương trong sensitivity, nhưng model health chưa sạch: AUC của mô hình, XGBoost vượt mô hình Logistic đối chứng.
- Nếu chưa có cổ phiếu: WAIT - Ngưỡng sau phí đang tốt hơn là 0.58, nhưng xác suất hiện tại chỉ 51.7%.
- Nếu đang nắm giữ: HOLD_DISCIPLINED - Chưa đủ điều kiện mua mới, nhưng kỹ thuật chưa xấu; nếu đang giữ thì có thể giữ có stop-loss, không mua thêm.

## Phân tích kỹ thuật

- SMA20 70.84; SMA60 72.13; RSI14 54.1.
- MACD 0.687; đường tín hiệu 0.358; biểu đồ cột 0.329.
- ATR14 3.17; ATR% 4.3%; ADX14 23.3.
- Xu hướng: Trung tính - Giá trên SMA60 nhưng chưa vượt SMA20.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Trung tính - RSI 54.1.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Đi ngang - ADX 23.3.
- Thanh khoản: Bình thường - 1.05 lần trung bình.
- Stochastic: Hồi phục - %K nằm trên %D.

## Phân tích cơ bản

- Doanh nghiệp: Vinhomes.
- Ngành: Real Estate.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 7.42.
- P/B: 2.28.
- ROE: 32.7%.
- ROA: 9.0%.
- Market cap: 592,288.8 tỷ.
- Revenue Growth: 177.8%.
- Profit Growth: 200.8%.
- P/E 7.42: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 2.28: nên đọc cùng ROE và đặc thù ngành.
- ROE 32.7%: hiệu quả vốn chủ sở hữu tốt.
- ROA 9.0%: khá tốt, đặc biệt với nhóm ngân hàng.
- Debt/Equity 3.05: đòn bẩy cao, cần đọc theo ngành.
- Current ratio 1.17: thanh khoản ngắn hạn khá.
- Revenue Growth 177.8% YoY.
- Profit Growth 200.8% YoY.
- CFO/LNST 1.97: chất lượng chuyển đổi lợi nhuận sang tiền mặt khá tốt.
- Dòng tiền tự do quý gần nhất dương; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là nợ vay ròng; không dùng một mình để kết luận rủi ro.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.12 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-10T03:53:05+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-10-19 -> 2026-08-11.
- XGBoost: độ chính xác cân bằng 0.530; AUC 0.523; log-loss 0.696.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.530; AUC 0.546.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 25.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận 29.9%; Sharpe 0.73; mức sụt giảm tối đa -14.7%.

### Khuyến nghị hành động sau phí

| Mục | Kết quả | Diễn giải |
|---|---:|---|
| Model health | WEAK | Có ngưỡng sau phí dương trong sensitivity, nhưng model health chưa sạch: AUC của mô hình, XGBoost vượt mô hình Logistic đối chứng. |
| Nếu chưa có cổ phiếu | WAIT | Chờ điểm mua tốt hơn |
| Lý do cho mua mới |  | Ngưỡng sau phí đang tốt hơn là 0.58, nhưng xác suất hiện tại chỉ 51.7%. |
| Nếu đang nắm giữ | HOLD_DISCIPLINED | Chưa đủ điều kiện mua mới, nhưng kỹ thuật chưa xấu; nếu đang giữ thì có thể giữ có stop-loss, không mua thêm. |
| Xác suất hiện tại | 51.7% | So với ngưỡng sau phí được chọn từ OOS. |
| Ngưỡng sau phí chọn | 0.58 | Ngưỡng 0.58; net +41.3%; 39 vòng. |
| Baseline cấu hình | 61 vòng | Net sau phí +29.9%. |
| Reward/Risk | 2.73 | Chỉ dùng nếu decision cuối cùng cho phép mở vị thế. |
| Kỹ thuật / tin | 4 điểm | Hồi phục / nghiêng tăng; news warning: không; sentiment 0.00. |

### Breakdown trước phí / sau phí

| Kịch bản | Kết quả | Diễn giải |
|---|---:|---|
| Kịch bản trước chi phí | +75.2% | Gross PnL 75,235,835 VND; chưa trừ commission/slippage/tax. |
| Chi phí giao dịch | -30.1% | 61 vòng; entry 20.0 bps + exit 30.0 bps = 50.0 bps/vòng; tổng phí 35,305,008 VND. |
| Kịch bản sau chi phí | +29.9% | Net PnL 29,925,992 VND; gross - cost gap khoảng +45.3%. |
| Ngưỡng phí hòa vốn | 124.9 bps/vòng | Phí hiện tại 50.0 bps/vòng; cao hơn ngưỡng này thì gross dương vẫn có thể thành net âm. |
| Kết luận hành động | CHƯA CÓ LỢI THẾ (NO_EDGE) | Sau phí vẫn dương; có thể xem tiếp các gate còn lại trước khi cân nhắc hành động. |
| Cách cải thiện cần test | Giảm turnover | Hiện có 61 phiên active/61 vòng; nên test threshold 0.58/0.60/0.62 hoặc giữ nhiều phiên hơn. |

### Bảng chính: turnover, gross, phí và net

| Kịch bản | Cách chọn | Vòng | Gross trước phí | Phí | Net sau phí | Sharpe | Ghi chú |
|---|---|---:|---:|---:|---:|---:|---|
| Gốc | Ngưỡng gốc ≥ 0.55 | 61 | +75.2% | 30.1% | +29.9% | 0.73 | Baseline 61 vòng nếu model phát tín hiệu nhiều. |
| Ngưỡng 0.58 | Chỉ vào lệnh khi xác suất ≥ 0.58 | 39 | +71.2% | 19.4% | +41.3% | 1.17 | Tăng ngưỡng để giảm vòng lệnh. |
| Ngưỡng 0.60 | Chỉ vào lệnh khi xác suất ≥ 0.60 | 25 | +40.8% | 12.4% | +24.5% | 0.93 | Tăng ngưỡng để giảm vòng lệnh. |
| Ngưỡng 0.62 | Chỉ vào lệnh khi xác suất ≥ 0.62 | 18 | +30.5% | 8.9% | +19.5% | 0.80 | Tăng ngưỡng để giảm vòng lệnh. |
| Giới hạn 10 vòng | Tối đa 10 vòng, ưu tiên xác suất cao hơn | 10 | +34.7% | 5.0% | +28.2% | 1.19 | Ngưỡng xác suất trong nhóm: 64.3%. |
| Giới hạn 5 vòng | Tối đa 5 vòng, ưu tiên xác suất cao hơn | 5 | +32.6% | 2.5% | +29.4% | 1.25 | Ngưỡng xác suất trong nhóm: 67.4%. |
| Giới hạn 1 vòng | Tối đa 1 vòng, ưu tiên xác suất cao hơn | 1 | +8.9% | 0.5% | +8.4% | 0.60 | Ngưỡng xác suất trong nhóm: 72.0%. |
Ghi chú: đọc bảng từ trái sang phải để thấy phí giảm khi turnover giảm; các dòng 10/5/1 giới hạn số vòng bằng xác suất model cao hơn, không phải chọn lệnh thắng sau khi biết kết quả và không tự biến NO_EDGE thành BUY.
- Mức độ quan trọng của đặc trưng: range_pct=11.73; market_volatility_20d=11.67; atr_pct_14=11.25; market_return_1d=10.36; day_of_week=9.99; return_1d=9.86.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 71.41; mục tiêu 1 81.70; mục tiêu 2 91.49.
- Tỷ lệ lợi nhuận/rủi ro 2.73; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 72.78 (-1.39%).
- P10/P90 cuối kỳ 58.76 / 91.49.
- Lịch giao dịch: VN stock calendar: loại Thứ Bảy/Chủ Nhật và các ngày nghỉ 2026 đã công bố; ngày làm bù Thứ Bảy không được tính là phiên giao dịch chứng khoán.
- Ngày nghỉ đã loại khỏi forecast: 2026-01-01, 2026-01-02, 2026-02-16, 2026-02-17, 2026-02-18, 2026-02-19, 2026-02-20, 2026-04-27, 2026-04-30, 2026-05-01, 2026-08-31, 2026-09-01, 2026-09-02.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.523 < 0.540.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5234451573580647, AUC logistic=0.5461613857064023.
- Điều kiện phát hành tín hiệu: Probability 51.7% < 55.0%.
- Trung hạn chưa xấu, ngắn hạn yếu vì giá dưới SMA20.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 51.7%.
- Mô hình Logistic đối chứng: 48.5%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 46.8%.
- Mức dừng lỗ tham chiếu 71.41, mục tiêu 1 81.70, tỷ lệ lợi nhuận/rủi ro 2.73.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
