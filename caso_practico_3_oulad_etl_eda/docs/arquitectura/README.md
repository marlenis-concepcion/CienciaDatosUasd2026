# Arquitectura - Caso practico 3

## Componentes

- `sql/01_schema.sql`: tablas, PK, FK y restricciones de dominio.
- `sql/02_indexes_views.sql`: indices y vistas analiticas.
- `sql/03_quality_checks.sql`: consultas de control.
- `src/extract.py`: lectura de CSV.
- `src/transform.py`: limpieza y variables derivadas.
- `src/quality.py`: perfiles, duplicados y dominios invalidos.
- `src/load.py`: carga a PostgreSQL.
- `src/eda.py`: graficas y tablas de analisis exploratorio.

## Decision tecnica

PostgreSQL es el motor recomendado por su soporte robusto para restricciones `CHECK`, claves foraneas, vistas, indices y consultas analiticas.

