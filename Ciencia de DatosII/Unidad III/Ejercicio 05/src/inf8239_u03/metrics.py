from __future__ import annotations

import numpy as np
import pandas as pd


def hit_rate_at_k(recommendations: dict[int, list[int]], truth: pd.DataFrame, k: int = 10) -> float:
    hits = []
    for row in truth.itertuples():
        if row.userId in recommendations:
            hits.append(int(row.movieId in recommendations[row.userId][:k]))
    return sum(hits) / len(hits) if hits else 0.0


def catalog_coverage(recommendations: dict[int, list[int]], catalog_size: int) -> float:
    recommended = {item for values in recommendations.values() for item in values}
    return len(recommended) / catalog_size if catalog_size else 0.0


def ranking_metrics(recommendations: dict[int, list[int]], relevant: dict[int, set[int]], k: int = 10) -> pd.DataFrame:
    """Precision, recall, NDCG y acierto por usuario; solo usuarios con al menos un ítem relevante."""
    rows = []
    for user, items in relevant.items():
        if not items:
            continue
        top = recommendations.get(user, [])[:k]
        gains = [1.0 if item in items else 0.0 for item in top]
        dcg = sum(g / np.log2(i + 2) for i, g in enumerate(gains))
        ideal = sum(1.0 / np.log2(i + 2) for i in range(min(len(items), k)))
        hits = sum(gains)
        rows.append({"userId": user, "precision": hits / k, "recall": hits / len(items),
                     "ndcg": dcg / ideal if ideal else 0.0, "hit": float(hits > 0), "relevantes": len(items)})
    return pd.DataFrame(rows)


def novelty(recommendations: dict[int, list[int]], popularity: pd.Series, n_users: int) -> float:
    """Autoinformación media -log2(p) de los ítems recomendados; más alta = menos obvia."""
    values = [-np.log2(max(popularity.get(item, 0), 1) / n_users) for items in recommendations.values() for item in items]
    return float(np.mean(values)) if values else 0.0
