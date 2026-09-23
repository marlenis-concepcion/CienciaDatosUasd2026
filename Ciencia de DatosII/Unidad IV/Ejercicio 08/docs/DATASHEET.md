# Datasheet · territorial_risk_synthetic.csv

Estructura según Gebru et al. (2021), *Datasheets for Datasets*.

**Trazabilidad.** SHA-256: `2af1858fe874f3914b0f9bfe068fd876cb716186694a6ece9a16e8c929128a01` (verificado por `tests/test_e08.py` y registrado en `reports/lab13/manifest.json`).

## Motivación
Creado por el docente del curso (proyecto base `INF8239_U04_Gobernanza_DSS_Proyecto_Base_uv`) para practicar contratos de datos, evaluación temporal, auditoría por subgrupos y gobernanza. No representa personas, lugares ni estadísticas reales de la República Dominicana.

## Composición
640 casos (filas), 9 columnas; del 1 de enero al 27 de diciembre de 2026; sin nulos ni `case_id` repetidos. Tasa de casos positivos: 55.2 %. Grupos: G1 (396) y G2 (244). Diccionario, sensibilidad y finalidad de cada columna en `docs/data_inventory.csv`.

## Proceso de recolección
Generación sintética con semilla fija por el autor del proyecto base; el procedimiento exacto no está publicado en el repositorio.

## Preprocesamiento
Ninguno en origen. En este sistema: orden por `received_date`, partición temporal 75/25 y vistas minimizadas (operativa y de auditoría) según el inventario.

## Usos
Previsto: enseñanza de gobernanza y auditoría. Prohibido: perfilar personas, inferir sobre poblaciones reales o tomar decisiones operativas.

## Distribución
Incluido en el repositorio porque es sintético y forma parte del material del curso.

## Mantenimiento
Responsable de datos: Data Engineer (R) y Data Protection Officer (A) según `student_inputs/raci.csv`. Cualquier cambio de versión debe actualizar el hash en este documento, en la Model Card y en el manifiesto.
