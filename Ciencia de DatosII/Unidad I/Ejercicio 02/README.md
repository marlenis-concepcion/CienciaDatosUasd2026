# Ejercicio 02 · Ensambles, reducción y Green AI

**Autora:** Marlenis Judith Concepción Cuevas · **Asignatura:** INF-8239-C2 · **Unidad:** I.

**Estado:** implementación ejecutable basada en el mandato compartido. Ionosphere es una propuesta **pendiente de aprobación docente**. Faltan los capítulos completos de LAB01–LAB03 para comprobar requisitos adicionales. No se debe declarar aprobación ni entrega definitiva sin esa confirmación.

## Archivos

- `notebooks/ejercicio_02.ipynb`: cuaderno ejecutado con resultados y figuras.
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

Ejecuta primero el Ejercicio 01. Este ejercicio carga sus datos, parámetros SVM e índices y verifica que la partición sea idéntica.

Ejecutar el experimento, generar el informe y verificar las pruebas:

```sh
python src/laboratorio_e02.py
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

PDF: [`reports/Ejercicio_02.pdf`](reports/Ejercicio_02.pdf). Revisar [`reports/conclusion.md`](reports/conclusion.md) y adaptar la reflexión a lo que puedas explicar y defender. Los resultados son reales; la conclusión redactada es un borrador para revisión personal.

Repositorio: [CienciaDatosUasd2026](https://github.com/marlenis-concepcion/CienciaDatosUasd2026/tree/main/Ciencia%20de%20DatosII/Unidad%20I/Ejercicio%2002).

## Seis configuraciones y medición

1. SVM con los parámetros del Ejercicio 01.
2. SVM con PCA que retiene al menos 95% de varianza de entrenamiento.
3. Random Forest: 50 árboles, profundidad máxima 6.
4. Random Forest: 150 árboles, profundidad sin límite.
5. Gradient Boosting: 50 etapas, profundidad 2, learning rate 0.1.
6. Gradient Boosting: 100 etapas, profundidad 2, learning rate 0.1.

Tres repeticiones con igual semilla y partición, orden alternado, un hilo y calentamiento excluido. Inferencia: 30 predicciones del mismo lote por repetición; mediana y división por número de filas. Después se toma la mediana de las tres repeticiones. Es latencia amortizada, no latencia de una petición aislada. Tamaño: pipeline serializado sin compresión en KiB. Los seis modelos están en `reports/modelos/`.

Pareto maximiza F1 macro de validación y minimiza ajuste, inferencia y tamaño. Se elige la menor latencia entre los no dominados cuyo F1 esté a no más de 0.02 del máximo. El desempate es tamaño y nombre. El test solo se informa para el elegido en este ejercicio. E01 ya evaluó SVM sobre ese mismo test; por ello no es una replicación independiente. No se usa ese resultado para elegir las seis configuraciones.

PCA y las dos proyecciones t-SNE (semillas 42/73, perplexity 30) emplean exclusivamente entrenamiento. t-SNE no alimenta ningún clasificador. Su calidad local se acompaña con trustworthiness. La figura Pareto es una proyección de cuatro objetivos a dos ejes.

Se registran equipo y método en `reports/entorno.json`. No se midió consumo eléctrico ni CO2, ni RAM máxima: no se presentan tiempo y tamaño como mediciones de energía. Las tres repeticiones no estiman variabilidad estadística del desempeño.

Las pruebas verifican dominancia de Pareto, regla de selección, seis pipelines y evidencia de particiones y repeticiones.

## Corrección durante la ejecución

Se corrigió la precedencia de importaciones para que el notebook 02 cargue su propio generador de informe y reutilice únicamente las funciones de datos del Ejercicio 01. Se repitió la ejecución completa tras corregirlo.
