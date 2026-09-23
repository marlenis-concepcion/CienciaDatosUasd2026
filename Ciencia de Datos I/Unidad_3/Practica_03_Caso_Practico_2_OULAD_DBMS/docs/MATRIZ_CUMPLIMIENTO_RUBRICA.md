# Matriz de cumplimiento de la rúbrica

| Componente | Evidencia principal | Estado |
| --- | --- | --- |
| EDA univariado y multivariado extendido | `src/eda.py`, `descriptiva_univariada.csv`, `eda_alto_nivel.png` | Cumple |
| Manejo de ordinales y missing | `src/features.py`, `auditoria_missing.csv`, pipelines con imputación | Cumple |
| Encapsulación funcional o POO | `OULADProject`, `OULADRepository`, `FeatureEngineer`, `EDAReporter`, `ModelLab` | Cumple |
| TAD/collection | `ResultRegistry` basado en `UserDict` | Cumple |
| RDBMS/schema | No se utiliza RDBMS; los datos se procesan desde CSV/ZIP | No aplica |
| Algoritmos y modelado | Tres algoritmos por cada tipo de objetivo | Cumple |
| Interpretación y métricas | `hallazgos.txt`, `metricas_generales.csv`, `f1_manual.csv` | Cumple |
| CSV caso a caso | `predicciones_binarias.csv`, `predicciones_ordinales.csv`, `predicciones_regresion.csv` | Cumple |
| Gráficos | EDA, scatter, box plot, correlación y matrices de confusión | Cumple |
| Importancias | `importancias_variables.csv`, calculadas por permutación | Cumple |
| Unit tests | 24 escenarios en `tests/` y catálogo en `docs/ESCENARIOS_DE_PRUEBA.md` | Cumple |
| Video colaborativo opcional | `docs/GUION_VIDEO_COLABORATIVO.md` | Preparado |

## Evidencia de niveles

Para aspirar a **Excelente**, el equipo debe ejecutar OULAD completo, conservar todas las
salidas, revisar que no haya errores y explicar decisiones y limitaciones durante la
presentación. Un archivo creado pero no ejecutado puede ser evaluado como cumplimiento
parcial.
