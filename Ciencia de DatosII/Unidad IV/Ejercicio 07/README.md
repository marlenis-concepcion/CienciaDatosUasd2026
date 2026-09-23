# Ejercicio 07 · Evaluación de impacto y auditoría de equidad

**Autora:** Marlenis Judith Concepción Cuevas · **Asignatura:** INF-8239-C2 · **Unidad:** IV · **Docente:** Edwin Ramón José Nolasco

Integra LAB11 (evaluación de impacto ético) y LAB12 (auditoría de equidad con Fairlearn) sobre el proyecto base `INF8239_U04_Gobernanza_DSS_Proyecto_Base_uv`. El sistema auditado ordena casos territoriales **sintéticos** para revisión humana; no decide intervenciones.

## Decisión: LIMITAR

| Candidato | Recall validación | Recall prueba | FPR prueba | Brecha de recall | Brecha de FPR | ¿Usa el grupo protegido al decidir? |
|---|---|---|---|---|---|---|
| **Regla transparente (elegida)** | **0.828** | **0.750** | 0.368 | **0.011** | **0.010** | No |
| Regresión logística 0.50 | 0.812 | 0.717 | 0.279 | 0.138 | 0.125 | No |
| Árbol 0.50 | 0.781 | 0.717 | 0.309 | 0.181 | 0.168 | No |
| Logística con umbral 0.56 | 0.812 | 0.696 | 0.191 | 0.135 | 0.077 | No |
| ThresholdOptimizer (equalized odds) | 0.750 | 0.804 | 0.441 | 0.069 | 0.168 | **Sí (descartado)** |

La regla transparente (4 o más incidentes previos o exposición ≥ 0.6) cumple las compuertas del proyecto base, pero el intervalo bootstrap del 95 % de la brecha de recall llega a 0.208 (tolerancia 0.16) y 7 de 8 celdas interseccionales tienen menos de 30 casos. Se usa solo para **ordenar revisiones humanas en un piloto**, con apelación y monitoreo; **no se utiliza el modelo de aprendizaje automático**. Registro: [`reports/lab11/DECISION_RECORD.md`](reports/lab11/DECISION_RECORD.md).

## Expediente

| Artefacto editable | Contenido |
|---|---|
| [`student_inputs/lab11_impact.yml`](student_inputs/lab11_impact.yml) | Finalidad, decisión asistida, usuarios, población afectada, responsable, alternativa no predictiva, usos prohibidos, retiro y apelación |
| [`student_inputs/stakeholders.csv`](student_inputs/stakeholders.csv) | Interesados con beneficio, daño, poder y participación |
| [`student_inputs/risk_register.csv`](student_inputs/risk_register.csv) | 8 riesgos con probabilidad, impacto, control, responsable, evidencia y subcategoría del NIST AI RMF |
| [`student_inputs/lab12_decision.yml`](student_inputs/lab12_decision.yml) | Daño prioritario, métrica, tolerancia, evidencia, limitación y recomendación |
| [`docs/MARCO_NORMATIVO.md`](docs/MARCO_NORMATIVO.md) | Obligación legal (Ley 172-13; Constitución, arts. 39, 44 y 70), marco voluntario (NIST AI RMF, Model Cards, Datasheets), recomendación ética y proporcionalidad |
| `reports/lab11/` | Registro de riesgos priorizado, resumen RMF y registro de decisión |
| `reports/lab12/` | Candidatos, métricas por grupo, por edad e interseccionales, intervalos bootstrap, gráfica y decisión |

## Instalación y ejecución

```bash
uv python install 3.12
uv sync
uv run python scripts/run_e07.py        # LAB11 + LAB12: riesgos, auditoría, mitigaciones y decisión
uv run python scripts/make_report.py    # reports/Ejercicio_07.pdf
uv run pytest -q
uv run jupyter nbconvert --to notebook --execute --inplace notebooks/ejercicio_07.ipynb
uv run streamlit run app.py             # aplicación del proyecto base
```

Alternativa con pip (Python 3.12): `pip install -r requirements.txt` y luego `pip install -e . --no-deps`.

## Datos

`data/territorial_risk_synthetic.csv` (proyecto base): 640 casos sintéticos, sin personas reales. Partición temporal: 480 de entrenamiento (los últimos 120 como validación) y 160 de prueba posteriores. `protected_group` no entra al modelo ni a la regla; se usa solo para auditar.

## Pruebas automatizadas

23 pruebas, todas aprobadas (`uv run pytest -q`, resultado en `reports/pruebas.txt`). Tabla con el criterio de la rúbrica en [`docs/PRUEBAS.md`](docs/PRUEBAS.md).

1. **`test_dataset_contract`** (proyecto base). El conjunto tiene al menos 500 casos y case_id es único. *Por qué:* Sin identificadores únicos no se puede trazar un caso ni atender una apelación.
2. **`test_direct_identifier_rejected`** (proyecto base). El esquema rechaza una columna email. *Por qué:* Minimización: los identificadores directos no hacen falta para ordenar revisiones.
3. **`test_prohibited_name_rejected`** (proyecto base). El esquema rechaza una columna name. *Por qué:* Refuerza la protección de datos exigida si se usaran datos reales (Ley 172-13).
4. **`test_complete_risk_is_scored`** (proyecto base). La prioridad de un riesgo es probabilidad × impacto. *Por qué:* El orden del registro decide qué controles se atienden primero.
5. **`test_placeholder_is_rejected`** (proyecto base). Un riesgo con texto REPLACE no se acepta. *Por qué:* Evita entregar un registro con campos sin completar.
6. **`test_fairness_metrics_are_bounded`** (proyecto base). La brecha de recall está entre 0 y 1 y existen los grupos G1 y G2. *Por qué:* Comprueba que la auditoría por grupo funciona sobre el modelo real.
7. **`test_predictions_are_binary`** (proyecto base). El modelo solo predice 0 o 1. *Por qué:* Las métricas de equidad asumen predicciones binarias.
8. **`test_failed_gate_requires_review`** (proyecto base). Si falla una compuerta el estado pasa a REVIEW. *Por qué:* Ningún sistema pasa a GO con una compuerta incumplida.
9. **`test_raci_requires_accountable`** (proyecto base). Una actividad sin responsable A se rechaza. *Por qué:* Toda decisión necesita una persona que rinda cuentas.
10. **`test_app_starts_and_discloses_synthetic_case`** (proyecto base). La aplicación arranca y advierte que los datos son sintéticos. *Por qué:* Transparencia con quien la usa: no representa estadísticas reales.
11. **`test_student_impact_assessment_is_complete`** (nueva). La evaluación de impacto no tiene campos vacíos y declara que el sistema solo asiste la revisión. *Por qué:* La finalidad limitada es la base de la proporcionalidad y de los usos prohibidos.
12. **`test_risk_register_is_complete_and_linked_to_nist_rmf`** (nueva). Hay 8 riesgos o más, cada uno con una subcategoría válida del NIST AI RMF, cubriendo las cuatro funciones, ordenados por prioridad. *Por qué:* Demuestra que el registro está trazado al marco y no es una lista suelta.
13. **`test_stakeholders_include_affected_people_without_placeholders`** (nueva). El mapa de interesados incluye a las personas afectadas y está completo. *Por qué:* Las personas afectadas son las de menor poder y deben estar representadas.
14. **`test_normative_matrix_separates_legal_voluntary_and_ethical`** (nueva). La matriz normativa distingue obligación legal, marco voluntario y recomendación ética y cita la Ley 172-13 y el NIST AI 100-1. *Por qué:* Es un requisito explícito del mandato.
15. **`test_protected_attribute_is_not_a_model_or_rule_input`** (nueva). Invertir el grupo protegido de todos los casos no cambia ninguna decisión de la regla. *Por qué:* Prueba de forma directa que no hay tratamiento diferenciado por grupo.
16. **`test_bootstrap_interval_contains_the_observed_gap`** (nueva). El intervalo bootstrap de la brecha está ordenado y acotado entre 0 y 1. *Por qué:* La decisión de limitar depende de este intervalo.
17. **`test_small_intersectional_cells_are_flagged`** (nueva). Una celda con 8 casos se marca como insuficiente y una con 35 no. *Por qué:* Evita sacar conclusiones de subgrupos demasiado pequeños (riesgo R02).
18. **`test_choice_excludes_threshold_optimizer_that_uses_protected_group`** (nueva). La regla de elección descarta ThresholdOptimizer aunque tenga mejor recall. *Por qué:* Esa mitigación necesita el grupo protegido al decidir; se documenta pero no se elige.
19. **`test_final_decision_maps_evidence_to_four_options[desplegar]`** (nueva). Con compuertas cumplidas y poca incertidumbre la decisión es desplegar. *Por qué:* Las cuatro opciones del mandato deben salir de reglas explícitas.
20. **`test_final_decision_maps_evidence_to_four_options[limitar]`** (nueva). Si se cumplen las compuertas pero el intervalo supera la tolerancia, la decisión es limitar. *Por qué:* Es el caso de este ejercicio.
21. **`test_final_decision_maps_evidence_to_four_options[modificar]`** (nueva). Si la brecha supera la tolerancia con recall suficiente, la decisión es modificar. *Por qué:* Obliga a mitigar antes de usar.
22. **`test_final_decision_maps_evidence_to_four_options[no utilizar]`** (nueva). Si el recall no alcanza el mínimo, la decisión es no utilizar. *Por qué:* Un sistema que no encuentra los casos de riesgo no debe usarse.
23. **`test_temporal_split_keeps_future_cases_in_test`** (nueva). Todos los casos de prueba son posteriores a los de entrenamiento. *Por qué:* La auditoría simula el uso real: se entrena con el pasado y se evalúa con casos nuevos.

## Uso de IA

Claude Code, Codex y DeepSeek. Los valores del análisis los decide la autora. Detalle en [`docs/AI_USE_DECLARATION.md`](docs/AI_USE_DECLARATION.md).

## Entrega

PDF: [`reports/Ejercicio_07.pdf`](reports/Ejercicio_07.pdf).
