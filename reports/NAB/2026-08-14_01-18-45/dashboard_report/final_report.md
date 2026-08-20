# Báo cáo ngày 2026-08-14 - NAB

## Tổng quan

- Dữ liệu: 2020-10-09 -> 2026-08-13, 1,450 phiên.
- Giá đóng cửa: 11.75 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Tiêu cực (điểm -7).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 49.9%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Model health: INSUFFICIENT_EDGE - Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 0/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định.
- Nếu chưa có cổ phiếu: INSUFFICIENT_EDGE - Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 0/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định.
- Nếu đang nắm giữ: REDUCE - Kỹ thuật chưa hỗ trợ và swing 5D chưa có edge; ưu tiên giảm rủi ro.

## Phân tích kỹ thuật

- SMA20 12.18; SMA60 12.46; RSI14 36.1.
- MACD -0.225; đường tín hiệu -0.192; biểu đồ cột -0.033.
- ATR14 0.34; ATR% 2.9%; ADX14 29.9.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Cẩn thận - MACD dưới signal, histogram âm.
- RSI14: Yếu - RSI 36.1.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng giảm - ADX 29.9, -DI vượt +DI.
- Thanh khoản: Bình thường - 0.84 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: Ngân hàng Nam Á.
- Ngành: Banks.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 5.25.
- P/B: 0.96.
- ROE: 19.5%.
- ROA: 1.1%.
- Market cap: 25,690.0 tỷ.
- Revenue Growth: 4.6%.
- Profit Growth: 16.9%.
- P/E 5.25: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 0.96: nên đọc cùng ROE và đặc thù ngành.
- ROE 19.5%: hiệu quả vốn chủ sở hữu tốt.
- Debt/Equity 16.44: đòn bẩy cao, cần đọc theo ngành.
- NPL 1.5%: đang ở mức kiểm soát.
- Revenue Growth 4.6% YoY.
- Profit Growth 16.9% YoY.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.14 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-10T08:27:16+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2024-10-31 -> 2026-08-12.
- XGBoost: độ chính xác cân bằng 0.500; AUC 0.513; log-loss 0.700.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.513; AUC 0.517.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 5.
- Thẩm định: expanding_walk_forward; 4 lần chia; khoảng cách 1 phiên.

## Chiến lược swing 5 phiên: contract phát hành tín hiệu

### Khuyến nghị hành động sau phí

| Mục | Kết quả | Diễn giải |
|---|---:|---|
| Lệnh mới hôm nay | 0 lệnh | Không DCA hoặc chia nhỏ lệnh khi fixed-horizon swing chưa qua publish gate. |
| Trạng thái edge 5D | INSUFFICIENT_EDGE | Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 0/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định. |
| Nếu chưa có cổ phiếu | INSUFFICIENT_EDGE | Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 0/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định. |
| Nếu đang nắm giữ | REDUCE | Kỹ thuật chưa hỗ trợ và swing 5D chưa có edge; ưu tiên giảm rủi ro. |
| Expected excess return 5D | +0.3% | Cần vượt chi phí + margin 0.9%. |
| Mẫu frozen holdout | 0/10 trade | Chưa đủ số trade thì không có kết luận lợi nhuận/Sharpe và không được trade live. |
| Kỹ thuật / tin | -7 điểm | Tiêu cực; news warning: không. |

- Target: signal after close[t]; enter open[t+1]; exit close[t+5] ; target is stock return minus VNINDEX return over the same window
- Expected excess return mới nhất: +0.3%; safety margin đã chọn 0.4%.
- Frozen holdout: 0/10 trade; net/Sharpe chỉ được kết luận khi đủ mẫu.
- Publish gate swing: CHƯA ĐẠT. Gate yêu cầu sample/ranking dương ở development+frozen, net/Sharpe dương và stress phí 1.5×; chưa đạt thì giữ NO_EDGE.
- Các file audit: swing_development_oos.csv, swing_frozen_holdout.csv, swing_development_backtest.csv, swing_frozen_backtest.csv và file trades tương ứng.
- Mức độ quan trọng của đặc trưng: stoch_k_14=18.93; excess_return_5d=16.69; rsi_14=15.28; market_return_20d=12.61; market_return_1d=12.16; corr_60d=11.88.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 11.29; mục tiêu 1 13.05; mục tiêu 2 13.19.
- Tỷ lệ lợi nhuận/rủi ro 2.37; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- Phương pháp: XGBoost direct quantile 5/10/20D + conformal calibration; toàn bộ horizon qua gate: chưa.
- P50 cuối kỳ 11.91 (1.40%).
- P10/P90 cuối kỳ 10.65 / 13.19.
- Lịch giao dịch: VN stock calendar: loại Thứ Bảy/Chủ Nhật và các ngày nghỉ 2026 đã công bố; ngày làm bù Thứ Bảy không được tính là phiên giao dịch chứng khoán.
- Ngày nghỉ đã loại khỏi forecast: 2026-01-01, 2026-01-02, 2026-02-16, 2026-02-17, 2026-02-18, 2026-02-19, 2026-02-20, 2026-04-27, 2026-04-30, 2026-05-01, 2026-08-31, 2026-09-01, 2026-09-02.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: Development OOS chỉ có 1 trade; cần >= 10..
- Điều kiện phát hành tín hiệu: Frozen holdout chỉ có 0 trade; cần >= 10..
- Điều kiện phát hành tín hiệu: Correlation dự báo-return development OOS không dương..
- Điều kiện phát hành tín hiệu: Correlation dự báo-return frozen holdout không dương..
- Điều kiện phát hành tín hiệu: Frozen holdout chưa có lợi thế ròng và Sharpe dương sau phí..
- Điều kiện phát hành tín hiệu: Frozen holdout không chịu được stress phí 1.5x..
- Điều kiện phát hành tín hiệu: Cận dưới expected excess return -0.03830378960797731 (dự báo điểm 0.002874567173421383) chưa vượt chi phí + margin 0.0088..
- Điều kiện phát hành tín hiệu: Technical score -7 < 2..
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Tiêu cực.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 49.9%.
- Mô hình Logistic đối chứng: 44.9%.
- Quantile forecast ước tính xác suất return cuối kỳ dương từ residual frozen holdout: 42.9%.
- Mức dừng lỗ tham chiếu 11.29, mục tiêu 1 13.05, tỷ lệ lợi nhuận/rủi ro 2.37.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. Chưa có live research hoặc News Reader được lưu cho report này.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Tiêu cực; điểm -7. Chi tiết artifact: Xu hướng: Cẩn thận (Giá nằm dưới SMA60.); MACD: Cẩn thận (MACD dưới signal, histogram âm.); RSI14: Yếu (RSI 36.1.); Bollinger: Ổn định (Giá nằm trong dải Bollinger.); ADX: Xu hướng giảm (ADX 29.9, -DI vượt +DI.); Thanh khoản: Bình thường (0.84 lần trung bình.); Stochastic: Yếu lại (%K nằm dưới %D.)
- Góc nhìn cơ bản: Artifact cơ bản: Ngân hàng Nam Á; kỳ 2026-Q2; P/E 5.25; P/B 0.96; ROE 19.5%; ROA 1.1%; Debt/Equity 16.44; Revenue Growth 4.6%; Profit Growth 16.9%.
- Tin doanh nghiệp: Không có snapshot tin đã lưu; không đưa ra nhận định tin tức.
- Live research: Live snapshot lấy lúc 2026-08-13T18:19:02.678117+00:00; News Reader đọc được 0 bài. ML có 8 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest.

### Bằng chứng

- ML decision artifact: NO_EDGE. Development OOS chỉ có 1 trade; cần >= 10.
- ML decision artifact: NO_EDGE. Frozen holdout chỉ có 0 trade; cần >= 10.
- ML decision artifact: NO_EDGE. Correlation dự báo-return development OOS không dương.
- ML decision artifact: NO_EDGE. Correlation dự báo-return frozen holdout không dương.
- ML decision artifact: NO_EDGE. Frozen holdout chưa có lợi thế ròng và Sharpe dương sau phí.
- ML decision artifact: NO_EDGE. Frozen holdout không chịu được stress phí 1.5x.
- ML decision artifact: NO_EDGE. Cận dưới expected excess return -0.03830378960797731 (dự báo điểm 0.002874567173421383) chưa vượt chi phí + margin 0.0088.
- ML decision artifact: NO_EDGE. Technical score -7 < 2.

### Rủi ro cần kiểm chứng

- ML guard: Development OOS chỉ có 1 trade; cần >= 10.
- ML guard: Frozen holdout chỉ có 0 trade; cần >= 10.
- ML guard: Correlation dự báo-return development OOS không dương.
- ML guard: Correlation dự báo-return frozen holdout không dương.
- ML guard: Frozen holdout chưa có lợi thế ròng và Sharpe dương sau phí.
- ML guard: Frozen holdout không chịu được stress phí 1.5x.
- ML guard: Cận dưới expected excess return -0.03830378960797731 (dự báo điểm 0.002874567173421383) chưa vượt chi phí + margin 0.0088.
- ML guard: Technical score -7 < 2.
- Chỉ lưu trích đoạn giới hạn để kiểm chứng nguồn; không lưu hay hiển thị toàn văn bài báo.
- Phân nhóm là keyword rule-based để định tuyến research, không phải sentiment hay dự báo tác động giá.
- Dữ liệu News Reader chỉ phục vụ research/report; không dùng làm feature train/backtest khi chưa có lịch sử available_at point-in-time.

### Nguồn live research


Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.

---

## News model riêng từng mã

- Symbol-news report: `/Users/tranlekhoa/Documents/DATA_SCI/vn_stock_analysis/reports/NAB/2026-08-14_01-18-45/all_files/symbol_news_model`
- Số bài tin trong CSV cho mã: 0
- Số dòng giá có news feature: 0
- XGBoost probability mới nhất: 0.497
- AUC OOS: 0.519
- Balanced accuracy OOS: 0.503
- Backtest total return: 0.000
- Base XGBoost probability: 0.499
- Chênh lệch News-adjusted - Base: -0.001
- Áp vào signal chính: not_applied
- Trạng thái news model: research_only
- Gate chưa đạt: min_articles_60, min_feature_rows_30, news_feature_gain_positive, auc_at_least_0_55, balanced_accuracy_at_least_0_52

News-adjusted model hiện là lớp kiểm chứng/shadow; signal chính vẫn do `signal_decision.json` quyết định.

Lưu ý: news model dùng dữ liệu `available_at` point-in-time trong CSV tích lũy; nếu lịch sử tin còn mỏng thì chỉ xem là research/smoke test.
