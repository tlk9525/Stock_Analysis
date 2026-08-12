# Báo cáo ngày 2026-08-09 - TCB

## Tổng quan

- Dữ liệu: 2018-06-04 -> 2026-08-07, 2,045 phiên.
- Giá đóng cửa: 29.70 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Trung tính (điểm 0).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 50.9%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 29.88; SMA60 31.56; RSI14 44.6.
- MACD -0.698; đường tín hiệu -0.802; biểu đồ cột 0.103.
- ATR14 0.79; ATR% 2.7%; ADX14 32.8.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Yếu - RSI 44.6.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng giảm - ADX 32.8, -DI vượt +DI.
- Thanh khoản: Đột biến - 1.74 lần trung bình.
- Stochastic: Hồi phục - %K nằm trên %D.

## Phân tích cơ bản

- Doanh nghiệp: Techcombank.
- Ngành: Banks.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 7.76.
- P/B: 1.17.
- ROE: 14.8%.
- ROA: 2.3%.
- Market cap: 210,461.3 tỷ.
- Revenue Growth: 17.3%.
- Profit Growth: 17.7%.
- P/E 7.76: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 1.17: nên đọc cùng ROE và đặc thù ngành.
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

- Kiểm thử: 2023-09-08 -> 2026-08-06.
- XGBoost: độ chính xác cân bằng 0.486; AUC 0.498; log-loss 0.695.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.495; AUC 0.502.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 15.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -27.1%; Sharpe -1.65; mức sụt giảm tối đa -27.7%.
- Mức độ quan trọng của đặc trưng: volatility_20d=14.39; bb_position_20=10.61; return_5d=10.13; close_vs_sma60=9.97; relative_strength_20d=9.91; return_2d=9.76.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 28.52; mục tiêu 1 32.35; mục tiêu 2 32.91.
- Tỷ lệ lợi nhuận/rủi ro 1.88; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 29.54 (-0.55%).
- P10/P90 cuối kỳ 26.28 / 32.91.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.498 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.486 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.4975284097502108, AUC logistic=0.5018604615182294.
- Điều kiện phát hành tín hiệu: Probability 50.9% < 55.0%.
- Điều kiện phát hành tín hiệu: Technical score 0 < 2.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.2705657999999995, Sharpe=-1.6492225771903177.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Trung tính.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 50.9%.
- Mô hình Logistic đối chứng: 44.6%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 47.7%.
- Mức dừng lỗ tham chiếu 28.52, mục tiêu 1 32.35, tỷ lệ lợi nhuận/rủi ro 1.88.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. Live research lưu 1 headline có URL để theo dõi thêm, nhưng chưa đọc và xác minh toàn văn nên không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Trung tính; điểm 0. Chi tiết artifact: Xu hướng: Cẩn thận (Giá nằm dưới SMA60.); MACD: Tích cực (MACD trên signal, histogram dương.); RSI14: Yếu (RSI 44.6.); Bollinger: Ổn định (Giá nằm trong dải Bollinger.); ADX: Xu hướng giảm (ADX 32.8, -DI vượt +DI.); Thanh khoản: Đột biến (1.74 lần trung bình.); Stochastic: Hồi phục (%K nằm trên %D.)
- Góc nhìn cơ bản: Artifact cơ bản: Techcombank; kỳ 2026-Q2; P/E 7.76; P/B 1.17; ROE 14.8%; ROA 2.3%; Debt/Equity 5.74; Revenue Growth 17.3%; Profit Growth 17.7%.
- Tin doanh nghiệp: Snapshot có 1 headline từ nguồn báo chí. Đây chỉ là danh sách chủ đề cần kiểm chứng; không có nhãn sentiment hoặc dữ liệu nội dung đã xác minh nên không được diễn giải là tin tích cực/tiêu cực.
- Live research: Live snapshot lấy lúc 2026-08-09T08:38:00.331995+00:00; News Reader đọc được 0 bài. ML có 6 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest.

### Bằng chứng

- ML decision artifact: NO_EDGE. AUC 0.498 < 0.540
- ML decision artifact: NO_EDGE. Balanced accuracy 0.486 < 0.520
- ML decision artifact: NO_EDGE. XGBoost chưa vượt logistic baseline: AUC XGBoost=0.4975284097502108, AUC logistic=0.5018604615182294
- ML decision artifact: NO_EDGE. Probability 50.9% < 55.0%
- ML decision artifact: NO_EDGE. Technical score 0 < 2
- ML decision artifact: NO_EDGE. Lợi thế OOS ròng không đạt: return=-0.2705657999999995, Sharpe=-1.6492225771903177
- Headline [Việt Báo]: VHM, VCB, TCB, STB, FPT, GMD, PHP vào danh mục đầu tư tháng 8? - Việt Báo (2026-08-05T22:01:39+00:00)

### Rủi ro cần kiểm chứng

- ML guard: AUC 0.498 < 0.540
- ML guard: Balanced accuracy 0.486 < 0.520
- ML guard: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.4975284097502108, AUC logistic=0.5018604615182294
- ML guard: Probability 50.9% < 55.0%
- ML guard: Technical score 0 < 2
- ML guard: Lợi thế OOS ròng không đạt: return=-0.2705657999999995, Sharpe=-1.6492225771903177
- Chỉ lưu trích đoạn giới hạn để kiểm chứng nguồn; không lưu hay hiển thị toàn văn bài báo.
- Phân nhóm là keyword rule-based để định tuyến research, không phải sentiment hay dự báo tác động giá.
- Dữ liệu News Reader chỉ phục vụ research/report; không dùng làm feature train/backtest khi chưa có lịch sử available_at point-in-time.
- Tin live/trích đoạn cần mở URL gốc để kiểm chứng bối cảnh, số liệu và thời điểm trước khi sử dụng.

### Nguồn live research

- [Việt Báo] VHM, VCB, TCB, STB, FPT, GMD, PHP vào danh mục đầu tư tháng 8? - Việt Báo (2026-08-05T22:01:39+00:00): https://news.google.com/rss/articles/CBMijwFBVV95cUxOclpTb3kwWDR2ZEFLZXdMS0ZZMTl5cy1pM290anV1cm9QM0M4aEpJYUdxaXVEXzlFMU9ua1ZQNWF2REh3dTBfZFhLWHlVNUhXcnR5bmFVTktVM1ktRjVfSTU1dXdqNzR3VGp3WV9OTGZ5S2hHci1McFl0TWlnX3JkMS1wMkJ2Sk1kZ2FJbWxJOA?oc=5

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.
