# Ejercicio 03 · Corpus público y clasificador de texto reproducible

**Autora:** Marlenis Judith Concepción Cuevas · **Asignatura:** INF-8239-C2 · **Unidad:** II · **Docente:** Edwin Ramón José Nolasco

Integra LAB04 (búsqueda, descarga y auditoría de un corpus) y LAB05 (TF-IDF, Naive Bayes y modelo lineal) sobre el proyecto base `INF8239_U02_NLP_Proyecto_Base`.

**Pregunta:** ¿puede un clasificador TF-IDF separar SMS no deseados (`spam`) de mensajes legítimos (`ham`) con un F1 macro claramente superior a una línea base, sin que los mensajes repetidos inflen el resultado?

## Resultado principal

| Modelo | F1 macro validación | F1 macro prueba | Precisión spam | Recall spam |
|---|---|---|---|---|
| Línea base (clase mayoritaria) | 0.468 | 0.468 | 0.000 | 0.000 |
| **TF-IDF + Naive Bayes (elegido)** | **0.954** | **0.976** | 0.957 | 0.957 |
| TF-IDF + regresión logística | 0.954 | 0.969 | 0.946 | 0.946 |

El modelo se eligió con validación y la decisión se guardó antes de evaluar en prueba (`reports/decision.json`). La diferencia entre ambos pipelines es pequeña y no concluyente.

## Estructura

- `notebooks/ejercicio_03.ipynb`: cuaderno ejecutado de principio a fin.
- `src/inf8239_u02/`: código reutilizable (`data.py`, `modeling.py`, `experiment.py`, `config.py`).
- `scripts/`: descarga, auditoría, entrenamiento, PDF y, del proyecto base, embeddings/red (LAB06, fuera de este ejercicio).
- `tests/`: 13 pruebas (6 del proyecto base y 7 de fuga, deduplicación, partición, decisión y errores).
- `docs/`: Dataset Card, comparación de candidatos, categorías de errores y declaración de uso de IA.
- `reports/`: auditoría, búsqueda, métricas, figuras, análisis de errores, pruebas y `Ejercicio_03.pdf`.
- `app/streamlit_app.py`: demostración del modelo (proyecto base).

## Instalación

Con [uv](https://docs.astral.sh/uv/), como indica el proyecto base:

```bash
uv python install 3.12
uv sync
```

Alternativa con pip (Python 3.12):

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e . --no-deps
```

## Ejecución

```bash
uv run python scripts/download_data.py   # descarga UCI y verifica SHA-256
uv run python scripts/audit_data.py      # auditoría -> reports/auditoria.*
uv run python scripts/train_text.py      # búsqueda, decisión, prueba y errores
uv run python scripts/make_report.py     # reports/Ejercicio_03.pdf
uv run pytest -q
uv run jupyter nbconvert --to notebook --execute --inplace notebooks/ejercicio_03.ipynb
```

Opcional: `uv run streamlit run app/streamlit_app.py`.

## Datos y reproducibilidad

Corpus: [SMS Spam Collection, UCI 228](https://archive.ics.uci.edu/dataset/228/sms+spam+collection). Almeida y Gómez Hidalgo (2011), [DOI 10.24432/C5CC84](https://doi.org/10.24432/C5CC84), licencia CC BY 4.0. Ficha completa en [`docs/DATASET_CARD.md`](docs/DATASET_CARD.md).

`scripts/download_data.py` descarga `https://archive.ics.uci.edu/static/public/228/sms+spam+collection.zip`, comprueba SHA-256 `1587ea43e58e82b14ff1f5425c88e17f8496bfcdb67a583dbff9eefaf9963ce3` y genera `data/raw/sms_spam.csv` (`id,text,label`). Si la suma no coincide, elimina el archivo y falla. `data/` no se versiona. La configuración se puede cambiar copiando `.env.example` a `.env`.

- 5574 mensajes; 434 duplicados al normalizar (403 exactos), eliminados **antes** de partir → 5140.
- Partición estratificada 70/15/15, semilla 42; índices en `reports/particiones.csv`.
- TF-IDF dentro del pipeline, ajustado solo con entrenamiento.
- Hiperparámetros por validación cruzada de 5 pliegues sobre entrenamiento, con la misma rejilla de TF-IDF para ambos pipelines.
- Dos ejecuciones completas producen las mismas métricas y los mismos errores.

## Pruebas automatizadas

13 pruebas, todas aprobadas (`uv run pytest -q`, resultado en `reports/pruebas.txt`). La tabla completa, con el criterio de la rúbrica de cada una, está en [`docs/PRUEBAS.md`](docs/PRUEBAS.md).

1. **`test_accepts_valid_dataframe`** (proyecto base). Un DataFrame con texto y etiqueta válidos pasa la validación sin error. *Por qué:* Asegura que la validación no rechaza datos correctos; si lo hiciera bloquearía todo el flujo.
2. **`test_rejects_missing_target`** (proyecto base). Falla con un mensaje claro si falta la columna objetivo. *Por qué:* Sin la etiqueta no se puede entrenar; es mejor detenerse que entrenar con una columna equivocada.
3. **`test_rejects_empty_text`** (proyecto base). Falla si hay textos vacíos. *Por qué:* Un texto vacío no aporta información y distorsiona TF-IDF y las métricas.
4. **`test_each_pipeline_predicts_one_label`** (proyecto base). Los tres pipelines (línea base, Naive Bayes y logística) entrenan y devuelven una predicción, y todos tienen los pasos tfidf y model. *Por qué:* Confirma que los tres modelos comparados tienen la misma estructura; así la comparación es justa.
5. **`test_tokenize_normalizes_and_removes_one_character_tokens`** (proyecto base). La tokenización pasa a minúsculas y elimina tokens de una letra. *Por qué:* Documenta cómo se normaliza el texto; si cambiara sin aviso cambiarían los resultados.
6. **`test_demo_network_has_valid_pagerank`** (proyecto base). El PageRank de la red de demostración suma 1 y cada valor está entre 0 y 1. *Por qué:* Comprueba que el entorno de LAB06 funciona; no forma parte de la evaluación de este ejercicio.
7. **`test_deduplicate_removes_normalized_copies_before_split`** (nueva). "Call 0800 NOW" y "call  0999 now" se reconocen como el mismo mensaje y se conserva solo el primero. *Por qué:* El corpus tiene 403 duplicados exactos y 31 más que solo difieren en mayúsculas, números o espacios; si no se eliminan, la misma plantilla de spam puede quedar en entrenamiento y en prueba.
8. **`test_deduplicate_rejects_contradictory_labels`** (nueva). Si un mismo texto aparece como ham y como spam el proceso se detiene. *Por qué:* Una etiqueta contradictoria indica un error de datos; eliminarla en silencio ocultaría el problema. En este corpus hay 0 casos, y la prueba garantiza que se detectarían.
9. **`test_splits_are_disjoint_complete_and_stratified`** (nueva). Entrenamiento, validación y prueba no comparten filas, entre las tres cubren todo el corpus y cada una mantiene la proporción de spam. *Por qué:* Si una fila estuviera en dos particiones la evaluación sería optimista; si se perdieran filas o cambiara la proporción la comparación dejaría de ser válida.
10. **`test_leakage_check_detects_normalized_duplicate_across_splits`** (nueva). El control de fuga detecta dos mensajes que solo difieren en números y mayúsculas aunque estén en particiones distintas. *Por qué:* Demuestra que la verificación que se ejecuta en cada corrida sí encuentra la fuga que se quiere evitar.
11. **`test_vectorizer_learns_vocabulary_only_from_training_texts`** (nueva). Una palabra que solo aparece en el texto de prueba no entra al vocabulario TF-IDF. *Por qué:* Si TF-IDF se ajustara con todos los datos, el modelo conocería palabras e IDF de la prueba antes de evaluarse; el pipeline lo evita y la prueba lo demuestra.
12. **`test_choose_ignores_baseline_and_breaks_ties_by_spam_recall`** (nueva). La regla de selección nunca elige la línea base y, si hay empate en F1 macro, prefiere el modelo con mayor recall de spam. *Por qué:* La decisión se toma en validación antes de ver la prueba; la prueba fija esa regla para que no se pueda ajustar después según el resultado.
13. **`test_every_analyzed_error_has_category_and_explanation`** (nueva). Hay al menos 20 errores clasificados, sin ids repetidos y todos con categoría y explicación. *Por qué:* La rúbrica exige analizar 20 errores; la prueba evita entregar errores sin interpretar.

## Análisis de errores

Se leyeron y clasificaron 23 errores del modelo elegido: los 8 de prueba y los 15 de validación ([`reports/error_analysis.csv`](reports/error_analysis.csv)). Las categorías más frecuentes son etiquetas dudosas de la fuente (7) y mensajes legítimos con vocabulario comercial (7).

## Uso de IA

Declaración completa, prompts, verificaciones y correcciones en [`docs/DECLARACION_IA.md`](docs/DECLARACION_IA.md).

## Entrega

PDF: [`reports/Ejercicio_03.pdf`](reports/Ejercicio_03.pdf).
