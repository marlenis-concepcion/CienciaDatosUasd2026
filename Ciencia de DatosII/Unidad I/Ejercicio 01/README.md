# Ejercicio 01 · Dataset público y SVM reproducible

**Autora:** Marlenis Judith Concepción Cuevas · **Asignatura:** INF-8239-C2 · **Unidad:** I.

**Estado:** implementación ejecutable basada en el mandato compartido. Ionosphere es una propuesta **pendiente de aprobación docente**. Faltan los capítulos completos de LAB01–LAB03 para comprobar requisitos adicionales. No se debe declarar aprobación ni entrega definitiva sin esa confirmación.

## Archivos

- `notebooks/ejercicio_01.ipynb`: cuaderno ejecutado con resultados y figuras.
- `src/`: código reutilizable de ejecución e informe.
- `tests/`: cuatro pruebas automatizadas.
- `reports/`: CSV, figuras, conclusión y PDF.
- `requirements.txt`: versiones de dependencias usadas.

## Instalación y ejecución

Python 3.9, utilizado en esta ejecución. Desde esta carpeta, en macOS/Linux:

```sh
python3 -m venv ../.venv
source ../.venv/bin/activate
python -m pip install -r requirements.txt
```

Ejecutar el experimento, generar el informe y verificar las pruebas:

```sh
python src/laboratorio_e01.py
python src/informe.py
python -m pytest -q tests
```

El notebook se puede abrir en VS Code o Jupyter seleccionando el intérprete de `Unidad I/.venv`. Ejecutar todas las celdas en orden. Su ejecución vuelve a generar los resultados. Los tiempos pueden variar entre ejecuciones.

## Datos y reproducibilidad

Dataset: [Ionosphere, UCI](https://archive.ics.uci.edu/dataset/52/ionosphere). Sigillito, Wing, Hutton y Baker (1989), [DOI](https://doi.org/10.24432/C5W01B), licencia CC BY 4.0.

La primera ejecución de E01 descarga `https://archive.ics.uci.edu/static/public/52/ionosphere.zip`, extrae `ionosphere.data` y valida SHA256 `46d52186b84e20be52918adb93e8fb9926b34795ff7504c24350ae0616a04bbd`. El archivo queda en `Ejercicio 01/data/`, excluido de Git. Si no hay red y no existe ese archivo, el programa falla explícitamente, sin sustituir los datos.

Target: `clase`, con `b=0` y `g=1`. Se elimina un duplicado exacto: quedan 350 filas. Se conservan 34 predictores y se registra una columna constante. División estratificada fija: 210 entrenamiento, 70 validación, 70 prueba; semilla 42. Los índices originales están en `reports/particiones.csv`. El identificador no se incluye como predictor.

La imputación, escala y, cuando corresponde, PCA se ajustan solo en entrenamiento, dentro del pipeline. Los hiperparámetros del SVM se eligen mediante cinco pliegues estratificados sobre entrenamiento; no se ajustan a prueba. Las métricas incluyen F1 macro, accuracy, precisión macro, recall por clase y ROC AUC.

## Entrega

PDF: [`reports/Ejercicio_01.pdf`](reports/Ejercicio_01.pdf). Revisar [`reports/conclusion.md`](reports/conclusion.md) y adaptar la reflexión a lo que puedas explicar y defender. Los resultados son reales; la conclusión redactada es un borrador para revisión personal.

Repositorio: [CienciaDatosUasd2026](https://github.com/marlenis-concepcion/CienciaDatosUasd2026/tree/main/Ciencia%20de%20DatosII/Unidad%20I/Ejercicio%2001).

## Evidencia y pruebas

- Comparación y aprobación pendiente: `reports/seleccion_dataset.md`.
- Auditoría y diccionario: `reports/auditoria.json`, `reports/diccionario.csv`.
- Búsqueda: `reports/busqueda_cv.csv`, `reports/parametros.json`.
- Resultados y errores: `reports/resultados.csv`, `reports/predicciones_prueba.csv`.
- Modelo: `reports/modelos/svm.joblib`.
- Las pruebas comprueban separación y cobertura, ajuste del escalador solo con entrenamiento, esquema sin target ni duplicados y tolerancia a faltantes.

## Decisiones y correcciones

La auditoría detectó un duplicado que se retiró antes de separar los conjuntos. Se conservó la columna constante para mantener el esquema; StandardScaler la maneja sin dividir por cero. La aprobación permanece pendiente.
