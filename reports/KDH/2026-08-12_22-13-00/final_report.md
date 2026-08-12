# Báo cáo ngày 2026-08-12 - KDH

## Tổng quan

- Dữ liệu: 2010-02-01 -> 2026-08-12, 4,119 phiên.
- Giá đóng cửa: 18.15 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận (điểm -3).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 48.7%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 17.81; SMA60 20.72; RSI14 42.5.
- MACD -0.600; đường tín hiệu -0.844; biểu đồ cột 0.245.
- ATR14 0.58; ATR% 3.2%; ADX14 41.1.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Yếu - RSI 42.5.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng giảm - ADX 41.1, -DI vượt +DI.
- Thanh khoản: Bình thường - 0.91 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: Nhà Khang Điền.
- Ngành: Real Estate.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 11.63.
- P/B: 1.10.
- ROE: 9.5%.
- ROA: 4.8%.
- Market cap: 20,424.3 tỷ.
- Revenue Growth: -84.7%.
- Profit Growth: 276.7%.
- P/E 11.63: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 1.10: nên đọc cùng ROE và đặc thù ngành.
- ROA 4.8%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 10.06: thanh khoản ngắn hạn khá.
- Revenue Growth -84.7% YoY.
- Profit Growth 276.7% YoY.
- CFO/LNST -1.10: dòng tiền chưa theo kịp lợi nhuận, cần đọc thêm biến động vốn lưu động.
- Dòng tiền tự do quý gần nhất âm; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là nợ vay ròng; không dùng một mình để kết luận rủi ro.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.04 (keyword_heuristic_v1).
- Bài mới nhất: 2026-07-31T07:54:28+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-08-23 -> 2026-08-11.
- XGBoost: độ chính xác cân bằng 0.499; AUC 0.493; log-loss 0.695.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.499; AUC 0.495.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 8.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận 2.5%; Sharpe 0.16; mức sụt giảm tối đa -8.8%.
- Mức độ quan trọng của đặc trưng: return_1d=14.81; return_5d=12.24; return_3d=11.30; adx_14=10.21; return_2d=9.92; return_skew_20d=9.63.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 17.29; mục tiêu 1 20.29; mục tiêu 2 20.29.
- Tỷ lệ lợi nhuận/rủi ro 2.15; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 17.79 (-1.97%).
- P10/P90 cuối kỳ 15.89 / 20.29.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.493 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.499 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.4926427575034874, AUC logistic=0.4954251601193958.
- Điều kiện phát hành tín hiệu: Probability 48.7% < 55.0%.
- Điều kiện phát hành tín hiệu: Technical score -3 < 2.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 48.7%.
- Mô hình Logistic đối chứng: 47.5%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 41.8%.
- Mức dừng lỗ tham chiếu 17.29, mục tiêu 1 20.29, tỷ lệ lợi nhuận/rủi ro 2.15.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. News Reader đã trích đoạn có nguồn của 3 bài để phân loại chủ đề (ket_qua_kinh_doanh: 2, co_tuc_va_hanh_dong_doanh_nghiep: 3, vi_mo: 2, nganh: 2, rui_ro: 2), nhưng các trích đoạn này không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Suy yếu / cẩn thận; điểm -3. Chi tiết artifact: Xu hướng: Cẩn thận (Giá nằm dưới SMA60.); MACD: Tích cực (MACD trên signal, histogram dương.); RSI14: Yếu (RSI 42.5.); Bollinger: Ổn định (Giá nằm trong dải Bollinger.); ADX: Xu hướng giảm (ADX 41.1, -DI vượt +DI.); Thanh khoản: Bình thường (0.91 lần trung bình.); Stochastic: Yếu lại (%K nằm dưới %D.)
- Góc nhìn cơ bản: Artifact cơ bản: Nhà Khang Điền; kỳ 2026-Q2; P/E 11.63; P/B 1.10; ROE 9.5%; ROA 4.8%; Debt/Equity 0.98; Revenue Growth -84.7%; Profit Growth 276.7%.
- Tin doanh nghiệp: Đã đọc trích đoạn giới hạn của 3 bài; phân nhóm rule-based: ket_qua_kinh_doanh: 2, co_tuc_va_hanh_dong_doanh_nghiep: 3, vi_mo: 2, nganh: 2, rui_ro: 2. Tác động cần kiểm chứng: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường. Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động. Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh. So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp. Xác minh công bố chính thức, phạm vi ảnh hưởng và khả năng định lượng rủi ro. Đây không phải sentiment hay dự báo tác động giá.
- Live research: Live snapshot lấy lúc 2026-08-12T15:13:18.000340+00:00; News Reader đọc được 3 bài. ML có 5 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest.

### Bằng chứng

- ML decision artifact: NO_EDGE. AUC 0.493 < 0.540
- ML decision artifact: NO_EDGE. Balanced accuracy 0.499 < 0.520
- ML decision artifact: NO_EDGE. XGBoost chưa vượt logistic baseline: AUC XGBoost=0.4926427575034874, AUC logistic=0.4954251601193958
- ML decision artifact: NO_EDGE. Probability 48.7% < 55.0%
- ML decision artifact: NO_EDGE. Technical score -3 < 2
- News Reader [VietstockFinance]: KDH: Khuyến nghị THEO DÕI với giá mục tiêu 19,600 đồng/cổ phiếu - VietstockFinance | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh (2026-08-05T22:16:57+00:00)
- News Reader [nhadautu.vn]: Trước thềm nâng hạng: 4 'ẩn số' BSR, DGC, GEE và KDH - nhadautu.vn | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh, rui_ro (2026-08-06T07:26:01+00:00)
- News Reader [Cộng đồng Kinh doanh Việt Nam]: Khang Điền (KDH) đầu tư dự án khu Mả Lạng và Chợ Gà - Gạo theo phương thức PPP (BT) - Cộng đồng Kinh doanh Việt Nam | nhóm: co_tuc_va_hanh_dong_doanh_nghiep, rui_ro (2026-08-10T05:01:49+00:00)

### Rủi ro cần kiểm chứng

- ML guard: AUC 0.493 < 0.540
- ML guard: Balanced accuracy 0.499 < 0.520
- ML guard: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.4926427575034874, AUC logistic=0.4954251601193958
- ML guard: Probability 48.7% < 55.0%
- ML guard: Technical score -3 < 2
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

- [VietstockFinance] KDH: Khuyến nghị THEO DÕI với giá mục tiêu 19,600 đồng/cổ phiếu - VietstockFinance (2026-08-05T22:16:57+00:00): https://finance.vietstock.vn/bao-cao-phan-tich/21344/kdh-khuyen-nghi-theo-doi-voi-gia-muc-tieu-19600-dongco-phieu.htm?languageid=1
- [nhadautu.vn] Trước thềm nâng hạng: 4 'ẩn số' BSR, DGC, GEE và KDH - nhadautu.vn (2026-08-06T07:26:01+00:00): https://nhadautu.vn/truoc-them-nang-hang-4-an-so-bsr-dgc-gee-va-kdh-d106811.html
- [Cộng đồng Kinh doanh Việt Nam] Khang Điền (KDH) đầu tư dự án khu Mả Lạng và Chợ Gà - Gạo theo phương thức PPP (BT) - Cộng đồng Kinh doanh Việt Nam (2026-08-10T05:01:49+00:00): https://vietnambusinessinsider.vn/khang-dien-kdh-dau-tu-du-an-khu-ma-lang-va-cho-ga-gao-theo-phuong-thuc-ppp-bt-a54873.html

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.
