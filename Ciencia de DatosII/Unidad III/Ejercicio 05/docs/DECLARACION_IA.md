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

## Responsabilidad
La autora revisó el código, las cifras y las conclusiones, y responde por ellos.
