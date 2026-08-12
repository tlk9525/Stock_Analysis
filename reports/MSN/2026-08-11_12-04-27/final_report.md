# Báo cáo ngày 2026-08-11 - MSN

## Tổng quan

- Dữ liệu: 2009-11-05 -> 2026-08-11, 4,180 phiên.
- Giá đóng cửa: 67.80 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng (điểm 3).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 49.9%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 66.43; SMA60 70.45; RSI14 50.4.
- MACD -0.508; đường tín hiệu -0.948; biểu đồ cột 0.440.
- ATR14 1.63; ATR% 2.4%; ADX14 31.1.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Trung tính - RSI 50.4.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng tăng - ADX 31.1, +DI vượt -DI.
- Thanh khoản: Thấp - 0.31 lần trung bình.
- Stochastic: Hồi phục - %K nằm trên %D.

## Phân tích cơ bản

- Doanh nghiệp: Tập đoàn Masan.
- Ngành: Food & Beverage.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 14.60.
- P/B: 2.46.
- ROE: 19.4%.
- ROA: 5.4%.
- Market cap: 98,867.4 tỷ.
- Revenue Growth: 53.5%.
- Profit Growth: 202.8%.
- P/E 14.60: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 2.46: nên đọc cùng ROE và đặc thù ngành.
- ROE 19.4%: hiệu quả vốn chủ sở hữu tốt.
- ROA 5.4%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 0.87: thanh khoản ngắn hạn cần theo dõi.
- Revenue Growth 53.5% YoY.
- Profit Growth 202.8% YoY.
- CFO/LNST -0.08: dòng tiền chưa theo kịp lợi nhuận, cần đọc thêm biến động vốn lưu động.
- Dòng tiền tự do quý gần nhất âm; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là nợ vay ròng; không dùng một mình để kết luận rủi ro.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.18 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-07T08:59:53+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-12-25 -> 2026-08-10.
- XGBoost: độ chính xác cân bằng 0.498; AUC 0.495; log-loss 0.692.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.499; AUC 0.513.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 13.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -15.4%; Sharpe -1.32; mức sụt giảm tối đa -18.3%.
- Mức độ quan trọng của đặc trưng: atr_pct_14=16.16; relative_strength_20d=15.86; close_vs_sma20=15.80; return_kurtosis_20d=13.42; volume_ratio_20=12.95; range_pct=12.56.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 65.36; mục tiêu 1 74.29; mục tiêu 2 74.29.
- Tỷ lệ lợi nhuận/rủi ro 2.21; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 67.30 (-0.74%).
- P10/P90 cuối kỳ 61.02 / 74.29.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.495 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.498 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.4945523495141816, AUC logistic=0.5125998408441157.
- Điều kiện phát hành tín hiệu: Probability 49.9% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.15437910000000032, Sharpe=-1.3238452789079527.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 49.9%.
- Mô hình Logistic đối chứng: 47.3%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 46.0%.
- Mức dừng lỗ tham chiếu 65.36, mục tiêu 1 74.29, tỷ lệ lợi nhuận/rủi ro 2.21.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. News Reader đã trích đoạn có nguồn của 4 bài để phân loại chủ đề (ket_qua_kinh_doanh: 1, vi_mo: 1, nganh: 1), nhưng các trích đoạn này không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Hồi phục / nghiêng tăng; điểm 3. Chi tiết artifact: Xu hướng: Cẩn thận (Giá nằm dưới SMA60.); MACD: Tích cực (MACD trên signal, histogram dương.); RSI14: Trung tính (RSI 50.4.); Bollinger: Ổn định (Giá nằm trong dải Bollinger.); ADX: Xu hướng tăng (ADX 31.1, +DI vượt -DI.); Thanh khoản: Thấp (0.31 lần trung bình.); Stochastic: Hồi phục (%K nằm trên %D.)
- Góc nhìn cơ bản: Artifact cơ bản: Tập đoàn Masan; kỳ 2026-Q2; P/E 14.60; P/B 2.46; ROE 19.4%; ROA 5.4%; Debt/Equity 1.88; Revenue Growth 53.5%; Profit Growth 202.8%.
- Tin doanh nghiệp: Đã đọc trích đoạn giới hạn của 4 bài; phân nhóm rule-based: ket_qua_kinh_doanh: 1, vi_mo: 1, nganh: 1. Tác động cần kiểm chứng: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường. Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh. So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp. Đây không phải sentiment hay dự báo tác động giá.
- Live research: Live snapshot lấy lúc 2026-08-11T05:04:41.896407+00:00; News Reader đọc được 4 bài. ML có 5 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest.

### Bằng chứng

- ML decision artifact: NO_EDGE. AUC 0.495 < 0.540
- ML decision artifact: NO_EDGE. Balanced accuracy 0.498 < 0.520
- ML decision artifact: NO_EDGE. XGBoost chưa vượt logistic baseline: AUC XGBoost=0.4945523495141816, AUC logistic=0.5125998408441157
- ML decision artifact: NO_EDGE. Probability 49.9% < 55.0%
- ML decision artifact: NO_EDGE. Lợi thế OOS ròng không đạt: return=-0.15437910000000032, Sharpe=-1.3238452789079527
- News Reader [Fili.vn]: Ngày 11/08/2026: 10 cổ phiếu nóng dưới góc nhìn PTKT của Vietstock - Fili.vn | nhóm: khác (2026-08-11T01:58:00+00:00)
- News Reader [nguoiquansat.vn]: Cổ phiếu đáng chú ý ngày 10/8: MSN, MWG, FPT - nguoiquansat.vn | nhóm: ket_qua_kinh_doanh, vi_mo, nganh (2026-08-09T14:51:01+00:00)
- News Reader [Fili.vn]: Tuần 10-14/08/2026: 10 cổ phiếu nóng dưới góc nhìn PTKT của Vietstock - Fili.vn | nhóm: khác (2026-08-10T01:57:45+00:00)
- News Reader [Fili.vn]: Ngày 06/08/2026: 10 cổ phiếu nóng dưới góc nhìn PTKT của Vietstock - Fili.vn | nhóm: khác (2026-08-06T02:00:48+00:00)

### Rủi ro cần kiểm chứng

- ML guard: AUC 0.495 < 0.540
- ML guard: Balanced accuracy 0.498 < 0.520
- ML guard: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.4945523495141816, AUC logistic=0.5125998408441157
- ML guard: Probability 49.9% < 55.0%
- ML guard: Lợi thế OOS ròng không đạt: return=-0.15437910000000032, Sharpe=-1.3238452789079527
- News Reader: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường.
- News Reader: Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh.
- News Reader: So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp.
- Chỉ lưu trích đoạn giới hạn để kiểm chứng nguồn; không lưu hay hiển thị toàn văn bài báo.
- Phân nhóm là keyword rule-based để định tuyến research, không phải sentiment hay dự báo tác động giá.
- Dữ liệu News Reader chỉ phục vụ research/report; không dùng làm feature train/backtest khi chưa có lịch sử available_at point-in-time.
- Tin live/trích đoạn cần mở URL gốc để kiểm chứng bối cảnh, số liệu và thời điểm trước khi sử dụng.

### Nguồn live research

- [Fili.vn] Ngày 11/08/2026: 10 cổ phiếu nóng dưới góc nhìn PTKT của Vietstock - Fili.vn (2026-08-11T01:58:00+00:00): https://fili.vn/2026/08/ngay-11082026-10-co-phieu-nong-duoi-goc-nhin-ptkt-cua-vietstock-585-1478860.htm
- [nguoiquansat.vn] Cổ phiếu đáng chú ý ngày 10/8: MSN, MWG, FPT - nguoiquansat.vn (2026-08-09T14:51:01+00:00): https://nguoiquansat.vn/co-phieu-dang-chu-y-ngay-10-8-msn-mwg-fpt-309471.html
- [Fili.vn] Tuần 10-14/08/2026: 10 cổ phiếu nóng dưới góc nhìn PTKT của Vietstock - Fili.vn (2026-08-10T01:57:45+00:00): https://fili.vn/2026/08/tuan-10-14082026-10-co-phieu-nong-duoi-goc-nhin-ptkt-cua-vietstock-585-1478344.htm
- [Fili.vn] Ngày 06/08/2026: 10 cổ phiếu nóng dưới góc nhìn PTKT của Vietstock - Fili.vn (2026-08-06T02:00:48+00:00): https://fili.vn/2026/08/ngay-06082026-10-co-phieu-nong-duoi-goc-nhin-ptkt-cua-vietstock-585-1477037.htm

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.
