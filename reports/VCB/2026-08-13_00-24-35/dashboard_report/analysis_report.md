# Báo cáo ngày 2026-08-13 - VCB

## Tổng quan

- Dữ liệu: 2009-06-30 -> 2026-08-12, 4,273 phiên.
- Giá đóng cửa: 59.70 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng (điểm 2).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 47.7%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Model health: BAD - Chưa tìm được ngưỡng nào có net dương và Sharpe dương sau phí trong OOS.
- Nếu chưa có cổ phiếu: NO_EDGE - Không có threshold nào trong kiểm thử OOS vừa net dương vừa Sharpe dương; không nên cố mở vị thế.
- Nếu đang nắm giữ: REDUCE_OR_EXIT - Model health xấu và chưa có edge sau phí; nếu đang giữ thì ưu tiên giảm tỷ trọng hoặc thoát theo kỷ luật.

## Phân tích kỹ thuật

- SMA20 57.43; SMA60 60.00; RSI14 55.7.
- MACD 0.246; đường tín hiệu -0.261; biểu đồ cột 0.507.
- ATR14 1.38; ATR% 2.3%; ADX14 26.4.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 55.7.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng tăng - ADX 26.4, +DI vượt -DI.
- Thanh khoản: Thấp - 0.46 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: Vietcombank.
- Ngành: Banks.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 12.00.
- P/B: 2.01.
- ROE: 17.9%.
- ROA: 1.7%.
- Market cap: 499,669.4 tỷ.
- Revenue Growth: 47.6%.
- Profit Growth: 64.7%.
- P/E 12.00: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 2.01: nên đọc cùng ROE và đặc thù ngành.
- ROE 17.9%: hiệu quả vốn chủ sở hữu tốt.
- Debt/Equity 9.69: đòn bẩy cao, cần đọc theo ngành.
- NPL 0.6%: đang ở mức kiểm soát.
- Revenue Growth 47.6% YoY.
- Profit Growth 64.7% YoY.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.12 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-06T09:03:02+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-11-22 -> 2026-08-11.
- XGBoost: độ chính xác cân bằng 0.503; AUC 0.468; log-loss 0.699.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.478; AUC 0.489.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 30.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -26.4%; Sharpe -2.25; mức sụt giảm tối đa -26.4%.

### Khuyến nghị hành động sau phí

| Mục | Kết quả | Diễn giải |
|---|---:|---|
| Model health | BAD | Chưa tìm được ngưỡng nào có net dương và Sharpe dương sau phí trong OOS. |
| Nếu chưa có cổ phiếu | NO_EDGE | Chưa có ngưỡng sau phí đủ tốt |
| Lý do cho mua mới |  | Không có threshold nào trong kiểm thử OOS vừa net dương vừa Sharpe dương; không nên cố mở vị thế. |
| Nếu đang nắm giữ | REDUCE_OR_EXIT | Model health xấu và chưa có edge sau phí; nếu đang giữ thì ưu tiên giảm tỷ trọng hoặc thoát theo kỷ luật. |
| Xác suất hiện tại | 47.7% | So với ngưỡng sau phí được chọn từ OOS. |
| Ngưỡng sau phí chọn | N/A | Chưa có threshold nào đạt net dương + Sharpe dương. |
| Baseline cấu hình | 41 vòng | Net sau phí -26.4%. |
| Reward/Risk | 1.67 | Chỉ dùng nếu decision cuối cùng cho phép mở vị thế. |
| Kỹ thuật / tin | 2 điểm | Hồi phục / nghiêng tăng; news warning: không; sentiment 0.00. |

### Breakdown trước phí / sau phí

| Kịch bản | Kết quả | Diễn giải |
|---|---:|---|
| Kịch bản trước chi phí | -10.3% | Gross PnL -10,291,240 VND; chưa trừ commission/slippage/tax. |
| Chi phí giao dịch | -19.7% | 41 vòng; entry 20.0 bps + exit 30.0 bps = 50.0 bps/vòng; tổng phí 16,712,005 VND. |
| Kịch bản sau chi phí | -26.4% | Net PnL -26,417,005 VND; gross - cost gap khoảng +16.1%. |
| Ngưỡng phí hòa vốn | -26.1 bps/vòng | Phí hiện tại 50.0 bps/vòng; cao hơn ngưỡng này thì gross dương vẫn có thể thành net âm. |
| Kết luận hành động | CHƯA CÓ LỢI THẾ (NO_EDGE) | Không đủ lợi thế sau phí; giữ NO_EDGE. |
| Cách cải thiện cần test | Giảm turnover | Hiện có 41 phiên active/41 vòng; nên test threshold 0.58/0.60/0.62 hoặc giữ nhiều phiên hơn. |

### Bảng chính: turnover, gross, phí và net

| Kịch bản | Cách chọn | Vòng | Gross trước phí | Phí | Net sau phí | Sharpe | Ghi chú |
|---|---|---:|---:|---:|---:|---:|---|
| Gốc | Ngưỡng gốc ≥ 0.55 | 41 | -10.3% | 19.7% | -26.4% | -2.25 | Baseline 61 vòng nếu model phát tín hiệu nhiều. |
| Ngưỡng 0.58 | Chỉ vào lệnh khi xác suất ≥ 0.58 | 20 | +0.9% | 9.7% | -8.5% | -1.04 | Tăng ngưỡng để giảm vòng lệnh. |
| Ngưỡng 0.60 | Chỉ vào lệnh khi xác suất ≥ 0.60 | 12 | +0.2% | 5.8% | -5.5% | -0.87 | Tăng ngưỡng để giảm vòng lệnh. |
| Ngưỡng 0.62 | Chỉ vào lệnh khi xác suất ≥ 0.62 | 4 | -1.0% | 2.0% | -2.9% | -0.50 | Tăng ngưỡng để giảm vòng lệnh. |
| Giới hạn 10 vòng | Tối đa 10 vòng, ưu tiên xác suất cao hơn | 10 | -0.6% | 4.9% | -5.4% | -0.86 | Ngưỡng xác suất trong nhóm: 60.5%. |
| Giới hạn 5 vòng | Tối đa 5 vòng, ưu tiên xác suất cao hơn | 5 | -1.5% | 2.4% | -3.9% | -0.65 | Ngưỡng xác suất trong nhóm: 62.0%. |
| Giới hạn 1 vòng | Tối đa 1 vòng, ưu tiên xác suất cao hơn | 1 | +1.0% | 0.5% | +0.5% | 0.61 | Ngưỡng xác suất trong nhóm: 83.0%. |
Ghi chú: đọc bảng từ trái sang phải để thấy phí giảm khi turnover giảm; các dòng 10/5/1 giới hạn số vòng bằng xác suất model cao hơn, không phải chọn lệnh thắng sau khi biết kết quả và không tự biến NO_EDGE thành BUY.
- Mức độ quan trọng của đặc trưng: rsi_14=12.14; return_1d=11.69; month_of_year=10.87; atr_pct_14=10.75; day_of_week=10.74; market_return_20d=10.35.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 59.40; mục tiêu 1 61.00; mục tiêu 2 66.79.
- Tỷ lệ lợi nhuận/rủi ro 1.67; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 58.81 (-1.49%).
- P10/P90 cuối kỳ 53.70 / 66.79.
- Lịch giao dịch: VN stock calendar: loại Thứ Bảy/Chủ Nhật và các ngày nghỉ 2026 đã công bố; ngày làm bù Thứ Bảy không được tính là phiên giao dịch chứng khoán.
- Ngày nghỉ đã loại khỏi forecast: 2026-01-01, 2026-01-02, 2026-02-16, 2026-02-17, 2026-02-18, 2026-02-19, 2026-02-20, 2026-04-27, 2026-04-30, 2026-05-01, 2026-08-31, 2026-09-01, 2026-09-02.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.468 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.503 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.4684203062960862, AUC logistic=0.4890527509926262.
- Điều kiện phát hành tín hiệu: Probability 47.7% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.26417005000000016, Sharpe=-2.247606612317961.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 47.7%.
- Mô hình Logistic đối chứng: 42.7%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 41.6%.
- Mức dừng lỗ tham chiếu 59.40, mục tiêu 1 61.00, tỷ lệ lợi nhuận/rủi ro 1.67.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
