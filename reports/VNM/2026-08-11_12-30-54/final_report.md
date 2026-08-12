# Báo cáo ngày 2026-08-11 - VNM

## Tổng quan

- Dữ liệu: 2008-03-10 -> 2026-08-11, 4,592 phiên.
- Giá đóng cửa: 62.60 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Tích cực (điểm 6).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 65.5%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 59.39; SMA60 57.48; RSI14 66.9.
- MACD 1.215; đường tín hiệu 0.939; biểu đồ cột 0.276.
- ATR14 1.46; ATR% 2.3%; ADX14 27.8.
- Xu hướng: Tích cực - Giá nằm trên SMA20 và SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 66.9.
- Bollinger: Gần biên trên - Giá sát/vượt biên trên.
- ADX: Xu hướng tăng - ADX 27.8, +DI vượt -DI.
- Thanh khoản: Thấp - 0.43 lần trung bình.
- Stochastic: Cực trị - %K 89.1, %D 85.1.

## Phân tích cơ bản

- Doanh nghiệp: VINAMILK.
- Ngành: Food & Beverage.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 11.84.
- P/B: 4.07.
- ROE: 33.9%.
- ROA: 19.8%.
- Market cap: 129,786.2 tỷ.
- Revenue Growth: 12.7%.
- Profit Growth: 28.0%.
- P/E 11.84: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 4.07: nên đọc cùng ROE và đặc thù ngành.
- ROE 33.9%: hiệu quả vốn chủ sở hữu tốt.
- ROA 19.8%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 1.91: thanh khoản ngắn hạn khá.
- Revenue Growth 12.7% YoY.
- Profit Growth 28.0% YoY.
- CFO/LNST 1.01: chất lượng chuyển đổi lợi nhuận sang tiền mặt khá tốt.
- Dòng tiền tự do quý gần nhất dương; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là nợ vay ròng; không dùng một mình để kết luận rủi ro.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.12 (keyword_heuristic_v1).
- Bài mới nhất: 2026-07-31T07:57:00+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-08-24 -> 2026-08-10.
- XGBoost: độ chính xác cân bằng 0.503; AUC 0.526; log-loss 0.684.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.538; AUC 0.561.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 89.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -33.9%; Sharpe -1.41; mức sụt giảm tối đa -35.8%.
- Mức độ quan trọng của đặc trưng: relative_strength_20d=11.62; close_vs_sma20=11.55; return_3d=11.53; return_1d=10.84; volatility_20d=10.25; bb_position_20=9.94.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 60.41; mục tiêu 1 68.50; mục tiêu 2 68.50.
- Tỷ lệ lợi nhuận/rủi ro 2.23; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 62.20 (-0.64%).
- P10/P90 cuối kỳ 56.75 / 68.50.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.526 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.503 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5264774209973586, AUC logistic=0.5608471501766222.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.3386612699999999, Sharpe=-1.4065692077437657.
- Xu hướng ngắn hạn thuận: giá trên SMA20 và SMA60.
- Xu hướng kỹ thuật nghiêng về: Tích cực.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 65.5%.
- Mô hình Logistic đối chứng: 56.9%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 46.1%.
- Mức dừng lỗ tham chiếu 60.41, mục tiêu 1 68.50, tỷ lệ lợi nhuận/rủi ro 2.23.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. News Reader đã trích đoạn có nguồn của 3 bài để phân loại chủ đề (ket_qua_kinh_doanh: 3, co_tuc_va_hanh_dong_doanh_nghiep: 2, vi_mo: 2, nganh: 3, rui_ro: 1), nhưng các trích đoạn này không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Tích cực; điểm 6. Chi tiết artifact: Xu hướng: Tích cực (Giá nằm trên SMA20 và SMA60.); MACD: Tích cực (MACD trên signal, histogram dương.); RSI14: Tích cực (RSI 66.9.); Bollinger: Gần biên trên (Giá sát/vượt biên trên.); ADX: Xu hướng tăng (ADX 27.8, +DI vượt -DI.); Thanh khoản: Thấp (0.43 lần trung bình.); Stochastic: Cực trị (%K 89.1, %D 85.1.)
- Góc nhìn cơ bản: Artifact cơ bản: VINAMILK; kỳ 2026-Q2; P/E 11.84; P/B 4.07; ROE 33.9%; ROA 19.8%; Debt/Equity 0.61; Revenue Growth 12.7%; Profit Growth 28.0%.
- Tin doanh nghiệp: Đã đọc trích đoạn giới hạn của 3 bài; phân nhóm rule-based: ket_qua_kinh_doanh: 3, co_tuc_va_hanh_dong_doanh_nghiep: 2, vi_mo: 2, nganh: 3, rui_ro: 1. Tác động cần kiểm chứng: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường. Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động. Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh. So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp. Xác minh công bố chính thức, phạm vi ảnh hưởng và khả năng định lượng rủi ro. Đây không phải sentiment hay dự báo tác động giá.
- Live research: Live snapshot lấy lúc 2026-08-11T05:31:08.097536+00:00; News Reader đọc được 3 bài. ML có 4 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest.

### Bằng chứng

- ML decision artifact: NO_EDGE. AUC 0.526 < 0.540
- ML decision artifact: NO_EDGE. Balanced accuracy 0.503 < 0.520
- ML decision artifact: NO_EDGE. XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5264774209973586, AUC logistic=0.5608471501766222
- ML decision artifact: NO_EDGE. Lợi thế OOS ròng không đạt: return=-0.3386612699999999, Sharpe=-1.4065692077437657
- News Reader [VietstockFinance]: VNM: Khuyến nghị MUA với giá mục tiêu 73,500 đồng/cổ phiếu - VietstockFinance | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh (2026-08-06T11:10:52+00:00)
- News Reader [nguoiquansat.vn]: Cổ phiếu đáng chú ý ngày 6/8: MSB, VNM, VPB, - nguoiquansat.vn | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh, rui_ro (2026-08-05T16:30:01+00:00)
- News Reader [VietnamBiz]: Cổ phiếu doanh nghiệp Nhà nước đồng loạt hút tiền, VNM, BCM, GAS và GVR tăng trần - VietnamBiz | nhóm: ket_qua_kinh_doanh, nganh (2026-08-07T03:52:00+00:00)

### Rủi ro cần kiểm chứng

- ML guard: AUC 0.526 < 0.540
- ML guard: Balanced accuracy 0.503 < 0.520
- ML guard: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5264774209973586, AUC logistic=0.5608471501766222
- ML guard: Lợi thế OOS ròng không đạt: return=-0.3386612699999999, Sharpe=-1.4065692077437657
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

- [VietstockFinance] VNM: Khuyến nghị MUA với giá mục tiêu 73,500 đồng/cổ phiếu - VietstockFinance (2026-08-06T11:10:52+00:00): https://finance.vietstock.vn/bao-cao-phan-tich/20425/vnm-khuyen-nghi-mua-voi-gia-muc-tieu-73500-dongco-phieu.htm?languageid=1
- [nguoiquansat.vn] Cổ phiếu đáng chú ý ngày 6/8: MSB, VNM, VPB, - nguoiquansat.vn (2026-08-05T16:30:01+00:00): https://nguoiquansat.vn/co-phieu-dang-chu-y-ngay-6-8-msb-vnm-vpb-308705.html
- [VietnamBiz] Cổ phiếu doanh nghiệp Nhà nước đồng loạt hút tiền, VNM, BCM, GAS và GVR tăng trần - VietnamBiz (2026-08-07T03:52:00+00:00): https://vietnambiz.vn/co-phieu-doanh-nghiep-nha-nuoc-dong-loat-hut-tien-vnm-bcm-gas-va-gvr-tang-tran-202687105140436.htm

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.
