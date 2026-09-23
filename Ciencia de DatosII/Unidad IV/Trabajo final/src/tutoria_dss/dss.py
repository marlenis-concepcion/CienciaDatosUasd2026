"""Lógica del DSS: priorización con cupos, tipo de apoyo por reglas explícitas, explicación y registro humano."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from .evaluation import top_k_mask
from .fairness import allocate_by_group

SUPPORTS = {
    "financiera": "Orientación financiera + tutoría",
    "academica": "Tutoría académica intensiva",
    "seguimiento": "Seguimiento del tutor",
}
READABLE = {
    "Curricular units 1st sem (approved)": "unidades aprobadas 1.er semestre",
    "Curricular units 1st sem (grade)": "nota media 1.er semestre",
    "Curricular units 1st sem (enrolled)": "unidades inscritas 1.er semestre",
    "Curricular units 1st sem (evaluations)": "evaluaciones 1.er semestre",
    "Curricular units 1st sem (without evaluations)": "unidades sin evaluación 1.er semestre",
    "Curricular units 1st sem (credited)": "unidades acreditadas",
    "Tuition fees up to date": "matrícula al día",
    "Debtor": "deuda con la institución",
    "Admission grade": "nota de admisión",
    "Previous qualification (grade)": "nota de estudios previos",
    "Application order": "orden de preferencia de la carrera",
    "Daytime/evening attendance": "turno diurno",
    "Displaced": "vive fuera de su domicilio",
    "Educational special needs": "necesidades educativas especiales",
    "Unemployment rate": "tasa de desempleo",
    "Inflation rate": "tasa de inflación",
    "GDP": "PIB",
    "Course": "carrera (código)",
    "Application mode": "modo de ingreso (código)",
    "Previous qualification": "estudios previos (código)",
    "Mother's qualification": "estudios de la madre (código)",
    "Father's qualification": "estudios del padre (código)",
    "Mother's occupation": "ocupación de la madre (código)",
    "Father's occupation": "ocupación del padre (código)",
}
LOG_COLUMNS = ["registrado_en", "student_id", "prioridad", "apoyo_sugerido", "decision", "apoyo_final", "motivo",
               "responsable"]


def support_type(row: pd.Series) -> str:
    """Reglas explícitas y auditables; el orden importa: lo financiero primero porque bloquea la continuidad."""
    if row["Debtor"] == 1 or row["Tuition fees up to date"] == 0:
        return SUPPORTS["financiera"]
    if row["Curricular units 1st sem (approved)"] == 0:
        return SUPPORTS["academica"]
    return SUPPORTS["seguimiento"]


def readable(feature: str, row: pd.Series | None = None) -> str:
    """Nombre legible con el valor real del estudiante, para que la explicación sea verificable."""
    name = feature.split("__", 1)[-1]
    if name in READABLE:
        value = "" if row is None else f" = {row[name]:g}"
        return READABLE[name] + value
    for original, text in READABLE.items():
        if name.startswith(original + "_"):
            return f"{text} = {name[len(original) + 1:]}"
    return name


def explain(contrib: pd.DataFrame, rows: pd.DataFrame | None = None, top: int = 3) -> list[str]:
    """Las variables que más aumentan el riesgo de cada estudiante, con su valor, en lenguaje de la coordinación."""
    out = []
    for index, values in contrib.iterrows():
        positive = values[values > 0].sort_values(ascending=False).head(top)
        row = None if rows is None else rows.loc[index]
        out.append("; ".join(readable(f, row) for f in positive.index) or "sin factores de riesgo destacados")
    return out


def prioritize(df: pd.DataFrame, risk: np.ndarray, share: float, contrib: pd.DataFrame | None = None,
               quota_groups: pd.Series | None = None) -> pd.DataFrame:
    """Lista para la coordinación: solo los cupos disponibles, ordenados por riesgo, con apoyo y explicación.
    Con quota_groups, los cupos se reparten entre grupos (mitigación elegida en validación)."""
    selected = top_k_mask(risk, share) if quota_groups is None else allocate_by_group(risk, quota_groups, share)
    table = df.loc[selected, ["student_id"]].copy()
    table["riesgo"] = np.asarray(risk)[selected]
    table["apoyo_sugerido"] = df.loc[selected].apply(support_type, axis=1).to_numpy()
    if contrib is not None:
        table["por_que"] = explain(contrib.loc[selected], df.loc[selected])
    table = table.sort_values(["riesgo", "student_id"], ascending=[False, True]).reset_index(drop=True)
    table.insert(0, "prioridad", np.arange(1, len(table) + 1))
    return table


def record_decision(log_path: Path, row: pd.Series, decision: str, final_support: str, reason: str,
                    owner: str) -> pd.DataFrame:
    """Registra la decisión humana; cambiar el apoyo o rechazar exige motivo."""
    if decision not in {"aceptar", "modificar", "rechazar"}:
        raise ValueError("La decisión debe ser aceptar, modificar o rechazar")
    if decision != "aceptar" and not reason.strip():
        raise ValueError("Modificar o rechazar requiere un motivo")
    if not owner.strip():
        raise ValueError("La decisión debe tener un responsable")
    entry = pd.DataFrame([{"registrado_en": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                           "student_id": row["student_id"], "prioridad": int(row["prioridad"]),
                           "apoyo_sugerido": row["apoyo_sugerido"], "decision": decision,
                           "apoyo_final": final_support if decision != "rechazar" else "",
                           "motivo": reason.strip(), "responsable": owner.strip()}], columns=LOG_COLUMNS)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    entry.to_csv(log_path, mode="a", header=not log_path.exists(), index=False)
    return pd.read_csv(log_path)
