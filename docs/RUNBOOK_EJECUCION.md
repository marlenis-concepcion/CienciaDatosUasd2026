# Runbook de ejecucion

## Preparacion

```bash
cd Unidad_2_UASDVirtual
python3 -m venv .venv
source .venv/bin/activate
```

Copiar `.env.example` a `.env` y completar credenciales locales. No subir `.env`.

## Caso 2: Sakila CRUD/ORM

```bash
cd caso_practico_2_sakila_crud_orm
pip install -r requirements.txt
python -m src.main
```

Requisitos:

- MySQL activo.
- Base de datos `sakila` instalada.
- Usuario con permisos sobre las tablas usadas.

## Caso 3: OULAD ETL/EDA

```bash
cd caso_practico_3_oulad_etl_eda
pip install -r requirements.txt
python -m src.main
python -m src.eda
```

Requisitos:

- Colocar los siete CSV de OULAD en `data/raw/`.
- PostgreSQL activo si se ejecuta la carga real.
- Esquema creado con `sql/01_schema.sql`.

## Pruebas

Desde `Unidad_2_UASDVirtual/`:

```bash
python -m pytest
```

Las pruebas de integracion con bases de datos reales deben marcarse como `integration`.

