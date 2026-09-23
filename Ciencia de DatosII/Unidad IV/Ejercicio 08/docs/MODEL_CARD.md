# Model Card · Territorial Review DSS

**Trazabilidad.** Datos: SHA-256 `2af1858fe874f3914b0f9bfe068fd876cb716186694a6ece9a16e8c929128a01` (ver `docs/DATASHEET.md`). Configuración, inventario, RACI y decisión: hashes en `reports/lab13/manifest.json`. Evidencia de la decisión: `reports/lab12/decision.json` (Ejercicio 07).

## Intended use
Ordenar casos territoriales sintéticos para revisión humana. **Sistema desplegado: regla transparente** `previous_incidents >= 4 or exposure >= 0.6`. La regresión logística y el árbol se evaluaron y **no se utilizan**.

## Out-of-scope use
Intervención automática, decisión de elegibilidad, declaratoria de emergencia, perfilado de personas, uso del grupo protegido o de la edad para decidir, uso con datos reales sin nueva evaluación.

## Data and split
640 casos sintéticos ordenados por fecha; 480 de entrenamiento (los últimos 120 como validación) y 160 de prueba posteriores. Vista operativa minimizada: `case_id`, `received_date`, `previous_incidents`, `exposure`.

## Global and subgroup evaluation
| Métrica (prueba, 160 casos) | Regla | Regresión logística (no usada) |
|---|---|---|
| Recall | 0.750 | 0.717 |
| FPR | 0.368 | 0.279 |
| Brecha de recall G1–G2 | 0.011 (IC 95 %: 0.004–0.208) | 0.138 (IC 95 %: 0.011–0.314) |
| Brecha de FPR G1–G2 | 0.010 (IC 95 %: 0.004–0.331) | 0.125 |

7 de 8 celdas interseccionales (grupo × edad) tienen menos de 30 casos y no se usan para decidir.

## Green AI evidence
La regla no se entrena ni necesita modelo guardado; se evalúa en microsegundos por caso. La regresión logística ocupa unos 3.6 KB y entrena en centésimas de segundo; aun así se descarta porque no mejora el recall y aumenta la brecha.

## Limitations, human oversight and appeal
Datos sintéticos y muestra de prueba pequeña; FPR alto (más casos a revisión). La lista solo ordena; decide una persona. Apelación: revisión manual por un analista distinto en 5 días hábiles. Monitoreo y respuesta a incidentes en `docs/RUNBOOK.md`; simulacro en `reports/lab13/INCIDENT_POSTMORTEM.md`.

## Owner and review date
Responsable: Product Owner (R) e Institutional Owner (A). Revisión: mensual durante el piloto; reevaluación completa cuando cada celda interseccional tenga al menos 30 casos.
