# Declaración de uso de inteligencia artificial

## Herramientas utilizadas
- Claude Code (modelo Claude Opus 5.5, de Anthropic), en VS Code sobre este repositorio.
- Codex (OpenAI), como apoyo complementario durante el desarrollo.
- DeepSeek, como apoyo complementario durante el desarrollo.

## Propósito de cada uso
Claude Code adaptó el proyecto base (validación explícita, VAE con `test_step`, líneas base de imagen media y PCA, VAE con latente 16, clasificador juez, medidas de fidelidad, diversidad y memoria), escribió pruebas, cuaderno, Model Card, README y el generador del PDF.

## Prompts o decisiones relevantes
- "Ya sabes, pon las pruebas, las evidencias y la justificación", acompañado del mandato U03.E06 y del proyecto base `INF8239_U03_Generativos_Proyecto_Base`.
- Decisión: comparar VAE 2 y VAE 16 por la pérdida total de validación, fijada antes de evaluar en prueba.

## Elementos verificados por el equipo
- Las 12 pruebas pasan (`reports/pruebas.txt`).
- Los modelos guardados, recargados en el cuaderno, reproducen el error de reconstrucción registrado.
- Las figuras de reconstrucción, muestras e interpolación se revisaron visualmente.
- Licencia MIT y referencia de Fashion-MNIST (Xiao, Rasul y Vollgraf, 2017).

## Cambios realizados sobre resultados generados
- Una prueba exigía error exactamente 0 para una copia perfecta; falló por el recorte a 1e-7 que evita log(0). Se ajustó la tolerancia de la prueba; el cálculo no cambió.
- El proyecto base entrenaba el VAE sin validación; se añadió `test_step` para poder usar parada temprana y comparar modelos.
- Se añadió `pandas` a las dependencias.

## Modelos de IA: uso real, responsabilidades y límites

La columna **«Uso en esta práctica»** solo describe lo que ocurrió. Las columnas **«Para qué sirve»** y **«Límite»** muestran el criterio con que se eligió cada herramienta, aunque algunos modelos no se hayan usado.

| Herramienta | Modelos | Uso en esta práctica | Para qué sirve cada modelo | Control |
|---|---|---|---|---|
| Claude Code (Anthropic) | **Claude Opus 5.5** · Claude Sonnet 5 · Claude Haiku 4.5 | **Agente principal (Opus 5.5)**: leyó el proyecto base, escribió código, pruebas, cuadernos y documentación, ejecutó los scripts y generó el PDF | Opus 5.5: tareas largas de varios pasos · Sonnet 5: programación cotidiana · Haiku 4.5: tareas rápidas y baratas | Todo se verificó con pruebas y reportes |
| Codex (OpenAI) | **GPT-5-Codex** · codex-mini | Apoyo complementario | GPT-5-Codex: proponer y revisar cambios de código en el repositorio · codex-mini: respuestas rápidas en terminal | El código se acepta solo si pasa las pruebas |
| DeepSeek | **DeepSeek-V3** · DeepSeek-R1 · DeepSeek-Coder-V2 | Apoyo complementario | V3: explicar conceptos y revisar redacción · R1: razonamiento paso a paso sobre métricas · Coder-V2: generar código | Toda referencia se verificó en la fuente |

### Reparto de responsabilidades

| Responsabilidad | Quién |
|---|---|
| Valores del análisis (daño prioritario, tolerancias, compuertas, decisiones de uso) | La autora |
| Elección de datos y verificación de licencias y referencias | La autora, con apoyo de las herramientas |
| Generación de borradores de código, pruebas y redacción | Herramientas de IA |
| Ejecución de pruebas y comprobación de cada cifra contra `reports/` | La autora, con Claude Code |
| Defensa oral y respuesta a preguntas técnicas | La autora |

## Responsabilidad asumida
La autora revisó el código, las cifras y las conclusiones, y responde por ellos.
