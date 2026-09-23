# Model Card · DSS de alerta temprana para tutoría

## Modelo y versión
Regresión logística (scikit-learn) con `class_weight="balanced"` y C = 1.0, elegido por validación cruzada de 5 pliegues (average precision) solo en entrenamiento. Pipeline: one-hot de 7 variables categóricas (mínimo 20 casos por categoría) y estandarización de 17 numéricas. 101 parámetros; 10.5 KB. Versión 1.0.0 (`models/logistica.joblib`).

## Uso previsto
Proponer a la coordinación de tutorías, al terminar el primer semestre, una lista de estudiantes a contactar con cupos limitados (15 % de la cohorte), un tipo de apoyo y una explicación. **Decide la coordinación**, que puede aceptar, modificar o rechazar cada propuesta, con registro de motivo y responsable.

## Usos fuera de alcance
Sanciones, exclusión, admisión, condiciones de beca, comunicación al estudiante de una etiqueta de «riesgo» y cualquier uso con estudiantes de la UASD sin reentrenar y sin nueva evaluación de impacto.

## Datos y partición
UCI 697 (Realinho et al., 2021; CC BY 4.0), 4424 estudiantes de Portugal. Partición estratificada 70/15/15 (semilla 42). Variables sensibles (género, edad, nacionalidad, estado civil, internacional, beca) y del segundo semestre **excluidas del modelo**.

## Métricas globales (prueba, 664 estudiantes, 100 cupos)
| Alternativa | Recall a capacidad | Precisión a capacidad | Brecha de recall por edad | Brecha por género |
|---|---|---|---|---|
| Aleatorio | 0.141 | 0.30 | — | — |
| Baseline de reglas | 0.390 | 0.83 | 0.246 | 0.021 |
| Regresión logística | 0.455 | 0.97 | 0.261 | 0.133 |
| **Logística con cupos por edad (elegida)** | **0.408** | **0.87** | **0.087** | **0.036** |

AUC de la logística: 0.916; average precision: 0.874. Recall máximo posible con 100 cupos: 0.469.

## Equidad
La tasa de abandono cambia mucho por edad (16 % en ≤ 20 años, 64 % en > 25). Con cupos globales, los jóvenes casi no entraban en la lista (recall 0.286). La mitigación reparte los cupos entre franjas de edad en proporción al abandono esperado por el propio modelo; el modelo **no** usa la edad. Se eligió en validación (brecha por edad 0.303 → 0.018) antes de mirar la prueba. Intervalo bootstrap del 95 % de la brecha en prueba: hasta 0.156 (género) y 0.194 (edad); el grupo de becarios tiene 27 abandonos (menos de 30) y no se usa para decidir.

## Decisión
**LIMITAR**: piloto con revisión humana de cada propuesta. Cumple el recall mínimo y las brechas observadas, pero el límite superior del intervalo supera la tolerancia de 0.15.

## Green AI
Entrenamiento: 0.02 s en CPU (Apple M1 Pro); inferencia: 0.004 ms por estudiante; 10.5 KB. No se justifican modelos más costosos: la logística ya está cerca del techo de recall a capacidad.

## Límites y supervisión
- Abandono «silencioso»: los abandonos no alcanzados tenían en promedio 3.4 unidades aprobadas y nota 9.0; no se detectan con señales académicas.
- Los códigos de carrera y de ingreso son de la institución portuguesa.
- Monitoreo por cohorte: recall a capacidad, brechas por grupo y proporción de decisiones modificadas por la coordinación.

## Responsable y revisión
Autora: Marlenis Judith Concepción Cuevas. Revisión al cierre de cada semestre del piloto.
