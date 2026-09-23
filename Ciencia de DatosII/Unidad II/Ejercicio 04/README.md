# Ejercicio 04 · Clasificador visual con CNN y Model Card

**Autora:** Marlenis Judith Concepción Cuevas · **Asignatura:** INF-8239-C2 · **Unidad:** II · **Docente:** Edwin Ramón José Nolasco

Integra LAB07 (CNN con Fashion-MNIST) sobre el proyecto base `INF8239_U02_CV_Proyecto_Base`.

## Resultado principal

| Modelo | F1 macro validación | F1 macro prueba | Parámetros | Entrenamiento (s) | Inferencia (ms/img) |
|---|---|---|---|---|---|
| Línea base (clase más frecuente) | 0.018 | 0.018 | 0 | — | — |
| Denso (proyecto base) | 0.888 | 0.876 | 50 890 | 10.9 | 0.008 |
| CNN pequeña (proyecto base) | 0.854 | 0.847 | 19 466 | 188.2 | 0.028 |
| **CNN Flatten (elegida)** | **0.926** | **0.919** | 421 642 | 86.8 | 0.032 |

Regla fijada antes de la prueba (`reports/decision.json`): elegir el modelo con menos parámetros entre los que están a menos de 0.01 del mejor F1 macro de validación. Métricas por clase, costo, límites y monitoreo en [`MODEL_CARD.md`](MODEL_CARD.md).

## Estructura

- `notebooks/ejercicio_04.ipynb`: cuaderno ejecutado; recalcula auditoría y partición, carga los modelos guardados y los evalúa.
- `src/inf8239_u02_cv/`: `data.py` (normalización, auditoría por hash, partición), `models.py` (denso, CNN base, CNN Flatten), `evaluation.py` (métricas por clase, confusiones, regla de decisión), `experiment.py`.
- `scripts/`: `check_runtime.py`, `train_cv.py`, `make_report.py`.
- `tests/`: 9 pruebas.
- `models/`: los tres modelos entrenados (`.keras`).
- `reports/`: auditoría, partición, historial, curvas, métricas, confusiones, errores, pruebas, `corrida_8_epocas/` y `Ejercicio_04.pdf`.
- `docs/DECLARACION_IA.md`: uso de IA, prompts, verificaciones y correcciones.

## Instalación

Con [uv](https://docs.astral.sh/uv/), como indica el proyecto base (CPU):

```bash
uv python install 3.12
uv sync --extra cpu
uv run python scripts/check_runtime.py
```

Alternativa con pip (Python 3.12):

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e . --no-deps
```

GPU: solo en WSL2/Linux con NVIDIA, `uv sync --extra gpu`.

## Ejecución

```bash
uv run python scripts/train_cv.py        # unos 5 minutos en CPU; máximo 30 épocas con parada temprana
uv run python scripts/make_report.py     # reports/Ejercicio_04.pdf
uv run pytest -q
uv run jupyter nbconvert --to notebook --execute --inplace notebooks/ejercicio_04.ipynb
```

`scripts/train_cv.py --epochs 8` reproduce la corrida corta del proyecto base, guardada en `reports/corrida_8_epocas/`.

## Datos y reproducibilidad

Fashion-MNIST (Xiao, Rasul y Vollgraf, 2017, [arXiv:1708.07747](https://arxiv.org/abs/1708.07747); licencia MIT) se descarga con `tf.keras.datasets.fashion_mnist` y se guarda en `~/.keras/datasets/`.

- Auditoría por hash: sin duplicados en entrenamiento ni en prueba, sin imágenes compartidas entre ambos y sin etiquetas contradictorias.
- Validación: 6000 imágenes estratificadas del entrenamiento oficial, semilla 42 (`reports/indices_validacion.csv`). La prueba oficial de 10 000 se evalúa una sola vez, después de la decisión.
- Semillas fijas y operaciones deterministas de TensorFlow; al recargar los modelos guardados se obtienen las mismas métricas.

## Hallazgo principal

Con las 8 épocas del proyecto base, la CNN pequeña obtuvo F1 0.785, por debajo del modelo denso; con 30 épocas seguía mejorando lentamente (0.847). Promedia cada mapa de activación y pierde la posición de los rasgos. La variante con Flatten converge en 12 épocas y supera al denso por 0.04. La clase más difícil es Shirt (recall 0.728), que se confunde con T-shirt/top, Coat y Pullover.

## Entrega

PDF: [`reports/Ejercicio_04.pdf`](reports/Ejercicio_04.pdf).
