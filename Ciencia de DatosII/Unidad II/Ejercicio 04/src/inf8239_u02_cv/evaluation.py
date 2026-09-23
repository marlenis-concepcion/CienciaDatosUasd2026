from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix, f1_score, precision_recall_fscore_support

from .data import CLASS_NAMES


def per_class(y_true, y_pred) -> pd.DataFrame:
    precision, recall, f1, support = precision_recall_fscore_support(
        y_true, y_pred, labels=range(10), zero_division=0
    )
    return pd.DataFrame({"clase": CLASS_NAMES, "precision": precision, "recall": recall,
                         "f1": f1, "soporte": support, "errores": support - np.round(recall * support).astype(int)})


def top_confusions(y_true, y_pred, n: int = 8) -> pd.DataFrame:
    matrix = confusion_matrix(y_true, y_pred, labels=range(10))
    np.fill_diagonal(matrix, 0)
    pairs = [(CLASS_NAMES[i], CLASS_NAMES[j], int(matrix[i, j])) for i in range(10) for j in range(10) if matrix[i, j]]
    table = pd.DataFrame(pairs, columns=["real", "predicha", "errores"])
    return table.sort_values("errores", ascending=False).head(n).reset_index(drop=True)


def choose(valid: dict[str, dict], tolerance: float = 0.01) -> tuple[str, str]:
    """Elige el modelo con menos parámetros cuyo F1 macro de validación esté a menos de `tolerance` del mejor."""
    best = max(v["f1_macro"] for v in valid.values())
    eligible = {k: v for k, v in valid.items() if best - v["f1_macro"] < tolerance}
    chosen = min(eligible, key=lambda k: (valid[k]["parametros"], k))
    return chosen, (f"F1 macro de validación máximo {best:.4f}; dentro de la tolerancia {tolerance}: "
                    f"{', '.join(sorted(eligible))}. Se elige el de menos parámetros: {chosen}.")


def f1_macro(y_true, y_pred) -> float:
    return float(f1_score(y_true, y_pred, average="macro"))
