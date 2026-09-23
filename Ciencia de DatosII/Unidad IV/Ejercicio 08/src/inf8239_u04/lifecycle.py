"""LAB13: minimización, retención, trazabilidad, monitoreo y respuesta a incidentes."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import recall_score

from .fairness import audit, gap

ROOT = Path(__file__).resolve().parents[2]


def load_inventory(path: Path = ROOT / "docs/data_inventory.csv") -> pd.DataFrame:
    return pd.read_csv(path)


def minimize(df: pd.DataFrame, inventory: pd.DataFrame, view: str) -> pd.DataFrame:
    """Devuelve solo las columnas que el inventario autoriza para la vista pedida (operational o audit)."""
    allowed = inventory.loc[inventory[f"{view}_view"].eq("yes"), "column"].tolist()
    unknown = set(df.columns) - set(inventory["column"])
    if unknown:
        raise ValueError(f"Columnas sin inventario: {sorted(unknown)}")
    return df[[c for c in df.columns if c in allowed]].copy()


def apply_retention(df: pd.DataFrame, as_of: str, months: int) -> tuple[pd.DataFrame, int]:
    """Conserva los casos recibidos dentro del plazo y devuelve cuántos se eliminan."""
    cutoff = pd.Timestamp(as_of) - pd.DateOffset(months=months)
    keep = df["received_date"] >= cutoff
    return df.loc[keep].copy(), int((~keep).sum())


def sha256(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def build_manifest(paths: dict[str, Path]) -> dict:
    return {name: {"path": str(Path(p).relative_to(ROOT)), "sha256": sha256(p)} for name, p in paths.items()}


def psi(reference: np.ndarray, current: np.ndarray, bins: int = 10) -> float:
    """Índice de estabilidad poblacional; categorías si la variable tiene pocos valores, cuantiles si es continua."""
    reference, current = np.asarray(reference, dtype=float), np.asarray(current, dtype=float)
    if len(np.unique(reference)) <= 15:
        values = np.union1d(np.unique(reference), np.unique(current))
        ref = np.array([(reference == v).mean() for v in values])
        cur = np.array([(current == v).mean() for v in values])
    else:
        edges = np.unique(np.quantile(reference, np.linspace(0, 1, bins + 1)))
        edges[0], edges[-1] = -np.inf, np.inf
        ref = np.histogram(reference, edges)[0] / len(reference)
        cur = np.histogram(current, edges)[0] / len(current)
    ref, cur = np.clip(ref, 1e-4, None), np.clip(cur, 1e-4, None)
    return float(((cur - ref) * np.log(cur / ref)).sum())


def mean_shift_z(reference: np.ndarray, current: np.ndarray) -> float:
    """Desplazamiento de la media del lote en errores estándar; útil con lotes pequeños."""
    return float((np.mean(current) - np.mean(reference)) / (np.std(reference, ddof=1) / np.sqrt(len(current))))


def rule(df: pd.DataFrame) -> np.ndarray:
    return ((df["previous_incidents"] >= 4) | (df["exposure"] >= 0.6)).astype(int).to_numpy()


def safe_baseline(df: pd.DataFrame) -> np.ndarray:
    """Respaldo si falla la variable exposure: solo incidentes previos."""
    return (df["previous_incidents"] >= 4).astype(int).to_numpy()


INPUTS = ["exposure", "previous_incidents"]


def check_inputs(batch: pd.DataFrame, reference: pd.DataFrame, limits: dict) -> dict:
    """Control semanal de calidad de entrada: no necesita etiquetas, así que detecta de inmediato."""
    result = {"n": int(len(batch))}
    alerts = []
    for column in INPUTS:
        z = mean_shift_z(reference[column].to_numpy(), batch[column].to_numpy())
        result[f"z_{column}"] = z
        if abs(z) > limits["max_abs_z"]:
            alerts.append(f"deriva en {column}")
    out_of_range = int((~batch["exposure"].between(0, 1)).sum() + (batch["previous_incidents"] < 0).sum())
    result["fuera_de_rango"] = out_of_range
    if out_of_range:
        alerts.append("valores fuera de rango")
    result["alerts"] = alerts
    return result


def check_performance(window: pd.DataFrame, pred: np.ndarray, limits: dict) -> dict:
    """Control de desempeño sobre los últimos casos con resultado conocido (ventana móvil)."""
    _, by_group, _ = audit(window.target, pred, window.protected_group)
    result = {"n": int(len(window)), "recall": float(recall_score(window.target, pred, zero_division=0)),
              "recall_gap": gap(by_group, "recall"), "fpr_gap": gap(by_group, "fpr"),
              "selection_rate": float(np.mean(pred))}
    alerts = []
    if result["n"] < limits["min_window"]:
        alerts.append("ventana insuficiente: solo informativo")
    else:
        if result["recall"] < limits["min_recall"]:
            alerts.append("recall bajo el mínimo")
        if result["recall_gap"] > limits["max_recall_gap"]:
            alerts.append("brecha de recall sobre la tolerancia")
    result["alerts"] = alerts
    return result


def respond(input_check: dict, performance: dict | None = None) -> str:
    """Runbook: deriva o datos fuera de rango -> CONTENER (respaldo + revisión manual); desempeño fuera de
    tolerancia sin deriva -> REVIEW; sin alertas -> OK."""
    if input_check["alerts"]:
        return "CONTENER"
    if performance and any(a.startswith(("recall", "brecha")) for a in performance["alerts"]):
        return "REVIEW"
    return "OK"


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
