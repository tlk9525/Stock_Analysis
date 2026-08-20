# Báo cáo ngày 2026-08-14 - VGC

## Tổng quan

- Dữ liệu: 2015-10-15 -> 2026-08-13, 2,680 phiên.
- Giá đóng cửa: 40.60 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Tích cực (điểm 5).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 53.0%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Model health: INSUFFICIENT_EDGE - Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 0/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định.
- Nếu chưa có cổ phiếu: INSUFFICIENT_EDGE - Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 0/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định.
- Nếu đang nắm giữ: HOLD_DISCIPLINED - Nếu đã nắm giữ: giữ theo stop-loss, không mua thêm khi swing 5D chưa đủ edge.

## Phân tích kỹ thuật

- SMA20 37.89; SMA60 39.38; RSI14 60.9.
- MACD 0.385; đường tín hiệu -0.153; biểu đồ cột 0.538.
- ATR14 1.21; ATR% 3.0%; ADX14 29.1.
- Xu hướng: Trung tính - Giá trên SMA60 nhưng chưa vượt SMA20.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 60.9.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng tăng - ADX 29.1, +DI vượt -DI.
- Thanh khoản: Bình thường - 0.74 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: Tổng Công ty Viglacera.
- Ngành: Construction & Materials.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 12.86.
- P/B: 2.18.
- ROE: 16.2%.
- ROA: 5.3%.
- Market cap: 18,292.7 tỷ.
- Revenue Growth: 38.2%.
- Profit Growth: 28.4%.
- P/E 12.86: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 2.18: nên đọc cùng ROE và đặc thù ngành.
- ROE 16.2%: hiệu quả vốn chủ sở hữu tốt.
- ROA 5.3%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 1.72: thanh khoản ngắn hạn khá.
- Revenue Growth 38.2% YoY.
- Profit Growth 28.4% YoY.
- CFO/LNST 0.08: dòng tiền chưa theo kịp lợi nhuận, cần đọc thêm biến động vốn lưu động.
- Dòng tiền tự do quý gần nhất âm; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là nợ vay ròng; không dùng một mình để kết luận rủi ro.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.12 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-04T10:28:31+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-09-12 -> 2026-08-12.
- XGBoost: độ chính xác cân bằng 0.520; AUC 0.552; log-loss 0.684.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.525; AUC 0.567.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 69.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.

## Chiến lược swing 5 phiên: contract phát hành tín hiệu

### Khuyến nghị hành động sau phí

| Mục | Kết quả | Diễn giải |
|---|---:|---|
| Lệnh mới hôm nay | 0 lệnh | Không DCA hoặc chia nhỏ lệnh khi fixed-horizon swing chưa qua publish gate. |
| Trạng thái edge 5D | INSUFFICIENT_EDGE | Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 0/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định. |
| Nếu chưa có cổ phiếu | INSUFFICIENT_EDGE | Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 0/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định. |
| Nếu đang nắm giữ | HOLD_DISCIPLINED | Nếu đã nắm giữ: giữ theo stop-loss, không mua thêm khi swing 5D chưa đủ edge. |
| Expected excess return 5D | +0.3% | Cần vượt chi phí + margin 0.5%. |
| Mẫu frozen holdout | 0/10 trade | Chưa đủ số trade thì không có kết luận lợi nhuận/Sharpe và không được trade live. |
| Kỹ thuật / tin | 5 điểm | Tích cực; news warning: không. |

- Target: signal after close[t]; enter open[t+1]; exit close[t+5] ; target is stock return minus VNINDEX return over the same window
- Expected excess return mới nhất: +0.3%; safety margin đã chọn 0.0%.
- Frozen holdout: 0/10 trade; net/Sharpe chỉ được kết luận khi đủ mẫu.
- Publish gate swing: CHƯA ĐẠT. Gate yêu cầu sample/ranking dương ở development+frozen, net/Sharpe dương và stress phí 1.5×; chưa đạt thì giữ NO_EDGE.
- Các file audit: swing_development_oos.csv, swing_frozen_holdout.csv, swing_development_backtest.csv, swing_frozen_backtest.csv và file trades tương ứng.
- Mức độ quan trọng của đặc trưng: market_return_1d=9.20; day_of_week=8.85; return_2d=8.30; excess_return_20d=7.99; market_return_5d=7.92; atr_pct_14=7.85.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 38.99; mục tiêu 1 46.93; mục tiêu 2 46.93.
- Tỷ lệ lợi nhuận/rủi ro 3.37; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- Phương pháp: XGBoost direct quantile 5/10/20D + conformal calibration; toàn bộ horizon qua gate: chưa.
- P50 cuối kỳ 41.54 (2.33%).
- P10/P90 cuối kỳ 35.60 / 46.93.
- Lịch giao dịch: VN stock calendar: loại Thứ Bảy/Chủ Nhật và các ngày nghỉ 2026 đã công bố; ngày làm bù Thứ Bảy không được tính là phiên giao dịch chứng khoán.
- Ngày nghỉ đã loại khỏi forecast: 2026-01-01, 2026-01-02, 2026-02-16, 2026-02-17, 2026-02-18, 2026-02-19, 2026-02-20, 2026-04-27, 2026-04-30, 2026-05-01, 2026-08-31, 2026-09-01, 2026-09-02.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: Frozen holdout chỉ có 0 trade; cần >= 10..
- Điều kiện phát hành tín hiệu: Frozen holdout chưa có lợi thế ròng và Sharpe dương sau phí..
- Điều kiện phát hành tín hiệu: Frozen holdout không chịu được stress phí 1.5x..
- Điều kiện phát hành tín hiệu: MAE frozen holdout chưa tốt hơn baseline dự báo excess return bằng 0..
- Điều kiện phát hành tín hiệu: Cận dưới expected excess return -0.04901968599225026 (dự báo điểm 0.0032380057964473963) chưa vượt chi phí + margin 0.0050..
- Trung hạn chưa xấu, ngắn hạn yếu vì giá dưới SMA20.
- Xu hướng kỹ thuật nghiêng về: Tích cực.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 53.0%.
- Mô hình Logistic đối chứng: 51.4%.
- Quantile forecast ước tính xác suất return cuối kỳ dương từ residual frozen holdout: 36.9%.
- Mức dừng lỗ tham chiếu 38.99, mục tiêu 1 46.93, tỷ lệ lợi nhuận/rủi ro 3.37.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. News Reader đã trích đoạn có nguồn của 2 bài để phân loại chủ đề (ket_qua_kinh_doanh: 2, vi_mo: 2, nganh: 1, rui_ro: 1), nhưng các trích đoạn này không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Tích cực; điểm 5. Chi tiết artifact: Xu hướng: Trung tính (Giá trên SMA60 nhưng chưa vượt SMA20.); MACD: Tích cực (MACD trên signal, histogram dương.); RSI14: Tích cực (RSI 60.9.); Bollinger: Ổn định (Giá nằm trong dải Bollinger.); ADX: Xu hướng tăng (ADX 29.1, +DI vượt -DI.); Thanh khoản: Bình thường (0.74 lần trung bình.); Stochastic: Yếu lại (%K nằm dưới %D.)
- Góc nhìn cơ bản: Artifact cơ bản: Tổng Công ty Viglacera; kỳ 2026-Q2; P/E 12.86; P/B 2.18; ROE 16.2%; ROA 5.3%; Debt/Equity 1.36; Revenue Growth 38.2%; Profit Growth 28.4%.
- Tin doanh nghiệp: Đã đọc trích đoạn giới hạn của 2 bài; phân nhóm rule-based: ket_qua_kinh_doanh: 2, vi_mo: 2, nganh: 1, rui_ro: 1. Tác động cần kiểm chứng: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường. Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh. So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp. Xác minh công bố chính thức, phạm vi ảnh hưởng và khả năng định lượng rủi ro. Đây không phải sentiment hay dự báo tác động giá.
- Live research: Live snapshot lấy lúc 2026-08-13T18:56:19.842484+00:00; News Reader đọc được 2 bài. ML có 5 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest.

### Bằng chứng

- ML decision artifact: NO_EDGE. Frozen holdout chỉ có 0 trade; cần >= 10.
- ML decision artifact: NO_EDGE. Frozen holdout chưa có lợi thế ròng và Sharpe dương sau phí.
- ML decision artifact: NO_EDGE. Frozen holdout không chịu được stress phí 1.5x.
- ML decision artifact: NO_EDGE. MAE frozen holdout chưa tốt hơn baseline dự báo excess return bằng 0.
- ML decision artifact: NO_EDGE. Cận dưới expected excess return -0.04901968599225026 (dự báo điểm 0.0032380057964473963) chưa vượt chi phí + margin 0.0050.
- News Reader [nguoiquansat.vn]: Cổ phiếu đáng chú ý ngày 11/8: TCB, GAS, VGC - nguoiquansat.vn | nhóm: ket_qua_kinh_doanh, vi_mo, nganh, rui_ro (2026-08-10T16:09:01+00:00)
- News Reader [nguoiquansat.vn]: 'Bắt đáy' cổ phiếu GEX, nhà đầu tư tạm lãi hơn 30% sau chưa đầy nửa tháng - nguoiquansat.vn | nhóm: ket_qua_kinh_doanh, vi_mo (2026-08-10T10:32:01+00:00)

### Rủi ro cần kiểm chứng

- ML guard: Frozen holdout chỉ có 0 trade; cần >= 10.
- ML guard: Frozen holdout chưa có lợi thế ròng và Sharpe dương sau phí.
- ML guard: Frozen holdout không chịu được stress phí 1.5x.
- ML guard: MAE frozen holdout chưa tốt hơn baseline dự báo excess return bằng 0.
- ML guard: Cận dưới expected excess return -0.04901968599225026 (dự báo điểm 0.0032380057964473963) chưa vượt chi phí + margin 0.0050.
- News Reader: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường.
- News Reader: Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh.
- News Reader: So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp.
- News Reader: Xác minh công bố chính thức, phạm vi ảnh hưởng và khả năng định lượng rủi ro.
- Chỉ lưu trích đoạn giới hạn để kiểm chứng nguồn; không lưu hay hiển thị toàn văn bài báo.
- Phân nhóm là keyword rule-based để định tuyến research, không phải sentiment hay dự báo tác động giá.
- Dữ liệu News Reader chỉ phục vụ research/report; không dùng làm feature train/backtest khi chưa có lịch sử available_at point-in-time.
- Tin live/trích đoạn cần mở URL gốc để kiểm chứng bối cảnh, số liệu và thời điểm trước khi sử dụng.

### Nguồn live research

- [nguoiquansat.vn] Cổ phiếu đáng chú ý ngày 11/8: TCB, GAS, VGC - nguoiquansat.vn (2026-08-10T16:09:01+00:00): https://nguoiquansat.vn/co-phieu-dang-chu-y-ngay-11-8-tcb-gas-vgc-309709.html
- [nguoiquansat.vn] 'Bắt đáy' cổ phiếu GEX, nhà đầu tư tạm lãi hơn 30% sau chưa đầy nửa tháng - nguoiquansat.vn (2026-08-10T10:32:01+00:00): https://nguoiquansat.vn/bat-day-co-phieu-gex-nha-dau-tu-tam-lai-hon-30-sau-chua-day-nua-thang-309652.html

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.

---

## News model riêng từng mã

- Symbol-news report: `/Users/tranlekhoa/Documents/DATA_SCI/vn_stock_analysis/reports/VGC/2026-08-14_01-56-01/all_files/symbol_news_model`
- Số bài tin trong CSV cho mã: 2
- Số dòng giá có news feature: 3
- XGBoost probability mới nhất: 0.577
- AUC OOS: 0.553
- Balanced accuracy OOS: 0.501
- Backtest total return: 0.000
- Base XGBoost probability: 0.530
- Chênh lệch News-adjusted - Base: +0.046
- Áp vào signal chính: not_applied
- Trạng thái news model: research_only
- Gate chưa đạt: min_articles_60, min_feature_rows_30, news_feature_gain_positive, balanced_accuracy_at_least_0_52

News-adjusted model hiện là lớp kiểm chứng/shadow; signal chính vẫn do `signal_decision.json` quyết định.

Lưu ý: news model dùng dữ liệu `available_at` point-in-time trong CSV tích lũy; nếu lịch sử tin còn mỏng thì chỉ xem là research/smoke test.
