# Báo cáo ngày 2026-08-13 - FPT

## Tổng quan

- Dữ liệu: 2008-03-07 -> 2026-08-12, 4,594 phiên.
- Giá đóng cửa: 70.80 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng (điểm 2).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 48.6%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 67.61; SMA60 70.82; RSI14 56.1.
- MACD 0.462; đường tín hiệu -0.258; biểu đồ cột 0.720.
- ATR14 1.89; ATR% 2.7%; ADX14 25.2.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 56.1.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng tăng - ADX 25.2, +DI vượt -DI.
- Thanh khoản: Thấp - 0.53 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: FPT Corp.
- Ngành: Technology.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 12.14.
- P/B: 3.05.
- ROE: 26.5%.
- ROA: 12.8%.
- Market cap: 122,060.0 tỷ.
- Revenue Growth: -17.1%.
- Profit Growth: 13.7%.
- P/E 12.14: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 3.05: nên đọc cùng ROE và đặc thù ngành.
- ROE 26.5%: hiệu quả vốn chủ sở hữu tốt.
- ROA 12.8%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 1.56: thanh khoản ngắn hạn khá.
- Revenue Growth -17.1% YoY.
- Profit Growth 13.7% YoY.
- CFO/LNST 0.66: dòng tiền chưa theo kịp lợi nhuận, cần đọc thêm biến động vốn lưu động.
- Dòng tiền tự do quý gần nhất dương; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là nợ vay ròng; không dùng một mình để kết luận rủi ro.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.12 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-03T09:13:52+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-08-08 -> 2026-08-11.
- XGBoost: độ chính xác cân bằng 0.510; AUC 0.574; log-loss 0.687.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.528; AUC 0.559.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 27.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -25.8%; Sharpe -0.86; mức sụt giảm tối đa -29.2%.

### Breakdown trước phí / sau phí

| Kịch bản | Kết quả | Diễn giải |
|---|---:|---|
| Kịch bản trước chi phí | +2.2% | Gross PnL 2,177,779 VND; chưa trừ commission/slippage/tax. |
| Chi phí giao dịch | -31.9% | 67 vòng; entry 20.0 bps + exit 30.0 bps = 50.0 bps/vòng; tổng phí 28,972,654 VND. |
| Kịch bản sau chi phí | -25.8% | Net PnL -25,799,654 VND; gross - cost gap khoảng +28.0%. |
| Ngưỡng phí hòa vốn | 3.4 bps/vòng | Phí hiện tại 50.0 bps/vòng; cao hơn ngưỡng này thì gross dương vẫn có thể thành net âm. |
| Kết luận hành động | CHƯA CÓ LỢI THẾ (NO_EDGE) | Không mở vị thế mới; nếu đang giữ thì ưu tiên giảm/bán theo kỷ luật vì sau phí vẫn âm. |
| Cách cải thiện cần test | Giảm turnover | Hiện có 67 phiên active/67 vòng; nên test threshold 0.58/0.60/0.62 hoặc giữ nhiều phiên hơn. |

### Bảng chính: turnover, gross, phí và net

| Kịch bản | Cách chọn | Vòng | Gross trước phí | Phí | Net sau phí | Sharpe | Ghi chú |
|---|---|---:|---:|---:|---:|---:|---|
| Gốc | Ngưỡng gốc ≥ 0.55 | 67 | +2.2% | 31.9% | -25.8% | -0.86 | Baseline 61 vòng nếu model phát tín hiệu nhiều. |
| Ngưỡng 0.58 | Chỉ vào lệnh khi xác suất ≥ 0.58 | 40 | +21.7% | 19.2% | +0.5% | 0.06 | Tăng ngưỡng để giảm vòng lệnh. |
| Ngưỡng 0.60 | Chỉ vào lệnh khi xác suất ≥ 0.60 | 25 | +23.9% | 12.0% | +10.0% | 0.46 | Tăng ngưỡng để giảm vòng lệnh. |
| Ngưỡng 0.62 | Chỉ vào lệnh khi xác suất ≥ 0.62 | 17 | +17.8% | 8.2% | +8.6% | 0.45 | Tăng ngưỡng để giảm vòng lệnh. |
| Giới hạn 10 vòng | Tối đa 10 vòng, ưu tiên xác suất cao hơn | 10 | +15.4% | 4.8% | +10.0% | 0.56 | Ngưỡng xác suất trong nhóm: 66.1%. |
| Giới hạn 5 vòng | Tối đa 5 vòng, ưu tiên xác suất cao hơn | 5 | +4.6% | 2.4% | +2.2% | 0.20 | Ngưỡng xác suất trong nhóm: 69.9%. |
| Giới hạn 1 vòng | Tối đa 1 vòng, ưu tiên xác suất cao hơn | 1 | -0.8% | 0.5% | -1.3% | -0.58 | Ngưỡng xác suất trong nhóm: 76.9%. |
Ghi chú: đọc bảng từ trái sang phải để thấy phí giảm khi turnover giảm; các dòng 10/5/1 giới hạn số vòng bằng xác suất model cao hơn, không phải chọn lệnh thắng sau khi biết kết quả và không tự biến NO_EDGE thành BUY.
- Mức độ quan trọng của đặc trưng: close_vs_sma20=15.22; return_1d=14.67; stoch_k_14=12.02; day_of_week=11.51; beta_60d=11.35; excess_return_1d=11.18.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 70.11; mục tiêu 1 73.30; mục tiêu 2 79.18.
- Tỷ lệ lợi nhuận/rủi ro 2.05; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 70.39 (-0.58%).
- P10/P90 cuối kỳ 63.03 / 79.18.
- Lịch giao dịch: VN stock calendar: loại Thứ Bảy/Chủ Nhật và các ngày nghỉ 2026 đã công bố; ngày làm bù Thứ Bảy không được tính là phiên giao dịch chứng khoán.
- Ngày nghỉ đã loại khỏi forecast: 2026-01-01, 2026-01-02, 2026-02-16, 2026-02-17, 2026-02-18, 2026-02-19, 2026-02-20, 2026-04-27, 2026-04-30, 2026-05-01, 2026-08-31, 2026-09-01, 2026-09-02.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.510 < 0.520.
- Điều kiện phát hành tín hiệu: Probability 48.6% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.2579965400000007, Sharpe=-0.8598343376559678.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 48.6%.
- Mô hình Logistic đối chứng: 46.0%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 47.2%.
- Mức dừng lỗ tham chiếu 70.11, mục tiêu 1 73.30, tỷ lệ lợi nhuận/rủi ro 2.05.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
