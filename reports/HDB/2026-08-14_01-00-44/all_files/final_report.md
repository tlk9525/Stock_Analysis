# Báo cáo ngày 2026-08-14 - HDB

## Tổng quan

- Dữ liệu: 2018-01-05 -> 2026-08-13, 2,145 phiên.
- Giá đóng cửa: 26.70 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng (điểm 4).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 48.4%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Model health: INSUFFICIENT_EDGE - Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 5/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định.
- Nếu chưa có cổ phiếu: INSUFFICIENT_EDGE - Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 5/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định.
- Nếu đang nắm giữ: HOLD_DISCIPLINED - Nếu đã nắm giữ: giữ theo stop-loss, không mua thêm khi swing 5D chưa đủ edge.

## Phân tích kỹ thuật

- SMA20 26.28; SMA60 26.07; RSI14 53.7.
- MACD 0.161; đường tín hiệu 0.054; biểu đồ cột 0.107.
- ATR14 0.67; ATR% 2.5%; ADX14 18.6.
- Xu hướng: Tích cực - Giá nằm trên SMA20 và SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Trung tính - RSI 53.7.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Đi ngang - ADX 18.6.
- Thanh khoản: Bình thường - 0.96 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: HDBank.
- Ngành: Banks.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 6.98.
- P/B: 1.59.
- ROE: 23.9%.
- ROA: 2.0%.
- Market cap: 136,143.5 tỷ.
- Revenue Growth: 9.4%.
- Profit Growth: 58.1%.
- P/E 6.98: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 1.59: nên đọc cùng ROE và đặc thù ngành.
- ROE 23.9%: hiệu quả vốn chủ sở hữu tốt.
- ROA 2.0%: khá tốt, đặc biệt với nhóm ngân hàng.
- Debt/Equity 10.59: đòn bẩy cao, cần đọc theo ngành.
- NPL 2.8%: cần theo dõi.
- Revenue Growth 9.4% YoY.
- Profit Growth 58.1% YoY.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.14 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-10T06:25:10+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-10-20 -> 2026-08-12.
- XGBoost: độ chính xác cân bằng 0.517; AUC 0.519; log-loss 0.695.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.514; AUC 0.526.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 31.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.

## Chiến lược swing 5 phiên: contract phát hành tín hiệu

### Khuyến nghị hành động sau phí

| Mục | Kết quả | Diễn giải |
|---|---:|---|
| Lệnh mới hôm nay | 0 lệnh | Không DCA hoặc chia nhỏ lệnh khi fixed-horizon swing chưa qua publish gate. |
| Trạng thái edge 5D | INSUFFICIENT_EDGE | Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 5/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định. |
| Nếu chưa có cổ phiếu | INSUFFICIENT_EDGE | Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 5/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định. |
| Nếu đang nắm giữ | HOLD_DISCIPLINED | Nếu đã nắm giữ: giữ theo stop-loss, không mua thêm khi swing 5D chưa đủ edge. |
| Expected excess return 5D | +0.2% | Cần vượt chi phí + margin 1.0%. |
| Mẫu frozen holdout | 5/10 trade | Chưa đủ số trade thì không có kết luận lợi nhuận/Sharpe và không được trade live. |
| Kỹ thuật / tin | 4 điểm | Hồi phục / nghiêng tăng; news warning: không. |

- Target: signal after close[t]; enter open[t+1]; exit close[t+5] ; target is stock return minus VNINDEX return over the same window
- Expected excess return mới nhất: +0.2%; safety margin đã chọn 0.5%.
- Frozen holdout: 5/10 trade; net/Sharpe chỉ được kết luận khi đủ mẫu.
- Publish gate swing: CHƯA ĐẠT. Gate yêu cầu sample/ranking dương ở development+frozen, net/Sharpe dương và stress phí 1.5×; chưa đạt thì giữ NO_EDGE.
- Các file audit: swing_development_oos.csv, swing_frozen_holdout.csv, swing_development_backtest.csv, swing_frozen_backtest.csv và file trades tương ứng.
- Mức độ quan trọng của đặc trưng: relative_strength_20d=12.14; close_vs_sma20=10.01; return_2d=8.96; macd_hist_pct=8.90; return_1d=8.71; close_vs_sma60=8.45.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 25.81; mục tiêu 1 29.30; mục tiêu 2 29.30.
- Tỷ lệ lợi nhuận/rủi ro 2.41; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- Phương pháp: XGBoost direct quantile 5/10/20D + conformal calibration; toàn bộ horizon qua gate: có.
- P50 cuối kỳ 26.96 (0.96%).
- P10/P90 cuối kỳ 24.66 / 29.30.
- Lịch giao dịch: VN stock calendar: loại Thứ Bảy/Chủ Nhật và các ngày nghỉ 2026 đã công bố; ngày làm bù Thứ Bảy không được tính là phiên giao dịch chứng khoán.
- Ngày nghỉ đã loại khỏi forecast: 2026-01-01, 2026-01-02, 2026-02-16, 2026-02-17, 2026-02-18, 2026-02-19, 2026-02-20, 2026-04-27, 2026-04-30, 2026-05-01, 2026-08-31, 2026-09-01, 2026-09-02.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: Không có margin nào đạt số trade tối thiểu trong validation; strict no-entry fallback không phải rule đã chọn..
- Điều kiện phát hành tín hiệu: Frozen holdout chỉ có 5 trade; cần >= 10..
- Điều kiện phát hành tín hiệu: Cận dưới expected excess return -0.03314973420347633 (dự báo điểm 0.001553021022118628) chưa vượt chi phí + margin 0.0100..
- Xu hướng ngắn hạn thuận: giá trên SMA20 và SMA60.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 48.4%.
- Mô hình Logistic đối chứng: 47.6%.
- Quantile forecast ước tính xác suất return cuối kỳ dương từ residual frozen holdout: 54.8%.
- Mức dừng lỗ tham chiếu 25.81, mục tiêu 1 29.30, tỷ lệ lợi nhuận/rủi ro 2.41.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. Live research lưu 2 headline có URL để theo dõi thêm, nhưng chưa đọc và xác minh toàn văn nên không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Hồi phục / nghiêng tăng; điểm 4. Chi tiết artifact: Xu hướng: Tích cực (Giá nằm trên SMA20 và SMA60.); MACD: Tích cực (MACD trên signal, histogram dương.); RSI14: Trung tính (RSI 53.7.); Bollinger: Ổn định (Giá nằm trong dải Bollinger.); ADX: Đi ngang (ADX 18.6.); Thanh khoản: Bình thường (0.96 lần trung bình.); Stochastic: Yếu lại (%K nằm dưới %D.)
- Góc nhìn cơ bản: Artifact cơ bản: HDBank; kỳ 2026-Q2; P/E 6.98; P/B 1.59; ROE 23.9%; ROA 2.0%; Debt/Equity 10.59; Revenue Growth 9.4%; Profit Growth 58.1%.
- Tin doanh nghiệp: Snapshot có 2 headline từ nguồn báo chí. Đây chỉ là danh sách chủ đề cần kiểm chứng; không có nhãn sentiment hoặc dữ liệu nội dung đã xác minh nên không được diễn giải là tin tích cực/tiêu cực.
- Live research: Live snapshot lấy lúc 2026-08-13T18:01:02.549503+00:00; News Reader đọc được 0 bài. ML có 3 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest.

### Bằng chứng

- ML decision artifact: NO_EDGE. Không có margin nào đạt số trade tối thiểu trong validation; strict no-entry fallback không phải rule đã chọn.
- ML decision artifact: NO_EDGE. Frozen holdout chỉ có 5 trade; cần >= 10.
- ML decision artifact: NO_EDGE. Cận dưới expected excess return -0.03314973420347633 (dự báo điểm 0.001553021022118628) chưa vượt chi phí + margin 0.0100.
- Headline [CafeF]: VN-Index tiến sát 1.800 điểm, thêm cổ phiếu ngân hàng lên sàn - CafeF (2026-08-12T09:35:00+00:00)
- Headline [CafeF]: Mới nhất: 9 cổ phiếu "hot" có thể lọt rổ FTSE GEIS trong kỳ nâng hạng tháng 9 - CafeF (2026-08-07T06:17:00+00:00)

### Rủi ro cần kiểm chứng

- ML guard: Không có margin nào đạt số trade tối thiểu trong validation; strict no-entry fallback không phải rule đã chọn.
- ML guard: Frozen holdout chỉ có 5 trade; cần >= 10.
- ML guard: Cận dưới expected excess return -0.03314973420347633 (dự báo điểm 0.001553021022118628) chưa vượt chi phí + margin 0.0100.
- Chỉ lưu trích đoạn giới hạn để kiểm chứng nguồn; không lưu hay hiển thị toàn văn bài báo.
- Phân nhóm là keyword rule-based để định tuyến research, không phải sentiment hay dự báo tác động giá.
- Dữ liệu News Reader chỉ phục vụ research/report; không dùng làm feature train/backtest khi chưa có lịch sử available_at point-in-time.
- Tin live/trích đoạn cần mở URL gốc để kiểm chứng bối cảnh, số liệu và thời điểm trước khi sử dụng.

### Nguồn live research

- [CafeF] VN-Index tiến sát 1.800 điểm, thêm cổ phiếu ngân hàng lên sàn - CafeF (2026-08-12T09:35:00+00:00): https://news.google.com/rss/articles/CBMioAFBVV95cUxOLUpMVjF2MF9ZS29seHczYkpnMHlNa1FkV2dWekt2VzltaHhaaWdpbExWeFl0SXBheHJiVzdNZFdFeE41V0txZGN6T0JnMzZxcm9sOVYwRE82UDJxOVVPREdmSlBCaGJ0QnhEQTNXZWY4WGpnby1nMFJBYlZLM2RoUGpLc1pEVjRIYV8xSUI0a0NaalJyRk1zMmhvVXh6RHlY?oc=5
- [CafeF] Mới nhất: 9 cổ phiếu "hot" có thể lọt rổ FTSE GEIS trong kỳ nâng hạng tháng 9 - CafeF (2026-08-07T06:17:00+00:00): https://news.google.com/rss/articles/CBMitAFBVV95cUxPWHYzbTkxZlozSnZXZjlZUGk1cHlGLWFjLUdvWVliOWEwVU1EQ3l0UEt2NWRfV1FxUXR0bTQ3UnMtT2hyVVF0VWlkZlZWUmtBa2VZeEVGNkRTQk1QT0lhRXFQeDdHdmphUjBkQ0dtY3VQRXlaWVlvUzduWDAzdXFpNUtweGlVZHh3cUF5bWRPRzllVXoyOG0yNXEzaDNzcEpUa3dNNHRoZXczVk1XTHE3UlVpRVA?oc=5

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.

---

## News model riêng từng mã

- Symbol-news report: `/Users/tranlekhoa/Documents/DATA_SCI/vn_stock_analysis/reports/HDB/2026-08-14_01-00-44/all_files/symbol_news_model`
- Số bài tin trong CSV cho mã: 0
- Số dòng giá có news feature: 0
- XGBoost probability mới nhất: 0.481
- AUC OOS: 0.512
- Balanced accuracy OOS: 0.493
- Backtest total return: 0.000
- Base XGBoost probability: 0.484
- Chênh lệch News-adjusted - Base: -0.003
- Áp vào signal chính: not_applied
- Trạng thái news model: research_only
- Gate chưa đạt: min_articles_60, min_feature_rows_30, news_feature_gain_positive, auc_at_least_0_55, balanced_accuracy_at_least_0_52

News-adjusted model hiện là lớp kiểm chứng/shadow; signal chính vẫn do `signal_decision.json` quyết định.

Lưu ý: news model dùng dữ liệu `available_at` point-in-time trong CSV tích lũy; nếu lịch sử tin còn mỏng thì chỉ xem là research/smoke test.
