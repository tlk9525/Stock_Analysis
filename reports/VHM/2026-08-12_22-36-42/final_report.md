# Báo cáo ngày 2026-08-12 - VHM

## Tổng quan

- Dữ liệu: 2011-11-10 -> 2026-08-12, 2,162 phiên.
- Giá đóng cửa: 73.80 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng (điểm 4).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 51.7%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 70.84; SMA60 72.13; RSI14 54.1.
- MACD 0.687; đường tín hiệu 0.358; biểu đồ cột 0.329.
- ATR14 3.17; ATR% 4.3%; ADX14 23.3.
- Xu hướng: Trung tính - Giá trên SMA60 nhưng chưa vượt SMA20.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Trung tính - RSI 54.1.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Đi ngang - ADX 23.3.
- Thanh khoản: Bình thường - 1.05 lần trung bình.
- Stochastic: Hồi phục - %K nằm trên %D.

## Phân tích cơ bản

- Doanh nghiệp: Vinhomes.
- Ngành: Real Estate.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 7.42.
- P/B: 2.28.
- ROE: 32.7%.
- ROA: 9.0%.
- Market cap: 592,288.8 tỷ.
- Revenue Growth: 177.8%.
- Profit Growth: 200.8%.
- P/E 7.42: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 2.28: nên đọc cùng ROE và đặc thù ngành.
- ROE 32.7%: hiệu quả vốn chủ sở hữu tốt.
- ROA 9.0%: khá tốt, đặc biệt với nhóm ngân hàng.
- Debt/Equity 3.05: đòn bẩy cao, cần đọc theo ngành.
- Current ratio 1.17: thanh khoản ngắn hạn khá.
- Revenue Growth 177.8% YoY.
- Profit Growth 200.8% YoY.
- CFO/LNST 1.97: chất lượng chuyển đổi lợi nhuận sang tiền mặt khá tốt.
- Dòng tiền tự do quý gần nhất dương; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là nợ vay ròng; không dùng một mình để kết luận rủi ro.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.12 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-10T03:53:05+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-10-19 -> 2026-08-11.
- XGBoost: độ chính xác cân bằng 0.530; AUC 0.523; log-loss 0.696.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.530; AUC 0.546.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 25.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận 29.9%; Sharpe 0.73; mức sụt giảm tối đa -14.7%.
- Mức độ quan trọng của đặc trưng: range_pct=11.73; market_volatility_20d=11.67; atr_pct_14=11.25; market_return_1d=10.36; day_of_week=9.99; return_1d=9.86.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 71.41; mục tiêu 1 81.70; mục tiêu 2 91.49.
- Tỷ lệ lợi nhuận/rủi ro 2.73; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 72.78 (-1.39%).
- P10/P90 cuối kỳ 58.76 / 91.49.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.523 < 0.540.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5234451573580647, AUC logistic=0.5461613857064023.
- Điều kiện phát hành tín hiệu: Probability 51.7% < 55.0%.
- Trung hạn chưa xấu, ngắn hạn yếu vì giá dưới SMA20.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 51.7%.
- Mô hình Logistic đối chứng: 48.5%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 46.8%.
- Mức dừng lỗ tham chiếu 71.41, mục tiêu 1 81.70, tỷ lệ lợi nhuận/rủi ro 2.73.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. News Reader đã trích đoạn có nguồn của 3 bài để phân loại chủ đề (nganh: 1), nhưng các trích đoạn này không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Hồi phục / nghiêng tăng; điểm 4. Chi tiết artifact: Xu hướng: Trung tính (Giá trên SMA60 nhưng chưa vượt SMA20.); MACD: Tích cực (MACD trên signal, histogram dương.); RSI14: Trung tính (RSI 54.1.); Bollinger: Ổn định (Giá nằm trong dải Bollinger.); ADX: Đi ngang (ADX 23.3.); Thanh khoản: Bình thường (1.05 lần trung bình.); Stochastic: Hồi phục (%K nằm trên %D.)
- Góc nhìn cơ bản: Artifact cơ bản: Vinhomes; kỳ 2026-Q2; P/E 7.42; P/B 2.28; ROE 32.7%; ROA 9.0%; Debt/Equity 3.05; Revenue Growth 177.8%; Profit Growth 200.8%.
- Tin doanh nghiệp: Đã đọc trích đoạn giới hạn của 3 bài; phân nhóm rule-based: nganh: 1. Tác động cần kiểm chứng: So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp. Đây không phải sentiment hay dự báo tác động giá.
- Live research: Live snapshot lấy lúc 2026-08-12T15:37:06.085695+00:00; News Reader đọc được 3 bài. ML có 3 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest.

### Bằng chứng

- ML decision artifact: NO_EDGE. AUC 0.523 < 0.540
- ML decision artifact: NO_EDGE. XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5234451573580647, AUC logistic=0.5461613857064023
- ML decision artifact: NO_EDGE. Probability 51.7% < 55.0%
- News Reader [nguoiquansat.vn]: Vingroup chuyển nhượng gần 5 triệu cổ phiếu VHM - nguoiquansat.vn | nhóm: khác (2026-08-10T08:50:01+00:00)
- News Reader [VietnamBiz]: Vingroup chuyển nhượng hơn 4,8 triệu cổ phiếu VHM - VietnamBiz | nhóm: khác (2026-08-10T08:10:00+00:00)
- News Reader [Fili.vn]: Nhịp đập Thị trường 10/08: Cổ phiếu VIC và VHM kìm hãm đà phục hồi của VN-Index - Fili.vn | nhóm: nganh (2026-08-10T09:13:31+00:00)

### Rủi ro cần kiểm chứng

- ML guard: AUC 0.523 < 0.540
- ML guard: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5234451573580647, AUC logistic=0.5461613857064023
- ML guard: Probability 51.7% < 55.0%
- News Reader: So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp.
- Chỉ lưu trích đoạn giới hạn để kiểm chứng nguồn; không lưu hay hiển thị toàn văn bài báo.
- Phân nhóm là keyword rule-based để định tuyến research, không phải sentiment hay dự báo tác động giá.
- Dữ liệu News Reader chỉ phục vụ research/report; không dùng làm feature train/backtest khi chưa có lịch sử available_at point-in-time.
- Tin live/trích đoạn cần mở URL gốc để kiểm chứng bối cảnh, số liệu và thời điểm trước khi sử dụng.

### Nguồn live research

- [nguoiquansat.vn] Vingroup chuyển nhượng gần 5 triệu cổ phiếu VHM - nguoiquansat.vn (2026-08-10T08:50:01+00:00): https://nguoiquansat.vn/vingroup-chuyen-nhuong-gan-5-trieu-co-phieu-vhm-309619.html
- [VietnamBiz] Vingroup chuyển nhượng hơn 4,8 triệu cổ phiếu VHM - VietnamBiz (2026-08-10T08:10:00+00:00): https://vietnambiz.vn/vingroup-chuyen-nhuong-hon-48-trieu-co-phieu-vhm-202681014242741.htm
- [Fili.vn] Nhịp đập Thị trường 10/08: Cổ phiếu VIC và VHM kìm hãm đà phục hồi của VN-Index - Fili.vn (2026-08-10T09:13:31+00:00): https://fili.vn/2026/08/nhip-dap-thi-truong-1008-co-phieu-vic-va-vhm-kim-ham-da-phuc-hoi-cua-vn-index-1636-1478504.htm

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.

---

## News model riêng từng mã

- Symbol-news report: `/Users/tranlekhoa/Documents/DATA_SCI/vn_stock_analysis/reports/VHM/2026-08-12_22-37-28_news_model`
- Số bài tin trong CSV cho mã: 10
- Số dòng giá có news feature: 5
- XGBoost probability mới nhất: 0.503
- AUC OOS: 0.533
- Balanced accuracy OOS: 0.520
- Backtest total return: 0.314

Lưu ý: news model dùng dữ liệu `available_at` point-in-time trong CSV tích lũy; nếu lịch sử tin còn mỏng thì chỉ xem là research/smoke test.
