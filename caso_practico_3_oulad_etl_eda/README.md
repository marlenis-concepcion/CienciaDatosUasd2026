# Caso practico 3: OULAD ETL, EDA y modelo relacional

Equipo: UASDVirtual

Asignatura: INF-8237-C2 Ciencia de Datos I

## Objetivo

Exportar el modelo del dataset OULAD a una base de datos relacional, aplicar limpieza de datos, definir llaves primarias, llaves foraneas y dominios completos, y desarrollar un ETL con EDA extendido en Python.

## Entregables

- Modelo relacional documentado.
- Scripts SQL de creacion de tablas, PK, FK y restricciones de dominio.
- Pipeline ETL en Python.
- Notebook o script de EDA extendido.
- Evidencias de carga y consultas.
- Informe academico en formato APA 7/UASD.

## Base de datos propuesta

PostgreSQL es una buena opcion por su soporte claro para restricciones, tipos de datos, analitica SQL y portabilidad. Si el equipo ya tiene MySQL instalado por Sakila, se puede usar MySQL para reducir configuracion.

## Decision de implementacion inicial

La primera version incluida en `sql/` y `src/` esta orientada a PostgreSQL. El pipeline espera los siete CSV clasicos de OULAD dentro de `data/raw/`. Si se decide usar MySQL, habria que adaptar principalmente los scripts SQL y la funcion de carga.

## Tablas OULAD esperadas

- `courses`
- `assessments`
- `vle`
- `student_info`
- `student_registration`
- `student_assessment`
- `student_vle`

## Estructura sugerida

```text
caso_practico_3_oulad_etl_eda/
  README.md
  data/
    raw/
    processed/
  sql/
    01_schema.sql
    02_constraints.sql
    03_quality_checks.sql
  notebooks/
    01_eda_oulad.ipynb
  src/
    extract.py
    transform.py
    load.py
    quality.py
    config.py
  docs/
    informe/
    evidencias/
```

## Ejecucion sugerida

```bash
cd caso_practico_3_oulad_etl_eda
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m src.main
python -m src.eda
```

Antes de ejecutar, colocar los archivos `courses.csv`, `assessments.csv`, `studentInfo.csv`, `studentRegistration.csv`, `studentAssessment.csv`, `studentVle.csv` y `vle.csv` en `data/raw/`.

## Pruebas

Desde `Unidad_2_UASDVirtual/`:

```bash
python -m pytest caso_practico_3_oulad_etl_eda/tests
```

Las pruebas actuales validan conversion de nombres, limpieza, duplicados y dominios invalidos. Las pruebas de carga requieren PostgreSQL y datos reales.

## Limpieza y validacion

- Verificar duplicados en llaves candidatas.
- Homologar valores categoricos.
- Tratar nulos segun significado de cada columna.
- Validar rangos: fechas relativas, calificaciones, pesos de evaluaciones y conteos de clics.
- Confirmar integridad referencial antes de cargar datos finales.

## EDA extendido sugerido

- Distribucion de resultados finales.
- Relacion entre interaccion en VLE y desempeno.
- Analisis por curso, modulo, genero, region y nivel educativo.
- Comparacion de estudiantes retirados, aprobados y reprobados.
- Correlaciones entre evaluaciones, actividad y resultado final.

## Checklist APA/UASD

- Presentacion.
- Resumen.
- Abstract.
- Tabla de contenido.
- Desarrollo de 5 a 10 paginas.
- Citas narrativa, parentetica y textual directa.
- Referencias solo con fuentes citadas.
- Anexos con diagramas, capturas y resultados.
