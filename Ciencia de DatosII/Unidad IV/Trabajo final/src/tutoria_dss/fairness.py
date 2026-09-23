"""Auditoría responsable: recall a capacidad por grupo, intersecciones, incertidumbre y compuertas."""
from __future__ import annotations

import numpy as np
import pandas as pd

from .evaluation import top_k_mask


def age_band(age: pd.Series) -> pd.Series:
    return pd.cut(age, [0, 20, 25, 200], labels=["≤20", "21-25", ">25"], right=True).astype(str)


def audit_groups(df: pd.DataFrame) -> pd.DataFrame:
    """Columnas de auditoría legibles; no se usan en el modelo."""
    return pd.DataFrame({
        "genero": df["Gender"].map({0: "mujer", 1: "hombre"}),
        "edad": age_band(df["Age at enrollment"]),
        "beca": df["Scholarship holder"].map({0: "sin beca", 1: "becario"}),
    }, index=df.index)


def by_group(y: np.ndarray, selected: np.ndarray, groups: pd.Series, min_size: int = 30) -> pd.DataFrame:
    frame = pd.DataFrame({"y": np.asarray(y), "sel": np.asarray(selected), "g": np.asarray(groups)})
    rows = []
    for name, part in frame.groupby("g"):
        positives = int(part["y"].sum())
        rows.append({"grupo": name, "n": len(part), "abandonos": positives,
                     "tasa_abandono": part["y"].mean(), "seleccion": part["sel"].mean(),
                     "recall_capacidad": (part["sel"] & (part["y"] == 1)).sum() / positives if positives else np.nan,
                     "precision_capacidad": part.loc[part["sel"], "y"].mean() if part["sel"].any() else np.nan,
                     "n_suficiente": positives >= min_size})
    return pd.DataFrame(rows)


def recall_gap(table: pd.DataFrame) -> float:
    valid = table[table["n_suficiente"]]["recall_capacidad"].dropna()
    return float(valid.max() - valid.min()) if len(valid) > 1 else 0.0


def bootstrap_gap(y, scores, groups, share: float, min_size: int, n: int = 500, seed: int = 42) -> list[float]:
    rng = np.random.default_rng(seed)
    y, scores, groups = np.asarray(y), np.asarray(scores), np.asarray(groups)
    gaps = []
    for _ in range(n):
        idx = rng.integers(0, len(y), len(y))
        gaps.append(recall_gap(by_group(y[idx], top_k_mask(scores[idx], share), groups[idx], min_size)))
    return [float(np.percentile(gaps, 2.5)), float(np.percentile(gaps, 97.5))]


def gate_decision(recall: float, gaps: dict[str, float], upper: dict[str, float], gates: dict) -> dict:
    """desplegar / limitar / modificar / no utilizar a partir de compuertas explícitas."""
    if recall < gates["min_recall_at_capacity"]:
        status = "no utilizar"
    elif any(g > gates["max_recall_gap"] for g in gaps.values()):
        status = "modificar"
    elif any(u > gates["max_recall_gap"] for u in upper.values()):
        status = "limitar"
    else:
        status = "desplegar"
    return {"decision": status, "recall_capacidad": recall, "brechas": gaps, "limite_superior_ic95": upper}


def allocate_by_group(scores: np.ndarray, groups: pd.Series, share: float) -> np.ndarray:
    """Reparte los cupos entre grupos en proporción al abandono esperado (suma de riesgos del propio modelo)
    y, dentro de cada grupo, elige a los de mayor riesgo. El modelo no usa el grupo; solo el reparto de cupos."""
    scores, groups = np.asarray(scores, dtype=float), np.asarray(groups)
    k = int(np.ceil(share * len(scores)))
    expected = pd.Series(scores).groupby(groups).sum()
    raw = expected / expected.sum() * k
    alloc = np.floor(raw).astype(int)
    for name in (raw - alloc).sort_values(ascending=False).index[: k - int(alloc.sum())]:
        alloc[name] += 1  # restos mayores: el total coincide exactamente con la capacidad
    selected = np.zeros(len(scores), dtype=bool)
    for name, n in alloc.items():
        idx = np.where(groups == name)[0]
        selected[idx[np.argsort(-scores[idx], kind="stable")[:n]]] = True
    return selected


def choose_mitigation(valid: pd.DataFrame, gates: dict) -> str:
    """Regla fijada en validación: entre las alternativas que cumplen recall mínimo y brechas máximas,
    la de mayor recall; si ninguna cumple, la de menor brecha máxima."""
    ok = valid[(valid["recall_capacidad"] >= gates["min_recall_at_capacity"])
               & (valid[["brecha_genero", "brecha_edad", "brecha_beca"]].max(axis=1) <= gates["max_recall_gap"])]
    if len(ok):
        return str(ok.sort_values("recall_capacidad", ascending=False).iloc[0]["alternativa"])
    worst = valid[["brecha_genero", "brecha_edad", "brecha_beca"]].max(axis=1)
    return str(valid.loc[worst.idxmin(), "alternativa"])
