# Unidad 2 - Manipulacion y Procesamiento de Datos

Equipo: Mccarthy Team

Asignatura: INF-8237-C2 Ciencia de Datos I

## Proposito del paquete

Este folder organiza el Caso practico 2 de la Unidad 2: un CRUD/ORM nativo con MySQL Sakila, programacion orientada a objetos y estructuras de datos.

La entrega combina codigo, SQL, documentacion tecnica, evidencias y plantillas de informe bajo el criterio APA 7/UASD indicado para INF-8237.

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
```

## Uso de IA y agentes

Los agentes estan documentados en `.agents/`. Su funcion es acelerar el trabajo colaborativo sin reemplazar la revision humana:

- `sakila_backend_agent`: mejora el CRUD/ORM nativo y revisa POO.
- `apa_uasd_agent`: valida estructura academica, citas y anexos.
- `qa_reviewer_agent`: revisa pruebas, riesgos, ejecucion y calidad.

Toda salida generada por IA debe validarse con datos reales, evidencias de ejecucion y revision academica antes de subirla a UASD Virtual.

## Guia rapida

1. Leer `PLAN_UNIDAD_2_UASDVIRTUAL.md`.
2. Abrir `index.html` para ver el resumen visual del Caso 2.
3. Configurar Sakila y ejecutar el Caso 2 con Docker o variables locales.
4. Generar capturas, logs y consultas SQL.
5. Completar el informe desde `docs/PLANTILLA_INFORME_CASO_2.md`.
6. Revisar `docs/CHECKLIST_ENTREGA.md` antes de entregar.

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

## Informe APA en PDF

El informe final en PDF esta en:

```text
caso_practico_2_sakila_crud_orm/docs/informe/Informe_Caso_2_Sakila_APA_UASD.pdf
```

Para regenerarlo:

```bash
python3 scripts/generar_informe_caso2_pdf.py
```

## Vista HTML

La pagina `index.html` presenta el Caso 2, los quickstarts, entregables, evidencias y enlace al PDF.

## Insumos pendientes

- Nombres, matriculas, facilitador y fecha de entrega.
