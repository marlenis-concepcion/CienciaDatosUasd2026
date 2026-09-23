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

## Responsabilidad
La autora revisó el código, las referencias, la interpretación normativa y las conclusiones, y responde por ellos.
