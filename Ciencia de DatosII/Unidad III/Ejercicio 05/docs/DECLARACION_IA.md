# Declaración de uso de IA · Ejercicio 05

## Herramientas
- Claude Code (modelo Claude Opus 5.5, de Anthropic), en VS Code sobre este repositorio.
- Codex (OpenAI), como apoyo complementario durante el desarrollo.
- DeepSeek, como apoyo complementario durante el desarrollo.

## Prompts relevantes
1. "Ya sabes, pon las pruebas, las evidencias y la justificación", acompañado del mandato U03.E05 y del proyecto base `INF8239_U03_Recomendadores_Proyecto_Base`.

## Qué hizo la IA
- Diseñó la partición temporal por usuario (70/10/20) y la reserva de 61 usuarios fríos.
- Extendió el proyecto base: puntuación vectorizada de todo el catálogo, métricas de ranking (precision, recall, NDCG, acierto), novedad, frontera de Pareto, búsqueda de hiperparámetros de la factorización y evaluación de usuarios fríos.
- Escribió las pruebas nuevas, el cuaderno, la Dataset Card, la System Card, el README y el generador del PDF.

## Qué se verificó
- Licencia y cita de MovieLens en el README del propio dataset; el dataset no se versiona.
- SHA-256 del ZIP; la descarga falla si no coincide.
- Las 13 pruebas pasan (`reports/pruebas.txt`).
- Tras corregir el error de ítems vistos, se volvió a ejecutar el experimento y las métricas no cambiaron.

## Correcciones realizadas
- Una prueba nueva mostró que `recommend` devolvía películas ya vistas cuando se pedían más recomendaciones que películas disponibles. Se corrigió para filtrar siempre las vistas.
- La figura de Pareto usaba un acceso frágil a columnas; se simplificó.
- La descarga del proyecto base no comparaba el SHA-256; se añadió la verificación.

## Modelos de IA: uso real, responsabilidades y límites

La columna **«Uso en esta práctica»** solo describe lo que ocurrió. Las columnas **«Para qué sirve»** y **«Límite»** muestran el criterio con que se eligió cada herramienta, aunque algunos modelos no se hayan usado.

| Herramienta | Modelo | Uso en esta práctica | Para qué sirve (responsabilidad asignable) | Límite y control |
|---|---|---|---|---|
| Claude Code (Anthropic) | **Claude Opus 5.5** | **Usado.** Agente en VS Code: leyó el proyecto base, escribió código, pruebas, cuadernos y documentación, ejecutó los scripts y generó el PDF | Tareas largas de varios pasos sobre un repositorio: leer código, ejecutar la terminal, depurar y documentar | Puede proponer errores o cifras sin respaldo; todo se verificó ejecutando pruebas y leyendo los reportes |
| Claude (Anthropic) | Claude Sonnet 5 | No usado | Programación cotidiana con buen equilibrio entre velocidad y calidad | Menos profundidad que Opus en tareas largas |
| Claude (Anthropic) | Claude Haiku 4.5 | No usado | Tareas rápidas y de bajo costo: resúmenes, clasificación de textos, revisiones breves | No indicado para diseño experimental complejo |
| Codex (OpenAI) | Modelo de OpenAI orientado a código (familia GPT-5-Codex) | Apoyo complementario durante el desarrollo | Agente de programación: proponer y revisar cambios de código, explicar errores y sugerir pruebas | El código generado se acepta solo si pasa las pruebas del repositorio |
| DeepSeek | DeepSeek-V3 (chat) | Apoyo complementario durante el desarrollo | Explicación de conceptos, lluvia de ideas y revisión de redacción | Puede inventar referencias; toda cita se verificó en la fuente original |
| DeepSeek | DeepSeek-R1 (razonamiento) | No usado; recomendado para revisar la lógica de las métricas | Razonamiento paso a paso: matemáticas, lógica de métricas y depuración | Respuestas más lentas y largas; el razonamiento no sustituye la ejecución |

### Reparto de responsabilidades

| Responsabilidad | Quién |
|---|---|
| Valores del análisis (daño prioritario, tolerancias, compuertas, decisiones de uso) | La autora |
| Elección de datos y verificación de licencias y referencias | La autora, con apoyo de las herramientas |
| Generación de borradores de código, pruebas y redacción | Herramientas de IA |
| Ejecución de pruebas y comprobación de cada cifra contra `reports/` | La autora, con Claude Code |
| Defensa oral y respuesta a preguntas técnicas | La autora |

## Responsabilidad
La autora revisó el código, las cifras y las conclusiones, y responde por ellos.
