# Ejercicio 06 · VAE, evaluación y Model Card

**Autora:** Marlenis Judith Concepción Cuevas · **Asignatura:** INF-8239-C2 · **Unidad:** III · **Docente:** Edwin Ramón José Nolasco

Integra LAB10 (VAE con Fashion-MNIST) sobre el proyecto base `INF8239_U03_Generativos_Proyecto_Base`.

## Resultado principal

| Modelo | MSE por píxel (prueba) | Pérdida validación | Clases generadas | Entropía de clases | Posibles copias | Parámetros |
|---|---|---|---|---|---|---|
| Imagen media (línea base) | 0.0866 | — | — | — | — | 784 |
| PCA 16 (línea base) | 0.0198 | — | — | — | — | 13 328 |
| AE 16 (proyecto base) | 0.0179 | — | — | — | — | 25 888 |
| VAE 2 (proyecto base) | 0.0292 | 262.9 | 9 | 0.883 | 19.0 % | 202 516 |
| **VAE 16 (elegido)** | **0.0140** | **242.6** | **10** | **0.981** | **0.5 %** | 207 920 |

Regla fijada en validación (`reports/decision.json`): el VAE con menor pérdida total (reconstrucción + KL). Fidelidad, diversidad y memoria, costo y límites en [`MODEL_CARD.md`](MODEL_CARD.md).

## Estructura

- `notebooks/ejercicio_06.ipynb`: cuaderno ejecutado; recarga los modelos guardados y comprueba que reproducen las métricas.
- `src/inf8239_u03_gen/`: `data.py` (normalización, partición), `models.py` (AE, VAE con validación, clasificador juez), `evaluation.py` (reconstrucción, vecino más cercano, diversidad, decisión), `experiment.py`.
- `scripts/`: `check_runtime.py`, `train_ae_vae.py`, `make_report.py`.
- `tests/`: 12 pruebas.
- `models/`: autoencoder y codificador/decodificador de ambos VAE (`decoder.keras` es el VAE 2 que usa `app/streamlit_app.py`).
- `reports/`: reconstrucción, generación, curvas, muestras, interpolación, espacio latente, métricas y `Ejercicio_06.pdf`.

## Instalación

```bash
uv python install 3.12
uv sync --extra cpu
uv run python scripts/check_runtime.py
```

Alternativa con pip (Python 3.12): `pip install -r requirements.txt` y luego `pip install -e . --no-deps`. GPU: solo WSL2/Linux con NVIDIA, `uv sync --extra gpu`.

## Ejecución

```bash
uv run python scripts/train_ae_vae.py     # unos 3 minutos en CPU
uv run python scripts/make_report.py      # reports/Ejercicio_06.pdf
uv run pytest -q
uv run jupyter nbconvert --to notebook --execute --inplace notebooks/ejercicio_06.ipynb
uv run streamlit run app/streamlit_app.py # explorador del espacio latente (VAE 2)
```

## Datos y particiones

Fashion-MNIST (Xiao, Rasul y Vollgraf, 2017, [arXiv:1708.07747](https://arxiv.org/abs/1708.07747); licencia MIT), descargado con `tf.keras.datasets`. No se usa ni se redistribuye MovieLens. Validación: 6000 imágenes aleatorias del entrenamiento oficial (semilla 42, `reports/indices_validacion.csv`); prueba: 10 000 oficiales.

## Cómo se mide

- **Reconstrucción:** MSE por píxel y BCE por imagen en prueba.
- **Fidelidad:** confianza de un clasificador juez entrenado solo con entrenamiento (exactitud 0.893).
- **Diversidad:** clases cubiertas, entropía del reparto de clases y distancia media entre pares.
- **Memoria:** distancia de cada muestra a su vecino más cercano en entrenamiento; posible copia si es menor que la del 95 % de las imágenes reales de prueba.

## Pruebas automatizadas

12 pruebas, todas aprobadas (`uv run pytest -q`, resultado en `reports/pruebas.txt`). Tabla completa con el criterio de la rúbrica en [`docs/PRUEBAS.md`](docs/PRUEBAS.md).

1. **`test_normalization_contract`** (proyecto base). Las imágenes pasan de 0–255 a 0–1 con un canal (28×28×1) y superan la validación. *Por qué:* La pérdida BCE del VAE solo tiene sentido con píxeles entre 0 y 1.
2. **`test_rejects_wrong_shape`** (proyecto base). Falla si una imagen no tiene forma 28×28×1. *Por qué:* Detiene el proceso antes de entrenar con datos mal cargados.
3. **`test_autoencoder_output_contract`** (proyecto base). El autoencoder devuelve una imagen del mismo tamaño que la entrada. *Por qué:* Sin esto no se puede calcular el error de reconstrucción contra la original.
4. **`test_decoder_output_contract`** (proyecto base). El decodificador convierte un punto latente en una imagen 28×28×1. *Por qué:* Es la pieza que genera muestras e interpolaciones.
5. **`test_encoder_returns_mean_and_log_variance_with_latent_size`** (nueva). El codificador del VAE devuelve media y log-varianza del tamaño latente pedido (16). *Por qué:* El VAE necesita ambas salidas para el truco de reparametrización y la KL; con el tamaño equivocado la comparación VAE 2 vs VAE 16 no sería válida.
6. **`test_vae_losses_are_finite_and_kl_is_non_negative`** (nueva). La reconstrucción es un número finito y la divergencia KL no es negativa. *Por qué:* La KL nunca puede ser negativa; si lo fuera, la pérdida estaría mal implementada y la decisión basada en ella sería inválida.
7. **`test_validation_split_is_disjoint_complete_and_reproducible`** (nueva). Entrenamiento y validación no comparten imágenes, cubren todo el conjunto y la semilla 42 repite la misma partición. *Por qué:* El proyecto base usaba validation_split (las últimas imágenes, sin barajar) y el VAE no tenía validación; ahora la decisión se toma con una validación explícita y reproducible.
8. **`test_reconstruction_error_is_zero_for_perfect_copy_and_grows_with_noise`** (nueva). El error es cero para una copia perfecta y aumenta si la reconstrucción es gris uniforme. *Por qué:* Confirma que la tabla de reconstrucción ordena bien a los modelos (media > PCA > AE > VAE 16).
9. **`test_nearest_distance_detects_a_memorized_copy`** (nueva). Una muestra idéntica a una imagen de entrenamiento tiene distancia 0 al vecino más cercano; una aleatoria no. *Por qué:* Es la base de la medida de memoria: si el modelo copiara imágenes de entrenamiento se detectaría.
10. **`test_class_diversity_distinguishes_collapse_from_variety`** (nueva). Si todas las muestras son de una clase la entropía es 0; si se reparten en 10 clases es 1. *Por qué:* Detecta el colapso de modos: un generador que solo produce una prenda tendría buena fidelidad pero cero diversidad.
11. **`test_pairwise_spread_is_zero_when_all_samples_are_equal`** (nueva). La dispersión entre muestras es 0 cuando todas son iguales. *Por qué:* Segunda medida de diversidad que no depende del clasificador juez.
12. **`test_choose_prefers_lower_validation_loss`** (nueva). La regla elige el VAE con menor pérdida total de validación. *Por qué:* Fija la decisión antes de mirar la prueba; la pérdida total (reconstrucción + KL) es comparable entre dimensiones latentes.

## Uso de IA

Claude Code, Codex y DeepSeek. Detalle, prompts, verificaciones y correcciones en [`AI_USE_DECLARATION.md`](AI_USE_DECLARATION.md).

## Entrega

PDF: [`reports/Ejercicio_06.pdf`](reports/Ejercicio_06.pdf).
