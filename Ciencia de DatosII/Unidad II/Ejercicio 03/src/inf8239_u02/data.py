from __future__ import annotations

import hashlib
import re
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

from .config import settings


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_dataset(path: Path | None = None) -> pd.DataFrame:
    selected = path or settings.dataset_path
    if not selected.exists():
        raise FileNotFoundError(
            f"Dataset no encontrado: {selected}. Ejecute: uv run python scripts/download_data.py"
        )
    return pd.read_csv(selected)


def validate_dataframe(df: pd.DataFrame, text_column: str, target_column: str) -> None:
    missing = {text_column, target_column} - set(df.columns)
    if missing:
        raise ValueError(f"Faltan columnas requeridas: {sorted(missing)}")
    if df.empty:
        raise ValueError("El dataset está vacío")
    if df[text_column].fillna("").astype(str).str.strip().eq("").any():
        raise ValueError("Existen textos vacíos")
    if df[target_column].nunique(dropna=True) < 2:
        raise ValueError("Se requieren al menos dos clases")


def normalize_text(value: str) -> str:
    """Clave para detectar duplicados: minúsculas, dígitos unificados y espacios colapsados."""
    value = re.sub(r"\d", "0", str(value).lower())
    return re.sub(r"\s+", " ", value).strip()


def deduplicate(df: pd.DataFrame, text_column: str, target_column: str) -> tuple[pd.DataFrame, dict]:
    """Conserva la primera aparición de cada texto normalizado antes de cualquier partición."""
    keys = df[text_column].map(normalize_text)
    labels_per_key = df.groupby(keys)[target_column].nunique()
    conflicts = int((labels_per_key > 1).sum())
    if conflicts:
        raise ValueError(f"Hay {conflicts} textos con etiquetas contradictorias")
    exact = int(df[text_column].duplicated().sum())
    normalized = int(keys.duplicated().sum())
    clean = df.loc[~keys.duplicated()].copy()
    summary = {
        "filas_originales": int(len(df)),
        "duplicados_exactos": exact,
        "duplicados_normalizados": normalized,
        "duplicados_solo_por_normalizacion": normalized - exact,
        "etiquetas_contradictorias": conflicts,
        "filas_finales": int(len(clean)),
    }
    return clean, summary


def split_data(
    df: pd.DataFrame, target_column: str, random_state: int = 42
) -> dict[str, pd.DataFrame]:
    """Partición estratificada 70/15/15 sobre el corpus ya deduplicado."""
    train, rest = train_test_split(
        df, test_size=0.30, stratify=df[target_column], random_state=random_state
    )
    valid, test = train_test_split(
        rest, test_size=0.50, stratify=rest[target_column], random_state=random_state
    )
    return {"train": train, "valid": valid, "test": test}


def check_no_leakage(splits: dict[str, pd.DataFrame], text_column: str) -> None:
    keys = {name: set(part[text_column].map(normalize_text)) for name, part in splits.items()}
    names = list(keys)
    for i, first in enumerate(names):
        for second in names[i + 1 :]:
            shared = keys[first] & keys[second]
            if shared:
                raise ValueError(f"{len(shared)} textos compartidos entre {first} y {second}")
