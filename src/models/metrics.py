from __future__ import annotations

import numpy as np
import pandas as pd


def binary_metrics(y_true: pd.Series, predictions: np.ndarray) -> dict:
    y = y_true.to_numpy(dtype=int)
    predicted = predictions.astype(int)
    tn = int(((y == 0) & (predicted == 0)).sum())
    fp = int(((y == 0) & (predicted == 1)).sum())
    fn = int(((y == 1) & (predicted == 0)).sum())
    tp = int(((y == 1) & (predicted == 1)).sum())
    accuracy = float((tp + tn) / max(len(y), 1))
    recall_0 = tn / max(tn + fp, 1)
    recall_1 = tp / max(tp + fn, 1)
    return {
        "accuracy": accuracy,
        "balanced_accuracy": float((recall_0 + recall_1) / 2),
        "confusion_matrix": [[tn, fp], [fn, tp]],
    }


def probability_metrics(y_true: pd.Series, probabilities: np.ndarray) -> dict:
    y = y_true.to_numpy(dtype=int)
    probability = np.clip(probabilities.astype(float), 1e-8, 1 - 1e-8)
    log_loss = -np.mean(y * np.log(probability) + (1 - y) * np.log(1 - probability))
    brier_score = np.mean((probability - y) ** 2)

    positives = int(y.sum())
    negatives = int(len(y) - positives)
    roc_auc = None
    if positives and negatives:
        ranks = pd.Series(probability).rank(method="average").to_numpy()
        positive_rank_sum = float(ranks[y == 1].sum())
        roc_auc = (
            positive_rank_sum - positives * (positives + 1) / 2
        ) / (positives * negatives)

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
    predictions = (probabilities >= threshold).astype(int)
    return {
        **binary_metrics(y_true, predictions),
        **probability_metrics(y_true, probabilities),
        "threshold": threshold,
    }

