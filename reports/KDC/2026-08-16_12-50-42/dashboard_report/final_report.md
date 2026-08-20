# Báo cáo ngày 2026-08-16 - KDC

## Tổng quan

- Dữ liệu: 2008-03-10 -> 2026-08-14, 4,593 phiên.
- Giá đóng cửa: 51.40 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng (điểm 2).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 41.1%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Model health: INSUFFICIENT_EDGE - Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 2/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định.
- Nếu chưa có cổ phiếu: INSUFFICIENT_EDGE - Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 2/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định.
- Nếu đang nắm giữ: HOLD_DISCIPLINED - Nếu đã nắm giữ: giữ theo stop-loss, không mua thêm khi swing 5D chưa đủ edge.

## Phân tích kỹ thuật

- SMA20 50.44; SMA60 50.16; RSI14 60.1.
- MACD 0.552; đường tín hiệu 0.452; biểu đồ cột 0.100.
- ATR14 1.10; ATR% 2.1%; ADX14 32.0.
- Xu hướng: Tích cực - Giá nằm trên SMA20 và SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 60.1.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng giảm - ADX 32.0, -DI vượt +DI.
- Thanh khoản: Thấp - 0.40 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: Tập đoàn KIDO.
- Ngành: Food & Beverage.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 29.83.
- P/B: 2.42.
- ROE: 7.6%.
- ROA: 3.8%.
- Market cap: 14,204.1 tỷ.
- Revenue Growth: -7.3%.
- Profit Growth: -105.8%.
- P/E 29.83: định giá cao, cần tăng trưởng lợi nhuận hỗ trợ.
- P/B 2.42: nên đọc cùng ROE và đặc thù ngành.
- ROE 7.6%: hiệu quả vốn còn yếu.
- ROA 3.8%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 1.02: thanh khoản ngắn hạn khá.
- Revenue Growth -7.3% YoY.
- Profit Growth -105.8% YoY.
- CFO/LNST -46.72: dòng tiền chưa theo kịp lợi nhuận, cần đọc thêm biến động vốn lưu động.
- Dòng tiền tự do quý gần nhất âm; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là nợ vay ròng; không dùng một mình để kết luận rủi ro.
- Khả năng trả lãi 0.44 lần: cần theo dõi áp lực lãi vay.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.06 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-13T09:27:28+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-08-25 -> 2026-08-13.
- XGBoost: độ chính xác cân bằng 0.511; AUC 0.535; log-loss 0.679.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.492; AUC 0.529.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 54.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.

## Chiến lược swing 5 phiên: contract phát hành tín hiệu

### Khuyến nghị hành động sau phí

| Mục | Kết quả | Diễn giải |
|---|---:|---|
| Lệnh mới hôm nay | 0 lệnh | Không DCA hoặc chia nhỏ lệnh khi fixed-horizon swing chưa qua publish gate. |
| Trạng thái edge 5D | INSUFFICIENT_EDGE | Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 2/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định. |
| Nếu chưa có cổ phiếu | INSUFFICIENT_EDGE | Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 2/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định. |
| Nếu đang nắm giữ | HOLD_DISCIPLINED | Nếu đã nắm giữ: giữ theo stop-loss, không mua thêm khi swing 5D chưa đủ edge. |
| Expected excess return 5D | -0.1% | Cần vượt chi phí + margin 1.0%. |
| Mẫu frozen holdout | 2/10 trade | Chưa đủ số trade thì không có kết luận lợi nhuận/Sharpe và không được trade live. |
| Kỹ thuật / tin | 2 điểm | Hồi phục / nghiêng tăng; news warning: không. |

- Target: signal after close[t]; enter open[t+1]; exit close[t+5] ; target is stock return minus VNINDEX return over the same window
- Expected excess return mới nhất: -0.1%; safety margin đã chọn 0.5%.
- Frozen holdout: 2/10 trade; net/Sharpe chỉ được kết luận khi đủ mẫu.
- Publish gate swing: CHƯA ĐẠT. Gate yêu cầu sample/ranking dương ở development+frozen, net/Sharpe dương và stress phí 1.5×; chưa đạt thì giữ NO_EDGE.
- Các file audit: swing_development_oos.csv, swing_frozen_holdout.csv, swing_development_backtest.csv, swing_frozen_backtest.csv và file trades tương ứng.
- Mức độ quan trọng của đặc trưng: month_of_year=11.86; return_5d=11.85; return_skew_20d=11.50; rsi_14=11.48; adx_14=11.24; volume_ratio_20=11.12.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 49.75; mục tiêu 1 N/A; mục tiêu 2 54.51.
- Tỷ lệ lợi nhuận/rủi ro N/A; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- Phương pháp: XGBoost direct quantile 5/10/20D + conformal calibration; toàn bộ horizon qua gate: chưa.
- P50 cuối kỳ 51.04 (-0.71%).
- P10/P90 cuối kỳ 48.52 / 54.51.
- Lịch giao dịch: VN stock calendar: loại Thứ Bảy/Chủ Nhật và các ngày nghỉ 2026 đã công bố; ngày làm bù Thứ Bảy không được tính là phiên giao dịch chứng khoán.
- Ngày nghỉ đã loại khỏi forecast: 2026-01-01, 2026-01-02, 2026-02-16, 2026-02-17, 2026-02-18, 2026-02-19, 2026-02-20, 2026-04-27, 2026-04-30, 2026-05-01, 2026-08-31, 2026-09-01, 2026-09-02.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: Không có margin nào đạt số trade tối thiểu trong validation; strict no-entry fallback không phải rule đã chọn..
- Điều kiện phát hành tín hiệu: Frozen holdout chỉ có 2 trade; cần >= 10..
- Điều kiện phát hành tín hiệu: Cận dưới expected excess return -0.037928263400936246 (dự báo điểm -0.0012838542461395264) chưa vượt chi phí + margin 0.0100..
- Điều kiện phát hành tín hiệu: Reward/risk N/A < 1.50..
- Điều kiện phát hành tín hiệu: Không còn vị thế theo lô hợp lệ sau giới hạn rủi ro và thanh khoản..
- Xu hướng ngắn hạn thuận: giá trên SMA20 và SMA60.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 41.1%.
- Mô hình Logistic đối chứng: 42.4%.
- Quantile forecast ước tính xác suất return cuối kỳ dương từ residual frozen holdout: 31.0%.
- Mức dừng lỗ tham chiếu 49.75, mục tiêu 1 N/A, tỷ lệ lợi nhuận/rủi ro N/A.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. News Reader đã trích đoạn có nguồn của 2 bài để phân loại chủ đề (ket_qua_kinh_doanh: 1, co_tuc_va_hanh_dong_doanh_nghiep: 2, vi_mo: 1), nhưng các trích đoạn này không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Hồi phục / nghiêng tăng; điểm 2. Chi tiết artifact: Xu hướng: Tích cực (Giá nằm trên SMA20 và SMA60.); MACD: Tích cực (MACD trên signal, histogram dương.); RSI14: Tích cực (RSI 60.1.); Bollinger: Ổn định (Giá nằm trong dải Bollinger.); ADX: Xu hướng giảm (ADX 32.0, -DI vượt +DI.); Thanh khoản: Thấp (0.40 lần trung bình.); Stochastic: Yếu lại (%K nằm dưới %D.)
- Góc nhìn cơ bản: Artifact cơ bản: Tập đoàn KIDO; kỳ 2026-Q2; P/E 29.83; P/B 2.42; ROE 7.6%; ROA 3.8%; Debt/Equity 0.96; Revenue Growth -7.3%; Profit Growth -105.8%.
- Tin doanh nghiệp: Đã đọc trích đoạn giới hạn của 2 bài; phân nhóm rule-based: ket_qua_kinh_doanh: 1, co_tuc_va_hanh_dong_doanh_nghiep: 2, vi_mo: 1. Tác động cần kiểm chứng: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường. Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động. Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh. Đây không phải sentiment hay dự báo tác động giá.
- Live research: Live snapshot lấy lúc 2026-08-16T05:51:00.646523+00:00; News Reader đọc được 2 bài. ML có 5 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest.

### Bằng chứng

- ML decision artifact: NO_EDGE. Không có margin nào đạt số trade tối thiểu trong validation; strict no-entry fallback không phải rule đã chọn.
- ML decision artifact: NO_EDGE. Frozen holdout chỉ có 2 trade; cần >= 10.
- ML decision artifact: NO_EDGE. Cận dưới expected excess return -0.037928263400936246 (dự báo điểm -0.0012838542461395264) chưa vượt chi phí + margin 0.0100.
- ML decision artifact: NO_EDGE. Reward/risk N/A < 1.50.
- ML decision artifact: NO_EDGE. Không còn vị thế theo lô hợp lệ sau giới hạn rủi ro và thanh khoản.
- News Reader [Báo Pháp Luật Việt Nam]: Tập đoàn Kido (KDC): Anh ruột lãnh đạo Kido bán ra hơn 400.000 cổ phiếu KDC, lãi quý II sụt giảm 60% - Báo Pháp Luật Việt Nam | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep (2026-08-15T02:08:00+00:00)
- News Reader [Tin nhanh chứng khoán]: Sự kiện chứng khoán đáng chú ý ngày 14/8 - Tin nhanh chứng khoán | nhóm: co_tuc_va_hanh_dong_doanh_nghiep, vi_mo (2026-08-13T11:07:57+00:00)

### Rủi ro cần kiểm chứng

- ML guard: Không có margin nào đạt số trade tối thiểu trong validation; strict no-entry fallback không phải rule đã chọn.
- ML guard: Frozen holdout chỉ có 2 trade; cần >= 10.
- ML guard: Cận dưới expected excess return -0.037928263400936246 (dự báo điểm -0.0012838542461395264) chưa vượt chi phí + margin 0.0100.
- ML guard: Reward/risk N/A < 1.50.
- ML guard: Không còn vị thế theo lô hợp lệ sau giới hạn rủi ro và thanh khoản.
- News Reader: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường.
- News Reader: Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động.
- News Reader: Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh.
- Chỉ lưu trích đoạn giới hạn để kiểm chứng nguồn; không lưu hay hiển thị toàn văn bài báo.
- Phân nhóm là keyword rule-based để định tuyến research, không phải sentiment hay dự báo tác động giá.
- Dữ liệu News Reader chỉ phục vụ research/report; không dùng làm feature train/backtest khi chưa có lịch sử available_at point-in-time.
- Tin live/trích đoạn cần mở URL gốc để kiểm chứng bối cảnh, số liệu và thời điểm trước khi sử dụng.

### Nguồn live research

- [Báo Pháp Luật Việt Nam] Tập đoàn Kido (KDC): Anh ruột lãnh đạo Kido bán ra hơn 400.000 cổ phiếu KDC, lãi quý II sụt giảm 60% - Báo Pháp Luật Việt Nam (2026-08-15T02:08:00+00:00): https://doanhnhan.baophapluat.vn/tap-doan-kido-kdc-anh-ruot-lanh-dao-kido-ban-ra-hon-400-000-co-phieu-kdc-lai-quy-ii-sut-giam-60.html
- [Tin nhanh chứng khoán] Sự kiện chứng khoán đáng chú ý ngày 14/8 - Tin nhanh chứng khoán (2026-08-13T11:07:57+00:00): https://m.tinnhanhchungkhoan.vn/su-kien-chung-khoan-dang-chu-y-ngay-148-post395879.amp

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.

---

## News model riêng từng mã

- Symbol-news report: `/Users/tranlekhoa/Documents/DATA_SCI/vn_stock_analysis/reports/KDC/2026-08-16_12-50-42/all_files/symbol_news_model`
- Số bài tin trong CSV cho mã: 2
- Số dòng giá có news feature: 1
- XGBoost probability mới nhất: 0.382
- AUC OOS: 0.520
- Balanced accuracy OOS: 0.494
- Backtest total return: 0.000
- Base XGBoost probability: 0.411
- Chênh lệch News-adjusted - Base: -0.029
- Áp vào signal chính: not_applied
- Trạng thái news model: research_only
- Gate chưa đạt: min_articles_60, min_feature_rows_30, news_feature_gain_positive, auc_at_least_0_55, balanced_accuracy_at_least_0_52

News-adjusted model hiện là lớp kiểm chứng/shadow; signal chính vẫn do `signal_decision.json` quyết định.

Lưu ý: news model dùng dữ liệu `available_at` point-in-time trong CSV tích lũy; nếu lịch sử tin còn mỏng thì chỉ xem là research/smoke test.
