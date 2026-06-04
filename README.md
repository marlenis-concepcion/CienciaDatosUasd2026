# Unidad 2 - Manipulacion y Procesamiento de Datos

Equipo: UASDVirtual

Asignatura: INF-8237-C2 Ciencia de Datos I

Estudiante visible en plataforma: Marlenis Judith Concepcion Cuevas

## Proposito del paquete

Este folder organiza las dos actividades colaborativas de la Unidad 2:

1. Caso practico 2: CRUD/ORM nativo con MySQL Sakila, POO y estructuras de datos.
2. Caso practico 3: dataset OULAD exportado a base de datos relacional con limpieza, PK, FK, dominios completos, ETL y EDA extendido.

La entrega combina codigo, SQL, documentacion tecnica, evidencias y plantillas de informe bajo el criterio APA 7/UASD indicado para INF-8237.

## Vista HTML del proyecto

Se agrego una pagina de presentacion para explicar los casos de forma visual:

```bash
open index.html
```

Si se prefiere no abrirla desde terminal, basta con hacer doble clic sobre `index.html`.

## Estructura

```text
Unidad_2_UASDVirtual/
  README.md
  index.html
  PLAN_UNIDAD_2_UASDVIRTUAL.md
  .agents/
  docs/
  scripts/
  caso_practico_2_sakila_crud_orm/
  caso_practico_3_oulad_etl_eda/
```

## Uso de IA y agentes

Los agentes estan documentados en `.agents/`. Su funcion es acelerar el trabajo colaborativo sin reemplazar la revision humana:

- `sakila_backend_agent`: mejora el CRUD/ORM nativo y revisa POO.
- `oulad_data_agent`: revisa ETL, limpieza, modelo relacional y EDA.
- `apa_uasd_agent`: valida estructura academica, citas y anexos.
- `qa_reviewer_agent`: revisa pruebas, riesgos, ejecucion y calidad.

Toda salida generada por IA debe validarse con datos reales, evidencias de ejecucion y revision academica antes de subirla a UASD Virtual.

## Guia rapida

1. Leer `PLAN_UNIDAD_2_UASDVIRTUAL.md`.
2. Abrir `index.html` para revisar el mapa visual de los casos.
3. Configurar Sakila y ejecutar el Caso 2 con Docker o variables locales.
4. Colocar los CSV de OULAD en `caso_practico_3_oulad_etl_eda/data/raw/`.
5. Ejecutar validaciones, ETL y EDA del Caso 3.
6. Generar capturas, tablas y graficas.
7. Completar el informe integrador desde `docs/PLANTILLA_INFORME_INTEGRADOR.md`.
8. Revisar `docs/CHECKLIST_ENTREGA.md` antes de entregar.

## Comandos principales

```bash
cd Unidad_2_UASDVirtual
python3 -m venv .venv
source .venv/bin/activate
python3 -m pytest
```

Caso 2:

```bash
cd caso_practico_2_sakila_crud_orm
python3 -m pip install -r requirements.txt
./setup_run_sakila_docker.sh
```

Si Sakila ya esta configurada fuera de Docker:

```bash
cd caso_practico_2_sakila_crud_orm
export SAKILA_DB_HOST=127.0.0.1
export SAKILA_DB_PORT=3307
export SAKILA_DB_USER=root
export SAKILA_DB_PASSWORD=sakila123
export SAKILA_DB_NAME=sakila
python3 -m src.check_connection
python3 -m src.main
```

Caso 3:

```bash
cd caso_practico_3_oulad_etl_eda
python3 -m pip install -r requirements.txt
python3 -m src.main
python3 -m src.eda
```

## Insumos pendientes

- Dataset OULAD en CSV.
- Motor final para OULAD si no se usa PostgreSQL.
- Nombres, matriculas, facilitador y fecha de entrega.
