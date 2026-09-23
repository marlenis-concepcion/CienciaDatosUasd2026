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
from sklearn.decomposition import PCA

from .data import CLASS_NAMES, normalize_images, split_train_valid, validate_images
from .evaluation import choose, class_diversity, nearest_distances, pairwise_spread, reconstruction_errors
from .models import build_autoencoder, build_encoder_decoder, build_judge, make_vae_class

ROOT = Path(__file__).resolve().parents[2]
SEED = 42
N_SAMPLES = 1000
VAE_DIMS = [2, 16]


def set_seeds(tf) -> None:
    os.environ.setdefault("TF_DETERMINISTIC_OPS", "1")
    tf.keras.utils.set_random_seed(SEED)
    tf.config.experimental.enable_op_determinism()


def show_rows(path: Path, rows: dict[str, np.ndarray], title: str) -> None:
    figure, axes = plt.subplots(len(rows), 12, figsize=(12, 1.15 * len(rows) + 0.4))
    for r, (label, images) in enumerate(rows.items()):
        for c in range(12):
            axes[r, c].imshow(images[c].squeeze(), cmap="gray", vmin=0, vmax=1)
            axes[r, c].set_xticks([])
            axes[r, c].set_yticks([])
        axes[r, 0].set_ylabel(label, rotation=0, ha="right", va="center", fontsize=8)
    figure.suptitle(title, fontsize=10)
    figure.tight_layout()
    figure.savefig(path, dpi=150)
    plt.close(figure)


def run(epochs_ae: int = 30, epochs_vae: int = 40, reports: Path = ROOT / "reports",
        models_dir: Path = ROOT / "models") -> dict:
    import tensorflow as tf

    set_seeds(tf)
    reports.mkdir(exist_ok=True)
    models_dir.mkdir(exist_ok=True)
    (x_all_raw, y_all), (x_test_raw, y_test) = tf.keras.datasets.fashion_mnist.load_data()
    x_all, x_test = normalize_images(x_all_raw), normalize_images(x_test_raw)
    train_idx, valid_idx = split_train_valid(len(x_all), seed=SEED)
    x_train, x_valid = x_all[train_idx], x_all[valid_idx]
    for images in (x_train, x_valid, x_test):
        validate_images(images)
    np.savetxt(reports / "indices_validacion.csv", valid_idx, fmt="%d", header="indice_entrenamiento_oficial", comments="")
    stop = lambda: [tf.keras.callbacks.EarlyStopping(patience=3, restore_best_weights=True)]
    results, histories, generators, costs = {}, {}, {}, {}

    # Líneas base: imagen media y PCA lineal con la misma dimensión latente que el autoencoder.
    mean_image = x_train.mean(axis=0, keepdims=True)
    results["media"] = reconstruction_errors(x_test, np.repeat(mean_image, len(x_test), axis=0))
    costs["media"] = {"parametros": 784, "segundos": 0.0}
    start = perf_counter()
    pca = PCA(n_components=16, random_state=SEED).fit(x_train.reshape(len(x_train), -1))
    pca_test = pca.inverse_transform(pca.transform(x_test.reshape(len(x_test), -1))).reshape(x_test.shape)
    results["pca_16"] = reconstruction_errors(x_test, pca_test)
    costs["pca_16"] = {"parametros": int(pca.components_.size + pca.mean_.size), "segundos": perf_counter() - start}

    # Autoencoder del proyecto base (latente 16).
    tf.keras.utils.set_random_seed(SEED)
    autoencoder = build_autoencoder(tf)
    autoencoder.compile(optimizer="adam", loss="binary_crossentropy")
    start = perf_counter()
    history = autoencoder.fit(x_train, x_train, validation_data=(x_valid, x_valid), epochs=epochs_ae,
                              batch_size=256, callbacks=stop(), verbose=2)
    costs["ae_16"] = {"parametros": int(autoencoder.count_params()), "segundos": perf_counter() - start,
                      "epocas": len(history.history["loss"])}
    histories["ae_16"] = history.history
    ae_test = autoencoder.predict(x_test, verbose=0)
    results["ae_16"] = reconstruction_errors(x_test, ae_test)
    autoencoder.save(models_dir / "autoencoder.keras")
    costs["ae_16"]["tamano_kb"] = (models_dir / "autoencoder.keras").stat().st_size / 1024

    # VAE con latente 2 (proyecto base) y 16.
    VAE = make_vae_class(tf)
    valid_losses, recon = {}, {}
    for dim in VAE_DIMS:
        name = f"vae_{dim}"
        tf.keras.utils.set_random_seed(SEED)
        encoder, decoder = build_encoder_decoder(tf, latent_dim=dim)
        vae = VAE(encoder, decoder)
        vae.compile(optimizer="adam")
        start = perf_counter()
        history = vae.fit(x_train, validation_data=(x_valid,), epochs=epochs_vae, batch_size=256,
                          callbacks=stop(), verbose=2)
        costs[name] = {"parametros": int(encoder.count_params() + decoder.count_params()),
                       "segundos": perf_counter() - start, "epocas": len(history.history["loss"])}
        histories[name] = history.history
        evaluation = vae.evaluate(x_valid, verbose=0, return_dict=True)
        valid_losses[name] = float(evaluation["loss"])
        mean, _ = encoder.predict(x_test, verbose=0)
        recon[name] = decoder.predict(mean, verbose=0)
        results[name] = {**reconstruction_errors(x_test, recon[name]), "perdida_valid": valid_losses[name],
                         "kl_valid": float(evaluation["kl"])}
        decoder.save(models_dir / f"decoder_{dim}.keras")
        encoder.save(models_dir / f"encoder_{dim}.keras")
        costs[name]["tamano_kb"] = sum((models_dir / f).stat().st_size for f in
                                       [f"decoder_{dim}.keras", f"encoder_{dim}.keras"]) / 1024
        generators[name] = (encoder, decoder)
    if 2 in VAE_DIMS:
        # Compatibilidad con app/streamlit_app.py del proyecto base (latente 2).
        generators["vae_2"][1].save(models_dir / "decoder.keras")

    chosen, reason = choose(valid_losses)
    decision = {"modelo_elegido": chosen, "razon": reason,
                "regla": "VAE con menor pérdida total (reconstrucción + KL) en validación", "tomada_antes_de_test": True}
    (reports / "decision.json").write_text(json.dumps(decision, indent=2, ensure_ascii=False), encoding="utf-8")

    # Juez: clasificador entrenado solo con entrenamiento para medir fidelidad y diversidad.
    tf.keras.utils.set_random_seed(SEED)
    judge = build_judge(tf)
    judge.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    judge.fit(x_train, y_all[train_idx], validation_data=(x_valid, y_all[valid_idx]), epochs=5, batch_size=256, verbose=2)
    judge_accuracy = float(judge.evaluate(x_test, y_test, verbose=0)[1])

    # Muestreo desde la prior N(0, I), fidelidad, diversidad y memoria.
    rng = np.random.default_rng(SEED)
    test_to_train = nearest_distances(x_test[:N_SAMPLES], x_train)
    threshold = float(np.percentile(test_to_train, 5))
    generation = {"real_prueba": {**class_diversity(judge.predict(x_test[:N_SAMPLES], verbose=0)),
                                  "dispersion": pairwise_spread(x_test[:N_SAMPLES]),
                                  "dist_vecino_train_mediana": float(np.median(test_to_train)),
                                  "posibles_copias": float((test_to_train < threshold).mean())}}
    samples = {}
    for name, (encoder, decoder) in generators.items():
        dim = int(name.split("_")[1])
        samples[name] = decoder.predict(rng.normal(size=(N_SAMPLES, dim)), verbose=0)
        distances = nearest_distances(samples[name], x_train)
        generation[name] = {**class_diversity(judge.predict(samples[name], verbose=0)),
                            "dispersion": pairwise_spread(samples[name]),
                            "dist_vecino_train_mediana": float(np.median(distances)),
                            "posibles_copias": float((distances < threshold).mean())}
    generation["umbral_copia"] = threshold
    generation["exactitud_juez_prueba"] = judge_accuracy

    # Figuras: reconstrucción, muestras, interpolación, espacio latente y curvas.
    show_rows(reports / "reconstruccion.png",
              {"original": x_test[:12], "PCA 16": pca_test[:12], "AE 16": ae_test[:12],
               "VAE 2": recon["vae_2"][:12], "VAE 16": recon["vae_16"][:12]},
              "Reconstrucción de 12 imágenes de prueba")
    show_rows(reports / "muestras.png", {"VAE 2": samples["vae_2"][:12], "VAE 16": samples["vae_16"][:12]},
              "Muestras generadas desde N(0, I)")
    a_index, b_index = int(np.where(y_test == 7)[0][0]), int(np.where(y_test == 9)[0][0])
    steps = np.linspace(0, 1, 12)[:, None]
    rows = {"píxeles": np.array([(1 - t) * x_test[a_index] + t * x_test[b_index] for t in steps.ravel()])}
    for name, (encoder, decoder) in generators.items():
        mean, _ = encoder.predict(x_test[[a_index, b_index]], verbose=0)
        rows[name.replace("_", " ").upper()] = decoder.predict((1 - steps) * mean[0] + steps * mean[1], verbose=0)
    show_rows(reports / "interpolacion.png", rows, "Interpolación Sneaker → Ankle boot (prueba)")
    mean2, _ = generators["vae_2"][0].predict(x_test, verbose=0)
    figure, axis = plt.subplots(figsize=(6.5, 5))
    scatter = axis.scatter(mean2[:, 0], mean2[:, 1], c=y_test, cmap="tab10", s=2)
    axis.legend(handles=scatter.legend_elements()[0], labels=CLASS_NAMES, fontsize=6, markerscale=0.8, loc="best")
    axis.set_title("Espacio latente del VAE 2 · prueba")
    figure.tight_layout()
    figure.savefig(reports / "espacio_latente.png", dpi=160)
    plt.close(figure)
    figure, axes = plt.subplots(1, 3, figsize=(12, 3.2))
    for axis, name in zip(axes, histories):
        axis.plot(histories[name]["loss"], label="entrenamiento")
        axis.plot(histories[name]["val_loss"], "--", label="validación")
        axis.set_title(name)
        axis.set_xlabel("época")
        axis.legend(fontsize=7)
    figure.tight_layout()
    figure.savefig(reports / "curvas.png", dpi=160)
    plt.close(figure)

    table = pd.DataFrame([{"modelo": k, **v, **costs[k]} for k, v in results.items()])
    table.to_csv(reports / "reconstruccion.csv", index=False)
    pd.DataFrame([{"conjunto": k, **{m: v for m, v in d.items() if m != "reparto"}}
                  for k, d in generation.items() if isinstance(d, dict)]).to_csv(reports / "generacion.csv", index=False)
    hardware = {"sistema": platform.platform(), "tensorflow": tf.__version__,
                "gpu": [d.name for d in tf.config.list_physical_devices("GPU")]}
    (reports / "metricas.json").write_text(json.dumps({"reconstruccion": results, "costos": costs, "generacion": generation,
                                                       "hardware": hardware}, indent=2, ensure_ascii=False), encoding="utf-8")
    return {"reconstruction": table, "generation": generation, "decision": decision, "costs": costs}
