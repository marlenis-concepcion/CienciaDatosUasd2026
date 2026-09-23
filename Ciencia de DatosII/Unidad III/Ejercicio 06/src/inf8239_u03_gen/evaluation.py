from __future__ import annotations

import numpy as np


def reconstruction_errors(originals: np.ndarray, reconstructed: np.ndarray) -> dict:
    x = originals.reshape(len(originals), -1).astype("float64")
    y = np.clip(reconstructed.reshape(len(reconstructed), -1).astype("float64"), 1e-7, 1 - 1e-7)
    bce = -(x * np.log(y) + (1 - x) * np.log(1 - y)).sum(axis=1)
    return {"mse_pixel": float(((x - y) ** 2).mean()), "bce_por_imagen": float(bce.mean())}


def nearest_distances(queries: np.ndarray, reference: np.ndarray, batch: int = 500) -> np.ndarray:
    """Distancia euclídea de cada consulta a su vecino más cercano en la referencia."""
    q = queries.reshape(len(queries), -1).astype("float32")
    r = reference.reshape(len(reference), -1).astype("float32")
    r_norm = (r ** 2).sum(axis=1)
    result = []
    for start in range(0, len(q), batch):
        block = q[start:start + batch]
        d2 = (block ** 2).sum(axis=1)[:, None] + r_norm[None, :] - 2 * block @ r.T
        result.append(np.sqrt(np.maximum(d2.min(axis=1), 0)))
    return np.concatenate(result)


def class_diversity(probabilities: np.ndarray) -> dict:
    """Confianza del clasificador (fidelidad) y entropía normalizada de las clases predichas (diversidad)."""
    predicted = probabilities.argmax(axis=1)
    share = np.bincount(predicted, minlength=probabilities.shape[1]) / len(predicted)
    nonzero = share[share > 0]
    return {"confianza_media": float(probabilities.max(axis=1).mean()),
            "confianza_mayor_0_9": float((probabilities.max(axis=1) > 0.9).mean()),
            "clases_cubiertas": int((share > 0.01).sum()),
            "entropia_clases": float(-(nonzero * np.log(nonzero)).sum() / np.log(probabilities.shape[1])),
            "reparto": share.round(3).tolist()}


def pairwise_spread(images: np.ndarray, n: int = 500, seed: int = 42) -> float:
    """Distancia media entre pares de imágenes: si es baja, las muestras se parecen entre sí."""
    x = images.reshape(len(images), -1)[np.random.default_rng(seed).permutation(len(images))[:n]].astype("float32")
    sq = (x ** 2).sum(axis=1)
    d = np.sqrt(np.maximum(sq[:, None] + sq[None, :] - 2 * x @ x.T, 0))
    return float(d[np.triu_indices(len(x), 1)].mean())


def choose(valid_losses: dict[str, float]) -> tuple[str, str]:
    """Elige el VAE con menor pérdida total de validación (reconstrucción + KL, comparable entre dimensiones)."""
    chosen = min(valid_losses, key=valid_losses.get)
    detail = ", ".join(f"{k}={v:.2f}" for k, v in sorted(valid_losses.items()))
    return chosen, f"Pérdida total en validación: {detail}. Se elige la menor: {chosen}."
