from __future__ import annotations

import numpy as np
import pandas as pd


def _as_array(values, dtype) -> np.ndarray:
    if isinstance(values, (pd.Series, pd.Index)):
        return values.to_numpy(dtype=dtype)
    return np.asarray(values, dtype=dtype)


def _validate_pair(y_true, values) -> tuple[np.ndarray, np.ndarray]:
    raw_y = _as_array(y_true, float)
    compared = _as_array(values, float)
    if raw_y.ndim != 1 or compared.ndim != 1:
        raise ValueError("Metrics chỉ hỗ trợ dữ liệu một chiều.")
    if len(raw_y) != len(compared):
        raise ValueError("Nhãn và dự báo phải có cùng số dòng.")
    if not len(raw_y):
        raise ValueError("Không thể tính metrics trên tập rỗng.")
    if not np.isfinite(raw_y).all() or not np.isin(raw_y, [0, 1]).all():
        raise ValueError("Nhãn phân lớp phải là 0 hoặc 1.")
    if not np.isfinite(compared).all():
        raise ValueError("Dự báo chứa giá trị NaN hoặc vô cực.")
    return raw_y.astype(int), compared


def binary_metrics(y_true: pd.Series, predictions: np.ndarray) -> dict:
    y, raw_predictions = _validate_pair(y_true, predictions)
    if not np.isin(raw_predictions, [0, 1]).all():
        raise ValueError("Dự báo phân lớp phải là 0 hoặc 1.")
    predicted = raw_predictions.astype(int)
    tn = int(((y == 0) & (predicted == 0)).sum())
    fp = int(((y == 0) & (predicted == 1)).sum())
    fn = int(((y == 1) & (predicted == 0)).sum())
    tp = int(((y == 1) & (predicted == 1)).sum())
    accuracy = float((tp + tn) / max(len(y), 1))
    recall_0 = tn / max(tn + fp, 1)
    recall_1 = tp / max(tp + fn, 1)
    precision_1 = tp / max(tp + fp, 1)
    f1_1 = 2 * precision_1 * recall_1 / max(precision_1 + recall_1, 1e-12)
    return {
        "rows": int(len(y)),
        "accuracy": accuracy,
        "balanced_accuracy": float((recall_0 + recall_1) / 2),
        "precision": float(precision_1),
        "recall": float(recall_1),
        "f1": float(f1_1),
        "actual_positive_rate": float(y.mean()),
        "predicted_positive_rate": float(predicted.mean()),
        "confusion_matrix": [[tn, fp], [fn, tp]],
    }


def probability_metrics(y_true: pd.Series, probabilities: np.ndarray) -> dict:
    y, raw_probability = _validate_pair(y_true, probabilities)
    if ((raw_probability < 0) | (raw_probability > 1)).any():
        raise ValueError("Xác suất dự báo phải nằm trong [0, 1].")
    probability = np.clip(raw_probability, 1e-8, 1 - 1e-8)
    log_loss = -np.mean(y * np.log(probability) + (1 - y) * np.log(1 - probability))
    brier_score = np.mean((probability - y) ** 2)

    positives = int(y.sum())
    negatives = int(len(y) - positives)
    roc_auc = None
    if positives and negatives:
        ranks = pd.Series(probability).rank(method="average").to_numpy()
        positive_rank_sum = float(ranks[y == 1].sum())
        roc_auc = (positive_rank_sum - positives * (positives + 1) / 2) / (
            positives * negatives
        )

    return {
        "log_loss": float(log_loss),
        "brier_score": float(brier_score),
        "roc_auc": float(roc_auc) if roc_auc is not None else None,
    }


def classification_metrics(
    y_true: pd.Series,
    probabilities: np.ndarray,
    threshold: float = 0.5,
) -> dict:
    probability = _as_array(probabilities, float)
    predictions = (probability >= threshold).astype(int)
    return {
        **binary_metrics(y_true, predictions),
        **probability_metrics(y_true, probability),
        "threshold": threshold,
    }


def classification_metrics_by_fold(
    y_true,
    probabilities,
    fold_ids,
    threshold: float = 0.5,
) -> tuple[dict, list[dict]]:
    """Tính metrics OOS tổng và riêng cho từng fold theo thứ tự xuất hiện."""

    y, probability = _validate_pair(y_true, probabilities)
    folds = _as_array(fold_ids, object)
    if folds.ndim != 1 or len(folds) != len(y):
        raise ValueError("fold_ids phải là mảng một chiều cùng số dòng với dự báo.")

    overall = classification_metrics(pd.Series(y), probability, threshold)
    per_fold: list[dict] = []
    for fold_id in pd.unique(folds):
        selected = folds == fold_id
        fold_metrics = classification_metrics(
            pd.Series(y[selected]),
            probability[selected],
            threshold,
        )
        per_fold.append({"fold": int(fold_id), **fold_metrics})
    return overall, per_fold
