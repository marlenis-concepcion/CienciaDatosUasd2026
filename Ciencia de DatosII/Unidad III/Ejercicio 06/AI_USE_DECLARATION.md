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

## Responsabilidad asumida
La autora revisó el código, las cifras y las conclusiones, y responde por ellos.
