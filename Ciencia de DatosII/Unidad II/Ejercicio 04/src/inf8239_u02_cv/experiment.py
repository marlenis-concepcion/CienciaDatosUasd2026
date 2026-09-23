from __future__ import annotations

import json
import os
import platform
from pathlib import Path
from time import perf_counter

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score

from .data import CLASS_NAMES, audit_arrays, normalize_images, split_train_valid, validate_images
from .evaluation import choose, f1_macro, per_class, top_confusions
from .models import build_cnn, build_cnn_flatten, build_dense

ROOT = Path(__file__).resolve().parents[2]
SEED = 42


def set_seeds(tf) -> None:
    os.environ.setdefault("TF_DETERMINISTIC_OPS", "1")
    tf.keras.utils.set_random_seed(SEED)
    tf.config.experimental.enable_op_determinism()


def compile_model(model):
    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    return model


def plot_samples(x, y, path: Path) -> None:
    figure, axes = plt.subplots(2, 10, figsize=(12, 2.8))
    for label in range(10):
        for row, index in enumerate(np.where(y == label)[0][:2]):
            axes[row, label].imshow(x[index], cmap="gray")
            axes[row, label].axis("off")
        axes[0, label].set_title(CLASS_NAMES[label], fontsize=8)
    figure.suptitle("Dos ejemplos por clase · entrenamiento", fontsize=10)
    figure.tight_layout()
    figure.savefig(path, dpi=150)
    plt.close(figure)


def plot_curves(histories: dict, path: Path) -> None:
    figure, axes = plt.subplots(1, 2, figsize=(10, 3.6))
    for name, history in histories.items():
        epochs = np.arange(1, len(history["loss"]) + 1)
        for axis, metric in zip(axes, ["loss", "accuracy"]):
            axis.plot(epochs, history[metric], "-o", ms=3, label=f"{name} · entrenamiento")
            axis.plot(epochs, history[f"val_{metric}"], "--o", ms=3, label=f"{name} · validación")
    axes[0].set_title("Pérdida por época")
    axes[1].set_title("Accuracy por época")
    for axis in axes:
        axis.set_xlabel("época")
        axis.legend(fontsize=7)
    figure.tight_layout()
    figure.savefig(path, dpi=160)
    plt.close(figure)


def plot_errors(x, y_true, y_pred, path: Path) -> None:
    """Un error por clase real, para ver qué confunde el modelo en cada categoría."""
    figure, axes = plt.subplots(2, 5, figsize=(11, 6.2))
    for label, axis in zip(range(10), axes.ravel()):
        wrong = np.where((y_true == label) & (y_pred != label))[0]
        axis.axis("off")
        if len(wrong):
            index = wrong[0]
            axis.imshow(x[index].squeeze(), cmap="gray")
            axis.set_title(f"Real: {CLASS_NAMES[label]}\nPred.: {CLASS_NAMES[y_pred[index]]}", fontsize=8)
    figure.suptitle("Primer error de prueba por clase real", fontsize=10)
    figure.tight_layout(h_pad=2.5)
    figure.savefig(path, dpi=160)
    plt.close(figure)


def run(epochs: int = 30, reports: Path = ROOT / "reports", models_dir: Path = ROOT / "models") -> dict:
    import tensorflow as tf

    set_seeds(tf)
    reports.mkdir(exist_ok=True)
    models_dir.mkdir(exist_ok=True)
    (x_train_raw, y_train_all), (x_test_raw, y_test) = tf.keras.datasets.fashion_mnist.load_data()
    audit = audit_arrays(x_train_raw, y_train_all, x_test_raw, y_test)
    (reports / "auditoria.json").write_text(json.dumps(audit, indent=2, ensure_ascii=False), encoding="utf-8")
    plot_samples(x_train_raw, y_train_all, reports / "muestras.png")

    train_idx, valid_idx = split_train_valid(x_train_raw, y_train_all, random_state=SEED)
    x_all, x_test = normalize_images(x_train_raw), normalize_images(x_test_raw)
    x_train, y_train = x_all[train_idx], y_train_all[train_idx]
    x_valid, y_valid = x_all[valid_idx], y_train_all[valid_idx]
    for images, labels in [(x_train, y_train), (x_valid, y_valid), (x_test, y_test)]:
        validate_images(images, labels)
    partition = {"semilla": SEED, "entrenamiento": len(train_idx), "validacion": len(valid_idx), "prueba": len(y_test),
                 "validacion_por_clase": np.bincount(y_valid).tolist(), "indices_validacion_inicio": valid_idx[:10].tolist()}
    (reports / "particion.json").write_text(json.dumps(partition, indent=2), encoding="utf-8")
    np.savetxt(reports / "indices_validacion.csv", valid_idx, fmt="%d", header="indice_entrenamiento_oficial", comments="")

    baseline = DummyClassifier(strategy="most_frequent").fit(np.zeros((len(y_train), 1)), y_train)
    valid_scores = {"baseline": {"f1_macro": f1_macro(y_valid, baseline.predict(np.zeros((len(y_valid), 1))))}}
    trained, histories, costs = {}, {}, {}
    for name, factory in {"dense": build_dense, "cnn": build_cnn, "cnn_flatten": build_cnn_flatten}.items():
        tf.keras.utils.set_random_seed(SEED)
        model = compile_model(factory(tf))
        path = models_dir / f"{name}.keras"
        callbacks = [tf.keras.callbacks.EarlyStopping(patience=2, restore_best_weights=True)]
        start = perf_counter()
        history = model.fit(x_train, y_train, validation_data=(x_valid, y_valid), epochs=epochs,
                            batch_size=128, callbacks=callbacks, verbose=2)
        train_seconds = perf_counter() - start
        model.save(path)
        histories[name] = history.history
        valid_pred = model.predict(x_valid, verbose=0).argmax(axis=1)
        valid_scores[name] = {"f1_macro": f1_macro(y_valid, valid_pred), "accuracy": float(accuracy_score(y_valid, valid_pred)),
                              "epocas": len(history.history["loss"]),
                              "parametros": int(model.count_params())}
        costs[name] = {"parametros": int(model.count_params()), "segundos_entrenamiento": train_seconds,
                       "tamano_kb": path.stat().st_size / 1024}
        trained[name] = model
    pd.concat([pd.DataFrame(h).assign(modelo=n, epoca=lambda d: d.index + 1) for n, h in histories.items()]).to_csv(
        reports / "historial.csv", index=False)
    plot_curves(histories, reports / "curvas.png")

    chosen, reason = choose({k: v for k, v in valid_scores.items() if k != "baseline"})
    decision = {"modelo_elegido": chosen, "razon": reason,
                "regla": "Menos parámetros entre los modelos a menos de 0.01 del mejor F1 macro de validación",
                "tomada_antes_de_test": True}
    (reports / "decision.json").write_text(json.dumps(decision, indent=2, ensure_ascii=False), encoding="utf-8")

    metrics = {"baseline": {"f1_macro_valid": valid_scores["baseline"]["f1_macro"],
                            "f1_macro": f1_macro(y_test, baseline.predict(np.zeros((len(y_test), 1)))),
                            "accuracy": float(accuracy_score(y_test, baseline.predict(np.zeros((len(y_test), 1))))),
                            "parametros": 0}}
    predictions = {}
    for name, model in trained.items():
        model.predict(x_test[:256], verbose=0)  # calentamiento para no medir la compilación
        start = perf_counter()
        pred = model.predict(x_test, batch_size=256, verbose=0).argmax(axis=1)
        inference = perf_counter() - start
        predictions[name] = pred
        metrics[name] = {"f1_macro_valid": valid_scores[name]["f1_macro"], "epocas": valid_scores[name]["epocas"],
                         "f1_macro": f1_macro(y_test, pred), "accuracy": float(accuracy_score(y_test, pred)),
                         **costs[name], "inferencia_ms_por_imagen": 1000 * inference / len(y_test)}
    metrics["hardware"] = {"cpu": platform.processor() or platform.machine(), "sistema": platform.platform(),
                           "tensorflow": tf.__version__, "gpu": [d.name for d in tf.config.list_physical_devices("GPU")]}
    (reports / "cv_metrics.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8")

    best = predictions[chosen]
    table = per_class(y_test, best)
    table.to_csv(reports / "metricas_por_clase.csv", index=False)
    for name, pred in predictions.items():
        per_class(y_test, pred).to_csv(reports / f"metricas_por_clase_{name}.csv", index=False)
    confusions = top_confusions(y_test, best)
    confusions.to_csv(reports / "confusiones_principales.csv", index=False)
    figure, axis = plt.subplots(figsize=(7.5, 6.5))
    ConfusionMatrixDisplay.from_predictions(y_test, best, display_labels=CLASS_NAMES, cmap="Blues",
                                            xticks_rotation=45, ax=axis, colorbar=False)
    axis.set_title(f"Matriz de confusión · {chosen} · prueba")
    figure.tight_layout()
    figure.savefig(reports / "confusion_cnn.png", dpi=160)
    plt.close(figure)
    plot_errors(x_test, y_test, best, reports / "cnn_errors.png")
    return {"audit": audit, "partition": partition, "valid": valid_scores, "decision": decision,
            "metrics": metrics, "per_class": table, "confusions": confusions}
