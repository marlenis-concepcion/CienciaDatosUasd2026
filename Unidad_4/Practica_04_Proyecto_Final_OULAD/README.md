# Proyecto final colaborativo: Machine Learning sobre OULAD

Asignatura: INF-8237-C2 Ciencia de Datos I  
Unidad 4: Introducción a Machine Learning  
Equipo: McCarthy Team
Facilitador: Silverio de Orbe Abad

## Enlaces de entrega

- **Práctica en GitHub:**  
  https://github.com/marlenis-concepcion/CienciaDatosUasd2026/tree/main/Unidad_4/Practica_04_Proyecto_Final_OULAD
- **Abrir cuaderno en Google Colab:**  
  https://colab.research.google.com/github/marlenis-concepcion/CienciaDatosUasd2026/blob/main/Unidad_4/Practica_04_Proyecto_Final_OULAD/notebooks/Proyecto_Final_OULAD_Colab.ipynb
- **Artículo científico APA 7:**  
  https://github.com/marlenis-concepcion/CienciaDatosUasd2026/blob/main/Unidad_4/Practica_04_Proyecto_Final_OULAD/docs/Articulo_Cientifico_OULAD_APA7.docx
- **Documentación del proyecto:**  
  https://github.com/marlenis-concepcion/CienciaDatosUasd2026/blob/main/Unidad_4/Practica_04_Proyecto_Final_OULAD/README.md

## Entregables incluidos

- `index.html`: documentación visual y navegable del proyecto.
- `notebooks/Proyecto_Final_OULAD_Colab.ipynb`: cuaderno listo para Google Colab.
- `src/`: implementación POO del flujo OSEMN.
- `docs/Articulo_Cientifico_OULAD_APA7.docx`: artículo en formato APA 7/UASD.
- `docs/Articulo_Cientifico_OULAD_APA7.md`: versión editable del contenido.
- `outputs/`: CSV de métricas, predicciones caso a caso, importancias y gráficos.
- `tests/`: validación del cálculo manual de F1 y de las estructuras del proyecto.

## Preguntas e hipótesis

**H1.** El compromiso temprano con el entorno virtual, medido por clics y días activos
durante los primeros 28 días, difiere entre quienes aprueban y quienes no aprueban.

**H2.** Un conjunto de variables demográficas, académicas y de interacción temprana permite
predecir el resultado final y el promedio de evaluaciones mejor que una referencia ingenua.

Se modelan tres tipos de variable:

- Dicotómica: `aprobo`.
- Ordinal: `resultado_ordinal` (retiro, reprobado, aprobado, distinción).
- Intervalo/razón: `promedio_evaluaciones`.

## Datos

El proyecto descarga OULAD desde UCI cuando no encuentra `data/oulad.zip`. La publicación
original describe 32,593 registros de estudiantes y más de 10.6 millones de interacciones VLE.

El complemento denominado **Experimento X** es sintético, anónimo y reproducible. No se
presenta como información real del Congo ni de otra institución.

## Ejecución local

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 run.py
```

Para una prueba rápida sin descargar OULAD:

```bash
python3 run.py --synthetic-only --sample-size 3000
```

## Google Colab

1. Subir el folder a Google Drive o abrir el cuaderno.
2. Ejecutar todas las celdas.
3. Descargar `outputs/`.
4. Compartir el cuaderno con permiso de lectura y salidas guardadas.

Todas las rutas son relativas al proyecto. No se incluyen rutas de una computadora personal.

Para abrir la documentación local:

```bash
python3 -m http.server 8000
```

Luego visite `http://localhost:8000`.

## División colaborativa propuesta

| Rol | Responsabilidad |
| --- | --- |
| Coordinación y artículo | Integración, hipótesis, revisión APA y conclusiones |
| Ingeniería de datos | Descarga, limpieza, faltantes y variables derivadas |
| EDA e inferencia | Gráficos, descriptiva y pruebas de hipótesis |
| Modelado | Entrenamiento, evaluación, F1 manual e importancias |
| QA y reproducibilidad | Pruebas, revisión de CSV, Colab y checklist |
