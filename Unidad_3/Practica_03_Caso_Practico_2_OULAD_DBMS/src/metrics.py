from __future__ import annotations

import numpy as np
from sklearn.metrics import confusion_matrix


def manual_binary_metrics(y_true, y_pred) -> dict[str, float]:
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
    accuracy = (tp + tn) / (tp + tn + fp + fn)
    return {
        "tp": int(tp),
        "fp": int(fp),
        "tn": int(tn),
        "fn": int(fn),
        "precision_manual": precision,
        "recall_manual": recall,
        "f1_manual": f1,
        "accuracy_manual": accuracy,
    }


def multiclass_mse_r2(y_true, y_pred) -> tuple[float, float]:
    true = np.asarray(y_true, dtype=float)
    pred = np.asarray(y_pred, dtype=float)
    mse = float(np.mean((true - pred) ** 2))
    denominator = float(np.sum((true - true.mean()) ** 2))
    r2 = 1 - float(np.sum((true - pred) ** 2)) / denominator if denominator else 0.0
    return mse, r2
