# Báo cáo ngày 2026-08-13 - PNJ

## Tổng quan

- Dữ liệu: 2009-03-23 -> 2026-08-12, 4,329 phiên.
- Giá đóng cửa: 35.05 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận (điểm -4).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 48.2%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Model health: BAD - Chưa tìm được ngưỡng nào có net dương và Sharpe dương sau phí trong OOS.
- Nếu chưa có cổ phiếu: NO_EDGE - Không có threshold nào trong kiểm thử OOS vừa net dương vừa Sharpe dương; không nên cố mở vị thế.
- Nếu đang nắm giữ: REDUCE_OR_EXIT - Model health xấu và chưa có edge sau phí; nếu đang giữ thì ưu tiên giảm tỷ trọng hoặc thoát theo kỷ luật.

## Phân tích kỹ thuật

- SMA20 35.45; SMA60 52.85; RSI14 36.5.
- MACD -4.115; đường tín hiệu -5.290; biểu đồ cột 1.175.
- ATR14 2.31; ATR% 6.6%; ADX14 37.4.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Yếu - RSI 36.5.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng giảm - ADX 37.4, -DI vượt +DI.
- Thanh khoản: Thấp - 0.24 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: Vàng Phú Nhuận.
- Ngành: Personal & Household Goods.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 6.14.
- P/B: 1.28.
- ROE: 21.6%.
- ROA: 14.9%.
- Market cap: 17,833.5 tỷ.
- Revenue Growth: 11.9%.
- Profit Growth: -164.7%.
- P/E 6.14: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 1.28: nên đọc cùng ROE và đặc thù ngành.
- ROE 21.6%: hiệu quả vốn chủ sở hữu tốt.
- ROA 14.9%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 2.74: thanh khoản ngắn hạn khá.
- Revenue Growth 11.9% YoY.
- Profit Growth -164.7% YoY.
- CFO/LNST 5.54: chất lượng chuyển đổi lợi nhuận sang tiền mặt khá tốt.
- Dòng tiền tự do quý gần nhất âm; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là nợ vay ròng; không dùng một mình để kết luận rủi ro.
- Khả năng trả lãi -6.08 lần: cần theo dõi áp lực lãi vay.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.02 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-10T08:24:18+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-12-14 -> 2026-08-11.
- XGBoost: độ chính xác cân bằng 0.492; AUC 0.487; log-loss 0.698.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.487; AUC 0.503.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 13.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -5.5%; Sharpe -0.19; mức sụt giảm tối đa -19.7%.

### Khuyến nghị hành động sau phí

| Mục | Kết quả | Diễn giải |
|---|---:|---|
| Model health | BAD | Chưa tìm được ngưỡng nào có net dương và Sharpe dương sau phí trong OOS. |
| Nếu chưa có cổ phiếu | NO_EDGE | Chưa có ngưỡng sau phí đủ tốt |
| Lý do cho mua mới |  | Không có threshold nào trong kiểm thử OOS vừa net dương vừa Sharpe dương; không nên cố mở vị thế. |
| Nếu đang nắm giữ | REDUCE_OR_EXIT | Model health xấu và chưa có edge sau phí; nếu đang giữ thì ưu tiên giảm tỷ trọng hoặc thoát theo kỷ luật. |
| Xác suất hiện tại | 48.2% | So với ngưỡng sau phí được chọn từ OOS. |
| Ngưỡng sau phí chọn | N/A | Chưa có threshold nào đạt net dương + Sharpe dương. |
| Baseline cấu hình | 37 vòng | Net sau phí -5.5%. |
| Reward/Risk | 1.53 | Chỉ dùng nếu decision cuối cùng cho phép mở vị thế. |
| Kỹ thuật / tin | -4 điểm | Suy yếu / cẩn thận; news warning: không; sentiment 0.00. |

### Breakdown trước phí / sau phí

| Kịch bản | Kết quả | Diễn giải |
|---|---:|---|
| Kịch bản trước chi phí | +13.0% | Gross PnL 12,952,378 VND; chưa trừ commission/slippage/tax. |
| Chi phí giao dịch | -17.8% | 37 vòng; entry 20.0 bps + exit 30.0 bps = 50.0 bps/vòng; tổng phí 15,660,290 VND. |
| Kịch bản sau chi phí | -5.5% | Net PnL -5,460,290 VND; gross - cost gap khoảng +18.4%. |
| Ngưỡng phí hòa vốn | 36.4 bps/vòng | Phí hiện tại 50.0 bps/vòng; cao hơn ngưỡng này thì gross dương vẫn có thể thành net âm. |
| Kết luận hành động | CHƯA CÓ LỢI THẾ (NO_EDGE) | Không mở vị thế mới; nếu đang giữ thì ưu tiên giảm/bán theo kỷ luật vì sau phí vẫn âm. |
| Cách cải thiện cần test | Giảm turnover | Hiện có 37 phiên active/37 vòng; nên test threshold 0.58/0.60/0.62 hoặc giữ nhiều phiên hơn. |

### Bảng chính: turnover, gross, phí và net

| Kịch bản | Cách chọn | Vòng | Gross trước phí | Phí | Net sau phí | Sharpe | Ghi chú |
|---|---|---:|---:|---:|---:|---:|---|
| Gốc | Ngưỡng gốc ≥ 0.55 | 37 | +13.0% | 17.8% | -5.5% | -0.19 | Baseline 61 vòng nếu model phát tín hiệu nhiều. |
| Ngưỡng 0.58 | Chỉ vào lệnh khi xác suất ≥ 0.58 | 14 | +6.8% | 6.7% | -0.1% | 0.01 | Tăng ngưỡng để giảm vòng lệnh. |
| Ngưỡng 0.60 | Chỉ vào lệnh khi xác suất ≥ 0.60 | 5 | -0.3% | 2.4% | -2.7% | -0.95 | Tăng ngưỡng để giảm vòng lệnh. |
| Ngưỡng 0.62 | Chỉ vào lệnh khi xác suất ≥ 0.62 | 5 | -0.3% | 2.4% | -2.7% | -0.95 | Tăng ngưỡng để giảm vòng lệnh. |
| Giới hạn 10 vòng | Tối đa 10 vòng, ưu tiên xác suất cao hơn | 10 | +0.5% | 4.9% | -4.3% | -1.04 | Ngưỡng xác suất trong nhóm: 59.0%. |
| Giới hạn 5 vòng | Tối đa 5 vòng, ưu tiên xác suất cao hơn | 5 | -0.3% | 2.4% | -2.7% | -0.95 | Ngưỡng xác suất trong nhóm: 62.0%. |
| Giới hạn 1 vòng | Tối đa 1 vòng, ưu tiên xác suất cao hơn | 1 | +0.7% | 0.5% | +0.2% | 0.62 | Ngưỡng xác suất trong nhóm: 74.1%. |
Ghi chú: đọc bảng từ trái sang phải để thấy phí giảm khi turnover giảm; các dòng 10/5/1 giới hạn số vòng bằng xác suất model cao hơn, không phải chọn lệnh thắng sau khi biết kết quả và không tự biến NO_EDGE thành BUY.
- Mức độ quan trọng của đặc trưng: return_20d=11.88; market_return_1d=11.22; rsi_14=11.02; close_vs_sma60=10.77; excess_return_1d=10.59; adx_14=10.47.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 31.59; mục tiêu 1 40.81; mục tiêu 2 43.35.
- Tỷ lệ lợi nhuận/rủi ro 1.53; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 35.44 (1.10%).
- P10/P90 cuối kỳ 28.81 / 40.81.
- Lịch giao dịch: VN stock calendar: loại Thứ Bảy/Chủ Nhật và các ngày nghỉ 2026 đã công bố; ngày làm bù Thứ Bảy không được tính là phiên giao dịch chứng khoán.
- Ngày nghỉ đã loại khỏi forecast: 2026-01-01, 2026-01-02, 2026-02-16, 2026-02-17, 2026-02-18, 2026-02-19, 2026-02-20, 2026-04-27, 2026-04-30, 2026-05-01, 2026-08-31, 2026-09-01, 2026-09-02.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.487 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.492 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.4871697237055955, AUC logistic=0.5025029022521477.
- Điều kiện phát hành tín hiệu: Probability 48.2% < 55.0%.
- Điều kiện phát hành tín hiệu: Technical score -4 < 2.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.05460289999999968, Sharpe=-0.1917641851198188.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 48.2%.
- Mô hình Logistic đối chứng: 58.7%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 53.4%.
- Mức dừng lỗ tham chiếu 31.59, mục tiêu 1 40.81, tỷ lệ lợi nhuận/rủi ro 1.53.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
