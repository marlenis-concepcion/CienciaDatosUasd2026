# Declaración de uso de IA · Ejercicio 07

## Herramientas
- Claude Code (modelo Claude Opus 5.5, de Anthropic), en VS Code sobre este repositorio.
- Codex (OpenAI), como apoyo complementario durante el desarrollo.
- DeepSeek, como apoyo complementario durante el desarrollo.

## Finalidad
Claude Code propuso la estructura del expediente, redactó los borradores de la evaluación de impacto, el mapa de interesados, el registro de riesgos y la matriz normativa, escribió el módulo `evaluation.py` (alternativa no predictiva, bootstrap, celdas pequeñas, mitigaciones y regla de decisión), las pruebas, el cuaderno y el generador del PDF.

## Prompts relevantes
- "Ahora la unidad 4 tiene la práctica", acompañado del mandato U04.E07 y del proyecto base `INF8239_U04_Gobernanza_DSS_Proyecto_Base_uv`.

## Qué decidió la autora y qué no decidió la IA
Los valores del análisis (el falso negativo como daño prioritario, la tolerancia de las compuertas del proyecto base, preferir la alternativa menos intrusiva y no usar el grupo protegido para decidir) son decisiones de la autora, que debe defender. La IA no fija esos valores.

## Verificaciones
- Las subcategorías del NIST AI RMF citadas (GOVERN 1.1, MAP 1.1, MAP 2.3, MAP 3.4, MEASURE 2.8, 2.10, 2.11 y MANAGE 4.1) se contrastaron con el texto del documento oficial NIST AI 100-1.
- La Ley 172-13 y los artículos 39, 44 y 70 de la Constitución se verificaron en fuentes oficiales (ONE, Presidencia).
- Las 23 pruebas pasan (`reports/pruebas.txt`); las cifras del PDF salen de `reports/`.

## Errores detectados y correcciones
- `scripts/lab11_impact.py` y `scripts/simulate_incident.py` del proyecto base tenían saltos de línea dentro de cadenas de texto y no ejecutaban; se corrigieron.
- `matplotlib` faltaba en las dependencias; se añadió.
- La recomendación de `lab12_decision.yml` se redactó después de ver la comparación de candidatos y se comprobó que coincide con la decisión calculada en `reports/lab12/decision.json`.

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

## Responsabilidad
La autora revisó el código, las referencias, la interpretación normativa y las conclusiones, y responde por ellos.
