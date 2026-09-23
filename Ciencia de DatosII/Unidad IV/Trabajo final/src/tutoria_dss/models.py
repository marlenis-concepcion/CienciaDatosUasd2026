"""Modelo candidato: regresión logística en un pipeline (preprocesamiento ajustado solo con entrenamiento)."""
from __future__ import annotations

from time import perf_counter

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from .data import CATEGORICAL, allowed_features


def build_logistic(C: float = 1.0, seed: int = 42) -> Pipeline:
    features = allowed_features()
    categorical = [c for c in CATEGORICAL if c in features]
    numeric = [c for c in features if c not in categorical]
    prep = ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="ignore", min_frequency=20), categorical),
        ("num", StandardScaler(), numeric),
    ])
    return Pipeline([("prep", prep), ("model", LogisticRegression(C=C, max_iter=3000, class_weight="balanced",
                                                                   random_state=seed))])


def tune(train: pd.DataFrame, seed: int = 42) -> tuple[Pipeline, pd.DataFrame, float]:
    """Elige C por validación cruzada de 5 pliegues (average precision) solo sobre entrenamiento."""
    search = GridSearchCV(build_logistic(seed=seed), {"model__C": [0.01, 0.1, 1.0, 10.0]}, scoring="average_precision",
                          cv=StratifiedKFold(5, shuffle=True, random_state=seed))
    start = perf_counter()
    search.fit(train[allowed_features()], train["abandono"])
    seconds = perf_counter() - start
    table = pd.DataFrame(search.cv_results_)[["param_model__C", "mean_test_score", "std_test_score"]]
    return search.best_estimator_, table.rename(columns={"param_model__C": "C"}), seconds


def predict_risk(model: Pipeline, df: pd.DataFrame) -> np.ndarray:
    return model.predict_proba(df[allowed_features()])[:, 1]


def contributions(model: Pipeline, df: pd.DataFrame) -> pd.DataFrame:
    """Contribución de cada variable transformada al logit (coeficiente × valor): base de la explicación."""
    prep, logistic = model.named_steps["prep"], model.named_steps["model"]
    values = prep.transform(df[allowed_features()])
    values = values.toarray() if hasattr(values, "toarray") else values
    return pd.DataFrame(values * logistic.coef_[0], columns=prep.get_feature_names_out(), index=df.index)
