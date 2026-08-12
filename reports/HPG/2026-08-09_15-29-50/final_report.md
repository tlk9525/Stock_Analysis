# Báo cáo ngày 2026-08-09 - HPG

## Tổng quan

- Dữ liệu: 2008-03-10 -> 2026-08-07, 4,590 phiên.
- Giá đóng cửa: 22.00 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Trung tính (điểm -1).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 52.7%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 21.61; SMA60 22.98; RSI14 49.1.
- MACD -0.230; đường tín hiệu -0.399; biểu đồ cột 0.169.
- ATR14 0.57; ATR% 2.6%; ADX14 36.1.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Trung tính - RSI 49.1.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng giảm - ADX 36.1, -DI vượt +DI.
- Thanh khoản: Thấp - 0.47 lần trung bình.
- Stochastic: Hồi phục - %K nằm trên %D.

## Phân tích cơ bản

- Doanh nghiệp: Hòa Phát.
- Ngành: Basic Resources.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 8.00.
- P/B: 1.32.
- ROE: 17.4%.
- ROA: 8.9%.
- Market cap: 185,745.2 tỷ.
- Revenue Growth: 53.6%.
- Profit Growth: 49.7%.
- P/E 8.00: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 1.32: nên đọc cùng ROE và đặc thù ngành.
- ROE 17.4%: hiệu quả vốn chủ sở hữu tốt.
- ROA 8.9%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 1.14: thanh khoản ngắn hạn khá.
- Revenue Growth 53.6% YoY.
- Profit Growth 49.7% YoY.
- CFO/LNST 0.82: chất lượng chuyển đổi lợi nhuận sang tiền mặt khá tốt.
- Dòng tiền tự do quý gần nhất âm; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là nợ vay ròng; không dùng một mình để kết luận rủi ro.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.26 (keyword_heuristic_v1).
- Bài mới nhất: 2026-07-30T07:51:50+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-08-24 -> 2026-08-06.
- XGBoost: độ chính xác cân bằng 0.520; AUC 0.588; log-loss 0.675.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.516; AUC 0.567.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 119.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -29.9%; Sharpe -1.42; mức sụt giảm tối đa -37.0%.
- Mức độ quan trọng của đặc trưng: adx_14=9.91; bb_position_20=9.83; macd_pct=9.52; market_return_1d=9.35; macd_hist_pct=9.20; relative_strength_20d=9.09.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 21.15; mục tiêu 1 23.91; mục tiêu 2 23.91.
- Tỷ lệ lợi nhuận/rủi ro 1.87; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 21.77 (-1.03%).
- P10/P90 cuối kỳ 19.98 / 23.91.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.520 < 0.520.
- Điều kiện phát hành tín hiệu: Probability 52.7% < 55.0%.
- Điều kiện phát hành tín hiệu: Technical score -1 < 2.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.29859459999999893, Sharpe=-1.4159739939095883.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Trung tính.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 52.7%.
- Mô hình Logistic đối chứng: 47.6%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 44.1%.
- Mức dừng lỗ tham chiếu 21.15, mục tiêu 1 23.91, tỷ lệ lợi nhuận/rủi ro 1.87.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. News Reader đã trích đoạn có nguồn của 5 bài để phân loại chủ đề (ket_qua_kinh_doanh: 4, co_tuc_va_hanh_dong_doanh_nghiep: 4, vi_mo: 4, nganh: 4, rui_ro: 2), nhưng các trích đoạn này không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Trung tính; điểm -1. Chi tiết artifact: Xu hướng: Cẩn thận (Giá nằm dưới SMA60.); MACD: Tích cực (MACD trên signal, histogram dương.); RSI14: Trung tính (RSI 49.1.); Bollinger: Ổn định (Giá nằm trong dải Bollinger.); ADX: Xu hướng giảm (ADX 36.1, -DI vượt +DI.); Thanh khoản: Thấp (0.47 lần trung bình.); Stochastic: Hồi phục (%K nằm trên %D.)
- Góc nhìn cơ bản: Artifact cơ bản: Hòa Phát; kỳ 2026-Q2; P/E 8.00; P/B 1.32; ROE 17.4%; ROA 8.9%; Debt/Equity 0.97; Revenue Growth 53.6%; Profit Growth 49.7%.
- Tin doanh nghiệp: Đã đọc trích đoạn giới hạn của 5 bài; phân nhóm rule-based: ket_qua_kinh_doanh: 4, co_tuc_va_hanh_dong_doanh_nghiep: 4, vi_mo: 4, nganh: 4, rui_ro: 2. Tác động cần kiểm chứng: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường. Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động. Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh. So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp. Xác minh công bố chính thức, phạm vi ảnh hưởng và khả năng định lượng rủi ro. Đây không phải sentiment hay dự báo tác động giá.
- Live research: Live snapshot lấy lúc 2026-08-09T08:30:03.164578+00:00; News Reader đọc được 5 bài. ML có 4 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest.

### Bằng chứng

- ML decision artifact: NO_EDGE. Balanced accuracy 0.520 < 0.520
- ML decision artifact: NO_EDGE. Probability 52.7% < 55.0%
- ML decision artifact: NO_EDGE. Technical score -1 < 2
- ML decision artifact: NO_EDGE. Lợi thế OOS ròng không đạt: return=-0.29859459999999893, Sharpe=-1.4159739939095883
- News Reader [VOV.VN]: Một số cổ phiếu cần quan tâm 5/8: Cơ hội đầu tư tiềm năng với HPG và MBB - VOV.VN | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh (2026-08-04T22:00:00+00:00)
- News Reader [nguoiquansat.vn]: Tiết lộ bất ngờ về lượng sở hữu cổ phiếu HPG của con gái tỷ phú Trần Đình Long - nguoiquansat.vn | nhóm: co_tuc_va_hanh_dong_doanh_nghiep (2026-08-07T04:27:01+00:00)
- News Reader [thuonghieucongluan.com.vn]: Cổ phiếu 5/8: HPG hưởng lợi chu kỳ thép, BMP giữ lợi thế biên lợi nhuận - thuonghieucongluan.com.vn | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh, rui_ro (2026-08-04T23:04:00+00:00)
- News Reader [bnews.vn]: Khuyến nghị mua cổ phiếu SHS, PVT, HPG với giá mục tiêu hấp dẫn - bnews.vn | nhóm: ket_qua_kinh_doanh, vi_mo, nganh (2026-08-05T01:32:00+00:00)
- News Reader [Tin nhanh chứng khoán]: Cổ phiếu cần quan tâm ngày 5/8 - Tin nhanh chứng khoán | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh, rui_ro (2026-08-04T10:22:00+00:00)

### Rủi ro cần kiểm chứng

- ML guard: Balanced accuracy 0.520 < 0.520
- ML guard: Probability 52.7% < 55.0%
- ML guard: Technical score -1 < 2
- ML guard: Lợi thế OOS ròng không đạt: return=-0.29859459999999893, Sharpe=-1.4159739939095883
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

- [VOV.VN] Một số cổ phiếu cần quan tâm 5/8: Cơ hội đầu tư tiềm năng với HPG và MBB - VOV.VN (2026-08-04T22:00:00+00:00): https://vov.vn/thi-truong/mot-so-co-phieu-can-quan-tam-58-co-hoi-dau-tu-tiem-nang-voi-hpg-va-mbb-post1321179.vov
- [nguoiquansat.vn] Tiết lộ bất ngờ về lượng sở hữu cổ phiếu HPG của con gái tỷ phú Trần Đình Long - nguoiquansat.vn (2026-08-07T04:27:01+00:00): https://nguoiquansat.vn/tiet-lo-bat-ngo-ve-luong-so-huu-co-phieu-hpg-cua-con-gai-ty-phu-tran-dinh-long-309030.html
- [thuonghieucongluan.com.vn] Cổ phiếu 5/8: HPG hưởng lợi chu kỳ thép, BMP giữ lợi thế biên lợi nhuận - thuonghieucongluan.com.vn (2026-08-04T23:04:00+00:00): https://thuonghieucongluan.com.vn/co-phieu-5-8-hpg-huong-loi-chu-ky-thep-bmp-giu-loi-the-bien-loi-nhuan-a329226.html
- [bnews.vn] Khuyến nghị mua cổ phiếu SHS, PVT, HPG với giá mục tiêu hấp dẫn - bnews.vn (2026-08-05T01:32:00+00:00): https://bnews.vn/khuyen-nghi-mua-co-phieu-shs-pvt-hpg-voi-gia-muc-tieu-hap-dan/431424.html
- [Tin nhanh chứng khoán] Cổ phiếu cần quan tâm ngày 5/8 - Tin nhanh chứng khoán (2026-08-04T10:22:00+00:00): https://www.tinnhanhchungkhoan.vn/co-phieu-can-quan-tam-ngay-58-post395300.html

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.
