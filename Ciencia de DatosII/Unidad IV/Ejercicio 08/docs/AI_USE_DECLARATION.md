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

## Responsabilidad
La autora revisó el código, las referencias, la interpretación normativa y las conclusiones, y responde por ellos.
