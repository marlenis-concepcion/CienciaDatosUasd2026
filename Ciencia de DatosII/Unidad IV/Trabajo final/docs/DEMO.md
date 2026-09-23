# Guion de demostración y defensa (10 minutos)

1. **Problema (1 min).** Cupos de tutoría limitados al final del primer semestre; la coordinación decide a quién contactar.
2. **Reproducir (2 min).** `uv sync`, `uv run python scripts/download_data.py` (SHA-256), `uv run pytest -q` (35 pruebas).
3. **Evidencia (3 min).** `reports/validacion.csv` → logística elegida en validación; `reports/prueba.csv` → 0.455 de recall a capacidad frente a 0.390 del baseline; `reports/errores_perfil.csv` → abandono «silencioso».
4. **Aplicación (2 min).** `uv run streamlit run app/streamlit_app.py`: mover los cupos, activar el reparto por edad, abrir un estudiante, leer el «por qué» y registrar una decisión con motivo.
5. **Responsabilidad (2 min).** Brecha por edad 0.261 → 0.087 con cupos por edad (elegido en validación); decisión LIMITAR por el intervalo de confianza; el modelo no usa variables sensibles.

## Preguntas probables

- **¿Por qué regresión logística y no un modelo más complejo?** Está a 0.014 del techo de recall posible, entrena en centésimas de segundo y permite explicar cada caso.
- **¿Por qué no usar las notas del segundo semestre?** No existen en el momento de decidir; usarlas sería fuga del futuro.
- **¿Usar la edad para repartir cupos no es discriminar?** No entra al modelo; solo reparte un apoyo voluntario para que los jóvenes, con menor tasa de abandono, no queden fuera de la lista. Es una decisión de valores declarada y requiere validación jurídica antes de un uso real.
- **¿Qué pasa con quien abandona sin señales académicas?** El sistema no lo detecta; se propone complementar con entrevistas o encuestas de bienestar.
