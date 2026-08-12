# Báo cáo ngày 2026-08-11 - CTG

## Tổng quan

- Dữ liệu: 2009-07-16 -> 2026-08-11, 4,260 phiên.
- Giá đóng cửa: 32.65 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng (điểm 4).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 51.1%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 30.81; SMA60 32.62; RSI14 59.5.
- MACD 0.011; đường tín hiệu -0.403; biểu đồ cột 0.414.
- ATR14 0.80; ATR% 2.4%; ADX14 25.1.
- Xu hướng: Trung tính - Giá trên SMA60 nhưng chưa vượt SMA20.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 59.5.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng tăng - ADX 25.1, +DI vượt -DI.
- Thanh khoản: Thấp - 0.39 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: VietinBank.
- Ngành: Banks.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 6.34.
- P/B: 1.28.
- ROE: 21.8%.
- ROA: 1.4%.
- Market cap: 254,755.8 tỷ.
- Revenue Growth: 26.1%.
- Profit Growth: 21.4%.
- P/E 6.34: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 1.28: nên đọc cùng ROE và đặc thù ngành.
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

- Kiểm thử: 2023-12-08 -> 2026-08-10.
- XGBoost: độ chính xác cân bằng 0.502; AUC 0.493; log-loss 0.694.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.509; AUC 0.493.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 17.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -5.9%; Sharpe -0.38; mức sụt giảm tối đa -13.8%.
- Mức độ quan trọng của đặc trưng: beta_60d=16.26; return_1d=15.61; atr_pct_14=14.70; close_vs_sma60=12.71; market_return_1d=11.89; volume_z_20=11.28.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 32.30; mục tiêu 1 35.98; mục tiêu 2 35.98.
- Tỷ lệ lợi nhuận/rủi ro 6.14; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 32.46 (-0.59%).
- P10/P90 cuối kỳ 29.51 / 35.98.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.493 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.502 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.4930783841040251, AUC logistic=0.49308751552341296.
- Điều kiện phát hành tín hiệu: Probability 51.1% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.059461009999999814, Sharpe=-0.37679650206545323.
- Trung hạn chưa xấu, ngắn hạn yếu vì giá dưới SMA20.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 51.1%.
- Mô hình Logistic đối chứng: 54.5%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 47.1%.
- Mức dừng lỗ tham chiếu 32.30, mục tiêu 1 35.98, tỷ lệ lợi nhuận/rủi ro 6.14.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. News Reader đã trích đoạn có nguồn của 2 bài để phân loại chủ đề (co_tuc_va_hanh_dong_doanh_nghiep: 1, vi_mo: 1), nhưng các trích đoạn này không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Hồi phục / nghiêng tăng; điểm 4. Chi tiết artifact: Xu hướng: Trung tính (Giá trên SMA60 nhưng chưa vượt SMA20.); MACD: Tích cực (MACD trên signal, histogram dương.); RSI14: Tích cực (RSI 59.5.); Bollinger: Ổn định (Giá nằm trong dải Bollinger.); ADX: Xu hướng tăng (ADX 25.1, +DI vượt -DI.); Thanh khoản: Thấp (0.39 lần trung bình.); Stochastic: Yếu lại (%K nằm dưới %D.)
- Góc nhìn cơ bản: Artifact cơ bản: VietinBank; kỳ 2026-Q2; P/E 6.34; P/B 1.28; ROE 21.8%; ROA 1.4%; Debt/Equity 13.79; Revenue Growth 26.1%; Profit Growth 21.4%.
- Tin doanh nghiệp: Đã đọc trích đoạn giới hạn của 2 bài; phân nhóm rule-based: co_tuc_va_hanh_dong_doanh_nghiep: 1, vi_mo: 1. Tác động cần kiểm chứng: Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động. Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh. Đây không phải sentiment hay dự báo tác động giá.
- Live research: Live snapshot lấy lúc 2026-08-11T04:58:17.275639+00:00; News Reader đọc được 2 bài. ML có 5 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest.

### Bằng chứng

- ML decision artifact: NO_EDGE. AUC 0.493 < 0.540
- ML decision artifact: NO_EDGE. Balanced accuracy 0.502 < 0.520
- ML decision artifact: NO_EDGE. XGBoost chưa vượt logistic baseline: AUC XGBoost=0.4930783841040251, AUC logistic=0.49308751552341296
- ML decision artifact: NO_EDGE. Probability 51.1% < 55.0%
- ML decision artifact: NO_EDGE. Lợi thế OOS ròng không đạt: return=-0.059461009999999814, Sharpe=-0.37679650206545323
- News Reader [Fili.vn]: Ngày 11/08/2026: 10 cổ phiếu nóng dưới góc nhìn PTKT của Vietstock - Fili.vn | nhóm: khác (2026-08-11T01:58:00+00:00)
- News Reader [VietnamBiz]: NHNN cần tăng nắm giữ bao nhiêu cổ phiếu CTG để sở hữu tối thiểu 65% VietinBank? - VietnamBiz | nhóm: co_tuc_va_hanh_dong_doanh_nghiep, vi_mo (2026-08-07T08:45:00+00:00)

### Rủi ro cần kiểm chứng

- ML guard: AUC 0.493 < 0.540
- ML guard: Balanced accuracy 0.502 < 0.520
- ML guard: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.4930783841040251, AUC logistic=0.49308751552341296
- ML guard: Probability 51.1% < 55.0%
- ML guard: Lợi thế OOS ròng không đạt: return=-0.059461009999999814, Sharpe=-0.37679650206545323
- News Reader: Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động.
- News Reader: Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh.
- Chỉ lưu trích đoạn giới hạn để kiểm chứng nguồn; không lưu hay hiển thị toàn văn bài báo.
- Phân nhóm là keyword rule-based để định tuyến research, không phải sentiment hay dự báo tác động giá.
- Dữ liệu News Reader chỉ phục vụ research/report; không dùng làm feature train/backtest khi chưa có lịch sử available_at point-in-time.
- Tin live/trích đoạn cần mở URL gốc để kiểm chứng bối cảnh, số liệu và thời điểm trước khi sử dụng.

### Nguồn live research

- [Fili.vn] Ngày 11/08/2026: 10 cổ phiếu nóng dưới góc nhìn PTKT của Vietstock - Fili.vn (2026-08-11T01:58:00+00:00): https://fili.vn/2026/08/ngay-11082026-10-co-phieu-nong-duoi-goc-nhin-ptkt-cua-vietstock-585-1478860.htm
- [VietnamBiz] NHNN cần tăng nắm giữ bao nhiêu cổ phiếu CTG để sở hữu tối thiểu 65% VietinBank? - VietnamBiz (2026-08-07T08:45:00+00:00): https://vietnambiz.vn/nhnn-can-tang-nam-giu-bao-nhieu-co-phieu-ctg-de-so-huu-toi-thieu-65-vietinbank-202687153739946.htm

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.
