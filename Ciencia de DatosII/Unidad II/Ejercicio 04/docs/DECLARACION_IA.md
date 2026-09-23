# Declaración de uso de IA · Ejercicio 04

## Herramienta
Claude Code (modelo Claude Opus 5.5, de Anthropic), usado dentro de VS Code sobre este repositorio.

## Prompts relevantes
1. "Hazlo ambos y sigue la guía del profesor", acompañado del texto del mandato U02.E04 y del proyecto base `INF8239_U02_CV_Proyecto_Base`.
2. "Termina el ejercicio, lo que quiero es entregarlo": se priorizó cerrar la entrega en lugar de seguir explorando arquitecturas.

## Qué hizo la IA
- Adaptó el proyecto base: auditoría de duplicados por hash, validación estratificada con semilla, línea base, curvas, métricas por clase, costo y regla de decisión.
- Propuso la variante `cnn_flatten` después de observar que la CNN del proyecto base no convergía.
- Escribió las pruebas nuevas, el cuaderno, la Model Card, el README y el generador del PDF.

## Qué se verificó
- Con 8 épocas, como indica el proyecto base, la CNN base obtuvo F1 0.785 en prueba, por debajo del modelo denso; se guardó esa corrida en `reports/corrida_8_epocas/`.
- Los modelos guardados, cargados desde el cuaderno, reproducen exactamente las métricas registradas en `reports/cv_metrics.json`.
- La partición de validación recalculada en el cuaderno coincide con los índices guardados.
- Las 9 pruebas pasan (`reports/pruebas.txt`).
- Licencia MIT y referencia de Fashion-MNIST (Xiao, Rasul y Vollgraf, 2017).

## Correcciones realizadas
- La primera regla de decisión comparaba solo denso contra CNN base; al añadir la tercera arquitectura se sustituyó por una regla general (menos parámetros dentro de 0.01 del mejor F1 de validación), fijada antes de evaluar en prueba.
- El proyecto base tomaba las últimas 6000 imágenes como validación sin estratificar; se cambió a una partición estratificada con semilla.
- Se añadió `pandas` a las dependencias, porque faltaba en el proyecto base.

## Responsabilidad
La autora revisó el código, las cifras y las conclusiones, y responde por ellos.
