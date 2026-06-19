from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import (
    HistGradientBoostingClassifier,
    HistGradientBoostingRegressor,
    RandomForestClassifier,
    RandomForestRegressor,
)
from sklearn.impute import SimpleImputer
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    f1_score,
    mean_squared_error,
    precision_score,
    r2_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from .config import ProjectConfig
from .domain import ModelResult, ResultRegistry, TaskType
from .features import FeatureEngineer
from .metrics import manual_binary_metrics, multiclass_mse_r2


class ModelLab:
    def __init__(self, config: ProjectConfig, engineer: FeatureEngineer):
        self.config = config
        self.engineer = engineer
        self.registry = ResultRegistry()
        self.metric_rows: list[dict] = []
        self.manual_rows: list[dict] = []
        self.prediction_frames: dict[str, list[pd.DataFrame]] = {
            "binarias": [],
            "ordinales": [],
            "regresion": [],
        }

    def _preprocessor(self) -> ColumnTransformer:
        numeric = Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ])
        categorical = Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ])
        return ColumnTransformer([
            ("num", numeric, self.engineer.numeric_columns),
            ("cat", categorical, self.engineer.categorical_columns),
        ])

    def run(self, data: pd.DataFrame) -> None:
        self._classification(data, ordinal=False)
        self._classification(data, ordinal=True)
        self._regression(data.dropna(subset=["promedio_evaluaciones"]))
        self._export()

    def _classification(self, data: pd.DataFrame, ordinal: bool) -> None:
        target = "resultado_ordinal" if ordinal else "aprobo"
        task = TaskType.ORDINAL if ordinal else TaskType.BINARY
        prefix = "ordinales" if ordinal else "binarias"
        X = data[self.engineer.feature_columns]
        y = data[target].astype(int)
        ids = data[["id_student", "fuente", "final_result"]]
        X_train, X_test, y_train, y_test, _, ids_test = train_test_split(
            X, y, ids,
            test_size=self.config.test_size,
            random_state=self.config.random_state,
            stratify=y,
        )
        models = {
            "regresion_logistica": LogisticRegression(max_iter=1200),
            "random_forest": RandomForestClassifier(
                n_estimators=220, min_samples_leaf=3, n_jobs=1,
                random_state=self.config.random_state, class_weight="balanced",
            ),
            "gradient_boosting": HistGradientBoostingClassifier(
                max_iter=180, random_state=self.config.random_state
            ),
        }
        for name, estimator in models.items():
            pipe = Pipeline([("prep", self._preprocessor()), ("model", estimator)])
            pipe.fit(X_train, y_train)
            pred = pipe.predict(X_test)
            metrics = {
                "precision_macro": precision_score(y_test, pred, average="macro", zero_division=0),
                "recall_macro": recall_score(y_test, pred, average="macro", zero_division=0),
                "f1_macro": f1_score(y_test, pred, average="macro", zero_division=0),
                "accuracy": accuracy_score(y_test, pred),
            }
            if ordinal:
                mse, r2 = multiclass_mse_r2(y_test, pred)
                metrics.update({"msePI2": mse, "r2PI2": r2, "roc_auc": np.nan})
            else:
                probability = pipe.predict_proba(X_test)[:, 1]
                metrics.update({
                    "roc_auc": roc_auc_score(y_test, probability),
                    "msePI2": mean_squared_error(y_test, pred),
                    "r2PI2": r2_score(y_test, pred),
                })
                manual = manual_binary_metrics(y_test, pred)
                self.manual_rows.append({"modelo": name, **manual})
                self._confusion_plot(y_test, pred, name)

            self.registry.add(ModelResult(task, name, metrics, pred))
            self.metric_rows.append({"tarea": task.value, "modelo": name, **metrics})
            prediction = ids_test.reset_index(drop=True).copy()
            prediction["y_test"] = y_test.reset_index(drop=True)
            prediction["y_pred"] = pred
            prediction["modelo"] = name
            self.prediction_frames[prefix].append(prediction)
            self._importance(pipe, X_test, y_test, task, name)

    def _regression(self, data: pd.DataFrame) -> None:
        X = data[self.engineer.feature_columns]
        y = data["promedio_evaluaciones"].astype(float)
        ids = data[["id_student", "fuente", "final_result"]]
        X_train, X_test, y_train, y_test, _, ids_test = train_test_split(
            X, y, ids,
            test_size=self.config.test_size,
            random_state=self.config.random_state,
        )
        models = {
            "ridge": Ridge(alpha=1.0),
            "random_forest": RandomForestRegressor(
                n_estimators=220, min_samples_leaf=3, n_jobs=1,
                random_state=self.config.random_state,
            ),
            "gradient_boosting": HistGradientBoostingRegressor(
                max_iter=180, random_state=self.config.random_state
            ),
        }
        for name, estimator in models.items():
            pipe = Pipeline([("prep", self._preprocessor()), ("model", estimator)])
            pipe.fit(X_train, y_train)
            pred = pipe.predict(X_test)
            metrics = {
                "mse": mean_squared_error(y_test, pred),
                "r2": r2_score(y_test, pred),
            }
            self.registry.add(ModelResult(TaskType.REGRESSION, name, metrics, pred))
            self.metric_rows.append({
                "tarea": TaskType.REGRESSION.value,
                "modelo": name,
                **metrics,
            })
            prediction = ids_test.reset_index(drop=True).copy()
            prediction["y_test"] = y_test.reset_index(drop=True)
            prediction["y_pred"] = pred
            prediction["modelo"] = name
            self.prediction_frames["regresion"].append(prediction)
            self._importance(pipe, X_test, y_test, TaskType.REGRESSION, name)

    def _importance(self, model, X_test, y_test, task: TaskType, name: str) -> None:
        sample_size = min(1800, len(X_test))
        sample = X_test.sample(sample_size, random_state=self.config.random_state)
        y_sample = y_test.loc[sample.index]
        scoring = "r2" if task is TaskType.REGRESSION else "f1_macro"
        result = permutation_importance(
            model, sample, y_sample, n_repeats=3,
            random_state=self.config.random_state, scoring=scoring, n_jobs=1,
        )
        frame = pd.DataFrame({
            "tarea": task.value,
            "modelo": name,
            "variable": self.engineer.feature_columns,
            "importancia": result.importances_mean,
        })
        path = self.config.output_dir / "_importancias_temporales.csv"
        frame.to_csv(path, mode="a", header=not path.exists(), index=False)

    def _confusion_plot(self, y_true, y_pred, name: str) -> None:
        fig, ax = plt.subplots(figsize=(5, 4))
        ConfusionMatrixDisplay.from_predictions(
            y_true, y_pred, display_labels=["No aprueba", "Aprueba"],
            cmap="Blues", ax=ax, colorbar=False,
        )
        ax.set_title(f"Matriz de confusión: {name}")
        plt.tight_layout()
        plt.savefig(
            self.config.output_dir / f"confusion_{name}.png",
            dpi=180, bbox_inches="tight",
        )
        plt.close()

    def _export(self) -> None:
        pd.DataFrame(self.metric_rows).to_csv(
            self.config.output_dir / "metricas_generales.csv", index=False
        )
        pd.DataFrame(self.manual_rows).to_csv(
            self.config.output_dir / "f1_manual.csv", index=False
        )
        for name, frames in self.prediction_frames.items():
            pd.concat(frames, ignore_index=True).to_csv(
                self.config.output_dir / f"predicciones_{name}.csv", index=False
            )
        temporary = self.config.output_dir / "_importancias_temporales.csv"
        if temporary.exists():
            temporary.replace(self.config.output_dir / "importancias_variables.csv")
