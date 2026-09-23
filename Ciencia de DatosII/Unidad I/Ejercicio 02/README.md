# Ejercicio 02 · Ensambles, reducción y Green AI

**Autora:** Marlenis Judith Concepción Cuevas · **Asignatura:** INF-8239-C2 · **Unidad:** I.

**Estado:** implementación ejecutable basada en el mandato compartido. Ionosphere es una propuesta **pendiente de aprobación docente**. Faltan los capítulos completos de LAB01–LAB03 para comprobar requisitos adicionales. No se debe declarar aprobación ni entrega definitiva sin esa confirmación.

## Archivos

- `notebooks/ejercicio_02.ipynb`: cuaderno ejecutado con resultados y figuras.
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

PDF: [`reports/Ejercicio_02.pdf`](reports/Ejercicio_02.pdf). Conclusión: [`reports/conclusion.md`](reports/conclusion.md).

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

## Pruebas automatizadas

15 pruebas, todas aprobadas (`python -m pytest -q tests`, resultado en `reports/pruebas.txt`).

1. **`test_pareto_descarta_dominado_y_conserva_compromiso`**. La frontera de Pareto excluye un modelo peor en todo y conserva los compromisos. *Por qué:* La decisión Green AI se basa en esta frontera.
2. **`test_decision_respeta_tolerancia_y_latencia`**. Se elige el modelo más rápido dentro de 0.02 del mejor F1. *Por qué:* Aplica la regla de decisión escrita.
3. **`test_seis_configuraciones_y_reduccion_dentro_pipeline`**. Hay seis configuraciones y el PCA está dentro del pipeline. *Por qué:* PCA fuera del pipeline filtraría información de validación.
4. **`test_evidencias_misma_particion_y_tres_repeticiones`**. Se usa la misma partición del Ejercicio 01 y cada modelo se mide tres veces. *Por qué:* Comparación justa y tiempos estables.
5. **`test_empate_exacto_no_domina`**. Dos modelos idénticos quedan ambos en la frontera. *Por qué:* Un empate no debe eliminar a ninguno.
6. **`test_modelo_mejor_en_todo_domina_al_resto`**. Un modelo mejor en F1 y en costo domina al otro. *Por qué:* Comprueba la dirección de cada objetivo (maximizar F1 y minimizar costos).
7. **`test_eleccion_ignora_modelos_fuera_de_la_frontera`**. Un modelo dominado no se elige aunque sea el más rápido. *Por qué:* La elección debe salir solo de la frontera.
8. **`test_desempate_por_tamano_y_nombre`**. Con igual F1 y latencia, gana el de menor tamaño y luego el nombre. *Por qué:* El desempate está escrito y es determinista.
9. **`test_hiperparametros_de_ensambles_y_semilla`**. Árboles, profundidad, imputación y semilla de cada ensamble son los documentados. *Por qué:* Los modelos comparados son exactamente los que describe el README.
10. **`test_pca_se_ajusta_solo_con_entrenamiento_y_retiene_95`**. El PCA aprende con 210 filas de entrenamiento y retiene al menos 95 % de la varianza con menos de 34 componentes. *Por qué:* Demuestra la reducción sin fuga.
11. **`test_varianza_acumulada_es_creciente_y_alcanza_95`**. La varianza acumulada guardada crece y llega al 95 %. *Por qué:* Valida la figura de PCA del PDF.
12. **`test_modelo_elegido_esta_en_la_frontera_y_dentro_de_tolerancia`**. El modelo de decision.json está en la frontera y dentro de la tolerancia. *Por qué:* La decisión guardada cumple su propia regla.
13. **`test_prueba_final_solo_evalua_el_modelo_elegido`**. La prueba final contiene solo el modelo elegido. *Por qué:* La prueba se usa una sola vez y después de decidir.
14. **`test_tsne_con_dos_semillas_y_confiabilidad_valida`**. t-SNE se evaluó con las semillas 42 y 73 y su confiabilidad está entre 0 y 1. *Por qué:* t-SNE cambia con la semilla; se documenta su estabilidad.
15. **`test_los_seis_modelos_guardados_cargan_y_predicen`**. Los seis modelos guardados cargan y predicen clases válidas. *Por qué:* Los artefactos del repositorio son utilizables.

