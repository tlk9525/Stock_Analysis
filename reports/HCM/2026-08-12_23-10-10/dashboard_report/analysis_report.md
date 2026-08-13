# Báo cáo ngày 2026-08-12 - HCM

## Tổng quan

- Dữ liệu: 2009-05-19 -> 2026-08-12, 4,301 phiên.
- Giá đóng cửa: 26.15 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng (điểm 4).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 52.6%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 25.51; SMA60 24.40; RSI14 59.9.
- MACD 0.420; đường tín hiệu 0.365; biểu đồ cột 0.055.
- ATR14 0.85; ATR% 3.3%; ADX14 15.4.
- Xu hướng: Tích cực - Giá nằm trên SMA20 và SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 59.9.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Đi ngang - ADX 15.4.
- Thanh khoản: Thấp - 0.59 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: Chứng khoán HSC.
- Ngành: Financial Services.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 20.17.
- P/B: 2.06.
- ROE: 9.8%.
- ROA: 3.1%.
- Market cap: 35,773.6 tỷ.
- Revenue Growth: 15.1%.
- Profit Growth: 42.0%.
- P/E 20.17: định giá cao, cần tăng trưởng lợi nhuận hỗ trợ.
- P/B 2.06: nên đọc cùng ROE và đặc thù ngành.
- ROA 3.1%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 1.54: thanh khoản ngắn hạn khá.
- Revenue Growth 15.1% YoY.
- Profit Growth 42.0% YoY.
- CFO/LNST 1.16: chất lượng chuyển đổi lợi nhuận sang tiền mặt khá tốt.
- Dòng tiền tự do quý gần nhất dương; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là nợ vay ròng; không dùng một mình để kết luận rủi ro.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.14 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-11T09:51:00+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-10-17 -> 2026-08-11.
- XGBoost: độ chính xác cân bằng 0.518; AUC 0.558; log-loss 0.687.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.519; AUC 0.563.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 51.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -12.6%; Sharpe -0.34; mức sụt giảm tối đa -20.4%.

### Breakdown trước phí / sau phí

| Kịch bản | Kết quả | Diễn giải |
|---|---:|---|
| Kịch bản trước chi phí | +18.3% | Gross PnL 18,289,135 VND; chưa trừ commission/slippage/tax. |
| Chi phí giao dịch | -30.3% | 61 vòng; entry 20.0 bps + exit 30.0 bps = 50.0 bps/vòng; tổng phí 28,355,115 VND. |
| Kịch bản sau chi phí | -12.6% | Net PnL -12,580,115 VND; gross - cost gap khoảng +30.9%. |
| Ngưỡng phí hòa vốn | 30.2 bps/vòng | Phí hiện tại 50.0 bps/vòng; cao hơn ngưỡng này thì gross dương vẫn có thể thành net âm. |
| Kết luận hành động | CHƯA CÓ LỢI THẾ (NO_EDGE) | Không mở vị thế mới; nếu đang giữ thì ưu tiên giảm/bán theo kỷ luật vì sau phí vẫn âm. |
| Cách cải thiện cần test | Giảm turnover | Hiện có 61 phiên active/61 vòng; nên test threshold 0.58/0.60/0.62 hoặc giữ nhiều phiên hơn. |
- Mức độ quan trọng của đặc trưng: volatility_20d=13.74; macd_pct=12.47; return_1d=11.38; corr_60d=11.30; market_return_1d=10.80; return_20d=10.52.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 24.88; mục tiêu 1 29.82; mục tiêu 2 29.82.
- Tỷ lệ lợi nhuận/rủi ro 2.52; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 25.96 (-0.71%).
- P10/P90 cuối kỳ 22.79 / 29.82.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.518 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5579594897488298, AUC logistic=0.5625782846595029.
- Điều kiện phát hành tín hiệu: Probability 52.6% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.12580115000000103, Sharpe=-0.3371169628402055.
- Xu hướng ngắn hạn thuận: giá trên SMA20 và SMA60.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 52.6%.
- Mô hình Logistic đối chứng: 45.9%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 47.3%.
- Mức dừng lỗ tham chiếu 24.88, mục tiêu 1 29.82, tỷ lệ lợi nhuận/rủi ro 2.52.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
