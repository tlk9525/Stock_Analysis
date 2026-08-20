# Báo cáo ngày 2026-08-16 - SSB

## Tổng quan

- Dữ liệu: 2021-03-24 -> 2026-08-14, 1,347 phiên.
- Giá đóng cửa: 15.05 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Tiêu cực (điểm -9).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 44.5%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Model health: INSUFFICIENT_EDGE - Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 0/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định.
- Nếu chưa có cổ phiếu: INSUFFICIENT_EDGE - Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 0/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định.
- Nếu đang nắm giữ: REDUCE - Kỹ thuật chưa hỗ trợ và swing 5D chưa có edge; ưu tiên giảm rủi ro.

## Phân tích kỹ thuật

- SMA20 15.43; SMA60 15.30; RSI14 39.1.
- MACD -0.105; đường tín hiệu -0.059; biểu đồ cột -0.046.
- ATR14 0.37; ATR% 2.4%; ADX14 41.0.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Cẩn thận - MACD dưới signal, histogram âm.
- RSI14: Yếu - RSI 39.1.
- Bollinger: Gần biên dưới - Giá sát/vượt biên dưới.
- ADX: Xu hướng giảm - ADX 41.0, -DI vượt +DI.
- Thanh khoản: Bình thường - 1.12 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: SeABank.
- Ngành: Banks.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 17.29.
- P/B: 1.22.
- ROE: 7.3%.
- ROA: 0.7%.
- Market cap: 51,603.4 tỷ.
- Revenue Growth: -7.5%.
- Profit Growth: -12.6%.
- P/E 17.29: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 1.22: nên đọc cùng ROE và đặc thù ngành.
- ROE 7.3%: hiệu quả vốn còn yếu.
- Debt/Equity 9.12: đòn bẩy cao, cần đọc theo ngành.
- NPL 2.2%: cần theo dõi.
- Revenue Growth -7.5% YoY.
- Profit Growth -12.6% YoY.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.04 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-14T06:54:00+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2025-04-01 -> 2026-08-13.
- XGBoost: độ chính xác cân bằng 0.509; AUC 0.511; log-loss 0.692.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.538; AUC 0.514.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 73.
- Thẩm định: expanding_walk_forward; 3 lần chia; khoảng cách 1 phiên.

## Chiến lược swing 5 phiên: contract phát hành tín hiệu

### Khuyến nghị hành động sau phí

| Mục | Kết quả | Diễn giải |
|---|---:|---|
| Lệnh mới hôm nay | 0 lệnh | Không DCA hoặc chia nhỏ lệnh khi fixed-horizon swing chưa qua publish gate. |
| Trạng thái edge 5D | INSUFFICIENT_EDGE | Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 0/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định. |
| Nếu chưa có cổ phiếu | INSUFFICIENT_EDGE | Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 0/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định. |
| Nếu đang nắm giữ | REDUCE | Kỹ thuật chưa hỗ trợ và swing 5D chưa có edge; ưu tiên giảm rủi ro. |
| Expected excess return 5D | +0.1% | Cần vượt chi phí + margin 1.0%. |
| Mẫu frozen holdout | 0/10 trade | Chưa đủ số trade thì không có kết luận lợi nhuận/Sharpe và không được trade live. |
| Kỹ thuật / tin | -9 điểm | Tiêu cực; news warning: không. |

- Target: signal after close[t]; enter open[t+1]; exit close[t+5] ; target is stock return minus VNINDEX return over the same window
- Expected excess return mới nhất: +0.1%; safety margin đã chọn 0.5%.
- Frozen holdout: 0/10 trade; net/Sharpe chỉ được kết luận khi đủ mẫu.
- Publish gate swing: CHƯA ĐẠT. Gate yêu cầu sample/ranking dương ở development+frozen, net/Sharpe dương và stress phí 1.5×; chưa đạt thì giữ NO_EDGE.
- Các file audit: swing_development_oos.csv, swing_frozen_holdout.csv, swing_development_backtest.csv, swing_frozen_backtest.csv và file trades tương ứng.
- Mức độ quan trọng của đặc trưng: stoch_k_14=7.50; day_of_week=7.11; volatility_20d=7.09; volume_z_20=7.06; relative_strength_20d=6.93; return_3d=6.75.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 14.65; mục tiêu 1 15.90; mục tiêu 2 16.38.
- Tỷ lệ lợi nhuận/rủi ro 1.64; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- Phương pháp: XGBoost direct quantile 5/10/20D + conformal calibration; toàn bộ horizon qua gate: chưa.
- P50 cuối kỳ 14.95 (-0.68%).
- P10/P90 cuối kỳ 13.77 / 16.38.
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
- Điều kiện phát hành tín hiệu: Cận dưới expected excess return -0.03876389602846586 (dự báo điểm 0.0009016630938276649) chưa vượt chi phí + margin 0.0100..
- Điều kiện phát hành tín hiệu: Technical score -9 < 2..
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Tiêu cực.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 44.5%.
- Mô hình Logistic đối chứng: 50.7%.
- Quantile forecast ước tính xác suất return cuối kỳ dương từ residual frozen holdout: 42.9%.
- Mức dừng lỗ tham chiếu 14.65, mục tiêu 1 15.90, tỷ lệ lợi nhuận/rủi ro 1.64.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. News Reader đã trích đoạn có nguồn của 4 bài để phân loại chủ đề (ket_qua_kinh_doanh: 1, co_tuc_va_hanh_dong_doanh_nghiep: 1, vi_mo: 2, nganh: 3, rui_ro: 1), nhưng các trích đoạn này không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Tiêu cực; điểm -9. Chi tiết artifact: Xu hướng: Cẩn thận (Giá nằm dưới SMA60.); MACD: Cẩn thận (MACD dưới signal, histogram âm.); RSI14: Yếu (RSI 39.1.); Bollinger: Gần biên dưới (Giá sát/vượt biên dưới.); ADX: Xu hướng giảm (ADX 41.0, -DI vượt +DI.); Thanh khoản: Bình thường (1.12 lần trung bình.); Stochastic: Yếu lại (%K nằm dưới %D.)
- Góc nhìn cơ bản: Artifact cơ bản: SeABank; kỳ 2026-Q2; P/E 17.29; P/B 1.22; ROE 7.3%; ROA 0.7%; Debt/Equity 9.12; Revenue Growth -7.5%; Profit Growth -12.6%.
- Tin doanh nghiệp: Đã đọc trích đoạn giới hạn của 4 bài; phân nhóm rule-based: ket_qua_kinh_doanh: 1, co_tuc_va_hanh_dong_doanh_nghiep: 1, vi_mo: 2, nganh: 3, rui_ro: 1. Tác động cần kiểm chứng: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường. Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động. Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh. So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp. Xác minh công bố chính thức, phạm vi ảnh hưởng và khả năng định lượng rủi ro. Đây không phải sentiment hay dự báo tác động giá.
- Live research: Live snapshot lấy lúc 2026-08-16T06:17:26.699261+00:00; News Reader đọc được 4 bài. ML có 8 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest.

### Bằng chứng

- ML decision artifact: NO_EDGE. Không có margin nào đạt số trade tối thiểu trong validation; strict no-entry fallback không phải rule đã chọn.
- ML decision artifact: NO_EDGE. Development OOS chỉ có 0 trade; cần >= 10.
- ML decision artifact: NO_EDGE. Frozen holdout chỉ có 0 trade; cần >= 10.
- ML decision artifact: NO_EDGE. Correlation dự báo-return development OOS không dương.
- ML decision artifact: NO_EDGE. Frozen holdout chưa có lợi thế ròng và Sharpe dương sau phí.
- ML decision artifact: NO_EDGE. Frozen holdout không chịu được stress phí 1.5x.
- ML decision artifact: NO_EDGE. Cận dưới expected excess return -0.03876389602846586 (dự báo điểm 0.0009016630938276649) chưa vượt chi phí + margin 0.0100.
- ML decision artifact: NO_EDGE. Technical score -9 < 2.
- News Reader [Chứng khoán DNSE]: Cổ phiếu SSB của SeABank được lựa chọn vào rổ MSCI Frontier Markets Index - Chứng khoán DNSE | nhóm: nganh (2026-08-14T09:28:00+00:00)
- News Reader [BÁO SÀI GÒN GIẢI PHÓNG]: 3 ngân hàng Việt Nam được thêm vào rổ MSCI Frontier Markets - BÁO SÀI GÒN GIẢI PHÓNG | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo (2026-08-14T08:20:02+00:00)
- News Reader [Thời báo Tài chính Việt Nam]: ACB, SSB và MSB được thêm vào rổ MSCI Frontier Markets - Thời báo Tài chính Việt Nam | nhóm: vi_mo, nganh, rui_ro (2026-08-14T04:33:06+00:00)
- News Reader [VietnamBiz]: Ba cổ phiếu ngân hàng ACB, SSB, MSB vào rổ MSCI Frontier Markets - VietnamBiz | nhóm: nganh (2026-08-13T02:10:00+00:00)

### Rủi ro cần kiểm chứng

- ML guard: Không có margin nào đạt số trade tối thiểu trong validation; strict no-entry fallback không phải rule đã chọn.
- ML guard: Development OOS chỉ có 0 trade; cần >= 10.
- ML guard: Frozen holdout chỉ có 0 trade; cần >= 10.
- ML guard: Correlation dự báo-return development OOS không dương.
- ML guard: Frozen holdout chưa có lợi thế ròng và Sharpe dương sau phí.
- ML guard: Frozen holdout không chịu được stress phí 1.5x.
- ML guard: Cận dưới expected excess return -0.03876389602846586 (dự báo điểm 0.0009016630938276649) chưa vượt chi phí + margin 0.0100.
- ML guard: Technical score -9 < 2.
- News Reader: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường.
- News Reader: Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động.
- News Reader: Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh.
- News Reader: So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp.
- News Reader: Xác minh công bố chính thức, phạm vi ảnh hưởng và khả năng định lượng rủi ro.
- Chỉ lưu trích đoạn giới hạn để kiểm chứng nguồn; không lưu hay hiển thị toàn văn bài báo.
- Phân nhóm là keyword rule-based để định tuyến research, không phải sentiment hay dự báo tác động giá.
- Dữ liệu News Reader chỉ phục vụ research/report; không dùng làm feature train/backtest khi chưa có lịch sử available_at point-in-time.
- Tin live/trích đoạn cần mở URL gốc để kiểm chứng bối cảnh, số liệu và thời điểm trước khi sử dụng.

### Nguồn live research

- [Chứng khoán DNSE] Cổ phiếu SSB của SeABank được lựa chọn vào rổ MSCI Frontier Markets Index - Chứng khoán DNSE (2026-08-14T09:28:00+00:00): https://www.dnse.com.vn/senses/tin-tuc/co-phieu-ssb-cua-seabank-duoc-lua-chon-vao-ro-msci-frontier-markets-index-35269848
- [BÁO SÀI GÒN GIẢI PHÓNG] 3 ngân hàng Việt Nam được thêm vào rổ MSCI Frontier Markets - BÁO SÀI GÒN GIẢI PHÓNG (2026-08-14T08:20:02+00:00): https://www.sggp.org.vn/3-ngan-hang-viet-nam-duoc-them-vao-ro-msci-frontier-markets-post867037.html
- [Thời báo Tài chính Việt Nam] ACB, SSB và MSB được thêm vào rổ MSCI Frontier Markets - Thời báo Tài chính Việt Nam (2026-08-14T04:33:06+00:00): https://thoibaotaichinhvietnam.vn/acb-ssb-va-msb-duoc-them-vao-ro-msci-frontier-markets-202280.html
- [VietnamBiz] Ba cổ phiếu ngân hàng ACB, SSB, MSB vào rổ MSCI Frontier Markets - VietnamBiz (2026-08-13T02:10:00+00:00): https://vietnambiz.vn/ba-co-phieu-ngan-hang-acb-ssb-msb-vao-ro-msci-frontier-markets-202681384052351.htm

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.

---

## News model riêng từng mã

- Symbol-news report: `/Users/tranlekhoa/Documents/DATA_SCI/vn_stock_analysis/reports/SSB/2026-08-16_13-17-16/all_files/symbol_news_model`
- Số bài tin trong CSV cho mã: 7
- Số dòng giá có news feature: 5
- XGBoost probability mới nhất: 0.511
- AUC OOS: 0.564
- Balanced accuracy OOS: 0.499
- Backtest total return: 0.000
- Base XGBoost probability: 0.445
- Chênh lệch News-adjusted - Base: +0.066
- Áp vào signal chính: not_applied
- Trạng thái news model: research_only
- Gate chưa đạt: min_articles_60, min_feature_rows_30, news_feature_gain_positive, balanced_accuracy_at_least_0_52

News-adjusted model hiện là lớp kiểm chứng/shadow; signal chính vẫn do `signal_decision.json` quyết định.

Lưu ý: news model dùng dữ liệu `available_at` point-in-time trong CSV tích lũy; nếu lịch sử tin còn mỏng thì chỉ xem là research/smoke test.
