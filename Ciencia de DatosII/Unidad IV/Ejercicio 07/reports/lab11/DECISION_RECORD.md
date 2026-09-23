# Registro de decisión · Ejercicio 07

**Sistema:** Territorial Review DSS - Synthetic · **Fecha:** 23 de septiembre de 2026 · **Responsable:** Institutional Owner (Product Owner del programa territorial)

## Decisión: LIMITAR
Usar la **regla transparente** (4 o más incidentes previos o exposición mayor o igual a 0.6) solo para **ordenar revisiones humanas** en un **piloto limitado**, con apelación y monitoreo mensual. **No utilizar** el modelo de regresión logística ni el árbol.

## Evidencia
- Validación temporal (120 casos): la regla tiene el mayor recall (0.828) entre los candidatos que cumplen las compuertas.
- Prueba (160 casos): la regla alcanza recall 0.750, brecha de recall 0.011 y brecha de FPR 0.010. La regresión logística tiene recall 0.717 y brecha de recall 0.138.
- `reports/lab12/candidatos.csv`, `decision.json`.

## Incertidumbre
- Intervalo bootstrap del 95 % de la brecha de recall de la regla: 0.004 a 0.208; de FPR: 0.004 a 0.331. El extremo superior supera la tolerancia de 0.16.
- 7 de 8 celdas interseccionales (grupo × edad) tienen menos de 30 casos.
- Datos sintéticos.

## Por qué no desplegar ni «no utilizar»
Cumple las compuertas en prueba, por eso no es «no utilizar»; pero la muestra no permite afirmar que la brecha sea tolerable con confianza, por eso no es «desplegar».

## Condiciones del piloto
Revisión humana de cada caso; registro de discrepancias; monitoreo mensual de recall y brechas; ampliar la muestra hasta al menos 30 casos por celda antes de reevaluar; retiro según `withdrawal_condition` de `student_inputs/lab11_impact.yml`.
