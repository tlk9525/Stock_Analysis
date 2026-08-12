# Báo cáo ngày 2026-08-11 - TCB

## Tổng quan

- Dữ liệu: 2018-06-04 -> 2026-08-11, 2,047 phiên.
- Giá đóng cửa: 31.25 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng (điểm 3).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 51.0%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 29.78; SMA60 31.51; RSI14 56.2.
- MACD -0.357; đường tín hiệu -0.665; biểu đồ cột 0.309.
- ATR14 0.85; ATR% 2.7%; ADX14 29.4.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 56.2.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng tăng - ADX 29.4, +DI vượt -DI.
- Thanh khoản: Thấp - 0.48 lần trung bình.
- Stochastic: Cực trị - %K 92.0, %D 89.3.

## Phân tích cơ bản

- Doanh nghiệp: Techcombank.
- Ngành: Banks.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 8.19.
- P/B: 1.24.
- ROE: 14.8%.
- ROA: 2.3%.
- Market cap: 222,153.6 tỷ.
- Revenue Growth: 17.3%.
- Profit Growth: 17.7%.
- P/E 8.19: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 1.24: nên đọc cùng ROE và đặc thù ngành.
- ROA 2.3%: khá tốt, đặc biệt với nhóm ngân hàng.
- Debt/Equity 5.74: đòn bẩy cao, cần đọc theo ngành.
- NPL 1.1%: đang ở mức kiểm soát.
- Revenue Growth 17.3% YoY.
- Profit Growth 17.7% YoY.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.18 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-07T08:42:05+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-09-08 -> 2026-08-10.
- XGBoost: độ chính xác cân bằng 0.486; AUC 0.497; log-loss 0.695.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.495; AUC 0.501.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 15.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -27.1%; Sharpe -1.65; mức sụt giảm tối đa -27.7%.
- Mức độ quan trọng của đặc trưng: volatility_20d=14.89; bb_position_20=11.12; relative_strength_20d=10.37; close_vs_sma60=9.90; return_3d=9.77; return_2d=9.74.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 31.19; mục tiêu 1 32.20; mục tiêu 2 34.73.
- Tỷ lệ lợi nhuận/rủi ro 3.72; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 31.14 (-0.34%).
- P10/P90 cuối kỳ 27.76 / 34.73.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.497 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.486 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.49738268188631385, AUC logistic=0.5009108728237057.
- Điều kiện phát hành tín hiệu: Probability 51.0% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.2705657999999995, Sharpe=-1.6469342728240042.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 51.0%.
- Mô hình Logistic đối chứng: 52.9%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 48.4%.
- Mức dừng lỗ tham chiếu 31.19, mục tiêu 1 32.20, tỷ lệ lợi nhuận/rủi ro 3.72.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. News Reader đã trích đoạn có nguồn của 4 bài để phân loại chủ đề (ket_qua_kinh_doanh: 3, co_tuc_va_hanh_dong_doanh_nghiep: 1, vi_mo: 1, nganh: 4, rui_ro: 2), nhưng các trích đoạn này không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Hồi phục / nghiêng tăng; điểm 3. Chi tiết artifact: Xu hướng: Cẩn thận (Giá nằm dưới SMA60.); MACD: Tích cực (MACD trên signal, histogram dương.); RSI14: Tích cực (RSI 56.2.); Bollinger: Ổn định (Giá nằm trong dải Bollinger.); ADX: Xu hướng tăng (ADX 29.4, +DI vượt -DI.); Thanh khoản: Thấp (0.48 lần trung bình.); Stochastic: Cực trị (%K 92.0, %D 89.3.)
- Góc nhìn cơ bản: Artifact cơ bản: Techcombank; kỳ 2026-Q2; P/E 8.19; P/B 1.24; ROE 14.8%; ROA 2.3%; Debt/Equity 5.74; Revenue Growth 17.3%; Profit Growth 17.7%.
- Tin doanh nghiệp: Đã đọc trích đoạn giới hạn của 4 bài; phân nhóm rule-based: ket_qua_kinh_doanh: 3, co_tuc_va_hanh_dong_doanh_nghiep: 1, vi_mo: 1, nganh: 4, rui_ro: 2. Tác động cần kiểm chứng: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường. Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động. Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh. So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp. Xác minh công bố chính thức, phạm vi ảnh hưởng và khả năng định lượng rủi ro. Đây không phải sentiment hay dự báo tác động giá.
- Live research: Live snapshot lấy lúc 2026-08-11T05:12:47.568599+00:00; News Reader đọc được 4 bài. ML có 5 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest.

### Bằng chứng

- ML decision artifact: NO_EDGE. AUC 0.497 < 0.540
- ML decision artifact: NO_EDGE. Balanced accuracy 0.486 < 0.520
- ML decision artifact: NO_EDGE. XGBoost chưa vượt logistic baseline: AUC XGBoost=0.49738268188631385, AUC logistic=0.5009108728237057
- ML decision artifact: NO_EDGE. Probability 51.0% < 55.0%
- ML decision artifact: NO_EDGE. Lợi thế OOS ròng không đạt: return=-0.2705657999999995, Sharpe=-1.6469342728240042
- News Reader [Tuổi Trẻ]: Tự doanh chứng khoán mua ròng hàng trăm tỉ đồng, cổ phiếu TCB áp sát kỷ lục lịch sử - Tuổi Trẻ | nhóm: nganh (2026-08-10T12:16:00+00:00)
- News Reader [VietnamFinance]: TCB cùng nhóm cổ phiếu doanh nghiệp Nhà nước 'kéo' VN-Index tăng gần 9 điểm - VietnamFinance | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, nganh, rui_ro (2026-08-10T09:22:36+00:00)
- News Reader [nguoiquansat.vn]: Cổ phiếu đáng chú ý ngày 11/8: TCB, GAS, VGC - nguoiquansat.vn | nhóm: ket_qua_kinh_doanh, vi_mo, nganh, rui_ro (2026-08-10T16:09:01+00:00)
- News Reader [nguoiquansat.vn]: Cổ phiếu TCB bứt phá, nhóm ngân hàng đồng loạt tăng - nguoiquansat.vn | nhóm: ket_qua_kinh_doanh, nganh (2026-08-10T09:11:01+00:00)

### Rủi ro cần kiểm chứng

- ML guard: AUC 0.497 < 0.540
- ML guard: Balanced accuracy 0.486 < 0.520
- ML guard: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.49738268188631385, AUC logistic=0.5009108728237057
- ML guard: Probability 51.0% < 55.0%
- ML guard: Lợi thế OOS ròng không đạt: return=-0.2705657999999995, Sharpe=-1.6469342728240042
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

- [Tuổi Trẻ] Tự doanh chứng khoán mua ròng hàng trăm tỉ đồng, cổ phiếu TCB áp sát kỷ lục lịch sử - Tuổi Trẻ (2026-08-10T12:16:00+00:00): https://tuoitre.vn/tu-doanh-chung-khoan-mua-rong-hang-tram-ti-dong-co-phieu-tcb-ap-sat-ky-luc-lich-su-100260810184528929.htm
- [VietnamFinance] TCB cùng nhóm cổ phiếu doanh nghiệp Nhà nước 'kéo' VN-Index tăng gần 9 điểm - VietnamFinance (2026-08-10T09:22:36+00:00): https://vietnamfinance.vn/tcb-cung-nhom-co-phieu-doanh-nghiep-nha-nuoc-keo-vn-index-tang-gan-9-diem-d148847.html
- [nguoiquansat.vn] Cổ phiếu đáng chú ý ngày 11/8: TCB, GAS, VGC - nguoiquansat.vn (2026-08-10T16:09:01+00:00): https://nguoiquansat.vn/co-phieu-dang-chu-y-ngay-11-8-tcb-gas-vgc-309709.html
- [nguoiquansat.vn] Cổ phiếu TCB bứt phá, nhóm ngân hàng đồng loạt tăng - nguoiquansat.vn (2026-08-10T09:11:01+00:00): https://nguoiquansat.vn/co-phieu-tcb-but-pha-nhom-ngan-hang-dong-loat-tang-309624.html

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.
