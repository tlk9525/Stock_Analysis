# Báo cáo ngày 2026-08-14 - NLG

## Tổng quan

- Dữ liệu: 2013-04-08 -> 2026-08-13, 3,309 phiên.
- Giá đóng cửa: 22.50 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận (điểm -3).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 49.4%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Model health: INSUFFICIENT_EDGE - Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 0/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định.
- Nếu chưa có cổ phiếu: INSUFFICIENT_EDGE - Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 0/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định.
- Nếu đang nắm giữ: REDUCE - Kỹ thuật chưa hỗ trợ và swing 5D chưa có edge; ưu tiên giảm rủi ro.

## Phân tích kỹ thuật

- SMA20 22.12; SMA60 24.65; RSI14 45.4.
- MACD -0.568; đường tín hiệu -0.826; biểu đồ cột 0.258.
- ATR14 0.71; ATR% 3.2%; ADX14 26.0.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Trung tính - RSI 45.4.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng giảm - ADX 26.0, -DI vượt +DI.
- Thanh khoản: Thấp - 0.67 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: BĐS Nam Long.
- Ngành: Real Estate.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 16.08.
- P/B: 0.88.
- ROE: 5.2%.
- ROA: 2.3%.
- Market cap: 10,987.5 tỷ.
- Revenue Growth: -46.3%.
- Profit Growth: -44.4%.
- P/E 16.08: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 0.88: nên đọc cùng ROE và đặc thù ngành.
- ROE 5.2%: hiệu quả vốn còn yếu.
- ROA 2.3%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 2.95: thanh khoản ngắn hạn khá.
- Revenue Growth -46.3% YoY.
- Profit Growth -44.4% YoY.
- CFO/LNST -8.58: dòng tiền chưa theo kịp lợi nhuận, cần đọc thêm biến động vốn lưu động.
- Dòng tiền tự do quý gần nhất âm; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là nợ vay ròng; không dùng một mình để kết luận rủi ro.
- Khả năng trả lãi 1.43 lần: cần theo dõi áp lực lãi vay.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.06 (keyword_heuristic_v1).
- Bài mới nhất: 2026-07-31T11:35:01+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-12-22 -> 2026-08-12.
- XGBoost: độ chính xác cân bằng 0.495; AUC 0.487; log-loss 0.697.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.489; AUC 0.491.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 19.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.

## Chiến lược swing 5 phiên: contract phát hành tín hiệu

### Khuyến nghị hành động sau phí

| Mục | Kết quả | Diễn giải |
|---|---:|---|
| Lệnh mới hôm nay | 0 lệnh | Không DCA hoặc chia nhỏ lệnh khi fixed-horizon swing chưa qua publish gate. |
| Trạng thái edge 5D | INSUFFICIENT_EDGE | Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 0/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định. |
| Nếu chưa có cổ phiếu | INSUFFICIENT_EDGE | Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 0/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định. |
| Nếu đang nắm giữ | REDUCE | Kỹ thuật chưa hỗ trợ và swing 5D chưa có edge; ưu tiên giảm rủi ro. |
| Expected excess return 5D | +0.0% | Cần vượt chi phí + margin 1.0%. |
| Mẫu frozen holdout | 0/10 trade | Chưa đủ số trade thì không có kết luận lợi nhuận/Sharpe và không được trade live. |
| Kỹ thuật / tin | -3 điểm | Suy yếu / cẩn thận; news warning: không. |

- Target: signal after close[t]; enter open[t+1]; exit close[t+5] ; target is stock return minus VNINDEX return over the same window
- Expected excess return mới nhất: +0.0%; safety margin đã chọn 0.5%.
- Frozen holdout: 0/10 trade; net/Sharpe chỉ được kết luận khi đủ mẫu.
- Publish gate swing: CHƯA ĐẠT. Gate yêu cầu sample/ranking dương ở development+frozen, net/Sharpe dương và stress phí 1.5×; chưa đạt thì giữ NO_EDGE.
- Các file audit: swing_development_oos.csv, swing_frozen_holdout.csv, swing_development_backtest.csv, swing_frozen_backtest.csv và file trades tương ứng.
- Mức độ quan trọng của đặc trưng: return_5d=11.08; stoch_k_14=9.88; return_1d=9.87; excess_return_20d=9.64; market_volatility_20d=9.63; rsi_14=9.39.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 21.43; mục tiêu 1 25.50; mục tiêu 2 26.87.
- Tỷ lệ lợi nhuận/rủi ro 2.45; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- Phương pháp: XGBoost direct quantile 5/10/20D + conformal calibration; toàn bộ horizon qua gate: chưa.
- P50 cuối kỳ 22.69 (0.82%).
- P10/P90 cuối kỳ 18.10 / 26.87.
- Lịch giao dịch: VN stock calendar: loại Thứ Bảy/Chủ Nhật và các ngày nghỉ 2026 đã công bố; ngày làm bù Thứ Bảy không được tính là phiên giao dịch chứng khoán.
- Ngày nghỉ đã loại khỏi forecast: 2026-01-01, 2026-01-02, 2026-02-16, 2026-02-17, 2026-02-18, 2026-02-19, 2026-02-20, 2026-04-27, 2026-04-30, 2026-05-01, 2026-08-31, 2026-09-01, 2026-09-02.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: Không có margin nào đạt số trade tối thiểu trong validation; strict no-entry fallback không phải rule đã chọn..
- Điều kiện phát hành tín hiệu: Development OOS chỉ có 0 trade; cần >= 10..
- Điều kiện phát hành tín hiệu: Frozen holdout chỉ có 0 trade; cần >= 10..
- Điều kiện phát hành tín hiệu: Correlation dự báo-return development OOS không dương..
- Điều kiện phát hành tín hiệu: Frozen holdout chưa có lợi thế ròng và Sharpe dương sau phí..
- Điều kiện phát hành tín hiệu: Frozen holdout không chịu được stress phí 1.5x..
- Điều kiện phát hành tín hiệu: MAE frozen holdout chưa tốt hơn baseline dự báo excess return bằng 0..
- Điều kiện phát hành tín hiệu: Cận dưới expected excess return -0.047698071307130774 (dự báo điểm 0.0003969183308072388) chưa vượt chi phí + margin 0.0100..
- Điều kiện phát hành tín hiệu: Technical score -3 < 2..
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 49.4%.
- Mô hình Logistic đối chứng: 49.8%.
- Quantile forecast ước tính xác suất return cuối kỳ dương từ residual frozen holdout: 25.8%.
- Mức dừng lỗ tham chiếu 21.43, mục tiêu 1 25.50, tỷ lệ lợi nhuận/rủi ro 2.45.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. Chưa có live research hoặc News Reader được lưu cho report này.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Suy yếu / cẩn thận; điểm -3. Chi tiết artifact: Xu hướng: Cẩn thận (Giá nằm dưới SMA60.); MACD: Tích cực (MACD trên signal, histogram dương.); RSI14: Trung tính (RSI 45.4.); Bollinger: Ổn định (Giá nằm trong dải Bollinger.); ADX: Xu hướng giảm (ADX 26.0, -DI vượt +DI.); Thanh khoản: Thấp (0.67 lần trung bình.); Stochastic: Yếu lại (%K nằm dưới %D.)
- Góc nhìn cơ bản: Artifact cơ bản: BĐS Nam Long; kỳ 2026-Q2; P/E 16.08; P/B 0.88; ROE 5.2%; ROA 2.3%; Debt/Equity 0.75; Revenue Growth -46.3%; Profit Growth -44.4%.
- Tin doanh nghiệp: Không có snapshot tin đã lưu; không đưa ra nhận định tin tức.
- Live research: Live snapshot lấy lúc 2026-08-13T18:21:14.746749+00:00; News Reader đọc được 0 bài. ML có 9 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest. Final report dùng fallback grounded từ artifact local.

### Bằng chứng

- ML decision artifact: NO_EDGE. Không có margin nào đạt số trade tối thiểu trong validation; strict no-entry fallback không phải rule đã chọn.
- ML decision artifact: NO_EDGE. Development OOS chỉ có 0 trade; cần >= 10.
- ML decision artifact: NO_EDGE. Frozen holdout chỉ có 0 trade; cần >= 10.
- ML decision artifact: NO_EDGE. Correlation dự báo-return development OOS không dương.
- ML decision artifact: NO_EDGE. Frozen holdout chưa có lợi thế ròng và Sharpe dương sau phí.
- ML decision artifact: NO_EDGE. Frozen holdout không chịu được stress phí 1.5x.
- ML decision artifact: NO_EDGE. MAE frozen holdout chưa tốt hơn baseline dự báo excess return bằng 0.
- ML decision artifact: NO_EDGE. Cận dưới expected excess return -0.047698071307130774 (dự báo điểm 0.0003969183308072388) chưa vượt chi phí + margin 0.0100.
- ML decision artifact: NO_EDGE. Technical score -3 < 2.

### Rủi ro cần kiểm chứng

- ML guard: Không có margin nào đạt số trade tối thiểu trong validation; strict no-entry fallback không phải rule đã chọn.
- ML guard: Development OOS chỉ có 0 trade; cần >= 10.
- ML guard: Frozen holdout chỉ có 0 trade; cần >= 10.
- ML guard: Correlation dự báo-return development OOS không dương.
- ML guard: Frozen holdout chưa có lợi thế ròng và Sharpe dương sau phí.
- ML guard: Frozen holdout không chịu được stress phí 1.5x.
- ML guard: MAE frozen holdout chưa tốt hơn baseline dự báo excess return bằng 0.
- ML guard: Cận dưới expected excess return -0.047698071307130774 (dự báo điểm 0.0003969183308072388) chưa vượt chi phí + margin 0.0100.
- ML guard: Technical score -3 < 2.
- Chỉ lưu trích đoạn giới hạn để kiểm chứng nguồn; không lưu hay hiển thị toàn văn bài báo.
- Phân nhóm là keyword rule-based để định tuyến research, không phải sentiment hay dự báo tác động giá.
- Dữ liệu News Reader chỉ phục vụ research/report; không dùng làm feature train/backtest khi chưa có lịch sử available_at point-in-time.
- Ollama AI chưa hoàn tất trong lệnh full: Exit: 

### Nguồn live research


Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.

---

## News model riêng từng mã

- Symbol-news report: `/Users/tranlekhoa/Documents/DATA_SCI/vn_stock_analysis/reports/NLG/2026-08-14_01-20-55/all_files/symbol_news_model`
- Số bài tin trong CSV cho mã: 0
- Số dòng giá có news feature: 0
- XGBoost probability mới nhất: 0.502
- AUC OOS: 0.491
- Balanced accuracy OOS: 0.500
- Backtest total return: 0.000
- Base XGBoost probability: 0.494
- Chênh lệch News-adjusted - Base: +0.008
- Áp vào signal chính: not_applied
- Trạng thái news model: research_only
- Gate chưa đạt: min_articles_60, min_feature_rows_30, news_feature_gain_positive, auc_at_least_0_55, balanced_accuracy_at_least_0_52

News-adjusted model hiện là lớp kiểm chứng/shadow; signal chính vẫn do `signal_decision.json` quyết định.

Lưu ý: news model dùng dữ liệu `available_at` point-in-time trong CSV tích lũy; nếu lịch sử tin còn mỏng thì chỉ xem là research/smoke test.
