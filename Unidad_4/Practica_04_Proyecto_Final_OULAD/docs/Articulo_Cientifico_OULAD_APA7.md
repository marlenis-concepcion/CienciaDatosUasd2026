# Predicción temprana del desempeño estudiantil mediante aprendizaje automático: análisis de OULAD y un experimento anónimo reproducible

## Presentación

**Universidad Autónoma de Santo Domingo**  
**Facultad de Ingeniería y Arquitectura**  
**Asignatura:** INF-8237-C2 Ciencia de Datos I  
**Unidad:** Unidad 4: Introducción a Machine Learning  
**Equipo:** Mccarthy Team  
**Integrantes y matrículas:** [Completar por el equipo]  
**Facilitador:** Silverio de Orbe Abad  
**Fecha:** 12 de julio de 2026

## Resumen

El objetivo de este estudio fue evaluar si variables demográficas, académicas y de interacción
temprana permiten anticipar el desempeño de estudiantes en educación virtual. Se utilizó el
Open University Learning Analytics Dataset (OULAD) y se incorporó un Experimento X sintético,
anónimo y reproducible para demostrar un escenario complementario sin divulgar información
personal. El proceso siguió OSEMN: obtención, depuración, exploración, modelado e
interpretación. Se plantearon dos hipótesis: que la interacción durante los primeros 28 días
difiere entre quienes aprueban y quienes no, y que las variables tempranas permiten predecir
resultados finales y calificaciones. Se trataron valores faltantes mediante imputación,
variables ordinales mediante mapas explícitos y variables nominales mediante codificación
one-hot. Se compararon regresión logística, bosque aleatorio y gradient boosting en tareas
dicotómicas y ordinales; para la variable continua se compararon Ridge, bosque aleatorio y
gradient boosting. La evaluación incluyó precisión macro, exhaustividad macro, F1 macro,
exactitud, ROC-AUC, error cuadrático medio y R². Además, el F1 binario se verificó manualmente
desde TP, FP, TN y FN. El proyecto exporta predicciones caso a caso e importancias de
variables. Los hallazgos deben interpretarse como apoyo académico y no como fundamento para
decisiones automáticas sin validación institucional, análisis de equidad y supervisión humana.

**Palabras clave:** analítica del aprendizaje, OULAD, predicción temprana, aprendizaje
automático, rendimiento académico

## Abstract

This study evaluated whether demographic, academic, and early-interaction variables can
anticipate student performance in virtual education. The Open University Learning Analytics
Dataset (OULAD) was used together with a synthetic, anonymous, and reproducible Experiment X
to demonstrate a complementary scenario without disclosing personal information. The workflow
followed OSEMN: obtain, scrub, explore, model, and interpret. Two hypotheses were proposed:
interaction during the first 28 days differs between students who pass and those who do not,
and early variables can predict final outcomes and assessment scores. Missing values were
handled through imputation, ordinal variables through explicit mappings, and nominal variables
through one-hot encoding. Logistic regression, random forest, and gradient boosting were
compared for binary and ordinal tasks; Ridge, random forest, and gradient boosting were
compared for the continuous target. Evaluation included macro precision, macro recall, macro
F1, accuracy, ROC-AUC, mean squared error, and R². Binary F1 was also verified manually from
TP, FP, TN, and FN. The project exports case-level predictions and feature importances.
Findings must be interpreted as academic evidence rather than a basis for automated decisions
without institutional validation, fairness analysis, and human oversight.

**Keywords:** learning analytics, OULAD, early prediction, machine learning, academic
performance

## Tabla de contenido

1. Introducción  
2. Marco de referencia  
3. Metodología  
4. Hallazgos  
5. Discusión  
6. Conclusiones  
7. Referencias  
8. Anexos

## Introducción

Los entornos virtuales de aprendizaje registran información sobre acceso a recursos,
participación, evaluaciones y trayectorias académicas. Estos registros pueden apoyar la
identificación temprana de estudiantes que necesitan acompañamiento, siempre que el análisis
respete criterios de privacidad, validez y equidad. La analítica del aprendizaje no consiste
únicamente en entrenar un algoritmo; exige definir una pregunta útil, comprender el momento en
que cada variable está disponible y evaluar si el modelo generaliza a observaciones no vistas.

Kuzilek et al. (2017) publicaron OULAD para facilitar estudios comparables sobre aprendizaje
en línea. El conjunto integra información de 32,593 estudiantes, 22 presentaciones de módulos,
resultados de evaluaciones y 10,655,280 registros diarios de interacción. Los autores señalan
que el conjunto “contains demographic data together with aggregated clickstream data”
(Kuzilek et al., 2017, sección Abstract). Esta combinación permite estudiar tanto factores
académicos como patrones de comportamiento digital.

El problema de investigación consiste en determinar si la actividad temprana, observada
durante los primeros 28 días, contiene información útil para anticipar tres resultados:
aprobación dicotómica, resultado final ordinal y promedio de evaluaciones. La ventana temprana
se definió antes de agregar las interacciones para reducir la fuga temporal. No se utilizaron
el resultado final ni el promedio de evaluaciones como predictores.

El estudio plantea dos hipótesis. H1 sostiene que la distribución de clics tempranos difiere
entre estudiantes que aprueban y quienes no aprueban. H2 sostiene que la combinación de
interacciones tempranas, antecedentes académicos y variables demográficas permite construir
modelos con desempeño superior a una referencia sin información. El objetivo general fue
desarrollar un flujo reproducible que cubriera exploración, inferencia, clasificación,
predicción ordinal y regresión, además de generar salidas auditables en CSV.

## Marco de referencia

La analítica del aprendizaje estudia datos generados por estudiantes y contextos educativos
para comprender y optimizar el aprendizaje. OULAD resulta especialmente útil porque enlaza
tablas demográficas, inscripciones, evaluaciones e interacciones VLE mediante identificadores
anónimos. Según Kuzilek et al. (2017), la anonimización eliminó identificadores privados,
generalizó cuasi-identificadores y aplicó criterios de k-anonimato. Por tanto, el conjunto
permite experimentación académica, aunque su anonimización no elimina la obligación de usarlo
responsablemente.

En aprendizaje supervisado, un modelo aprende una función a partir de ejemplos con variable
objetivo conocida. La regresión logística estima probabilidades y ofrece una referencia
interpretable para clasificación. El bosque aleatorio combina múltiples árboles construidos
sobre muestras y subconjuntos de variables; Breiman (2001) mostró que esta estrategia puede
reducir la varianza y capturar relaciones no lineales. Gradient boosting construye modelos de
forma secuencial para corregir errores previos (Friedman, 2001). En regresión, Ridge controla
la magnitud de coeficientes mediante regularización, mientras los métodos basados en árboles
modelan interacciones no lineales.

Las métricas deben corresponder al problema. En clasificación desbalanceada, la exactitud
puede ocultar errores en clases minoritarias, por lo que se complementó con precisión,
exhaustividad, F1 macro y ROC-AUC. El F1 es la media armónica entre precisión y
exhaustividad. En regresión se utilizaron MSE y R²: el primero penaliza errores grandes y el
segundo compara la variabilidad explicada con una predicción basada en la media. Pedregosa et
al. (2011) describen scikit-learn como una biblioteca que integra herramientas de
preprocesamiento, selección, entrenamiento y evaluación bajo interfaces consistentes.

## Metodología

### Diseño y fuentes de datos

El estudio fue cuantitativo, no experimental y predictivo. La fuente principal fue OULAD,
publicado bajo licencia CC BY 4.0. Se utilizaron `studentInfo.csv`, `studentVle.csv`,
`assessments.csv` y `studentAssessment.csv`. La unidad de análisis fue el registro
estudiante-módulo-presentación. El Experimento X se generó con semilla fija y variables
armonizadas; su función es demostrar cómo integrar una segunda fuente anónima, no representar
una institución real.

### Flujo OSEMN y programación

La solución se encapsuló en clases que corresponden a las etapas OSEMN. `OULADRepository`
obtiene los archivos y agrega clics; `FeatureEngineer` depura y transforma; `EDAReporter`
genera descriptiva y gráficos; `ModelLab` entrena y evalúa; y `OULADProject` coordina el flujo.
La clase `ResultRegistry`, basada en una colección de diccionario, funciona como tipo abstracto
de datos para registrar resultados por tarea y algoritmo.

La descarga y todas las salidas usan rutas relativas al folder del proyecto. El archivo
comprimido de OULAD permanece fuera del control de versiones. La tabla de interacciones,
debido a su tamaño, se procesa en bloques de 500,000 filas. Primero se filtran fechas entre el
día 0 y el día 28; después se calculan clics acumulados y días activos por estudiante.

### Variables y preparación

Los predictores numéricos fueron clics en 28 días, días activos, créditos estudiados,
intentos previos, educación ordinal, edad ordinal y punto medio del índice de privación. Los
predictores categóricos fueron género, discapacidad y módulo. La fuente de datos se conservó
para auditoría, pero no se incluyó como predictor, evitando que el modelo aprendiera a separar
OULAD del experimento sintético.

Los valores faltantes numéricos se imputaron con la mediana y los categóricos con la moda. Las
variables nominales se codificaron mediante one-hot. Educación, edad y resultado final se
mapearon respetando su orden. La aprobación se definió como `Pass` o `Distinction`; `Fail` y
`Withdrawn` formaron la clase no aprobada. El resultado ordinal se codificó de 0 a 3:
retiro, reprobado, aprobado y distinción.

### Análisis exploratorio e hipótesis

El EDA incluyó medidas de tendencia y dispersión, asimetría, curtosis, auditoría de faltantes,
histogramas, box plots, diagrama de dispersión y matriz de correlación de Spearman. H1 se
evaluó mediante Mann-Whitney U porque el conteo de clics es discreto, asimétrico y suele
contener valores extremos. Se informó el valor p y una medida de tamaño del efecto basada en
rangos. Un resultado significativo no se interpretó como causalidad.

### Modelado y evaluación

Los datos se dividieron en 75 % entrenamiento y 25 % prueba con semilla fija; las tareas de
clasificación conservaron proporciones mediante estratificación. Todo preprocesamiento se
ajustó dentro de un `Pipeline` usando solo entrenamiento. Para las variables dicotómica y
ordinal se compararon regresión logística, bosque aleatorio y gradient boosting. Para el
promedio de evaluaciones se compararon Ridge, bosque aleatorio y gradient boosting.

Las métricas binarias y ordinales fueron precisión macro, exhaustividad macro, F1 macro y
exactitud. ROC-AUC se calculó para la tarea binaria. La variable ordinal también se evaluó con
MSE y R² sobre códigos ordenados. La regresión continua se evaluó con MSE y R². En el caso
binario se calcularon TP, FP, TN y FN y se reconstruyeron manualmente precisión,
exhaustividad, F1 y exactitud. Finalmente, la importancia por permutación cuantificó cuánto
disminuye el desempeño al alterar cada predictor.

## Hallazgos

La ejecución completa integró 35,093 observaciones de OULAD y Experimento X. Para H1, la
prueba de Mann-Whitney encontró una diferencia estadísticamente significativa entre los clics
tempranos de quienes aprobaron y quienes no aprobaron, U = 223,548,383, p < .001, con un
efecto biserial por rangos de aproximadamente .455. El grupo que aprobó registró una media de
328.66 clics durante los primeros 28 días, frente a 148.31 en el grupo que no aprobó. Se
rechazó H0, pero la asociación no demuestra que aumentar clics por sí solo cause aprobación.

En la tarea dicotómica, gradient boosting obtuvo el mejor F1 macro (.719), exactitud (.719) y
ROC-AUC (.798). El bosque aleatorio logró F1 macro de .714 y ROC-AUC de .788, mientras que la
regresión logística alcanzó F1 macro de .706 y ROC-AUC de .784. La proximidad entre resultados
indica que el patrón temprano contiene señal estable, aunque el método no lineal produjo una
ventaja moderada.

La clasificación ordinal fue más difícil. El bosque aleatorio obtuvo el mayor F1 macro
(.438), pero gradient boosting alcanzó mayor exactitud (.539), menor MSE ordinal (.902) y el
único R² ordinal positivo (.062). Esta diferencia muestra por qué no conviene seleccionar un
modelo con una sola métrica: F1 favorece equilibrio entre clases, mientras el MSE ordinal
penaliza cuánto se aleja la categoría predicha de la verdadera.

Para el promedio de evaluaciones, gradient boosting fue el mejor modelo con MSE = 213.491 y
R² = .222. Ridge obtuvo MSE = 216.070 y R² = .213; el bosque aleatorio obtuvo MSE = 226.284 y
R² = .176. El poder explicativo es limitado, por lo que el modelo no sustituye la evaluación
académica. Los CSV caso a caso permiten revisar cada error y `f1_manual.csv` confirma el
cálculo desde TP, FP, TN y FN.

Las importancias por permutación identifican las variables que más contribuyen al desempeño
predictivo del mejor clasificador. Estas importancias deben interpretarse como contribución a
la predicción en esta muestra, no como efectos causales ni como justificación para intervenir
sobre atributos demográficos.

## Discusión

El proyecto responde a la consigna mediante un diseño que diferencia claramente los tipos de
objetivo. La variable dicotómica es apropiada para alertas simples; la ordinal preserva la
jerarquía entre retiro, reprobación, aprobación y distinción; la continua permite estimar el
promedio de evaluaciones. Esta separación evita aplicar una única métrica o un solo algoritmo
a problemas conceptualmente distintos.

La ventana de 28 días fortalece la utilidad práctica porque una predicción temprana puede
apoyar intervenciones durante el curso. Sin embargo, todavía existen riesgos de fuga si una
variable agregada contiene información generada después del momento de decisión. Por eso el
promedio total de evaluaciones se utiliza únicamente como objetivo de regresión. Asimismo,
`final_result` solo se utiliza para construir objetivos y nunca como predictor.

Las variables demográficas requieren cautela. Aunque pueden aumentar desempeño, también
pueden reproducir desigualdades históricas. Un modelo educativo debe auditar métricas por
subgrupos, calibración, estabilidad temporal y costo de falsos negativos. La finalidad
razonable es orientar apoyo humano, no sancionar ni excluir estudiantes. La supervisión
institucional debe incluir políticas de acceso, explicación, corrección y retiro de datos.

Entre las limitaciones se encuentran la antigüedad de OULAD, las diferencias entre módulos,
la naturaleza observacional y la simplificación del Experimento X. La mezcla de fuentes se
usa con propósito didáctico y no demuestra transportabilidad entre países o instituciones.
Una extensión recomendable consiste en entrenar por presentación temporal, validar en una
presentación posterior y comparar desempeño por módulo.

## Conclusiones

Se desarrolló un proyecto reproducible de aprendizaje automático que integra OULAD con un
experimento sintético anónimo, aplica OSEMN y cumple tres tareas predictivas. La arquitectura
POO separa obtención, transformación, exploración, modelado e interpretación. El proyecto
documenta faltantes, ordinalidad, fuga temporal, métricas y trazabilidad de predicciones.

La primera hipótesis se decide mediante Mann-Whitney U y tamaño del efecto; la segunda se
examina comparando nueve combinaciones de tarea y algoritmo sobre un conjunto de prueba. La
elección final no debe depender de una sola métrica: en alertas tempranas importan tanto F1 y
exhaustividad como ROC-AUC, estabilidad y costo de error. En regresión deben considerarse MSE
y R² conjuntamente.

El aporte principal no es declarar un algoritmo universalmente superior, sino ofrecer un
procedimiento auditable que permite reproducir hallazgos, revisar errores caso a caso e
identificar variables influyentes. Antes de un uso real se requiere validación externa,
análisis de equidad y supervisión humana.

## Referencias

Breiman, L. (2001). Random forests. *Machine Learning, 45*, 5-32.
https://doi.org/10.1023/A:1010933404324

Friedman, J. H. (2001). Greedy function approximation: A gradient boosting machine. *The
Annals of Statistics, 29*(5), 1189-1232. https://doi.org/10.1214/aos/1013203451

James, G., Witten, D., Hastie, T. y Tibshirani, R. (2021). *An introduction to statistical
learning: With applications in R* (2.ª ed.). Springer.
https://doi.org/10.1007/978-1-0716-1418-1

Kuzilek, J., Hlosta, M. y Zdrahal, Z. (2017). Open University Learning Analytics dataset.
*Scientific Data, 4*, 170171. https://doi.org/10.1038/sdata.2017.171

Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel,
M., Prettenhofer, P., Weiss, R., Dubourg, V., Vanderplas, J., Passos, A., Cournapeau, D.,
Brucher, M., Perrot, M. y Duchesnay, É. (2011). Scikit-learn: Machine learning in Python.
*Journal of Machine Learning Research, 12*, 2825-2830.

## Anexos

### Anexo A. Estructura del proyecto

Se incluyen el cuaderno Colab, el paquete `src`, pruebas, documentación y salidas CSV. Las
rutas son relativas y el archivo OULAD se descarga desde UCI.

El código, la documentación y las evidencias se encuentran en:
https://github.com/marlenis-concepcion/CienciaDatosUasd2026/tree/main/Unidad_4/Practica_04_Proyecto_Final_OULAD

El cuaderno puede abrirse directamente en Google Colab:
https://colab.research.google.com/github/marlenis-concepcion/CienciaDatosUasd2026/blob/main/Unidad_4/Practica_04_Proyecto_Final_OULAD/notebooks/Proyecto_Final_OULAD_Colab.ipynb

### Anexo B. Salidas reproducibles

Las figuras incluyen EDA, box plot, dispersión, correlación y matrices de confusión. Los CSV
incluyen métricas generales, predicciones caso a caso, F1 manual e importancias.

### Anexo C. División del trabajo colaborativo

El equipo debe completar la tabla del README con nombres, matrículas, responsabilidad,
evidencia revisada y fecha. La integración final debe ser revisada por todos los integrantes.

### Anexo D. Declaración sobre Experimento X e IA

Experimento X es sintético y no representa personas ni una institución real. Se utilizaron
herramientas de inteligencia artificial como apoyo para estructuración, programación y
revisión; el equipo es responsable de ejecutar, verificar, interpretar y aprobar la entrega.
