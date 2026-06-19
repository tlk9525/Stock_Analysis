from __future__ import annotations

import numpy as np
import pandas as pd

from src.features.technical import MODEL_FEATURES
from src.models.logistic import fit_logistic, predict_logistic
from src.models.metrics import binary_metrics, classification_metrics


def _split_data(
    frame: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    model_frame = frame.dropna(subset=MODEL_FEATURES + ["target_next_up"]).copy()
    labeled = model_frame.iloc[:-1]
    latest_features = model_frame.tail(1)[MODEL_FEATURES]
    if len(labeled) < 100 or latest_features.empty:
        raise ValueError(
            f"Khong du du lieu sach de train model: can toi thieu 100 dong, hien co {len(labeled)}."
        )

    split_index = int(len(labeled) * 0.8)
    training_pool = labeled.iloc[:split_index]
    test = labeled.iloc[split_index:]
    validation_size = max(int(len(training_pool) * 0.15), 30)
    train = training_pool.iloc[:-validation_size]
    validation = training_pool.iloc[-validation_size:]
    if train.empty or validation.empty or test.empty:
        raise ValueError("Khong tach duoc train/test theo thoi gian.")
    return train, validation, test, latest_features


def _xgboost_params(config: dict, labels: pd.Series) -> tuple[dict, dict]:
    options = config.get("xgboost", {})
    positives = max(float(labels.sum()), 1.0)
    negatives = max(float(len(labels) - labels.sum()), 1.0)
    params = {
        "objective": "binary:logistic",
        "eval_metric": "logloss",
        "tree_method": "hist",
        "eta": float(options.get("learning_rate", 0.03)),
        "max_depth": int(options.get("max_depth", 4)),
        "min_child_weight": float(options.get("min_child_weight", 3)),
        "subsample": float(options.get("subsample", 0.8)),
        "colsample_bytree": float(options.get("colsample_bytree", 0.8)),
        "lambda": float(options.get("reg_lambda", 1.0)),
        "alpha": float(options.get("reg_alpha", 0.05)),
        "scale_pos_weight": negatives / positives,
        "seed": int(options.get("random_state", 42)),
        "nthread": int(options.get("n_jobs", 4)),
    }
    training = {
        "num_boost_round": int(options.get("num_boost_round", 400)),
        "early_stopping_rounds": int(options.get("early_stopping_rounds", 40)),
    }
    return params, training


def _best_iteration(booster, default_rounds: int) -> int:
    try:
        return int(booster.best_iteration)
    except (AttributeError, TypeError):
        return default_rounds - 1


def train_models(
    frame: pd.DataFrame,
    config: dict,
) -> tuple[dict, pd.DataFrame, dict, object]:
    try:
        import xgboost as xgb
    except Exception as exc:
        raise RuntimeError(
            "Khong nap duoc XGBoost. Hay chay ./setup_env.sh va cai OpenMP tren macOS."
        ) from exc

    train, validation, test, latest_features = _split_data(frame)
    x_train = train[MODEL_FEATURES]
    y_train = train["target_next_up"]
    x_validation = validation[MODEL_FEATURES]
    y_validation = validation["target_next_up"]
    x_test = test[MODEL_FEATURES]
    y_test = test["target_next_up"]

    params, training_options = _xgboost_params(config, y_train)
    train_matrix = xgb.DMatrix(x_train, label=y_train, feature_names=MODEL_FEATURES)
    validation_matrix = xgb.DMatrix(
        x_validation,
        label=y_validation,
        feature_names=MODEL_FEATURES,
    )
    evaluation_history: dict = {}
    tuning_booster = xgb.train(
        params=params,
        dtrain=train_matrix,
        num_boost_round=training_options["num_boost_round"],
        evals=[(train_matrix, "train"), (validation_matrix, "validation")],
        evals_result=evaluation_history,
        early_stopping_rounds=training_options["early_stopping_rounds"],
        verbose_eval=False,
    )
    best_iteration = _best_iteration(
        tuning_booster,
        training_options["num_boost_round"],
    )
    best_rounds = best_iteration + 1

    training_pool = pd.concat([train, validation])
    evaluation_params, _ = _xgboost_params(
        config,
        training_pool["target_next_up"],
    )
    training_pool_matrix = xgb.DMatrix(
        training_pool[MODEL_FEATURES],
        label=training_pool["target_next_up"],
        feature_names=MODEL_FEATURES,
    )
    evaluation_booster = xgb.train(
        params=evaluation_params,
        dtrain=training_pool_matrix,
        num_boost_round=best_rounds,
        verbose_eval=False,
    )
    test_matrix = xgb.DMatrix(x_test, label=y_test, feature_names=MODEL_FEATURES)
    xgboost_probability = evaluation_booster.predict(test_matrix)
    xgboost_prediction = (xgboost_probability >= 0.5).astype(int)

    scored_test = test.copy()
    scored_test["xgboost_prediction"] = xgboost_prediction
    scored_test["xgboost_prob_up"] = xgboost_probability

    importance = evaluation_booster.get_score(importance_type="gain")
    feature_importance = {
        feature: float(importance.get(feature, 0.0))
        for feature in MODEL_FEATURES
    }
    feature_importance = dict(
        sorted(feature_importance.items(), key=lambda item: item[1], reverse=True)
    )

    xgboost_metrics = classification_metrics(y_test, xgboost_probability)
    xgboost_metrics.update(
        {
            "best_iteration": best_iteration,
            "feature_importance_gain": feature_importance,
            "train_logloss_at_best": float(
                evaluation_history["train"]["logloss"][best_iteration]
            ),
            "validation_logloss_at_best": float(
                evaluation_history["validation"]["logloss"][best_iteration]
            ),
        }
    )

    logistic_model = fit_logistic(
        training_pool[MODEL_FEATURES],
        training_pool["target_next_up"],
    )
    logistic_probability = predict_logistic(logistic_model, x_test)
    scored_test["logistic_prediction"] = (logistic_probability >= 0.5).astype(int)
    scored_test["logistic_prob_up"] = logistic_probability

    majority_class = int(training_pool["target_next_up"].mode().iloc[0])
    majority_prediction = np.full(len(y_test), majority_class)

    all_labeled = pd.concat([train, validation, test])
    final_params, _ = _xgboost_params(config, all_labeled["target_next_up"])
    final_matrix = xgb.DMatrix(
        all_labeled[MODEL_FEATURES],
        label=all_labeled["target_next_up"],
        feature_names=MODEL_FEATURES,
    )
    final_booster = xgb.train(
        params=final_params,
        dtrain=final_matrix,
        num_boost_round=best_rounds,
        verbose_eval=False,
    )
    latest_matrix = xgb.DMatrix(latest_features, feature_names=MODEL_FEATURES)
    latest_xgboost_probability = float(final_booster.predict(latest_matrix)[0])

    final_logistic = fit_logistic(
        all_labeled[MODEL_FEATURES],
        all_labeled["target_next_up"],
    )
    latest_logistic_probability = float(
        predict_logistic(final_logistic, latest_features)[0]
    )

    metrics = {
        "split": {
            "train_start": str(train.index.min().date()),
            "train_end": str(train.index.max().date()),
            "validation_start": str(validation.index.min().date()),
            "validation_end": str(validation.index.max().date()),
            "test_start": str(test.index.min().date()),
            "test_end": str(test.index.max().date()),
            "train_rows": int(len(train)),
            "validation_rows": int(len(validation)),
            "test_rows": int(len(test)),
        },
        "xgboost": xgboost_metrics,
        "logistic_baseline": classification_metrics(y_test, logistic_probability),
        "majority_baseline": {
            "class": majority_class,
            **binary_metrics(y_test, majority_prediction),
        },
    }
    latest_probabilities = {
        "xgboost": latest_xgboost_probability,
        "logistic_regression": latest_logistic_probability,
    }
    return metrics, scored_test, latest_probabilities, final_booster
