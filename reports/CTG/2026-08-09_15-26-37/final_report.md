# Báo cáo ngày 2026-08-09 - CTG

## Tổng quan

- Dữ liệu: 2009-07-16 -> 2026-08-07, 4,258 phiên.
- Giá đóng cửa: 32.50 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Tích cực (điểm 5).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 47.9%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 30.75; SMA60 32.72; RSI14 59.1.
- MACD -0.238; đường tín hiệu -0.610; biểu đồ cột 0.372.
- ATR14 0.85; ATR% 2.6%; ADX14 27.4.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 59.1.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng tăng - ADX 27.4, +DI vượt -DI.
- Thanh khoản: Đột biến - 1.52 lần trung bình.
- Stochastic: Cực trị - %K 89.1, %D 84.4.

## Phân tích cơ bản

- Doanh nghiệp: VietinBank.
- Ngành: Banks.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 6.28.
- P/B: 1.27.
- ROE: 21.8%.
- ROA: 1.4%.
- Market cap: 252,425.7 tỷ.
- Revenue Growth: 26.1%.
- Profit Growth: 21.4%.
- P/E 6.28: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 1.27: nên đọc cùng ROE và đặc thù ngành.
- ROE 21.8%: hiệu quả vốn chủ sở hữu tốt.
- Debt/Equity 13.79: đòn bẩy cao, cần đọc theo ngành.
- NPL 1.2%: đang ở mức kiểm soát.
- Revenue Growth 26.1% YoY.
- Profit Growth 21.4% YoY.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.10 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-04T10:18:58+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-12-08 -> 2026-08-06.
- XGBoost: độ chính xác cân bằng 0.502; AUC 0.492; log-loss 0.694.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.507; AUC 0.491.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 17.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -5.9%; Sharpe -0.38; mức sụt giảm tối đa -13.8%.
- Mức độ quan trọng của đặc trưng: return_1d=15.95; atr_pct_14=14.79; beta_60d=14.19; close_vs_sma60=14.02; rsi_14=13.84; market_return_1d=12.75.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 32.39; mục tiêu 1 33.19; mục tiêu 2 35.68.
- Tỷ lệ lợi nhuận/rủi ro 1.93; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 32.23 (-0.84%).
- P10/P90 cuối kỳ 29.23 / 35.68.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.492 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.502 < 0.520.
- Điều kiện phát hành tín hiệu: Probability 47.9% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.059461009999999814, Sharpe=-0.37736557135369075.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Tích cực.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 47.9%.
- Mô hình Logistic đối chứng: 43.4%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 45.4%.
- Mức dừng lỗ tham chiếu 32.39, mục tiêu 1 33.19, tỷ lệ lợi nhuận/rủi ro 1.93.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. News Reader đã trích đoạn có nguồn của 1 bài để phân loại chủ đề (co_tuc_va_hanh_dong_doanh_nghiep: 1, vi_mo: 1), nhưng các trích đoạn này không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Tích cực; điểm 5. Chi tiết artifact: Xu hướng: Cẩn thận (Giá nằm dưới SMA60.); MACD: Tích cực (MACD trên signal, histogram dương.); RSI14: Tích cực (RSI 59.1.); Bollinger: Ổn định (Giá nằm trong dải Bollinger.); ADX: Xu hướng tăng (ADX 27.4, +DI vượt -DI.); Thanh khoản: Đột biến (1.52 lần trung bình.); Stochastic: Cực trị (%K 89.1, %D 84.4.)
- Góc nhìn cơ bản: Artifact cơ bản: VietinBank; kỳ 2026-Q2; P/E 6.28; P/B 1.27; ROE 21.8%; ROA 1.4%; Debt/Equity 13.79; Revenue Growth 26.1%; Profit Growth 21.4%.
- Tin doanh nghiệp: Đã đọc trích đoạn giới hạn của 1 bài; phân nhóm rule-based: co_tuc_va_hanh_dong_doanh_nghiep: 1, vi_mo: 1. Tác động cần kiểm chứng: Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động. Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh. Đây không phải sentiment hay dự báo tác động giá.
- Live research: Live snapshot lấy lúc 2026-08-09T08:26:51.760046+00:00; News Reader đọc được 1 bài. ML có 4 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest.

### Bằng chứng

- ML decision artifact: NO_EDGE. AUC 0.492 < 0.540
- ML decision artifact: NO_EDGE. Balanced accuracy 0.502 < 0.520
- ML decision artifact: NO_EDGE. Probability 47.9% < 55.0%
- ML decision artifact: NO_EDGE. Lợi thế OOS ròng không đạt: return=-0.059461009999999814, Sharpe=-0.37736557135369075
- News Reader [VietnamBiz]: NHNN cần tăng nắm giữ bao nhiêu cổ phiếu CTG để sở hữu tối thiểu 65% VietinBank? - VietnamBiz | nhóm: co_tuc_va_hanh_dong_doanh_nghiep, vi_mo (2026-08-07T08:45:00+00:00)

### Rủi ro cần kiểm chứng

- ML guard: AUC 0.492 < 0.540
- ML guard: Balanced accuracy 0.502 < 0.520
- ML guard: Probability 47.9% < 55.0%
- ML guard: Lợi thế OOS ròng không đạt: return=-0.059461009999999814, Sharpe=-0.37736557135369075
- News Reader: Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động.
- News Reader: Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh.
- Chỉ lưu trích đoạn giới hạn để kiểm chứng nguồn; không lưu hay hiển thị toàn văn bài báo.
- Phân nhóm là keyword rule-based để định tuyến research, không phải sentiment hay dự báo tác động giá.
- Dữ liệu News Reader chỉ phục vụ research/report; không dùng làm feature train/backtest khi chưa có lịch sử available_at point-in-time.
- Tin live/trích đoạn cần mở URL gốc để kiểm chứng bối cảnh, số liệu và thời điểm trước khi sử dụng.

### Nguồn live research

- [VietnamBiz] NHNN cần tăng nắm giữ bao nhiêu cổ phiếu CTG để sở hữu tối thiểu 65% VietinBank? - VietnamBiz (2026-08-07T08:45:00+00:00): https://vietnambiz.vn/nhnn-can-tang-nam-giu-bao-nhieu-co-phieu-ctg-de-so-huu-toi-thieu-65-vietinbank-202687153739946.htm

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.
