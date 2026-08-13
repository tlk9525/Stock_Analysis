# Báo cáo ngày 2026-08-13 - GMD

## Tổng quan

- Dữ liệu: 2008-03-07 -> 2026-08-12, 4,595 phiên.
- Giá đóng cửa: 77.20 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng (điểm 4).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 48.1%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 75.75; SMA60 75.58; RSI14 55.1.
- MACD 0.530; đường tín hiệu 0.245; biểu đồ cột 0.285.
- ATR14 2.18; ATR% 2.8%; ADX14 17.0.
- Xu hướng: Tích cực - Giá nằm trên SMA20 và SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 55.1.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Đi ngang - ADX 17.0.
- Thanh khoản: Thấp - 0.62 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: Tập đoàn Gemadept.
- Ngành: Industrial Goods & Services.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 12.78.
- P/B: 2.43.
- ROE: 19.4%.
- ROA: 12.8%.
- Market cap: 33,505.9 tỷ.
- Revenue Growth: 17.9%.
- Profit Growth: 154.6%.
- P/E 12.78: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 2.43: nên đọc cùng ROE và đặc thù ngành.
- ROE 19.4%: hiệu quả vốn chủ sở hữu tốt.
- ROA 12.8%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 2.42: thanh khoản ngắn hạn khá.
- Revenue Growth 17.9% YoY.
- Profit Growth 154.6% YoY.
- CFO/LNST 0.54: dòng tiền chưa theo kịp lợi nhuận, cần đọc thêm biến động vốn lưu động.
- Dòng tiền tự do quý gần nhất dương; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là nợ vay ròng; không dùng một mình để kết luận rủi ro.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.14 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-07T08:30:10+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-08-23 -> 2026-08-11.
- XGBoost: độ chính xác cân bằng 0.508; AUC 0.528; log-loss 0.693.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.512; AUC 0.539.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 52.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -20.5%; Sharpe -0.74; mức sụt giảm tối đa -21.9%.

### Breakdown trước phí / sau phí

| Kịch bản | Kết quả | Diễn giải |
|---|---:|---|
| Kịch bản trước chi phí | +7.7% | Gross PnL 7,676,072 VND; chưa trừ commission/slippage/tax. |
| Chi phí giao dịch | -30.3% | 63 vòng; entry 20.0 bps + exit 30.0 bps = 50.0 bps/vòng; tổng phí 27,079,394 VND. |
| Kịch bản sau chi phí | -20.5% | Net PnL -20,506,394 VND; gross - cost gap khoảng +28.2%. |
| Ngưỡng phí hòa vốn | 12.7 bps/vòng | Phí hiện tại 50.0 bps/vòng; cao hơn ngưỡng này thì gross dương vẫn có thể thành net âm. |
| Kết luận hành động | CHƯA CÓ LỢI THẾ (NO_EDGE) | Không mở vị thế mới; nếu đang giữ thì ưu tiên giảm/bán theo kỷ luật vì sau phí vẫn âm. |
| Cách cải thiện cần test | Giảm turnover | Hiện có 63 phiên active/63 vòng; nên test threshold 0.58/0.60/0.62 hoặc giữ nhiều phiên hơn. |

### Bảng chính: turnover, gross, phí và net

| Kịch bản | Cách chọn | Vòng | Gross trước phí | Phí | Net sau phí | Sharpe | Ghi chú |
|---|---|---:|---:|---:|---:|---:|---|
| Gốc | Ngưỡng gốc ≥ 0.55 | 63 | +7.7% | 30.3% | -20.5% | -0.74 | Baseline 61 vòng nếu model phát tín hiệu nhiều. |
| Ngưỡng 0.58 | Chỉ vào lệnh khi xác suất ≥ 0.58 | 32 | +7.8% | 15.5% | -7.6% | -0.29 | Tăng ngưỡng để giảm vòng lệnh. |
| Ngưỡng 0.60 | Chỉ vào lệnh khi xác suất ≥ 0.60 | 16 | +10.3% | 7.8% | +2.0% | 0.13 | Tăng ngưỡng để giảm vòng lệnh. |
| Ngưỡng 0.62 | Chỉ vào lệnh khi xác suất ≥ 0.62 | 10 | +9.9% | 4.9% | +4.7% | 0.33 | Tăng ngưỡng để giảm vòng lệnh. |
| Giới hạn 10 vòng | Tối đa 10 vòng, ưu tiên xác suất cao hơn | 10 | +9.9% | 4.9% | +4.7% | 0.33 | Ngưỡng xác suất trong nhóm: 63.0%. |
| Giới hạn 5 vòng | Tối đa 5 vòng, ưu tiên xác suất cao hơn | 5 | +4.9% | 2.4% | +2.4% | 0.20 | Ngưỡng xác suất trong nhóm: 65.3%. |
| Giới hạn 1 vòng | Tối đa 1 vòng, ưu tiên xác suất cao hơn | 1 | +0.0% | 0.5% | -0.5% | -0.58 | Ngưỡng xác suất trong nhóm: 80.3%. |
Ghi chú: đọc bảng từ trái sang phải để thấy phí giảm khi turnover giảm; các dòng 10/5/1 giới hạn số vòng bằng xác suất model cao hơn, không phải chọn lệnh thắng sau khi biết kết quả và không tự biến NO_EDGE thành BUY.
- Mức độ quan trọng của đặc trưng: day_of_week=10.66; return_kurtosis_20d=9.95; return_3d=9.95; macd_pct=9.90; return_10d=9.88; return_2d=9.57.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 74.83; mục tiêu 1 82.00; mục tiêu 2 86.82.
- Tỷ lệ lợi nhuận/rủi ro 1.60; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 76.96 (-0.31%).
- P10/P90 cuối kỳ 67.89 / 86.82.
- Lịch giao dịch: VN stock calendar: loại Thứ Bảy/Chủ Nhật và các ngày nghỉ 2026 đã công bố; ngày làm bù Thứ Bảy không được tính là phiên giao dịch chứng khoán.
- Ngày nghỉ đã loại khỏi forecast: 2026-01-01, 2026-01-02, 2026-02-16, 2026-02-17, 2026-02-18, 2026-02-19, 2026-02-20, 2026-04-27, 2026-04-30, 2026-05-01, 2026-08-31, 2026-09-01, 2026-09-02.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.528 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.508 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5276393751683275, AUC logistic=0.5390295358649789.
- Điều kiện phát hành tín hiệu: Probability 48.1% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.2050639400000005, Sharpe=-0.7448701519430575.
- Xu hướng ngắn hạn thuận: giá trên SMA20 và SMA60.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 48.1%.
- Mô hình Logistic đối chứng: 50.5%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 48.7%.
- Mức dừng lỗ tham chiếu 74.83, mục tiêu 1 82.00, tỷ lệ lợi nhuận/rủi ro 1.60.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
