# Báo cáo ngày 2026-08-13 - VCB

## Tổng quan

- Dữ liệu: 2009-06-30 -> 2026-08-13, 4,274 phiên.
- Giá đóng cửa: 59.50 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng (điểm 2).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 50.6%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Model health: INSUFFICIENT_EDGE - Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 2/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định.
- Nếu chưa có cổ phiếu: INSUFFICIENT_EDGE - Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 2/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định.
- Nếu đang nắm giữ: HOLD_DISCIPLINED - Nếu đã nắm giữ: giữ theo stop-loss, không mua thêm khi swing 5D chưa đủ edge.

## Phân tích kỹ thuật

- SMA20 57.46; SMA60 59.92; RSI14 54.5.
- MACD 0.275; đường tín hiệu -0.154; biểu đồ cột 0.429.
- ATR14 1.38; ATR% 2.3%; ADX14 25.5.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Trung tính - RSI 54.5.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng tăng - ADX 25.5, +DI vượt -DI.
- Thanh khoản: Bình thường - 0.88 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: Vietcombank.
- Ngành: Banks.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 11.98.
- P/B: 2.01.
- ROE: 17.9%.
- ROA: 1.7%.
- Market cap: 498,833.8 tỷ.
- Revenue Growth: 47.6%.
- Profit Growth: 64.7%.
- P/E 11.98: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 2.01: nên đọc cùng ROE và đặc thù ngành.
- ROE 17.9%: hiệu quả vốn chủ sở hữu tốt.
- Debt/Equity 9.69: đòn bẩy cao, cần đọc theo ngành.
- NPL 0.6%: đang ở mức kiểm soát.
- Revenue Growth 47.6% YoY.
- Profit Growth 64.7% YoY.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.12 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-06T09:03:02+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-11-22 -> 2026-08-12.
- XGBoost: độ chính xác cân bằng 0.504; AUC 0.469; log-loss 0.699.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.478; AUC 0.490.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 30.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.

## Chiến lược swing 5 phiên: contract phát hành tín hiệu

### Khuyến nghị hành động sau phí

| Mục | Kết quả | Diễn giải |
|---|---:|---|
| Lệnh mới hôm nay | 0 lệnh | Không DCA hoặc chia nhỏ lệnh khi fixed-horizon swing chưa qua publish gate. |
| Trạng thái edge 5D | INSUFFICIENT_EDGE | Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 2/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định. |
| Nếu chưa có cổ phiếu | INSUFFICIENT_EDGE | Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 2/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định. |
| Nếu đang nắm giữ | HOLD_DISCIPLINED | Nếu đã nắm giữ: giữ theo stop-loss, không mua thêm khi swing 5D chưa đủ edge. |
| Expected excess return 5D | +0.1% | Cần vượt chi phí + margin 0.6%. |
| Mẫu frozen holdout | 2/10 trade | Chưa đủ số trade thì không có kết luận lợi nhuận/Sharpe và không được trade live. |
| Kỹ thuật / tin | 2 điểm | Hồi phục / nghiêng tăng; news warning: không. |

- Target: signal after close[t]; enter open[t+1]; exit close[t+5] ; target is stock return minus VNINDEX return over the same window
- Expected excess return mới nhất: +0.1%; safety margin đã chọn 0.1%.
- Frozen holdout: 2/10 trade; net/Sharpe chỉ được kết luận khi đủ mẫu.
- Publish gate swing: CHƯA ĐẠT. Gate yêu cầu sample/ranking dương ở development+frozen, net/Sharpe dương và stress phí 1.5×; chưa đạt thì giữ NO_EDGE.
- Các file audit: swing_development_oos.csv, swing_frozen_holdout.csv, swing_development_backtest.csv, swing_frozen_backtest.csv và file trades tương ứng.
- Mức độ quan trọng của đặc trưng: rsi_14=14.50; return_1d=11.21; market_return_20d=10.74; month_of_year=10.66; market_return_5d=10.61; day_of_week=10.47.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 59.32; mục tiêu 1 61.00; mục tiêu 2 66.49.
- Tỷ lệ lợi nhuận/rủi ro 2.50; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 58.60 (-1.51%).
- P10/P90 cuối kỳ 53.64 / 66.49.
- Lịch giao dịch: VN stock calendar: loại Thứ Bảy/Chủ Nhật và các ngày nghỉ 2026 đã công bố; ngày làm bù Thứ Bảy không được tính là phiên giao dịch chứng khoán.
- Ngày nghỉ đã loại khỏi forecast: 2026-01-01, 2026-01-02, 2026-02-16, 2026-02-17, 2026-02-18, 2026-02-19, 2026-02-20, 2026-04-27, 2026-04-30, 2026-05-01, 2026-08-31, 2026-09-01, 2026-09-02.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: Không có margin nào đạt số trade tối thiểu trong validation; strict no-entry fallback không phải rule đã chọn..
- Điều kiện phát hành tín hiệu: Frozen holdout chỉ có 2 trade; cần >= 10..
- Điều kiện phát hành tín hiệu: Expected excess return 0.0009368061437271535 chưa vượt chi phí + margin 0.0063..
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 50.6%.
- Mô hình Logistic đối chứng: 50.0%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 42.0%.
- Mức dừng lỗ tham chiếu 59.32, mục tiêu 1 61.00, tỷ lệ lợi nhuận/rủi ro 2.50.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. News Reader đã trích đoạn có nguồn của 2 bài để phân loại chủ đề (ket_qua_kinh_doanh: 1, co_tuc_va_hanh_dong_doanh_nghiep: 1, vi_mo: 1, nganh: 1), nhưng các trích đoạn này không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Hồi phục / nghiêng tăng; điểm 2. Chi tiết artifact: Xu hướng: Cẩn thận (Giá nằm dưới SMA60.); MACD: Tích cực (MACD trên signal, histogram dương.); RSI14: Trung tính (RSI 54.5.); Bollinger: Ổn định (Giá nằm trong dải Bollinger.); ADX: Xu hướng tăng (ADX 25.5, +DI vượt -DI.); Thanh khoản: Bình thường (0.88 lần trung bình.); Stochastic: Yếu lại (%K nằm dưới %D.)
- Góc nhìn cơ bản: Artifact cơ bản: Vietcombank; kỳ 2026-Q2; P/E 11.98; P/B 2.01; ROE 17.9%; ROA 1.7%; Debt/Equity 9.69; Revenue Growth 47.6%; Profit Growth 64.7%.
- Tin doanh nghiệp: Đã đọc trích đoạn giới hạn của 2 bài; phân nhóm rule-based: ket_qua_kinh_doanh: 1, co_tuc_va_hanh_dong_doanh_nghiep: 1, vi_mo: 1, nganh: 1. Tác động cần kiểm chứng: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường. Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động. Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh. So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp. Đây không phải sentiment hay dự báo tác động giá.
- Live research: Live snapshot lấy lúc 2026-08-13T16:51:53.086583+00:00; News Reader đọc được 2 bài. ML có 3 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest.

### Bằng chứng

- ML decision artifact: NO_EDGE. Không có margin nào đạt số trade tối thiểu trong validation; strict no-entry fallback không phải rule đã chọn.
- ML decision artifact: NO_EDGE. Frozen holdout chỉ có 2 trade; cần >= 10.
- ML decision artifact: NO_EDGE. Expected excess return 0.0009368061437271535 chưa vượt chi phí + margin 0.0063.
- News Reader [bnews.vn]: Chứng khoán hôm nay: Khuyến nghị mua DMX, POW và chờ mua VCB - bnews.vn | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh (2026-08-07T01:19:00+00:00)
- News Reader [nguoiquansat.vn]: Dòng vốn thụ động 1,5 tỷ USD theo FTSE dự kiến vào Việt Nam qua 4 đợt: VIC, VHM, VCB, HPG, LPB, STB... được phân bổ ra sao? - nguoiquansat.vn | nhóm: khác (2026-08-12T07:33:01+00:00)

### Rủi ro cần kiểm chứng

- ML guard: Không có margin nào đạt số trade tối thiểu trong validation; strict no-entry fallback không phải rule đã chọn.
- ML guard: Frozen holdout chỉ có 2 trade; cần >= 10.
- ML guard: Expected excess return 0.0009368061437271535 chưa vượt chi phí + margin 0.0063.
- News Reader: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường.
- News Reader: Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động.
- News Reader: Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh.
- News Reader: So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp.
- Chỉ lưu trích đoạn giới hạn để kiểm chứng nguồn; không lưu hay hiển thị toàn văn bài báo.
- Phân nhóm là keyword rule-based để định tuyến research, không phải sentiment hay dự báo tác động giá.
- Dữ liệu News Reader chỉ phục vụ research/report; không dùng làm feature train/backtest khi chưa có lịch sử available_at point-in-time.
- Tin live/trích đoạn cần mở URL gốc để kiểm chứng bối cảnh, số liệu và thời điểm trước khi sử dụng.

### Nguồn live research

- [bnews.vn] Chứng khoán hôm nay: Khuyến nghị mua DMX, POW và chờ mua VCB - bnews.vn (2026-08-07T01:19:00+00:00): https://bnews.vn/chung-khoan-hom-nay-khuyen-nghi-mua-dmx-pow-va-cho-mua-vcb/431720.html
- [nguoiquansat.vn] Dòng vốn thụ động 1,5 tỷ USD theo FTSE dự kiến vào Việt Nam qua 4 đợt: VIC, VHM, VCB, HPG, LPB, STB... được phân bổ ra sao? - nguoiquansat.vn (2026-08-12T07:33:01+00:00): https://nguoiquansat.vn/dong-von-thu-dong-1-5-ty-usd-theo-ftse-du-kien-vao-viet-nam-qua-4-dot-vic-vhm-vcb-hpg-lpb-stb-duoc-phan-bo-ra-sao-310061.html

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.

---

## News model riêng từng mã

- Symbol-news report: `/Users/tranlekhoa/Documents/DATA_SCI/vn_stock_analysis/reports/VCB/2026-08-13_23-51-35/all_files/symbol_news_model`
- Số bài tin trong CSV cho mã: 7
- Số dòng giá có news feature: 10
- XGBoost probability mới nhất: 0.505
- AUC OOS: 0.456
- Balanced accuracy OOS: 0.499
- Backtest total return: 0.000
- Base XGBoost probability: 0.506
- Chênh lệch News-adjusted - Base: -0.000
- Áp vào signal chính: not_applied
- Trạng thái news model: research_only
- Gate chưa đạt: min_articles_60, min_feature_rows_30, news_feature_gain_positive, auc_at_least_0_55, balanced_accuracy_at_least_0_52

News-adjusted model hiện là lớp kiểm chứng/shadow; signal chính vẫn do `signal_decision.json` quyết định.

Lưu ý: news model dùng dữ liệu `available_at` point-in-time trong CSV tích lũy; nếu lịch sử tin còn mỏng thì chỉ xem là research/smoke test.
