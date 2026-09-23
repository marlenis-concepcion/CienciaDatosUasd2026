from __future__ import annotations

import numpy as np
import pandas as pd
from fairlearn.postprocessing import ThresholdOptimizer
from sklearn.metrics import accuracy_score, recall_score

from .data import features, temporal_split
from .fairness import audit, gap, intersectional
from .model import build_model

MIN_CELL = 30


def rule_baseline(df: pd.DataFrame) -> np.ndarray:
    """Alternativa no predictiva: priorizar si hay 4+ incidentes previos o exposición >= 0.6."""
    return ((df["previous_incidents"] >= 4) | (df["exposure"] >= 0.6)).astype(int).to_numpy()


def summarize(y, pred, groups) -> dict:
    overall, by_group, _ = audit(y, pred, groups)
    return {"accuracy": float(accuracy_score(y, pred)), "recall": float(recall_score(y, pred, zero_division=0)),
            "fpr": float(overall["fpr"]), "selection_rate": float(overall["selection_rate"]),
            "recall_gap": gap(by_group, "recall"), "fpr_gap": gap(by_group, "fpr"),
            "selection_gap": gap(by_group, "selection_rate")}


def bootstrap_gaps(y, pred, groups, n: int = 1000, seed: int = 42) -> dict:
    """Intervalo del 95 % para las brechas, remuestreando casos de prueba."""
    rng = np.random.default_rng(seed)
    y, pred, groups = np.asarray(y), np.asarray(pred), np.asarray(groups)
    values = {"recall_gap": [], "fpr_gap": []}
    for _ in range(n):
        idx = rng.integers(0, len(y), len(y))
        _, by_group, _ = audit(y[idx], pred[idx], groups[idx])
        values["recall_gap"].append(gap(by_group, "recall"))
        values["fpr_gap"].append(gap(by_group, "fpr"))
    return {k: [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))] for k, v in values.items()}


def flag_small_cells(by_group: pd.DataFrame, min_n: int = MIN_CELL) -> pd.DataFrame:
    out = by_group.copy()
    out["n_suficiente"] = out["count"] >= min_n
    return out


def threshold_for_recall(probabilities: np.ndarray, y: np.ndarray, target: float) -> float:
    """Umbral global más alto que alcanza el recall objetivo en validación."""
    for threshold in np.round(np.arange(0.95, 0.04, -0.01), 2):
        if recall_score(y, (probabilities >= threshold).astype(int), zero_division=0) >= target:
            return float(threshold)
    return 0.05


def candidates(df: pd.DataFrame, target_recall: float = 0.80, seed: int = 42) -> tuple[pd.DataFrame, dict, dict]:
    """Evalúa alternativas en validación temporal (último 25 % del entrenamiento) y luego en prueba."""
    train, test = temporal_split(df)
    inner, valid = temporal_split(train)
    probe = build_model("logistic").fit(features(inner), inner.target)
    threshold = threshold_for_recall(probe.predict_proba(features(valid))[:, 1], valid.target.to_numpy(), target_recall)

    rows, predictions = [], {}
    for stage, fit_df, eval_df in [("validacion", inner, valid), ("prueba", train, test)]:
        logistic = build_model("logistic").fit(features(fit_df), fit_df.target)
        tree = build_model("tree").fit(features(fit_df), fit_df.target)
        proba = logistic.predict_proba(features(eval_df))[:, 1]
        optimizer = ThresholdOptimizer(estimator=build_model("logistic"), constraints="equalized_odds",
                                       objective="balanced_accuracy_score", predict_method="predict_proba")
        optimizer.fit(features(fit_df), fit_df.target, sensitive_features=fit_df.protected_group)
        preds = {
            "regla_no_predictiva": rule_baseline(eval_df),
            "logistica_0.50": (proba >= 0.5).astype(int),
            "arbol_0.50": tree.predict(features(eval_df)),
            f"logistica_{threshold:.2f}": (proba >= threshold).astype(int),
            "threshold_optimizer_eo": optimizer.predict(features(eval_df), sensitive_features=eval_df.protected_group,
                                                        random_state=seed),
        }
        for name, pred in preds.items():
            rows.append({"etapa": stage, "candidato": name, **summarize(eval_df.target, pred, eval_df.protected_group)})
        if stage == "prueba":
            predictions = preds
    return pd.DataFrame(rows), predictions, {"umbral_global": threshold, "recall_objetivo": target_recall,
                                             "train": len(train), "valid": len(valid), "test": len(test)}


def choose(valid_table: pd.DataFrame, gates: dict) -> tuple[str, str]:
    """Regla fijada antes de la prueba: descartar lo que usa el atributo protegido al decidir;
    entre los que cumplen las compuertas en validación, el de mayor recall; desempate por menor brecha de recall."""
    table = valid_table[(valid_table["etapa"] == "validacion") & (valid_table["candidato"] != "threshold_optimizer_eo")]
    ok = table[(table["recall"] >= gates["min_recall"]) & (table["recall_gap"] <= gates["max_recall_gap"])
               & (table["fpr_gap"] <= gates["max_fpr_gap"])]
    pool = ok if len(ok) else table
    chosen = pool.sort_values(["recall", "recall_gap"], ascending=[False, True]).iloc[0]["candidato"]
    reason = (f"Cumplen las compuertas en validación: {', '.join(ok['candidato']) or 'ninguno'}. "
              f"Se elige el de mayor recall: {chosen}. ThresholdOptimizer se excluye porque necesita el grupo protegido "
              "en el momento de decidir (tratamiento diferenciado explícito).")
    return str(chosen), reason


def final_decision(test_row: pd.Series, ci: dict, gates: dict, small_cells: int) -> dict:
    """Traduce la evidencia a desplegar / modificar / limitar / no utilizar."""
    passes = (test_row["recall"] >= gates["min_recall"] and test_row["recall_gap"] <= gates["max_recall_gap"]
              and test_row["fpr_gap"] <= gates["max_fpr_gap"])
    uncertain = ci["recall_gap"][1] > gates["max_recall_gap"] or ci["fpr_gap"][1] > gates["max_fpr_gap"]
    if not passes and test_row["recall"] < gates["min_recall"]:
        status = "no utilizar"
    elif not passes:
        status = "modificar"
    elif uncertain or small_cells:
        status = "limitar"
    else:
        status = "desplegar"
    return {"decision": status, "cumple_compuertas_en_prueba": bool(passes),
            "incertidumbre_supera_tolerancia": bool(uncertain), "celdas_interseccionales_pequenas": int(small_cells)}


__all__ = ["bootstrap_gaps", "candidates", "choose", "final_decision", "flag_small_cells", "intersectional",
           "rule_baseline", "summarize", "threshold_for_recall"]
