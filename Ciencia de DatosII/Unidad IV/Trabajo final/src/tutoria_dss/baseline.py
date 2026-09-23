"""Baseline de reglas: sin aprendizaje, fácil de explicar."""
from __future__ import annotations

import numpy as np
import pandas as pd


def rule_score(df: pd.DataFrame) -> np.ndarray:
    """Puntaje de riesgo: menos unidades aprobadas del 1.er semestre y matrícula atrasada suben la prioridad."""
    enrolled = df["Curricular units 1st sem (enrolled)"].clip(lower=1)
    failed_share = 1 - (df["Curricular units 1st sem (approved)"] / enrolled).clip(0, 1)
    return (failed_share + (1 - df["Tuition fees up to date"]) + 0.5 * df["Debtor"]).to_numpy(dtype=float)
