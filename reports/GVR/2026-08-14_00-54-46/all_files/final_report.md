# Báo cáo ngày 2026-08-14 - GVR

## Tổng quan

- Dữ liệu: 2018-03-21 -> 2026-08-13, 2,093 phiên.
- Giá đóng cửa: 32.65 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Tích cực (điểm 6).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 49.8%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Model health: INSUFFICIENT_EDGE - Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 2/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định.
- Nếu chưa có cổ phiếu: INSUFFICIENT_EDGE - Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 2/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định.
- Nếu đang nắm giữ: HOLD_DISCIPLINED - Nếu đã nắm giữ: giữ theo stop-loss, không mua thêm khi swing 5D chưa đủ edge.

## Phân tích kỹ thuật

- SMA20 28.51; SMA60 31.81; RSI14 65.9.
- MACD 0.234; đường tín hiệu -0.572; biểu đồ cột 0.806.
- ATR14 1.10; ATR% 3.4%; ADX14 37.0.
- Xu hướng: Trung tính - Giá trên SMA60 nhưng chưa vượt SMA20.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 65.9.
- Bollinger: Gần biên trên - Giá sát/vượt biên trên.
- ADX: Xu hướng tăng - ADX 37.0, +DI vượt -DI.
- Thanh khoản: Đột biến - 2.37 lần trung bình.
- Stochastic: Cực trị - %K 96.6, %D 93.0.

## Phân tích cơ bản

- Doanh nghiệp: Tập đoàn CN Cao su VN.
- Ngành: Chemicals.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 18.09.
- P/B: 2.13.
- ROE: 12.2%.
- ROA: 8.2%.
- Market cap: 129,000.0 tỷ.
- Revenue Growth: 20.5%.
- Profit Growth: 58.2%.
- P/E 18.09: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 2.13: nên đọc cùng ROE và đặc thù ngành.
- ROA 8.2%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 4.20: thanh khoản ngắn hạn khá.
- Revenue Growth 20.5% YoY.
- Profit Growth 58.2% YoY.
- CFO/LNST 0.99: chất lượng chuyển đổi lợi nhuận sang tiền mặt khá tốt.
- Dòng tiền tự do quý gần nhất dương; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là tiền mặt ròng; không dùng một mình để kết luận rủi ro.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.18 (keyword_heuristic_v1).
- Bài mới nhất: 2026-07-30T10:43:09+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2024-01-03 -> 2026-08-12.
- XGBoost: độ chính xác cân bằng 0.525; AUC 0.524; log-loss 0.698.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.529; AUC 0.541.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 9.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.

## Chiến lược swing 5 phiên: contract phát hành tín hiệu

### Khuyến nghị hành động sau phí

| Mục | Kết quả | Diễn giải |
|---|---:|---|
| Lệnh mới hôm nay | 0 lệnh | Không DCA hoặc chia nhỏ lệnh khi fixed-horizon swing chưa qua publish gate. |
| Trạng thái edge 5D | INSUFFICIENT_EDGE | Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 2/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định. |
| Nếu chưa có cổ phiếu | INSUFFICIENT_EDGE | Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 2/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định. |
| Nếu đang nắm giữ | HOLD_DISCIPLINED | Nếu đã nắm giữ: giữ theo stop-loss, không mua thêm khi swing 5D chưa đủ edge. |
| Expected excess return 5D | +0.5% | Cần vượt chi phí + margin 0.8%. |
| Mẫu frozen holdout | 2/10 trade | Chưa đủ số trade thì không có kết luận lợi nhuận/Sharpe và không được trade live. |
| Kỹ thuật / tin | 6 điểm | Tích cực; news warning: không. |

- Target: signal after close[t]; enter open[t+1]; exit close[t+5] ; target is stock return minus VNINDEX return over the same window
- Expected excess return mới nhất: +0.5%; safety margin đã chọn 0.2%.
- Frozen holdout: 2/10 trade; net/Sharpe chỉ được kết luận khi đủ mẫu.
- Publish gate swing: CHƯA ĐẠT. Gate yêu cầu sample/ranking dương ở development+frozen, net/Sharpe dương và stress phí 1.5×; chưa đạt thì giữ NO_EDGE.
- Các file audit: swing_development_oos.csv, swing_frozen_holdout.csv, swing_development_backtest.csv, swing_frozen_backtest.csv và file trades tương ứng.
- Mức độ quan trọng của đặc trưng: rsi_14=16.80; return_2d=13.54; range_pct=11.95; return_1d=10.80; corr_60d=10.44; return_skew_20d=10.41.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 31.49; mục tiêu 1 39.93; mục tiêu 2 39.93.
- Tỷ lệ lợi nhuận/rủi ro 5.40; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- Phương pháp: XGBoost direct quantile 5/10/20D + conformal calibration; toàn bộ horizon qua gate: chưa.
- P50 cuối kỳ 33.58 (2.85%).
- P10/P90 cuối kỳ 27.11 / 39.93.
- Lịch giao dịch: VN stock calendar: loại Thứ Bảy/Chủ Nhật và các ngày nghỉ 2026 đã công bố; ngày làm bù Thứ Bảy không được tính là phiên giao dịch chứng khoán.
- Ngày nghỉ đã loại khỏi forecast: 2026-01-01, 2026-01-02, 2026-02-16, 2026-02-17, 2026-02-18, 2026-02-19, 2026-02-20, 2026-04-27, 2026-04-30, 2026-05-01, 2026-08-31, 2026-09-01, 2026-09-02.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: Frozen holdout chỉ có 2 trade; cần >= 10..
- Điều kiện phát hành tín hiệu: Correlation dự báo-return development OOS không dương..
- Điều kiện phát hành tín hiệu: Correlation dự báo-return frozen holdout không dương..
- Điều kiện phát hành tín hiệu: Frozen holdout chưa có lợi thế ròng và Sharpe dương sau phí..
- Điều kiện phát hành tín hiệu: Frozen holdout không chịu được stress phí 1.5x..
- Điều kiện phát hành tín hiệu: MAE frozen holdout chưa tốt hơn baseline dự báo excess return bằng 0..
- Điều kiện phát hành tín hiệu: Cận dưới expected excess return -0.04620832938938524 (dự báo điểm 0.005052703898400068) chưa vượt chi phí + margin 0.0075..
- Trung hạn chưa xấu, ngắn hạn yếu vì giá dưới SMA20.
- Xu hướng kỹ thuật nghiêng về: Tích cực.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 49.8%.
- Mô hình Logistic đối chứng: 50.4%.
- Quantile forecast ước tính xác suất return cuối kỳ dương từ residual frozen holdout: 39.3%.
- Mức dừng lỗ tham chiếu 31.49, mục tiêu 1 39.93, tỷ lệ lợi nhuận/rủi ro 5.40.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. News Reader đã trích đoạn có nguồn của 3 bài để phân loại chủ đề (ket_qua_kinh_doanh: 3, vi_mo: 1, nganh: 3, rui_ro: 1), nhưng các trích đoạn này không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Tích cực; điểm 6. Chi tiết artifact: Xu hướng: Trung tính (Giá trên SMA60 nhưng chưa vượt SMA20.); MACD: Tích cực (MACD trên signal, histogram dương.); RSI14: Tích cực (RSI 65.9.); Bollinger: Gần biên trên (Giá sát/vượt biên trên.); ADX: Xu hướng tăng (ADX 37.0, +DI vượt -DI.); Thanh khoản: Đột biến (2.37 lần trung bình.); Stochastic: Cực trị (%K 96.6, %D 93.0.)
- Góc nhìn cơ bản: Artifact cơ bản: Tập đoàn CN Cao su VN; kỳ 2026-Q2; P/E 18.09; P/B 2.13; ROE 12.2%; ROA 8.2%; Debt/Equity 0.35; Revenue Growth 20.5%; Profit Growth 58.2%.
- Tin doanh nghiệp: Đã đọc trích đoạn giới hạn của 3 bài; phân nhóm rule-based: ket_qua_kinh_doanh: 3, vi_mo: 1, nganh: 3, rui_ro: 1. Tác động cần kiểm chứng: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường. Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh. So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp. Xác minh công bố chính thức, phạm vi ảnh hưởng và khả năng định lượng rủi ro. Đây không phải sentiment hay dự báo tác động giá.
- Live research: Live snapshot lấy lúc 2026-08-13T17:55:04.935665+00:00; News Reader đọc được 3 bài. ML có 7 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest.

### Bằng chứng

- ML decision artifact: NO_EDGE. Frozen holdout chỉ có 2 trade; cần >= 10.
- ML decision artifact: NO_EDGE. Correlation dự báo-return development OOS không dương.
- ML decision artifact: NO_EDGE. Correlation dự báo-return frozen holdout không dương.
- ML decision artifact: NO_EDGE. Frozen holdout chưa có lợi thế ròng và Sharpe dương sau phí.
- ML decision artifact: NO_EDGE. Frozen holdout không chịu được stress phí 1.5x.
- ML decision artifact: NO_EDGE. MAE frozen holdout chưa tốt hơn baseline dự báo excess return bằng 0.
- ML decision artifact: NO_EDGE. Cận dưới expected excess return -0.04620832938938524 (dự báo điểm 0.005052703898400068) chưa vượt chi phí + margin 0.0075.
- News Reader [Chứng khoán DNSE]: Gợi ý mã cổ phiếu tiềm năng: GVR - Chứng khoán DNSE | nhóm: ket_qua_kinh_doanh, nganh (2026-08-10T18:47:43+00:00)
- News Reader [Nhadautu.vn]: Những cổ phiếu vốn Nhà nước kỳ vọng hưởng lợi từ Quyết định 40 - Nhadautu.vn | nhóm: ket_qua_kinh_doanh, vi_mo, nganh, rui_ro (2026-08-08T01:47:29+00:00)
- News Reader [congly.vn]: Chứng khoán trưa 10/8: BCM tăng trần, GAS - GVR kéo VN-Index tiến sát 1.780 điểm - congly.vn | nhóm: ket_qua_kinh_doanh, nganh (2026-08-10T06:21:55+00:00)

### Rủi ro cần kiểm chứng

- ML guard: Frozen holdout chỉ có 2 trade; cần >= 10.
- ML guard: Correlation dự báo-return development OOS không dương.
- ML guard: Correlation dự báo-return frozen holdout không dương.
- ML guard: Frozen holdout chưa có lợi thế ròng và Sharpe dương sau phí.
- ML guard: Frozen holdout không chịu được stress phí 1.5x.
- ML guard: MAE frozen holdout chưa tốt hơn baseline dự báo excess return bằng 0.
- ML guard: Cận dưới expected excess return -0.04620832938938524 (dự báo điểm 0.005052703898400068) chưa vượt chi phí + margin 0.0075.
- News Reader: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường.
- News Reader: Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh.
- News Reader: So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp.
- News Reader: Xác minh công bố chính thức, phạm vi ảnh hưởng và khả năng định lượng rủi ro.
- Chỉ lưu trích đoạn giới hạn để kiểm chứng nguồn; không lưu hay hiển thị toàn văn bài báo.
- Phân nhóm là keyword rule-based để định tuyến research, không phải sentiment hay dự báo tác động giá.
- Dữ liệu News Reader chỉ phục vụ research/report; không dùng làm feature train/backtest khi chưa có lịch sử available_at point-in-time.
- Tin live/trích đoạn cần mở URL gốc để kiểm chứng bối cảnh, số liệu và thời điểm trước khi sử dụng.

### Nguồn live research

- [Chứng khoán DNSE] Gợi ý mã cổ phiếu tiềm năng: GVR - Chứng khoán DNSE (2026-08-10T18:47:43+00:00): https://www.dnse.com.vn/tin-tuc/goi-y-ma-co-phieu-tiem-nang-gvr
- [Nhadautu.vn] Những cổ phiếu vốn Nhà nước kỳ vọng hưởng lợi từ Quyết định 40 - Nhadautu.vn (2026-08-08T01:47:29+00:00): https://nhadautu.vn/nhung-co-phieu-von-nha-nuoc-ky-vong-huong-loi-tu-quyet-dinh-40-d106854.html
- [congly.vn] Chứng khoán trưa 10/8: BCM tăng trần, GAS - GVR kéo VN-Index tiến sát 1.780 điểm - congly.vn (2026-08-10T06:21:55+00:00): https://doanhnhan.congly.vn/chung-khoan-trua-10-8-bcm-tang-tran-gas-gvr-keo-vn-index-tien-sat-1-780-diem.html

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.

---

## News model riêng từng mã

- Symbol-news report: `/Users/tranlekhoa/Documents/DATA_SCI/vn_stock_analysis/reports/GVR/2026-08-14_00-54-46/all_files/symbol_news_model`
- Số bài tin trong CSV cho mã: 3
- Số dòng giá có news feature: 4
- XGBoost probability mới nhất: 0.495
- AUC OOS: 0.534
- Balanced accuracy OOS: 0.537
- Backtest total return: 0.000
- Base XGBoost probability: 0.498
- Chênh lệch News-adjusted - Base: -0.004
- Áp vào signal chính: not_applied
- Trạng thái news model: research_only
- Gate chưa đạt: min_articles_60, min_feature_rows_30, news_feature_gain_positive, auc_at_least_0_55

News-adjusted model hiện là lớp kiểm chứng/shadow; signal chính vẫn do `signal_decision.json` quyết định.

Lưu ý: news model dùng dữ liệu `available_at` point-in-time trong CSV tích lũy; nếu lịch sử tin còn mỏng thì chỉ xem là research/smoke test.
