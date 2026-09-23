"""Carga, contrato de datos, variables permitidas en el punto de decisión y partición."""
from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

from .config import DATA_PATH

TARGET = "Target"
SENSITIVE = ["Gender", "Age at enrollment", "Nacionality", "Marital status", "International", "Scholarship holder"]
SECOND_SEMESTER = [
    "Curricular units 2nd sem (credited)", "Curricular units 2nd sem (enrolled)",
    "Curricular units 2nd sem (evaluations)", "Curricular units 2nd sem (approved)",
    "Curricular units 2nd sem (grade)", "Curricular units 2nd sem (without evaluations)",
]
CATEGORICAL = ["Application mode", "Course", "Previous qualification", "Mother's qualification",
               "Father's qualification", "Mother's occupation", "Father's occupation"]
NUMERIC = [
    "Application order", "Daytime/evening attendance", "Previous qualification (grade)", "Admission grade",
    "Displaced", "Educational special needs", "Debtor", "Tuition fees up to date",
    "Curricular units 1st sem (credited)", "Curricular units 1st sem (enrolled)",
    "Curricular units 1st sem (evaluations)", "Curricular units 1st sem (approved)",
    "Curricular units 1st sem (grade)", "Curricular units 1st sem (without evaluations)",
    "Unemployment rate", "Inflation rate", "GDP",
]
FEATURES = CATEGORICAL + NUMERIC


def load(path: Path = DATA_PATH) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"No existe {path}. Ejecute: uv run python scripts/download_data.py")
    df = pd.read_csv(path, sep=";", encoding="utf-8-sig")
    df.columns = df.columns.str.strip()
    validate(df)
    df = df.reset_index(drop=True)
    df.insert(0, "student_id", [f"E{i:04d}" for i in range(len(df))])
    df["abandono"] = (df[TARGET] == "Dropout").astype(int)
    return df


def validate(df: pd.DataFrame) -> None:
    """Contrato: columnas esperadas, sin nulos, objetivo válido y rangos básicos."""
    missing = set(FEATURES + SENSITIVE + SECOND_SEMESTER + [TARGET]) - set(df.columns)
    if missing:
        raise ValueError(f"Faltan columnas: {sorted(missing)}")
    if df[FEATURES + [TARGET]].isna().any().any():
        raise ValueError("Hay valores nulos")
    if not set(df[TARGET]).issubset({"Dropout", "Graduate", "Enrolled"}):
        raise ValueError("Target con valores inesperados")
    if (df["Curricular units 1st sem (approved)"] > df["Curricular units 1st sem (enrolled)"]
            + df["Curricular units 1st sem (credited)"]).any():
        raise ValueError("Unidades aprobadas mayores que las inscritas más acreditadas")


def allowed_features() -> list[str]:
    """Variables que pueden entrar al modelo: sin sensibles ni segundo semestre."""
    forbidden = set(SENSITIVE) | set(SECOND_SEMESTER) | {TARGET, "abandono", "student_id"}
    return [f for f in FEATURES if f not in forbidden]


def split(df: pd.DataFrame, seed: int = 42) -> dict[str, pd.DataFrame]:
    """Partición estratificada 70/15/15 por abandono."""
    train, rest = train_test_split(df, test_size=0.30, stratify=df["abandono"], random_state=seed)
    valid, test = train_test_split(rest, test_size=0.50, stratify=rest["abandono"], random_state=seed)
    return {"train": train, "valid": valid, "test": test}


def audit(df: pd.DataFrame) -> dict:
    return {
        "filas": int(len(df)), "columnas": int(df.shape[1]),
        "nulos": int(df.isna().sum().sum()), "duplicados": int(df.drop(columns="student_id").duplicated().sum()),
        "clases": {k: int(v) for k, v in df[TARGET].value_counts().items()},
        "tasa_abandono": round(float(df["abandono"].mean()), 4),
        "abandono_por_genero": {("hombre" if k == 1 else "mujer"): round(float(v), 4)
                                for k, v in df.groupby("Gender")["abandono"].mean().items()},
        "abandono_por_beca": {("becario" if k == 1 else "sin beca"): round(float(v), 4)
                              for k, v in df.groupby("Scholarship holder")["abandono"].mean().items()},
        "variables_modelo": len(allowed_features()),
        "variables_excluidas": sorted(set(SENSITIVE) | set(SECOND_SEMESTER)),
    }
