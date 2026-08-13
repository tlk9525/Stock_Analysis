# Báo cáo ngày 2026-08-13 - BID

## Tổng quan

- Dữ liệu: 2014-01-24 -> 2026-08-12, 3,127 phiên.
- Giá đóng cửa: 39.25 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Trung tính (điểm 0).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 40.2%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 37.44; SMA60 40.14; RSI14 55.4.
- MACD -0.156; đường tín hiệu -0.607; biểu đồ cột 0.450.
- ATR14 1.02; ATR% 2.6%; ADX14 24.6.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 55.4.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Đi ngang - ADX 24.6.
- Thanh khoản: Thấp - 0.61 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: BIDV.
- Ngành: Banks.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 8.60.
- P/B: 1.47.
- ROE: 17.7%.
- ROA: 1.0%.
- Market cap: 284,650.5 tỷ.
- Revenue Growth: 7.0%.
- Profit Growth: 20.6%.
- P/E 8.60: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 1.47: nên đọc cùng ROE và đặc thù ngành.
- ROE 17.7%: hiệu quả vốn chủ sở hữu tốt.
- Debt/Equity 16.31: đòn bẩy cao, cần đọc theo ngành.
- NPL 1.8%: đang ở mức kiểm soát.
- Revenue Growth 7.0% YoY.
- Profit Growth 20.6% YoY.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.16 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-06T10:32:48+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-10-09 -> 2026-08-11.
- XGBoost: độ chính xác cân bằng 0.504; AUC 0.576; log-loss 0.677.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.514; AUC 0.540.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 93.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -25.3%; Sharpe -1.14; mức sụt giảm tối đa -29.1%.

### Breakdown trước phí / sau phí

| Kịch bản | Kết quả | Diễn giải |
|---|---:|---|
| Kịch bản trước chi phí | -2.6% | Gross PnL -2,605,096 VND; chưa trừ commission/slippage/tax. |
| Chi phí giao dịch | -26.4% | 54 vòng; entry 20.0 bps + exit 30.0 bps = 50.0 bps/vòng; tổng phí 21,685,625 VND. |
| Kịch bản sau chi phí | -25.3% | Net PnL -25,265,625 VND; gross - cost gap khoảng +22.7%. |
| Ngưỡng phí hòa vốn | -4.9 bps/vòng | Phí hiện tại 50.0 bps/vòng; cao hơn ngưỡng này thì gross dương vẫn có thể thành net âm. |
| Kết luận hành động | CHƯA CÓ LỢI THẾ (NO_EDGE) | Không đủ lợi thế sau phí; giữ NO_EDGE. |
| Cách cải thiện cần test | Giảm turnover | Hiện có 54 phiên active/54 vòng; nên test threshold 0.58/0.60/0.62 hoặc giữ nhiều phiên hơn. |

### Bảng chính: turnover, gross, phí và net

| Kịch bản | Cách chọn | Vòng | Gross trước phí | Phí | Net sau phí | Sharpe | Ghi chú |
|---|---|---:|---:|---:|---:|---:|---|
| Gốc | Ngưỡng gốc ≥ 0.55 | 54 | -2.6% | 26.4% | -25.3% | -1.14 | Baseline 61 vòng nếu model phát tín hiệu nhiều. |
| Ngưỡng 0.58 | Chỉ vào lệnh khi xác suất ≥ 0.58 | 27 | +12.8% | 13.3% | -1.2% | -0.05 | Tăng ngưỡng để giảm vòng lệnh. |
| Ngưỡng 0.60 | Chỉ vào lệnh khi xác suất ≥ 0.60 | 17 | +13.0% | 8.4% | +4.0% | 0.28 | Tăng ngưỡng để giảm vòng lệnh. |
| Ngưỡng 0.62 | Chỉ vào lệnh khi xác suất ≥ 0.62 | 13 | +14.0% | 6.4% | +7.0% | 0.50 | Tăng ngưỡng để giảm vòng lệnh. |
| Giới hạn 10 vòng | Tối đa 10 vòng, ưu tiên xác suất cao hơn | 10 | +10.6% | 4.9% | +5.3% | 0.40 | Ngưỡng xác suất trong nhóm: 63.4%. |
| Giới hạn 5 vòng | Tối đa 5 vòng, ưu tiên xác suất cao hơn | 5 | +11.8% | 2.5% | +9.1% | 0.71 | Ngưỡng xác suất trong nhóm: 69.4%. |
| Giới hạn 1 vòng | Tối đa 1 vòng, ưu tiên xác suất cao hơn | 1 | +3.9% | 0.5% | +3.4% | 0.60 | Ngưỡng xác suất trong nhóm: 85.3%. |
Ghi chú: đọc bảng từ trái sang phải để thấy phí giảm khi turnover giảm; các dòng 10/5/1 giới hạn số vòng bằng xác suất model cao hơn, không phải chọn lệnh thắng sau khi biết kết quả và không tự biến NO_EDGE thành BUY.
- Mức độ quan trọng của đặc trưng: return_1d=10.23; return_2d=9.63; day_of_week=9.63; corr_60d=9.06; range_pct=8.75; excess_return_1d=8.63.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 37.72; mục tiêu 1 44.08; mục tiêu 2 44.08.
- Tỷ lệ lợi nhuận/rủi ro 2.69; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 38.78 (-1.21%).
- P10/P90 cuối kỳ 34.74 / 44.08.
- Lịch giao dịch: VN stock calendar: loại Thứ Bảy/Chủ Nhật và các ngày nghỉ 2026 đã công bố; ngày làm bù Thứ Bảy không được tính là phiên giao dịch chứng khoán.
- Ngày nghỉ đã loại khỏi forecast: 2026-01-01, 2026-01-02, 2026-02-16, 2026-02-17, 2026-02-18, 2026-02-19, 2026-02-20, 2026-04-27, 2026-04-30, 2026-05-01, 2026-08-31, 2026-09-01, 2026-09-02.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.504 < 0.520.
- Điều kiện phát hành tín hiệu: Probability 40.2% < 55.0%.
- Điều kiện phát hành tín hiệu: Technical score 0 < 2.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.2526562499999999, Sharpe=-1.1421172553543388.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Trung tính.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 40.2%.
- Mô hình Logistic đối chứng: 45.3%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 44.2%.
- Mức dừng lỗ tham chiếu 37.72, mục tiêu 1 44.08, tỷ lệ lợi nhuận/rủi ro 2.69.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
