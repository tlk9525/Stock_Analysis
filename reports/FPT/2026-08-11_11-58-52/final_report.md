# Báo cáo ngày 2026-08-11 - FPT

## Tổng quan

- Dữ liệu: 2008-03-10 -> 2026-08-11, 4,592 phiên.
- Giá đóng cửa: 72.10 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Tích cực (điểm 5).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 49.2%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 67.46; SMA60 70.93; RSI14 61.3.
- MACD 0.462; đường tín hiệu -0.424; biểu đồ cột 0.886.
- ATR14 1.93; ATR% 2.7%; ADX14 25.8.
- Xu hướng: Trung tính - Giá trên SMA60 nhưng chưa vượt SMA20.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 61.3.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng tăng - ADX 25.8, +DI vượt -DI.
- Thanh khoản: Thấp - 0.64 lần trung bình.
- Stochastic: Cực trị - %K 89.8, %D 85.3.

## Phân tích cơ bản

- Doanh nghiệp: FPT Corp.
- Ngành: Technology.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 12.24.
- P/B: 3.08.
- ROE: 26.5%.
- ROA: 12.8%.
- Market cap: 123,088.6 tỷ.
- Revenue Growth: -17.1%.
- Profit Growth: 13.7%.
- P/E 12.24: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 3.08: nên đọc cùng ROE và đặc thù ngành.
- ROE 26.5%: hiệu quả vốn chủ sở hữu tốt.
- ROA 12.8%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 1.56: thanh khoản ngắn hạn khá.
- Revenue Growth -17.1% YoY.
- Profit Growth 13.7% YoY.
- CFO/LNST 0.66: dòng tiền chưa theo kịp lợi nhuận, cần đọc thêm biến động vốn lưu động.
- Dòng tiền tự do quý gần nhất dương; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là nợ vay ròng; không dùng một mình để kết luận rủi ro.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.12 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-03T09:13:52+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-08-08 -> 2026-08-10.
- XGBoost: độ chính xác cân bằng 0.510; AUC 0.574; log-loss 0.687.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.527; AUC 0.560.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 27.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -25.8%; Sharpe -0.86; mức sụt giảm tối đa -29.2%.
- Mức độ quan trọng của đặc trưng: return_1d=15.05; close_vs_sma20=13.81; day_of_week=11.91; return_3d=11.64; stoch_k_14=11.60; macd_hist_pct=11.26.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 70.22; mục tiêu 1 80.39; mục tiêu 2 80.39.
- Tỷ lệ lợi nhuận/rủi ro 3.54; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 71.46 (-0.89%).
- P10/P90 cuối kỳ 64.08 / 80.39.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.510 < 0.520.
- Điều kiện phát hành tín hiệu: Probability 49.2% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.2579965400000007, Sharpe=-0.8604090548950347.
- Trung hạn chưa xấu, ngắn hạn yếu vì giá dưới SMA20.
- Xu hướng kỹ thuật nghiêng về: Tích cực.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 49.2%.
- Mô hình Logistic đối chứng: 50.8%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 45.8%.
- Mức dừng lỗ tham chiếu 70.22, mục tiêu 1 80.39, tỷ lệ lợi nhuận/rủi ro 3.54.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. News Reader đã trích đoạn có nguồn của 4 bài để phân loại chủ đề (ket_qua_kinh_doanh: 4, co_tuc_va_hanh_dong_doanh_nghiep: 4, vi_mo: 2, nganh: 2), nhưng các trích đoạn này không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Tích cực; điểm 5. Chi tiết artifact: Xu hướng: Trung tính (Giá trên SMA60 nhưng chưa vượt SMA20.); MACD: Tích cực (MACD trên signal, histogram dương.); RSI14: Tích cực (RSI 61.3.); Bollinger: Ổn định (Giá nằm trong dải Bollinger.); ADX: Xu hướng tăng (ADX 25.8, +DI vượt -DI.); Thanh khoản: Thấp (0.64 lần trung bình.); Stochastic: Cực trị (%K 89.8, %D 85.3.)
- Góc nhìn cơ bản: Artifact cơ bản: FPT Corp; kỳ 2026-Q2; P/E 12.24; P/B 3.08; ROE 26.5%; ROA 12.8%; Debt/Equity 0.80; Revenue Growth -17.1%; Profit Growth 13.7%.
- Tin doanh nghiệp: Đã đọc trích đoạn giới hạn của 4 bài; phân nhóm rule-based: ket_qua_kinh_doanh: 4, co_tuc_va_hanh_dong_doanh_nghiep: 4, vi_mo: 2, nganh: 2. Tác động cần kiểm chứng: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường. Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động. Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh. So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp. Đây không phải sentiment hay dự báo tác động giá.
- Live research: Live snapshot lấy lúc 2026-08-11T04:59:06.599873+00:00; News Reader đọc được 4 bài. ML có 3 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest.

### Bằng chứng

- ML decision artifact: NO_EDGE. Balanced accuracy 0.510 < 0.520
- ML decision artifact: NO_EDGE. Probability 49.2% < 55.0%
- ML decision artifact: NO_EDGE. Lợi thế OOS ròng không đạt: return=-0.2579965400000007, Sharpe=-0.8604090548950347
- News Reader [Chungta]: Cổ phiếu FPT tăng 7 trong 10 phiên gần nhất - Chungta | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep (2026-08-07T07:14:00+00:00)
- News Reader [VOV.VN]: Một số cổ phiếu cần quan tâm 7/8: Cơ hội tiềm năng với FPT và VPB - VOV.VN | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh (2026-08-06T22:00:00+00:00)
- News Reader [Vietstock]: FPT Online sắp trả cổ tức tiền tỷ lệ 100% - Vietstock | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep (2026-08-05T12:47:00+00:00)
- News Reader [Tạp chí Kinh tế - Tài chính Online]: Ba doanh nghiệp trả cổ tức bằng tiền, FPT Online chi 10.000 đồng/cổ phiếu - Tạp chí Kinh tế - Tài chính Online | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh (2026-08-09T13:05:49+00:00)

### Rủi ro cần kiểm chứng

- ML guard: Balanced accuracy 0.510 < 0.520
- ML guard: Probability 49.2% < 55.0%
- ML guard: Lợi thế OOS ròng không đạt: return=-0.2579965400000007, Sharpe=-0.8604090548950347
- News Reader: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường.
- News Reader: Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động.
- News Reader: Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh.
- News Reader: So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp.
- Chỉ lưu trích đoạn giới hạn để kiểm chứng nguồn; không lưu hay hiển thị toàn văn bài báo.
- Phân nhóm là keyword rule-based để định tuyến research, không phải sentiment hay dự báo tác động giá.
- Dữ liệu News Reader chỉ phục vụ research/report; không dùng làm feature train/backtest khi chưa có lịch sử available_at point-in-time.
- Tin live/trích đoạn cần mở URL gốc để kiểm chứng bối cảnh, số liệu và thời điểm trước khi sử dụng.

### Nguồn live research

- [Chungta] Cổ phiếu FPT tăng 7 trong 10 phiên gần nhất - Chungta (2026-08-07T07:14:00+00:00): https://chungta.vn/kinh-doanh/co-phieu-fpt-tang-7-trong-10-phien-gan-nhat-1141876.html
- [VOV.VN] Một số cổ phiếu cần quan tâm 7/8: Cơ hội tiềm năng với FPT và VPB - VOV.VN (2026-08-06T22:00:00+00:00): https://vov.vn/thi-truong/mot-so-co-phieu-can-quan-tam-78-co-hoi-tiem-nang-voi-fpt-va-vpb-post1321824.vov
- [Vietstock] FPT Online sắp trả cổ tức tiền tỷ lệ 100% - Vietstock (2026-08-05T12:47:00+00:00): https://vietstock.vn/2026/08/fpt-online-sap-tra-co-tuc-tien-ty-le-100-738-1477175.htm
- [Tạp chí Kinh tế - Tài chính Online] Ba doanh nghiệp trả cổ tức bằng tiền, FPT Online chi 10.000 đồng/cổ phiếu - Tạp chí Kinh tế - Tài chính Online (2026-08-09T13:05:49+00:00): https://tapchikinhtetaichinh.vn/ba-doanh-nghiep-tra-co-tuc-bang-tien-fpt-online-chi-10-000-dong-co-phieu-164034.html

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.
