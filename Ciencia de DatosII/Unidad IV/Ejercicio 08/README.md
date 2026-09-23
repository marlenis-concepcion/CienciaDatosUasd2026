# Ejercicio 08 · Expediente de gobernanza y simulacro

**Autora:** Marlenis Judith Concepción Cuevas · **Asignatura:** INF-8239-C2 · **Unidad:** IV · **Docente:** Edwin Ramón José Nolasco

Integra LAB13 (gobernanza, roles y trazabilidad) sobre el sistema del [Ejercicio 07](../Ejercicio%2007/README.md): la regla transparente que ordena casos territoriales **sintéticos** para revisión humana.

## Decisión: LIMITAR (piloto)

El expediente de gobernanza está completo y el simulacro demostró que una falla de datos se detecta en la primera semana, se contiene y se revierte con responsables definidos. No se despliega de forma general hasta tener al menos 30 casos por celda interseccional.

| Evidencia | Resultado |
|---|---|
| Minimización | Vista operativa de 9 a 4 columnas; grupo, edad, zona y resultado solo en la vista de auditoría |
| Retención (simulación al 30-06-2027) | Operativa a 12 meses: 324 casos eliminados; auditoría a 24 meses: 0 |
| Trazabilidad | Datasheet, Model Card y manifiesto con SHA-256 verificados por pruebas |
| RACI | 10 actividades, un solo responsable A por actividad; traspasos con criterio de aceptación |
| Monitoreo normal | 14 semanas sin alertas (máximo |z| = 2.0, umbral 4) |
| Simulacro | Exposición × 0.1 desde el 1 de diciembre → detectado en la primera semana (z = −7.8) → CONTENER; sin detección se perderían 3 casos de alto riesgo, con detección 1 |

## Expediente

| Artefacto editable | Contenido |
|---|---|
| [`docs/data_inventory.csv`](docs/data_inventory.csv) | Columna, sensibilidad, vistas, finalidad, base legal si fueran datos reales, retención y minimización |
| [`configs/governance.yml`](configs/governance.yml) | Usos prohibidos, compuertas, plazos de retención y umbrales de monitoreo |
| [`docs/DATASHEET.md`](docs/DATASHEET.md) · [`docs/MODEL_CARD.md`](docs/MODEL_CARD.md) | Documentación trazable por hash |
| [`student_inputs/raci.csv`](student_inputs/raci.csv) · [`docs/TRASPASO.md`](docs/TRASPASO.md) | Responsabilidades y traspasos entre roles |
| [`docs/RUNBOOK.md`](docs/RUNBOOK.md) | Detección, contención, evidencia, comunicación, reversión y postmortem |
| [`docs/MARCO_NORMATIVO.md`](docs/MARCO_NORMATIVO.md) | Obligación legal, marco voluntario y recomendación ética |
| `reports/lab13/` | Minimización y retención, manifiesto, monitoreo, simulacro, gráfica y [`INCIDENT_POSTMORTEM.md`](reports/lab13/INCIDENT_POSTMORTEM.md) |

Los plazos de retención y los umbrales son decisiones propias (recomendación ética), no plazos fijados por la Ley 172-13.

## Instalación y ejecución

```bash
uv python install 3.12
uv sync
uv run python scripts/run_e07.py        # auditoría y decisión heredadas del Ejercicio 07
uv run python scripts/run_e08.py        # inventario, retención, RACI, monitoreo, simulacro y manifiesto
uv run python scripts/make_report.py    # reports/Ejercicio_08.pdf
uv run pytest -q
uv run jupyter nbconvert --to notebook --execute --inplace notebooks/ejercicio_08.ipynb
```

Alternativa con pip (Python 3.12): `pip install -r requirements.txt` y luego `pip install -e . --no-deps`.

## Pruebas automatizadas

34 pruebas, todas aprobadas (`uv run pytest -q`, resultado en `reports/pruebas.txt`). Tabla con el criterio de la rúbrica en [`docs/PRUEBAS.md`](docs/PRUEBAS.md).

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
11. **`test_student_impact_assessment_is_complete`** (ejercicio 07). La evaluación de impacto no tiene campos vacíos y declara que el sistema solo asiste la revisión. *Por qué:* La finalidad limitada es la base de la proporcionalidad y de los usos prohibidos.
12. **`test_risk_register_is_complete_and_linked_to_nist_rmf`** (ejercicio 07). Hay 8 riesgos o más, cada uno con una subcategoría válida del NIST AI RMF, cubriendo las cuatro funciones, ordenados por prioridad. *Por qué:* Demuestra que el registro está trazado al marco y no es una lista suelta.
13. **`test_stakeholders_include_affected_people_without_placeholders`** (ejercicio 07). El mapa de interesados incluye a las personas afectadas y está completo. *Por qué:* Las personas afectadas son las de menor poder y deben estar representadas.
14. **`test_normative_matrix_separates_legal_voluntary_and_ethical`** (ejercicio 07). La matriz normativa distingue obligación legal, marco voluntario y recomendación ética y cita la Ley 172-13 y el NIST AI 100-1. *Por qué:* Es un requisito explícito del mandato.
15. **`test_protected_attribute_is_not_a_model_or_rule_input`** (ejercicio 07). Invertir el grupo protegido de todos los casos no cambia ninguna decisión de la regla. *Por qué:* Prueba de forma directa que no hay tratamiento diferenciado por grupo.
16. **`test_bootstrap_interval_contains_the_observed_gap`** (ejercicio 07). El intervalo bootstrap de la brecha está ordenado y acotado entre 0 y 1. *Por qué:* La decisión de limitar depende de este intervalo.
17. **`test_small_intersectional_cells_are_flagged`** (ejercicio 07). Una celda con 8 casos se marca como insuficiente y una con 35 no. *Por qué:* Evita sacar conclusiones de subgrupos demasiado pequeños (riesgo R02).
18. **`test_choice_excludes_threshold_optimizer_that_uses_protected_group`** (ejercicio 07). La regla de elección descarta ThresholdOptimizer aunque tenga mejor recall. *Por qué:* Esa mitigación necesita el grupo protegido al decidir; se documenta pero no se elige.
19. **`test_final_decision_maps_evidence_to_four_options[desplegar]`** (ejercicio 07). Con compuertas cumplidas y poca incertidumbre la decisión es desplegar. *Por qué:* Las cuatro opciones del mandato deben salir de reglas explícitas.
20. **`test_final_decision_maps_evidence_to_four_options[limitar]`** (ejercicio 07). Si se cumplen las compuertas pero el intervalo supera la tolerancia, la decisión es limitar. *Por qué:* Es el caso de este ejercicio.
21. **`test_final_decision_maps_evidence_to_four_options[modificar]`** (ejercicio 07). Si la brecha supera la tolerancia con recall suficiente, la decisión es modificar. *Por qué:* Obliga a mitigar antes de usar.
22. **`test_final_decision_maps_evidence_to_four_options[no utilizar]`** (ejercicio 07). Si el recall no alcanza el mínimo, la decisión es no utilizar. *Por qué:* Un sistema que no encuentra los casos de riesgo no debe usarse.
23. **`test_temporal_split_keeps_future_cases_in_test`** (ejercicio 07). Todos los casos de prueba son posteriores a los de entrenamiento. *Por qué:* La auditoría simula el uso real: se entrena con el pasado y se evalúa con casos nuevos.
24. **`test_inventory_covers_every_column_with_purpose_and_retention`** (nueva). Cada columna del dataset aparece en el inventario con finalidad, sensibilidad y retención. *Por qué:* Sin inventario completo no se puede justificar por qué se guarda cada dato.
25. **`test_operational_view_excludes_sensitive_and_unneeded_columns`** (nueva). La vista operativa solo tiene case_id, fecha, incidentes y exposición; el grupo, la edad, la zona y el resultado quedan fuera. *Por qué:* Minimización: el analista solo ve lo que la regla necesita; los datos sensibles quedan en la vista de auditoría.
26. **`test_minimize_rejects_columns_missing_from_inventory`** (nueva). Una columna nueva que no está en el inventario hace fallar el proceso. *Por qué:* Impide que entren datos nuevos sin una decisión documentada.
27. **`test_retention_deletes_only_cases_older_than_the_limit`** (nueva). Con 12 meses de retención solo se elimina el caso más antiguo. *Por qué:* La política de retención debe aplicarse de forma exacta y verificable.
28. **`test_datasheet_and_model_card_hash_match_the_current_dataset`** (nueva). El SHA-256 escrito en la Datasheet y en la Model Card coincide con el archivo de datos actual. *Por qué:* Si cambian los datos sin actualizar la documentación, la prueba falla: la documentación queda atada a la versión real.
29. **`test_manifest_hashes_match_files_on_disk`** (nueva). Los hashes del manifiesto (datos, configuración, inventario, RACI, decisión, Datasheet, Model Card y runbook) coinciden con los archivos. *Por qué:* Garantiza que la evidencia entregada es la que se ejecutó.
30. **`test_raci_has_exactly_one_accountable_and_covers_critical_activities`** (nueva). Cada actividad tiene un solo responsable A y el RACI cubre minimización, retención, monitoreo, incidentes y apelaciones. *Por qué:* Con dos A nadie rinde cuentas; sin esas actividades, los controles no tienen dueño.
31. **`test_input_monitor_is_quiet_on_normal_weeks_and_detects_scale_bug`** (nueva). Ninguna semana normal de prueba genera alerta y un lote con exposure multiplicada por 0.1 activa CONTENER. *Por qué:* Un monitor que alerta siempre se ignora y uno que nunca alerta es inútil; la prueba verifica ambas cosas con los datos reales.
32. **`test_performance_monitor_does_not_alert_on_small_windows`** (nueva). Con 20 casos el monitor de desempeño solo informa y no activa el runbook. *Por qué:* Con pocos casos el recall es muy variable; alertar provocaría falsas alarmas.
33. **`test_psi_is_zero_for_same_distribution_and_grows_with_shift`** (nueva). El índice de estabilidad es 0 si la distribución no cambia y supera 1 con un cambio de escala. *Por qué:* Comprueba la medida de deriva que se reporta en el monitoreo.
34. **`test_runbook_and_postmortem_are_complete_with_owners_and_dates`** (nueva). El runbook tiene los 6 pasos sin REPLACE y el postmortem tiene al menos 3 acciones con fecha. *Por qué:* Un runbook incompleto no sirve en un incidente real; el postmortem debe cerrar con responsables y fechas.

## Uso de IA

Claude Code, Codex y DeepSeek. Los plazos, umbrales y responsabilidades los decide la autora. Detalle en [`docs/AI_USE_DECLARATION.md`](docs/AI_USE_DECLARATION.md).

## Entrega

PDF: [`reports/Ejercicio_08.pdf`](reports/Ejercicio_08.pdf).
