# System Card · Recomendador

## Usuarios y propósito
Sugerir 10 películas no vistas a usuarios de MovieLens, con fines académicos. La lista ordena alternativas; no decide qué debe ver una persona.

## Catálogo y candidatos
Películas con al menos una valoración en el historial disponible (entrenamiento, o entrenamiento + validación en la prueba final). Se excluyen las ya valoradas por el usuario. El 93.3 % de los ítems relevantes de prueba está en ese catálogo; el resto (películas nuevas) no se puede recomendar.

## Señales utilizadas
Valoraciones explícitas (0.5–5), su orden temporal y los géneros de cada película. Se considera relevante una valoración ≥ 4.0.

## Modelos y fallback
| Modelo | Idea |
|---|---|
| Popularidad | Media ponderada por cantidad de valoraciones (percentil 80 como mínimo) |
| Contenido | Perfil TF-IDF de géneros ponderado por el rating del usuario y similitud coseno |
| Factorización | SGD sobre la matriz usuario-película (proyecto base); búsqueda de factores y épocas en validación |
| Híbrido α | α · factorización + (1 − α) · contenido, ambos normalizados a [0, 1]; α ∈ {0.25, 0.5, 0.75} |

**Elegido:** híbrido α = 0.75 con factorización de 10 factores y 12 épocas (`reports/decision.json`).
**Fallback:** un usuario sin historial recibe la lista de popularidad; con 5 valoraciones iniciales se puede usar contenido, pero la popularidad sigue siendo mejor (ver abajo).

## Métricas offline
Particiones por usuario según el tiempo: 70 % más antiguo para entrenamiento, 10 % para validación y 20 % más reciente para prueba. Se reservan 61 usuarios fríos. Métricas: precision, recall, NDCG y acierto @10, cobertura del catálogo, novedad y RMSE. Resultados en `reports/resultados_test.csv`.

## Cold start, cobertura y diversidad
- Usuarios fríos: popularidad obtiene NDCG@10 0.227; contenido con 5 valoraciones, 0.080. Estos valores no se comparan con los de usuarios cálidos, porque la verdad incluye toda su historia.
- Cobertura: popularidad recomienda el 0.7 % del catálogo; el híbrido elegido, el 8.9 %; contenido, el 10.1 %.
- Usuarios poco activos (mediana de 21 valoraciones) reciben NDCG@10 0.020 frente a 0.108 de los más activos.

## Riesgos y monitoreo
Sobre-especialización en géneros, refuerzo de lo popular y peor servicio a usuarios con poca historia. Monitorear NDCG y cobertura por segmento de actividad, la proporción de recomendaciones del top 1 % de popularidad y las quejas de usuarios. Reentrenar periódicamente y no usar la lista para decisiones automáticas sobre personas.
