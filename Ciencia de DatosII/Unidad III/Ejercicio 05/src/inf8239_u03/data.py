from __future__ import annotations

import hashlib
import io
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import requests


def download_zip(url: str, destination: Path) -> tuple[Path, str]:
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    digest = hashlib.sha256(response.content).hexdigest()
    destination.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(response.content)) as archive:
        root = destination.resolve()
        for member in archive.infolist():
            target = (destination / member.filename).resolve()
            if root not in target.parents and target != root:
                raise ValueError(f"Ruta insegura en ZIP: {member.filename}")
        archive.extractall(destination)
    return destination, digest


def load_movielens(directory: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    ratings = pd.read_csv(directory / "ratings.csv")
    movies = pd.read_csv(directory / "movies.csv")
    validate_movielens(ratings, movies)
    return ratings, movies


def validate_movielens(ratings: pd.DataFrame, movies: pd.DataFrame) -> None:
    required_ratings = {"userId", "movieId", "rating", "timestamp"}
    required_movies = {"movieId", "title", "genres"}
    if not required_ratings <= set(ratings.columns):
        raise ValueError("ratings.csv no tiene las columnas requeridas")
    if not required_movies <= set(movies.columns):
        raise ValueError("movies.csv no tiene las columnas requeridas")
    if not ratings["movieId"].isin(movies["movieId"]).all():
        raise ValueError("Existen ratings sin película correspondiente")
    if not ratings["rating"].between(0.5, 5.0).all():
        raise ValueError("Existen ratings fuera del rango 0.5–5.0")


def select_cold_users(ratings: pd.DataFrame, fraction: float = 0.10, seed: int = 42) -> set[int]:
    """Usuarios que se retiran por completo del entrenamiento para simular usuarios nuevos."""
    users = np.sort(ratings["userId"].unique())
    rng = np.random.default_rng(seed)
    return set(rng.choice(users, size=max(1, round(len(users) * fraction)), replace=False).tolist())


def temporal_split_per_user(
    ratings: pd.DataFrame, valid_fraction: float = 0.10, test_fraction: float = 0.20
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Para cada usuario: lo más antiguo a entrenamiento, luego validación y lo más reciente a prueba."""
    ordered = ratings.sort_values(["userId", "timestamp", "movieId"]).copy()
    position = ordered.groupby("userId").cumcount()
    size = ordered.groupby("userId")["movieId"].transform("size")
    n_test = np.maximum(1, np.round(size * test_fraction)).astype(int)
    n_valid = np.maximum(1, np.round(size * valid_fraction)).astype(int)
    ordered["split"] = np.where(position >= size - n_test, "test",
                                np.where(position >= size - n_test - n_valid, "valid", "train"))
    parts = [ordered[ordered["split"] == name].drop(columns="split").reset_index(drop=True)
             for name in ["train", "valid", "test"]]
    return parts[0], parts[1], parts[2]
