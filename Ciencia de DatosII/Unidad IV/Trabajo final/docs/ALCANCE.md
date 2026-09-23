# Alcance · DSS de alerta temprana para tutoría universitaria

**Modalidad B · Sistema de soporte a decisiones.** Trabajo individual: baseline + 1 modelo candidato, al menos 6 pruebas, documentación, repositorio y demostración.

## Problema
Una coordinación de tutorías tiene cupos limitados al terminar el primer semestre. Debe decidir **a qué estudiantes contactar primero** y **qué tipo de apoyo ofrecer** para reducir el abandono. Hoy la selección depende de reportes informales.

## Decisor humano
Coordinación de tutorías. El sistema **propone** una lista priorizada con un tipo de apoyo y una explicación por estudiante; la coordinación **decide** a quién contactar, puede cambiar el orden y registra su decisión. El sistema nunca sanciona, excluye ni condiciona becas.

## Punto de decisión y datos permitidos
Fin del primer semestre. Solo se usan variables conocidas en ese momento: datos de ingreso y resultados del primer semestre. Las variables del segundo semestre se excluyen para evitar fuga de información del futuro. Las variables sensibles (género, edad, nacionalidad, estado civil, estudiante internacional, beca) **no entran al modelo** y se usan solo para auditar.

## Alternativas que compara el DSS
| Alternativa | Descripción |
|---|---|
| Sin priorizar | Contacto aleatorio hasta llenar los cupos (referencia) |
| **Baseline de reglas** | Prioriza a quien aprobó menos unidades del primer semestre o no está al día con la matrícula |
| **Modelo candidato** | Regresión logística con las variables permitidas; ordena por riesgo estimado |

## Priorización y apoyo
- Capacidad: 15 % de la cohorte (`configs/dss.yml`).
- Tipo de apoyo por reglas explícitas: orientación financiera si hay deuda o matrícula atrasada; tutoría académica intensiva si no aprobó unidades del primer semestre; seguimiento del tutor en los demás casos.
- Explicación: las variables que más empujan el riesgo de cada estudiante.

## Métricas de éxito
Recall a capacidad (proporción de abandonos reales que reciben tutoría), precisión a capacidad y brecha de recall entre grupos. Compuertas en `configs/dss.yml`.

## Riesgos iniciales
| Riesgo | Control |
|---|---|
| Estigmatizar a estudiantes marcados como «en riesgo» | La lista es interna; se comunica como oferta de apoyo, no como etiqueta |
| Discriminación indirecta por género o edad | Variables sensibles fuera del modelo; auditoría por grupo con tamaño mínimo |
| Fuga temporal (usar notas del 2.º semestre) | Lista explícita de variables permitidas y prueba automática |
| Sesgo de automatización | La coordinación puede reordenar y registra su decisión |
| Datos de otro país (Portugal) | No se generaliza a la UASD sin reentrenar y reevaluar |
