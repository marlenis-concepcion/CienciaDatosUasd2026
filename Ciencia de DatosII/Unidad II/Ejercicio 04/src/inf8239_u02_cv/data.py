from __future__ import annotations

import hashlib
from collections import Counter

import numpy as np
from sklearn.model_selection import train_test_split

CLASS_NAMES = ["T-shirt/top", "Trouser", "Pullover", "Dress", "Coat",
               "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"]


def normalize_images(images: np.ndarray) -> np.ndarray:
    values = images.astype("float32") / 255.0
    return values[..., None]


def validate_images(images: np.ndarray, labels: np.ndarray) -> None:
    if images.ndim != 4 or images.shape[1:] != (28, 28, 1):
        raise ValueError(f"Forma inesperada: {images.shape}")
    if len(images) != len(labels):
        raise ValueError("Imágenes y etiquetas no coinciden")
    if not np.isfinite(images).all() or images.min() < 0 or images.max() > 1:
        raise ValueError("Las imágenes deben estar normalizadas entre 0 y 1")


def image_hashes(images: np.ndarray) -> list[str]:
    return [hashlib.sha1(np.ascontiguousarray(image).tobytes()).hexdigest() for image in images]


def audit_arrays(x_train, y_train, x_test, y_test) -> dict:
    """Auditoría sobre los arreglos originales (uint8), antes de normalizar o partir."""
    train_hashes, test_hashes = image_hashes(x_train), image_hashes(x_test)
    train_counts = Counter(train_hashes)
    test_set = set(test_hashes)
    labels_by_hash: dict[str, set[int]] = {}
    for key, label in zip(train_hashes, y_train):
        labels_by_hash.setdefault(key, set()).add(int(label))
    return {
        "forma_entrenamiento": list(x_train.shape),
        "forma_prueba": list(x_test.shape),
        "tipo": str(x_train.dtype),
        "rango_pixeles": [int(x_train.min()), int(x_train.max())],
        "media_pixel_entrenamiento": round(float(x_train.mean()) / 255, 4),
        "desviacion_pixel_entrenamiento": round(float(x_train.std()) / 255, 4),
        "clases_entrenamiento": {CLASS_NAMES[k]: int(v) for k, v in sorted(Counter(y_train.tolist()).items())},
        "clases_prueba": {CLASS_NAMES[k]: int(v) for k, v in sorted(Counter(y_test.tolist()).items())},
        "duplicados_en_entrenamiento": int(sum(v - 1 for v in train_counts.values())),
        "duplicados_en_prueba": int(len(test_hashes) - len(test_set)),
        "entrenamiento_repetido_en_prueba": int(sum(key in test_set for key in train_hashes)),
        "etiquetas_contradictorias": int(sum(len(v) > 1 for v in labels_by_hash.values())),
        "imagenes_vacias": int((x_train.max(axis=(1, 2)) == 0).sum() + (x_test.max(axis=(1, 2)) == 0).sum()),
    }


def split_train_valid(x, y, valid_size: int = 6000, random_state: int = 42):
    """Validación estratificada tomada solo del conjunto oficial de entrenamiento."""
    indices = np.arange(len(y))
    train_idx, valid_idx = train_test_split(
        indices, test_size=valid_size, stratify=y, random_state=random_state
    )
    return np.sort(train_idx), np.sort(valid_idx)
