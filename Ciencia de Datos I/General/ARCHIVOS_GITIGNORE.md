# Archivos incluidos y excluidos de Git

## Incluidos en GitHub

- Código fuente y scripts.
- Pruebas automatizadas.
- README y documentación HTML/Markdown.
- Cuadernos de Google Colab.
- Artículos DOCX y documentos académicos.
- Resultados finales CSV.
- Gráficos y matrices de confusión.
- Predicciones generales y caso a caso.
- Métricas, F1 manual e importancias.
- Plantillas y recursos académicos.

## Excluidos mediante `.gitignore`

- `.venv/`: dependencias instaladas localmente.
- `__pycache__/` y `*.pyc`: archivos compilados de Python.
- `.pytest_cache/`: caché de pruebas.
- `.matplotlib-cache/`: caché de fuentes y gráficos.
- `.DS_Store`: metadatos de macOS.
- `.env`: credenciales y configuración privada.
- `data/oulad.zip`: dataset público descargable de aproximadamente 45 MB.
- `*.zip`: paquetes de entrega que duplican archivos versionados.
- `evidencias_locales/`: logs que pueden contener información del entorno local.

## Razón

Todo archivo necesario para comprender, revisar y evaluar las prácticas está publicado. Solo
se excluyen archivos regenerables, duplicados, pesados o potencialmente privados.
