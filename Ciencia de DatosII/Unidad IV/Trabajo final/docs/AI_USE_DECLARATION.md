# Declaración de uso de IA · Trabajo final

## Herramientas
- Claude Code (modelo Claude Opus 5.5, de Anthropic), en VS Code sobre este repositorio.
- Codex (OpenAI), como apoyo complementario durante el desarrollo.
- DeepSeek, como apoyo complementario durante el desarrollo.

## Finalidad
Claude Code propuso el tema dentro del mandato, la estructura del proyecto y el flujo de trabajo en GitHub (issues, ramas, pull requests), y escribió el código (`src/tutoria_dss`), los scripts, las pruebas, la aplicación, la documentación y el generador del informe.

## Prompts relevantes
- «Haz el trabajo final también, el folder que va», con el mandato del trabajo final.
- «Pon muchas pruebas, más de 15, que se vea que se hizo el trabajo».

## Decisiones de valores de la autora
Capacidad del 15 %, compuertas (recall mínimo 0.35 y brecha máxima 0.15), reglas de tipo de apoyo y **repartir los cupos por franja de edad**. Esta última usa la edad para asignar un apoyo voluntario, no dentro del modelo ni para sancionar; la autora debe confirmarla y defenderla.

## Verificaciones
- Licencia CC BY 4.0 y DOI 10.24432/C5MC89 en la ficha de UCI; SHA-256 del archivo descargado.
- Todas las pruebas pasan (`reports/pruebas.txt`); cada cifra del informe sale de `reports/`.
- La mitigación se eligió en validación y la prueba se evaluó una sola vez.

## Errores detectados y correcciones
- El riesgo se redondeaba antes de seleccionar y una prueba falló; ahora se redondea solo al mostrar.
- Las explicaciones decían «unidades aprobadas» sin valor; ahora muestran el valor del estudiante.
- La primera versión de los pull requests usaba «Cierra #1», que GitHub no reconoce; se cambió a «Closes».

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
La autora revisó el código, las cifras, las referencias y las conclusiones, y responde por ellos.
