# Báo cáo ngày 2026-08-11 - HCM

## Tổng quan

- Dữ liệu: 2009-05-19 -> 2026-08-11, 4,300 phiên.
- Giá đóng cửa: 27.00 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Tích cực (điểm 5).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 48.4%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 25.39; SMA60 24.40; RSI14 67.3.
- MACD 0.442; đường tín hiệu 0.359; biểu đồ cột 0.083.
- ATR14 0.88; ATR% 3.2%; ADX14 13.9.
- Xu hướng: Tích cực - Giá nằm trên SMA20 và SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 67.3.
- Bollinger: Gần biên trên - Giá sát/vượt biên trên.
- ADX: Đi ngang - ADX 13.9.
- Thanh khoản: Bình thường - 1.23 lần trung bình.
- Stochastic: Cực trị - %K 89.2, %D 77.8.

## Phân tích cơ bản

- Doanh nghiệp: Chứng khoán HSC.
- Ngành: Financial Services.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 19.74.
- P/B: 2.02.
- ROE: 9.8%.
- ROA: 3.1%.
- Market cap: 35,031.1 tỷ.
- Revenue Growth: 15.1%.
- Profit Growth: 42.0%.
- P/E 19.74: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 2.02: nên đọc cùng ROE và đặc thù ngành.
- ROA 3.1%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 1.54: thanh khoản ngắn hạn khá.
- Revenue Growth 15.1% YoY.
- Profit Growth 42.0% YoY.
- CFO/LNST 1.16: chất lượng chuyển đổi lợi nhuận sang tiền mặt khá tốt.
- Dòng tiền tự do quý gần nhất dương; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là nợ vay ròng; không dùng một mình để kết luận rủi ro.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.16 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-04T10:19:59+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-10-17 -> 2026-08-10.
- XGBoost: độ chính xác cân bằng 0.518; AUC 0.558; log-loss 0.687.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.519; AUC 0.562.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 51.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -12.6%; Sharpe -0.34; mức sụt giảm tối đa -20.4%.
- Mức độ quan trọng của đặc trưng: volatility_20d=12.51; macd_pct=11.09; return_1d=10.87; corr_60d=10.45; market_return_1d=10.32; beta_60d=10.29.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 25.68; mục tiêu 1 30.67; mục tiêu 2 30.67.
- Tỷ lệ lợi nhuận/rủi ro 2.43; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 26.70 (-1.11%).
- P10/P90 cuối kỳ 23.44 / 30.67.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.518 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5584911271934173, AUC logistic=0.562002247116751.
- Điều kiện phát hành tín hiệu: Probability 48.4% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.12580115000000103, Sharpe=-0.3373570968837999.
- Xu hướng ngắn hạn thuận: giá trên SMA20 và SMA60.
- Xu hướng kỹ thuật nghiêng về: Tích cực.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 48.4%.
- Mô hình Logistic đối chứng: 43.1%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 45.9%.
- Mức dừng lỗ tham chiếu 25.68, mục tiêu 1 30.67, tỷ lệ lợi nhuận/rủi ro 2.43.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. News Reader đã trích đoạn có nguồn của 4 bài để phân loại chủ đề (ket_qua_kinh_doanh: 2, co_tuc_va_hanh_dong_doanh_nghiep: 1, vi_mo: 2, nganh: 3, rui_ro: 2), nhưng các trích đoạn này không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Tích cực; điểm 5. Chi tiết artifact: Xu hướng: Tích cực (Giá nằm trên SMA20 và SMA60.); MACD: Tích cực (MACD trên signal, histogram dương.); RSI14: Tích cực (RSI 67.3.); Bollinger: Gần biên trên (Giá sát/vượt biên trên.); ADX: Đi ngang (ADX 13.9.); Thanh khoản: Bình thường (1.23 lần trung bình.); Stochastic: Cực trị (%K 89.2, %D 77.8.)
- Góc nhìn cơ bản: Artifact cơ bản: Chứng khoán HSC; kỳ 2026-Q2; P/E 19.74; P/B 2.02; ROE 9.8%; ROA 3.1%; Debt/Equity 1.82; Revenue Growth 15.1%; Profit Growth 42.0%.
- Tin doanh nghiệp: Đã đọc trích đoạn giới hạn của 4 bài; phân nhóm rule-based: ket_qua_kinh_doanh: 2, co_tuc_va_hanh_dong_doanh_nghiep: 1, vi_mo: 2, nganh: 3, rui_ro: 2. Tác động cần kiểm chứng: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường. Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động. Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh. So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp. Xác minh công bố chính thức, phạm vi ảnh hưởng và khả năng định lượng rủi ro. Đây không phải sentiment hay dự báo tác động giá.
- Live research: Live snapshot lấy lúc 2026-08-11T05:01:06.455529+00:00; News Reader đọc được 4 bài. ML có 4 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest.

### Bằng chứng

- ML decision artifact: NO_EDGE. Balanced accuracy 0.518 < 0.520
- ML decision artifact: NO_EDGE. XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5584911271934173, AUC logistic=0.562002247116751
- ML decision artifact: NO_EDGE. Probability 48.4% < 55.0%
- ML decision artifact: NO_EDGE. Lợi thế OOS ròng không đạt: return=-0.12580115000000103, Sharpe=-0.3373570968837999
- News Reader [nguoiquansat.vn]: Cổ phiếu chứng khoán 'chạy' trước nâng hạng: HCM phá đỉnh, VCI, VIX, SHS... cùng tăng mạnh - nguoiquansat.vn | nhóm: vi_mo, nganh (2026-08-11T04:48:01+00:00)
- News Reader [24HMoney]: 7 cổ phiếu được kỳ vọng tăng giá từ 10-27% - 24HMoney | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh, rui_ro (2026-08-11T00:33:04+00:00)
- News Reader [VOV.VN]: 57 mã cổ phiếu không đủ điều kiện giao dịch ký quỹ trên sàn Tp.HCM - VOV.VN | nhóm: rui_ro (2026-08-07T02:20:00+00:00)
- News Reader [24HMoney]: Cổ phiếu MBS, HCM, VCK - Có nên mua? Đánh giá KQKD quý 2 và dự phóng lợi nhuận quý 3 năm 2026 - 24HMoney | nhóm: ket_qua_kinh_doanh, nganh (2026-08-06T06:54:33+00:00)

### Rủi ro cần kiểm chứng

- ML guard: Balanced accuracy 0.518 < 0.520
- ML guard: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5584911271934173, AUC logistic=0.562002247116751
- ML guard: Probability 48.4% < 55.0%
- ML guard: Lợi thế OOS ròng không đạt: return=-0.12580115000000103, Sharpe=-0.3373570968837999
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

- [nguoiquansat.vn] Cổ phiếu chứng khoán 'chạy' trước nâng hạng: HCM phá đỉnh, VCI, VIX, SHS... cùng tăng mạnh - nguoiquansat.vn (2026-08-11T04:48:01+00:00): https://nguoiquansat.vn/co-phieu-chung-khoan-chay-truoc-nang-hang-hcm-pha-dinh-vci-vix-shs-cung-tang-manh-309801.html
- [24HMoney] 7 cổ phiếu được kỳ vọng tăng giá từ 10-27% - 24HMoney (2026-08-11T00:33:04+00:00): https://24hmoney.vn/news/7-co-phieu-duoc-ky-vong-tang-gia-tu-10-27-c1a2819001.html
- [VOV.VN] 57 mã cổ phiếu không đủ điều kiện giao dịch ký quỹ trên sàn Tp.HCM - VOV.VN (2026-08-07T02:20:00+00:00): https://vov1.vov.vn/kinh-te/truoc-gio-mo-cua/57-ma-co-phieu-khong-du-dieu-kien-giao-dich-ky-quy-tren-san-tphcm-133490.vov
- [24HMoney] Cổ phiếu MBS, HCM, VCK - Có nên mua? Đánh giá KQKD quý 2 và dự phóng lợi nhuận quý 3 năm 2026 - 24HMoney (2026-08-06T06:54:33+00:00): https://24hmoney.vn/news/co-phieu-mbs-hcm-vck-co-nen-mua-danh-gia-kqkd-quy-2-va-du-phong-loi-nhuan-quy-3-nam-2026-c30a2817334.html

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.
