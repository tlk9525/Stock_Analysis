# Báo cáo ngày 2026-08-09 - VCB

## Tổng quan

- Dữ liệu: 2009-06-30 -> 2026-08-07, 4,270 phiên.
- Giá đóng cửa: 59.70 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng (điểm 4).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 50.8%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 57.23; SMA60 60.18; RSI14 56.7.
- MACD -0.073; đường tín hiệu -0.687; biểu đồ cột 0.615.
- ATR14 1.50; ATR% 2.5%; ADX14 27.9.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 56.7.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng tăng - ADX 27.9, +DI vượt -DI.
- Thanh khoản: Bình thường - 1.23 lần trung bình.
- Stochastic: Cực trị - %K 84.5, %D 80.2.

## Phân tích cơ bản

- Doanh nghiệp: Vietcombank.
- Ngành: Banks.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 11.98.
- P/B: 2.01.
- ROE: 17.9%.
- ROA: 1.7%.
- Market cap: 498,833.8 tỷ.
- Revenue Growth: 47.6%.
- Profit Growth: 64.7%.
- P/E 11.98: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 2.01: nên đọc cùng ROE và đặc thù ngành.
- ROE 17.9%: hiệu quả vốn chủ sở hữu tốt.
- Debt/Equity 9.69: đòn bẩy cao, cần đọc theo ngành.
- NPL 0.6%: đang ở mức kiểm soát.
- Revenue Growth 47.6% YoY.
- Profit Growth 64.7% YoY.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.12 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-06T09:03:02+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-11-22 -> 2026-08-06.
- XGBoost: độ chính xác cân bằng 0.503; AUC 0.468; log-loss 0.699.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.477; AUC 0.490.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 30.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -26.4%; Sharpe -2.25; mức sụt giảm tối đa -26.4%.
- Mức độ quan trọng của đặc trưng: return_1d=11.45; atr_pct_14=10.48; market_return_20d=10.36; market_return_1d=10.18; rsi_14=10.01; macd_pct=9.87.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 59.58; mục tiêu 1 61.00; mục tiêu 2 66.65.
- Tỷ lệ lợi nhuận/rủi ro 2.37; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 58.77 (-1.56%).
- P10/P90 cuối kỳ 53.70 / 66.65.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.468 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.503 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.4677033948325432, AUC logistic=0.4902229584356734.
- Điều kiện phát hành tín hiệu: Probability 50.8% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.26417005000000016, Sharpe=-2.2527039312868156.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 50.8%.
- Mô hình Logistic đối chứng: 45.9%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 41.7%.
- Mức dừng lỗ tham chiếu 59.58, mục tiêu 1 61.00, tỷ lệ lợi nhuận/rủi ro 2.37.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. News Reader đã trích đoạn có nguồn của 4 bài để phân loại chủ đề (ket_qua_kinh_doanh: 4, co_tuc_va_hanh_dong_doanh_nghiep: 3, vi_mo: 3, nganh: 4, rui_ro: 1), nhưng các trích đoạn này không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Hồi phục / nghiêng tăng; điểm 4. Chi tiết artifact: Xu hướng: Cẩn thận (Giá nằm dưới SMA60.); MACD: Tích cực (MACD trên signal, histogram dương.); RSI14: Tích cực (RSI 56.7.); Bollinger: Ổn định (Giá nằm trong dải Bollinger.); ADX: Xu hướng tăng (ADX 27.9, +DI vượt -DI.); Thanh khoản: Bình thường (1.23 lần trung bình.); Stochastic: Cực trị (%K 84.5, %D 80.2.)
- Góc nhìn cơ bản: Artifact cơ bản: Vietcombank; kỳ 2026-Q2; P/E 11.98; P/B 2.01; ROE 17.9%; ROA 1.7%; Debt/Equity 9.69; Revenue Growth 47.6%; Profit Growth 64.7%.
- Tin doanh nghiệp: Đã đọc trích đoạn giới hạn của 4 bài; phân nhóm rule-based: ket_qua_kinh_doanh: 4, co_tuc_va_hanh_dong_doanh_nghiep: 3, vi_mo: 3, nganh: 4, rui_ro: 1. Tác động cần kiểm chứng: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường. Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động. Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh. So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp. Xác minh công bố chính thức, phạm vi ảnh hưởng và khả năng định lượng rủi ro. Đây không phải sentiment hay dự báo tác động giá.
- Live research: Live snapshot lấy lúc 2026-08-09T08:38:35.762692+00:00; News Reader đọc được 4 bài. ML có 5 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest.

### Bằng chứng

- ML decision artifact: NO_EDGE. AUC 0.468 < 0.540
- ML decision artifact: NO_EDGE. Balanced accuracy 0.503 < 0.520
- ML decision artifact: NO_EDGE. XGBoost chưa vượt logistic baseline: AUC XGBoost=0.4677033948325432, AUC logistic=0.4902229584356734
- ML decision artifact: NO_EDGE. Probability 50.8% < 55.0%
- ML decision artifact: NO_EDGE. Lợi thế OOS ròng không đạt: return=-0.26417005000000016, Sharpe=-2.2527039312868156
- News Reader [bnews.vn]: Chứng khoán hôm nay: Khuyến nghị mua DMX, POW và chờ mua VCB - bnews.vn | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh (2026-08-07T01:19:00+00:00)
- News Reader [nguoiquansat.vn]: Cổ phiếu đáng chú ý ngày 7/8: DMX, POW, VCB - nguoiquansat.vn | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh (2026-08-06T16:40:01+00:00)
- News Reader [dautucophieu.net]: Cập nhật cổ phiếu VCB – LNTT Q2 tăng 58%, vượt trội so với dự báo - dautucophieu.net | nhóm: ket_qua_kinh_doanh, nganh, rui_ro (2026-08-05T04:45:15+00:00)
- News Reader [VietstockFinance]: VCB: Khuyến nghị MUA với giá mục tiêu 81,400 đồng/cổ phiếu - VietstockFinance | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh (2026-08-06T05:45:18+00:00)

### Rủi ro cần kiểm chứng

- ML guard: AUC 0.468 < 0.540
- ML guard: Balanced accuracy 0.503 < 0.520
- ML guard: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.4677033948325432, AUC logistic=0.4902229584356734
- ML guard: Probability 50.8% < 55.0%
- ML guard: Lợi thế OOS ròng không đạt: return=-0.26417005000000016, Sharpe=-2.2527039312868156
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

- [bnews.vn] Chứng khoán hôm nay: Khuyến nghị mua DMX, POW và chờ mua VCB - bnews.vn (2026-08-07T01:19:00+00:00): https://bnews.vn/chung-khoan-hom-nay-khuyen-nghi-mua-dmx-pow-va-cho-mua-vcb/431720.html
- [nguoiquansat.vn] Cổ phiếu đáng chú ý ngày 7/8: DMX, POW, VCB - nguoiquansat.vn (2026-08-06T16:40:01+00:00): https://nguoiquansat.vn/co-phieu-dang-chu-y-ngay-7-8-dmx-pow-vcb-308947.html
- [dautucophieu.net] Cập nhật cổ phiếu VCB – LNTT Q2 tăng 58%, vượt trội so với dự báo - dautucophieu.net (2026-08-05T04:45:15+00:00): https://dautucophieu.net/cap-nhat-co-phieu-vcb-lntt-q2-tang-58-vuot-troi-so-voi-du-bao/
- [VietstockFinance] VCB: Khuyến nghị MUA với giá mục tiêu 81,400 đồng/cổ phiếu - VietstockFinance (2026-08-06T05:45:18+00:00): https://finance.vietstock.vn/bao-cao-phan-tich/21362/vcb-khuyen-nghi-mua-voi-gia-muc-tieu-81400-dongco-phieu.htm?languageid=1

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.
