# Declaración de uso de IA · Ejercicio 03

## Herramienta
Claude Code (modelo Claude Opus 5.5, de Anthropic), usado dentro de VS Code sobre este repositorio.

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

## Responsabilidad
La autora revisó el código, las cifras y las conclusiones, y responde por ellos.
