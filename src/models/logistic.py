from __future__ import annotations

import numpy as np
import pandas as pd


def sigmoid(values: np.ndarray) -> np.ndarray:
    return 1 / (1 + np.exp(-np.clip(values, -35, 35)))


def fit_logistic(
    x_train: pd.DataFrame,
    y_train: pd.Series,
    iterations: int = 2500,
    learning_rate: float = 0.08,
    l2: float = 0.01,
) -> dict:
    features = x_train.to_numpy(dtype=float)
    labels = y_train.to_numpy(dtype=float)
    mean = np.nanmean(features, axis=0)
    standard_deviation = np.nanstd(features, axis=0)
    standard_deviation[standard_deviation == 0] = 1
    scaled = (features - mean) / standard_deviation
    augmented = np.column_stack([np.ones(len(scaled)), scaled])

    weights = np.zeros(augmented.shape[1])
    positive_count = max(float(labels.sum()), 1.0)
    negative_count = max(float(len(labels) - labels.sum()), 1.0)
    positive_weight = len(labels) / (2 * positive_count)
    negative_weight = len(labels) / (2 * negative_count)
    row_weights = np.where(labels == 1, positive_weight, negative_weight)

    for _ in range(iterations):
        probability = sigmoid(augmented @ weights)
        error = (probability - labels) * row_weights
        gradient = (augmented.T @ error) / len(labels)
        gradient[1:] += l2 * weights[1:] / len(labels)
        weights -= learning_rate * gradient

    return {
        "weights": weights,
        "mean": mean,
        "standard_deviation": standard_deviation,
    }


def predict_logistic(model: dict, features: pd.DataFrame) -> np.ndarray:
    values = features.to_numpy(dtype=float)
    scaled = (values - model["mean"]) / model["standard_deviation"]
    augmented = np.column_stack([np.ones(len(scaled)), scaled])
    return sigmoid(augmented @ model["weights"])

