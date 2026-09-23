# Ejercicio 05 · Motor recomendador reproducible

**Autora:** Marlenis Judith Concepción Cuevas · **Asignatura:** INF-8239-C2 · **Unidad:** III · **Docente:** Edwin Ramón José Nolasco

Integra LAB08 (recomendador por contenido) y LAB09 (factorización e hibridación) sobre el proyecto base `INF8239_U03_Recomendadores_Proyecto_Base`.

## Resultado principal (prueba, NDCG@10 y cobertura)

| Modelo | NDCG@10 validación | NDCG@10 prueba | Hit@10 | Cobertura | Novedad |
|---|---|---|---|---|---|
| Popularidad | 0.043 | 0.058 | 0.274 | 0.007 | 2.29 |
| Contenido (géneros) | 0.009 | 0.011 | 0.086 | 0.101 | 6.19 |
| Factorización (10 factores) | 0.050 | 0.062 | 0.308 | 0.066 | 2.69 |
| **Híbrido α = 0.75 (elegido)** | **0.053** | 0.059 | 0.291 | **0.089** | 3.03 |

Regla fijada en validación (`reports/decision.json`): frontera de Pareto sobre NDCG@10 y cobertura; entre los no dominados, el de mayor cobertura con al menos el 95 % del mejor NDCG. Usuarios nuevos: fallback de popularidad (NDCG@10 0.227 en 61 usuarios fríos). Detalle en [`docs/SYSTEM_CARD.md`](docs/SYSTEM_CARD.md).

## Estructura

- `notebooks/ejercicio_05.ipynb`: cuaderno ejecutado de principio a fin (descarga, auditoría, validación, prueba, usuarios fríos y errores).
- `src/inf8239_u03/`: `data.py` (descarga, validación, corte temporal, usuarios fríos), `recommenders.py` (popularidad, contenido, factorización, `Scorer`, Pareto), `metrics.py` (hit rate, cobertura, precision, recall, NDCG, novedad), `experiment.py`.
- `scripts/`: `download_data.py`, `audit_data.py`, `lab08_content.py`, `lab09_hybrid.py` (proyecto base), `run_experiment.py`, `make_report.py`.
- `tests/`: 13 pruebas.
- `docs/`: Dataset Card, System Card, pruebas y declaración de uso de IA.
- `reports/`: auditoría, búsqueda de la factorización, validación, Pareto, resultados de prueba, usuarios fríos, errores y `Ejercicio_05.pdf`.

## Instalación

```bash
uv python install 3.12
uv sync
```

Alternativa con pip (Python 3.12): `pip install -r requirements.txt` y luego `pip install -e . --no-deps`.

## Ejecución

```bash
uv run python scripts/download_data.py    # descarga MovieLens y verifica SHA-256
uv run python scripts/run_experiment.py   # auditoría, validación, decisión, prueba, fríos y errores (~1 min)
uv run python scripts/make_report.py      # reports/Ejercicio_05.pdf
uv run pytest -q
uv run jupyter nbconvert --to notebook --execute --inplace notebooks/ejercicio_05.ipynb
```

## Datos y términos de uso

MovieLens `ml-latest-small` (GroupLens, Universidad de Minnesota). Cita: Harper, F. M. y Konstan, J. A. (2015). *The MovieLens Datasets: History and Context*. ACM TiiS 5(4). https://doi.org/10.1145/2827872. Uso para investigación, no comercial, con cita y sin implicar respaldo de la universidad. **El dataset no se redistribuye**: `data/` está en `.gitignore` y `scripts/download_data.py` lo descarga y comprueba el SHA-256 `696d65a3…e436`.

## Particiones

- 61 usuarios (10 %, semilla 42) reservados como fríos: no entran al entrenamiento.
- Resto (549 usuarios), por usuario y en orden temporal: 70 % entrenamiento, 10 % validación, 20 % prueba.
- Relevante = rating ≥ 4. La prueba se evalúa una sola vez, después de reentrenar con entrenamiento + validación.

## Errores y límites

Los usuarios menos activos (mediana de 21 valoraciones) obtienen NDCG@10 0.020 y 124 de 139 no reciben ningún acierto; los más activos llegan a 0.108. En los ejemplos sin aciertos el usuario cambia de géneros entre el pasado y el periodo de prueba. Solo se usan géneros como contenido, la evaluación es offline y hay una sola semilla.

## Pruebas automatizadas

13 pruebas, todas aprobadas (`uv run pytest -q`, resultado en `reports/pruebas.txt`). Tabla completa con el criterio de la rúbrica en [`docs/PRUEBAS.md`](docs/PRUEBAS.md).

1. **`test_valid_contract`** (proyecto base). Un conjunto con las columnas y rangos esperados pasa la validación. *Por qué:* Asegura que la validación no bloquea datos correctos.
2. **`test_rejects_orphan_rating`** (proyecto base). Falla si hay una valoración de una película que no existe en movies.csv. *Por qué:* Una valoración huérfana no tiene géneros ni título y rompería el modelo de contenido.
3. **`test_content_excludes_query_and_returns_unique_items`** (proyecto base). El recomendador por contenido no devuelve la propia película consultada ni repite películas. *Por qué:* Recomendar lo que el usuario acaba de ver o repetir ítems infla la lista sin aportar nada.
4. **`test_popularity_contains_weighted_score`** (proyecto base). La popularidad calcula una puntuación ponderada por cantidad de valoraciones. *Por qué:* Evita que una película con una sola valoración de 5 estrellas encabece la lista.
5. **`test_temporal_split_keeps_last_event`** (proyecto base). En la partición del proyecto base la prueba contiene el evento más reciente de cada usuario. *Por qué:* Evaluar con el futuro y entrenar con el pasado evita usar información que no existiría en el momento de recomendar.
6. **`test_matrix_factorization_predicts_finite_value`** (proyecto base). La factorización entrena y predice un número finito. *Por qué:* Detecta divergencias del SGD (valores infinitos o NaN).
7. **`test_ranking_metrics`** (proyecto base). Hit rate y cobertura coinciden con un cálculo manual. *Por qué:* Las métricas de ranking son la base de la decisión.
8. **`test_temporal_split_keeps_past_in_train_and_future_in_test`** (nueva). Para cada usuario, todo el entrenamiento es anterior a la validación y esta anterior a la prueba; no se pierden ni se repiten valoraciones. *Por qué:* El corte 70/10/20 por usuario es la base de toda la evaluación; si mezclara pasado y futuro, las métricas serían optimistas.
9. **`test_cold_users_are_reproducible_and_disjoint_from_training`** (nueva). Los usuarios fríos son siempre los mismos con semilla 42 y ninguno aparece en el entrenamiento. *Por qué:* Si un usuario frío tuviera historial en entrenamiento no sería frío y la evaluación del fallback no valdría.
10. **`test_ranking_metrics_match_hand_calculation`** (nueva). Precision@k, recall@k, NDCG@k y acierto coinciden con un ejemplo calculado a mano. *Por qué:* NDCG premia que el acierto esté arriba en la lista; la prueba confirma la fórmula antes de usarla para decidir.
11. **`test_novelty_is_higher_for_less_popular_items`** (nueva). Recomendar una película poco valorada da más novedad que una muy popular. *Por qué:* La novedad se usa para mostrar el sesgo de popularidad; debe crecer en la dirección correcta.
12. **`test_recommendations_exclude_seen_items_and_cold_user_gets_popularity`** (nueva). Ningún método recomienda películas ya vistas, aunque se pidan más de las disponibles, y un usuario desconocido recibe la lista de popularidad. *Por qué:* Esta prueba encontró un error real: con pocas películas sin ver, la lista se rellenaba con películas ya vistas. Se corrigió el código.
13. **`test_pareto_front_and_decision_rule`** (nueva). La frontera de Pareto excluye un modelo dominado en NDCG y cobertura, y la regla elige el de mayor cobertura con NDCG ≥ 95 % del máximo. *Por qué:* La decisión final se toma con esta regla en validación antes de ver la prueba; la prueba evita cambiarla después.

## Uso de IA

Claude Code, Codex y DeepSeek. Detalle, prompts, verificaciones y correcciones en [`docs/DECLARACION_IA.md`](docs/DECLARACION_IA.md).

## Entrega

PDF: [`reports/Ejercicio_05.pdf`](reports/Ejercicio_05.pdf).
