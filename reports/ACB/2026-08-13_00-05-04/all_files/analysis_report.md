# Báo cáo ngày 2026-08-13 - ACB

## Tổng quan

- Dữ liệu: 2008-03-05 -> 2026-08-12, 4,598 phiên.
- Giá đóng cửa: 22.75 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng (điểm 4).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 48.9%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 22.59; SMA60 22.32; RSI14 54.4.
- MACD 0.019; đường tín hiệu 0.006; biểu đồ cột 0.013.
- ATR14 0.48; ATR% 2.1%; ADX14 21.9.
- Xu hướng: Tích cực - Giá nằm trên SMA20 và SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Trung tính - RSI 54.4.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Đi ngang - ADX 21.9.
- Thanh khoản: Thấp - 0.68 lần trung bình.
- Stochastic: Cực trị - %K 95.0, %D 83.6.

## Phân tích cơ bản

- Doanh nghiệp: ACB.
- Ngành: Banks.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 8.39.
- P/B: 1.32.
- ROE: 16.3%.
- ROA: 1.5%.
- Market cap: 131,470.2 tỷ.
- Revenue Growth: -1.6%.
- Profit Growth: -12.1%.
- P/E 8.39: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 1.32: nên đọc cùng ROE và đặc thù ngành.
- ROE 16.3%: hiệu quả vốn chủ sở hữu tốt.
- Debt/Equity 9.75: đòn bẩy cao, cần đọc theo ngành.
- NPL 1.0%: đang ở mức kiểm soát.
- Revenue Growth -1.6% YoY.
- Profit Growth -12.1% YoY.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.20 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-06T10:36:23+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-11-20 -> 2026-08-11.
- XGBoost: độ chính xác cân bằng 0.513; AUC 0.522; log-loss 0.690.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.499; AUC 0.527.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 46.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -10.3%; Sharpe -0.60; mức sụt giảm tối đa -10.8%.

### Breakdown trước phí / sau phí

| Kịch bản | Kết quả | Diễn giải |
|---|---:|---|
| Kịch bản trước chi phí | +11.0% | Gross PnL 10,976,480 VND; chưa trừ commission/slippage/tax. |
| Chi phí giao dịch | -21.3% | 43 vòng; entry 20.0 bps + exit 30.0 bps = 50.0 bps/vòng; tổng phí 19,955,541 VND. |
| Kịch bản sau chi phí | -10.3% | Net PnL -10,298,541 VND; gross - cost gap khoảng +21.3%. |
| Ngưỡng phí hòa vốn | 25.8 bps/vòng | Phí hiện tại 50.0 bps/vòng; cao hơn ngưỡng này thì gross dương vẫn có thể thành net âm. |
| Kết luận hành động | CHƯA CÓ LỢI THẾ (NO_EDGE) | Không mở vị thế mới; nếu đang giữ thì ưu tiên giảm/bán theo kỷ luật vì sau phí vẫn âm. |
| Cách cải thiện cần test | Giảm turnover | Hiện có 43 phiên active/43 vòng; nên test threshold 0.58/0.60/0.62 hoặc giữ nhiều phiên hơn. |

### Bảng chính: turnover, gross, phí và net

| Kịch bản | Cách chọn | Vòng | Gross trước phí | Phí | Net sau phí | Sharpe | Ghi chú |
|---|---|---:|---:|---:|---:|---:|---|
| Gốc | Ngưỡng gốc ≥ 0.55 | 43 | +11.0% | 21.3% | -10.3% | -0.60 | Baseline 61 vòng nếu model phát tín hiệu nhiều. |
| Ngưỡng 0.58 | Chỉ vào lệnh khi xác suất ≥ 0.58 | 19 | +15.8% | 9.4% | +5.4% | 0.43 | Tăng ngưỡng để giảm vòng lệnh. |
| Ngưỡng 0.60 | Chỉ vào lệnh khi xác suất ≥ 0.60 | 13 | +16.9% | 6.5% | +9.6% | 0.80 | Tăng ngưỡng để giảm vòng lệnh. |
| Ngưỡng 0.62 | Chỉ vào lệnh khi xác suất ≥ 0.62 | 12 | +15.9% | 6.0% | +9.3% | 0.77 | Tăng ngưỡng để giảm vòng lệnh. |
| Giới hạn 10 vòng | Tối đa 10 vòng, ưu tiên xác suất cao hơn | 10 | +9.5% | 5.0% | +4.2% | 0.43 | Ngưỡng xác suất trong nhóm: 63.2%. |
| Giới hạn 5 vòng | Tối đa 5 vòng, ưu tiên xác suất cao hơn | 5 | +9.6% | 2.5% | +6.9% | 0.85 | Ngưỡng xác suất trong nhóm: 64.1%. |
| Giới hạn 1 vòng | Tối đa 1 vòng, ưu tiên xác suất cao hơn | 1 | +2.7% | 0.5% | +2.1% | 0.61 | Ngưỡng xác suất trong nhóm: 85.6%. |
Ghi chú: đọc bảng từ trái sang phải để thấy phí giảm khi turnover giảm; các dòng 10/5/1 giới hạn số vòng bằng xác suất model cao hơn, không phải chọn lệnh thắng sau khi biết kết quả và không tự biến NO_EDGE thành BUY.
- Mức độ quan trọng của đặc trưng: market_return_1d=13.03; relative_strength_20d=12.16; return_1d=11.34; return_2d=11.34; beta_60d=10.33; return_5d=10.29.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 22.10; mục tiêu 1 24.79; mục tiêu 2 24.79.
- Tỷ lệ lợi nhuận/rủi ro 2.51; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 22.56 (-0.82%).
- P10/P90 cuối kỳ 20.88 / 24.79.
- Lịch giao dịch: VN stock calendar: loại Thứ Bảy/Chủ Nhật và các ngày nghỉ 2026 đã công bố; ngày làm bù Thứ Bảy không được tính là phiên giao dịch chứng khoán.
- Ngày nghỉ đã loại khỏi forecast: 2026-01-01, 2026-01-02, 2026-02-16, 2026-02-17, 2026-02-18, 2026-02-19, 2026-02-20, 2026-04-27, 2026-04-30, 2026-05-01, 2026-08-31, 2026-09-01, 2026-09-02.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.522 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.513 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5217332843299838, AUC logistic=0.5274523337845227.
- Điều kiện phát hành tín hiệu: Probability 48.9% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.10298540999999994, Sharpe=-0.6023229276200178.
- Xu hướng ngắn hạn thuận: giá trên SMA20 và SMA60.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 48.9%.
- Mô hình Logistic đối chứng: 46.7%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 44.7%.
- Mức dừng lỗ tham chiếu 22.10, mục tiêu 1 24.79, tỷ lệ lợi nhuận/rủi ro 2.51.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
