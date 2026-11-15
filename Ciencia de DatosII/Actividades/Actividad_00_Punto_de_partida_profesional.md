# Actividad 00 · Punto de partida profesional

**Asignatura:** INF-8239 Ciencia de Datos II · **Unidad:** 01 · Modelos avanzados, reducción dimensional y Green AI · **Código:** U01.ACT00
**Estudiante:** Marlenis Judith Concepción Cuevas · Maestría en Ciencia de Datos e Inteligencia Artificial, UASD
**Tipo:** consulta diagnóstica sin puntuación

## Pregunta

¿Cuál de estas experiencias describe mejor tu punto de partida para la Unidad 01?

| Opción | Enunciado |
|---|---|
| **1** | **He entrenado y evaluado varios modelos de clasificación.** |
| 2 | He usado modelos, pero necesito reforzar validación y métricas. |
| 3 | Conozco Python y análisis de datos, pero tengo poca experiencia con modelos avanzados. |
| 4 | Necesito acompañamiento desde la preparación del entorno y el pipeline. |

## Respuesta: Opción 1

> He entrenado y evaluado varios modelos de clasificación.

## Justificación

La elijo porque en la maestría ya construí, entrené y evalué modelos de clasificación de principio a fin, con datos reales, partición de datos, líneas base y métricas, y con código probado en un repositorio.

### Ciencia de Datos I (INF-8237)

| Trabajo | Qué hice |
|---|---|
| Práctica 02 · Sakila CRUD/ORM | Proyecto en Python con MySQL: programación orientada a objetos, operaciones CRUD, importación y exportación, y métricas descriptivas. |
| Práctica 03 · Caso OULAD con DBMS | Metodología OSEMN sobre OULAD (Open University): base de datos, análisis exploratorio, métricas y modelos supervisados. |
| Recuperación · Métricas inferenciales y ML | Contraste de métricas inferenciales y de aprendizaje automático. |
| Ensayo 02 · Revisión de literatura ML | Revisión académica sobre aprendizaje automático en APA 7. |
| Práctica 04 · Proyecto final OULAD | Proyecto integrador con datos, SQL, código en `src` y pruebas. |

### Ciencia de Datos II (INF-8239)

| Unidad | Trabajo | Evidencia de modelado y evaluación |
|---|---|---|
| I | Ejercicio 01 · SVM reproducible | SVM con validación cruzada estratificada frente a una línea base: F1 macro 0.938 frente a 0.391; 15 pruebas. |
| I | Ejercicio 02 · Ensambles y Green AI | SVM, PCA, Random Forest y Gradient Boosting comparados por desempeño y costo con una frontera de Pareto. |
| II | Ejercicio 03 · Clasificador de texto | TF-IDF con Naive Bayes y regresión logística; eliminación de duplicados para evitar fuga; análisis de 23 errores. |
| II | Ejercicio 04 · CNN y Model Card | Red densa frente a CNN en Fashion-MNIST; métricas por clase y costo computacional. |
| III | Ejercicio 05 · Recomendador | Popularidad, contenido, factorización e híbridos con métricas de ranking y usuarios nuevos. |
| III | Ejercicio 06 · VAE | Autoencoder y VAE: reconstrucción, diversidad y detección de memorización. |
| IV | Ejercicios 07 y 08 | Auditoría de equidad por grupo, evaluación de impacto, gobernanza, monitoreo y simulacro de incidente. |
| IV | Trabajo final | Sistema de apoyo a decisiones para priorizar tutorías: línea base de reglas frente a regresión logística, con auditoría de equidad. |

## Lo que ya domino

- Partición en entrenamiento, validación y prueba, estratificada y reproducible con semilla.
- Pipelines de scikit-learn para que el preprocesamiento no use datos de evaluación.
- Líneas base (clase mayoritaria o reglas) antes de cualquier modelo.
- Métricas más allá de la exactitud: F1 macro, recall por clase, ROC AUC y matriz de confusión.
- Pruebas automatizadas con pytest y trabajo reproducible con Git.

## Lo que quiero reforzar en esta asignatura

- Kernels del SVM y el efecto de C y gamma en el margen.
- Reducción dimensional (PCA y t-SNE) y cuándo ayuda realmente al modelo.
- Medir el costo computacional (Green AI) para decidir entre modelos con desempeño parecido.
- Estimar la incertidumbre de las métricas cuando la muestra de prueba es pequeña.

## Qué espero de la unidad

Pasar de «entrenar un modelo que funciona» a **defender una decisión**: por qué ese modelo, con qué evidencia, a qué costo y con qué límites.
