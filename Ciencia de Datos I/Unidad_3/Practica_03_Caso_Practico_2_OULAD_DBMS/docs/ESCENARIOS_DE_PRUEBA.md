# Catálogo de escenarios de prueba

Comando:

```bash
python3 -m pytest -q
```

Resultado validado: **24 pruebas aprobadas**.

## Métricas y colección

| ID | Escenario | Resultado esperado |
| --- | --- | --- |
| MET-01 | Matriz binaria con TP, FP, TN y FN conocidos | Conteos y F1 iguales al cálculo manual |
| MET-02 | No existen predicciones positivas | Precisión, recall y F1 iguales a cero, sin división por cero |
| MET-03 | Predicción ordinal perfecta | MSE = 0 y R² = 1 |
| MET-04 | Objetivo ordinal constante | R² controlado en cero |
| TAD-01 | Registro de resultados de tareas diferentes | Filtrado correcto por `TaskType` |

## Transformación de variables

| ID | Escenario | Resultado esperado |
| --- | --- | --- |
| FEA-01 | Banda IMD `0-10%` y `90-100%` | Puntos medios 5 y 95 |
| FEA-02 | IMD faltante o texto inválido | Valor `NaN` para imputación posterior |
| FEA-03 | Clics y días activos faltantes | Conversión a cero |
| FEA-04 | Educación, edad y resultado conocidos | Códigos ordinales correctos |
| FEA-05 | Resultado final desconocido | Registro excluido del modelado |
| FEA-06 | IMD faltante después de transformar | Se conserva para el `SimpleImputer` |

## Datos y repositorio ZIP

| ID | Escenario | Resultado esperado |
| --- | --- | --- |
| DAT-01 | Dos fábricas con la misma semilla | DataFrames idénticos |
| DAT-02 | Identificadores y rangos del Experimento X | IDs únicos, notas 0-100 y días 0-29 |
| DAT-03 | CSV dentro de un subfolder ZIP | Archivo localizado por nombre final |
| DAT-04 | Tabla requerida ausente | `FileNotFoundError` descriptivo |
| DAT-05 | Interacciones dentro y fuera de 28 días | Solo se agregan las tempranas |
| DAT-06 | Ninguna interacción dentro de la ventana | DataFrame vacío con esquema válido |

## Contratos de salida

| ID | Escenario | Resultado esperado |
| --- | --- | --- |
| OUT-01 | Métricas generales | Tres algoritmos en cada una de las tres tareas |
| OUT-02 | Predicciones binarias | IDs, fuente, `y_test`, `y_pred` y modelo presentes |
| OUT-03 | Archivo F1 manual | Tres modelos, conteos no negativos y métricas 0-1 |
| OUT-04 | Importancias | Diez variables para cada combinación tarea-modelo |
| OUT-05 | Evidencias gráficas y hallazgos | Archivos existentes y no vacíos |

## Documentación HTML

| ID | Escenario | Resultado esperado |
| --- | --- | --- |
| DOC-01 | Secciones requeridas | Resumen, hipótesis, OSEMN, arquitectura, resultados, pruebas y entregables |
| DOC-02 | Enlaces e imágenes locales | Todos los destinos existen |
| DOC-03 | Privacidad de rutas | No aparecen rutas absolutas de la computadora |
