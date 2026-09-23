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

## Análisis de errores

Se leyeron y clasificaron 23 errores del modelo elegido: los 8 de prueba y los 15 de validación ([`reports/error_analysis.csv`](reports/error_analysis.csv)). Las categorías más frecuentes son etiquetas dudosas de la fuente (7) y mensajes legítimos con vocabulario comercial (7).

## Uso de IA

Declaración completa, prompts, verificaciones y correcciones en [`docs/DECLARACION_IA.md`](docs/DECLARACION_IA.md).

## Entrega

PDF: [`reports/Ejercicio_03.pdf`](reports/Ejercicio_03.pdf).
