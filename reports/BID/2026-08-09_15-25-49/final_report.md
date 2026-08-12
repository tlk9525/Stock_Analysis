# Báo cáo ngày 2026-08-09 - BID

## Tổng quan

- Dữ liệu: 2014-01-24 -> 2026-08-07, 3,124 phiên.
- Giá đóng cửa: 39.05 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng (điểm 4).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 38.3%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 37.47; SMA60 40.37; RSI14 54.9.
- MACD -0.554; đường tín hiệu -0.949; biểu đồ cột 0.395.
- ATR14 1.10; ATR% 2.8%; ADX14 27.9.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Trung tính - RSI 54.9.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng tăng - ADX 27.9, +DI vượt -DI.
- Thanh khoản: Đột biến - 1.93 lần trung bình.
- Stochastic: Cực trị - %K 93.1, %D 78.5.

## Phân tích cơ bản

- Doanh nghiệp: BIDV.
- Ngành: Banks.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 8.59.
- P/B: 1.47.
- ROE: 17.7%.
- ROA: 1.0%.
- Market cap: 284,286.5 tỷ.
- Revenue Growth: 7.0%.
- Profit Growth: 20.6%.
- P/E 8.59: định giá tương đối thấp nếu lợi nhuận bền vững.
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

- Kiểm thử: 2023-10-09 -> 2026-08-06.
- XGBoost: độ chính xác cân bằng 0.503; AUC 0.575; log-loss 0.677.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.514; AUC 0.538.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 93.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -25.3%; Sharpe -1.14; mức sụt giảm tối đa -29.1%.
- Mức độ quan trọng của đặc trưng: return_1d=10.05; day_of_week=9.74; return_2d=9.55; range_pct=9.05; corr_60d=9.02; return_skew_20d=8.73.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 37.40; mục tiêu 1 43.59; mục tiêu 2 43.59.
- Tỷ lệ lợi nhuận/rủi ro 2.35; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 38.46 (-1.51%).
- P10/P90 cuối kỳ 34.40 / 43.59.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.503 < 0.520.
- Điều kiện phát hành tín hiệu: Probability 38.3% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.2526562499999999, Sharpe=-1.1445538913624684.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 38.3%.
- Mô hình Logistic đối chứng: 39.2%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 42.5%.
- Mức dừng lỗ tham chiếu 37.40, mục tiêu 1 43.59, tỷ lệ lợi nhuận/rủi ro 2.35.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. News Reader đã trích đoạn có nguồn của 1 bài để phân loại chủ đề (ket_qua_kinh_doanh: 1, co_tuc_va_hanh_dong_doanh_nghiep: 1, vi_mo: 1, rui_ro: 1), nhưng các trích đoạn này không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Hồi phục / nghiêng tăng; điểm 4. Chi tiết artifact: Xu hướng: Cẩn thận (Giá nằm dưới SMA60.); MACD: Tích cực (MACD trên signal, histogram dương.); RSI14: Trung tính (RSI 54.9.); Bollinger: Ổn định (Giá nằm trong dải Bollinger.); ADX: Xu hướng tăng (ADX 27.9, +DI vượt -DI.); Thanh khoản: Đột biến (1.93 lần trung bình.); Stochastic: Cực trị (%K 93.1, %D 78.5.)
- Góc nhìn cơ bản: Artifact cơ bản: BIDV; kỳ 2026-Q2; P/E 8.59; P/B 1.47; ROE 17.7%; ROA 1.0%; Debt/Equity 16.31; Revenue Growth 7.0%; Profit Growth 20.6%.
- Tin doanh nghiệp: Đã đọc trích đoạn giới hạn của 1 bài; phân nhóm rule-based: ket_qua_kinh_doanh: 1, co_tuc_va_hanh_dong_doanh_nghiep: 1, vi_mo: 1, rui_ro: 1. Tác động cần kiểm chứng: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường. Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động. Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh. Xác minh công bố chính thức, phạm vi ảnh hưởng và khả năng định lượng rủi ro. Đây không phải sentiment hay dự báo tác động giá.
- Live research: Live snapshot lấy lúc 2026-08-09T08:26:02.674357+00:00; News Reader đọc được 1 bài. ML có 3 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest.

### Bằng chứng

- ML decision artifact: NO_EDGE. Balanced accuracy 0.503 < 0.520
- ML decision artifact: NO_EDGE. Probability 38.3% < 55.0%
- ML decision artifact: NO_EDGE. Lợi thế OOS ròng không đạt: return=-0.2526562499999999, Sharpe=-1.1445538913624684
- News Reader [MoneyF]: BIDV sắp phát hành gần 500 triệu cổ phiếu, vốn điều lệ tiến sát 78.000 tỷ đồng - MoneyF | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, rui_ro (2026-08-06T05:45:00+00:00)

### Rủi ro cần kiểm chứng

- ML guard: Balanced accuracy 0.503 < 0.520
- ML guard: Probability 38.3% < 55.0%
- ML guard: Lợi thế OOS ròng không đạt: return=-0.2526562499999999, Sharpe=-1.1445538913624684
- News Reader: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường.
- News Reader: Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động.
- News Reader: Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh.
- News Reader: Xác minh công bố chính thức, phạm vi ảnh hưởng và khả năng định lượng rủi ro.
- Chỉ lưu trích đoạn giới hạn để kiểm chứng nguồn; không lưu hay hiển thị toàn văn bài báo.
- Phân nhóm là keyword rule-based để định tuyến research, không phải sentiment hay dự báo tác động giá.
- Dữ liệu News Reader chỉ phục vụ research/report; không dùng làm feature train/backtest khi chưa có lịch sử available_at point-in-time.
- Tin live/trích đoạn cần mở URL gốc để kiểm chứng bối cảnh, số liệu và thời điểm trước khi sử dụng.

### Nguồn live research

- [MoneyF] BIDV sắp phát hành gần 500 triệu cổ phiếu, vốn điều lệ tiến sát 78.000 tỷ đồng - MoneyF (2026-08-06T05:45:00+00:00): https://moneyf.vn/bidv-sap-phat-hanh-gan-500-trieu-co-phieu-von-dieu-a268geso

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.
