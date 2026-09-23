# Dataset Card · Predict Students' Dropout and Academic Success

## Identificación
- **Fuente:** UCI Machine Learning Repository, dataset 697 · https://archive.ics.uci.edu/dataset/697/predict+students+dropout+and+academic+success · DOI 10.24432/C5MC89
- **Autores:** Realinho, V., Vieira Martins, M., Machado, J. y Baptista, L. (2021). Descripción: Realinho et al. (2022). *Predicting Student Dropout and Academic Success*. Data, 7(11), 146. https://doi.org/10.3390/data7110146
- **Licencia:** CC BY 4.0 (ficha de UCI)
- **Archivo:** ZIP de UCI con `data.csv` (separador `;`, UTF-8 con BOM); SHA-256 del ZIP `e90e55fd65ec462ae283ebeb2cca409319e3460ed898d8754f62fb35cc83a65d`; descargado el 23 de septiembre de 2026 con `scripts/download_data.py`. No se versiona.

## Contenido
4424 estudiantes de pregrado de una institución de educación superior de Portugal, 36 variables y `Target` con tres clases: Graduate (2209), Dropout (1421) y Enrolled (794). Sin nulos ni filas duplicadas.

## Variable objetivo usada
`abandono = 1` si `Target == "Dropout"` (32.1 %); `Graduate` y `Enrolled` son 0.

## Grupos de variables
| Grupo | Uso en el DSS |
|---|---|
| Ingreso: modo y orden de aplicación, carrera, turno, calificación previa, nota de admisión, ocupación y estudios de los padres, desplazado, necesidades especiales | Modelo |
| Económicas: deudor, matrícula al día | Modelo y regla de apoyo |
| Primer semestre: unidades acreditadas, inscritas, evaluadas, aprobadas, nota, sin evaluación | Modelo y baseline |
| Macroeconómicas: desempleo, inflación, PIB | Modelo |
| **Sensibles:** género, edad al ingreso, nacionalidad, estado civil, internacional, becario | **Solo auditoría** |
| **Segundo semestre** | **Excluidas: no se conocen en el punto de decisión** |

## Observaciones de calidad y sesgos
- Tasa de abandono de 45.1 % en hombres y 25.1 % en mujeres (`Gender`: 1 = hombre, 0 = mujer). Es una diferencia de tasa base: la paridad de selección no es un objetivo adecuado; se audita el recall.
- Edad al ingreso entre 17 y 70 años (mediana 20).
- Datos de una sola institución europea: no representan a la UASD.

## Usos prohibidos
Sanciones, exclusión, condiciones de beca o admisión, decisiones automáticas sobre personas y cualquier uso con datos reales de estudiantes sin nueva evaluación de impacto y base legal (en la República Dominicana, Ley 172-13).
