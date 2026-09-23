# Comparación de datasets y solicitud de aprobación

| Criterio | Ionosphere (propuesto) | Banknote Authentication |
|---|---|---|
| Fuente | UCI, dataset 52 | UCI, dataset 267 |
| Registros / predictores | 351 / 34 | 1372 / 4 |
| Problema | Clasificar retornos de radar g/b | Clasificar especímenes de billetes |
| Procedencia | Radar de Goose Bay, Labrador | Características de imágenes mediante wavelets |
| Licencia | CC BY 4.0 | CC BY 4.0 |
| Faltantes según UCI | No | No |
| Ventaja | Más dimensiones para estudiar PCA y SVM | Tamaño pequeño y descarga sencilla |
| Limitación | Pocas observaciones y contexto histórico de un radar | Solo cuatro predictores para reducción dimensional |

**Pregunta:** ¿Puede un pipeline SVM clasificar retornos de radar como buenos (`g`) o malos (`b`) y superar una predicción constante, con evaluación separada del entrenamiento?

**Decisión propuesta:** Ionosphere, por su dimensionalidad y bajo costo de experimentación. No se seleccionó por el resultado en prueba.

**Aprobación docente: PENDIENTE.** Falta registrar la confirmación real del profesor. No se ha solicitado en su nombre ni se ha inventado una aprobación.

**Fuentes y atribución:**
- Sigillito, V., Wing, S., Hutton, L., y Baker, K. (1989). Ionosphere. UCI. https://doi.org/10.24432/C5W01B · https://archive.ics.uci.edu/dataset/52/ionosphere
- Lohweg, V. (2012). Banknote Authentication. UCI. https://doi.org/10.24432/C55P57 · https://archive.ics.uci.edu/dataset/267/banknote+authentication

Fuentes consultadas el 23 de septiembre de 2026. No hay identificadores personales en las variables seleccionadas. No se afirma representatividad fuera del radar de origen ni ausencia general de sesgo.
