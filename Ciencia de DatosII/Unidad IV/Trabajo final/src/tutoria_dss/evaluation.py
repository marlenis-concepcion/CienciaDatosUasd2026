"""Métricas a capacidad: la coordinación solo puede atender a una fracción de la cohorte."""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score, roc_auc_score


def top_k_mask(scores: np.ndarray, share: float) -> np.ndarray:
    """Marca los k = ceil(share · n) puntajes más altos; desempate estable por posición."""
    k = int(np.ceil(share * len(scores)))
    order = np.argsort(-np.asarray(scores), kind="stable")[:k]
    mask = np.zeros(len(scores), dtype=bool)
    mask[order] = True
    return mask


def at_capacity(y: np.ndarray, scores: np.ndarray, share: float) -> dict:
    y = np.asarray(y)
    selected = top_k_mask(scores, share)
    hits = int((selected & (y == 1)).sum())
    return {"seleccionados": int(selected.sum()), "aciertos": hits,
            "precision_capacidad": hits / max(int(selected.sum()), 1),
            "recall_capacidad": hits / max(int((y == 1).sum()), 1),
            "auc": float(roc_auc_score(y, scores)), "average_precision": float(average_precision_score(y, scores))}


def compare(y: np.ndarray, candidates: dict[str, np.ndarray], share: float) -> pd.DataFrame:
    return pd.DataFrame([{"alternativa": name, **at_capacity(y, s, share)} for name, s in candidates.items()])


def choose(valid_table: pd.DataFrame) -> str:
    """Regla fijada antes de la prueba: mayor recall a capacidad en validación; desempate por average precision."""
    ranked = valid_table[valid_table["alternativa"] != "aleatorio"].sort_values(
        ["recall_capacidad", "average_precision"], ascending=False)
    return str(ranked.iloc[0]["alternativa"])


def error_profile(df: pd.DataFrame, scores: np.ndarray, share: float) -> pd.DataFrame:
    """Abandonos reales que quedaron fuera de los cupos (falsos negativos), comparados con los alcanzados."""
    selected = top_k_mask(scores, share)
    dropouts = df.assign(alcanzado=selected)[df["abandono"] == 1]
    cols = ["Curricular units 1st sem (approved)", "Curricular units 1st sem (grade)", "Tuition fees up to date",
            "Debtor", "Admission grade", "Curricular units 1st sem (enrolled)"]
    return dropouts.groupby("alcanzado")[cols].mean().rename(index={True: "alcanzado", False: "no alcanzado"}).T
