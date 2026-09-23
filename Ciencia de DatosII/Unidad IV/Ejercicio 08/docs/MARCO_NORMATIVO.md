# Marco normativo · obligación legal, marco voluntario y recomendación ética

Análisis académico; no sustituye asesoría jurídica. Los datos del proyecto son sintéticos y no contienen personas reales, así que las obligaciones legales se aplicarían si el sistema se usara con datos reales en República Dominicana.

| Tipo | Fuente | Qué exige o recomienda | Cómo se aplica aquí | Evidencia |
|---|---|---|---|---|
| **Obligación legal** | Ley No. 172-13 sobre protección de datos personales (13 de diciembre de 2013; Gaceta Oficial No. 10737) | Protección integral de los datos personales en archivos, registros y bancos de datos, públicos o privados | Con datos reales: base legal para el tratamiento, finalidad declarada y datos mínimos. El esquema rechaza identificadores directos | `configs/governance.yml`, `tests/test_privacy.py` |
| **Obligación legal** | Constitución de la República Dominicana, art. 44 (intimidad y honor) | Respeto y no injerencia en la vida privada | No se usan ni guardan identificadores; el sistema no perfila personas | `src/inf8239_u04/data.py` |
| **Obligación legal** | Constitución, art. 70 (hábeas data) | Derecho a conocer, rectificar y exigir la supresión de datos propios, incluso en caso de discriminación | Mecanismo de apelación y revisión manual documentado | `student_inputs/lab11_impact.yml` |
| **Obligación legal** | Constitución, art. 39 (igualdad) | Igualdad y no discriminación | El grupo protegido no se usa para decidir; se audita la brecha por grupo | `reports/lab12/` |
| **Marco voluntario** | NIST AI Risk Management Framework 1.0 (NIST AI 100-1, 2023) | Funciones GOVERN, MAP, MEASURE y MANAGE | Cada riesgo del registro se vincula a una subcategoría (GOVERN 1.1, MAP 1.1, MAP 2.3, MAP 3.4, MEASURE 2.8, 2.10, 2.11 y MANAGE 4.1) | `student_inputs/risk_register.csv` |
| **Marco voluntario** | Mitchell et al. (2019), *Model Cards*; Gebru et al. (2021), *Datasheets for Datasets* | Documentar uso previsto, datos, métricas por grupo y límites | Dataset Card y Model Card (se completan en el Ejercicio 08) | `docs/` |
| **Recomendación ética** | Decisión propia del análisis | Preferir la alternativa menos intrusiva y explicable cuando rinde igual | Se elige la regla transparente en lugar del modelo | `reports/lab12/decision.json` |
| **Recomendación ética** | Decisión propia del análisis | No decidir sobre subgrupos con menos de 30 casos | Se marcan las celdas pequeñas y se limita el uso a un piloto | `reports/lab12/interseccional.csv` |
| **Recomendación ética** | Decisión propia del análisis | Supervisión humana significativa y derecho a apelar | La lista solo ordena revisiones; decide una persona | `app.py`, `lab11_impact.yml` |

## Proporcionalidad

- **Necesidad:** el volumen de casos obliga a ordenar la revisión; la lista de espera sin criterio (orden de llegada) no distingue riesgo.
- **Idoneidad:** la regla transparente alcanza recall 0.75 en prueba con brechas entre grupos de 0.01.
- **Menor intrusión:** la regla usa solo dos variables operativas (incidentes previos y exposición), sin edad, zona ni grupo protegido; es más simple que el modelo y rinde igual o mejor.
- **Equilibrio:** a cambio, envía más casos a revisión (FPR 0.37 frente a 0.28 de la regresión logística); se acepta porque el daño prioritario es el falso negativo, y la carga se vigila (riesgo R06).

## Referencias

- Ley No. 172-13. https://www.one.gob.do/media/u5ohmfyp/ley-172-13.pdf
- Constitución de la República Dominicana (2015). https://presidencia.gob.do/sites/default/files/statics/transparencia/base-legal/Constitucion-de-la-Republica-Dominicana-2015-actualizada.pdf
- NIST (2023). *Artificial Intelligence Risk Management Framework (AI RMF 1.0)*, NIST AI 100-1. https://doi.org/10.6028/NIST.AI.100-1
- Bird, S. et al. (2020). *Fairlearn: A toolkit for assessing and improving fairness in AI*. Microsoft, MSR-TR-2020-32.
- Hardt, M., Price, E. y Srebro, N. (2016). Equality of Opportunity in Supervised Learning. *NeurIPS*.
- Mitchell, M. et al. (2019). Model Cards for Model Reporting. *FAT\* '19*. https://doi.org/10.1145/3287560.3287596
- Gebru, T. et al. (2021). Datasheets for Datasets. *Communications of the ACM*, 64(12). https://doi.org/10.1145/3458723
