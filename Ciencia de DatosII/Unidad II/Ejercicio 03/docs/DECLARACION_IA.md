# Declaración de uso de IA · Ejercicio 03

## Herramientas
- Claude Code (modelo Claude Opus 5.5, de Anthropic), usado dentro de VS Code sobre este repositorio.
- Codex (OpenAI), como apoyo complementario durante el desarrollo.
- DeepSeek, como apoyo complementario durante el desarrollo.

## Prompts relevantes
1. "Hazlo ambos y sigue la guía del profesor", acompañado del texto del mandato U02.E03 y del proyecto base `INF8239_U02_NLP_Proyecto_Base`.
2. Solicitudes de seguimiento para usar el índice del repositorio y ajustar la redacción de los README.

## Qué hizo la IA
- Propuso los dos corpus candidatos y adaptó el proyecto base del profesor: descarga verificada, deduplicación antes de partir, partición 70/15/15, búsqueda de hiperparámetros con validación cruzada y selección en validación.
- Escribió las pruebas nuevas (`tests/test_leakage.py`), el cuaderno, la Dataset Card, este README y el generador del PDF.
- Propuso la clasificación inicial de los 23 errores a partir de la lectura de cada mensaje.

## Qué se verificó
- Licencia CC BY 4.0 y DOI de ambos candidatos, comprobados en las fichas de UCI.
- Composición del corpus y referencia bibliográfica, comprobadas en el `readme` incluido en el ZIP original.
- SHA-256 del archivo descargado; la descarga se rechaza si no coincide.
- Las 13 pruebas pasan (`reports/pruebas.txt`) y dos ejecuciones completas producen las mismas métricas y los mismos 23 errores.
- Cada cifra del PDF y del cuaderno procede de los archivos de `reports/` generados por el código.

## Correcciones realizadas
- La primera versión de la Dataset Card describía tres fuentes del corpus; al leer el `readme` original se corrigió a cuatro, con sus cantidades exactas, y se eliminó un rango de años que no estaba respaldado.
- Una prueba de partición falló porque el corpus sintético solo variaba en los dígitos y la normalización lo convertía en duplicados. Se corrigió el corpus de la prueba; el código evaluado no cambió.
- El proyecto base guardaba solo el modelo logístico y tomaba la partición sin validación; se añadió un conjunto de validación y la decisión se registra antes de evaluar en prueba.

## Modelos de IA: uso real, responsabilidades y límites

La columna **«Uso en esta práctica»** solo describe lo que ocurrió. Las columnas **«Para qué sirve»** y **«Límite»** muestran el criterio con que se eligió cada herramienta, aunque algunos modelos no se hayan usado.

| Herramienta | Modelo | Uso en esta práctica | Para qué sirve (responsabilidad asignable) | Límite y control |
|---|---|---|---|---|
| Claude Code (Anthropic) | **Claude Opus 5.5** | **Usado.** Agente en VS Code: leyó el proyecto base, escribió código, pruebas, cuadernos y documentación, ejecutó los scripts y generó el PDF | Tareas largas de varios pasos sobre un repositorio: leer código, ejecutar la terminal, depurar y documentar | Puede proponer errores o cifras sin respaldo; todo se verificó ejecutando pruebas y leyendo los reportes |
| Claude (Anthropic) | Claude Sonnet 5 | No usado | Programación cotidiana con buen equilibrio entre velocidad y calidad | Menos profundidad que Opus en tareas largas |
| Claude (Anthropic) | Claude Haiku 4.5 | No usado | Tareas rápidas y de bajo costo: resúmenes, clasificación de textos, revisiones breves | No indicado para diseño experimental complejo |
| Codex (OpenAI) | Modelo de OpenAI configurado en Codex (versión a verificar en la configuración usada) | Apoyo complementario durante el desarrollo | Agente de programación: proponer y revisar cambios de código, explicar errores y sugerir pruebas | El código generado se acepta solo si pasa las pruebas del repositorio |
| DeepSeek | DeepSeek-V3 (chat) | Apoyo complementario durante el desarrollo | Explicación de conceptos, lluvia de ideas y revisión de redacción | Puede inventar referencias; toda cita se verificó en la fuente original |
| DeepSeek | DeepSeek-R1 (razonamiento) | No consta su uso (verificar) | Razonamiento paso a paso: matemáticas, lógica de métricas y depuración | Respuestas más lentas y largas; el razonamiento no sustituye la ejecución |

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
