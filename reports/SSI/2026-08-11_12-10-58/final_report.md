# Báo cáo ngày 2026-08-11 - SSI

## Tổng quan

- Dữ liệu: 2008-03-10 -> 2026-08-11, 4,592 phiên.
- Giá đóng cửa: 25.20 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận (điểm -2).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 51.1%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 23.86; SMA60 25.94; RSI14 54.4.
- MACD -0.245; đường tín hiệu -0.554; biểu đồ cột 0.309.
- ATR14 0.80; ATR% 3.2%; ADX14 29.5.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Trung tính - RSI 54.4.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng giảm - ADX 29.5, -DI vượt +DI.
- Thanh khoản: Thấp - 0.42 lần trung bình.
- Stochastic: Cực trị - %K 95.9, %D 93.0.

## Phân tích cơ bản

- Doanh nghiệp: Chứng khoán SSI.
- Ngành: Financial Services.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 11.70.
- P/B: 1.55.
- ROE: 13.4%.
- ROA: 5.0%.
- Market cap: 62,777.6 tỷ.
- Revenue Growth: 10.9%.
- Profit Growth: 27.0%.
- P/E 11.70: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 1.55: nên đọc cùng ROE và đặc thù ngành.
- ROA 5.0%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 1.65: thanh khoản ngắn hạn khá.
- Revenue Growth 10.9% YoY.
- Profit Growth 27.0% YoY.
- CFO/LNST -2.27: dòng tiền chưa theo kịp lợi nhuận, cần đọc thêm biến động vốn lưu động.
- Dòng tiền tự do quý gần nhất âm; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là nợ vay ròng; không dùng một mình để kết luận rủi ro.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.10 (keyword_heuristic_v1).
- Bài mới nhất: 2026-07-31T08:59:45+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-08-24 -> 2026-08-10.
- XGBoost: độ chính xác cân bằng 0.500; AUC 0.544; log-loss 0.687.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.542; AUC 0.551.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 19.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -1.0%; Sharpe -0.03; mức sụt giảm tối đa -8.2%.
- Mức độ quan trọng của đặc trưng: stoch_k_14=15.56; beta_60d=13.61; relative_strength_20d=13.52; volume_z_20=13.50; return_1d=12.61; market_return_1d=12.09.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 24.00; mục tiêu 1 28.27; mục tiêu 2 28.27.
- Tỷ lệ lợi nhuận/rủi ro 2.22; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 24.95 (-0.98%).
- P10/P90 cuối kỳ 22.09 / 28.27.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.500 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5439867314664816, AUC logistic=0.5512072822649078.
- Điều kiện phát hành tín hiệu: Probability 51.1% < 55.0%.
- Điều kiện phát hành tín hiệu: Technical score -2 < 2.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.009731229999999313, Sharpe=-0.030003067262322575.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 51.1%.
- Mô hình Logistic đối chứng: 58.0%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 46.0%.
- Mức dừng lỗ tham chiếu 24.00, mục tiêu 1 28.27, tỷ lệ lợi nhuận/rủi ro 2.22.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. News Reader đã trích đoạn có nguồn của 3 bài để phân loại chủ đề (ket_qua_kinh_doanh: 3, co_tuc_va_hanh_dong_doanh_nghiep: 3, vi_mo: 3, nganh: 2, rui_ro: 2), nhưng các trích đoạn này không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Suy yếu / cẩn thận; điểm -2. Chi tiết artifact: Xu hướng: Cẩn thận (Giá nằm dưới SMA60.); MACD: Tích cực (MACD trên signal, histogram dương.); RSI14: Trung tính (RSI 54.4.); Bollinger: Ổn định (Giá nằm trong dải Bollinger.); ADX: Xu hướng giảm (ADX 29.5, -DI vượt +DI.); Thanh khoản: Thấp (0.42 lần trung bình.); Stochastic: Cực trị (%K 95.9, %D 93.0.)
- Góc nhìn cơ bản: Artifact cơ bản: Chứng khoán SSI; kỳ 2026-Q2; P/E 11.70; P/B 1.55; ROE 13.4%; ROA 5.0%; Debt/Equity 1.37; Revenue Growth 10.9%; Profit Growth 27.0%.
- Tin doanh nghiệp: Đã đọc trích đoạn giới hạn của 3 bài; phân nhóm rule-based: ket_qua_kinh_doanh: 3, co_tuc_va_hanh_dong_doanh_nghiep: 3, vi_mo: 3, nganh: 2, rui_ro: 2. Tác động cần kiểm chứng: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường. Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động. Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh. So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp. Xác minh công bố chính thức, phạm vi ảnh hưởng và khả năng định lượng rủi ro. Đây không phải sentiment hay dự báo tác động giá.
- Live research: Live snapshot lấy lúc 2026-08-11T05:11:11.940177+00:00; News Reader đọc được 3 bài. ML có 5 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest.

### Bằng chứng

- ML decision artifact: NO_EDGE. Balanced accuracy 0.500 < 0.520
- ML decision artifact: NO_EDGE. XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5439867314664816, AUC logistic=0.5512072822649078
- ML decision artifact: NO_EDGE. Probability 51.1% < 55.0%
- ML decision artifact: NO_EDGE. Technical score -2 < 2
- ML decision artifact: NO_EDGE. Lợi thế OOS ròng không đạt: return=-0.009731229999999313, Sharpe=-0.030003067262322575
- News Reader [Tin nhanh chứng khoán]: SSI: Ngày GDKHQ trả cổ tức năm 2025 bằng tiền (10%), cổ phiếu thưởng (5:1) - Tin nhanh chứng khoán | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo (2026-08-10T05:38:49+00:00)
- News Reader [Tạp chí Kinh tế - Tài chính Online]: Điểm danh những mã cổ phiếu đáng chú ý trong tháng 8 - Tạp chí Kinh tế - Tài chính Online | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh, rui_ro (2026-08-07T03:01:54+00:00)
- News Reader [VnEconomy]: Dự báo 9 cổ phiếu mới nhất được thêm vào rổ FTSE GEIS, 5 cổ phiếu khác bị loại - VnEconomy | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh, rui_ro (2026-08-07T02:17:45+00:00)

### Rủi ro cần kiểm chứng

- ML guard: Balanced accuracy 0.500 < 0.520
- ML guard: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5439867314664816, AUC logistic=0.5512072822649078
- ML guard: Probability 51.1% < 55.0%
- ML guard: Technical score -2 < 2
- ML guard: Lợi thế OOS ròng không đạt: return=-0.009731229999999313, Sharpe=-0.030003067262322575
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

- [Tin nhanh chứng khoán] SSI: Ngày GDKHQ trả cổ tức năm 2025 bằng tiền (10%), cổ phiếu thưởng (5:1) - Tin nhanh chứng khoán (2026-08-10T05:38:49+00:00): https://www.tinnhanhchungkhoan.vn/ssi-ngay-gdkhq-tra-co-tuc-nam-2025-bang-tien-10-co-phieu-thuong-51-post395640.html
- [Tạp chí Kinh tế - Tài chính Online] Điểm danh những mã cổ phiếu đáng chú ý trong tháng 8 - Tạp chí Kinh tế - Tài chính Online (2026-08-07T03:01:54+00:00): https://tapchikinhtetaichinh.vn/nhung-ma-co-phieu-dang-chu-y-trong-thang-8-163869.html
- [VnEconomy] Dự báo 9 cổ phiếu mới nhất được thêm vào rổ FTSE GEIS, 5 cổ phiếu khác bị loại - VnEconomy (2026-08-07T02:17:45+00:00): https://vneconomy.vn/du-bao-9-co-phieu-moi-nhat-duoc-them-vao-ro-ftse-geis-5-co-phieu-khac-bi-loai.htm

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.
