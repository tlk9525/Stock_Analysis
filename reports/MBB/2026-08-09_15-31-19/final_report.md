# Báo cáo ngày 2026-08-09 - MBB

## Tổng quan

- Dữ liệu: 2011-11-01 -> 2026-08-07, 3,684 phiên.
- Giá đóng cửa: 24.15 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Tích cực (điểm 5).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 50.2%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 23.21; SMA60 23.83; RSI14 57.4.
- MACD -0.011; đường tín hiệu -0.247; biểu đồ cột 0.236.
- ATR14 0.58; ATR% 2.4%; ADX14 27.6.
- Xu hướng: Trung tính - Giá trên SMA60 nhưng chưa vượt SMA20.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 57.4.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng tăng - ADX 27.6, +DI vượt -DI.
- Thanh khoản: Thấp - 0.66 lần trung bình.
- Stochastic: Cực trị - %K 88.9, %D 87.8.

## Phân tích cơ bản

- Doanh nghiệp: MBBank.
- Ngành: Banks.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 6.47.
- P/B: 1.30.
- ROE: 20.7%.
- ROA: 1.9%.
- Market cap: 194,528.2 tỷ.
- Revenue Growth: 18.5%.
- Profit Growth: 40.0%.
- P/E 6.47: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 1.30: nên đọc cùng ROE và đặc thù ngành.
- ROE 20.7%: hiệu quả vốn chủ sở hữu tốt.
- Debt/Equity 10.06: đòn bẩy cao, cần đọc theo ngành.
- NPL 1.4%: đang ở mức kiểm soát.
- Revenue Growth 18.5% YoY.
- Profit Growth 40.0% YoY.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.14 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-07T08:40:35+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2024-01-17 -> 2026-08-06.
- XGBoost: độ chính xác cân bằng 0.528; AUC 0.523; log-loss 0.693.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.510; AUC 0.505.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 25.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận 13.2%; Sharpe 0.69; mức sụt giảm tối đa -5.0%.
- Mức độ quan trọng của đặc trưng: return_1d=13.15; beta_60d=12.42; volatility_20d=11.90; return_skew_20d=11.52; stoch_k_14=11.30; excess_return_1d=10.60.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 23.59; mục tiêu 1 26.89; mục tiêu 2 26.89.
- Tỷ lệ lợi nhuận/rủi ro 3.84; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 23.76 (-1.63%).
- P10/P90 cuối kỳ 21.57 / 26.89.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.523 < 0.540.
- Điều kiện phát hành tín hiệu: Probability 50.2% < 55.0%.
- Trung hạn chưa xấu, ngắn hạn yếu vì giá dưới SMA20.
- Xu hướng kỹ thuật nghiêng về: Tích cực.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 50.2%.
- Mô hình Logistic đối chứng: 46.4%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 41.6%.
- Mức dừng lỗ tham chiếu 23.59, mục tiêu 1 26.89, tỷ lệ lợi nhuận/rủi ro 3.84.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. News Reader đã trích đoạn có nguồn của 4 bài để phân loại chủ đề (ket_qua_kinh_doanh: 4, co_tuc_va_hanh_dong_doanh_nghiep: 4, vi_mo: 2, nganh: 1, rui_ro: 1), nhưng các trích đoạn này không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Tích cực; điểm 5. Chi tiết artifact: Xu hướng: Trung tính (Giá trên SMA60 nhưng chưa vượt SMA20.); MACD: Tích cực (MACD trên signal, histogram dương.); RSI14: Tích cực (RSI 57.4.); Bollinger: Ổn định (Giá nằm trong dải Bollinger.); ADX: Xu hướng tăng (ADX 27.6, +DI vượt -DI.); Thanh khoản: Thấp (0.66 lần trung bình.); Stochastic: Cực trị (%K 88.9, %D 87.8.)
- Góc nhìn cơ bản: Artifact cơ bản: MBBank; kỳ 2026-Q2; P/E 6.47; P/B 1.30; ROE 20.7%; ROA 1.9%; Debt/Equity 10.06; Revenue Growth 18.5%; Profit Growth 40.0%.
- Tin doanh nghiệp: Đã đọc trích đoạn giới hạn của 4 bài; phân nhóm rule-based: ket_qua_kinh_doanh: 4, co_tuc_va_hanh_dong_doanh_nghiep: 4, vi_mo: 2, nganh: 1, rui_ro: 1. Tác động cần kiểm chứng: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường. Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động. Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh. So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp. Xác minh công bố chính thức, phạm vi ảnh hưởng và khả năng định lượng rủi ro. Đây không phải sentiment hay dự báo tác động giá.
- Live research: Live snapshot lấy lúc 2026-08-09T08:31:33.731157+00:00; News Reader đọc được 4 bài. ML có 2 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest.

### Bằng chứng

- ML decision artifact: NO_EDGE. AUC 0.523 < 0.540
- ML decision artifact: NO_EDGE. Probability 50.2% < 55.0%
- News Reader [Tin nhanh chứng khoán]: MB chốt quyền chia cổ tức 15%, phát hành chào bán gần 805,5 triệu cổ phiếu giá 10.000 đồng/CP - Tin nhanh chứng khoán | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh (2026-08-04T08:39:02+00:00)
- News Reader [Vietstock]: MB chốt quyền chia cổ tức và chào bán cổ phiếu, nâng vốn điều lệ lên hơn 100,600 tỷ - Vietstock | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep (2026-08-04T04:58:05+00:00)
- News Reader [Báo Pháp Luật Việt Nam]: MBBank (MBB) sắp chào bán cổ phiếu và trả cổ tức cho cổ đông - Báo Pháp Luật Việt Nam | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, rui_ro (2026-08-02T12:44:00+00:00)
- News Reader [nguoiquansat.vn]: Lịch chốt quyền cổ tức tuần 10-14/8: MBB, BSR, MCH đồng loạt thanh toán; tỷ lệ cao nhất 100% - nguoiquansat.vn | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep (2026-08-09T03:12:01+00:00)

### Rủi ro cần kiểm chứng

- ML guard: AUC 0.523 < 0.540
- ML guard: Probability 50.2% < 55.0%
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

- [Tin nhanh chứng khoán] MB chốt quyền chia cổ tức 15%, phát hành chào bán gần 805,5 triệu cổ phiếu giá 10.000 đồng/CP - Tin nhanh chứng khoán (2026-08-04T08:39:02+00:00): https://www.tinnhanhchungkhoan.vn/mb-chot-quyen-chia-co-tuc-15-phat-hanh-chao-ban-gan-8055-trieu-co-phieu-gia-10000-dongcp-post395281.html
- [Vietstock] MB chốt quyền chia cổ tức và chào bán cổ phiếu, nâng vốn điều lệ lên hơn 100,600 tỷ - Vietstock (2026-08-04T04:58:05+00:00): https://vietstock.vn/2026/08/mb-chot-quyen-chia-co-tuc-va-chao-ban-co-phieu-nang-von-dieu-le-len-hon-100600-ty-738-1476203.htm
- [Báo Pháp Luật Việt Nam] MBBank (MBB) sắp chào bán cổ phiếu và trả cổ tức cho cổ đông - Báo Pháp Luật Việt Nam (2026-08-02T12:44:00+00:00): https://doanhnhan.baophapluat.vn/mbbank-mbb-sap-chao-ban-co-phieu-va-tra-co-tuc-cho-co-dong.html
- [nguoiquansat.vn] Lịch chốt quyền cổ tức tuần 10-14/8: MBB, BSR, MCH đồng loạt thanh toán; tỷ lệ cao nhất 100% - nguoiquansat.vn (2026-08-09T03:12:01+00:00): https://nguoiquansat.vn/lich-chot-quyen-co-tuc-tuan-10-14-8-mbb-bsr-mch-dong-loat-thanh-toan-ty-le-cao-nhat-100-309384.html

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.
