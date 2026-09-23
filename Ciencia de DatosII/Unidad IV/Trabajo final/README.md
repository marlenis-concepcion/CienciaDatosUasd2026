# Trabajo final · DSS de alerta temprana para tutoría universitaria

**Autora:** Marlenis Judith Concepción Cuevas · **Asignatura:** INF-8239-C2 Ciencia de Datos II · **Docente:** Edwin Ramón José Nolasco
**Modalidad:** B · Sistema de soporte a decisiones · **Equipo:** individual · **Versión final:** etiqueta `trabajo-final-v1.0`

Al terminar el primer semestre, la coordinación de tutorías tiene cupos para el 15 % de la cohorte. El DSS propone **a quién contactar primero**, **qué apoyo ofrecer** y **por qué**; la coordinación decide y deja registro. No se usa para sancionar, excluir ni condicionar becas.

## Resultado

| Alternativa (prueba, 100 cupos) | Recall a capacidad | Precisión | Brecha por edad | Brecha por género |
|---|---|---|---|---|
| Aleatorio | 0.141 | 0.30 | — | — |
| Baseline de reglas | 0.390 | 0.83 | 0.246 | 0.021 |
| Regresión logística | 0.455 | 0.97 | 0.261 | 0.133 |
| **Logística con cupos por edad (elegida en validación)** | **0.408** | **0.87** | **0.087** | **0.036** |

Recall máximo posible con 100 cupos: 0.469. **Decisión: LIMITAR**: piloto con revisión humana; el límite superior del IC 95 % de la brecha por edad (0.194) supera la tolerancia de 0.15. Informe completo: [`reports/Informe_Trabajo_Final.pdf`](reports/Informe_Trabajo_Final.pdf).

## Alcance cumplido (equipo individual)

| Requisito del mandato | Dónde |
|---|---|
| Baseline + 1 modelo candidato | `src/tutoria_dss/baseline.py`, `src/tutoria_dss/models.py` |
| 6 pruebas como mínimo | **35 pruebas** en `tests/` |
| DSS: reglas explícitas, alternativas, priorización y explicación | `src/tutoria_dss/dss.py` |
| Aplicación práctica | `app/streamlit_app.py` |
| Datos o mecanismo para obtenerlos | `scripts/download_data.py` (SHA-256) · [`docs/DATASET_CARD.md`](docs/DATASET_CARD.md) |
| Informe técnico y README | `reports/Informe_Trabajo_Final.pdf` · este archivo |
| Model Card y declaración de IA | [`docs/MODEL_CARD.md`](docs/MODEL_CARD.md) · [`docs/AI_USE_DECLARATION.md`](docs/AI_USE_DECLARATION.md) |
| Auditoría responsable y Green AI | `src/tutoria_dss/fairness.py`, `reports/equidad.csv`, `reports/decision_final.json` |
| Evidencia Git | Issues #1–#6, pull requests #7–#12 con revisión, etiqueta `trabajo-final-v1.0` |
| Demostración y defensa | [`docs/DEMO.md`](docs/DEMO.md) |

## Ejecución

```bash
uv python install 3.12
uv sync
uv run python scripts/download_data.py      # UCI 697, verifica SHA-256
uv run python scripts/audit_data.py         # reports/auditoria.json
uv run python scripts/train.py              # baseline vs logística, decisión en validación, prueba y errores
uv run python scripts/audit_fairness.py     # mitigación elegida en validación, equidad, Green AI, decisión
uv run python scripts/make_report.py        # reports/Informe_Trabajo_Final.pdf
uv run pytest -q
uv run streamlit run app/streamlit_app.py   # demostración para la coordinación
```

Alternativa con pip (Python 3.12): `pip install -r requirements.txt` y `pip install -e . --no-deps`. Cuaderno ejecutado: [`notebooks/trabajo_final.ipynb`](notebooks/trabajo_final.ipynb).

## Datos

UCI 697 *Predict Students' Dropout and Academic Success* (Realinho et al., 2021; CC BY 4.0; DOI 10.24432/C5MC89): 4424 estudiantes de Portugal. No se redistribuye. Punto de decisión: fin del primer semestre; las variables del segundo semestre y las sensibles (género, edad, nacionalidad, estado civil, internacional, beca) no entran al modelo. Los códigos de carrera y de modo de ingreso son los de la ficha de UCI.

## Estructura

- `src/tutoria_dss/`: `data.py` (contrato, variables permitidas, partición), `baseline.py`, `models.py`, `evaluation.py` (métricas a capacidad), `dss.py` (priorización, apoyo, explicación, registro humano), `fairness.py` (auditoría, cupos por grupo, compuertas).
- `scripts/`, `app/`, `tests/`, `notebooks/`, `configs/dss.yml`, `docs/`, `reports/`.

## Pruebas automatizadas

35 pruebas, todas aprobadas (resultado en `reports/pruebas.txt`).

1. **`test_dataset_contract_and_binary_target`** (Datos). Hay 4424 estudiantes, cada uno con identificador único y objetivo binario. *Por qué:* Contrato mínimo antes de cualquier análisis.
2. **`test_contract_rejects_nulls_and_impossible_approvals`** (Datos). El contrato rechaza nulos y más unidades aprobadas que inscritas. *Por qué:* Un dato imposible en origen produciría prioridades absurdas.
3. **`test_model_features_exclude_sensitive_and_second_semester`** (Datos). El modelo no usa variables sensibles ni del 2.º semestre. *Por qué:* Evita la discriminación directa y la fuga de información del futuro.
4. **`test_split_is_disjoint_complete_and_stratified`** (Datos). Entrenamiento, validación y prueba no se solapan, cubren todo y mantienen la tasa de abandono. *Por qué:* Base de una evaluación honesta.
5. **`test_rule_baseline_prioritizes_failed_units_and_unpaid_tuition`** (Baseline). La regla da más prioridad a quien no aprobó unidades o no pagó la matrícula. *Por qué:* El baseline debe reflejar el criterio que usaría una persona sin modelo.
6. **`test_model_outputs_valid_probabilities`** (Modelo). El modelo devuelve una probabilidad entre 0 y 1 por estudiante. *Por qué:* La lista se ordena por esa probabilidad.
7. **`test_scaler_is_fitted_only_on_training_data`** (Modelo). La estandarización aprende solo con entrenamiento. *Por qué:* Evita fuga de validación o prueba al modelo.
8. **`test_model_ignores_sensitive_columns_even_if_they_change`** (Equidad). Cambiar género o edad no cambia el riesgo estimado. *Por qué:* Prueba directa de que el modelo no usa atributos sensibles.
9. **`test_contributions_add_up_to_the_logit`** (Explicación). Las contribuciones por variable reconstruyen exactamente la probabilidad. *Por qué:* La explicación que ve la coordinación es fiel al modelo.
10. **`test_top_k_selects_exactly_capacity_and_highest_scores`** (Priorización). La selección toma exactamente los cupos y a los de mayor riesgo. *Por qué:* El DSS no puede ofrecer más tutorías de las disponibles.
11. **`test_capacity_metrics_match_hand_calculation`** (Evaluación). Recall y precisión a capacidad coinciden con un cálculo manual. *Por qué:* Son las métricas de éxito del proyecto.
12. **`test_choice_ignores_random_reference_and_uses_recall_then_ap`** (Evaluación). La regla de elección ignora el azar y usa recall y luego average precision. *Por qué:* La decisión se toma con una regla escrita antes de la prueba.
13. **`test_support_rules_are_explicit_and_ordered[deuda]`** (Reglas DSS). Con deuda se sugiere orientación financiera. *Por qué:* Lo financiero bloquea la continuidad y va primero.
14. **`test_support_rules_are_explicit_and_ordered[matrícula y 0 aprobadas]`** (Reglas DSS). Matrícula atrasada tiene prioridad sobre las unidades no aprobadas. *Por qué:* Comprueba el orden de las reglas.
15. **`test_support_rules_are_explicit_and_ordered[0 aprobadas]`** (Reglas DSS). Sin unidades aprobadas se sugiere tutoría académica intensiva. *Por qué:* Apoyo acorde con la causa probable.
16. **`test_support_rules_are_explicit_and_ordered[resto]`** (Reglas DSS). En los demás casos se sugiere seguimiento del tutor. *Por qué:* Toda persona priorizada recibe una propuesta.
17. **`test_priority_list_respects_capacity_and_is_sorted`** (Priorización). La lista tiene tantos estudiantes como cupos y está ordenada. *Por qué:* La coordinación ve primero a quien más lo necesita.
18. **`test_priority_list_contains_the_highest_risk_students`** (Priorización). Nadie fuera de la lista tiene más riesgo que el último de la lista. *Por qué:* Detectó un error real de redondeo que se corrigió.
19. **`test_every_prioritized_student_gets_support_and_explanation`** (Explicación). Cada estudiante de la lista tiene apoyo sugerido y explicación. *Por qué:* Una recomendación sin razón no es un DSS.
20. **`test_explanations_never_mention_sensitive_attributes`** (Equidad). Las explicaciones no mencionan género, edad, nacionalidad ni beca. *Por qué:* Evita estigmatizar y confirma que no hay variables sensibles en el modelo.
21. **`test_explanation_lists_only_risk_increasing_factors`** (Explicación). La explicación muestra solo factores que suben el riesgo y con su valor. *Por qué:* La coordinación puede verificar cada razón.
22. **`test_human_decision_log_requires_reason_and_owner`** (Supervisión humana). Rechazar o modificar exige motivo y toda decisión exige responsable. *Por qué:* La decisión final es humana y queda trazada.
23. **`test_streamlit_app_starts_and_warns_about_human_decision`** (Interfaz). La aplicación arranca y advierte que la coordinación decide. *Por qué:* El artefacto práctico funciona y es transparente.
24. **`test_age_bands_cover_all_ages_without_gaps`** (Equidad). Las franjas de edad cubren todas las edades sin huecos. *Por qué:* Nadie queda fuera de la auditoría.
25. **`test_audit_groups_are_readable_and_complete`** (Equidad). Los grupos de auditoría son legibles y no tienen vacíos. *Por qué:* Tablas de equidad comprensibles.
26. **`test_group_recall_matches_hand_calculation`** (Equidad). El recall por grupo y la brecha coinciden con un cálculo manual. *Por qué:* Base de la decisión de equidad.
27. **`test_small_groups_do_not_count_in_the_gap`** (Equidad). Los grupos con menos de 30 abandonos no cuentan en la brecha. *Por qué:* Evita conclusiones con muestras pequeñas.
28. **`test_quota_allocation_uses_exact_capacity_and_top_risk_within_group`** (Mitigación). El reparto por cupos usa exactamente la capacidad y elige a los de mayor riesgo en cada grupo. *Por qué:* La mitigación no regala ni pierde cupos.
29. **`test_quota_gives_places_to_low_risk_groups_that_global_ranking_ignores`** (Mitigación). Un grupo con menor riesgo promedio recibe cupos. *Por qué:* Es el propósito de la mitigación por edad.
30. **`test_prioritized_list_with_quota_keeps_capacity`** (Mitigación). La lista con cupos por edad mantiene la capacidad. *Por qué:* La mitigación se integra en el DSS real.
31. **`test_mitigation_choice_prefers_best_recall_among_those_that_pass_gates`** (Decisión). Se elige la alternativa con mejor recall entre las que cumplen las compuertas. *Por qué:* La mitigación se elige con una regla y en validación.
32. **`test_gate_decision_maps_to_four_options[desplegar]`** (Decisión). Compuertas cumplidas con poca incertidumbre dan desplegar. *Por qué:* Las cuatro opciones salen de reglas explícitas.
33. **`test_gate_decision_maps_to_four_options[limitar]`** (Decisión). Compuertas cumplidas con intervalo amplio dan limitar. *Por qué:* Es la decisión de este proyecto.
34. **`test_gate_decision_maps_to_four_options[modificar]`** (Decisión). Brecha observada fuera de tolerancia da modificar. *Por qué:* Obliga a mitigar antes de usar.
35. **`test_gate_decision_maps_to_four_options[no utilizar]`** (Decisión). Recall por debajo del mínimo da no utilizar. *Por qué:* Un sistema que no alcanza a quien abandona no sirve.
