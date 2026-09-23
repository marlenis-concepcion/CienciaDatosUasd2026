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

## Pruebas automatizadas

9 pruebas, todas aprobadas (`uv run pytest -q`, resultado en `reports/pruebas.txt`). La tabla completa, con el criterio de la rúbrica de cada una, está en [`docs/PRUEBAS.md`](docs/PRUEBAS.md).

1. **`test_normalize_adds_channel_and_scales`** (proyecto base). Las imágenes pasan de 0–255 a 0–1 y reciben el canal (28×28×1). *Por qué:* La red espera ese formato y esa escala; con píxeles sin escalar el entrenamiento es inestable.
2. **`test_validate_rejects_wrong_shape`** (proyecto base). Falla si una imagen no tiene la forma 28×28×1. *Por qué:* Detiene el proceso antes de entrenar con datos mal cargados en lugar de fallar dentro de Keras con un error poco claro.
3. **`test_cnn_output_contract`** (proyecto base). La CNN del proyecto base devuelve 10 probabilidades por imagen que suman 1. *Por qué:* Confirma que la salida es una distribución válida sobre las 10 clases; sin eso las métricas no tienen sentido.
4. **`test_other_models_output_probabilities[build_dense]`** (nueva). El modelo denso cumple el mismo contrato: 10 probabilidades que suman 1. *Por qué:* Los tres modelos se comparan con las mismas métricas, así que deben producir el mismo tipo de salida.
5. **`test_other_models_output_probabilities[build_cnn_flatten]`** (nueva). La CNN Flatten (la elegida) cumple el mismo contrato. *Por qué:* Es el modelo que se entrega; se verifica igual que el del profesor.
6. **`test_validation_split_is_disjoint_stratified_and_reproducible`** (nueva). Entrenamiento y validación no comparten imágenes, suman el total, cada clase tiene la misma cantidad en validación y con la semilla 42 la partición es idéntica al repetirla. *Por qué:* El proyecto base tomaba las últimas 6000 imágenes sin estratificar; la prueba garantiza una validación equilibrada y reproducible, sin tocar la prueba oficial.
7. **`test_audit_detects_train_images_repeated_in_test`** (nueva). La auditoría por hash detecta una imagen de entrenamiento copiada en prueba. *Por qué:* En Fashion-MNIST se encontraron 0 copias; la prueba demuestra que la auditoría sí las habría encontrado, así que ese 0 es confiable.
8. **`test_choose_prefers_cheaper_model_within_tolerance`** (nueva). Si dos modelos están a menos de 0.01 de F1, se elige el de menos parámetros; si la diferencia es mayor, se elige el mejor. *Por qué:* Fija la regla de decisión técnica antes de ver la prueba: solo se paga más costo si la mejora es real.
9. **`test_per_class_and_confusions_count_errors`** (nueva). Los errores por clase y las confusiones principales (por ejemplo Shirt → T-shirt/top) se cuentan correctamente en un caso pequeño calculado a mano. *Por qué:* Las tablas de errores por clase del PDF y la Model Card salen de estas funciones; la prueba confirma que los conteos son correctos.

## Hallazgo principal

Con las 8 épocas del proyecto base, la CNN pequeña obtuvo F1 0.785, por debajo del modelo denso; con 30 épocas seguía mejorando lentamente (0.847). Promedia cada mapa de activación y pierde la posición de los rasgos. La variante con Flatten converge en 12 épocas y supera al denso por 0.04. La clase más difícil es Shirt (recall 0.728), que se confunde con T-shirt/top, Coat y Pullover.

## Entrega

PDF: [`reports/Ejercicio_04.pdf`](reports/Ejercicio_04.pdf).
