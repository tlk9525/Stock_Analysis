# Báo cáo ngày 2026-08-12 - POW

## Tổng quan

- Dữ liệu: 2018-03-06 -> 2026-08-12, 2,100 phiên.
- Giá đóng cửa: 13.75 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận (điểm -2).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 55.6%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 13.62; SMA60 13.92; RSI14 49.5.
- MACD -0.071; đường tín hiệu -0.111; biểu đồ cột 0.040.
- ATR14 0.37; ATR% 2.7%; ADX14 28.2.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Trung tính - RSI 49.5.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng giảm - ADX 28.2, -DI vượt +DI.
- Thanh khoản: Bình thường - 0.81 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: Điện lực Dầu khí Việt Nam.
- Ngành: Utilities.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 6.55.
- P/B: 1.02.
- ROE: 16.5%.
- ROA: 6.5%.
- Market cap: 42,182.9 tỷ.
- Revenue Growth: 116.1%.
- Profit Growth: 484.1%.
- P/E 6.55: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 1.02: nên đọc cùng ROE và đặc thù ngành.
- ROE 16.5%: hiệu quả vốn chủ sở hữu tốt.
- ROA 6.5%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 1.37: thanh khoản ngắn hạn khá.
- Revenue Growth 116.1% YoY.
- Profit Growth 484.1% YoY.
- CFO/LNST 0.49: dòng tiền chưa theo kịp lợi nhuận, cần đọc thêm biến động vốn lưu động.
- Dòng tiền tự do quý gần nhất dương; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là nợ vay ròng; không dùng một mình để kết luận rủi ro.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.02 (keyword_heuristic_v1).
- Bài mới nhất: 2026-07-31T07:13:42+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-12-21 -> 2026-08-11.
- XGBoost: độ chính xác cân bằng 0.530; AUC 0.586; log-loss 0.672.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.543; AUC 0.551.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 104.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -35.8%; Sharpe -1.41; mức sụt giảm tối đa -43.2%.
- Mức độ quan trọng của đặc trưng: return_1d=10.83; relative_strength_20d=9.17; stoch_k_14=8.97; atr_pct_14=8.83; return_2d=8.60; macd_hist_pct=8.39.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 13.19; mục tiêu 1 15.39; mục tiêu 2 15.39.
- Tỷ lệ lợi nhuận/rủi ro 2.51; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 13.67 (-0.60%).
- P10/P90 cuối kỳ 12.11 / 15.39.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: Technical score -2 < 2.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.3577952299999997, Sharpe=-1.4137404056790535.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 55.6%.
- Mô hình Logistic đối chứng: 51.0%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 47.3%.
- Mức dừng lỗ tham chiếu 13.19, mục tiêu 1 15.39, tỷ lệ lợi nhuận/rủi ro 2.51.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. News Reader đã trích đoạn có nguồn của 3 bài để phân loại chủ đề (ket_qua_kinh_doanh: 3, co_tuc_va_hanh_dong_doanh_nghiep: 3, vi_mo: 3, nganh: 3), nhưng các trích đoạn này không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Suy yếu / cẩn thận; điểm -2. Chi tiết artifact: Xu hướng: Cẩn thận (Giá nằm dưới SMA60.); MACD: Tích cực (MACD trên signal, histogram dương.); RSI14: Trung tính (RSI 49.5.); Bollinger: Ổn định (Giá nằm trong dải Bollinger.); ADX: Xu hướng giảm (ADX 28.2, -DI vượt +DI.); Thanh khoản: Bình thường (0.81 lần trung bình.); Stochastic: Yếu lại (%K nằm dưới %D.)
- Góc nhìn cơ bản: Artifact cơ bản: Điện lực Dầu khí Việt Nam; kỳ 2026-Q2; P/E 6.55; P/B 1.02; ROE 16.5%; ROA 6.5%; Debt/Equity 1.38; Revenue Growth 116.1%; Profit Growth 484.1%.
- Tin doanh nghiệp: Đã đọc trích đoạn giới hạn của 3 bài; phân nhóm rule-based: ket_qua_kinh_doanh: 3, co_tuc_va_hanh_dong_doanh_nghiep: 3, vi_mo: 3, nganh: 3. Tác động cần kiểm chứng: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường. Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động. Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh. So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp. Đây không phải sentiment hay dự báo tác động giá.
- Live research: Live snapshot lấy lúc 2026-08-12T15:31:43.682920+00:00; News Reader đọc được 3 bài. ML có 2 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest.

### Bằng chứng

- ML decision artifact: NO_EDGE. Technical score -2 < 2
- ML decision artifact: NO_EDGE. Lợi thế OOS ròng không đạt: return=-0.3577952299999997, Sharpe=-1.4137404056790535
- News Reader [bnews.vn]: Chứng khoán hôm nay: Khuyến nghị mua DMX, POW và chờ mua VCB - bnews.vn | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh (2026-08-07T01:19:00+00:00)
- News Reader [nguoiquansat.vn]: Cổ phiếu đáng chú ý ngày 7/8: DMX, POW, VCB - nguoiquansat.vn | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh (2026-08-06T16:40:01+00:00)
- News Reader [index.vn]: Cổ phiếu 7/8: DMX được kỳ vọng sinh lời 22%, POW gần 37% - index.vn | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh (2026-08-07T01:27:00+00:00)

### Rủi ro cần kiểm chứng

- ML guard: Technical score -2 < 2
- ML guard: Lợi thế OOS ròng không đạt: return=-0.3577952299999997, Sharpe=-1.4137404056790535
- News Reader: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường.
- News Reader: Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động.
- News Reader: Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh.
- News Reader: So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp.
- Chỉ lưu trích đoạn giới hạn để kiểm chứng nguồn; không lưu hay hiển thị toàn văn bài báo.
- Phân nhóm là keyword rule-based để định tuyến research, không phải sentiment hay dự báo tác động giá.
- Dữ liệu News Reader chỉ phục vụ research/report; không dùng làm feature train/backtest khi chưa có lịch sử available_at point-in-time.
- Tin live/trích đoạn cần mở URL gốc để kiểm chứng bối cảnh, số liệu và thời điểm trước khi sử dụng.

### Nguồn live research

- [bnews.vn] Chứng khoán hôm nay: Khuyến nghị mua DMX, POW và chờ mua VCB - bnews.vn (2026-08-07T01:19:00+00:00): https://bnews.vn/chung-khoan-hom-nay-khuyen-nghi-mua-dmx-pow-va-cho-mua-vcb/431720.html
- [nguoiquansat.vn] Cổ phiếu đáng chú ý ngày 7/8: DMX, POW, VCB - nguoiquansat.vn (2026-08-06T16:40:01+00:00): https://nguoiquansat.vn/co-phieu-dang-chu-y-ngay-7-8-dmx-pow-vcb-308947.html
- [index.vn] Cổ phiếu 7/8: DMX được kỳ vọng sinh lời 22%, POW gần 37% - index.vn (2026-08-07T01:27:00+00:00): https://index.vn/tin-tuc/co-phieu-7-8-dmx-duoc-ky-vong-sinh-loi-22-pow-gan-37

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.

---

## News model riêng từng mã

- Symbol-news report: `/Users/tranlekhoa/Documents/DATA_SCI/vn_stock_analysis/reports/POW/2026-08-12_22-31-54_news_model`
- Số bài tin trong CSV cho mã: 9
- Số dòng giá có news feature: 9
- XGBoost probability mới nhất: 0.522
- AUC OOS: 0.582
- Balanced accuracy OOS: 0.534
- Backtest total return: -0.355

Lưu ý: news model dùng dữ liệu `available_at` point-in-time trong CSV tích lũy; nếu lịch sử tin còn mỏng thì chỉ xem là research/smoke test.
