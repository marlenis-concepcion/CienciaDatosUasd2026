# Declaración de uso de IA · Ejercicio 08

## Herramientas
- Claude Code (modelo Claude Opus 5.5, de Anthropic), en VS Code sobre este repositorio.
- Codex (OpenAI), como apoyo complementario durante el desarrollo.
- DeepSeek, como apoyo complementario durante el desarrollo.

## Finalidad
Claude Code redactó los borradores del inventario de datos, la Datasheet, la Model Card, el RACI, el documento de traspaso y el runbook; escribió `lifecycle.py` (minimización, retención, manifiesto de hashes, monitoreo de entradas y desempeño, respuesta del runbook), el simulacro (`scripts/run_e08.py`), las pruebas, el cuaderno y el generador del PDF.

## Prompts relevantes
- "Ahora la unidad 4 tiene la práctica", acompañado del mandato U04.E08 y del proyecto base.

## Qué decidió la autora
Plazos de retención, umbrales de monitoreo, reparto de responsabilidades (RACI) y la decisión de contener ante deriva de datos son decisiones de la autora, que debe defender.

## Verificaciones
- Las 34 pruebas pasan (`reports/pruebas.txt`), incluidas las que comparan los hashes de la documentación con los archivos reales.
- El monitor no alerta en ninguna semana normal y sí detecta la falla inyectada en la primera semana.
- Las cifras del postmortem salen de `reports/lab13/simulacro.json`.

## Errores detectados y correcciones
- El primer diseño del simulacro (exposición en 0 solo en la zona Sur) no cambiaba ninguna predicción; se rediseñó como un cambio de escala en la ingesta.
- El primer monitor mensual alertaba en meses normales por lotes pequeños (unos 50 casos); se separó en control semanal de entradas (sin etiquetas) y control de desempeño con ventana de 100 casos.
- El PSI con cortes por cuantiles era inestable para variables enteras; se calcula por categorías cuando hay pocos valores.
- Al crear este ejercicio, el entorno del Ejercicio 07 quedó apuntando a este código; se separaron los entornos.

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
La autora revisó el código, las referencias, la interpretación normativa y las conclusiones, y responde por ellos.
