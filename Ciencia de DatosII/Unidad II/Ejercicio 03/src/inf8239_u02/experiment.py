from __future__ import annotations

import json
from pathlib import Path
from time import perf_counter

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    PrecisionRecallDisplay,
    accuracy_score,
    f1_score,
    precision_recall_fscore_support,
)
from sklearn.model_selection import GridSearchCV, StratifiedKFold

from .config import ROOT, settings
from .data import check_no_leakage, deduplicate, load_dataset, split_data, validate_dataframe
from .modeling import PARAM_GRIDS, build_models

POSITIVE = "spam"
MIN_ERRORS = 20


def prepare(random_state: int = settings.random_state) -> tuple[dict[str, pd.DataFrame], dict]:
    df = load_dataset()
    validate_dataframe(df, settings.text_column, settings.target_column)
    clean, summary = deduplicate(df, settings.text_column, settings.target_column)
    splits = split_data(clean, settings.target_column, random_state)
    check_no_leakage(splits, settings.text_column)
    return splits, summary


def scores(y_true, y_pred) -> dict:
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true, y_pred, labels=["ham", "spam"], zero_division=0
    )
    return {
        "f1_macro": float(f1_score(y_true, y_pred, average="macro", zero_division=0)),
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision_spam": float(precision[1]),
        "recall_spam": float(recall[1]),
        "f1_spam": float(f1[1]),
        "recall_ham": float(recall[0]),
    }


def tune(splits: dict[str, pd.DataFrame], random_state: int = settings.random_state):
    x, y = splits["train"][settings.text_column], splits["train"][settings.target_column]
    folds = StratifiedKFold(n_splits=5, shuffle=True, random_state=random_state)
    base = build_models(random_state)
    fitted, cv_rows = {"dummy": base["dummy"].fit(x, y)}, []
    for name, grid in PARAM_GRIDS.items():
        search = GridSearchCV(base[name], grid, scoring="f1_macro", cv=folds, n_jobs=1)
        start = perf_counter()
        search.fit(x, y)
        seconds = perf_counter() - start
        fitted[name] = search.best_estimator_
        cv_rows.append({
            "modelo": name,
            "mejores_parametros": json.dumps({k: str(v) for k, v in search.best_params_.items()}),
            "f1_macro_cv": float(search.best_score_),
            "f1_macro_cv_std": float(search.cv_results_["std_test_score"][search.best_index_]),
            "combinaciones": len(search.cv_results_["params"]),
            "segundos_busqueda": seconds,
        })
    return fitted, pd.DataFrame(cv_rows)


def choose(valid_table: pd.DataFrame) -> str:
    """Elige por F1 macro en validación; empata a favor del recall de spam."""
    candidates = valid_table[valid_table["modelo"] != "dummy"]
    ordered = candidates.sort_values(["f1_macro", "recall_spam"], ascending=False)
    return str(ordered.iloc[0]["modelo"])


def collect_errors(fitted, splits, chosen: str) -> pd.DataFrame:
    """Errores del modelo elegido en test; si no llegan a 20, se completa con validación."""
    frames = []
    for split in ["test", "valid"]:
        part = splits[split]
        model = fitted[chosen]
        pred = model.predict(part[settings.text_column])
        proba = model.predict_proba(part[settings.text_column])[:, list(model.classes_).index(POSITIVE)]
        wrong = part.assign(predicho=pred, prob_spam=proba.round(3), particion=split)
        frames.append(wrong[wrong[settings.target_column] != wrong["predicho"]])
        if sum(len(f) for f in frames) >= MIN_ERRORS:
            break
    errors = pd.concat(frames).rename(columns={settings.target_column: "real"})
    errors = errors.assign(modelo=chosen)[["id", "particion", "modelo", "real", "predicho", "prob_spam", settings.text_column]]
    categories = ROOT / "docs/error_categories.csv"
    if categories.exists():
        errors = errors.merge(pd.read_csv(categories), on="id", how="left")
    else:
        errors["categoria"], errors["explicacion"] = "REVISAR", ""
    return errors


def run(reports: Path = ROOT / "reports", models_dir: Path = ROOT / "models") -> dict:
    reports.mkdir(exist_ok=True)
    models_dir.mkdir(exist_ok=True)
    splits, dedup = prepare()
    pd.concat([p[["id"]].assign(particion=n) for n, p in splits.items()]).sort_values("id").to_csv(
        reports / "particiones.csv", index=False
    )
    fitted, cv_table = tune(splits)
    cv_table.to_csv(reports / "busqueda_cv.csv", index=False)

    valid_rows = []
    for name, model in fitted.items():
        pred = model.predict(splits["valid"][settings.text_column])
        valid_rows.append({"modelo": name, **scores(splits["valid"][settings.target_column], pred)})
    valid_table = pd.DataFrame(valid_rows)
    chosen = choose(valid_table)
    decision = {"modelo_elegido": chosen, "criterio": "F1 macro en validación; desempate por recall de spam",
                "tomada_antes_de_test": True}
    (reports / "decision.json").write_text(json.dumps(decision, indent=2, ensure_ascii=False), encoding="utf-8")

    x_test, y_test = splits["test"][settings.text_column], splits["test"][settings.target_column]
    rows = []
    for name, model in fitted.items():
        start = perf_counter()
        pred = model.predict(x_test)
        ms = 1000 * (perf_counter() - start) / len(x_test)
        path = models_dir / f"{name}.joblib"
        joblib.dump(model, path)
        val = valid_table.set_index("modelo").loc[name]
        rows.append({
            "modelo": name, "f1_macro_valid": val["f1_macro"], **{f"{k}_test": v for k, v in scores(y_test, pred).items()},
            "inferencia_ms_por_texto": ms, "tamano_kb": path.stat().st_size / 1024,
        })
    results = pd.DataFrame(rows)
    results.to_csv(reports / "text_metrics.csv", index=False)
    joblib.dump(fitted[chosen], models_dir / "text_model.joblib")

    best = fitted[chosen]
    pred = best.predict(x_test)
    report = precision_recall_fscore_support(y_test, pred, labels=["ham", "spam"], zero_division=0)
    pd.DataFrame(np.array(report).T, index=["ham", "spam"], columns=["precision", "recall", "f1", "soporte"]).to_csv(
        reports / "metricas_por_clase.csv", index_label="clase"
    )
    figure, axes = plt.subplots(1, 2, figsize=(10, 4))
    ConfusionMatrixDisplay.from_predictions(y_test, pred, cmap="Blues", ax=axes[0], colorbar=False)
    axes[0].set_title(f"Matriz de confusión · {chosen} · test")
    for name in ["naive_bayes", "logistic"]:
        PrecisionRecallDisplay.from_estimator(fitted[name], x_test, y_test, pos_label=POSITIVE, ax=axes[1], name=name)
    axes[1].set_title("Precisión-recall de spam · test")
    figure.tight_layout()
    figure.savefig(reports / "confusion_text.png", dpi=160)
    plt.close(figure)

    errors = collect_errors(fitted, splits, chosen)
    errors.to_csv(reports / "error_analysis.csv", index=False)
    counts = {k: {s: int((v[settings.target_column] == s).sum()) for s in ["ham", "spam"]} for k, v in splits.items()}
    return {"dedup": dedup, "splits": counts, "cv": cv_table, "valid": valid_table, "decision": decision,
            "results": results, "errors": errors}
