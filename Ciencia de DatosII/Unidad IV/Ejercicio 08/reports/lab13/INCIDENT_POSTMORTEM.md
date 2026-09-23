# Postmortem · simulacro de incidente de datos

Simulacro ejecutado por `scripts/run_e08.py` sobre la línea temporal sintética. Valores calculados en `reports/lab13/simulacro.json`.

- **Escenario:** desde el 2026-12-01 la ingesta registra `exposure` multiplicada por 0.1 (cambio de unidad no comunicado).
- **Detección:** semana del 2026-11-30; `check_inputs` mide un desplazamiento de la media de exposure de -7.8 errores estándar (umbral ±4.0). Ninguna semana normal superó |z| = 2.0.
- **Clasificación:** severidad alta (deriva de una variable de decisión). Estado del runbook: **CONTENER**.
- **Contención:** el ML Engineer desactiva el orden sugerido y pasa a orden de llegada con revisión manual; autoriza el Institutional Owner (RACI: Respuesta a incidentes).
- **Evidencia preservada:** lote afectado, alertas (`monitoreo_entradas.csv`), hashes (`manifest.json`) y commit del código.
- **Impacto medido:** 46 casos en diciembre con 29 de alto riesgo. Si nadie lo detectara, el recall caería de 0.793 a 0.690 y se dejarían sin priorizar 3 casos de alto riesgo más; al detectarlo en la primera semana, la pérdida se limita a 1 caso(s), que se revisan de inmediato al volver a puntuar.
- **Comunicación:** interna el mismo día; el Product Owner informa a las comunidades de las zonas con casos reordenados y ofrece revisión prioritaria en 5 días hábiles.
- **Reversión:** volver a la versión anterior de la ingesta, volver a puntuar todos los casos desde el 2026-12-01 y revisar primero los casos de alto riesgo reordenados.
- **Causa raíz:** cambio de unidad en la fuente sin contrato de datos que fijara la escala.

## Acciones correctivas
| Acción | Responsable | Fecha límite |
|---|---|---|
| Añadir la escala y el rango esperado de `exposure` al contrato de datos | Data Engineer | 2026-12-15 |
| Prueba automática de deriva en cada carga (`check_inputs`) antes de puntuar | ML Engineer | 2026-12-15 |
| Protocolo de aviso de cambios de fuente entre proveedor de datos y Data Engineer | Product Owner | 2026-12-31 |
| Revisión del postmortem y cierre | Institutional Owner | 2027-01-08 |
