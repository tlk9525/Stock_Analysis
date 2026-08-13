# Báo cáo ngày 2026-08-12 - STB

## Tổng quan

- Dữ liệu: 2008-03-10 -> 2026-08-12, 4,594 phiên.
- Giá đóng cửa: 74.10 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng (điểm 4).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 50.0%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 72.78; SMA60 71.38; RSI14 56.8.
- MACD 0.700; đường tín hiệu 0.494; biểu đồ cột 0.206.
- ATR14 2.00; ATR% 2.7%; ADX14 15.5.
- Xu hướng: Tích cực - Giá nằm trên SMA20 và SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 56.8.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Đi ngang - ADX 15.5.
- Thanh khoản: Thấp - 0.39 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: NH Sài Gòn Tài Lộc (SACOMBANK).
- Ngành: Banks.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 45.48.
- P/B: 2.23.
- ROE: 5.0%.
- ROA: 0.4%.
- Market cap: 140,071.5 tỷ.
- Revenue Growth: 28.1%.
- Profit Growth: -53.5%.
- P/E 45.48: định giá cao, cần tăng trưởng lợi nhuận hỗ trợ.
- P/B 2.23: nên đọc cùng ROE và đặc thù ngành.
- ROE 5.0%: hiệu quả vốn còn yếu.
- Debt/Equity 13.20: đòn bẩy cao, cần đọc theo ngành.
- NPL 7.5%: cần theo dõi.
- Revenue Growth 28.1% YoY.
- Profit Growth -53.5% YoY.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.10 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-07T09:37:32+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-08-23 -> 2026-08-11.
- XGBoost: độ chính xác cân bằng 0.504; AUC 0.504; log-loss 0.693.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.514; AUC 0.511.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 33.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -13.4%; Sharpe -0.48; mức sụt giảm tối đa -19.5%.
- Mức độ quan trọng của đặc trưng: market_return_1d=13.54; return_5d=11.91; beta_60d=11.88; range_pct=11.51; return_1d=11.23; bb_position_20=11.11.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 71.09; mục tiêu 1 84.34; mục tiêu 2 84.34.
- Tỷ lệ lợi nhuận/rủi ro 2.92; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 73.34 (-1.03%).
- P10/P90 cuối kỳ 64.53 / 84.34.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.504 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.504 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5035330612004303, AUC logistic=0.5105512901752163.
- Điều kiện phát hành tín hiệu: Probability 50.0% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.13432860000000035, Sharpe=-0.48071319287150394.
- Xu hướng ngắn hạn thuận: giá trên SMA20 và SMA60.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 50.0%.
- Mô hình Logistic đối chứng: 45.2%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 46.0%.
- Mức dừng lỗ tham chiếu 71.09, mục tiêu 1 84.34, tỷ lệ lợi nhuận/rủi ro 2.92.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. News Reader đã trích đoạn có nguồn của 1 bài để phân loại chủ đề (ket_qua_kinh_doanh: 1, nganh: 1, rui_ro: 1), nhưng các trích đoạn này không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Hồi phục / nghiêng tăng; điểm 4. Chi tiết artifact: Xu hướng: Tích cực (Giá nằm trên SMA20 và SMA60.); MACD: Tích cực (MACD trên signal, histogram dương.); RSI14: Tích cực (RSI 56.8.); Bollinger: Ổn định (Giá nằm trong dải Bollinger.); ADX: Đi ngang (ADX 15.5.); Thanh khoản: Thấp (0.39 lần trung bình.); Stochastic: Yếu lại (%K nằm dưới %D.)
- Góc nhìn cơ bản: Artifact cơ bản: NH Sài Gòn Tài Lộc (SACOMBANK); kỳ 2026-Q2; P/E 45.48; P/B 2.23; ROE 5.0%; ROA 0.4%; Debt/Equity 13.20; Revenue Growth 28.1%; Profit Growth -53.5%.
- Tin doanh nghiệp: Đã đọc trích đoạn giới hạn của 1 bài; phân nhóm rule-based: ket_qua_kinh_doanh: 1, nganh: 1, rui_ro: 1. Tác động cần kiểm chứng: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường. So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp. Xác minh công bố chính thức, phạm vi ảnh hưởng và khả năng định lượng rủi ro. Đây không phải sentiment hay dự báo tác động giá.
- Live research: Live snapshot lấy lúc 2026-08-12T15:34:31.091521+00:00; News Reader đọc được 1 bài. ML có 5 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest.

### Bằng chứng

- ML decision artifact: NO_EDGE. AUC 0.504 < 0.540
- ML decision artifact: NO_EDGE. Balanced accuracy 0.504 < 0.520
- ML decision artifact: NO_EDGE. XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5035330612004303, AUC logistic=0.5105512901752163
- ML decision artifact: NO_EDGE. Probability 50.0% < 55.0%
- ML decision artifact: NO_EDGE. Lợi thế OOS ròng không đạt: return=-0.13432860000000035, Sharpe=-0.48071319287150394
- News Reader [dautucophieu.net]: Cập nhật cổ phiếu STB – Q2/2026: Chi phí dự phòng gia tăng áp lực lên lợi nhuận - dautucophieu.net | nhóm: ket_qua_kinh_doanh, nganh, rui_ro (2026-08-11T04:22:31+00:00)

### Rủi ro cần kiểm chứng

- ML guard: AUC 0.504 < 0.540
- ML guard: Balanced accuracy 0.504 < 0.520
- ML guard: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5035330612004303, AUC logistic=0.5105512901752163
- ML guard: Probability 50.0% < 55.0%
- ML guard: Lợi thế OOS ròng không đạt: return=-0.13432860000000035, Sharpe=-0.48071319287150394
- News Reader: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường.
- News Reader: So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp.
- News Reader: Xác minh công bố chính thức, phạm vi ảnh hưởng và khả năng định lượng rủi ro.
- Chỉ lưu trích đoạn giới hạn để kiểm chứng nguồn; không lưu hay hiển thị toàn văn bài báo.
- Phân nhóm là keyword rule-based để định tuyến research, không phải sentiment hay dự báo tác động giá.
- Dữ liệu News Reader chỉ phục vụ research/report; không dùng làm feature train/backtest khi chưa có lịch sử available_at point-in-time.
- Tin live/trích đoạn cần mở URL gốc để kiểm chứng bối cảnh, số liệu và thời điểm trước khi sử dụng.

### Nguồn live research

- [dautucophieu.net] Cập nhật cổ phiếu STB – Q2/2026: Chi phí dự phòng gia tăng áp lực lên lợi nhuận - dautucophieu.net (2026-08-11T04:22:31+00:00): https://dautucophieu.net/cap-nhat-co-phieu-stb-q2-2026-chi-phi-du-phong-gia-tang-ap-luc-len-loi-nhuan/

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.

---

## News model riêng từng mã

- Symbol-news report: `/Users/tranlekhoa/Documents/DATA_SCI/vn_stock_analysis/reports/STB/2026-08-12_22-34-34_news_model`
- Số bài tin trong CSV cho mã: 2
- Số dòng giá có news feature: 5
- XGBoost probability mới nhất: 0.500
- AUC OOS: 0.512
- Balanced accuracy OOS: 0.497
- Backtest total return: -0.097

Lưu ý: news model dùng dữ liệu `available_at` point-in-time trong CSV tích lũy; nếu lịch sử tin còn mỏng thì chỉ xem là research/smoke test.
