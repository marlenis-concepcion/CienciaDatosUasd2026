# Storyboard y guion del video colaborativo

Duración máxima: 5 minutos.

## 0:00-0:30 | Presentación

**Integrante 1**

“Somos el Mccarthy Team. Nuestro proyecto analiza OULAD y un Experimento X sintético para
predecir aprobación, resultado ordinal y promedio de evaluaciones. El objetivo es construir
una alerta académica reproducible, no tomar decisiones automáticas sobre estudiantes.”

Mostrar: portada del artículo y estructura del folder.

## 0:30-1:20 | Datos, hipótesis y OSEMN

**Integrante 2**

Explicar OULAD, las dos hipótesis y la ventana de 28 días. Mostrar las clases
`OULADRepository`, `FeatureEngineer`, `EDAReporter`, `ModelLab` y `OULADProject`.

Frase clave: “Filtramos las interacciones antes de agregarlas para reducir fuga temporal.”

## 1:20-2:10 | EDA, ordinales y missing

**Integrante 3**

Mostrar `eda_alto_nivel.png`, `auditoria_missing.csv` y `descriptiva_univariada.csv`.
Explicar histograma, box plot, scatter, curtosis y correlación. Mostrar los mapas ordinales de
educación, edad y resultado final, junto con imputación de mediana y moda.

## 2:10-3:25 | Modelos y métricas

**Integrante 4**

Explicar los tres algoritmos de clasificación y los tres de regresión. Mostrar
`metricas_generales.csv`, una matriz de confusión y `f1_manual.csv`.

Fórmula oral:

“Precisión es TP dividido entre TP más FP; recall es TP dividido entre TP más FN; F1 es dos
por precisión por recall dividido entre la suma de ambas.”

## 3:25-4:10 | Salidas e importancias

**Integrante 1 o 5**

Mostrar los CSV caso a caso con `y_test` y `y_pred`, luego
`importancias_variables.csv`. Aclarar que importancia predictiva no significa causalidad.

## 4:10-4:40 | Unit tests

**Integrante de QA**

Ejecutar:

```bash
python -m pytest -q
```

Explicar que las pruebas verifican TP, FP, TN, FN, F1 manual y la colección de resultados.

## 4:40-5:00 | Cierre

**Todo el equipo o coordinador**

Resumir el mejor modelo según F1/ROC-AUC y R², mencionar limitaciones y confirmar que el
Experimento X es sintético. Cerrar con la utilidad de intervención humana temprana.
