from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def weighted_popularity(ratings: pd.DataFrame, movies: pd.DataFrame, quantile: float = 0.80) -> pd.DataFrame:
    stats = ratings.groupby("movieId")["rating"].agg(["mean", "count"])
    global_mean = float(ratings["rating"].mean())
    minimum = float(stats["count"].quantile(quantile))
    stats["weighted_score"] = (
        stats["count"] / (stats["count"] + minimum) * stats["mean"]
        + minimum / (stats["count"] + minimum) * global_mean
    )
    return stats.query("count >= @minimum").join(movies.set_index("movieId")).sort_values("weighted_score", ascending=False)


class ContentRecommender:
    def fit(self, movies: pd.DataFrame) -> "ContentRecommender":
        self.movies = movies.reset_index(drop=True).copy()
        self.movies["genres_text"] = self.movies["genres"].str.replace("|", " ", regex=False)
        self.vectorizer = TfidfVectorizer()
        self.matrix = self.vectorizer.fit_transform(self.movies["genres_text"])
        return self

    def recommend(self, title: str, k: int = 10) -> pd.DataFrame:
        matches = self.movies.index[self.movies["title"].eq(title)]
        if len(matches) == 0:
            raise KeyError(f"Título no encontrado: {title}")
        index = int(matches[0])
        scores = cosine_similarity(self.matrix[index], self.matrix).ravel()
        order = [value for value in scores.argsort()[::-1] if value != index][:k]
        result = self.movies.loc[order, ["movieId", "title", "genres"]].copy()
        result["content_score"] = scores[order]
        return result.reset_index(drop=True)


class MatrixFactorization:
    def __init__(self, factors: int = 20, learning_rate: float = 0.01, regularization: float = 0.05, seed: int = 42):
        self.factors = factors
        self.learning_rate = learning_rate
        self.regularization = regularization
        self.seed = seed

    def fit(self, ratings: pd.DataFrame, epochs: int = 12) -> "MatrixFactorization":
        self.users = sorted(ratings["userId"].unique())
        self.items = sorted(ratings["movieId"].unique())
        self.user_index = {value: index for index, value in enumerate(self.users)}
        self.item_index = {value: index for index, value in enumerate(self.items)}
        rng = np.random.default_rng(self.seed)
        self.user_factors = rng.normal(0, 0.1, (len(self.users), self.factors))
        self.item_factors = rng.normal(0, 0.1, (len(self.items), self.factors))
        self.global_mean = float(ratings["rating"].mean())
        observations = [(self.user_index[r.userId], self.item_index[r.movieId], float(r.rating)) for r in ratings.itertuples()]
        for _ in range(epochs):
            rng.shuffle(observations)
            for user, item, rating in observations:
                error = rating - self.predict_indices(user, item)
                previous_user = self.user_factors[user].copy()
                self.user_factors[user] += self.learning_rate * (error * self.item_factors[item] - self.regularization * self.user_factors[user])
                self.item_factors[item] += self.learning_rate * (error * previous_user - self.regularization * self.item_factors[item])
        return self

    def predict_indices(self, user_index: int, item_index: int) -> float:
        return float(self.global_mean + self.user_factors[user_index] @ self.item_factors[item_index])

    def predict(self, user_id: int, movie_id: int) -> float:
        return self.predict_indices(self.user_index[user_id], self.item_index[movie_id])

    def top_n(self, user_id: int, seen: set[int], k: int = 10) -> pd.DataFrame:
        if user_id not in self.user_index:
            return pd.DataFrame(columns=["movieId", "collaborative_score"])
        candidates = [item for item in self.items if item not in seen]
        scores = np.array([self.predict(user_id, item) for item in candidates])
        order = scores.argsort()[::-1][:k]
        return pd.DataFrame({"movieId": np.asarray(candidates)[order], "collaborative_score": scores[order]})


def temporal_leave_one_out(ratings: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    ordered = ratings.sort_values(["userId", "timestamp"])
    test = ordered.groupby("userId", sort=False).tail(1)
    train = ordered.drop(test.index)
    return train.reset_index(drop=True), test.reset_index(drop=True)


def minmax(values: np.ndarray) -> np.ndarray:
    low, high = float(np.min(values)), float(np.max(values))
    return (values - low) / max(high - low, 1e-9)


class Scorer:
    """Puntúa todo el catálogo para un usuario con popularidad, contenido y factorización."""

    def __init__(self, train: pd.DataFrame, movies: pd.DataFrame, mf: MatrixFactorization, quantile: float = 0.80):
        self.catalog = np.array(sorted(train["movieId"].unique()))
        self.position = {item: i for i, item in enumerate(self.catalog)}
        stats = weighted_popularity(train, movies, quantile=0.0).reindex(self.catalog)
        minimum = float(stats["count"].quantile(quantile))
        mean = float(train["rating"].mean())
        self.popularity = (stats["count"] / (stats["count"] + minimum) * stats["mean"]
                           + minimum / (stats["count"] + minimum) * mean).to_numpy()
        table = movies.set_index("movieId").loc[self.catalog, "genres"].str.replace("|", " ", regex=False)
        self.genres = TfidfVectorizer(token_pattern=r"[^ ]+").fit_transform(table)
        self.mf = mf
        self.item_rows = np.array([mf.item_index[item] for item in self.catalog])
        self.history = {user: group for user, group in train.groupby("userId")}

    def content(self, history: pd.DataFrame) -> np.ndarray:
        rows = [self.position[i] for i in history["movieId"] if i in self.position]
        if not rows:
            return np.zeros(len(self.catalog))
        weights = np.clip(history.loc[history["movieId"].isin(self.position), "rating"].to_numpy() - 2.5, 0.1, None)
        profile = np.asarray(self.genres[rows].multiply(weights[:, None]).sum(axis=0) / weights.sum())
        return cosine_similarity(profile, self.genres).ravel()

    def collaborative(self, user: int) -> np.ndarray:
        if user not in self.mf.user_index:
            return np.zeros(len(self.catalog))
        return self.mf.global_mean + self.mf.item_factors[self.item_rows] @ self.mf.user_factors[self.mf.user_index[user]]

    def recommend(self, user: int, method: str, alpha: float = 0.5, k: int = 10,
                  history: pd.DataFrame | None = None) -> list[int]:
        history = self.history.get(user) if history is None else history
        seen = set() if history is None else set(history["movieId"])
        if method == "popularity" or history is None or history.empty:
            scores = self.popularity.copy()
        elif method == "content":
            scores = self.content(history) + 1e-6 * minmax(self.popularity)
        elif method == "mf":
            scores = self.collaborative(user)
        elif method == "hybrid":
            scores = alpha * minmax(self.collaborative(user)) + (1 - alpha) * minmax(self.content(history))
        else:
            raise ValueError(f"Método desconocido: {method}")
        mask = np.array([item in seen for item in self.catalog])
        scores = np.where(mask, -np.inf, scores)
        order = [i for i in np.argsort(-scores, kind="stable") if not mask[i]][:k]
        return self.catalog[order].astype(int).tolist()


def pareto_front(table: pd.DataFrame, maximize: list[str]) -> pd.Series:
    """True para las filas que ninguna otra supera o iguala en todos los objetivos con mejora en alguno."""
    values = table[maximize].to_numpy()
    dominated = [
        any((other >= row).all() and (other > row).any() for j, other in enumerate(values) if j != i)
        for i, row in enumerate(values)
    ]
    return pd.Series(~np.array(dominated), index=table.index)
