# Báo cáo ngày 2026-08-16 - CTS

## Tổng quan

- Dữ liệu: 2009-07-31 -> 2026-08-14, 4,248 phiên.
- Giá đóng cửa: 22.40 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Trung tính (điểm 0).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 52.9%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Model health: INSUFFICIENT_EDGE - Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 7/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định.
- Nếu chưa có cổ phiếu: INSUFFICIENT_EDGE - Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 7/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định.
- Nếu đang nắm giữ: REDUCE - Kỹ thuật chưa hỗ trợ và swing 5D chưa có edge; ưu tiên giảm rủi ro.

## Phân tích kỹ thuật

- SMA20 22.10; SMA60 23.76; RSI14 45.1.
- MACD -0.535; đường tín hiệu -0.709; biểu đồ cột 0.174.
- ATR14 1.07; ATR% 4.8%; ADX14 20.4.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Trung tính - RSI 45.1.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Đi ngang - ADX 20.4.
- Thanh khoản: Bình thường - 0.79 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: Chứng khoán Vietinbank.
- Ngành: Financial Services.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 16.18.
- P/B: 2.13.
- ROE: 13.2%.
- ROA: 3.1%.
- Market cap: 6,098.3 tỷ.
- Revenue Growth: -38.3%.
- Profit Growth: -91.2%.
- P/E 16.18: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 2.13: nên đọc cùng ROE và đặc thù ngành.
- ROA 3.1%: khá tốt, đặc biệt với nhóm ngân hàng.
- Debt/Equity 3.27: đòn bẩy cao, cần đọc theo ngành.
- Current ratio 1.30: thanh khoản ngắn hạn khá.
- Revenue Growth -38.3% YoY.
- Profit Growth -91.2% YoY.
- CFO/LNST 69.76: chất lượng chuyển đổi lợi nhuận sang tiền mặt khá tốt.
- Dòng tiền tự do quý gần nhất dương; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là nợ vay ròng; không dùng một mình để kết luận rủi ro.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.14 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-06T10:34:25+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-12-29 -> 2026-08-13.
- XGBoost: độ chính xác cân bằng 0.542; AUC 0.549; log-loss 0.687.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.528; AUC 0.561.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 101.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.

## Chiến lược swing 5 phiên: contract phát hành tín hiệu

### Khuyến nghị hành động sau phí

| Mục | Kết quả | Diễn giải |
|---|---:|---|
| Lệnh mới hôm nay | 0 lệnh | Không DCA hoặc chia nhỏ lệnh khi fixed-horizon swing chưa qua publish gate. |
| Trạng thái edge 5D | INSUFFICIENT_EDGE | Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 7/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định. |
| Nếu chưa có cổ phiếu | INSUFFICIENT_EDGE | Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 7/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định. |
| Nếu đang nắm giữ | REDUCE | Kỹ thuật chưa hỗ trợ và swing 5D chưa có edge; ưu tiên giảm rủi ro. |
| Expected excess return 5D | +1.0% | Cần vượt chi phí + margin 0.5%. |
| Mẫu frozen holdout | 7/10 trade | Chưa đủ số trade thì không có kết luận lợi nhuận/Sharpe và không được trade live. |
| Kỹ thuật / tin | 0 điểm | Trung tính; news warning: không. |

- Target: signal after close[t]; enter open[t+1]; exit close[t+5] ; target is stock return minus VNINDEX return over the same window
- Expected excess return mới nhất: +1.0%; safety margin đã chọn 0.0%.
- Frozen holdout: 7/10 trade; net/Sharpe chỉ được kết luận khi đủ mẫu.
- Publish gate swing: CHƯA ĐẠT. Gate yêu cầu sample/ranking dương ở development+frozen, net/Sharpe dương và stress phí 1.5×; chưa đạt thì giữ NO_EDGE.
- Các file audit: swing_development_oos.csv, swing_frozen_holdout.csv, swing_development_backtest.csv, swing_frozen_backtest.csv và file trades tương ứng.
- Mức độ quan trọng của đặc trưng: return_1d=10.44; return_3d=10.27; bb_position_20=10.21; return_2d=10.19; relative_strength_20d=9.73; close_vs_sma60=9.30.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 20.79; mục tiêu 1 25.10; mục tiêu 2 27.41.
- Tỷ lệ lợi nhuận/rủi ro 1.50; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- Phương pháp: XGBoost direct quantile 5/10/20D + conformal calibration; toàn bộ horizon qua gate: chưa.
- P50 cuối kỳ 22.88 (2.15%).
- P10/P90 cuối kỳ 18.25 / 27.41.
- Lịch giao dịch: VN stock calendar: loại Thứ Bảy/Chủ Nhật và các ngày nghỉ 2026 đã công bố; ngày làm bù Thứ Bảy không được tính là phiên giao dịch chứng khoán.
- Ngày nghỉ đã loại khỏi forecast: 2026-01-01, 2026-01-02, 2026-02-16, 2026-02-17, 2026-02-18, 2026-02-19, 2026-02-20, 2026-04-27, 2026-04-30, 2026-05-01, 2026-08-31, 2026-09-01, 2026-09-02.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: Không có margin nào đạt số trade tối thiểu trong validation; strict no-entry fallback không phải rule đã chọn..
- Điều kiện phát hành tín hiệu: Frozen holdout chỉ có 7 trade; cần >= 10..
- Điều kiện phát hành tín hiệu: Correlation dự báo-return frozen holdout không dương..
- Điều kiện phát hành tín hiệu: Frozen holdout chưa có lợi thế ròng và Sharpe dương sau phí..
- Điều kiện phát hành tín hiệu: Cận dưới expected excess return -0.047377260483469685 (dự báo điểm 0.009953822940587997) chưa vượt chi phí + margin 0.0050..
- Điều kiện phát hành tín hiệu: Technical score 0 < 2..
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Trung tính.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 52.9%.
- Mô hình Logistic đối chứng: 59.2%.
- Quantile forecast ước tính xác suất return cuối kỳ dương từ residual frozen holdout: 42.1%.
- Mức dừng lỗ tham chiếu 20.79, mục tiêu 1 25.10, tỷ lệ lợi nhuận/rủi ro 1.50.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. Live research lưu 2 headline có URL để theo dõi thêm, nhưng chưa đọc và xác minh toàn văn nên không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Trung tính; điểm 0. Chi tiết artifact: Xu hướng: Cẩn thận (Giá nằm dưới SMA60.); MACD: Tích cực (MACD trên signal, histogram dương.); RSI14: Trung tính (RSI 45.1.); Bollinger: Ổn định (Giá nằm trong dải Bollinger.); ADX: Đi ngang (ADX 20.4.); Thanh khoản: Bình thường (0.79 lần trung bình.); Stochastic: Yếu lại (%K nằm dưới %D.)
- Góc nhìn cơ bản: Artifact cơ bản: Chứng khoán Vietinbank; kỳ 2026-Q2; P/E 16.18; P/B 2.13; ROE 13.2%; ROA 3.1%; Debt/Equity 3.27; Revenue Growth -38.3%; Profit Growth -91.2%.
- Tin doanh nghiệp: Snapshot có 2 headline từ nguồn báo chí. Đây chỉ là danh sách chủ đề cần kiểm chứng; không có nhãn sentiment hoặc dữ liệu nội dung đã xác minh nên không được diễn giải là tin tích cực/tiêu cực.
- Live research: Live snapshot lấy lúc 2026-08-16T05:29:58.702749+00:00; News Reader đọc được 0 bài. ML có 6 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest.

### Bằng chứng

- ML decision artifact: NO_EDGE. Không có margin nào đạt số trade tối thiểu trong validation; strict no-entry fallback không phải rule đã chọn.
- ML decision artifact: NO_EDGE. Frozen holdout chỉ có 7 trade; cần >= 10.
- ML decision artifact: NO_EDGE. Correlation dự báo-return frozen holdout không dương.
- ML decision artifact: NO_EDGE. Frozen holdout chưa có lợi thế ròng và Sharpe dương sau phí.
- ML decision artifact: NO_EDGE. Cận dưới expected excess return -0.047377260483469685 (dự báo điểm 0.009953822940587997) chưa vượt chi phí + margin 0.0050.
- ML decision artifact: NO_EDGE. Technical score 0 < 2.
- Headline [24HMoney]: Cổ phiếu CTS - Có nên mua? Dự phóng lợi nhuận H2/2026 & 2027? - 24HMoney (2026-08-14T02:30:07+00:00)
- Headline [24HMoney]: Cổ phiếu VIX, SHS, CTS, VDS - Có nên mua? Nhóm TỰ DOANH CHỨNG KHOÁN có lãi trong năm 2026? - 24HMoney (2026-08-10T01:40:54+00:00)

### Rủi ro cần kiểm chứng

- ML guard: Không có margin nào đạt số trade tối thiểu trong validation; strict no-entry fallback không phải rule đã chọn.
- ML guard: Frozen holdout chỉ có 7 trade; cần >= 10.
- ML guard: Correlation dự báo-return frozen holdout không dương.
- ML guard: Frozen holdout chưa có lợi thế ròng và Sharpe dương sau phí.
- ML guard: Cận dưới expected excess return -0.047377260483469685 (dự báo điểm 0.009953822940587997) chưa vượt chi phí + margin 0.0050.
- ML guard: Technical score 0 < 2.
- Chỉ lưu trích đoạn giới hạn để kiểm chứng nguồn; không lưu hay hiển thị toàn văn bài báo.
- Phân nhóm là keyword rule-based để định tuyến research, không phải sentiment hay dự báo tác động giá.
- Dữ liệu News Reader chỉ phục vụ research/report; không dùng làm feature train/backtest khi chưa có lịch sử available_at point-in-time.
- Tin live/trích đoạn cần mở URL gốc để kiểm chứng bối cảnh, số liệu và thời điểm trước khi sử dụng.

### Nguồn live research

- [24HMoney] Cổ phiếu CTS - Có nên mua? Dự phóng lợi nhuận H2/2026 & 2027? - 24HMoney (2026-08-14T02:30:07+00:00): https://news.google.com/rss/articles/CBMingFBVV95cUxQSGwxY3o3X2pqZnJia00xUUtreDlRVl9lTkhDQXhBaVlVci16NDRHaEY1eDZJdjFWVTJuOTQ1V3NVbk1uMEFtMEpvd2U4a1RRUnRmTkdZM09BbkpYZ2tPcUNld2ZUTDVDbzVLQjQtYWtPZzF6bFV4VzNJbVF6OXZVZEJOSzRCYlB2ZU9VUTRNSWhpOVBfYlJnMEluOFBpZw?oc=5
- [24HMoney] Cổ phiếu VIX, SHS, CTS, VDS - Có nên mua? Nhóm TỰ DOANH CHỨNG KHOÁN có lãi trong năm 2026? - 24HMoney (2026-08-10T01:40:54+00:00): https://news.google.com/rss/articles/CBMiwwFBVV95cUxObnlyTVdYbExxMFNmelp0SGtaVDRUZFVUXzUtVUYxaEN6Zmo3eHk5dTZyQ3M1bGhUNzRUaEI5OFFtcTlDYWVEQl9qWTNvUktSaUNZV3ZnVDlHMHJPdkVOcG5Tam91X1NGdW1wSXloUTFlSzBmU1czMFNvQm5tcWpnSFU5U19LeDh1Znk2MnpPal94NzhEemZtVWxwSnNPYTNYYjNZVGlBS2wtTHd1WTFRMURoaXAyNVg3c2ZuLUdIV1g2WHM?oc=5

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.

---

## News model riêng từng mã

- Symbol-news report: `/Users/tranlekhoa/Documents/DATA_SCI/vn_stock_analysis/reports/CTS/2026-08-16_12-29-43/all_files/symbol_news_model`
- Số bài tin trong CSV cho mã: 0
- Số dòng giá có news feature: 0
- XGBoost probability mới nhất: 0.517
- AUC OOS: 0.561
- Balanced accuracy OOS: 0.533
- Backtest total return: 0.000
- Base XGBoost probability: 0.529
- Chênh lệch News-adjusted - Base: -0.012
- Áp vào signal chính: not_applied
- Trạng thái news model: research_only
- Gate chưa đạt: min_articles_60, min_feature_rows_30, news_feature_gain_positive

News-adjusted model hiện là lớp kiểm chứng/shadow; signal chính vẫn do `signal_decision.json` quyết định.

Lưu ý: news model dùng dữ liệu `available_at` point-in-time trong CSV tích lũy; nếu lịch sử tin còn mỏng thì chỉ xem là research/smoke test.
