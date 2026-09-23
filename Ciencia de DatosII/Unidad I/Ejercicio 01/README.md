# Ejercicio 01 · Dataset público y SVM reproducible

**Autora:** Marlenis Judith Concepción Cuevas · **Asignatura:** INF-8239-C2 · **Unidad:** I.

**Estado:** implementación ejecutable basada en el mandato compartido. Ionosphere es una propuesta **pendiente de aprobación docente**. Faltan los capítulos completos de LAB01–LAB03 para comprobar requisitos adicionales. No se debe declarar aprobación ni entrega definitiva sin esa confirmación.

## Archivos

- `notebooks/ejercicio_01.ipynb`: cuaderno ejecutado con resultados y figuras.
- `src/`: código reutilizable de ejecución e informe.
- `tests/`: 15 pruebas automatizadas; lista justificada en `docs/pruebas.csv` y abajo.
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

PDF: [`reports/Ejercicio_01.pdf`](reports/Ejercicio_01.pdf). Conclusión: [`reports/conclusion.md`](reports/conclusion.md).

Repositorio: [CienciaDatosUasd2026](https://github.com/marlenis-concepcion/CienciaDatosUasd2026/tree/main/Ciencia%20de%20DatosII/Unidad%20I/Ejercicio%2001).

## Evidencia y pruebas

- Comparación y aprobación pendiente: `reports/seleccion_dataset.md`.
- Auditoría y diccionario: `reports/auditoria.json`, `reports/diccionario.csv`.
- Búsqueda: `reports/busqueda_cv.csv`, `reports/parametros.json`.
- Resultados y errores: `reports/resultados.csv`, `reports/predicciones_prueba.csv`.
- Modelo: `reports/modelos/svm.joblib`.
- Las pruebas comprueban separación y cobertura, ajuste del escalador solo con entrenamiento, esquema sin target ni duplicados y tolerancia a faltantes.

## Pruebas automatizadas

15 pruebas, todas aprobadas (`python -m pytest -q tests`, resultado en `reports/pruebas.txt`).

1. **`test_particiones_sin_solapamiento_y_con_cobertura`**. Entrenamiento, validación y prueba no comparten filas, cubren todo el conjunto, tienen las dos clases y se repiten igual. *Por qué:* Base de toda la evaluación: sin esto habría fuga o resultados no reproducibles.
2. **`test_escalador_no_usa_datos_de_evaluacion`**. El escalador aprende la media solo de entrenamiento y no cambia al predecir datos nuevos. *Por qué:* Evita fuga de información de validación o prueba hacia el modelo.
3. **`test_esquema_target_y_duplicados`**. Las 34 columnas son las esperadas, el target no está entre los predictores y no quedan duplicados. *Por qué:* Contrato de datos antes de entrenar.
4. **`test_pipeline_admite_faltantes_sin_reajustar`**. El pipeline predice aunque aparezca un valor faltante. *Por qué:* Robustez ante datos incompletos en uso real.
5. **`test_descarga_rechaza_archivo_alterado`**. Un archivo con SHA256 distinto al documentado se rechaza. *Por qué:* Garantiza que siempre se usan los mismos datos de UCI.
6. **`test_duplicado_eliminado_antes_de_partir`**. Hay 351 registros originales y 350 después de quitar el único duplicado. *Por qué:* Un duplicado podría quedar a la vez en entrenamiento y en prueba.
7. **`test_codificacion_del_target_respeta_las_clases_originales`**. Las cantidades de b=0 y g=1 coinciden con las etiquetas originales. *Por qué:* Un error al codificar invertiría el significado de todas las métricas.
8. **`test_tamanos_y_estratificacion_de_la_particion`**. La partición es 210/70/70 y cada parte mantiene la proporción de clases. *Por qué:* Comparar particiones solo tiene sentido si están equilibradas.
9. **`test_pipeline_tiene_pasos_y_parametros_esperados`**. El pipeline tiene imputar → escalar → SVM y respeta kernel y C. *Por qué:* La búsqueda de hiperparámetros depende de estos nombres.
10. **`test_columna_constante_no_produce_valores_invalidos`**. La columna constante no genera valores infinitos o NaN al escalar. *Por qué:* La auditoría detectó una columna constante y se decidió conservarla.
11. **`test_entrenamiento_es_reproducible`**. Dos entrenamientos con la misma semilla dan exactamente las mismas puntuaciones. *Por qué:* Reproducibilidad exigida por el mandato.
12. **`test_metricas_acotadas_y_perfectas_con_prediccion_perfecta`**. Las seis métricas existen, están entre 0 y 1 y valen 1 con predicción perfecta. *Por qué:* Comprueba la función de métricas que alimenta la tabla del PDF.
13. **`test_particiones_guardadas_coinciden_con_el_codigo`**. El archivo particiones.csv coincide con la partición que produce el código. *Por qué:* La evidencia guardada es la que realmente se usó.
14. **`test_parametros_elegidos_son_el_mejor_rango_de_la_validacion_cruzada`**. Los parámetros guardados son los de rango 1 en la búsqueda con validación cruzada. *Por qué:* Demuestra que la elección no se hizo mirando la prueba.
15. **`test_svm_supera_al_baseline_en_prueba`**. El F1 macro del SVM en prueba supera al del baseline por más de 0.4. *Por qué:* Responde la pregunta del ejercicio con la evidencia guardada.

## Decisiones y correcciones

La auditoría detectó un duplicado que se retiró antes de separar los conjuntos. Se conservó la columna constante para mantener el esquema; StandardScaler la maneja sin dividir por cero. La aprobación permanece pendiente.
