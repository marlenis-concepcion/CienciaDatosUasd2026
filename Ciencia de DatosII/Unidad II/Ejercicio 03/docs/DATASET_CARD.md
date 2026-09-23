# Dataset Card · SMS Spam Collection

## Identificación
- Nombre: SMS Spam Collection v.1
- Fuente original: UCI Machine Learning Repository, dataset 228 · https://archive.ics.uci.edu/dataset/228/sms+spam+collection · DOI https://doi.org/10.24432/C5CC84
- Responsable: Tiago A. Almeida y José María Gómez Hidalgo
- Referencia: Almeida, T. A., Gómez Hidalgo, J. M. y Yamakami, A. (2011). Contributions to the study of SMS spam filtering: New collection and results. ACM DocEng'11.
- Versión o fecha: archivo `sms+spam+collection.zip` de UCI; SHA-256 `1587ea43e58e82b14ff1f5425c88e17f8496bfcdb67a583dbff9eefaf9963ce3`; consultado el 23 de septiembre de 2026
- Licencia: CC BY 4.0 (según la ficha de UCI)
- Idioma: inglés, con abreviaturas de SMS e inglés de Singapur

## Propósito y variable objetivo
Pregunta: ¿puede un clasificador basado en TF-IDF separar SMS no deseados (`spam`) de mensajes legítimos (`ham`) con un F1 macro claramente superior a una línea base, sin que los mensajes repetidos inflen el resultado?

Variable objetivo: `label`, con dos clases. La clase de interés es `spam`.

## Diccionario de datos

| Columna | Tipo | Descripción | Valores o unidad |
|---|---|---|---|
| `id` | entero | Posición de la línea en el archivo original, empezando en 0. Solo sirve para trazabilidad; no se usa como predictor. | 0–5573 |
| `text` | texto | Contenido completo del SMS. | 2–910 caracteres |
| `label` | categórica | Clase asignada por los autores del corpus. | `ham` (4827), `spam` (747) |

## Procedimiento de obtención
`uv run python scripts/download_data.py` descarga el ZIP de UCI, comprueba su SHA-256, extrae `SMSSpamCollection` (UTF-8, separado por tabulador) y lo guarda como `data/raw/sms_spam.csv` con las columnas `id,text,label`. Si la suma no coincide, borra el archivo y termina con error. `data/` no se versiona.

## Calidad observada
Auditoría completa en `reports/auditoria.json` y `reports/auditoria.png`.
- No hay nulos ni textos vacíos.
- Desbalance: 86.6 % `ham`, 13.4 % `spam`.
- 403 duplicados exactos y 434 al normalizar (minúsculas, dígitos unificados y espacios). Hay 300 textos que se repiten; el más repetido, "Sorry, I'll call later", aparece 30 veces.
- Ningún texto normalizado tiene etiquetas contradictorias.
- El spam es más largo y uniforme (mediana de 149 caracteres) que el ham (mediana de 52).

Decisión: se eliminan los 434 duplicados normalizados **antes** de partir los datos. Quedan 5140 mensajes. Si se dejaran, una misma plantilla podría quedar en entrenamiento y en prueba, y la métrica mediría memoria en lugar de generalización.

## Población cubierta y excluida
Según el readme del corpus, combina cuatro fuentes: 425 spam extraídos del foro británico Grumbletext; 450 ham de la tesis doctoral de Caroline Tagg; 3375 ham del NUS SMS Corpus, escritos sobre todo por estudiantes de la Universidad Nacional de Singapur; y 1002 ham y 322 spam del SMS Spam Corpus v.0.1 Big. No cubre español, mensajería actual (WhatsApp, enlaces acortados, estafas bancarias recientes) ni la mayoría de países.

## Riesgos, sesgos y usos prohibidos
- La etiqueta depende de la fuente: parte del "spam" son comentarios copiados del foro y no SMS masivos (ver `reports/error_analysis.csv`). Eso introduce ruido en las etiquetas.
- El ham procede en su mayoría de un grupo demográfico concreto (estudiantes de Singapur); el modelo puede confundir otros dialectos o jergas con spam.
- Los mensajes son reales y pueden contener nombres o números de teléfono; no deben republicarse fuera del uso académico ni usarse para identificar personas.
- No debe usarse para bloquear mensajes automáticamente en un servicio real sin revisión humana ni reentrenamiento con datos actuales.
