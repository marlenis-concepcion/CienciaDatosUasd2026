from __future__ import annotations

import shutil

import pandas as pd

from .config import ProjectConfig
from .data import ExperimentXFactory, OULADRepository
from .eda import EDAReporter
from .features import FeatureEngineer
from .modeling import ModelLab


class OULADProject:
    """Orquesta OSEMN: Obtain, Scrub, Explore, Model e iNterpret."""

    def __init__(self, config: ProjectConfig):
        self.config = config
        self.engineer = FeatureEngineer()

    def run(self) -> pd.DataFrame:
        self._prepare_outputs()
        raw = self._obtain()
        clean = self._scrub(raw)
        hypotheses = EDAReporter(self.config.output_dir).run(clean)
        lab = ModelLab(self.config, self.engineer)
        lab.run(clean)
        self._interpret(clean, hypotheses)
        return pd.DataFrame(lab.metric_rows)

    def _prepare_outputs(self) -> None:
        self.config.output_dir.mkdir(parents=True, exist_ok=True)
        for path in self.config.output_dir.iterdir():
            if path.name != "README.md":
                if path.is_dir():
                    shutil.rmtree(path)
                else:
                    path.unlink()

    def _obtain(self) -> pd.DataFrame:
        experiment = ExperimentXFactory(self.config.random_state).create()
        if self.config.synthetic_only:
            return experiment
        oulad = OULADRepository(self.config).load_oulad()
        return pd.concat([oulad, experiment], ignore_index=True, sort=False)

    def _scrub(self, raw: pd.DataFrame) -> pd.DataFrame:
        clean = self.engineer.transform(raw)
        if self.config.sample_size and len(clean) > self.config.sample_size:
            clean = clean.sample(
                self.config.sample_size,
                random_state=self.config.random_state,
            ).reset_index(drop=True)
        clean.to_csv(self.config.output_dir / "dataset_modelado.csv", index=False)
        return clean

    def _interpret(self, data: pd.DataFrame, hypotheses: dict[str, float]) -> None:
        metrics = pd.read_csv(self.config.output_dir / "metricas_generales.csv")
        best_binary = (
            metrics.loc[metrics["tarea"] == "dicotomica"]
            .sort_values("f1_macro", ascending=False)
            .iloc[0]
        )
        best_regression = (
            metrics.loc[metrics["tarea"] == "intervalo_razon"]
            .sort_values("r2", ascending=False)
            .iloc[0]
        )
        best_ordinal = (
            metrics.loc[metrics["tarea"] == "ordinal"]
            .sort_values("f1_macro", ascending=False)
            .iloc[0]
        )
        importances = pd.read_csv(self.config.output_dir / "importancias_variables.csv")
        top_variables = (
            importances.loc[
                (importances["tarea"] == "dicotomica")
                & (importances["modelo"] == best_binary["modelo"])
            ]
            .sort_values("importancia", ascending=False)
            .head(3)["variable"]
            .tolist()
        )
        p_text = "< .001" if hypotheses["p_value"] < 0.001 else f"= {hypotheses['p_value']:.4g}"
        text = f"""HALLAZGOS PRINCIPALES

Muestra modelada: {len(data):,} observaciones.
H1: U = {hypotheses['mann_whitney_u']:.2f}, p {p_text},
r biserial = {hypotheses['rank_biserial_r']:.3f}.
Media de clics, aprueba: {hypotheses['media_clicks_aprueba']:.2f}.
Media de clics, no aprueba: {hypotheses['media_clicks_no_aprueba']:.2f}.

Mejor modelo dicotómico por F1 macro: {best_binary['modelo']}
(F1 = {best_binary['f1_macro']:.3f}, ROC-AUC = {best_binary['roc_auc']:.3f}).
Mejor modelo ordinal por F1 macro: {best_ordinal['modelo']}
(F1 = {best_ordinal['f1_macro']:.3f}, MSE ordinal = {best_ordinal['msePI2']:.3f}).
Mejor regresión por R²: {best_regression['modelo']}
(MSE = {best_regression['mse']:.3f}, R² = {best_regression['r2']:.3f}).
Variables más influyentes del mejor clasificador: {", ".join(top_variables)}.

El Experimento X es sintético. Los resultados no establecen causalidad ni deben utilizarse
para decisiones automáticas sobre estudiantes sin validación institucional, análisis de
equidad y supervisión humana.
"""
        (self.config.output_dir / "hallazgos.txt").write_text(text, encoding="utf-8")
        print(text)
