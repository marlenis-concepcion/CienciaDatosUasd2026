# Declaración de uso de IA · Ejercicio 04

## Herramientas
- Claude Code (modelo Claude Opus 5.5, de Anthropic), usado dentro de VS Code sobre este repositorio.
- Codex (OpenAI), como apoyo complementario durante el desarrollo.
- DeepSeek, como apoyo complementario durante el desarrollo.

## Prompts relevantes
1. "Hazlo ambos y sigue la guía del profesor", acompañado del texto del mandato U02.E04 y del proyecto base `INF8239_U02_CV_Proyecto_Base`.
2. "Termina el ejercicio, lo que quiero es entregarlo": se priorizó cerrar la entrega en lugar de seguir explorando arquitecturas.

## Qué hizo la IA
- Adaptó el proyecto base: auditoría de duplicados por hash, validación estratificada con semilla, línea base, curvas, métricas por clase, costo y regla de decisión.
- Propuso la variante `cnn_flatten` después de observar que la CNN del proyecto base no convergía.
- Escribió las pruebas nuevas, el cuaderno, la Model Card, el README y el generador del PDF.

## Qué se verificó
- Con 8 épocas, como indica el proyecto base, la CNN base obtuvo F1 0.785 en prueba, por debajo del modelo denso; se guardó esa corrida en `reports/corrida_8_epocas/`.
- Los modelos guardados, cargados desde el cuaderno, reproducen exactamente las métricas registradas en `reports/cv_metrics.json`.
- La partición de validación recalculada en el cuaderno coincide con los índices guardados.
- Las 9 pruebas pasan (`reports/pruebas.txt`).
- Licencia MIT y referencia de Fashion-MNIST (Xiao, Rasul y Vollgraf, 2017).

## Correcciones realizadas
- La primera regla de decisión comparaba solo denso contra CNN base; al añadir la tercera arquitectura se sustituyó por una regla general (menos parámetros dentro de 0.01 del mejor F1 de validación), fijada antes de evaluar en prueba.
- El proyecto base tomaba las últimas 6000 imágenes como validación sin estratificar; se cambió a una partición estratificada con semilla.
- Se añadió `pandas` a las dependencias, porque faltaba en el proyecto base.

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
