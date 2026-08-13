# Báo cáo ngày 2026-08-13 - MSN

## Tổng quan

- Dữ liệu: 2009-11-05 -> 2026-08-12, 4,181 phiên.
- Giá đóng cửa: 67.20 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận (điểm -3).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 48.5%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Khuyến nghị sau phí: NO_EDGE - Chưa có ngưỡng sau phí đủ tốt.
- Lý do khuyến nghị: Không có threshold nào trong kiểm thử OOS vừa net dương vừa Sharpe dương; không nên cố mở vị thế.

## Phân tích kỹ thuật

- SMA20 66.35; SMA60 70.30; RSI14 47.7.
- MACD -0.510; đường tín hiệu -0.870; biểu đồ cột 0.360.
- ATR14 1.60; ATR% 2.4%; ADX14 29.1.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Trung tính - RSI 47.7.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng giảm - ADX 29.1, -DI vượt +DI.
- Thanh khoản: Thấp - 0.50 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: Tập đoàn Masan.
- Ngành: Food & Beverage.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 14.47.
- P/B: 2.44.
- ROE: 19.4%.
- ROA: 5.4%.
- Market cap: 97,991.1 tỷ.
- Revenue Growth: 53.5%.
- Profit Growth: 202.8%.
- P/E 14.47: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 2.44: nên đọc cùng ROE và đặc thù ngành.
- ROE 19.4%: hiệu quả vốn chủ sở hữu tốt.
- ROA 5.4%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 0.87: thanh khoản ngắn hạn cần theo dõi.
- Revenue Growth 53.5% YoY.
- Profit Growth 202.8% YoY.
- CFO/LNST -0.08: dòng tiền chưa theo kịp lợi nhuận, cần đọc thêm biến động vốn lưu động.
- Dòng tiền tự do quý gần nhất âm; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là nợ vay ròng; không dùng một mình để kết luận rủi ro.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.18 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-07T08:59:53+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-12-25 -> 2026-08-11.
- XGBoost: độ chính xác cân bằng 0.498; AUC 0.496; log-loss 0.692.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.500; AUC 0.512.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 13.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -15.4%; Sharpe -1.32; mức sụt giảm tối đa -18.3%.

### Khuyến nghị đầu tư sau phí

| Mục | Kết quả | Diễn giải |
|---|---:|---|
| Khuyến nghị sau phí | NO_EDGE | Chưa có ngưỡng sau phí đủ tốt |
| Lý do chính |  | Không có threshold nào trong kiểm thử OOS vừa net dương vừa Sharpe dương; không nên cố mở vị thế. |
| Xác suất hiện tại | 48.5% | So với ngưỡng sau phí được chọn từ OOS. |
| Ngưỡng sau phí chọn | N/A | Chưa có threshold nào đạt net dương + Sharpe dương. |
| Baseline cấu hình | 17 vòng | Net sau phí -15.4%. |
| Reward/Risk | 2.15 | Chỉ dùng nếu decision cuối cùng cho phép mở vị thế. |

### Breakdown trước phí / sau phí

| Kịch bản | Kết quả | Diễn giải |
|---|---:|---|
| Kịch bản trước chi phí | -8.3% | Gross PnL -8,279,702 VND; chưa trừ commission/slippage/tax. |
| Chi phí giao dịch | -8.1% | 17 vòng; entry 20.0 bps + exit 30.0 bps = 50.0 bps/vòng; tổng phí 7,407,910 VND. |
| Kịch bản sau chi phí | -15.4% | Net PnL -15,437,910 VND; gross - cost gap khoảng +7.2%. |
| Ngưỡng phí hòa vốn | -51.3 bps/vòng | Phí hiện tại 50.0 bps/vòng; cao hơn ngưỡng này thì gross dương vẫn có thể thành net âm. |
| Kết luận hành động | CHƯA CÓ LỢI THẾ (NO_EDGE) | Không đủ lợi thế sau phí; giữ NO_EDGE. |
| Cách cải thiện cần test | Giảm turnover | Hiện có 17 phiên active/17 vòng; nên test threshold 0.58/0.60/0.62 hoặc giữ nhiều phiên hơn. |

### Bảng chính: turnover, gross, phí và net

| Kịch bản | Cách chọn | Vòng | Gross trước phí | Phí | Net sau phí | Sharpe | Ghi chú |
|---|---|---:|---:|---:|---:|---:|---|
| Gốc | Ngưỡng gốc ≥ 0.55 | 17 | -8.3% | 8.1% | -15.4% | -1.32 | Baseline 61 vòng nếu model phát tín hiệu nhiều. |
| Ngưỡng 0.58 | Chỉ vào lệnh khi xác suất ≥ 0.58 | 5 | -4.0% | 2.4% | -6.3% | -0.81 | Tăng ngưỡng để giảm vòng lệnh. |
| Ngưỡng 0.60 | Chỉ vào lệnh khi xác suất ≥ 0.60 | 4 | -4.3% | 1.9% | -6.1% | -0.79 | Tăng ngưỡng để giảm vòng lệnh. |
| Ngưỡng 0.62 | Chỉ vào lệnh khi xác suất ≥ 0.62 | 1 | -0.1% | 0.5% | -0.6% | -0.62 | Tăng ngưỡng để giảm vòng lệnh. |
| Giới hạn 10 vòng | Tối đa 10 vòng, ưu tiên xác suất cao hơn | 10 | -3.3% | 4.8% | -7.8% | -0.71 | Ngưỡng xác suất trong nhóm: 57.2%. |
| Giới hạn 5 vòng | Tối đa 5 vòng, ưu tiên xác suất cao hơn | 5 | -4.0% | 2.4% | -6.3% | -0.81 | Ngưỡng xác suất trong nhóm: 59.5%. |
| Giới hạn 1 vòng | Tối đa 1 vòng, ưu tiên xác suất cao hơn | 1 | -0.1% | 0.5% | -0.6% | -0.62 | Ngưỡng xác suất trong nhóm: 62.0%. |
Ghi chú: đọc bảng từ trái sang phải để thấy phí giảm khi turnover giảm; các dòng 10/5/1 giới hạn số vòng bằng xác suất model cao hơn, không phải chọn lệnh thắng sau khi biết kết quả và không tự biến NO_EDGE thành BUY.
- Mức độ quan trọng của đặc trưng: close_vs_sma20=18.12; return_kurtosis_20d=15.33; atr_pct_14=15.26; relative_strength_20d=15.03; range_pct=12.51; volume_z_20=11.90.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 64.80; mục tiêu 1 73.43; mục tiêu 2 73.43.
- Tỷ lệ lợi nhuận/rủi ro 2.15; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 66.70 (-0.74%).
- P10/P90 cuối kỳ 60.51 / 73.43.
- Lịch giao dịch: VN stock calendar: loại Thứ Bảy/Chủ Nhật và các ngày nghỉ 2026 đã công bố; ngày làm bù Thứ Bảy không được tính là phiên giao dịch chứng khoán.
- Ngày nghỉ đã loại khỏi forecast: 2026-01-01, 2026-01-02, 2026-02-16, 2026-02-17, 2026-02-18, 2026-02-19, 2026-02-20, 2026-04-27, 2026-04-30, 2026-05-01, 2026-08-31, 2026-09-01, 2026-09-02.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.496 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.498 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.4956490210297317, AUC logistic=0.512445367775317.
- Điều kiện phát hành tín hiệu: Probability 48.5% < 55.0%.
- Điều kiện phát hành tín hiệu: Technical score -3 < 2.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.15437910000000032, Sharpe=-1.3228257273228545.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 48.5%.
- Mô hình Logistic đối chứng: 44.8%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 46.0%.
- Mức dừng lỗ tham chiếu 64.80, mục tiêu 1 73.43, tỷ lệ lợi nhuận/rủi ro 2.15.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
