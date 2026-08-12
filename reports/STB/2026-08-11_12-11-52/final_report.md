# Báo cáo ngày 2026-08-11 - STB

## Tổng quan

- Dữ liệu: 2008-03-10 -> 2026-08-11, 4,593 phiên.
- Giá đóng cửa: 74.70 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Tích cực (điểm 6).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 50.8%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 72.58; SMA60 71.35; RSI14 59.4.
- MACD 0.707; đường tín hiệu 0.449; biểu đồ cột 0.258.
- ATR14 2.04; ATR% 2.7%; ADX14 15.2.
- Xu hướng: Tích cực - Giá nằm trên SMA20 và SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 59.4.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Đi ngang - ADX 15.2.
- Thanh khoản: Thấp - 0.12 lần trung bình.
- Stochastic: Hồi phục - %K nằm trên %D.

## Phân tích cơ bản

- Doanh nghiệp: NH Sài Gòn Tài Lộc (SACOMBANK).
- Ngành: Banks.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 45.66.
- P/B: 2.24.
- ROE: 5.0%.
- ROA: 0.4%.
- Market cap: 140,637.1 tỷ.
- Revenue Growth: 28.1%.
- Profit Growth: -53.5%.
- P/E 45.66: định giá cao, cần tăng trưởng lợi nhuận hỗ trợ.
- P/B 2.24: nên đọc cùng ROE và đặc thù ngành.
- ROE 5.0%: hiệu quả vốn còn yếu.
- Debt/Equity 13.20: đòn bẩy cao, cần đọc theo ngành.
- NPL 7.5%: cần theo dõi.
- Revenue Growth 28.1% YoY.
- Profit Growth -53.5% YoY.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.10 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-07T09:37:32+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-08-23 -> 2026-08-10.
- XGBoost: độ chính xác cân bằng 0.504; AUC 0.504; log-loss 0.693.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.513; AUC 0.511.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 33.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -13.4%; Sharpe -0.48; mức sụt giảm tối đa -19.5%.
- Mức độ quan trọng của đặc trưng: market_return_1d=13.73; bb_position_20=11.64; volatility_20d=11.42; return_5d=11.35; range_pct=11.31; beta_60d=11.13.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 71.65; mục tiêu 1 84.80; mục tiêu 2 84.80.
- Tỷ lệ lợi nhuận/rủi ro 2.84; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 73.85 (-1.14%).
- P10/P90 cuối kỳ 65.06 / 84.80.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.504 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.504 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5037007763504879, AUC logistic=0.510795777717042.
- Điều kiện phát hành tín hiệu: Probability 50.8% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.13432860000000035, Sharpe=-0.4810386267184205.
- Xu hướng ngắn hạn thuận: giá trên SMA20 và SMA60.
- Xu hướng kỹ thuật nghiêng về: Tích cực.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 50.8%.
- Mô hình Logistic đối chứng: 49.8%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 45.5%.
- Mức dừng lỗ tham chiếu 71.65, mục tiêu 1 84.80, tỷ lệ lợi nhuận/rủi ro 2.84.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. Live research lưu 1 headline có URL để theo dõi thêm, nhưng chưa đọc và xác minh toàn văn nên không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Tích cực; điểm 6. Chi tiết artifact: Xu hướng: Tích cực (Giá nằm trên SMA20 và SMA60.); MACD: Tích cực (MACD trên signal, histogram dương.); RSI14: Tích cực (RSI 59.4.); Bollinger: Ổn định (Giá nằm trong dải Bollinger.); ADX: Đi ngang (ADX 15.2.); Thanh khoản: Thấp (0.12 lần trung bình.); Stochastic: Hồi phục (%K nằm trên %D.)
- Góc nhìn cơ bản: Artifact cơ bản: NH Sài Gòn Tài Lộc (SACOMBANK); kỳ 2026-Q2; P/E 45.66; P/B 2.24; ROE 5.0%; ROA 0.4%; Debt/Equity 13.20; Revenue Growth 28.1%; Profit Growth -53.5%.
- Tin doanh nghiệp: Snapshot có 1 headline từ nguồn báo chí. Đây chỉ là danh sách chủ đề cần kiểm chứng; không có nhãn sentiment hoặc dữ liệu nội dung đã xác minh nên không được diễn giải là tin tích cực/tiêu cực.
- Live research: Live snapshot lấy lúc 2026-08-11T05:12:05.684284+00:00; News Reader đọc được 0 bài. ML có 5 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest.

### Bằng chứng

- ML decision artifact: NO_EDGE. AUC 0.504 < 0.540
- ML decision artifact: NO_EDGE. Balanced accuracy 0.504 < 0.520
- ML decision artifact: NO_EDGE. XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5037007763504879, AUC logistic=0.510795777717042
- ML decision artifact: NO_EDGE. Probability 50.8% < 55.0%
- ML decision artifact: NO_EDGE. Lợi thế OOS ròng không đạt: return=-0.13432860000000035, Sharpe=-0.4810386267184205
- Headline [Việt Báo]: VHM, VCB, TCB, STB, FPT, GMD, PHP vào danh mục đầu tư tháng 8? - Việt Báo (2026-08-05T22:01:39+00:00)

### Rủi ro cần kiểm chứng

- ML guard: AUC 0.504 < 0.540
- ML guard: Balanced accuracy 0.504 < 0.520
- ML guard: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5037007763504879, AUC logistic=0.510795777717042
- ML guard: Probability 50.8% < 55.0%
- ML guard: Lợi thế OOS ròng không đạt: return=-0.13432860000000035, Sharpe=-0.4810386267184205
- Chỉ lưu trích đoạn giới hạn để kiểm chứng nguồn; không lưu hay hiển thị toàn văn bài báo.
- Phân nhóm là keyword rule-based để định tuyến research, không phải sentiment hay dự báo tác động giá.
- Dữ liệu News Reader chỉ phục vụ research/report; không dùng làm feature train/backtest khi chưa có lịch sử available_at point-in-time.
- Tin live/trích đoạn cần mở URL gốc để kiểm chứng bối cảnh, số liệu và thời điểm trước khi sử dụng.

### Nguồn live research

- [Việt Báo] VHM, VCB, TCB, STB, FPT, GMD, PHP vào danh mục đầu tư tháng 8? - Việt Báo (2026-08-05T22:01:39+00:00): https://news.google.com/rss/articles/CBMijwFBVV95cUxOclpTb3kwWDR2ZEFLZXdMS0ZZMTl5cy1pM290anV1cm9QM0M4aEpJYUdxaXVEXzlFMU9ua1ZQNWF2REh3dTBfZFhLWHlVNUhXcnR5bmFVTktVM1ktRjVfSTU1dXdqNzR3VGp3WV9OTGZ5S2hHci1McFl0TWlnX3JkMS1wMkJ2Sk1kZ2FJbWxJOA?oc=5

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.
