# Báo cáo ngày 2026-08-11 - NVL

## Tổng quan

- Dữ liệu: 2016-12-28 -> 2026-08-11, 2,399 phiên.
- Giá đóng cửa: 13.85 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng (điểm 4).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 51.7%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 13.04; SMA60 13.07; RSI14 64.4.
- MACD 0.286; đường tín hiệu 0.150; biểu đồ cột 0.136.
- ATR14 0.52; ATR% 3.7%; ADX14 28.4.
- Xu hướng: Trung tính - Giá trên SMA60 nhưng chưa vượt SMA20.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 64.4.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng tăng - ADX 28.4, +DI vượt -DI.
- Thanh khoản: Thấp - 0.37 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: Novaland.
- Ngành: Real Estate.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 7.51.
- P/B: 0.69.
- ROE: 9.5%.
- ROA: 1.7%.
- Market cap: 33,388.7 tỷ.
- Revenue Growth: -22.1%.
- P/E 7.51: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 0.69: nên đọc cùng ROE và đặc thù ngành.
- Debt/Equity 2.96: đòn bẩy cao, cần đọc theo ngành.
- Current ratio 2.12: thanh khoản ngắn hạn khá.
- Revenue Growth -22.1% YoY.
- CFO/LNST -3.46: dòng tiền chưa theo kịp lợi nhuận, cần đọc thêm biến động vốn lưu động.
- Dòng tiền tự do quý gần nhất âm; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là nợ vay ròng; không dùng một mình để kết luận rủi ro.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.14 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-06T10:14:03+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-10-17 -> 2026-08-10.
- XGBoost: độ chính xác cân bằng 0.497; AUC 0.534; log-loss 0.685.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.505; AUC 0.516.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 45.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -31.5%; Sharpe -0.90; mức sụt giảm tối đa -42.2%.
- Mức độ quan trọng của đặc trưng: macd_pct=11.05; market_return_1d=10.57; adx_14=9.65; relative_strength_20d=9.53; beta_60d=9.39; rsi_14=8.66.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 13.07; mục tiêu 1 16.63; mục tiêu 2 16.63.
- Tỷ lệ lợi nhuận/rủi ro 3.20; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 13.58 (-1.97%).
- P10/P90 cuối kỳ 11.44 / 16.63.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.534 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.497 < 0.520.
- Điều kiện phát hành tín hiệu: Probability 51.7% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.31516711, Sharpe=-0.9016851255892111.
- Trung hạn chưa xấu, ngắn hạn yếu vì giá dưới SMA20.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 51.7%.
- Mô hình Logistic đối chứng: 51.0%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 44.1%.
- Mức dừng lỗ tham chiếu 13.07, mục tiêu 1 16.63, tỷ lệ lợi nhuận/rủi ro 3.20.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. News Reader đã trích đoạn có nguồn của 3 bài để phân loại chủ đề (ket_qua_kinh_doanh: 3), nhưng các trích đoạn này không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Hồi phục / nghiêng tăng; điểm 4. Chi tiết artifact: Xu hướng: Trung tính (Giá trên SMA60 nhưng chưa vượt SMA20.); MACD: Tích cực (MACD trên signal, histogram dương.); RSI14: Tích cực (RSI 64.4.); Bollinger: Ổn định (Giá nằm trong dải Bollinger.); ADX: Xu hướng tăng (ADX 28.4, +DI vượt -DI.); Thanh khoản: Thấp (0.37 lần trung bình.); Stochastic: Yếu lại (%K nằm dưới %D.)
- Góc nhìn cơ bản: Artifact cơ bản: Novaland; kỳ 2026-Q2; P/E 7.51; P/B 0.69; ROE 9.5%; ROA 1.7%; Debt/Equity 2.96; Revenue Growth -22.1%.
- Tin doanh nghiệp: Đã đọc trích đoạn giới hạn của 3 bài; phân nhóm rule-based: ket_qua_kinh_doanh: 3. Tác động cần kiểm chứng: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường. Đây không phải sentiment hay dự báo tác động giá.
- Live research: Live snapshot lấy lúc 2026-08-11T05:06:16.437027+00:00; News Reader đọc được 3 bài. ML có 4 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest.

### Bằng chứng

- ML decision artifact: NO_EDGE. AUC 0.534 < 0.540
- ML decision artifact: NO_EDGE. Balanced accuracy 0.497 < 0.520
- ML decision artifact: NO_EDGE. Probability 51.7% < 55.0%
- ML decision artifact: NO_EDGE. Lợi thế OOS ròng không đạt: return=-0.31516711, Sharpe=-0.9016851255892111
- News Reader [nguoiquansat.vn]: Cổ phiếu Novaland (NVL) nối dài đà tăng bất chấp sức ép bán ròng của khối ngoại - nguoiquansat.vn | nhóm: ket_qua_kinh_doanh (2026-08-06T05:45:01+00:00)
- News Reader [24HMoney]: Đánh giá tiềm năng cổ phiếu NVL (Novaland) - 24HMoney | nhóm: ket_qua_kinh_doanh (2026-08-04T08:54:30+00:00)
- News Reader [nguoiquansat.vn]: Nợ vay lập kỷ lục, Novaland (NVL) huy động hơn 8.000 tỷ đồng từ cổ đông để thanh toán - nguoiquansat.vn | nhóm: ket_qua_kinh_doanh (2026-08-07T02:51:01+00:00)

### Rủi ro cần kiểm chứng

- ML guard: AUC 0.534 < 0.540
- ML guard: Balanced accuracy 0.497 < 0.520
- ML guard: Probability 51.7% < 55.0%
- ML guard: Lợi thế OOS ròng không đạt: return=-0.31516711, Sharpe=-0.9016851255892111
- News Reader: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường.
- Chỉ lưu trích đoạn giới hạn để kiểm chứng nguồn; không lưu hay hiển thị toàn văn bài báo.
- Phân nhóm là keyword rule-based để định tuyến research, không phải sentiment hay dự báo tác động giá.
- Dữ liệu News Reader chỉ phục vụ research/report; không dùng làm feature train/backtest khi chưa có lịch sử available_at point-in-time.
- Tin live/trích đoạn cần mở URL gốc để kiểm chứng bối cảnh, số liệu và thời điểm trước khi sử dụng.

### Nguồn live research

- [nguoiquansat.vn] Cổ phiếu Novaland (NVL) nối dài đà tăng bất chấp sức ép bán ròng của khối ngoại - nguoiquansat.vn (2026-08-06T05:45:01+00:00): https://nguoiquansat.vn/co-phieu-novaland-nvl-noi-dai-da-tang-bat-chap-suc-ep-ban-rong-cua-khoi-ngoai-308808.html
- [24HMoney] Đánh giá tiềm năng cổ phiếu NVL (Novaland) - 24HMoney (2026-08-04T08:54:30+00:00): https://24hmoney.vn/news/danh-gia-tiem-nang-co-phieu-nvl-novaland-c30a2816353.html
- [nguoiquansat.vn] Nợ vay lập kỷ lục, Novaland (NVL) huy động hơn 8.000 tỷ đồng từ cổ đông để thanh toán - nguoiquansat.vn (2026-08-07T02:51:01+00:00): https://nguoiquansat.vn/no-vay-lap-ky-luc-novaland-nvl-huy-dong-hon-8-000-ty-dong-tu-co-dong-de-thanh-toan-308998.html

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.
