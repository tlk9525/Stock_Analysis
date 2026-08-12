# Báo cáo ngày 2026-08-09 - HCM

## Tổng quan

- Dữ liệu: 2009-05-19 -> 2026-08-07, 4,298 phiên.
- Giá đóng cửa: 25.35 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Trung tính (điểm -1).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 48.3%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 25.10; SMA60 24.38; RSI14 54.6.
- MACD 0.305; đường tín hiệu 0.338; biểu đồ cột -0.034.
- ATR14 0.84; ATR% 3.3%; ADX14 12.3.
- Xu hướng: Tích cực - Giá nằm trên SMA20 và SMA60.
- MACD: Cẩn thận - MACD dưới signal, histogram âm.
- RSI14: Trung tính - RSI 54.6.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Đi ngang - ADX 12.3.
- Thanh khoản: Thấp - 0.50 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: Chứng khoán HSC.
- Ngành: Financial Services.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 19.24.
- P/B: 1.97.
- ROE: 9.8%.
- ROA: 3.1%.
- Market cap: 34,221.1 tỷ.
- Revenue Growth: 15.1%.
- Profit Growth: 42.0%.
- P/E 19.24: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 1.97: nên đọc cùng ROE và đặc thù ngành.
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

- Kiểm thử: 2023-10-17 -> 2026-08-06.
- XGBoost: độ chính xác cân bằng 0.518; AUC 0.557; log-loss 0.687.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.519; AUC 0.564.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 51.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -12.6%; Sharpe -0.34; mức sụt giảm tối đa -20.4%.
- Mức độ quan trọng của đặc trưng: volatility_20d=13.23; return_1d=11.61; macd_pct=11.47; beta_60d=10.96; market_return_1d=10.71; corr_60d=10.65.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 24.13; mục tiêu 1 28.79; mục tiêu 2 28.79.
- Tỷ lệ lợi nhuận/rủi ro 2.46; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 25.05 (-1.17%).
- P10/P90 cuối kỳ 22.04 / 28.79.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.518 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.557401586588834, AUC logistic=0.5642535215952369.
- Điều kiện phát hành tín hiệu: Probability 48.3% < 55.0%.
- Điều kiện phát hành tín hiệu: Technical score -1 < 2.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.12580115000000103, Sharpe=-0.3378389084634233.
- Xu hướng ngắn hạn thuận: giá trên SMA20 và SMA60.
- Xu hướng kỹ thuật nghiêng về: Trung tính.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 48.3%.
- Mô hình Logistic đối chứng: 40.3%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 45.5%.
- Mức dừng lỗ tham chiếu 24.13, mục tiêu 1 28.79, tỷ lệ lợi nhuận/rủi ro 2.46.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. News Reader đã trích đoạn có nguồn của 3 bài để phân loại chủ đề (ket_qua_kinh_doanh: 1, nganh: 1, rui_ro: 2), nhưng các trích đoạn này không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Trung tính; điểm -1. Chi tiết artifact: Xu hướng: Tích cực (Giá nằm trên SMA20 và SMA60.); MACD: Cẩn thận (MACD dưới signal, histogram âm.); RSI14: Trung tính (RSI 54.6.); Bollinger: Ổn định (Giá nằm trong dải Bollinger.); ADX: Đi ngang (ADX 12.3.); Thanh khoản: Thấp (0.50 lần trung bình.); Stochastic: Yếu lại (%K nằm dưới %D.)
- Góc nhìn cơ bản: Artifact cơ bản: Chứng khoán HSC; kỳ 2026-Q2; P/E 19.24; P/B 1.97; ROE 9.8%; ROA 3.1%; Debt/Equity 1.82; Revenue Growth 15.1%; Profit Growth 42.0%.
- Tin doanh nghiệp: Đã đọc trích đoạn giới hạn của 3 bài; phân nhóm rule-based: ket_qua_kinh_doanh: 1, nganh: 1, rui_ro: 2. Tác động cần kiểm chứng: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường. So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp. Xác minh công bố chính thức, phạm vi ảnh hưởng và khả năng định lượng rủi ro. Đây không phải sentiment hay dự báo tác động giá.
- Live research: Live snapshot lấy lúc 2026-08-09T08:29:14.941445+00:00; News Reader đọc được 3 bài. ML có 5 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest.

### Bằng chứng

- ML decision artifact: NO_EDGE. Balanced accuracy 0.518 < 0.520
- ML decision artifact: NO_EDGE. XGBoost chưa vượt logistic baseline: AUC XGBoost=0.557401586588834, AUC logistic=0.5642535215952369
- ML decision artifact: NO_EDGE. Probability 48.3% < 55.0%
- ML decision artifact: NO_EDGE. Technical score -1 < 2
- ML decision artifact: NO_EDGE. Lợi thế OOS ròng không đạt: return=-0.12580115000000103, Sharpe=-0.3378389084634233
- News Reader [VOV.VN]: 57 mã cổ phiếu không đủ điều kiện giao dịch ký quỹ trên sàn Tp.HCM - VOV.VN | nhóm: rui_ro (2026-08-07T02:20:00+00:00)
- News Reader [24HMoney]: Cổ phiếu MBS, HCM, VCK - Có nên mua? Đánh giá KQKD quý 2 và dự phóng lợi nhuận quý 3 năm 2026 - 24HMoney | nhóm: ket_qua_kinh_doanh, nganh (2026-08-06T06:54:33+00:00)
- News Reader [nguoiquansat.vn]: 5 cổ phiếu hot LPB, ACB, HCM, POW và VNM dưới góc nhìn phân tích kỹ thuật: Mua được không? - nguoiquansat.vn | nhóm: rui_ro (2026-08-03T03:55:01+00:00)

### Rủi ro cần kiểm chứng

- ML guard: Balanced accuracy 0.518 < 0.520
- ML guard: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.557401586588834, AUC logistic=0.5642535215952369
- ML guard: Probability 48.3% < 55.0%
- ML guard: Technical score -1 < 2
- ML guard: Lợi thế OOS ròng không đạt: return=-0.12580115000000103, Sharpe=-0.3378389084634233
- News Reader: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường.
- News Reader: So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp.
- News Reader: Xác minh công bố chính thức, phạm vi ảnh hưởng và khả năng định lượng rủi ro.
- Chỉ lưu trích đoạn giới hạn để kiểm chứng nguồn; không lưu hay hiển thị toàn văn bài báo.
- Phân nhóm là keyword rule-based để định tuyến research, không phải sentiment hay dự báo tác động giá.
- Dữ liệu News Reader chỉ phục vụ research/report; không dùng làm feature train/backtest khi chưa có lịch sử available_at point-in-time.
- Tin live/trích đoạn cần mở URL gốc để kiểm chứng bối cảnh, số liệu và thời điểm trước khi sử dụng.

### Nguồn live research

- [VOV.VN] 57 mã cổ phiếu không đủ điều kiện giao dịch ký quỹ trên sàn Tp.HCM - VOV.VN (2026-08-07T02:20:00+00:00): https://vov1.vov.vn/kinh-te/truoc-gio-mo-cua/57-ma-co-phieu-khong-du-dieu-kien-giao-dich-ky-quy-tren-san-tphcm-133490.vov
- [24HMoney] Cổ phiếu MBS, HCM, VCK - Có nên mua? Đánh giá KQKD quý 2 và dự phóng lợi nhuận quý 3 năm 2026 - 24HMoney (2026-08-06T06:54:33+00:00): https://24hmoney.vn/news/co-phieu-mbs-hcm-vck-co-nen-mua-danh-gia-kqkd-quy-2-va-du-phong-loi-nhuan-quy-3-nam-2026-c30a2817334.html
- [nguoiquansat.vn] 5 cổ phiếu hot LPB, ACB, HCM, POW và VNM dưới góc nhìn phân tích kỹ thuật: Mua được không? - nguoiquansat.vn (2026-08-03T03:55:01+00:00): https://nguoiquansat.vn/5-co-phieu-hot-lpb-acb-hcm-pow-va-vnm-duoi-goc-nhin-phan-tich-ky-thuat-mua-duoc-khong-308053.html

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.
