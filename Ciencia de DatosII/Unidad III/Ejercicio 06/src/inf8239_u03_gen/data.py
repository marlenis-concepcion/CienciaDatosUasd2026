from __future__ import annotations

import numpy as np


def normalize_images(images: np.ndarray) -> np.ndarray:
    return (images.astype("float32") / 255.0)[..., None]


def validate_images(images: np.ndarray) -> None:
    if images.ndim != 4 or images.shape[1:] != (28, 28, 1):
        raise ValueError(f"Forma inesperada: {images.shape}")
    if not np.isfinite(images).all() or images.min() < 0 or images.max() > 1:
        raise ValueError("Las imágenes deben contener valores finitos entre 0 y 1")


CLASS_NAMES = ["T-shirt/top", "Trouser", "Pullover", "Dress", "Coat",
               "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"]


def split_train_valid(n: int, valid_size: int = 6000, seed: int = 42) -> tuple[np.ndarray, np.ndarray]:
    """Validación aleatoria y reproducible tomada solo del entrenamiento oficial."""
    order = np.random.default_rng(seed).permutation(n)
    return np.sort(order[valid_size:]), np.sort(order[:valid_size])
