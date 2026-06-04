# Runbook de ejecucion - Unidad 2

Este runbook resume los pasos operativos para correr los casos practicos y generar evidencias.

## Vista general

Abrir la pagina visual del proyecto:

```bash
cd Unidad_2_UASDVirtual
open index.html
```

## Preparacion general

```bash
cd Unidad_2_UASDVirtual
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -U pip
```

## Caso practico 2: Sakila CRUD/ORM

Desde la carpeta del caso:

Mac:

```bash
cd Unidad_2_UASDVirtual/caso_practico_2_sakila_crud_orm
chmod +x MAC_SH_QUICKSTART.sh
./MAC_SH_QUICKSTART.sh
```

Linux:

```bash
cd Unidad_2_UASDVirtual/caso_practico_2_sakila_crud_orm
chmod +x LINUX_SH_QUICKSTART.sh
./LINUX_SH_QUICKSTART.sh
```

Windows PowerShell:

```powershell
cd Unidad_2_UASDVirtual\caso_practico_2_sakila_crud_orm
.\WINDOWS_QUICKSTART.ps1
```

Script base:

```bash
cd Unidad_2_UASDVirtual/caso_practico_2_sakila_crud_orm
python3 -m pip install -r requirements.txt
chmod +x setup_run_sakila_docker.sh
./setup_run_sakila_docker.sh
```

El script realiza:

- Verificacion de Docker.
- Creacion o inicio del contenedor `sakila-mysql`.
- Importacion de Sakila cuando la base no tiene tablas.
- Exportacion de variables `SAKILA_DB_*`.
- Prueba de conexion.
- Apertura del menu CRUD/ORM.

Credenciales por defecto:

```text
Host: 127.0.0.1
Puerto: 3307
Usuario: root
Password: sakila123
Base: sakila
```

Comprobacion manual:

```bash
export SAKILA_DB_HOST=127.0.0.1
export SAKILA_DB_PORT=3307
export SAKILA_DB_USER=root
export SAKILA_DB_PASSWORD=sakila123
export SAKILA_DB_NAME=sakila
python3 -m src.check_connection
python3 -m src.main
```

Evidencias minimas:

- Conexion exitosa.
- Crear, buscar, listar, actualizar y eliminar registros de prueba.
- Metricas descriptivas de peliculas.
- Consultas SQL de `sql/01_fase_i_10_consultas.sql`.
- Restricciones de integridad de `sql/02_integridad_unique_constraints.sql`.

## Caso practico 3: OULAD ETL/EDA

Colocar los siete CSV en:

```text
caso_practico_3_oulad_etl_eda/data/raw/
```

Archivos esperados:

```text
courses.csv
assessments.csv
studentInfo.csv
studentRegistration.csv
studentAssessment.csv
studentVle.csv
vle.csv
```

Ejecutar:

```bash
cd Unidad_2_UASDVirtual/caso_practico_3_oulad_etl_eda
python3 -m pip install -r requirements.txt
python3 -m src.main
python3 -m src.eda
```

Pruebas:

```bash
cd Unidad_2_UASDVirtual
python3 -m pytest caso_practico_2_sakila_crud_orm/tests
python3 -m pytest caso_practico_3_oulad_etl_eda/tests
```

Evidencias minimas:

- CSV cargados en `data/raw/`.
- Salidas procesadas en `data/processed/`.
- Reportes o tablas de calidad.
- Consultas SQL de validacion.
- Graficas o tablas del EDA.
