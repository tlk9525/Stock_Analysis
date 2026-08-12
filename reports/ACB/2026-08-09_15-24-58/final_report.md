# Báo cáo ngày 2026-08-09 - ACB

## Tổng quan

- Dữ liệu: 2008-03-06 -> 2026-08-07, 4,594 phiên.
- Giá đóng cửa: 22.40 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Trung tính (điểm -1).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 50.5%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 22.61; SMA60 22.17; RSI14 49.2.
- MACD -0.042; đường tín hiệu 0.011; biểu đồ cột -0.053.
- ATR14 0.52; ATR% 2.3%; ADX14 24.4.
- Xu hướng: Trung tính - Giá trên SMA60 nhưng chưa vượt SMA20.
- MACD: Cẩn thận - MACD dưới signal, histogram âm.
- RSI14: Trung tính - RSI 49.2.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Đi ngang - ADX 24.4.
- Thanh khoản: Thấp - 0.55 lần trung bình.
- Stochastic: Hồi phục - %K nằm trên %D.

## Phân tích cơ bản

- Doanh nghiệp: ACB.
- Ngành: Banks.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 8.29.
- P/B: 1.31.
- ROE: 16.3%.
- ROA: 1.5%.
- Market cap: 130,019.1 tỷ.
- Revenue Growth: -1.6%.
- Profit Growth: -12.1%.
- P/E 8.29: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 1.31: nên đọc cùng ROE và đặc thù ngành.
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

- Kiểm thử: 2023-11-20 -> 2026-08-06.
- XGBoost: độ chính xác cân bằng 0.511; AUC 0.522; log-loss 0.690.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.500; AUC 0.527.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 46.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -10.2%; Sharpe -0.60; mức sụt giảm tối đa -10.8%.
- Mức độ quan trọng của đặc trưng: market_return_1d=12.16; return_1d=11.46; relative_strength_20d=11.36; return_2d=11.31; beta_60d=11.19; return_5d=10.80.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 21.95; mục tiêu 1 23.85; mục tiêu 2 24.47.
- Tỷ lệ lợi nhuận/rủi ro 2.36; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 22.18 (-1.00%).
- P10/P90 cuối kỳ 20.55 / 24.47.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.522 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.511 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5216411426088845, AUC logistic=0.5271079975381051.
- Điều kiện phát hành tín hiệu: Probability 50.5% < 55.0%.
- Điều kiện phát hành tín hiệu: Technical score -1 < 2.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.10245695999999993, Sharpe=-0.6002212379316486.
- Trung hạn chưa xấu, ngắn hạn yếu vì giá dưới SMA20.
- Xu hướng kỹ thuật nghiêng về: Trung tính.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 50.5%.
- Mô hình Logistic đối chứng: 48.0%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 43.9%.
- Mức dừng lỗ tham chiếu 21.95, mục tiêu 1 23.85, tỷ lệ lợi nhuận/rủi ro 2.36.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. News Reader đã trích đoạn có nguồn của 4 bài để phân loại chủ đề (ket_qua_kinh_doanh: 2, co_tuc_va_hanh_dong_doanh_nghiep: 1, vi_mo: 1, nganh: 1, rui_ro: 2), nhưng các trích đoạn này không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Trung tính; điểm -1. Chi tiết artifact: Xu hướng: Trung tính (Giá trên SMA60 nhưng chưa vượt SMA20.); MACD: Cẩn thận (MACD dưới signal, histogram âm.); RSI14: Trung tính (RSI 49.2.); Bollinger: Ổn định (Giá nằm trong dải Bollinger.); ADX: Đi ngang (ADX 24.4.); Thanh khoản: Thấp (0.55 lần trung bình.); Stochastic: Hồi phục (%K nằm trên %D.)
- Góc nhìn cơ bản: Artifact cơ bản: ACB; kỳ 2026-Q2; P/E 8.29; P/B 1.31; ROE 16.3%; ROA 1.5%; Debt/Equity 9.75; Revenue Growth -1.6%; Profit Growth -12.1%.
- Tin doanh nghiệp: Đã đọc trích đoạn giới hạn của 4 bài; phân nhóm rule-based: ket_qua_kinh_doanh: 2, co_tuc_va_hanh_dong_doanh_nghiep: 1, vi_mo: 1, nganh: 1, rui_ro: 2. Tác động cần kiểm chứng: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường. Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động. Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh. So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp. Xác minh công bố chính thức, phạm vi ảnh hưởng và khả năng định lượng rủi ro. Đây không phải sentiment hay dự báo tác động giá.
- Live research: Live snapshot lấy lúc 2026-08-09T08:25:12.615070+00:00; News Reader đọc được 4 bài. ML có 6 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest.

### Bằng chứng

- ML decision artifact: NO_EDGE. AUC 0.522 < 0.540
- ML decision artifact: NO_EDGE. Balanced accuracy 0.511 < 0.520
- ML decision artifact: NO_EDGE. XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5216411426088845, AUC logistic=0.5271079975381051
- ML decision artifact: NO_EDGE. Probability 50.5% < 55.0%
- ML decision artifact: NO_EDGE. Technical score -1 < 2
- ML decision artifact: NO_EDGE. Lợi thế OOS ròng không đạt: return=-0.10245695999999993, Sharpe=-0.6002212379316486
- News Reader [VOV.VN]: Một số cổ phiếu cần quan tâm 3/8: Cơ hội đầu tư tiềm năng với ACB và POW - VOV.VN | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh, rui_ro (2026-08-02T22:00:00+00:00)
- News Reader [congly.vn]: ACB vào rổ 20 cổ phiếu phát triển bền vững VNSI 2026 - congly.vn | nhóm: ket_qua_kinh_doanh, rui_ro (2026-08-04T03:54:07+00:00)
- News Reader [fili.vn]: Ngày 06/08/2026: 10 cổ phiếu nóng dưới góc nhìn PTKT của Vietstock - fili.vn | nhóm: khác (2026-08-06T02:00:48+00:00)
- News Reader [fili.vn]: Ngày 04/08/2026: 10 cổ phiếu nóng dưới góc nhìn PTKT của Vietstock - fili.vn | nhóm: khác (2026-08-04T01:58:00+00:00)

### Rủi ro cần kiểm chứng

- ML guard: AUC 0.522 < 0.540
- ML guard: Balanced accuracy 0.511 < 0.520
- ML guard: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5216411426088845, AUC logistic=0.5271079975381051
- ML guard: Probability 50.5% < 55.0%
- ML guard: Technical score -1 < 2
- ML guard: Lợi thế OOS ròng không đạt: return=-0.10245695999999993, Sharpe=-0.6002212379316486
- News Reader: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường.
- News Reader: Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động.
- News Reader: Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh.
- News Reader: So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp.
- News Reader: Xác minh công bố chính thức, phạm vi ảnh hưởng và khả năng định lượng rủi ro.
- Chỉ lưu trích đoạn giới hạn để kiểm chứng nguồn; không lưu hay hiển thị toàn văn bài báo.
- Phân nhóm là keyword rule-based để định tuyến research, không phải sentiment hay dự báo tác động giá.
- Dữ liệu News Reader chỉ phục vụ research/report; không dùng làm feature train/backtest khi chưa có lịch sử available_at point-in-time.
- Tin live/trích đoạn cần mở URL gốc để kiểm chứng bối cảnh, số liệu và thời điểm trước khi sử dụng.

### Nguồn live research

- [VOV.VN] Một số cổ phiếu cần quan tâm 3/8: Cơ hội đầu tư tiềm năng với ACB và POW - VOV.VN (2026-08-02T22:00:00+00:00): https://vov.vn/thi-truong/mot-so-co-phieu-can-quan-tam-38-co-hoi-dau-tu-tiem-nang-voi-acb-va-pow-post1320406.vov
- [congly.vn] ACB vào rổ 20 cổ phiếu phát triển bền vững VNSI 2026 - congly.vn (2026-08-04T03:54:07+00:00): https://doanhnhan.congly.vn/acb-vao-ro-20-co-phieu-phat-trien-ben-vung-vnsi-2026.html
- [fili.vn] Ngày 06/08/2026: 10 cổ phiếu nóng dưới góc nhìn PTKT của Vietstock - fili.vn (2026-08-06T02:00:48+00:00): https://fili.vn/2026/08/ngay-06082026-10-co-phieu-nong-duoi-goc-nhin-ptkt-cua-vietstock-585-1477037.htm
- [fili.vn] Ngày 04/08/2026: 10 cổ phiếu nóng dưới góc nhìn PTKT của Vietstock - fili.vn (2026-08-04T01:58:00+00:00): https://fili.vn/2026/08/ngay-04082026-10-co-phieu-nong-duoi-goc-nhin-ptkt-cua-vietstock-585-1475953.htm

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.
